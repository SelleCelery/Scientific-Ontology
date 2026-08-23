#!/usr/bin/env python3
"""Serve the Scientific Ontology navigator with explicit UTF-8 text media types."""

from __future__ import annotations

import argparse
import json
import os
import shlex
import subprocess
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
TEXT_MEDIA_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".htm": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".js": "text/javascript; charset=utf-8",
    ".mjs": "text/javascript; charset=utf-8",
    ".ts": "text/plain; charset=utf-8",
    ".md": "text/markdown; charset=utf-8",
    ".markdown": "text/markdown; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".yml": "text/yaml; charset=utf-8",
    ".yaml": "text/yaml; charset=utf-8",
    ".txt": "text/plain; charset=utf-8",
    ".xml": "application/xml; charset=utf-8",
    ".svg": "image/svg+xml; charset=utf-8",
}

ASSESSMENT_RUNNER: list[str] | None = None
ASSESSMENT_TIMEOUT_SECONDS = 180

BLOCKED_MARKERS = (
    "99_Private_Core",
    "private-core",
    "Private_Core",
)


def is_blocked_repo_path(relative: str) -> bool:
    normalized = relative.replace("\\", "/").lstrip("/")
    if any(part.startswith("000") for part in normalized.split("/")):
        return True
    return any(marker in normalized for marker in BLOCKED_MARKERS)


def exposed_markdown_paths() -> list[str]:
    paths: set[str] = set()
    index_path = ROOT / "tools" / "docs_index.json"
    graph_path = ROOT / "tools" / "docs_graph.json"
    if index_path.exists():
        data = json.loads(index_path.read_text(encoding="utf-8"))
        for doc in data.get("documents", []):
            path = str(doc.get("path") or "")
            if path.endswith(".md") and not is_blocked_repo_path(path):
                paths.add(path)
    if graph_path.exists():
        data = json.loads(graph_path.read_text(encoding="utf-8"))
        for node in data.get("nodes", []):
            if node.get("type") not in {"document", "observed_document"}:
                continue
            path = str(node.get("path") or "")
            if path.endswith(".md") and not is_blocked_repo_path(path):
                paths.add(path)
    return sorted(paths)


def strict_utf8_check() -> int:
    failures: list[str] = []
    missing: list[str] = []
    paths = exposed_markdown_paths()
    for relative in paths:
        path = ROOT / relative
        if not path.is_file():
            missing.append(relative)
            continue
        try:
            path.read_bytes().decode("utf-8", errors="strict")
        except UnicodeDecodeError as exc:
            failures.append(f"{relative}: {exc}")
    if missing:
        print(f"UTF-8 Reader check: {len(missing)} missing exposed Markdown file(s)", file=sys.stderr)
        for item in missing[:20]:
            print(f"  MISSING {item}", file=sys.stderr)
    if failures:
        print(f"UTF-8 Reader check: {len(failures)} decode failure(s)", file=sys.stderr)
        for item in failures[:20]:
            print(f"  FAIL {item}", file=sys.stderr)
    if failures or missing:
        return 1
    print(f"UTF-8 Reader check: PASS ({len(paths)} exposed Markdown files)")
    for suffix, content_type in sorted(TEXT_MEDIA_TYPES.items()):
        if "charset=utf-8" not in content_type:
            print(f"Content-Type mapping missing charset for {suffix}", file=sys.stderr)
            return 1
    print("UTF-8 Content-Type mappings: PASS")
    return 0


class Utf8NavigatorHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def _request_path_blocked(self) -> bool:
        decoded = unquote(urlparse(self.path).path).replace("\\", "/")
        parts = [part for part in decoded.split("/") if part]
        if any(part.startswith("000") for part in parts):
            return True
        if any(part in {".git", ".venv", "venv", "__pycache__"} for part in parts):
            return True
        normalized = "/".join(parts)
        return any(marker in normalized for marker in BLOCKED_MARKERS)

    def _send_json(self, payload: object, status: int = 200) -> None:
        data = (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self) -> None:
        path = unquote(urlparse(self.path).path)
        if path == "/api/assessment/runner":
            self._send_json({
                "repository_assessment_runner": {
                    "available": bool(ASSESSMENT_RUNNER),
                    "mode": "local-command" if ASSESSMENT_RUNNER else "export-import",
                }
            })
            return
        if self._request_path_blocked():
            self.send_error(404)
            return
        super().do_GET()

    def do_POST(self) -> None:
        path = unquote(urlparse(self.path).path)
        if path != "/api/assessment/run":
            self.send_error(404)
            return
        if not ASSESSMENT_RUNNER:
            self._send_json({"error": "assessment runner is not configured"}, status=503)
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            self._send_json({"error": "invalid Content-Length"}, status=400)
            return
        if length <= 0 or length > 12 * 1024 * 1024:
            self._send_json({"error": "assessment execution payload must be between 1 byte and 12 MiB"}, status=413)
            return
        try:
            raw = self.rfile.read(length)
            payload = json.loads(raw.decode("utf-8"))
            if not isinstance(payload, dict) or not isinstance(payload.get("repository_assessment_execution"), dict):
                raise ValueError("repository_assessment_execution is required")
            completed = subprocess.run(
                ASSESSMENT_RUNNER,
                input=json.dumps(payload, ensure_ascii=False),
                text=True,
                capture_output=True,
                cwd=str(ROOT),
                timeout=ASSESSMENT_TIMEOUT_SECONDS,
                check=False,
            )
            if completed.returncode != 0:
                self._send_json({
                    "error": "assessment runner failed",
                    "returncode": completed.returncode,
                    "stderr": completed.stderr[-4000:],
                }, status=502)
                return
            result = json.loads(completed.stdout)
            if not isinstance(result, dict) or not isinstance(result.get("repository_assessment_run"), dict):
                raise ValueError("runner stdout must contain repository_assessment_run JSON")
            self._send_json(result)
        except subprocess.TimeoutExpired:
            self._send_json({"error": "assessment runner timed out"}, status=504)
        except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
            self._send_json({"error": str(exc)}, status=400)
        except OSError as exc:
            self._send_json({"error": f"assessment runner could not start: {exc}"}, status=502)

    def do_HEAD(self) -> None:
        if self._request_path_blocked():
            self.send_error(404)
            return
        super().do_HEAD()

    def guess_type(self, path: str) -> str:
        parsed = urlparse(path)
        suffix = Path(unquote(parsed.path)).suffix.lower()
        if suffix in TEXT_MEDIA_TYPES:
            return TEXT_MEDIA_TYPES[suffix]
        return super().guess_type(path)

    def end_headers(self) -> None:
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()


def main() -> int:
    parser = argparse.ArgumentParser(description="Serve the Scientific Ontology browser navigator with explicit UTF-8 text types.")
    parser.add_argument("--host", default="127.0.0.1", help="Bind host (default: 127.0.0.1).")
    parser.add_argument("--port", type=int, default=8000, help="Bind port (default: 8000).")
    parser.add_argument("--check", action="store_true", help="Strict-decode all Markdown exposed by the index/graph and validate MIME mappings, then exit.")
    parser.add_argument(
        "--assessment-runner",
        default=os.environ.get("SO_ASSESSMENT_RUNNER", ""),
        help="Optional local command that reads repository_assessment_execution JSON on stdin and returns repository_assessment_run JSON on stdout.",
    )
    parser.add_argument("--assessment-timeout", type=int, default=180, help="Local assessment runner timeout in seconds (default: 180).")
    args = parser.parse_args()

    global ASSESSMENT_RUNNER, ASSESSMENT_TIMEOUT_SECONDS
    ASSESSMENT_RUNNER = shlex.split(args.assessment_runner) if args.assessment_runner.strip() else None
    ASSESSMENT_TIMEOUT_SECONDS = max(1, args.assessment_timeout)

    if args.check:
        return strict_utf8_check()

    server = ThreadingHTTPServer((args.host, args.port), Utf8NavigatorHandler)
    print(f"Scientific Ontology Public Navigator: http://{args.host}:{args.port}/navigator/")
    print(f"Scientific Ontology Developer Navigator: http://{args.host}:{args.port}/navigator/dev.html")
    print("Text resources are served with explicit charset=utf-8.")
    print(f"Repository Assessment runner: {'configured' if ASSESSMENT_RUNNER else 'not configured (export/import mode)'}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

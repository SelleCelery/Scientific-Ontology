#!/usr/bin/env python3
"""Serve the Scientific Ontology navigator with explicit UTF-8 text media types."""

from __future__ import annotations

import argparse
import json
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

    def do_GET(self) -> None:
        if self._request_path_blocked():
            self.send_error(404)
            return
        super().do_GET()

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
    args = parser.parse_args()

    if args.check:
        return strict_utf8_check()

    server = ThreadingHTTPServer((args.host, args.port), Utf8NavigatorHandler)
    print(f"Scientific Ontology Navigator: http://{args.host}:{args.port}/navigator/")
    print("Text resources are served with explicit charset=utf-8.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

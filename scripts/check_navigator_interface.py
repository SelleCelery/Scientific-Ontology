#!/usr/bin/env python3
"""Validate the DN-5.4A public/developer Navigator interface boundary."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_CONTENT = ROOT / "navigator" / "public-content.json"
PUBLIC_HTML = ROOT / "navigator" / "index.html"
DEV_HTML = ROOT / "navigator" / "dev.html"
APP_SOURCE = ROOT / "navigator" / "src" / "app.ts"
GRAPH = ROOT / "tools" / "docs_graph.json"

BLOCKED_MARKERS = ("99_Private_Core", "private-core", "Private_Core", "/Gate", "/U5")


def fail(message: str) -> int:
    print(f"NAVIGATOR INTERFACE CHECK FAIL: {message}", file=sys.stderr)
    return 1


def main() -> int:
    for path in (PUBLIC_CONTENT, PUBLIC_HTML, DEV_HTML, APP_SOURCE, GRAPH):
        if not path.is_file():
            return fail(f"missing {path.relative_to(ROOT)}")
        try:
            path.read_bytes().decode("utf-8", errors="strict")
        except UnicodeDecodeError as exc:
            return fail(f"{path.relative_to(ROOT)} is not strict UTF-8: {exc}")

    data = json.loads(PUBLIC_CONTENT.read_text(encoding="utf-8"))
    if data.get("schema_version") != "0.1":
        return fail("navigator/public-content.json schema_version must be 0.1")

    layers = data.get("layers") or []
    guides = data.get("guides") or []
    if not isinstance(layers, list) or not layers:
        return fail("public-content layers must be a non-empty list")
    if not isinstance(guides, list) or not guides:
        return fail("public-content guides must be a non-empty list")

    layer_ids: set[str] = set()
    configured_paths: list[str] = []
    for layer in layers:
        layer_id = str(layer.get("id") or "")
        if not layer_id or layer_id in layer_ids:
            return fail(f"invalid/duplicate layer id: {layer_id!r}")
        layer_ids.add(layer_id)
        readme = str(layer.get("readme_path") or "")
        if not readme:
            return fail(f"layer {layer_id} missing readme_path")
        configured_paths.append(readme)

    guide_ids: set[str] = set()
    for guide in guides:
        guide_id = str(guide.get("id") or "")
        if not guide_id or guide_id in guide_ids:
            return fail(f"invalid/duplicate guide id: {guide_id!r}")
        guide_ids.add(guide_id)
        path_value = guide.get("path")
        if isinstance(path_value, dict):
            paths = [str(value or "") for value in path_value.values() if str(value or "")]
        else:
            paths = [str(path_value or "")] if str(path_value or "") else []
        if not paths:
            return fail(f"guide {guide_id} missing path")
        configured_paths.extend(paths)

    graph = json.loads(GRAPH.read_text(encoding="utf-8"))
    exposed = {
        str(node.get("path") or "")
        for node in graph.get("nodes", [])
        if node.get("type") in {"document", "observed_document"}
    }
    for relative in configured_paths:
        normalized = relative.replace("\\", "/")
        if any(part.startswith("000") for part in normalized.split("/")):
            return fail(f"public-content references pending/local path: {relative}")
        if any(marker in normalized for marker in BLOCKED_MARKERS):
            return fail(f"public-content references blocked path: {relative}")
        if not (ROOT / relative).is_file():
            return fail(f"public-content path does not exist: {relative}")
        if relative.endswith(".md") and relative not in exposed:
            return fail(f"public-content Markdown is outside Reader graph boundary: {relative}")

    public_html = PUBLIC_HTML.read_text(encoding="utf-8")
    dev_html = DEV_HTML.read_text(encoding="utf-8")
    app_source = APP_SOURCE.read_text(encoding="utf-8")
    if 'data-interface="public"' not in public_html:
        return fail("navigator/index.html must declare data-interface=public")
    if 'data-interface="developer"' not in dev_html:
        return fail("navigator/dev.html must declare data-interface=developer")
    for marker in ("Candidate review", "Data audit", "docs_registration_candidates"):
        if marker in public_html:
            return fail(f"public shell exposes developer marker: {marker}")
    required_source_fragments = (
        'document.body.dataset.interface === "developer"',
        'isDeveloper()\n      ? fetch(CANDIDATES_URL)',
        'fetch(PUBLIC_CONTENT_URL)',
    )
    for fragment in required_source_fragments:
        if fragment not in app_source:
            return fail(f"runtime boundary fragment missing from app.ts: {fragment}")

    print(
        "NAVIGATOR INTERFACE CHECK PASS: "
        f"{len(layers)} public layers, {len(guides)} guide entrances, public/developer shells separated"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

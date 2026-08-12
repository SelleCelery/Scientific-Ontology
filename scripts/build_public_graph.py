#!/usr/bin/env python3
"""Build the sanitized graph read model used by the Public Navigator.

The canonical graph keeps source hashes and diagnostics for repository/developer audit.
The public graph projects only graph semantics needed by the reader-facing UI.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / "tools" / "docs_graph.json"
PUBLIC = ROOT / "tools" / "docs_public_graph.json"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def public_projection(graph: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": graph.get("schema_version"),
        "public_graph_contract_version": "1.0",
        "principles": graph.get("principles", []),
        "relation_types": graph.get("relation_types", {}),
        "nodes": graph.get("nodes", []),
        "edges": graph.get("edges", []),
    }


def encoded(payload: dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=False) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Build Public Navigator graph projection.")
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--check", action="store_true", help="Verify the generated public graph is current.")
    args = parser.parse_args()

    root = args.root.resolve()
    canonical = root / "tools" / "docs_graph.json"
    public = root / "tools" / "docs_public_graph.json"

    graph = load_json(canonical)
    payload = public_projection(graph)
    text = encoded(payload)

    if args.check:
        if not public.exists():
            print("PUBLIC GRAPH CHECK FAILED: tools/docs_public_graph.json is missing")
            return 1
        current = public.read_text(encoding="utf-8")
        if current != text:
            print("PUBLIC GRAPH CHECK FAILED: tools/docs_public_graph.json is stale")
            return 1
        if "source" in payload or "diagnostics" in payload:
            print("PUBLIC GRAPH CHECK FAILED: developer-only top-level data is present")
            return 1
        print(
            "PUBLIC GRAPH CHECK PASS: "
            f"{len(payload.get('nodes', []))} nodes / {len(payload.get('edges', []))} edges; "
            "source hashes and diagnostics removed"
        )
        return 0

    public.write_text(text, encoding="utf-8", newline="\n")
    print(
        f"WROTE {public.relative_to(root)}: "
        f"{len(payload.get('nodes', []))} nodes / {len(payload.get('edges', []))} edges"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

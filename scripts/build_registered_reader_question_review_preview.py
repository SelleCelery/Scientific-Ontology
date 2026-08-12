#!/usr/bin/env python3
"""Build a developer-only JSON read model for registered reader-question revision proposals."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "tools" / "docs_registered_reader_question_review.yml"
OUTPUT = ROOT / "tools" / "docs_registered_reader_question_review.preview.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description="Build registered reader-question revision seed JSON for Developer Navigator.")
    parser.add_argument("--root", default=str(ROOT))
    parser.add_argument("--source", default="tools/docs_registered_reader_question_review.yml")
    parser.add_argument("--output", default="tools/docs_registered_reader_question_review.preview.json")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    source_path = root / args.source
    output_path = root / args.output
    try:
        raw = source_path.read_bytes()
        data = yaml.safe_load(raw.decode("utf-8", errors="strict")) or {}
        payload = data.get("registered_reader_question_review") if isinstance(data, dict) else None
        if not isinstance(payload, dict):
            raise ValueError("registered_reader_question_review root object is required")
        if payload.get("schema_version") != "0.1":
            raise ValueError("registered reader-question review schema_version must be 0.1")
        source = payload.get("source") if isinstance(payload.get("source"), dict) else {}
        manifest_path = root / str(source.get("manifest_path") or "tools/docs_manifest.yml")
        index_path = root / str(source.get("index_path") or "tools/docs_index.json")
        if sha256(manifest_path) != str(source.get("manifest_sha256") or ""):
            raise ValueError("registered review seed manifest hash is stale")
        if sha256(index_path) != str(source.get("index_sha256") or ""):
            raise ValueError("registered review seed index hash is stale")
        docs = payload.get("documents")
        if not isinstance(docs, list):
            raise ValueError("documents must be an array")
        seen: set[str] = set()
        for item in docs:
            if not isinstance(item, dict):
                raise ValueError("registered review document must be an object")
            path = str(item.get("path") or "")
            if not path or path in seen:
                raise ValueError(f"duplicate/empty registered review path: {path}")
            seen.add(path)
            if not (root / path).is_file():
                raise ValueError(f"registered review path does not exist: {path}")
        output_data = json.loads(json.dumps(data, ensure_ascii=False))
        output_payload = output_data["registered_reader_question_review"]
        output_payload.setdefault("source", {})["review_seed_sha256"] = hashlib.sha256(raw).hexdigest()
        output_payload["source"]["preview_contract"] = "developer-only revision seed; not canonical manifest"
        generated = (json.dumps(output_data, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    except Exception as exc:
        print(f"REGISTERED REVIEW PREVIEW BUILD FAILED: {exc}", file=sys.stderr)
        return 1
    if args.check:
        if not output_path.is_file():
            print(f"REGISTERED REVIEW PREVIEW CHECK FAILED: missing {output_path.relative_to(root)}", file=sys.stderr)
            return 1
        if output_path.read_bytes() != generated:
            print("REGISTERED REVIEW PREVIEW CHECK FAILED: generated preview is stale", file=sys.stderr)
            return 1
        print(f"REGISTERED REVIEW PREVIEW CHECK PASS: {len(docs)} registered revision proposals")
        return 0
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(generated.decode("utf-8"))
    print(f"REGISTERED REVIEW PREVIEW BUILT: {output_path.relative_to(root)} ({len(docs)} proposals)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

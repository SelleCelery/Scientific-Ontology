#!/usr/bin/env python3
"""Dry-run or apply accepted DN-5.4B registration review decisions to docs_manifest.yml.

Safety contract:
- stale review files are rejected;
- hold/reject decisions do not change the manifest;
- concept_ownership and logical_contract are never inferred from candidate data;
- default mode is dry-run;
- --output writes a reviewed manifest copy;
- --apply overwrites the canonical manifest only after validation.
"""
from __future__ import annotations

import argparse
import copy
import json
import sys
import tempfile
from pathlib import Path
from typing import Any

from ruamel.yaml import YAML

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "tools" / "docs_manifest.yml"

sys.path.insert(0, str(ROOT / "scripts"))
import validate_registration_review as review_validator  # noqa: E402
import build_docs_index  # noqa: E402
import build_docs_graph  # noqa: E402

FIELDS = (
    "path", "document_type", "title_ja", "title_en", "layer", "status", "scope", "public_profile",
    "state", "role_ja", "role_en", "doc_id", "language_relation", "discovery",
)


def clean_manifest_entry(proposed: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for field in FIELDS:
        value = proposed.get(field)
        if value is None or value == "" or value == [] or value == {}:
            continue
        result[field] = copy.deepcopy(value)
    return result


def load_roundtrip(path: Path):
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.width = 110
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.load(handle)
    return yaml, data


def apply_review(manifest: Any, review: dict[str, Any]) -> tuple[list[str], list[str]]:
    docs = manifest.get("documents")
    if not isinstance(docs, list):
        raise ValueError("docs_manifest.yml documents must be a list")
    by_path = {str(item.get("path") or ""): item for item in docs if isinstance(item, dict)}
    added: list[str] = []
    updated: list[str] = []
    payload = review["registration_review"]
    for decision in payload.get("decisions", []):
        if decision.get("decision") not in {"approve", "approve_with_edits"}:
            continue
        proposed = clean_manifest_entry(decision.get("after") or {})
        path = str(proposed.get("path") or decision.get("path") or "")
        proposed["path"] = path
        if path in by_path:
            target = by_path[path]
            for key, value in proposed.items():
                target[key] = value
            updated.append(path)
        else:
            docs.append(proposed)
            by_path[path] = proposed
            added.append(path)
    for manual in payload.get("manual_candidates", []):
        if manual.get("decision") != "approve":
            continue
        proposed = clean_manifest_entry(manual.get("proposed") or {})
        path = str(proposed.get("path") or "")
        if not path:
            continue
        if path in by_path:
            raise ValueError(f"manual candidate path already registered: {path}")
        docs.append(proposed)
        by_path[path] = proposed
        added.append(path)
    for revision in payload.get("revision_candidates", []):
        if revision.get("decision") != "approve":
            continue
        after = revision.get("after")
        if not isinstance(after, dict) or not after:
            continue
        path = str(revision.get("path") or after.get("path") or "")
        if path not in by_path:
            raise ValueError(f"revision candidate path is not currently registered: {path}")
        target = by_path[path]
        for key, value in clean_manifest_entry(after).items():
            target[key] = value
        updated.append(path)
    return added, updated




def validate_proposed_manifest(yaml: YAML, manifest: Any) -> None:
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", newline="\n", suffix=".yml", delete=False) as handle:
        temp_path = Path(handle.name)
        yaml.dump(manifest, handle)
    try:
        index = build_docs_index.compile_index(ROOT, temp_path, ROOT / "tools" / "docs_search.yml", "preview")
        build_docs_index.validate_index(index)
        graph = build_docs_graph.build_graph(ROOT, temp_path, ROOT / "tools" / "docs_search.yml", ROOT / "tools" / "docs_graph.yml", "preview")
        build_docs_graph.validate_graph(graph)
    finally:
        temp_path.unlink(missing_ok=True)

def main() -> int:
    parser = argparse.ArgumentParser(description="Dry-run/apply a validated registration-review transaction.")
    parser.add_argument("review", help="Exported docs registration review JSON")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--output", help="Write a reviewed manifest copy instead of changing canonical manifest")
    group.add_argument("--apply", action="store_true", help="Overwrite tools/docs_manifest.yml explicitly")
    args = parser.parse_args()
    review_path = Path(args.review)
    try:
        review = review_validator.load_json(review_path)
        errors = review_validator.validate(review)
        if errors:
            print("REGISTRATION REVIEW APPLY BLOCKED", file=sys.stderr)
            for error in errors: print(f"ERROR {error}", file=sys.stderr)
            return 1
        yaml, manifest = load_roundtrip(MANIFEST)
        added, updated = apply_review(manifest, review)
        validate_proposed_manifest(yaml, manifest)
    except Exception as exc:
        print(f"REGISTRATION REVIEW APPLY FAILED: {exc}", file=sys.stderr)
        return 1
    payload = review["registration_review"]
    counts: dict[str, int] = {}
    for item in payload.get("decisions", []):
        counts[item["decision"]] = counts.get(item["decision"], 0) + 1
    print("REGISTRATION REVIEW DRY RUN" if not args.output and not args.apply else "REGISTRATION REVIEW APPLY PLAN")
    print(f"  decisions: {counts}")
    print(f"  manifest additions: {len(added)}")
    print(f"  manifest updates: {len(set(updated))}")
    print("  concept ownership changes: 0 (not inferred)")
    print("  typed relation changes: 0 (not inferred)")
    print("  proposed index/graph structural validation: PASS")
    for path in added[:20]: print(f"  ADD {path}")
    for path in sorted(set(updated))[:20]: print(f"  UPDATE {path}")
    if not args.output and not args.apply:
        print("No files written. Use --output <path> for a reviewed copy or --apply for the canonical manifest.")
        return 0
    target = MANIFEST if args.apply else Path(args.output)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8", newline="\n") as handle:
        yaml.dump(manifest, handle)
    print(f"WROTE {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

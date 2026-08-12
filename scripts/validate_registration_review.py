#!/usr/bin/env python3
"""Validate an exported DN-5.4B registration-review transaction.

The review file is a human judgment transaction, not the canonical manifest.
Validation refuses stale candidate sets by default.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
CANDIDATES = ROOT / "tools" / "docs_registration_candidates.yml"
MANIFEST = ROOT / "tools" / "docs_manifest.yml"
GRAPH = ROOT / "tools" / "docs_graph.json"
REGISTERED_REVIEW_SEED = ROOT / "tools" / "docs_registered_reader_question_review.yml"
DECISIONS = {"approve", "approve_with_edits", "hold", "reject"}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("review root must be an object")
    return data


def candidate_payload() -> dict[str, Any]:
    data = yaml.safe_load(CANDIDATES.read_text(encoding="utf-8"))
    payload = data.get("registration_candidates") if isinstance(data, dict) else None
    if not isinstance(payload, dict):
        raise ValueError("candidate ledger missing registration_candidates root")
    return payload


def registered_review_seed_payload() -> dict[str, Any]:
    data = yaml.safe_load(REGISTERED_REVIEW_SEED.read_text(encoding="utf-8"))
    payload = data.get("registered_reader_question_review") if isinstance(data, dict) else None
    if not isinstance(payload, dict):
        raise ValueError("registered review seed missing registered_reader_question_review root")
    return payload


def validate(data: dict[str, Any], *, allow_stale: bool = False) -> list[str]:
    errors: list[str] = []
    payload = data.get("registration_review")
    if not isinstance(payload, dict):
        return ["registration_review root object is required"]
    schema_version = str(payload.get("schema_version") or "")
    if schema_version not in {"0.1", "0.2"}:
        errors.append("schema_version must be 0.1 or 0.2")
    if payload.get("status") not in {"in_progress", "complete"}:
        errors.append("status must be in_progress or complete")
    source = payload.get("source")
    if not isinstance(source, dict):
        errors.append("source object is required")
        source = {}
    if not allow_stale:
        expected = {
            "candidate_source_sha256": sha256(CANDIDATES),
            "manifest_sha256": sha256(MANIFEST),
            "graph_sha256": sha256(GRAPH),
        }
        if schema_version == "0.2":
            expected["registered_review_seed_sha256"] = sha256(REGISTERED_REVIEW_SEED)
        for key, current in expected.items():
            if str(source.get(key) or "") != current:
                errors.append(f"stale source: {key} review={source.get(key)!r} current={current}")
    ledger = candidate_payload()
    candidates = {str(c.get("path") or ""): c for c in ledger.get("candidates", []) if isinstance(c, dict)}
    registered_seed = registered_review_seed_payload() if REGISTERED_REVIEW_SEED.is_file() else {"documents": []}
    seeded_revisions = {
        str(item.get("path") or ""): item
        for item in registered_seed.get("documents", [])
        if isinstance(item, dict) and str(item.get("path") or "")
    }
    if schema_version == "0.2":
        if int(source.get("registered_review_seed_count") or -1) != len(seeded_revisions):
            errors.append(
                "registered_review_seed_count does not match current registered review seed: "
                f"review={source.get('registered_review_seed_count')!r} current={len(seeded_revisions)}"
            )
    decisions = payload.get("decisions")
    if not isinstance(decisions, list):
        errors.append("decisions must be an array")
        decisions = []
    seen: set[str] = set()
    for idx, item in enumerate(decisions):
        if not isinstance(item, dict):
            errors.append(f"decisions[{idx}] must be an object")
            continue
        path = str(item.get("path") or "")
        decision = str(item.get("decision") or "")
        if not path:
            errors.append(f"decisions[{idx}] missing path")
        elif path in seen:
            errors.append(f"duplicate decision path: {path}")
        seen.add(path)
        if path and path not in candidates:
            errors.append(f"decision does not match current candidate ledger: {path}")
        if decision not in DECISIONS:
            errors.append(f"invalid decision for {path or idx}: {decision}")
        before = item.get("before")
        after = item.get("after")
        if not isinstance(before, dict) or not isinstance(after, dict):
            errors.append(f"decision before/after must be objects: {path or idx}")
        if path in candidates:
            current = candidates[path].get("proposed") or {}
            if isinstance(before, dict) and before != current:
                errors.append(f"candidate baseline changed: {path}")
        if decision == "approve" and before != after:
            errors.append(f"approve must not contain edits: {path}")
        if decision == "approve_with_edits" and before == after:
            errors.append(f"approve_with_edits has no actual edit: {path}")
    manual_candidates = payload.get("manual_candidates")
    if not isinstance(manual_candidates, list):
        errors.append("manual_candidates must be an array")
        manual_candidates = []
    registered_paths: set[str] = set()
    try:
        manifest = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
        registered_paths = {str(item.get("path") or "") for item in (manifest.get("documents") or []) if isinstance(item, dict)}
    except Exception as exc:
        errors.append(f"cannot inspect manifest documents for manual/revision validation: {exc}")
    manual_paths: set[str] = set()
    for idx, item in enumerate(manual_candidates):
        if not isinstance(item, dict):
            errors.append(f"manual_candidates[{idx}] must be an object")
            continue
        proposed = item.get("proposed")
        if not isinstance(proposed, dict):
            errors.append(f"manual_candidates[{idx}].proposed must be an object")
            continue
        path = str(proposed.get("path") or "")
        doc_id = str(proposed.get("doc_id") or "")
        if item.get("decision") not in {"approve", "hold", "reject"}:
            errors.append(f"manual candidate has invalid decision: {path or idx}")
        if not path or not doc_id:
            errors.append(f"manual candidate requires path and doc_id: index {idx}")
        if path in registered_paths:
            errors.append(f"manual candidate path is already registered; use revision queue instead: {path}")
        if path in manual_paths:
            errors.append(f"duplicate manual candidate path: {path}")
        manual_paths.add(path)
        if path and not (ROOT / path).is_file():
            errors.append(f"manual candidate path does not exist: {path}")
    revision_candidates = payload.get("revision_candidates")
    if not isinstance(revision_candidates, list):
        errors.append("revision_candidates must be an array")
        revision_candidates = []
    revision_paths: set[str] = set()
    for idx, item in enumerate(revision_candidates):
        if not isinstance(item, dict):
            errors.append(f"revision_candidates[{idx}] must be an object")
            continue
        path = str(item.get("path") or "")
        if item.get("decision") not in {"approve", "hold", "reject"}:
            errors.append(f"revision candidate has invalid decision: {path or idx}")
        if not path or path not in registered_paths:
            errors.append(f"revision candidate must reference a registered path: {path or idx}")
        if path in revision_paths:
            errors.append(f"duplicate revision candidate path: {path}")
        revision_paths.add(path)
        if not isinstance(item.get("before"), dict):
            errors.append(f"revision candidate requires before snapshot: {path or idx}")
        after = item.get("after")
        if after is not None and not isinstance(after, dict):
            errors.append(f"revision candidate after must be an object when present: {path or idx}")
        if item.get("source_kind") == "registered_reader_question_seed":
            if path not in seeded_revisions:
                errors.append(f"seeded revision path is not in current registered review seed: {path or idx}")
            seed_hash = str(item.get("seed_source_sha256") or "")
            current_seed_hash = sha256(REGISTERED_REVIEW_SEED)
            if seed_hash != current_seed_hash:
                errors.append(f"seeded revision source hash is stale: {path or idx}")
    return errors


def self_test() -> int:
    ledger = candidate_payload()
    first = ledger["candidates"][0]
    proposed = first["proposed"]
    data = {
        "registration_review": {
            "schema_version": "0.2",
            "status": "in_progress",
            "source": {
                "candidate_source_sha256": sha256(CANDIDATES),
                "manifest_sha256": sha256(MANIFEST),
                "graph_sha256": sha256(GRAPH),
                "candidate_count": len(ledger.get("candidates", [])),
                "registered_review_seed_sha256": sha256(REGISTERED_REVIEW_SEED),
                "registered_review_seed_count": len(registered_review_seed_payload().get("documents", [])),
            },
            "decisions": [{
                "path": first["path"], "doc_id": proposed.get("doc_id", ""), "decision": "approve",
                "reviewed_at": "self-test", "reviewer_note": "", "before": proposed, "after": proposed,
            }],
            "manual_candidates": [], "revision_candidates": [],
        }
    }
    errors = validate(data)
    if errors:
        for error in errors: print(f"ERROR {error}", file=sys.stderr)
        return 1
    print("REGISTRATION REVIEW SELF-TEST PASS")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a Navigator registration-review export.")
    parser.add_argument("review", nargs="?", help="Path to exported review JSON.")
    parser.add_argument("--allow-stale", action="store_true", help="Validate structure without current-source hash equality.")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    if not args.review:
        parser.error("review path is required unless --self-test is used")
    try:
        data = load_json(Path(args.review))
        errors = validate(data, allow_stale=args.allow_stale)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, yaml.YAMLError, ValueError) as exc:
        print(f"REGISTRATION REVIEW CHECK FAILED: {exc}", file=sys.stderr)
        return 1
    if errors:
        print(f"REGISTRATION REVIEW CHECK FAILED: {len(errors)} issue(s)", file=sys.stderr)
        for error in errors: print(f"ERROR {error}", file=sys.stderr)
        return 1
    payload = data["registration_review"]
    counts: dict[str, int] = {}
    for item in payload.get("decisions", []):
        counts[item["decision"]] = counts.get(item["decision"], 0) + 1
    print(f"REGISTRATION REVIEW CHECK PASS: {len(payload.get('decisions', []))} decisions, {counts}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

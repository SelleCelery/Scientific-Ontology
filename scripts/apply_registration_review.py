#!/usr/bin/env python3
"""Dry-run or explicitly apply a validated registration-review transaction.

Safety contract:
- stale review files are rejected;
- browser review never writes the manifest directly;
- approved provisional reviews promote registration_state to registered;
- hold/reject decisions do not delete or mutate current public entries;
- concept_ownership and typed logical relations are never inferred here;
- default mode is dry-run;
- --output writes a reviewed manifest copy;
- --apply overwrites the canonical manifest only after validation.
"""
from __future__ import annotations

import argparse
import copy
import os
import sys
import tempfile
from pathlib import Path
from typing import Any

from ruamel.yaml import YAML

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "tools" / "docs_manifest.yml"
REVISION_PROPOSALS = ROOT / "tools" / "docs_revision_proposals.yml"

sys.path.insert(0, str(ROOT / "scripts"))
import validate_registration_review as review_validator  # noqa: E402
import build_docs_index  # noqa: E402
import build_docs_graph  # noqa: E402

FIELDS = (
    "path",
    "document_type",
    "title_ja",
    "title_en",
    "layer",
    "status",
    "scope",
    "public_profile",
    "state",
    "registration_state",
    "role_ja",
    "role_en",
    "doc_id",
    "language_relation",
    "document_role",
    "catalog_document",
    "assessment",
    "discovery",
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


def apply_review(manifest: Any, review: dict[str, Any]) -> tuple[list[str], list[str], list[str]]:
    docs = manifest.get("documents")
    if not isinstance(docs, list):
        raise ValueError("docs_manifest.yml documents must be a list")
    by_path = {str(item.get("path") or ""): item for item in docs if isinstance(item, dict)}
    added: list[str] = []
    promoted: list[str] = []
    updated: list[str] = []
    payload = review["registration_review"]

    for decision in payload.get("decisions", []):
        if decision.get("decision") not in {"approve", "approve_with_edits"}:
            continue
        path = str(decision.get("path") or "")
        if path not in by_path:
            raise ValueError(f"approved provisional path is not in manifest: {path}")
        target = by_path[path]
        if str(target.get("registration_state") or "") != "provisional":
            raise ValueError(f"approved provisional path is no longer provisional: {path}")
        proposed = clean_manifest_entry(decision.get("after") or {})
        proposed["path"] = path
        proposed["registration_state"] = "registered"
        for key, value in proposed.items():
            target[key] = value
        promoted.append(path)

    for manual in payload.get("manual_candidates", []):
        if manual.get("decision") != "approve":
            continue
        proposed = clean_manifest_entry(manual.get("proposed") or {})
        path = str(proposed.get("path") or "")
        if not path:
            continue
        if path in by_path:
            raise ValueError(f"manual candidate path already registered: {path}")
        proposed["registration_state"] = "registered"
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
        if str(target.get("registration_state") or "") != "registered":
            raise ValueError(f"revision candidate target is not registered: {path}")
        proposed = clean_manifest_entry(after)
        proposed["path"] = path
        proposed["registration_state"] = "registered"
        for key, value in proposed.items():
            target[key] = value
        updated.append(path)
    return added, promoted, updated



def reconcile_revision_proposals(source: Any, review: dict[str, Any]) -> list[str]:
    payload = source.get("revision_proposals")
    if not isinstance(payload, dict):
        raise ValueError("docs_revision_proposals.yml requires revision_proposals object")
    proposals = payload.get("proposals")
    if not isinstance(proposals, list):
        raise ValueError("docs_revision_proposals.yml revision_proposals.proposals must be a list")
    consumed = {
        str(item.get("proposal_id") or "")
        for item in review["registration_review"].get("revision_candidates", [])
        if item.get("source_kind") == "revision_proposal"
        and item.get("decision") in {"approve", "reject"}
        and str(item.get("proposal_id") or "")
    }
    if not consumed:
        return []
    existing = {str(item.get("proposal_id") or "") for item in proposals if isinstance(item, dict)}
    missing = sorted(consumed - existing)
    if missing:
        raise ValueError(f"resolved revision proposal id(s) no longer exist: {missing}")
    payload["proposals"] = [
        item for item in proposals
        if not isinstance(item, dict) or str(item.get("proposal_id") or "") not in consumed
    ]
    payload["status"] = "active" if payload["proposals"] else "empty"
    return sorted(consumed)


def yaml_bytes(yaml: YAML, data: Any) -> bytes:
    from io import StringIO

    buffer = StringIO()
    yaml.dump(data, buffer)
    rendered = buffer.getvalue()
    normalized = "\n".join(line.rstrip() for line in rendered.splitlines()) + "\n"
    if yaml.load(normalized) != data:
        raise ValueError("Whitespace normalization would alter manifest data")
    return normalized.encode("utf-8")


def write_with_rollback(files: list[tuple[Path, bytes]]) -> None:
    originals = {path: path.read_bytes() if path.exists() else None for path, _ in files}
    temps: list[tuple[Path, Path]] = []
    replaced: list[Path] = []
    try:
        for path, content in files:
            path.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.NamedTemporaryFile("wb", dir=path.parent, prefix=f".{path.name}.", suffix=".tmp", delete=False) as handle:
                handle.write(content)
                temp_path = Path(handle.name)
            temps.append((path, temp_path))
        for path, temp_path in temps:
            os.replace(temp_path, path)
            replaced.append(path)
    except Exception:
        for path in reversed(replaced):
            original = originals[path]
            if original is None:
                path.unlink(missing_ok=True)
            else:
                path.write_bytes(original)
        raise
    finally:
        for _, temp_path in temps:
            temp_path.unlink(missing_ok=True)

def validate_proposed_manifest(yaml: YAML, manifest: Any) -> None:
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", newline="\n", suffix=".yml", delete=False) as handle:
        temp_path = Path(handle.name)
        yaml.dump(manifest, handle)
    try:
        index = build_docs_index.compile_index(ROOT, temp_path, ROOT / "tools" / "docs_search.yml", "preview")
        build_docs_index.validate_index(index)
        graph = build_docs_graph.build_graph(
            ROOT,
            temp_path,
            ROOT / "tools" / "docs_search.yml",
            ROOT / "tools" / "docs_graph.yml",
            "preview",
        )
        build_docs_graph.validate_graph(graph)
    finally:
        temp_path.unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Dry-run/apply a validated registration-review transaction.")
    parser.add_argument("review", help="Exported docs registration review JSON")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--output", help="Write a reviewed manifest copy instead of changing canonical manifest")
    group.add_argument("--apply", action="store_true", help="Overwrite tools/docs_manifest.yml explicitly")
    parser.add_argument("--assessment-run", type=Path)
    parser.add_argument("--assessment-review", type=Path)
    args = parser.parse_args()
    review_path = Path(args.review)
    try:
        review = review_validator.load_json(review_path)
        errors = review_validator.validate(review, assessment_run=args.assessment_run, assessment_review=args.assessment_review)
        if errors:
            print("REGISTRATION REVIEW APPLY BLOCKED", file=sys.stderr)
            for error in errors:
                print(f"ERROR {error}", file=sys.stderr)
            return 1
        yaml, manifest = load_roundtrip(MANIFEST)
        proposals_yaml, proposals_source = load_roundtrip(REVISION_PROPOSALS)
        added, promoted, updated = apply_review(manifest, review)
        consumed_proposals = reconcile_revision_proposals(proposals_source, review)
        validate_proposed_manifest(yaml, manifest)
    except Exception as exc:
        print(f"REGISTRATION REVIEW APPLY FAILED: {exc}", file=sys.stderr)
        return 1

    payload = review["registration_review"]
    counts: dict[str, int] = {}
    for item in payload.get("decisions", []):
        counts[item["decision"]] = counts.get(item["decision"], 0) + 1
    print("REGISTRATION REVIEW DRY RUN" if not args.output and not args.apply else "REGISTRATION REVIEW APPLY PLAN")
    print(f"  provisional decisions: {counts}")
    print(f"  provisional -> registered: {len(promoted)}")
    print(f"  manifest additions: {len(added)}")
    print(f"  registered metadata updates: {len(set(updated))}")
    print(f"  resolved revision proposals: {len(consumed_proposals)}")
    print("  concept ownership changes: 0 (not inferred)")
    print("  typed relation changes: 0 (not inferred)")
    print("  proposed index/graph structural validation: PASS")
    for path in promoted[:20]:
        print(f"  PROMOTE {path}")
    for path in added[:20]:
        print(f"  ADD {path}")
    for path in sorted(set(updated))[:20]:
        print(f"  UPDATE {path}")
    if not args.output and not args.apply:
        print("No files written. Use --output <path> for a reviewed copy or --apply for the canonical manifest.")
        return 0
    if args.apply:
        writes = [(MANIFEST, yaml_bytes(yaml, manifest))]
        if consumed_proposals:
            writes.append((REVISION_PROPOSALS, yaml_bytes(proposals_yaml, proposals_source)))
        write_with_rollback(writes)
        print(f"WROTE {MANIFEST}")
        if consumed_proposals:
            print(f"WROTE {REVISION_PROPOSALS} (consumed {len(consumed_proposals)} resolved proposal(s))")
        return 0

    target = Path(args.output)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8", newline="\n") as handle:
        yaml.dump(manifest, handle)
    print(f"WROTE {target}")
    if consumed_proposals:
        print("NOTE: --output does not consume docs_revision_proposals.yml; only --apply reconciles the active proposal source.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

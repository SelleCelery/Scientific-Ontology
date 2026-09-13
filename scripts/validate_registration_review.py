#!/usr/bin/env python3
"""Validate an exported Developer Registration Workbench transaction.

Schema 0.3 binds provisional review directly to the current manifest and binds
registered revision proposals to the current generic proposal ledger. The browser
never writes canonical YAML; repository-side validation is required before apply.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import build_registration_workbench_preview as workbench  # noqa: E402

MANIFEST = ROOT / "tools" / "docs_manifest.yml"
GRAPH = ROOT / "tools" / "docs_graph.json"
REVISION_PROPOSALS = ROOT / "tools" / "docs_revision_proposals.yml"
DECISIONS = {"approve", "approve_with_edits", "hold", "reject"}
REVISION_DECISIONS = {"approve", "hold", "reject"}
REVIEW_FIELD_SET = set(workbench.REVIEW_FIELDS)


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("review root must be an object")
    return data


def current_workbench() -> dict[str, Any]:
    return workbench.build_payload(ROOT)["registration_workbench"]


def manifest_map() -> dict[str, dict[str, Any]]:
    data = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    docs = data.get("documents") if isinstance(data, dict) else None
    if not isinstance(docs, list):
        raise ValueError("docs_manifest.yml documents must be an array")
    return {str(item.get("path") or ""): item for item in docs if isinstance(item, dict) and str(item.get("path") or "")}


def safe_review_object(value: Any, label: str, errors: list[str]) -> dict[str, Any]:
    if not isinstance(value, dict):
        errors.append(f"{label} must be an object")
        return {}
    forbidden = set(value) - REVIEW_FIELD_SET
    if forbidden:
        errors.append(f"{label} contains non-workbench field(s): {sorted(forbidden)}")
    return value


def validate(data: dict[str, Any], *, allow_stale: bool = False, assessment_run: Path | None = None, assessment_review: Path | None = None) -> list[str]:
    errors: list[str] = []
    payload = data.get("registration_review")
    if not isinstance(payload, dict):
        return ["registration_review root object is required"]
    if str(payload.get("schema_version") or "") != "0.3":
        errors.append("schema_version must be 0.3")
    if payload.get("status") not in {"in_progress", "complete"}:
        errors.append("status must be in_progress or complete")

    current = current_workbench()
    expected_source = current.get("source") or {}
    source = payload.get("source")
    if not isinstance(source, dict):
        errors.append("source object is required")
        source = {}
    expected_counts = {
        "provisional_count": len(current.get("provisional_documents") or []),
        "revision_proposal_count": len(current.get("revision_proposals") or []),
    }
    if not allow_stale:
        for key in ("manifest_sha256", "graph_sha256", "revision_proposals_sha256"):
            if str(source.get(key) or "") != str(expected_source.get(key) or ""):
                errors.append(f"stale source: {key} review={source.get(key)!r} current={expected_source.get(key)!r}")
        for key, expected in expected_counts.items():
            try:
                actual = int(source.get(key))
            except (TypeError, ValueError):
                actual = -1
            if actual != expected:
                errors.append(f"stale source: {key} review={source.get(key)!r} current={expected}")

    provisional = {str(item.get("path") or ""): item for item in current.get("provisional_documents") or [] if isinstance(item, dict)}
    proposals_by_id = {str(item.get("proposal_id") or ""): item for item in current.get("revision_proposals") or [] if isinstance(item, dict)}
    manifest = manifest_map()

    decisions = payload.get("decisions")
    if not isinstance(decisions, list):
        errors.append("decisions must be an array")
        decisions = []
    seen_decisions: set[str] = set()
    for idx, item in enumerate(decisions):
        if not isinstance(item, dict):
            errors.append(f"decisions[{idx}] must be an object")
            continue
        path = str(item.get("path") or "")
        decision = str(item.get("decision") or "")
        if not path:
            errors.append(f"decisions[{idx}] missing path")
            continue
        if path in seen_decisions:
            errors.append(f"duplicate provisional decision path: {path}")
        seen_decisions.add(path)
        current_item = provisional.get(path)
        if not current_item:
            errors.append(f"decision path is not currently provisional: {path}")
            continue
        if decision not in DECISIONS:
            errors.append(f"invalid decision for {path}: {decision}")
        before = safe_review_object(item.get("before"), f"decision before for {path}", errors)
        after = safe_review_object(item.get("after"), f"decision after for {path}", errors)
        baseline = current_item.get("baseline") or {}
        if before != baseline:
            errors.append(f"provisional baseline changed: {path}")
        if str(item.get("doc_id") or "") != str(current_item.get("doc_id") or ""):
            errors.append(f"provisional doc_id mismatch: {path}")
        if after and str(after.get("path") or path) != path:
            errors.append(f"provisional path cannot be edited: {path}")
        if after and str(after.get("doc_id") or "") != str(current_item.get("doc_id") or ""):
            errors.append(f"provisional doc_id cannot be edited: {path}")
        if after and str(after.get("registration_state") or "provisional") != "provisional":
            errors.append(f"registration_state is promoted only by repository apply: {path}")
        if decision == "approve" and before != after:
            errors.append(f"approve must not contain metadata edits: {path}")
        if decision == "approve_with_edits" and before == after:
            errors.append(f"approve_with_edits has no actual edit: {path}")

    manual_candidates = payload.get("manual_candidates")
    if not isinstance(manual_candidates, list):
        errors.append("manual_candidates must be an array")
        manual_candidates = []
    seen_manual_paths: set[str] = set()
    for idx, item in enumerate(manual_candidates):
        if not isinstance(item, dict):
            errors.append(f"manual_candidates[{idx}] must be an object")
            continue
        if str(item.get("decision") or "") not in REVISION_DECISIONS:
            errors.append(f"invalid manual candidate decision at index {idx}")
        proposed = safe_review_object(item.get("proposed"), f"manual candidate proposed[{idx}]", errors)
        path = str(proposed.get("path") or "")
        doc_id = str(proposed.get("doc_id") or "")
        if not path or not doc_id:
            errors.append(f"manual candidate requires path and doc_id at index {idx}")
            continue
        if path in seen_manual_paths:
            errors.append(f"duplicate manual candidate path: {path}")
        seen_manual_paths.add(path)
        if path in manifest:
            errors.append(f"manual candidate path is already in manifest: {path}")

    revisions = payload.get("revision_candidates")
    if not isinstance(revisions, list):
        errors.append("revision_candidates must be an array")
        revisions = []
    seen_revision_paths: set[str] = set()
    for idx, item in enumerate(revisions):
        if not isinstance(item, dict):
            errors.append(f"revision_candidates[{idx}] must be an object")
            continue
        path = str(item.get("path") or "")
        doc_id = str(item.get("doc_id") or "")
        decision = str(item.get("decision") or "")
        source_kind = str(item.get("source_kind") or "")
        if not path:
            errors.append(f"revision_candidates[{idx}] missing path")
            continue
        if path in seen_revision_paths:
            errors.append(f"duplicate revision path: {path}")
        seen_revision_paths.add(path)
        entry = manifest.get(path)
        if not entry:
            errors.append(f"revision path is not in manifest: {path}")
            continue
        if str(entry.get("registration_state") or "") != "registered":
            errors.append(f"revision target is not registered: {path}")
        expected_doc_id = str(entry.get("doc_id") or workbench.fallback_doc_id(path))
        if doc_id != expected_doc_id:
            errors.append(f"revision doc_id mismatch: {path}")
        if decision not in REVISION_DECISIONS:
            errors.append(f"invalid revision decision for {path}: {decision}")
        if source_kind not in {"revision_proposal", "ad_hoc_registered_revision"}:
            errors.append(f"invalid revision source_kind for {path}: {source_kind}")
        before = safe_review_object(item.get("before"), f"revision before for {path}", errors)
        after = safe_review_object(item.get("after"), f"revision after for {path}", errors)
        baseline = workbench.review_projection(entry)
        if before != baseline:
            errors.append(f"registered revision baseline changed: {path}")
        if after:
            if str(after.get("path") or path) != path:
                errors.append(f"revision path cannot be edited: {path}")
            if str(after.get("doc_id") or expected_doc_id) != expected_doc_id:
                errors.append(f"revision doc_id cannot be edited: {path}")
            if str(after.get("registration_state") or "registered") != "registered":
                errors.append(f"registered revision cannot change registration_state: {path}")
        if decision == "approve" and (not after or after == before):
            errors.append(f"approved revision contains no actual change: {path}")
        if source_kind == "revision_proposal":
            proposal_id = str(item.get("proposal_id") or "")
            proposal = proposals_by_id.get(proposal_id)
            if not proposal or str(proposal.get("path") or "") != path:
                errors.append(f"revision proposal binding is invalid: {path}")
            if str(item.get("proposal_source_sha256") or "") != str(expected_source.get("revision_proposals_sha256") or ""):
                errors.append(f"revision proposal source hash is stale: {path}")

    # A generic metadata edit is not an assessment approval.
    changed_assessments = {}
    for item in [*decisions, *revisions]:
        if item.get("decision") not in {"approve", "approve_with_edits"}:
            continue
        before, after = item.get("before") or {}, item.get("after") or {}
        if before.get("assessment") != after.get("assessment"):
            changed_assessments[str(item.get("path"))] = after.get("assessment")
    for item in manual_candidates:
        if (item.get("proposed") or {}).get("assessment", {}).get("review_state") == "approved":
            errors.append("Manual registration cannot introduce an already-approved assessment")
    if changed_assessments:
        if not assessment_run or not assessment_review:
            errors.append("Assessment changes require --assessment-run and --assessment-review; metadata approval is not score approval")
        else:
            try:
                from assessment_registration import summaries_from_review
                expected = summaries_from_review(ROOT, assessment_run, assessment_review)
                for path, summary in changed_assessments.items():
                    if summary != expected.get(path):
                        errors.append("Assessment summary does not match explicitly reviewed evidence: " + path)
            except Exception as exc:
                errors.append(str(exc))
    return errors


def self_test() -> int:
    current = current_workbench()
    provisional = current.get("provisional_documents") or []
    decisions = []
    if provisional:
        first = provisional[0]
        baseline = first["baseline"]
        decisions.append({
            "path": first["path"],
            "doc_id": first["doc_id"],
            "decision": "approve",
            "reviewed_at": "self-test",
            "reviewer_note": "",
            "before": baseline,
            "after": baseline,
        })
    data = {
        "registration_review": {
            "schema_version": "0.3",
            "status": "in_progress",
            "source": {
                "manifest_sha256": current["source"]["manifest_sha256"],
                "graph_sha256": current["source"]["graph_sha256"],
                "provisional_count": len(provisional),
                "revision_proposals_sha256": current["source"]["revision_proposals_sha256"],
                "revision_proposal_count": len(current.get("revision_proposals") or []),
            },
            "decisions": decisions,
            "manual_candidates": [],
            "revision_candidates": [],
        }
    }
    errors = validate(data)
    if errors:
        for error in errors:
            print(f"ERROR {error}", file=sys.stderr)
        return 1
    print("REGISTRATION REVIEW SELF-TEST PASS")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a Navigator registration-review export.")
    parser.add_argument("review", nargs="?", help="Path to exported review JSON.")
    parser.add_argument("--allow-stale", action="store_true", help="Validate structure without current-source hash equality.")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--assessment-run", type=Path)
    parser.add_argument("--assessment-review", type=Path)
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    if not args.review:
        parser.error("review path is required unless --self-test is used")
    try:
        data = load_json(Path(args.review))
        errors = validate(data, allow_stale=args.allow_stale, assessment_run=args.assessment_run, assessment_review=args.assessment_review)
    except Exception as exc:
        print(f"REGISTRATION REVIEW CHECK FAILED: {exc}", file=sys.stderr)
        return 1
    if errors:
        print(f"REGISTRATION REVIEW CHECK FAILED: {len(errors)} issue(s)", file=sys.stderr)
        for error in errors:
            print(f"ERROR {error}", file=sys.stderr)
        return 1
    payload = data["registration_review"]
    counts: dict[str, int] = {}
    for item in payload.get("decisions", []):
        counts[item["decision"]] = counts.get(item["decision"], 0) + 1
    print(f"REGISTRATION REVIEW CHECK PASS: {len(payload.get('decisions', []))} provisional decisions, {counts}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

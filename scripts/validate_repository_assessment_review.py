#!/usr/bin/env python3
"""Validate a repository assessment review transaction against a raw run."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ISSUES = {
    "proposition_error", "merge_error", "attribution_error", "domain_error", "commitment_error",
    "responsibility_error", "scope_error", "document_profile_error", "hotspot_detection_error",
    "strength_error", "exposure_error", "ground_owner_error", "evidence_error", "protocol_rule_error", "other",
}
DECISIONS = {"approve", "approve_with_edits", "hold", "reject"}
KINDS = {"document_profile", "representative_claim", "claim_hotspot"}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fail(message: str) -> None:
    raise ValueError(message)


def run_review_keys(run: dict) -> set[str]:
    keys: set[str] = set()
    for doc in run.get("documents", []):
        path = str(doc.get("path") or "")
        if path:
            keys.add(f"document_profile::{path}")
        for rep in doc.get("representative_claims", []):
            cid = str(rep.get("claim_id") or "")
            if cid:
                keys.add(f"representative_claim::{cid}")
        for hotspot in doc.get("claim_hotspots", []):
            hid = str(hotspot.get("hotspot_id") or "")
            if hid:
                keys.add(f"claim_hotspot::{hid}")
    return keys


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("review", type=Path)
    parser.add_argument("--run", type=Path, required=True)
    args = parser.parse_args()

    review_data = json.loads(args.review.read_text(encoding="utf-8-sig"))
    payload = review_data.get("repository_assessment_review")
    if not isinstance(payload, dict):
        fail("repository_assessment_review is required")
    if str(payload.get("schema_version")) != "0.2":
        fail("schema_version must be 0.2")
    if str(payload.get("source_run_sha256")) != sha256(args.run):
        fail("source_run_sha256 does not match --run bytes")

    run_data = json.loads(args.run.read_text(encoding="utf-8-sig"))
    run = run_data.get("repository_assessment_run") or {}
    valid_keys = run_review_keys(run)

    seen: set[str] = set()
    for item in payload.get("decisions", []):
        key = str(item.get("review_key") or "")
        if not key or key not in valid_keys:
            fail(f"unknown review_key in review: {key}")
        if key in seen:
            fail(f"duplicate review decision: {key}")
        seen.add(key)
        if item.get("kind") not in KINDS:
            fail(f"{key}: invalid kind")
        if item.get("decision") not in DECISIONS:
            fail(f"{key}: invalid decision")
        bad = set(item.get("issue_types") or []) - ISSUES
        if bad:
            fail(f"{key}: invalid issue type(s): {sorted(bad)}")
        if not isinstance(item.get("before"), dict) or not isinstance(item.get("after"), dict):
            fail(f"{key}: before/after required")

    print(f"Repository assessment review: PASS ({len(seen)} decisions / {len(valid_keys)} reviewable items)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

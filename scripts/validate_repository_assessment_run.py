#!/usr/bin/env python3
"""Validate a repository assessment run and its binding to a protocol preview."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PREVIEW = ROOT / "tools" / "assessment" / "repository_assessment_protocols.preview.json"

VALID_COMMITMENTS = {"represented", "endorsed", "derived", "suspended", "indeterminate"}
VALID_STRENGTH = {None, "S0", "S1", "S2", "S3", "S4", "S5"}
VALID_EXPOSURE = {None, "E0", "E1", "E2", "E3"}
VALID_ROLES = {"central_claim", "core_definition", "conclusion", "supporting_argument", "bridge", "scope_control", "other"}
VALID_HOTSPOT_REASONS = {"different_ground_owner", "external_bridge", "scope_expansion", "identity_or_universality", "causal_or_mechanistic", "strong_correspondence", "separate_responsibility", "other"}


def fail(message: str) -> None:
    raise ValueError(message)


def validate_classification(label: str, value: dict) -> None:
    strength = value.get("strength")
    exposure = value.get("exposure")
    if strength not in VALID_STRENGTH:
        fail(f"{label}: invalid strength")
    if exposure not in VALID_EXPOSURE:
        fail(f"{label}: invalid exposure")


def validate_attribution(label: str, value: dict) -> None:
    commitment = str(value.get("repository_commitment") or "")
    if commitment not in VALID_COMMITMENTS:
        fail(f"{label}: invalid repository_commitment")
    for field in ("represented_system", "responsibility", "scope"):
        if field not in value:
            fail(f"{label}: attribution.{field} is required")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("run", type=Path)
    args = parser.parse_args()
    text = args.run.read_text(encoding="utf-8-sig")
    data = json.loads(text)
    run = data.get("repository_assessment_run")
    if not isinstance(run, dict):
        fail("repository_assessment_run is required")
    if str(run.get("schema_version")) != "0.2":
        fail("schema_version must be 0.2")
    if not str(run.get("run_id") or "").strip():
        fail("run_id is required")

    protocol = run.get("protocol") or {}
    preview = json.loads(PREVIEW.read_text(encoding="utf-8"))["repository_assessment_protocols_preview"]
    matched = [p for p in preview.get("protocols", []) if p.get("id") == protocol.get("id") and p.get("revision") == protocol.get("revision")]
    if not matched:
        fail("protocol id/revision is not present in current preview")
    expected_schema = str((matched[0].get("output_contract") or {}).get("schema") or "")
    if expected_schema != "repository_assessment_run/0.2":
        fail(f"protocol expects {expected_schema}, not repository_assessment_run/0.2")
    if str(protocol.get("source_sha256")) != str(matched[0].get("source_sha256")):
        fail("protocol source_sha256 does not match current protocol revision")

    targets = run.get("fixture", {}).get("targets")
    if not isinstance(targets, list) or not targets:
        fail("fixture.targets is required")
    target_paths = {str(item.get("path") or "") for item in targets if isinstance(item, dict)}

    documents = run.get("documents")
    if not isinstance(documents, list) or not documents:
        fail("documents must be a non-empty array")

    seen_paths: set[str] = set()
    rep_ids: set[str] = set()
    hotspot_ids: set[str] = set()
    boundary_ids: set[str] = set()
    total_reps = total_hotspots = total_nonclaims = 0

    for doc in documents:
        if not isinstance(doc, dict):
            fail("document entry must be an object")
        path = str(doc.get("path") or "")
        if not path:
            fail("document path is required")
        if path in seen_paths:
            fail(f"duplicate document path: {path}")
        seen_paths.add(path)
        if path not in target_paths:
            fail(f"document path is not in fixture.targets: {path}")

        profile = doc.get("document_profile") or {}
        validate_classification(f"{path}: document_profile", profile.get("classification") or {})
        basis_ids = profile.get("basis_claim_ids")
        if not isinstance(basis_ids, list) or not basis_ids:
            fail(f"{path}: document_profile.basis_claim_ids is required")

        reps = doc.get("representative_claims")
        hotspots = doc.get("claim_hotspots")
        nonclaims = doc.get("nonclaim_boundaries")
        if not isinstance(reps, list) or not reps:
            fail(f"{path}: representative_claims must be non-empty")
        if not isinstance(hotspots, list):
            fail(f"{path}: claim_hotspots must be an array")
        if not isinstance(nonclaims, list):
            fail(f"{path}: nonclaim_boundaries must be an array")

        local_rep_ids: set[str] = set()
        for rep in reps:
            cid = str(rep.get("claim_id") or "")
            if not cid or cid in rep_ids:
                fail(f"invalid or duplicate representative claim_id: {cid}")
            rep_ids.add(cid)
            local_rep_ids.add(cid)
            if rep.get("argument_role") not in VALID_ROLES:
                fail(f"{cid}: invalid argument_role")
            if not isinstance(rep.get("source_refs"), list) or not rep["source_refs"]:
                fail(f"{cid}: source_refs is required")
            validate_attribution(cid, rep.get("attribution") or {})
            validate_classification(cid, rep.get("classification") or {})
        missing_basis = set(str(value) for value in basis_ids) - local_rep_ids
        if missing_basis:
            fail(f"{path}: basis_claim_ids not found in representative_claims: {sorted(missing_basis)}")

        for hotspot in hotspots:
            hid = str(hotspot.get("hotspot_id") or "")
            if not hid or hid in hotspot_ids:
                fail(f"invalid or duplicate hotspot_id: {hid}")
            hotspot_ids.add(hid)
            if hotspot.get("argument_role") not in VALID_ROLES:
                fail(f"{hid}: invalid argument_role")
            reasons = hotspot.get("hotspot_reasons")
            if not isinstance(reasons, list) or not reasons or any(reason not in VALID_HOTSPOT_REASONS for reason in reasons):
                fail(f"{hid}: invalid hotspot_reasons")
            validate_attribution(hid, hotspot.get("attribution") or {})
            validate_classification(hid, hotspot.get("classification") or {})
            if hotspot.get("classification_effect") != "local_only":
                fail(f"{hid}: classification_effect must be local_only")
            ground = hotspot.get("ground") or {}
            if not str(ground.get("owner") or "") or not str(ground.get("relation") or ""):
                fail(f"{hid}: ground.owner and ground.relation are required")

        for boundary in nonclaims:
            bid = str(boundary.get("boundary_id") or "")
            if not bid or bid in boundary_ids:
                fail(f"invalid or duplicate boundary_id: {bid}")
            boundary_ids.add(bid)
            if not str(boundary.get("proposition") or ""):
                fail(f"{bid}: proposition is required")

        total_reps += len(reps)
        total_hotspots += len(hotspots)
        total_nonclaims += len(nonclaims)

    if seen_paths != target_paths:
        missing = sorted(target_paths - seen_paths)
        extra = sorted(seen_paths - target_paths)
        fail(f"documents/fixture mismatch; missing={missing}, extra={extra}")

    print(f"Repository assessment run: PASS ({len(documents)} documents)")
    print(f"Representative claims: {total_reps}")
    print(f"Claim hotspots: {total_hotspots}")
    print(f"Nonclaim boundaries: {total_nonclaims}")
    print(f"Protocol: {protocol.get('id')} / {protocol.get('revision')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

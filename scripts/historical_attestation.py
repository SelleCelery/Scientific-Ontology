#!/usr/bin/env python3
"""Observe, classify, and evaluate historical attestation state.

This module intentionally separates three operations:

1. observation: what differs now;
2. classification: what kind of difference it is;
3. policy evaluation: whether that difference blocks the current operation.

Historical evidence records remain immutable. Aggregate counts are generated
observations, not manifest-owned acceptance criteria.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path, PurePosixPath
from typing import Any, Mapping, Sequence

import yaml

SHA_PATTERN = re.compile(r"^[0-9a-f]{64}$")
FORBIDDEN_PARTS = {".git", ".github", ".venv", "node_modules", "__pycache__", "_build"}
DEFAULT_POLICY_PATH = Path("tools/historical_attestation_policy.yml")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def resolve_repo_path(root: Path, value: str) -> Path:
    if not isinstance(value, str) or not value or "\\" in value or ":" in value:
        raise ValueError(f"Unsafe repository path: {value!r}")
    parts = PurePosixPath(value)
    if parts.is_absolute() or ".." in parts.parts or any(p in FORBIDDEN_PARTS for p in parts.parts):
        raise ValueError(f"Unsafe repository path: {value!r}")
    resolved = (root / value).resolve()
    if not resolved.is_relative_to(root.resolve()):
        raise ValueError(f"Path escapes repository: {value!r}")
    return resolved


def checksum_manifest_entries(path: Path) -> tuple[list[tuple[str, str]], list[dict[str, Any]]]:
    entries: list[tuple[str, str]] = []
    issues: list[dict[str, Any]] = []
    seen: set[str] = set()
    for line_number, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), start=1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        match = re.match(r"^([0-9a-fA-F]{64})\s+\*?(.+?)\s*$", line)
        if not match:
            issues.append({
                "code": "invalid_checksum_entry",
                "message": f"Invalid checksum entry at {path.as_posix()}:{line_number}",
                "line": line_number,
            })
            continue
        rel = match[2]
        if rel in seen:
            issues.append({
                "code": "duplicate_checksum_path",
                "message": f"Duplicate checksum path in {path.as_posix()}: {rel}",
                "path": rel,
                "line": line_number,
            })
            continue
        seen.add(rel)
        entries.append((match[1].lower(), rel))
    return entries, issues


def _record_path(spec: Mapping[str, Any], rel: str) -> str:
    return (PurePosixPath(str(spec["root"])) / PurePosixPath(rel)).as_posix()


def _equivalence_class(
    record: Mapping[str, Any] | None,
    *,
    expected_digest: str,
    actual_digest: str,
) -> str | None:
    """Return a declared equivalence class for an exact known representation.

    No generic normalization is inferred. An alternative representation is
    accepted only when its digest and basis are explicitly bound in the asset
    record.
    """
    if record is None:
        return None
    integrity = record.get("integrity") or {}
    if (
        record.get("document_role") == "provenance_asset"
        and integrity.get("basis") == "rc004_snapshot_not_historical_certification"
        and integrity.get("sha256") == expected_digest
        and integrity.get("git_lf_basis") == "rc004_HEAD_blob_CRLF_only_difference"
        and integrity.get("git_lf_sha256") == actual_digest
    ):
        return "eol_only_declared_equivalent"
    return None


def _observe_checksum_set(
    root: Path,
    spec: Mapping[str, Any],
    checksum_path: Path,
    *,
    records: Mapping[str, Mapping[str, Any]] | None,
    relation_prefix: str,
) -> dict[str, Any]:
    entries, parse_issues = checksum_manifest_entries(checksum_path)
    base = resolve_repo_path(root, str(spec["root"]))
    result: dict[str, Any] = {
        "entry_count": len(entries),
        "exact_paths": [],
        "equivalent_paths": [],
        "divergent_paths": [],
        "missing_paths": [],
        "unsafe_paths": [],
        "parse_issues": parse_issues,
        "path_digests": [],
        "declared_paths": [rel for _digest, rel in entries],
    }
    for expected_digest, rel in entries:
        target = (base / rel).resolve()
        if not target.is_relative_to(base.resolve()):
            result["unsafe_paths"].append(rel)
            continue
        if not target.is_file():
            result["missing_paths"].append(rel)
            continue
        data = target.read_bytes()
        actual_digest = sha256_bytes(data)
        full_record_path = _record_path(spec, rel)
        record = records.get(full_record_path) if records is not None else None
        item = {
            "path": rel,
            "repository_path": full_record_path,
            "expected_sha256": expected_digest,
            "actual_sha256": actual_digest,
        }
        if actual_digest == expected_digest:
            item["classification"] = "exact"
            result["exact_paths"].append(item)
        else:
            equivalence = _equivalence_class(
                record,
                expected_digest=expected_digest,
                actual_digest=actual_digest,
            )
            if equivalence:
                item["classification"] = equivalence
                result["equivalent_paths"].append(item)
            else:
                item["classification"] = f"{relation_prefix}_content_divergence"
                result["divergent_paths"].append(item)
        result["path_digests"].append(item)
    result["counts"] = {
        "exact": len(result["exact_paths"]),
        "equivalent": len(result["equivalent_paths"]),
        "divergent": len(result["divergent_paths"]),
        "missing": len(result["missing_paths"]),
        "unsafe": len(result["unsafe_paths"]),
        "invalid": len(result["parse_issues"]),
    }
    return result


def observe_historical_attestation(
    root: Path,
    spec: Mapping[str, Any],
    *,
    records: Mapping[str, Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    root = root.resolve()
    observation: dict[str, Any] = {
        "id": str(spec.get("id", "<unknown>")),
        "integrity_claim": spec.get("integrity_claim"),
        "metadata_issues": [],
        "historical_relation": None,
        "attested_current_relation": None,
        "path_set": {"missing_from_snapshot": [], "extra_in_snapshot": []},
    }
    att = spec.get("attestation")
    if not isinstance(att, Mapping):
        observation["metadata_issues"].append({
            "code": "attestation_missing",
            "message": f"Historical attestation is missing for {observation['id']}",
        })
        return observation

    status = str(att.get("status", ""))
    profile = str(att.get("policy_profile") or status or "strict")
    observation["attestation_status"] = status
    observation["policy_profile"] = profile
    if status != "accepted_as_historical_method_record":
        observation["metadata_issues"].append({
            "code": "attestation_status_invalid",
            "message": f"Historical attestation status is not accepted: {observation['id']}",
        })
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", str(att.get("attested_at", ""))):
        observation["metadata_issues"].append({
            "code": "attestation_date_invalid",
            "message": f"Historical attestation date is invalid: {observation['id']}",
        })
    if not str(att.get("acceptance_scope", "")).strip():
        observation["metadata_issues"].append({
            "code": "acceptance_scope_missing",
            "message": f"Historical attestation acceptance_scope is missing: {observation['id']}",
        })
    if spec.get("release_review_required") is not False:
        observation["metadata_issues"].append({
            "code": "release_review_flag_invalid",
            "message": f"Attested provenance set must set release_review_required: false: {observation['id']}",
        })

    try:
        historical_path = resolve_repo_path(root, str(spec["path"]))
        attestation_path_value = str(att.get("attestation_path", ""))
        snapshot_path_value = str(att.get("current_snapshot_path", ""))
        attestation_path = resolve_repo_path(root, attestation_path_value)
        snapshot_path = resolve_repo_path(root, snapshot_path_value)
    except ValueError as exc:
        observation["metadata_issues"].append({"code": "unsafe_contract_path", "message": str(exc)})
        return observation

    if not historical_path.is_file():
        observation["metadata_issues"].append({
            "code": "historical_manifest_missing",
            "message": f"Historical checksum manifest is missing: {spec['path']}",
        })
        return observation
    if not attestation_path.is_file():
        observation["metadata_issues"].append({
            "code": "attestation_record_missing",
            "message": f"Historical attestation record is missing: {attestation_path_value}",
        })
    if not snapshot_path.is_file():
        observation["metadata_issues"].append({
            "code": "attested_snapshot_missing",
            "message": f"Historical attested-current snapshot is missing: {snapshot_path_value}",
        })
        return observation

    if records is not None:
        att_entry = records.get(attestation_path_value)
        snap_entry = records.get(snapshot_path_value)
        if not att_entry or att_entry.get("document_role") != "historical_support":
            observation["metadata_issues"].append({
                "code": "attestation_record_role_invalid",
                "message": f"Historical attestation record is not registered as historical_support: {attestation_path_value}",
            })
        if not snap_entry or snap_entry.get("document_role") != "provenance_asset":
            observation["metadata_issues"].append({
                "code": "attested_snapshot_role_invalid",
                "message": f"Historical current snapshot is not registered as provenance_asset: {snapshot_path_value}",
            })

    historical = _observe_checksum_set(
        root,
        spec,
        historical_path,
        records=records,
        relation_prefix="historical",
    )
    current = _observe_checksum_set(
        root,
        spec,
        snapshot_path,
        records=records,
        relation_prefix="attested_current",
    )
    observation["historical_relation"] = historical
    observation["attested_current_relation"] = current

    historical_paths = set(historical.get("declared_paths", []))
    current_paths = set(current.get("declared_paths", []))
    observation["path_set"] = {
        "missing_from_snapshot": sorted(historical_paths - current_paths),
        "extra_in_snapshot": sorted(current_paths - historical_paths),
    }
    return observation


def load_policy(root: Path, path: Path | None = None) -> dict[str, Any]:
    policy_path = path or (root / DEFAULT_POLICY_PATH)
    if not policy_path.is_absolute():
        policy_path = root / policy_path
    data = yaml.safe_load(policy_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"Historical attestation policy must be a mapping: {policy_path}")
    if data.get("schema_version") != "historical-attestation-policy/1.0":
        raise ValueError(f"Unsupported historical attestation policy schema: {data.get('schema_version')!r}")
    if not isinstance(data.get("profiles"), dict):
        raise ValueError("Historical attestation policy profiles are missing")
    return data


def _finding(code: str, message: str, *, paths: Sequence[str] = ()) -> dict[str, Any]:
    return {"code": code, "message": message, "paths": list(paths)}


def classify_observation(observation: Mapping[str, Any]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = [dict(item) for item in observation.get("metadata_issues", [])]
    historical = observation.get("historical_relation") or {}
    current = observation.get("attested_current_relation") or {}
    path_set = observation.get("path_set") or {}
    oid = observation.get("id", "<unknown>")

    if historical.get("parse_issues"):
        findings.append(_finding(
            "historical_manifest_invalid",
            f"Historical checksum manifest contains invalid or duplicate entries: {oid}",
            paths=[str(x.get("path") or x.get("line") or "") for x in historical["parse_issues"]],
        ))
    if historical.get("unsafe_paths"):
        findings.append(_finding("historical_path_unsafe", f"Historical manifest contains unsafe paths: {oid}", paths=historical["unsafe_paths"]))
    if historical.get("missing_paths"):
        findings.append(_finding("historical_path_missing", f"Historical manifest paths are missing: {oid}", paths=historical["missing_paths"]))
    if historical.get("equivalent_paths"):
        findings.append(_finding(
            "historical_eol_equivalent",
            f"Historical relation contains declared EOL-only equivalents: {oid}",
            paths=[x["path"] for x in historical["equivalent_paths"]],
        ))
    if historical.get("divergent_paths"):
        findings.append(_finding(
            "historical_content_divergence",
            f"Historical relation contains current divergence: {oid}",
            paths=[x["path"] for x in historical["divergent_paths"]],
        ))

    if current.get("parse_issues"):
        findings.append(_finding(
            "attested_snapshot_invalid",
            f"Attested-current snapshot contains invalid or duplicate entries: {oid}",
            paths=[str(x.get("path") or x.get("line") or "") for x in current["parse_issues"]],
        ))
    if path_set.get("missing_from_snapshot") or path_set.get("extra_in_snapshot"):
        findings.append(_finding(
            "attested_snapshot_path_set_drift",
            f"Attested-current snapshot path set differs from historical manifest: {oid}",
            paths=[*path_set.get("missing_from_snapshot", []), *path_set.get("extra_in_snapshot", [])],
        ))
    if current.get("unsafe_paths"):
        findings.append(_finding("attested_snapshot_path_unsafe", f"Attested-current snapshot contains unsafe paths: {oid}", paths=current["unsafe_paths"]))
    if current.get("missing_paths"):
        findings.append(_finding("attested_snapshot_path_missing", f"Attested-current snapshot paths are missing: {oid}", paths=current["missing_paths"]))
    if current.get("equivalent_paths"):
        findings.append(_finding(
            "attested_snapshot_eol_equivalent",
            f"Attested-current snapshot contains declared EOL-only equivalents: {oid}",
            paths=[x["path"] for x in current["equivalent_paths"]],
        ))
    if current.get("divergent_paths"):
        findings.append(_finding(
            "attested_snapshot_content_drift",
            f"Historical attested-current snapshot content drift detected: {oid}",
            paths=[x["path"] for x in current["divergent_paths"]],
        ))
    return findings


def evaluate_policy(
    observation: Mapping[str, Any],
    policy: Mapping[str, Any],
    *,
    release_gate: bool,
) -> list[dict[str, Any]]:
    profile_name = str(observation.get("policy_profile") or policy.get("default_profile") or "strict")
    profiles = policy.get("profiles") or {}
    profile = profiles.get(profile_name)
    if not isinstance(profile, Mapping):
        profile = profiles.get(str(policy.get("default_profile")))
    if not isinstance(profile, Mapping):
        raise ValueError(f"Historical attestation policy profile not found: {profile_name}")
    rules = profile.get("rules") or {}
    default_action = str(profile.get("default_action", "block"))
    evaluated: list[dict[str, Any]] = []
    for finding in classify_observation(observation):
        rule = rules.get(finding["code"], default_action)
        if isinstance(rule, Mapping):
            action = str(rule.get("release_gate" if release_gate else "ordinary", rule.get("default", default_action)))
        else:
            action = str(rule)
        if action not in {"ignore", "observe", "warn", "block"}:
            raise ValueError(f"Invalid historical attestation policy action {action!r} for {finding['code']}")
        evaluated.append({**finding, "action": action, "profile": profile_name})
    return evaluated


def observation_summary(observation: Mapping[str, Any]) -> dict[str, Any]:
    historical = observation.get("historical_relation") or {}
    current = observation.get("attested_current_relation") or {}
    return {
        "id": observation.get("id"),
        "policy_profile": observation.get("policy_profile"),
        "historical": historical.get("counts", {}),
        "attested_current": current.get("counts", {}),
        "path_set": observation.get("path_set", {}),
    }


def report_payload(observations: Sequence[Mapping[str, Any]], evaluations: Sequence[Sequence[Mapping[str, Any]]]) -> dict[str, Any]:
    items = []
    for observation, findings in zip(observations, evaluations):
        items.append({
            "summary": observation_summary(observation),
            "observation": observation,
            "policy_findings": list(findings),
        })
    return {
        "schema_version": "historical-attestation-observation/1.0",
        "sets": items,
        "blocking_findings": sum(1 for fs in evaluations for f in fs if f.get("action") == "block"),
        "warning_findings": sum(1 for fs in evaluations for f in fs if f.get("action") == "warn"),
        "observed_findings": sum(1 for fs in evaluations for f in fs if f.get("action") == "observe"),
    }


def write_json_report(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_markdown_report(path: Path, payload: Mapping[str, Any]) -> None:
    lines = ["# Historical Attestation Observation Report", ""]
    for item in payload.get("sets", []):
        summary = item["summary"]
        lines.extend([
            f"## {summary['id']}",
            "",
            f"- Policy profile: `{summary.get('policy_profile')}`",
            f"- Historical relation: `{summary.get('historical', {})}`",
            f"- Attested-current relation: `{summary.get('attested_current', {})}`",
            "",
            "### Policy findings",
            "",
        ])
        findings = item.get("policy_findings", [])
        if not findings:
            lines.append("- None")
        for finding in findings:
            lines.append(f"- **{finding['action'].upper()}** `{finding['code']}`: {finding['message']}")
            for rel in finding.get("paths", []):
                lines.append(f"  - `{rel}`")
        lines.append("")
    lines.extend([
        "## Aggregate decision surface",
        "",
        f"- Blocking findings: {payload.get('blocking_findings', 0)}",
        f"- Warning findings: {payload.get('warning_findings', 0)}",
        f"- Observation-only findings: {payload.get('observed_findings', 0)}",
        "",
    ])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")

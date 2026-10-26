#!/usr/bin/env python3
"""Validate current metadata, role contracts, coverage and fixed-source identity."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from document_contract import load_manifest, validate_manifest
from historical_attestation import (
    load_policy,
    report_payload,
    write_json_report,
    write_markdown_report,
)


def _emit_historical_observations(items: list[dict], *, github_annotations: bool) -> None:
    for item in items:
        observation = item["observation"]
        historical = (observation.get("historical_relation") or {}).get("counts", {})
        current = (observation.get("attested_current_relation") or {}).get("counts", {})
        print(
            "HISTORICAL ATTESTATION OBSERVATION: "
            f"{observation.get('id')} "
            f"historical={historical} attested_current={current}"
        )
        for finding in item["policy_findings"]:
            action = finding["action"]
            if action == "ignore":
                continue
            print(f"{action.upper()}: {finding['code']}: {finding['message']}")
            for rel in finding.get("paths", []):
                print(f"  - {rel}")
            if github_annotations:
                level = {"block": "error", "warn": "warning", "observe": "notice"}[action]
                message = finding["message"]
                if finding.get("paths"):
                    message += f" ({len(finding['paths'])} path(s); see uploaded report)"
                print(f"::{level} title=Historical attestation::{message}")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    p.add_argument(
        "--release-gate",
        action="store_true",
        help="Apply release-gate policy actions. Observation-only findings do not block.",
    )
    p.add_argument(
        "--historical-policy",
        type=Path,
        default=Path("tools/historical_attestation_policy.yml"),
    )
    p.add_argument("--historical-json-log", type=Path)
    p.add_argument("--historical-md-log", type=Path)
    p.add_argument("--github-annotations", action="store_true")
    args = p.parse_args()
    root = args.root.resolve()
    observations: list[dict] = []
    try:
        manifest = load_manifest(root)
        policy = load_policy(root, args.historical_policy)
        errors, warnings = validate_manifest(
            root,
            manifest,
            release_gate=args.release_gate,
            historical_policy=policy,
            historical_observations=observations,
        )
    except Exception as exc:
        print(f"MANIFEST CONTRACT ERROR: {exc}", file=sys.stderr)
        return 1

    _emit_historical_observations(observations, github_annotations=args.github_annotations)
    payload = report_payload(
        [x["observation"] for x in observations],
        [x["policy_findings"] for x in observations],
    )
    if args.historical_json_log:
        write_json_report(args.historical_json_log, payload)
    if args.historical_md_log:
        write_markdown_report(args.historical_md_log, payload)

    for message in warnings:
        print("WARNING: " + message)
        if args.github_annotations:
            print(f"::warning title=Manifest contract::{message}")
    for message in errors:
        print("ERROR: " + message, file=sys.stderr)
        if args.github_annotations:
            print(f"::error title=Manifest contract::{message}")

    if errors or (warnings and args.release_gate):
        print(f"MANIFEST CONTRACT BLOCKED: errors={len(errors)} unresolved={len(warnings)}")
        return 1
    print(
        "MANIFEST CONTRACT PASS: "
        f"documents={len(manifest['documents'])} "
        f"managed_assets={len(manifest['managed_assets'])} "
        f"retired={len(manifest['retired_documents'])}; "
        "assessment approval is separate"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

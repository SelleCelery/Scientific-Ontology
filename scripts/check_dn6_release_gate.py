#!/usr/bin/env python3
"""DN-6 release integration gate for Scientific Ontology.

Default mode checks release-candidate readiness. Publication mode additionally invokes
release_update.py --release-check and therefore requires real publication date / DOI facts.
"""
from __future__ import annotations

import argparse
import collections
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

try:
    import yaml
except ModuleNotFoundError as exc:  # pragma: no cover - operational guidance
    raise SystemExit(
        "PyYAML is required. Install repository public-check dependencies with: "
        "python -m pip install -r requirements-public-check.txt"
    ) from exc

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "tools" / "dn6_release_gate.yml"
REPORT = ROOT / "tools" / "DN6_RELEASE_GATE_REPORT.ja.md"


def load_yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def run_command(root: Path, label: str, command: list[str]) -> dict[str, Any]:
    result = subprocess.run(command, cwd=root, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return {
        "label": label,
        "command": command,
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "pass": result.returncode == 0,
    }


def walk_forbidden_keys(value: Any, forbidden: set[str], found: set[str]) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if str(key) in forbidden:
                found.add(str(key))
            walk_forbidden_keys(child, forbidden, found)
    elif isinstance(value, list):
        for child in value:
            walk_forbidden_keys(child, forbidden, found)


def gate_data_checks(root: Path, cfg: dict[str, Any]) -> list[dict[str, Any]]:
    boundary = cfg["public_boundary"]
    checks: list[dict[str, Any]] = []

    catalog = load_json(root / "tools" / "docs_public_catalog.json")
    graph = load_json(root / "tools" / "docs_graph.json")
    public_graph = load_json(root / "tools" / "docs_public_graph.json")
    manifest = load_yaml(root / "tools" / "docs_manifest.yml")

    # Manifest / generated-data freshness is checked by prior commands.
    # Only the remaining publication-boundary invariants belong in this gate.
    unregistered = graph.get("diagnostics", {}).get("observed_unregistered_documents", [])
    checks.append({
        "label": "no-unregistered-documents",
        "pass": isinstance(unregistered, list) and len(unregistered) == 0,
        "detail": f"unregistered={len(unregistered) if isinstance(unregistered, list) else 'invalid'}",
    })

    forbidden_catalog = set(boundary.get("public_catalog_forbidden_keys", []))
    found_catalog: set[str] = set()
    walk_forbidden_keys(catalog, forbidden_catalog, found_catalog)
    checks.append({
        "label": "public-catalog-no-developer-fields",
        "pass": not found_catalog,
        "detail": "none" if not found_catalog else ", ".join(sorted(found_catalog)),
    })

    forbidden_graph_top = set(boundary.get("public_graph_forbidden_top_level_keys", []))
    found_graph_top = sorted(forbidden_graph_top.intersection(public_graph.keys()))
    checks.append({
        "label": "public-graph-no-developer-top-level-data",
        "pass": not found_graph_top,
        "detail": "none" if not found_graph_top else ", ".join(found_graph_top),
    })

    checks.append({
        "label": "public-graph-semantic-parity",
        "pass": public_graph.get("nodes") == graph.get("nodes") and public_graph.get("edges") == graph.get("edges"),
        "detail": f"public={len(public_graph.get('nodes', []))}/{len(public_graph.get('edges', []))}, canonical={len(graph.get('nodes', []))}/{len(graph.get('edges', []))}",
    })

    provisional_ids = {
        str(doc.get("doc_id"))
        for doc in manifest.get("documents", [])
        if doc.get("registration_state") == "provisional"
    }
    strong = set(boundary.get("strong_relation_types_forbidden_from_provisional_documents", []))
    violations = []
    for edge in graph.get("edges", []):
        rel = str(edge.get("type", ""))
        source_id = str(edge.get("source", ""))
        if rel in strong and source_id.startswith("doc:") and source_id[4:] in provisional_ids:
            violations.append(f"{source_id}:{rel}")
    checks.append({
        "label": "provisional-no-invented-strong-relations",
        "pass": not violations,
        "detail": "none" if not violations else ", ".join(violations[:20]),
    })

    return checks


def public_format_check(root: Path, cfg: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    fd, temp_name = tempfile.mkstemp(prefix="dn6-public-format-", suffix=".json")
    os.close(fd)
    Path(temp_name).unlink(missing_ok=True)
    command = [
        sys.executable,
        "scripts/check_public_format.py",
        "--release-gate",
        "--check-release-metadata",
        "--json-log",
        temp_name,
    ]
    result = run_command(root, "public-format-release-gate", command)
    report_path = Path(temp_name)
    report_exists = report_path.is_file()
    report_error = None
    try:
        report = load_json(report_path) if report_exists else {"summary": {}, "issues": []}
    except (ValueError, OSError) as exc:
        report = {"summary": {}, "issues": []}
        report_error = str(exc)
    finally:
        report_path.unlink(missing_ok=True)

    report_valid = (
        isinstance(report, dict)
        and isinstance(report.get("summary"), dict)
        and isinstance(report.get("issues"), list)
        and all(isinstance(issue, dict) for issue in report["issues"])
    )
    issues = report["issues"] if report_valid else []
    error_count = sum(1 for issue in issues if str(issue.get("severity", "")).lower() == "error")
    warning_counts = collections.Counter(
        str(issue.get("code", "UNKNOWN"))
        for issue in issues
        if str(issue.get("severity", "")).lower() == "warning"
    )
    execution_ok = result["returncode"] == 0 and report_exists and report_error is None and report_valid
    checks = [
        {
            "label": "public-format-check-executed",
            "pass": execution_ok,
            "detail": f"returncode={result['returncode']}, report_exists={report_exists}, report_valid={report_valid}, report_error={report_error}",
        },
        {
            "label": "public-format-errors-zero",
            "pass": error_count == 0,
            "detail": f"errors={error_count}",
        },
    ]
    # Warnings remain visible; an outdated numerical ceiling does not decide publication.
    result["pass"] = execution_ok and error_count == 0
    result["warning_counts"] = dict(sorted(warning_counts.items()))
    result["summary"] = report.get("summary", {})
    return result, checks


def display_command(command: list[str]) -> str:
    shown = list(command)
    if shown and Path(shown[0]).resolve() == Path(sys.executable).resolve():
        shown[0] = "python"
    for i, value in enumerate(shown):
        if i > 0 and shown[i - 1] == "--json-log":
            shown[i] = "<temporary-json-report>"
    return " ".join(shown)


def markdown_report(mode: str, overall: bool, command_results: list[dict[str, Any]], data_checks: list[dict[str, Any]], public_format: dict[str, Any], cfg: dict[str, Any], target_release: str) -> str:
    status = "PASS" if overall else "BLOCKED"
    lines = [
        "# DN-6 Release Gate Report / DN-6 リリースゲート報告",
        "",
        f"> Gate: `{cfg['gate']['id']}`",
        f"> Target: `{target_release}`",
        f"> Mode: `{mode}`",
        f"> Result: **{status}**",
        "",
        "## 1. 判定",
        "",
    ]
    if overall:
        lines.append(f"{target_release} のこのモードに必要な機械検証は通過した。warning は観測として保持し、公開エラーとは混同しない。")
    else:
        lines.append("少なくとも一つの release blocker が残っている。失敗した項目を解消するまで、このモードではリリース可能と判定しない。")
    lines += ["", "## 2. Required checks", ""]
    for result in command_results:
        mark = "PASS" if result.get("pass") else "FAIL"
        cmd = display_command(result.get("command", []))
        lines.append(f"- **{mark}** `{result['label']}` — `{cmd}`")
    lines += ["", "## 3. Data / boundary checks", ""]
    for check in data_checks:
        mark = "PASS" if check.get("pass") else "FAIL"
        lines.append(f"- **{mark}** `{check['label']}` — {check.get('detail', '')}")
    lines += ["", "## 4. Public format warning debt", ""]
    summary = public_format.get("summary", {})
    lines.append(f"- Errors: {summary.get('errors', 0)}")
    lines.append(f"- Warnings: {summary.get('warnings', 0)}")
    lines.append(f"- Info: {summary.get('info', 0)}")
    lines.append("")
    for code, count in sorted(public_format.get("warning_counts", {}).items()):
        lines.append(f"- `{code}`: {count}")
    lines += [
        "",
        "## 5. 今回のrelease blockerにしない Developer 系",
        "",
    ]
    for item in cfg.get("v5_1_deferred_developer_work", []):
        lines.append(f"- {item}")
    lines += [
        "",
        "## 6. Publication mode",
        "",
        "release-candidate gate と実公開 gate は分離する。Zenodo の版固有 DOI、公開日、published status が確定するまで、それらを推測して埋めない。",
        "",
        "```powershell",
        "python scripts/check_dn6_release_gate.py --mode publication",
        "```",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run DN-6 release integration gate.")
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--config", type=Path, default=None)
    parser.add_argument("--mode", choices=["release_candidate", "publication"], default="release_candidate")
    parser.add_argument("--write-report", action="store_true", help="Write tools/DN6_RELEASE_GATE_REPORT.ja.md")
    args = parser.parse_args()

    root = args.root.resolve()
    config_path = args.config.resolve() if args.config else root / "tools" / "dn6_release_gate.yml"
    if not config_path.exists():
        print(f"DN-6 RELEASE GATE BLOCKED: missing config {config_path}", file=sys.stderr)
        return 1
    cfg = load_yaml(config_path)

    visibility = "public" if args.mode == "publication" else "preview"
    commands = [
        (
            "index-fresh",
            [
                sys.executable,
                "scripts/build_docs_index.py",
                "--visibility",
                visibility,
                "--check",
            ],
        ),
        (
            "graph-fresh",
            [
                sys.executable,
                "scripts/build_docs_graph.py",
                "--visibility",
                visibility,
                "--check",
            ],
        ),
        ("public-graph-fresh", [sys.executable, "scripts/build_public_graph.py", "--check"]),
        ("public-catalog-fresh", [sys.executable, "scripts/build_public_catalog.py", "--check"]),
        ("search-browse-regression", [sys.executable, "scripts/query_docs.py", "test"]),
        ("graph-regression", [sys.executable, "scripts/query_docs.py", "graph-test"]),
        ("web-parity", ["node", "scripts/check_docs_web_parity.mjs"]),
        ("language-resolution", ["node", "scripts/check_navigator_language_resolution.mjs"]),
        ("reader-boundary", [sys.executable, "scripts/serve_navigator.py", "--check"]),
        ("navigator-interface", [sys.executable, "scripts/check_navigator_interface.py"]),
    ]
    # Publication --release-check subsumes ordinary --check; do not execute both.
    release_flag = "--release-check" if args.mode == "publication" else "--check"
    commands.append(("release-metadata-sync", [sys.executable, "90_Repository_Governance/Release_Update/release_update.py", release_flag]))

    command_results = [run_command(root, label, command) for label, command in commands]
    pf_result, pf_checks = public_format_check(root, cfg)
    command_results.append(pf_result)
    data_checks = gate_data_checks(root, cfg) + pf_checks

    overall = all(item.get("pass") for item in command_results) and all(item.get("pass") for item in data_checks)

    print(f"DN-6 RELEASE GATE {'PASS' if overall else 'BLOCKED'} ({args.mode})")
    for item in command_results:
        print(f"{'PASS' if item.get('pass') else 'FAIL'} {item['label']}")
        if not item.get("pass"):
            tail = (item.get("stdout", "") + "\n" + item.get("stderr", "")).strip().splitlines()[-8:]
            for line in tail:
                print(f"  {line}")
    for item in data_checks:
        print(f"{'PASS' if item.get('pass') else 'FAIL'} {item['label']}: {item.get('detail', '')}")

    if args.write_report:
        state = load_yaml(root / "90_Repository_Governance" / "Release_Update" / "release_state.yml")
        target_release = str(state.get("release", {}).get("display_version", "unresolved"))
        report = markdown_report(args.mode, overall, command_results, data_checks, pf_result, cfg, target_release)
        (root / "tools" / "DN6_RELEASE_GATE_REPORT.ja.md").write_text(report, encoding="utf-8", newline="\n")
        print("WROTE tools/DN6_RELEASE_GATE_REPORT.ja.md")

    return 0 if overall else 1


if __name__ == "__main__":
    raise SystemExit(main())

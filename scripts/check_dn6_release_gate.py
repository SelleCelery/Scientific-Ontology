#!/usr/bin/env python3
"""DN-6 release integration gate for Scientific Ontology v5.0.

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
    expected = cfg["expected_public_state"]
    boundary = cfg["public_boundary"]
    checks: list[dict[str, Any]] = []

    catalog = load_json(root / "tools" / "docs_public_catalog.json")
    graph = load_json(root / "tools" / "docs_graph.json")
    public_graph = load_json(root / "tools" / "docs_public_graph.json")
    manifest = load_yaml(root / "tools" / "docs_manifest.yml")

    source = catalog.get("source", {})
    facts = {
        "catalog_documents": len(catalog.get("documents", [])),
        "registered_documents": source.get("registered_documents"),
        "provisional_documents": source.get("provisional_documents"),
        "language_pair_families": source.get("language_pair_families"),
        "graph_nodes": len(graph.get("nodes", [])),
        "graph_edges": len(graph.get("edges", [])),
        "observed_unregistered_documents": len(graph.get("diagnostics", {}).get("observed_unregistered_documents", [])),
    }
    for key, actual in facts.items():
        wanted = expected.get(key)
        checks.append({
            "label": f"expected:{key}",
            "pass": actual == wanted,
            "detail": f"actual={actual!r}, expected={wanted!r}",
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
    report = load_json(report_path) if report_path.exists() else {"summary": {}, "issues": []}
    report_path.unlink(missing_ok=True)

    error_count = sum(1 for issue in report.get("issues", []) if str(issue.get("severity", "")).lower() == "error")
    warning_counts = collections.Counter(
        str(issue.get("code", "UNKNOWN"))
        for issue in report.get("issues", [])
        if str(issue.get("severity", "")).lower() == "warning"
    )
    ceilings = {str(k): int(v) for k, v in cfg.get("public_format_warning_ceiling", {}).items()}
    unknown = sorted(set(warning_counts) - set(ceilings))
    exceeded = sorted((code, count, ceilings.get(code, -1)) for code, count in warning_counts.items() if count > ceilings.get(code, -1))

    checks = [
        {
            "label": "public-format-errors-zero",
            "pass": error_count == 0,
            "detail": f"errors={error_count}",
        },
        {
            "label": "public-format-warning-codes-known",
            "pass": not unknown,
            "detail": "none" if not unknown else ", ".join(unknown),
        },
        {
            "label": "public-format-warning-debt-not-increased",
            "pass": not exceeded,
            "detail": "none" if not exceeded else "; ".join(f"{c}={n}>{m}" for c, n, m in exceeded),
        },
    ]
    # The raw checker may return non-zero because of errors. The explicit checks above own gate semantics.
    result["pass"] = error_count == 0 and not unknown and not exceeded
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


def markdown_report(mode: str, overall: bool, command_results: list[dict[str, Any]], data_checks: list[dict[str, Any]], public_format: dict[str, Any], cfg: dict[str, Any]) -> str:
    status = "PASS" if overall else "BLOCKED"
    lines = [
        "# DN-6 Release Gate Report / DN-6 リリースゲート報告",
        "",
        f"> Gate: `{cfg['gate']['id']}`",
        f"> Target: `{cfg['gate']['target_release']}`",
        f"> Mode: `{mode}`",
        f"> Result: **{status}**",
        "",
        "## 1. 判定",
        "",
    ]
    if overall:
        lines.append("v5.0 のこのモードに必要な機械検証は通過した。既知 warning は解決済みとは扱わず、設定された上限内の技術負債として保持する。")
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
        ceiling = cfg.get("public_format_warning_ceiling", {}).get(code)
        lines.append(f"- `{code}`: {count} / ceiling {ceiling}")
    lines += [
        "",
        "## 5. v5.1 以降へ持ち越す Developer 系",
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

    commands = [
        ("index-fresh", [sys.executable, "scripts/build_docs_index.py", "--check"]),
        ("graph-fresh", [sys.executable, "scripts/build_docs_graph.py", "--check"]),
        ("public-graph-fresh", [sys.executable, "scripts/build_public_graph.py", "--check"]),
        ("public-catalog-fresh", [sys.executable, "scripts/build_public_catalog.py", "--check"]),
        ("search-browse-regression", [sys.executable, "scripts/query_docs.py", "test"]),
        ("graph-regression", [sys.executable, "scripts/query_docs.py", "graph-test"]),
        ("web-parity", ["node", "scripts/check_docs_web_parity.mjs"]),
        ("language-resolution", ["node", "scripts/check_navigator_language_resolution.mjs"]),
        ("reader-boundary", [sys.executable, "scripts/serve_navigator.py", "--check"]),
        ("navigator-interface", [sys.executable, "scripts/check_navigator_interface.py"]),
        ("release-metadata-sync", [sys.executable, "90_Repository_Governance/Release_Update/release_update.py", "--check"]),
    ]
    if args.mode == "publication":
        commands.append(("publication-release-check", [sys.executable, "90_Repository_Governance/Release_Update/release_update.py", "--release-check"]))

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
        report = markdown_report(args.mode, overall, command_results, data_checks, pf_result, cfg)
        (root / "tools" / "DN6_RELEASE_GATE_REPORT.ja.md").write_text(report, encoding="utf-8", newline="\n")
        print("WROTE tools/DN6_RELEASE_GATE_REPORT.ja.md")

    return 0 if overall else 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Static contract checks for the Developer Registration Workbench."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "navigator" / "src" / "app.ts"
DEV = ROOT / "navigator" / "dev.html"
PUBLIC = ROOT / "navigator" / "index.html"
SCHEMA = ROOT / "tools" / "docs_registration_review.schema.json"
VALIDATOR = ROOT / "scripts" / "validate_registration_review.py"
APPLIER = ROOT / "scripts" / "apply_registration_review.py"
DOC = ROOT / "tools" / "DOCS_REGISTRATION_WORKBENCH.md"
REGISTERED_REVIEW_SOURCE = ROOT / "tools" / "docs_registered_reader_question_review.yml"
REGISTERED_REVIEW_PREVIEW = ROOT / "tools" / "docs_registered_reader_question_review.preview.json"
REGISTERED_REVIEW_BUILDER = ROOT / "scripts" / "build_registered_reader_question_review_preview.py"


def fail(message: str) -> int:
    print(f"REGISTRATION WORKBENCH CHECK FAIL: {message}", file=sys.stderr)
    return 1


def main() -> int:
    paths = (
        APP,
        DEV,
        PUBLIC,
        SCHEMA,
        VALIDATOR,
        APPLIER,
        DOC,
        REGISTERED_REVIEW_SOURCE,
        REGISTERED_REVIEW_PREVIEW,
        REGISTERED_REVIEW_BUILDER,
    )
    for path in paths:
        if not path.is_file():
            return fail(f"missing {path.relative_to(ROOT)}")
        try:
            path.read_bytes().decode("utf-8", errors="strict")
        except UnicodeDecodeError as exc:
            return fail(f"not strict UTF-8: {path.relative_to(ROOT)}: {exc}")

    app = APP.read_text(encoding="utf-8")
    public = PUBLIC.read_text(encoding="utf-8")
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    required = (
        'const REVIEW_STORAGE_PREFIX = "scientific-ontology-registration-review:"',
        'const REGISTERED_REVIEW_URL = "../tools/docs_registered_reader_question_review.preview.json";',
        "function reviewExportPayload()",
        'schema_version: "0.2"',
        "registered_review_seed_sha256",
        "function downloadReviewExport()",
        'exportButton.addEventListener("click", downloadReviewExport)',
        "async function importReviewExport(file: File)",
        "function renderManualCandidate()",
        "function addRevisionCandidate(doc: JsonObject)",
        "function renderRegisteredRevisionProposal(path: string)",
        "function reviewPoolItems()",
        'isDeveloper() && params.get("view") === "manual-candidate"',
        'isDeveloper() && params.get("view") === "registered-review"',
        "candidate_source_sha256",
        "manifest_sha256",
        "graph_sha256",
        "before: baseline, after",
    )
    for fragment in required:
        if fragment not in app:
            return fail(f"missing workbench runtime fragment: {fragment}")

    versions = (
        schema.get("properties", {})
        .get("registration_review", {})
        .get("properties", {})
        .get("schema_version", {})
        .get("enum", [])
    )
    if "0.2" not in versions:
        return fail("review schema does not accept schema_version 0.2")

    if "docs_registration_review" in public or "Registration Workbench" in public:
        return fail("public HTML exposes workbench marker")
    for fragment in ('method: "POST"', "method: 'POST'"):
        if fragment in app:
            return fail(f"browser workbench contains direct write transport: {fragment}")

    preview = json.loads(REGISTERED_REVIEW_PREVIEW.read_text(encoding="utf-8"))
    payload = preview.get("registered_reader_question_review") or {}
    proposals = payload.get("documents") or []
    if not proposals:
        return fail("registered revision preview contains no proposals")
    if not str((payload.get("source") or {}).get("review_seed_sha256") or ""):
        return fail("registered revision preview lacks review_seed_sha256")

    print(
        "REGISTRATION WORKBENCH CHECK PASS: unified provisional/registered review pool, "
        f"{len(proposals)} registered revision proposals, explicit export/import, no browser write API"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

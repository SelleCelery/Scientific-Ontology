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
PROPOSALS = ROOT / "tools" / "docs_revision_proposals.yml"
PROPOSAL_SCHEMA = ROOT / "tools" / "docs_revision_proposals.schema.json"
WORKBENCH_PREVIEW = ROOT / "tools" / "docs_registration_workbench.preview.json"
WORKBENCH_BUILDER = ROOT / "scripts" / "build_registration_workbench_preview.py"

sys.path.insert(0, str(ROOT / "scripts"))
import build_registration_workbench_preview as workbench_builder  # noqa: E402


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
        PROPOSALS,
        PROPOSAL_SCHEMA,
        WORKBENCH_PREVIEW,
        WORKBENCH_BUILDER,
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
        'const REGISTRATION_WORKBENCH_URL = "../tools/docs_registration_workbench.preview.json";',
        "function reviewExportPayload()",
        'schema_version: "0.3"',
        "revision_proposals_sha256",
        "function downloadReviewExport()",
        'exportButton.addEventListener("click", downloadReviewExport)',
        "async function importReviewExport(file: File)",
        "function renderManualCandidate()",
        "function addRevisionCandidate(doc: JsonObject)",
        "function renderRegisteredRevisionProposal(path: string)",
        "function reviewPoolItems()",
        'isDeveloper() && params.get("view") === "manual-candidate"',
        'isDeveloper() && params.get("view") === "registered-review"',
        "manifest_sha256",
        "graph_sha256",
        "before: baseline, after",
    )
    for fragment in required:
        if fragment not in app:
            return fail(f"missing workbench runtime fragment: {fragment}")

    version = (
        schema.get("properties", {})
        .get("registration_review", {})
        .get("properties", {})
        .get("schema_version", {})
        .get("const")
    )
    if version != "0.3":
        return fail("review schema must require schema_version 0.3")

    if "docs_registration_review" in public or "Registration Workbench" in public:
        return fail("public HTML exposes workbench marker")

    # Assessment Lab legitimately uses POST to the local runner.  Only canonical
    # registration/manifest write transports are forbidden in browser code.
    forbidden_write_markers = (
        "REGISTRATION_WRITE_URL",
        "/api/registration/apply",
        "/api/manifest/write",
        "/api/docs_manifest/write",
    )
    for marker in forbidden_write_markers:
        if marker in app:
            return fail(f"browser workbench contains canonical write transport: {marker}")

    preview = json.loads(WORKBENCH_PREVIEW.read_text(encoding="utf-8"))
    expected_preview = workbench_builder.build_payload(ROOT)
    if preview != expected_preview:
        return fail("docs_registration_workbench.preview.json is stale; rebuild it from current manifest/proposals")
    payload = preview.get("registration_workbench") or {}
    provisional = payload.get("provisional_documents") or []
    registered = payload.get("registered_documents") or []
    proposals = payload.get("revision_proposals") or []
    source = payload.get("source") or {}
    if not isinstance(provisional, list) or not isinstance(registered, list) or not isinstance(proposals, list):
        return fail("workbench preview review collections must be arrays")
    for key in ("manifest_sha256", "graph_sha256", "revision_proposals_sha256"):
        if not str(source.get(key) or ""):
            return fail(f"workbench preview lacks {key}")

    print(
        "REGISTRATION WORKBENCH CHECK PASS: manifest-backed provisional review, "
        f"{len(provisional)} provisional + {len(proposals)} revision proposals, "
        "explicit export/import/apply boundary, no browser canonical write API"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

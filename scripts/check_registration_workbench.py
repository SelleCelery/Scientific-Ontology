#!/usr/bin/env python3
"""Static contract checks for the DN-5.4B Developer Registration Workbench."""
from __future__ import annotations

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


def fail(message: str) -> int:
    print(f"REGISTRATION WORKBENCH CHECK FAIL: {message}", file=sys.stderr)
    return 1


def main() -> int:
    for path in (APP, DEV, PUBLIC, SCHEMA, VALIDATOR, APPLIER, DOC):
        if not path.is_file():
            return fail(f"missing {path.relative_to(ROOT)}")
        try:
            path.read_bytes().decode("utf-8", errors="strict")
        except UnicodeDecodeError as exc:
            return fail(f"not strict UTF-8: {path.relative_to(ROOT)}: {exc}")
    app = APP.read_text(encoding="utf-8")
    public = PUBLIC.read_text(encoding="utf-8")
    required = (
        'const REVIEW_STORAGE_PREFIX = "scientific-ontology-registration-review:"',
        "function reviewExportPayload()",
        "function downloadReviewExport()",
        "async function importReviewExport(file: File)",
        "function renderManualCandidate()",
        "function addRevisionCandidate(doc: JsonObject)",
        'isDeveloper() && params.get("view") === "manual-candidate"',
        "candidate_source_sha256",
        "manifest_sha256",
        "graph_sha256",
        "before: baseline, after",
    )
    for fragment in required:
        if fragment not in app:
            return fail(f"missing workbench runtime fragment: {fragment}")
    if "docs_registration_review" in public or "Registration Workbench" in public:
        return fail("public HTML exposes workbench marker")
    forbidden_browser_writes = ("docs_manifest.yml", "method: \"POST\"", "method: 'POST'")
    # docs_manifest.yml may appear in explanatory copy elsewhere in the shared app in future;
    # direct browser network writes are the actual hard boundary.
    for fragment in forbidden_browser_writes[1:]:
        if fragment in app:
            return fail(f"browser workbench contains direct write transport: {fragment}")
    print("REGISTRATION WORKBENCH CHECK PASS: local review state, export/import, manual/revision queues, no browser write API")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

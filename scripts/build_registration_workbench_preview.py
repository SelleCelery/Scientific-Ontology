#!/usr/bin/env python3
"""Build the single Developer Registration Workbench read model.

The canonical manifest is the read source for provisional registrations. A separate
revision-proposal ledger holds only active proposed metadata changes for already
registered documents. The browser reads the generated JSON and never writes YAML.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_REL = Path("tools/docs_manifest.yml")
GRAPH_REL = Path("tools/docs_graph.json")
REVISION_REL = Path("tools/docs_revision_proposals.yml")
OUTPUT_REL = Path("tools/docs_registration_workbench.preview.json")

REVIEW_FIELDS = (
    "path",
    "doc_id",
    "document_type",
    "title_ja",
    "title_en",
    "layer",
    "status",
    "scope",
    "public_profile",
    "state",
    "registration_state",
    "role_ja",
    "role_en",
    "language_relation",
    "discovery",
)
REVISION_PATCH_FIELDS = {
    "document_type",
    "title_ja",
    "title_en",
    "layer",
    "status",
    "scope",
    "public_profile",
    "state",
    "role_ja",
    "role_en",
    "language_relation",
    "discovery",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml_object(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path.name} root must be an object")
    return data


def fallback_doc_id(path_value: str) -> str:
    value = path_value.lower()
    if value.endswith(".md"):
        value = value[:-3]
    value = re.sub(r"[^a-z0-9]+", "_", value).strip("_")
    return value or "document"


def normalized_entry(entry: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(entry)
    discovery = result.get("discovery")
    if not isinstance(discovery, dict):
        discovery = {}
        result["discovery"] = discovery
    discovery.setdefault("topics", [])
    aliases = discovery.get("aliases")
    if not isinstance(aliases, dict):
        aliases = {}
        discovery["aliases"] = aliases
    aliases.setdefault("ja", [])
    aliases.setdefault("en", [])
    questions = discovery.get("reader_questions")
    if not isinstance(questions, dict):
        questions = {}
        discovery["reader_questions"] = questions
    questions.setdefault("ja", [])
    questions.setdefault("en", [])
    discovery.setdefault("entry_level", "")
    return result


def review_projection(entry: dict[str, Any]) -> dict[str, Any]:
    normalized = normalized_entry(entry)
    path = str(normalized.get("path") or "")
    normalized["doc_id"] = str(normalized.get("doc_id") or fallback_doc_id(path))
    return {key: copy.deepcopy(normalized[key]) for key in REVIEW_FIELDS if key in normalized}


def deep_merge(base: dict[str, Any], patch: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(base)
    for key, value in patch.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = copy.deepcopy(value)
    return result


def partial_matches(current: Any, expected: Any) -> bool:
    if isinstance(expected, dict):
        if not isinstance(current, dict):
            return False
        return all(key in current and partial_matches(current[key], value) for key, value in expected.items())
    return current == expected


def manifest_documents(root: Path) -> tuple[list[dict[str, Any]], str]:
    path = root / MANIFEST_REL
    data = load_yaml_object(path)
    docs = data.get("documents")
    if not isinstance(docs, list):
        raise ValueError("docs_manifest.yml documents must be an array")
    objects = [item for item in docs if isinstance(item, dict)]
    return objects, sha256(path)


def revision_source(root: Path) -> tuple[list[dict[str, Any]], str]:
    path = root / REVISION_REL
    data = load_yaml_object(path)
    payload = data.get("revision_proposals")
    if not isinstance(payload, dict):
        raise ValueError("revision_proposals root object is required")
    if str(payload.get("schema_version") or "") != "0.1":
        raise ValueError("revision_proposals schema_version must be 0.1")
    proposals = payload.get("proposals")
    if not isinstance(proposals, list):
        raise ValueError("revision_proposals.proposals must be an array")
    return [item for item in proposals if isinstance(item, dict)], sha256(path)


def build_payload(root: Path) -> dict[str, Any]:
    docs, manifest_hash = manifest_documents(root)
    by_path = {str(item.get("path") or ""): item for item in docs if str(item.get("path") or "")}
    provisional_entries = [item for item in docs if str(item.get("registration_state") or "") == "provisional"]
    registered_entries = [item for item in docs if str(item.get("registration_state") or "") == "registered"]
    provisional_entries.sort(key=lambda item: str(item.get("path") or ""))
    registered_entries.sort(key=lambda item: str(item.get("path") or ""))

    provisional_documents = []
    for entry in provisional_entries:
        baseline = review_projection(entry)
        path = str(entry.get("path") or "")
        doc_id = str(entry.get("doc_id") or "")
        if not path or not doc_id:
            raise ValueError(f"provisional manifest entry requires path and doc_id: {path or '<empty>'}")
        provisional_documents.append({"path": path, "doc_id": doc_id, "baseline": baseline})

    registered_documents = []
    for entry in registered_entries:
        path = str(entry.get("path") or "")
        if not path:
            raise ValueError("registered manifest entry requires path")
        baseline = review_projection(entry)
        registered_documents.append({"path": path, "doc_id": str(baseline.get("doc_id") or ""), "baseline": baseline})

    proposals, revision_hash = revision_source(root)
    revision_proposals = []
    seen_ids: set[str] = set()
    seen_paths: set[str] = set()
    for proposal in proposals:
        proposal_id = str(proposal.get("proposal_id") or "")
        path = str(proposal.get("path") or "")
        if not proposal_id or proposal_id in seen_ids:
            raise ValueError(f"duplicate/empty revision proposal_id: {proposal_id!r}")
        if not path or path in seen_paths:
            raise ValueError(f"duplicate/empty revision proposal path: {path!r}")
        seen_ids.add(proposal_id)
        seen_paths.add(path)
        entry = by_path.get(path)
        if not entry:
            raise ValueError(f"revision proposal path is not in manifest: {path}")
        if str(entry.get("registration_state") or "") != "registered":
            raise ValueError(f"revision proposal target must already be registered: {path}")
        before_patch = proposal.get("before")
        after_patch = proposal.get("after")
        if not isinstance(before_patch, dict) or not isinstance(after_patch, dict):
            raise ValueError(f"revision proposal before/after must be objects: {path}")
        forbidden = (set(before_patch) | set(after_patch)) - REVISION_PATCH_FIELDS
        if forbidden:
            raise ValueError(f"revision proposal touches non-workbench field(s) {sorted(forbidden)}: {path}")
        if not partial_matches(normalized_entry(entry), before_patch):
            raise ValueError(f"revision proposal baseline is stale at targeted fields: {path}")
        baseline = review_projection(entry)
        after = deep_merge(baseline, after_patch)
        if after == baseline:
            raise ValueError(f"revision proposal contains no change: {path}")
        revision_proposals.append(
            {
                "proposal_id": proposal_id,
                "path": path,
                "doc_id": str(entry.get("doc_id") or fallback_doc_id(path)),
                "source_kind": str(proposal.get("source_kind") or "metadata_revision"),
                "review_note": str(proposal.get("review_note") or ""),
                "before": baseline,
                "after": after,
            }
        )
    revision_proposals.sort(key=lambda item: (str(item.get("path") or ""), str(item.get("proposal_id") or "")))

    graph_path = root / GRAPH_REL
    if not graph_path.is_file():
        raise ValueError(f"missing graph read model: {GRAPH_REL.as_posix()}")

    return {
        "registration_workbench": {
            "schema_version": "0.3",
            "source": {
                "manifest_path": MANIFEST_REL.as_posix(),
                "manifest_sha256": manifest_hash,
                "graph_path": GRAPH_REL.as_posix(),
                "graph_sha256": sha256(graph_path),
                "revision_proposals_path": REVISION_REL.as_posix(),
                "revision_proposals_sha256": revision_hash,
                "preview_contract": "manifest-backed Developer read model; browser writes no canonical YAML",
            },
            "summary": {
                "provisional_documents": len(provisional_documents),
                "registered_documents": len(registered_documents),
                "registered_revision_proposals": len(revision_proposals),
            },
            "provisional_documents": provisional_documents,
            "registered_documents": registered_documents,
            "revision_proposals": revision_proposals,
        }
    }


def serialize(data: dict[str, Any]) -> bytes:
    return (json.dumps(data, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the Developer Registration Workbench preview from current sources.")
    parser.add_argument("--root", default=str(ROOT))
    parser.add_argument("--output", default=str(OUTPUT_REL))
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    output = root / args.output
    try:
        payload = build_payload(root)
        generated = serialize(payload)
    except Exception as exc:
        print(f"REGISTRATION WORKBENCH PREVIEW BUILD FAILED: {exc}", file=sys.stderr)
        return 1
    if args.check:
        if not output.is_file():
            print(f"REGISTRATION WORKBENCH PREVIEW CHECK FAILED: missing {output.relative_to(root)}", file=sys.stderr)
            return 1
        if output.read_bytes() != generated:
            print("REGISTRATION WORKBENCH PREVIEW CHECK FAILED: generated preview is stale", file=sys.stderr)
            return 1
        summary = payload["registration_workbench"]["summary"]
        print(
            "REGISTRATION WORKBENCH PREVIEW CHECK PASS: "
            f"{summary['provisional_documents']} provisional + "
            f"{summary['registered_revision_proposals']} revision proposals"
        )
        return 0
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(generated)
    summary = payload["registration_workbench"]["summary"]
    print(
        "REGISTRATION WORKBENCH PREVIEW BUILT: "
        f"{output.relative_to(root)} ({summary['provisional_documents']} provisional + "
        f"{summary['registered_revision_proposals']} revision proposals)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

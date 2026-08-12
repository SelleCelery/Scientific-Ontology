#!/usr/bin/env python3
"""Build the public Navigator catalog from canonical index + public-safe provisional candidates.

This is a read model, not a canonical registry. It intentionally strips candidate-review
metadata and never invents concept ownership or typed logical relations.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "tools" / "docs_index.json"
CANDIDATES = ROOT / "tools" / "docs_registration_candidates.yml"
OUTPUT = ROOT / "tools" / "docs_public_catalog.json"

sys.path.insert(0, str(ROOT / "scripts"))
import build_docs_index  # noqa: E402

CATALOG_CONTRACT_VERSION = "0.1"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_json(path: Path) -> tuple[dict[str, Any], bytes]:
    raw = path.read_bytes()
    data = json.loads(raw.decode("utf-8", errors="strict"))
    if not isinstance(data, dict):
        raise ValueError(f"JSON root must be an object: {path}")
    return data, raw


def load_yaml(path: Path) -> tuple[dict[str, Any], bytes]:
    raw = path.read_bytes()
    data = yaml.safe_load(raw.decode("utf-8", errors="strict")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"YAML root must be a mapping: {path}")
    return data, raw


def provisional_id(path_value: str) -> str:
    return "provisional_" + build_docs_index.fallback_doc_id(path_value)


def candidate_search_fields(proposed: dict[str, Any], topics: dict[str, Any]) -> dict[str, list[dict[str, str]]]:
    fields: dict[str, list[dict[str, str]]] = {
        "title": [],
        "owned_concept": [],
        "aliases": [],
        "topics": [],
        "reader_questions": [],
        "role": [],
        "scope": [],
    }
    build_docs_index.add_value(fields, "title", proposed.get("title_ja"), "ja")
    build_docs_index.add_value(fields, "title", proposed.get("title_en"), "en")

    discovery = proposed.get("discovery") if isinstance(proposed.get("discovery"), dict) else {}
    for topic_id in discovery.get("topics") or []:
        topic_id = str(topic_id)
        build_docs_index.add_value(fields, "topics", topic_id, "und")
        topic = topics.get(topic_id, {})
        if isinstance(topic, dict):
            build_docs_index.add_value(fields, "topics", topic.get("ja"), "ja")
            build_docs_index.add_value(fields, "topics", topic.get("en"), "en")
    aliases = discovery.get("aliases") if isinstance(discovery.get("aliases"), dict) else {}
    questions = discovery.get("reader_questions") if isinstance(discovery.get("reader_questions"), dict) else {}
    for lang in ("ja", "en"):
        for value in aliases.get(lang) or []:
            build_docs_index.add_value(fields, "aliases", value, lang)
        for value in questions.get(lang) or []:
            build_docs_index.add_value(fields, "reader_questions", value, lang)
    build_docs_index.add_value(fields, "role", proposed.get("role_ja"), "ja")
    build_docs_index.add_value(fields, "role", proposed.get("role_en"), "en")
    build_docs_index.add_value(fields, "scope", proposed.get("scope"), "und")
    return fields


def build_candidate_document(candidate: dict[str, Any], topics: dict[str, Any]) -> dict[str, Any]:
    path_value = str(candidate.get("path") or "").strip()
    build_docs_index.validate_public_path(path_value)
    if not (ROOT / path_value).is_file():
        raise ValueError(f"Candidate path does not exist: {path_value}")
    proposed = candidate.get("proposed") if isinstance(candidate.get("proposed"), dict) else {}
    discovery = proposed.get("discovery") if isinstance(proposed.get("discovery"), dict) else {}
    unknown_topics = sorted(set(str(v) for v in discovery.get("topics") or []) - set(topics))
    if unknown_topics:
        raise ValueError(f"Unknown public-catalog topic(s) for {path_value}: {', '.join(unknown_topics)}")
    navigation = candidate.get("navigation") if isinstance(candidate.get("navigation"), dict) else {}
    return {
        "id": provisional_id(path_value),
        "id_source": "provisional_path",
        "proposed_doc_id": str(proposed.get("doc_id") or ""),
        "path": path_value,
        "title": {"ja": str(proposed.get("title_ja") or ""), "en": str(proposed.get("title_en") or "")},
        "layer": str(proposed.get("layer") or ""),
        "document_type": str(proposed.get("document_type") or ""),
        "status": str(proposed.get("status") or ""),
        "state": str(proposed.get("state") or "public-candidate"),
        "scope": str(proposed.get("scope") or ""),
        "role": {"ja": str(proposed.get("role_ja") or ""), "en": str(proposed.get("role_en") or "")},
        "language_relation": copy.deepcopy(proposed.get("language_relation")),
        "discovery": {
            "topics": [str(v) for v in discovery.get("topics") or []],
            "aliases": {
                "ja": [str(v) for v in (discovery.get("aliases") or {}).get("ja", [])],
                "en": [str(v) for v in (discovery.get("aliases") or {}).get("en", [])],
            },
            "reader_questions": {
                "ja": [str(v) for v in (discovery.get("reader_questions") or {}).get("ja", [])],
                "en": [str(v) for v in (discovery.get("reader_questions") or {}).get("en", [])],
            },
            "entry_level": str(discovery.get("entry_level") or ""),
        },
        # Provisional publication is navigation/search metadata only. These remain empty
        # until canonical manifest/logical-contract review establishes them.
        "concepts": {"owned": [], "imports": [], "exports": []},
        "relations": {"related": [], "tests": [], "returns_to": [], "delegates": []},
        "search_fields": candidate_search_fields(proposed, topics),
        "registration_state": "provisional",
        "publication": {
            "registration_state": "provisional",
            "visibility": str(navigation.get("visibility") or "secondary"),
            "searchable": bool(navigation.get("searchable", True)),
            "source": "registration_candidate_public_projection",
        },
    }


def validate_alignment(index: dict[str, Any], candidates: dict[str, Any], index_raw: bytes) -> None:
    payload = candidates.get("registration_candidates")
    if not isinstance(payload, dict):
        raise ValueError("registration_candidates root object is required")
    source = payload.get("source") if isinstance(payload.get("source"), dict) else {}
    manifest_hash = str(index.get("source", {}).get("manifest_sha256") or "")
    if str(source.get("manifest_sha256") or "") != manifest_hash:
        raise ValueError("Candidate ledger and canonical index do not reference the same manifest")
    if int(payload.get("summary", {}).get("total_candidates") or 0) != len(payload.get("candidates") or []):
        raise ValueError("Candidate summary count is stale")
    if not index_raw:
        raise ValueError("Canonical index is empty")


def build_catalog(index: dict[str, Any], index_raw: bytes, candidates: dict[str, Any], candidates_raw: bytes) -> dict[str, Any]:
    validate_alignment(index, candidates, index_raw)
    payload = candidates["registration_candidates"]
    topics = index.get("topics") if isinstance(index.get("topics"), dict) else {}

    registered: list[dict[str, Any]] = []
    registered_paths: set[str] = set()
    registered_ids: set[str] = set()
    for source_doc in index.get("documents") or []:
        doc = copy.deepcopy(source_doc)
        doc["registration_state"] = "registered"
        doc["publication"] = {
            "registration_state": "registered",
            "visibility": "canonical",
            "searchable": True,
            "source": "docs_manifest",
        }
        registered.append(doc)
        registered_paths.add(str(doc.get("path") or ""))
        registered_ids.add(str(doc.get("id") or ""))

    provisional: list[dict[str, Any]] = []
    excluded_support = 0
    for candidate in payload.get("candidates") or []:
        if not isinstance(candidate, dict):
            continue
        navigation = candidate.get("navigation") if isinstance(candidate.get("navigation"), dict) else {}
        if not bool(navigation.get("searchable", True)):
            excluded_support += 1
            continue
        doc = build_candidate_document(candidate, topics)
        if doc["path"] in registered_paths:
            raise ValueError(f"Candidate path already exists in canonical index: {doc['path']}")
        if doc["id"] in registered_ids or any(existing["id"] == doc["id"] for existing in provisional):
            raise ValueError(f"Duplicate public-catalog document id: {doc['id']}")
        provisional.append(doc)

    output = copy.deepcopy(index)
    output["catalog_contract_version"] = CATALOG_CONTRACT_VERSION
    output["source"] = {
        **copy.deepcopy(index.get("source") or {}),
        "canonical_index_sha256": sha256_bytes(index_raw),
        "candidate_source_sha256": sha256_bytes(candidates_raw),
        "catalog_mode": "registered_plus_public_provisional",
        "registered_documents": len(registered),
        "provisional_documents": len(provisional),
        "candidate_support_excluded_from_default_discovery": excluded_support,
    }
    output["documents"] = registered + provisional
    return output


def serialize(data: dict[str, Any]) -> bytes:
    return (json.dumps(data, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def nested_keys(value: Any) -> set[str]:
    keys: set[str] = set()
    if isinstance(value, dict):
        for key, child in value.items():
            keys.add(str(key))
            keys.update(nested_keys(child))
    elif isinstance(value, list):
        for child in value:
            keys.update(nested_keys(child))
    return keys


def validate_catalog(data: dict[str, Any]) -> None:
    docs = data.get("documents")
    if not isinstance(docs, list):
        raise ValueError("documents must be an array")
    developer_only_keys = {
        "review", "evidence", "needs_human_judgment", "confidence",
        "recommended_action", "observed_node_id", "reviewer_note",
    }
    ids: set[str] = set()
    paths: set[str] = set()
    for doc in docs:
        if not isinstance(doc, dict):
            raise ValueError("catalog document must be an object")
        doc_id = str(doc.get("id") or "")
        path = str(doc.get("path") or "")
        if not doc_id or doc_id in ids:
            raise ValueError(f"duplicate/empty catalog id: {doc_id}")
        if not path or path in paths:
            raise ValueError(f"duplicate/empty catalog path: {path}")
        ids.add(doc_id)
        paths.add(path)
        build_docs_index.validate_public_path(path)
        if doc.get("registration_state") not in {"registered", "provisional"}:
            raise ValueError(f"invalid registration_state: {path}")
        if not isinstance(doc.get("search_fields"), dict):
            raise ValueError(f"search_fields missing: {path}")
        if doc.get("registration_state") == "provisional":
            leaked = sorted(developer_only_keys.intersection(nested_keys(doc)))
            if leaked:
                raise ValueError(f"developer-only candidate key leaked into public catalog for {path}: {', '.join(leaked)}")
            concepts = doc.get("concepts") if isinstance(doc.get("concepts"), dict) else {}
            relations = doc.get("relations") if isinstance(doc.get("relations"), dict) else {}
            if any(concepts.get(key) for key in ("owned", "imports", "exports")):
                raise ValueError(f"provisional public catalog must not infer concept contracts: {path}")
            if any(relations.get(key) for key in ("related", "tests", "returns_to", "delegates")):
                raise ValueError(f"provisional public catalog must not infer typed logical relations: {path}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build public Navigator catalog from registered + public-safe provisional metadata.")
    parser.add_argument("--root", default=str(ROOT))
    parser.add_argument("--index", default="tools/docs_index.json")
    parser.add_argument("--candidates", default="tools/docs_registration_candidates.yml")
    parser.add_argument("--output", default="tools/docs_public_catalog.json")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    index_path = root / args.index
    candidates_path = root / args.candidates
    output_path = root / args.output
    try:
        index, index_raw = load_json(index_path)
        candidates, candidates_raw = load_yaml(candidates_path)
        generated_data = build_catalog(index, index_raw, candidates, candidates_raw)
        validate_catalog(generated_data)
        generated = serialize(generated_data)
    except Exception as exc:
        print(f"PUBLIC CATALOG BUILD FAILED: {exc}", file=sys.stderr)
        return 1
    if args.check:
        if not output_path.is_file():
            print(f"PUBLIC CATALOG CHECK FAILED: missing {output_path.relative_to(root)}", file=sys.stderr)
            return 1
        if output_path.read_bytes() != generated:
            print("PUBLIC CATALOG CHECK FAILED: generated public catalog is stale", file=sys.stderr)
            return 1
        src = generated_data["source"]
        print(
            "PUBLIC CATALOG CHECK PASS: "
            f"{src['registered_documents']} registered + {src['provisional_documents']} provisional "
            f"({src['candidate_support_excluded_from_default_discovery']} support candidates excluded)"
        )
        return 0
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(generated.decode("utf-8"))
    src = generated_data["source"]
    print(
        "PUBLIC CATALOG BUILT: "
        f"{output_path.relative_to(root)} ({src['registered_documents']} registered + {src['provisional_documents']} provisional)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

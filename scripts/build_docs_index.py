#!/usr/bin/env python3
"""Compile tools/docs_manifest.yml into a deterministic docs_index.json.

The manifest remains the human-maintained source of document identity, role,
relations, and curated discovery metadata. The generated index is a read model.
"""

from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Sequence

try:
    import yaml
except Exception as exc:  # pragma: no cover
    raise SystemExit("PyYAML is required: python -m pip install pyyaml") from exc

SCHEMA_VERSION = "0.2"
DOC_ID_RE = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*$")
PROCESS_MARKER_RE = re.compile(r"^(?:gate[_-]?\d+|u\d+(?:[_-][a-z0-9]+)?)$", re.IGNORECASE)
FORBIDDEN_TEXT = (
    "sandbox:/",
    "/mnt/data",
    "10_PUBLIC_GITHUB",
    "CURRENT_WORK_SPACE",
    "file_000000",
    "myfiles_browser",
)
PRIVATE_PARTS = {"99_Private_Core_Not_Included", ".git", ".github"}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_yaml(path: Path) -> Dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except Exception as exc:
        raise ValueError(f"Could not parse YAML {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"YAML root must be a mapping: {path}")
    return data


def normalize_text(value: Any) -> str:
    text = unicodedata.normalize("NFKC", str(value or ""))
    text = text.casefold()
    chars: List[str] = []
    for char in text:
        category = unicodedata.category(char)
        if category.startswith("P") or category.startswith("S"):
            chars.append(" ")
        else:
            chars.append(char)
    return " ".join("".join(chars).split())


def compact_text(value: Any) -> str:
    return normalize_text(value).replace(" ", "")


def fallback_doc_id(path_value: str) -> str:
    value = path_value.lower()
    if value.endswith(".md"):
        value = value[:-3]
    value = re.sub(r"[^a-z0-9]+", "_", value).strip("_")
    return value or "document"


def validate_public_path(path_value: str) -> None:
    path = Path(path_value)
    if path.is_absolute():
        raise ValueError(f"Absolute path cannot enter document index: {path_value}")
    if "\\" in path_value:
        raise ValueError(f"Manifest path must use POSIX separators: {path_value}")
    for part in path.parts:
        if part in PRIVATE_PARTS:
            raise ValueError(f"Private or operational path cannot enter document index: {path_value}")
        if part.startswith("000"):
            raise ValueError(f"000-prefixed pending path cannot enter document index: {path_value}")
        normalized_part = normalize_text(part).replace(" ", "_")
        if PROCESS_MARKER_RE.match(normalized_part):
            raise ValueError(f"Gate/U support artifact cannot enter document index: {path_value}")
    for marker in FORBIDDEN_TEXT:
        if marker.lower() in path_value.lower():
            raise ValueError(f"Forbidden local/private marker in index path: {path_value}")


def as_list(value: Any) -> List[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def search_value(text: Any, lang: str) -> Dict[str, str]:
    original = str(text or "").strip()
    return {
        "lang": lang,
        "text": original,
        "normalized": normalize_text(original),
        "compact": compact_text(original),
    }


def add_value(target: MutableMapping[str, List[Dict[str, str]]], field: str, text: Any, lang: str) -> None:
    original = str(text or "").strip()
    if not original:
        return
    item = search_value(original, lang)
    seen = {(v["lang"], v["normalized"]) for v in target.setdefault(field, [])}
    key = (item["lang"], item["normalized"])
    if key not in seen:
        target[field].append(item)


def relation_targets(items: Any) -> List[str]:
    targets: List[str] = []
    for item in as_list(items):
        if isinstance(item, dict) and item.get("target"):
            targets.append(str(item["target"]))
        elif isinstance(item, str):
            targets.append(item)
    return sorted(set(targets))


def validate_navigation_topics(topics: Mapping[str, Any]) -> None:
    featured_orders: Dict[int, str] = {}
    for topic_id, raw in topics.items():
        topic_id = str(topic_id)
        if not DOC_ID_RE.fullmatch(topic_id):
            raise ValueError(f"Invalid navigation topic ID: {topic_id}")
        if not isinstance(raw, Mapping):
            raise ValueError(f"Navigation topic must be a mapping: {topic_id}")
        if not str(raw.get("ja", "")).strip() or not str(raw.get("en", "")).strip():
            raise ValueError(f"Navigation topic requires ja/en labels: {topic_id}")
        browse = raw.get("browse")
        if browse is None:
            continue
        if not isinstance(browse, Mapping):
            raise ValueError(f"browse metadata must be a mapping: {topic_id}")
        enabled = bool(browse.get("enabled", False))
        if not enabled:
            continue
        try:
            order = int(browse.get("order"))
        except Exception as exc:
            raise ValueError(f"Featured browse topic requires integer order: {topic_id}") from exc
        if order in featured_orders:
            raise ValueError(
                f"Featured browse topic order collision: {topic_id} and {featured_orders[order]} use {order}"
            )
        featured_orders[order] = topic_id
        for field in ("label", "description", "starter_questions"):
            if not isinstance(browse.get(field), Mapping):
                raise ValueError(f"Featured browse topic requires {field}: {topic_id}")
        for lang in ("ja", "en"):
            if not str(browse["label"].get(lang, "")).strip():
                raise ValueError(f"Featured browse topic requires {lang} label: {topic_id}")
            if not str(browse["description"].get(lang, "")).strip():
                raise ValueError(f"Featured browse topic requires {lang} description: {topic_id}")
            questions = as_list(browse["starter_questions"].get(lang))
            if len(questions) < 2:
                raise ValueError(f"Featured browse topic requires at least 2 {lang} starter questions: {topic_id}")
            if len(questions) > 5:
                print(f"WARNING: more than 5 starter questions ({lang}) in topic {topic_id}", file=sys.stderr)


def build_document(
    raw: Mapping[str, Any],
    concept_ownership: Mapping[str, Any],
    topics: Mapping[str, Any],
    root: Path,
) -> Dict[str, Any]:
    path_value = str(raw.get("path", "")).strip()
    validate_public_path(path_value)
    abs_path = root / path_value
    if not abs_path.exists():
        raise ValueError(f"Indexed manifest path does not exist: {path_value}")

    explicit_id = str(raw.get("doc_id", "")).strip()
    doc_id = explicit_id or fallback_doc_id(path_value)
    if not DOC_ID_RE.fullmatch(doc_id):
        raise ValueError(f"Invalid doc_id '{doc_id}' for {path_value}")

    logical = raw.get("logical_contract", {}) if isinstance(raw.get("logical_contract"), dict) else {}
    owned = {str(v) for v in as_list(logical.get("owns"))}
    for concept_id, config in concept_ownership.items():
        if isinstance(config, dict) and str(config.get("canonical_owner", "")) == path_value:
            owned.add(str(concept_id))
    imports = {str(v) for v in as_list(logical.get("imports"))}
    exports = {str(v) for v in as_list(logical.get("exports"))}

    discovery = raw.get("discovery", {}) if isinstance(raw.get("discovery"), dict) else {}
    discovery_topics = [str(v) for v in as_list(discovery.get("topics"))]
    unknown_topics = sorted(set(discovery_topics) - set(topics.keys()))
    if unknown_topics:
        raise ValueError(f"Unknown topic IDs for {path_value}: {', '.join(unknown_topics)}")

    aliases = discovery.get("aliases", {}) if isinstance(discovery.get("aliases"), dict) else {}
    questions = discovery.get("reader_questions", {}) if isinstance(discovery.get("reader_questions"), dict) else {}
    entry_level = str(discovery.get("entry_level", "")).strip()
    if entry_level and entry_level not in {"foundation", "intermediate", "advanced"}:
        raise ValueError(f"Invalid entry_level '{entry_level}' for {path_value}")

    if len(discovery_topics) > 6:
        print(f"WARNING: more than 6 topics in {path_value}", file=sys.stderr)
    for lang in ("ja", "en"):
        if len(as_list(aliases.get(lang))) > 8:
            print(f"WARNING: more than 8 aliases ({lang}) in {path_value}", file=sys.stderr)
        if len(as_list(questions.get(lang))) > 5:
            print(f"WARNING: more than 5 reader questions ({lang}) in {path_value}", file=sys.stderr)

    fields: Dict[str, List[Dict[str, str]]] = {
        "title": [],
        "owned_concept": [],
        "aliases": [],
        "topics": [],
        "reader_questions": [],
        "role": [],
        "scope": [],
    }
    add_value(fields, "title", raw.get("title_ja"), "ja")
    add_value(fields, "title", raw.get("title_en"), "en")
    for concept_id in sorted(owned):
        add_value(fields, "owned_concept", concept_id, "und")
    for topic_id in discovery_topics:
        add_value(fields, "topics", topic_id, "und")
        topic = topics.get(topic_id, {})
        if isinstance(topic, dict):
            add_value(fields, "topics", topic.get("ja"), "ja")
            add_value(fields, "topics", topic.get("en"), "en")
    for lang in ("ja", "en"):
        for value in as_list(aliases.get(lang)):
            add_value(fields, "aliases", value, lang)
        for value in as_list(questions.get(lang)):
            add_value(fields, "reader_questions", value, lang)
    add_value(fields, "role", raw.get("role_ja"), "ja")
    add_value(fields, "role", raw.get("role_en"), "en")
    add_value(fields, "scope", raw.get("scope"), "und")

    relations = {
        "related": sorted(str(v) for v in as_list(raw.get("related"))),
        "tests": relation_targets(logical.get("tests")),
        "returns_to": relation_targets(logical.get("returns_to")),
        "delegates": relation_targets(logical.get("delegates")),
    }

    return {
        "id": doc_id,
        "id_source": "explicit" if explicit_id else "fallback",
        "path": path_value,
        "title": {
            "ja": str(raw.get("title_ja", "")),
            "en": str(raw.get("title_en", "")),
        },
        "layer": str(raw.get("layer", "")),
        "document_type": str(raw.get("document_type", "")),
        "status": str(raw.get("status", "")),
        "state": str(raw.get("state", "")),
        "scope": str(raw.get("scope", "")),
        "role": {
            "ja": str(raw.get("role_ja", "")),
            "en": str(raw.get("role_en", "")),
        },
        "language_relation": raw.get("language_relation"),
        "discovery": {
            "topics": discovery_topics,
            "aliases": {
                "ja": [str(v) for v in as_list(aliases.get("ja"))],
                "en": [str(v) for v in as_list(aliases.get("en"))],
            },
            "reader_questions": {
                "ja": [str(v) for v in as_list(questions.get("ja"))],
                "en": [str(v) for v in as_list(questions.get("en"))],
            },
            "entry_level": entry_level,
        },
        "concepts": {
            "owned": sorted(owned),
            "imports": sorted(imports),
            "exports": sorted(exports),
        },
        "relations": relations,
        "search_fields": {name: values for name, values in fields.items()},
    }


def validate_index(index: Mapping[str, Any]) -> None:
    required = {"schema_version", "search_spec_version", "source", "search_profile", "topics", "query_expansions", "documents"}
    missing = sorted(required - set(index.keys()))
    if missing:
        raise ValueError("Index missing top-level fields: " + ", ".join(missing))
    if index.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("Unexpected schema_version")
    source = index.get("source")
    if not isinstance(source, dict):
        raise ValueError("source must be an object")
    if source.get("visibility_profile") not in {"preview", "public"}:
        raise ValueError("visibility_profile must be preview or public")
    ids: set[str] = set()
    paths: set[str] = set()
    for doc in index.get("documents", []):
        if not isinstance(doc, dict):
            raise ValueError("document entry must be an object")
        doc_id = str(doc.get("id", ""))
        path_value = str(doc.get("path", ""))
        if not DOC_ID_RE.fullmatch(doc_id):
            raise ValueError(f"Invalid document ID in index: {doc_id}")
        if doc_id in ids:
            raise ValueError(f"Duplicate document ID in index: {doc_id}")
        if path_value in paths:
            raise ValueError(f"Duplicate document path in index: {path_value}")
        ids.add(doc_id)
        paths.add(path_value)
        validate_public_path(path_value)
        fields = doc.get("search_fields")
        if not isinstance(fields, dict):
            raise ValueError(f"search_fields missing for {doc_id}")
        for values in fields.values():
            if not isinstance(values, list):
                raise ValueError(f"search field values must be arrays for {doc_id}")
    serialized = json.dumps(index, ensure_ascii=False)
    for marker in FORBIDDEN_TEXT:
        if marker.lower() in serialized.lower():
            raise ValueError(f"Forbidden local/private marker in generated index: {marker}")


def compile_index(root: Path, manifest_path: Path, search_path: Path, visibility: str) -> Dict[str, Any]:
    manifest_bytes = manifest_path.read_bytes()
    search_bytes = search_path.read_bytes()
    manifest = load_yaml(manifest_path)
    search_data = load_yaml(search_path)
    search = search_data.get("search", {}) if isinstance(search_data.get("search"), dict) else {}
    topics = search.get("navigation_topics", {}) if isinstance(search.get("navigation_topics"), dict) else {}
    expansions = search.get("query_expansions", {}) if isinstance(search.get("query_expansions"), dict) else {}
    if str(search.get("spec_version", "")) != SCHEMA_VERSION:
        raise ValueError(f"docs_search.yml spec_version must be {SCHEMA_VERSION}")
    validate_navigation_topics(topics)

    allowed_states = {"public"} if visibility == "public" else {"public", "public-candidate"}
    documents: List[Dict[str, Any]] = []
    concept_ownership = manifest.get("concept_ownership", {}) if isinstance(manifest.get("concept_ownership"), dict) else {}
    for raw in manifest.get("documents", []):
        if not isinstance(raw, dict):
            continue
        if str(raw.get("state", "")) not in allowed_states:
            continue
        documents.append(build_document(raw, concept_ownership, topics, root))

    documents.sort(key=lambda item: item["id"])
    index = {
        "schema_version": SCHEMA_VERSION,
        "search_spec_version": str(search.get("spec_version", "")),
        "source": {
            "manifest_sha256": sha256_bytes(manifest_bytes),
            "search_config_sha256": sha256_bytes(search_bytes),
            "coverage": str(manifest.get("manifest", {}).get("coverage", "")),
            "visibility_profile": visibility,
        },
        "search_profile": {
            "normalization": search.get("normalization", {}),
            "query_mode": search.get("query_mode", {}),
            "modes": search.get("modes", {}),
            "match_strength": search.get("match_strength", {}),
            "thresholds": search.get("thresholds", {}),
            "question_markers_ja": search.get("question_markers_ja", []),
        },
        "topics": topics,
        "query_expansions": expansions,
        "documents": documents,
    }
    validate_index(index)
    return index


def render_index(index: Mapping[str, Any]) -> str:
    return json.dumps(index, ensure_ascii=False, indent=2, sort_keys=False) + "\n"


def build_parser() -> argparse.ArgumentParser:
    root = repo_root()
    parser = argparse.ArgumentParser(description="Build deterministic Scientific Ontology document index.")
    parser.add_argument("--root", default=str(root))
    parser.add_argument("--manifest", default="tools/docs_manifest.yml")
    parser.add_argument("--search-config", default="tools/docs_search.yml")
    parser.add_argument("--output", default="tools/docs_index.json")
    parser.add_argument("--visibility", choices=["preview", "public"], default="preview")
    parser.add_argument("--check", action="store_true")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = Path(args.root).resolve()
    manifest_path = root / args.manifest
    search_path = root / args.search_config
    output_path = root / args.output
    try:
        index = compile_index(root, manifest_path, search_path, args.visibility)
        rendered = render_index(index)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if args.check:
        if not output_path.exists():
            print(f"STALE: index does not exist: {output_path}", file=sys.stderr)
            return 1
        existing = output_path.read_text(encoding="utf-8")
        try:
            validate_index(json.loads(existing))
        except Exception as exc:
            print(f"INVALID: existing index failed structural validation: {exc}", file=sys.stderr)
            return 1
        if existing != rendered:
            print("STALE: tools/docs_index.json does not match manifest/search configuration.", file=sys.stderr)
            diff = difflib.unified_diff(
                existing.splitlines(), rendered.splitlines(),
                fromfile="tracked", tofile="expected", lineterm=""
            )
            for line in list(diff)[:120]:
                print(line, file=sys.stderr)
            return 1
        print(f"INDEX CHECK PASS ({len(index['documents'])} documents, visibility={args.visibility})")
        return 0

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(rendered, encoding="utf-8", newline="\n")
    print(f"INDEX BUILD PASS ({len(index['documents'])} documents, visibility={args.visibility})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

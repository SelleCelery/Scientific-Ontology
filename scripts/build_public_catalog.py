#!/usr/bin/env python3
"""Build the Public Navigator catalog from the single canonical manifest-derived index.

DN-5.5 contract: provisional documents are canonical ledger entries carrying
registration_state=provisional. The Public catalog is therefore a safe read-model
projection of docs_index.json and no longer merges the candidate ledger at runtime.

DN-5.5 language-resolution extension: every public document receives normalized
presentation metadata used by the browser to select the UI-language counterpart.
The normalization is presentation-only; it does not merge canonical identities.
"""
from __future__ import annotations
import argparse, copy, json, re, sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CATALOG_CONTRACT_VERSION = "0.4"


def _normalized_path(value: Any) -> str:
    return str(value or "").replace("\\", "/")


def _language_for_document(doc: dict[str, Any]) -> str:
    path = _normalized_path(doc.get("path"))
    if re.search(r"\.ja\.md$", path, re.I):
        return "ja"
    if re.search(r"\.en\.md$", path, re.I):
        return "en"

    relation = doc.get("language_relation")
    if isinstance(relation, dict):
        language = str(relation.get("language") or "").lower()
        if language in {"ja", "en"}:
            return language
        if language in {"ja+en", "ja-en", "bilingual", "both"}:
            return "bilingual"
    elif isinstance(relation, str):
        legacy = relation.lower()
        if "japanese_authoritative" in legacy:
            return "ja"
        if "english_commensuration" in legacy:
            return "en"

    return "und"


def _declared_counterpart(doc: dict[str, Any]) -> str:
    relation = doc.get("language_relation")
    if isinstance(relation, dict):
        return _normalized_path(relation.get("counterpart_path"))
    return ""


def _path_counterpart(path: str) -> str:
    if re.search(r"\.ja\.md$", path, re.I):
        return re.sub(r"\.ja\.md$", ".en.md", path, flags=re.I)
    if re.search(r"\.en\.md$", path, re.I):
        return re.sub(r"\.en\.md$", ".ja.md", path, flags=re.I)
    return ""


def _family_key(path: str, counterpart: str) -> str:
    if re.search(r"\.(ja|en)\.md$", path, re.I):
        base = re.sub(r"\.(ja|en)\.md$", ".md", path, flags=re.I)
        return f"path-family:{base}"
    if counterpart:
        return "path-pair:" + "|".join(sorted([path, counterpart]))
    return f"path:{path}"


def _add_presentation_metadata(docs: list[dict[str, Any]]) -> tuple[int, int]:
    paths = {_normalized_path(doc.get("path")) for doc in docs}
    pair_keys: set[str] = set()
    fallback_count = 0

    for doc in docs:
        path = _normalized_path(doc.get("path"))
        language = _language_for_document(doc)
        declared = _declared_counterpart(doc)
        inferred = _path_counterpart(path)
        counterpart = declared if declared in paths else inferred if inferred in paths else ""
        family_key = _family_key(path, counterpart)
        if counterpart:
            pair_keys.add(family_key)
        elif language in {"ja", "en"}:
            fallback_count += 1
        doc["presentation"] = {
            "language": language,
            "family_key": family_key,
            "counterpart_path": counterpart or None,
        }

    return len(pair_keys), fallback_count


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(ROOT))
    ap.add_argument("--index", default="tools/docs_index.json")
    ap.add_argument("--output", default="tools/docs_public_catalog.json")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    root = Path(args.root).resolve()
    ip = root / args.index
    op = root / args.output
    try:
        raw = ip.read_bytes()
        index = json.loads(raw.decode("utf-8"))
        docs: list[dict[str, Any]] = []
        registered = provisional = 0
        for source in index.get("documents") or []:
            d = copy.deepcopy(source)
            rs = str(d.get("registration_state") or "registered")
            if rs not in {"registered", "provisional"}:
                raise ValueError(f'invalid registration_state for {d.get("path")}: {rs}')
            if rs == "registered":
                registered += 1
            else:
                provisional += 1
            d["registration_state"] = rs
            d["publication"] = {
                "registration_state": rs,
                "visibility": str((d.get("discovery") or {}).get("visibility") or ("canonical" if rs == "registered" else "secondary")),
                "searchable": bool((d.get("discovery") or {}).get("searchable", True)),
                "source": "docs_manifest",
            }
            docs.append(d)

        language_pairs, unmatched_language_specific = _add_presentation_metadata(docs)

        out = copy.deepcopy(index)
        out["catalog_contract_version"] = CATALOG_CONTRACT_VERSION
        index_source = copy.deepcopy(index.get("source") or {})
        out["source"] = {
            "coverage": str(index_source.get("coverage") or ""),
            "visibility_profile": str(index_source.get("visibility_profile") or ""),
            "catalog_mode": "single_manifest_registered_plus_provisional",
            "registered_documents": registered,
            "provisional_documents": provisional,
            "catalog_documents": len(docs),
            "language_pair_families": language_pairs,
            "unmatched_language_specific_documents": unmatched_language_specific,
        }
        out["documents"] = docs
        generated = (json.dumps(out, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    except Exception as exc:
        print(f"PUBLIC CATALOG BUILD FAILED: {exc}", file=sys.stderr)
        return 1

    if args.check:
        if not op.is_file() or op.read_bytes() != generated:
            print("PUBLIC CATALOG CHECK FAILED: generated public catalog is stale", file=sys.stderr)
            return 1
        print(
            "PUBLIC CATALOG CHECK PASS: "
            f"{registered} registered + {provisional} provisional = {len(docs)} manifest documents; "
            f"{language_pairs} language-pair families"
        )
        return 0

    op.write_bytes(generated)
    print(
        f"PUBLIC CATALOG BUILT: {op.relative_to(root)} "
        f"({registered} registered + {provisional} provisional = {len(docs)}; "
        f"{language_pairs} language-pair families)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

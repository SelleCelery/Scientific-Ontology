#!/usr/bin/env python3
"""Explainable reference search client for Scientific Ontology documents."""

from __future__ import annotations

import argparse
import json
import math
import sys
import unicodedata
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple
from urllib.parse import quote

try:
    import yaml
except Exception as exc:  # pragma: no cover
    raise SystemExit("PyYAML is required: python -m pip install pyyaml") from exc

METHOD_PRIORITY = {
    "exact": 5,
    "contains": 4,
    "term_coverage": 3,
    "query_expansion": 2,
    "char_ngram": 1,
}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_json(path: Path) -> Dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise ValueError(f"Could not parse JSON {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"JSON root must be an object: {path}")
    return data


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


def ngrams(value: str, n: int) -> set[str]:
    if not value:
        return set()
    if len(value) < n:
        return {value}
    return {value[i:i+n] for i in range(len(value) - n + 1)}


def dice_similarity(a: str, b: str) -> float:
    if not a or not b:
        return 0.0
    n = 2 if min(len(a), len(b)) <= 5 else 3
    left = ngrams(a, n)
    right = ngrams(b, n)
    if not left or not right:
        return 0.0
    return 2.0 * len(left & right) / (len(left) + len(right))


def allowed_lang(entry_lang: str, selected: str) -> bool:
    return selected == "both" or entry_lang == "und" or entry_lang == selected


def known_term_values(index: Mapping[str, Any], lang: str) -> set[str]:
    values: set[str] = set()
    for doc in index.get("documents", []):
        for field in ("title", "aliases", "owned_concept", "topics"):
            for item in doc.get("search_fields", {}).get(field, []):
                if allowed_lang(str(item.get("lang", "und")), lang):
                    norm = str(item.get("normalized", ""))
                    if norm:
                        values.add(norm)
        values.add(normalize_text(doc.get("id", "")))
    return values


def classify_query(query: str, index: Mapping[str, Any], mode: str, lang: str) -> str:
    if mode in {"term", "question"}:
        return mode
    normalized = normalize_text(query)
    compact = normalized.replace(" ", "")
    if normalized in known_term_values(index, lang):
        return "term"
    profile = index.get("search_profile", {})
    markers = [normalize_text(v) for v in profile.get("question_markers_ja", [])]
    if any(marker and marker in normalized for marker in markers):
        return "question"
    if len(compact) >= 18 or len(normalized.split()) >= 5:
        return "question"
    return "term"


def expansion_phrases(group: Mapping[str, Any], lang: str) -> Iterable[Tuple[str, str]]:
    languages = ("ja", "en") if lang == "both" else (lang,)
    for item_lang in languages:
        for phrase in group.get(item_lang, []) or []:
            yield item_lang, str(phrase)


def active_expansion_groups(query: str, index: Mapping[str, Any], lang: str) -> List[str]:
    query_norm = normalize_text(query)
    query_compact = query_norm.replace(" ", "")
    thresholds = index.get("search_profile", {}).get("thresholds", {})
    min_sim = max(float(thresholds.get("char_ngram_min_similarity", 0.28)), 0.46)
    active: List[str] = []
    for group_id, group in index.get("query_expansions", {}).items():
        if not isinstance(group, dict):
            continue
        contacted = False
        for _, phrase in expansion_phrases(group, lang):
            norm = normalize_text(phrase)
            compact = norm.replace(" ", "")
            if not norm:
                continue
            if query_norm == norm or query_norm in norm or norm in query_norm:
                contacted = True
                break
            if min(len(query_compact), len(compact)) >= 4 and dice_similarity(query_compact, compact) >= min_sim:
                contacted = True
                break
        if contacted:
            active.append(str(group_id))
    return sorted(active)


def term_coverage(query_norm: str, text_norm: str) -> float:
    terms = [t for t in query_norm.split() if len(t) >= 2]
    if len(terms) < 2:
        return 0.0
    matched = sum(1 for term in terms if term in text_norm)
    return matched / len(terms)


def match_entry(
    query: str,
    entry: Mapping[str, Any],
    index: Mapping[str, Any],
    active_groups: Sequence[str],
    lang: str,
) -> Dict[str, Any] | None:
    entry_lang = str(entry.get("lang", "und"))
    if not allowed_lang(entry_lang, lang):
        return None
    query_norm = normalize_text(query)
    query_compact = query_norm.replace(" ", "")
    text_norm = str(entry.get("normalized", ""))
    text_compact = str(entry.get("compact", ""))
    profile = index.get("search_profile", {})
    strengths = profile.get("match_strength", {})
    thresholds = profile.get("thresholds", {})
    candidates: List[Dict[str, Any]] = []

    if query_norm and query_norm == text_norm:
        candidates.append({"method": "exact", "strength": float(strengths.get("exact", 1.0)), "expansion_group": None})
    if query_norm and text_norm and (query_norm in text_norm or text_norm in query_norm):
        candidates.append({"method": "contains", "strength": float(strengths.get("contains", 0.9)), "expansion_group": None})

    coverage = term_coverage(query_norm, text_norm)
    if coverage >= 0.5:
        candidates.append({
            "method": "term_coverage",
            "strength": float(strengths.get("term_coverage", 0.75)) * coverage,
            "expansion_group": None,
        })

    min_chars = int(thresholds.get("char_ngram_min_chars", 4))
    min_sim = float(thresholds.get("char_ngram_min_similarity", 0.28))
    if min(len(query_compact), len(text_compact)) >= min_chars:
        sim = dice_similarity(query_compact, text_compact)
        if sim >= min_sim:
            candidates.append({
                "method": "char_ngram",
                "strength": min(float(strengths.get("char_ngram_cap", 0.45)), sim),
                "expansion_group": None,
                "similarity": sim,
            })

    expansion_strength = float(strengths.get("query_expansion", 0.65))
    expansions = index.get("query_expansions", {})
    expansion_allowed = str(entry.get("field", "")) not in {"topics", "owned_concept"}
    if not expansion_allowed:
        active_groups = []
    for group_id in active_groups:
        group = expansions.get(group_id, {})
        if not isinstance(group, dict):
            continue
        for _, phrase in expansion_phrases(group, lang):
            phrase_norm = normalize_text(phrase)
            phrase_compact = phrase_norm.replace(" ", "")
            if not phrase_norm:
                continue
            if phrase_norm == text_norm or phrase_norm in text_norm or text_norm in phrase_norm:
                candidates.append({
                    "method": "query_expansion",
                    "strength": expansion_strength,
                    "expansion_group": group_id,
                    "expansion_phrase": phrase,
                })
            elif min(len(phrase_compact), len(text_compact)) >= min_chars:
                sim = dice_similarity(phrase_compact, text_compact)
                if sim >= min_sim:
                    candidates.append({
                        "method": "query_expansion",
                        "strength": expansion_strength * sim,
                        "expansion_group": group_id,
                        "expansion_phrase": phrase,
                        "similarity": sim,
                    })

    if not candidates:
        return None
    candidates.sort(key=lambda item: (float(item["strength"]), METHOD_PRIORITY.get(str(item["method"]), 0)), reverse=True)
    best = dict(candidates[0])
    best["text"] = str(entry.get("text", ""))
    best["lang"] = entry_lang
    return best


def search_documents(
    query: str,
    index: Mapping[str, Any],
    mode: str = "auto",
    limit: int = 10,
    lang: str = "both",
) -> Tuple[str, List[Dict[str, Any]]]:
    resolved_mode = classify_query(query, index, mode, lang)
    active_groups = active_expansion_groups(query, index, lang)
    modes = index.get("search_profile", {}).get("modes", {})
    weights = modes.get(resolved_mode, {}).get("field_weights", {})
    minimum = float(index.get("search_profile", {}).get("thresholds", {}).get("minimum_result_score", 2.5))
    results: List[Dict[str, Any]] = []

    for doc in index.get("documents", []):
        score = 0.0
        matches: List[Dict[str, Any]] = []
        direct_count = 0
        fields = doc.get("search_fields", {})
        for field, weight in weights.items():
            best: Dict[str, Any] | None = None
            for entry in fields.get(field, []):
                entry_with_field = dict(entry)
                entry_with_field["field"] = field
                candidate = match_entry(query, entry_with_field, index, active_groups, lang)
                if candidate is None:
                    continue
                if best is None or (candidate["strength"], METHOD_PRIORITY.get(candidate["method"], 0)) > (
                    best["strength"], METHOD_PRIORITY.get(best["method"], 0)
                ):
                    best = candidate
            if best is None:
                continue
            contribution = float(weight) * float(best["strength"])
            score += contribution
            if best["method"] in {"exact", "contains", "term_coverage"}:
                direct_count += 1
            best.update({
                "field": field,
                "weight": float(weight),
                "contribution": contribution,
            })
            matches.append(best)
        if score >= minimum:
            matches.sort(key=lambda item: item["contribution"], reverse=True)
            results.append({
                "doc_id": doc["id"],
                "score": round(score, 6),
                "direct_match_count": direct_count,
                "path": doc["path"],
                "title": doc["title"],
                "role": doc["role"],
                "state": doc["state"],
                "entry_level": doc.get("discovery", {}).get("entry_level", ""),
                "matches": matches,
                "active_expansion_groups": active_groups,
            })

    results.sort(key=lambda item: (-float(item["score"]), -int(item["direct_match_count"]), str(item["doc_id"])))
    return resolved_mode, results[:limit]


def display_title(result: Mapping[str, Any], lang: str) -> str:
    title = result.get("title", {})
    if lang == "en":
        return str(title.get("en") or title.get("ja") or result.get("doc_id"))
    return str(title.get("ja") or title.get("en") or result.get("doc_id"))


def result_url(path_value: str, base_url: str | None) -> str:
    if not base_url:
        return path_value
    return base_url.rstrip("/") + "/" + quote(path_value, safe="/")


def print_search(query: str, mode: str, results: Sequence[Mapping[str, Any]], lang: str, base_url: str | None) -> None:
    print(f"Query mode: {mode}")
    if not results:
        print("No results.")
        return
    for position, result in enumerate(results, 1):
        print(f"{position}. {display_title(result, lang)}")
        print(f"   id: {result['doc_id']}")
        print(f"   score: {result['score']:.3f}")
        print(f"   path: {result_url(str(result['path']), base_url)}")
        reasons = list(result.get("matches", []))[:3]
        for reason in reasons:
            suffix = ""
            if reason.get("expansion_group"):
                suffix = f" via {reason['expansion_group']}"
            print(
                f"   - {reason['field']} / {reason['method']}{suffix}: "
                f"+{reason['contribution']:.3f} :: {reason['text']}"
            )


def find_documents(query: str, index: Mapping[str, Any], lang: str) -> List[Dict[str, Any]]:
    norm = normalize_text(query)
    matches: List[Tuple[int, str, Dict[str, Any]]] = []
    for doc in index.get("documents", []):
        values = [normalize_text(doc.get("id", ""))]
        values.extend(str(v.get("normalized", "")) for v in doc.get("search_fields", {}).get("title", []))
        values.extend(str(v.get("normalized", "")) for v in doc.get("search_fields", {}).get("aliases", []))
        rank = 0
        if norm == normalize_text(doc.get("id", "")):
            rank = 4
        elif norm in values:
            rank = 3
        elif any(norm and norm in value for value in values):
            rank = 2
        elif any(value and value in norm for value in values):
            rank = 1
        if rank:
            matches.append((rank, str(doc["id"]), doc))
    matches.sort(key=lambda item: (-item[0], item[1]))
    return [item[2] for item in matches]


def get_doc(index: Mapping[str, Any], doc_id: str) -> Dict[str, Any]:
    for doc in index.get("documents", []):
        if doc.get("id") == doc_id:
            return doc
    raise KeyError(doc_id)


def print_document(doc: Mapping[str, Any]) -> None:
    print(f"id: {doc['id']} ({doc['id_source']})")
    print(f"path: {doc['path']}")
    print(f"title_ja: {doc.get('title', {}).get('ja', '')}")
    print(f"title_en: {doc.get('title', {}).get('en', '')}")
    print(f"state: {doc.get('state', '')}")
    print(f"layer: {doc.get('layer', '')}")
    print(f"scope: {doc.get('scope', '')}")
    print(f"role_ja: {doc.get('role', {}).get('ja', '')}")
    print(f"role_en: {doc.get('role', {}).get('en', '')}")
    print("topics: " + ", ".join(doc.get("discovery", {}).get("topics", [])))
    print("owned concepts: " + ", ".join(doc.get("concepts", {}).get("owned", [])))


def run_tests(index: Mapping[str, Any], tests_path: Path) -> int:
    tests_data = load_yaml(tests_path)
    failures = 0
    tests = tests_data.get("tests", [])
    for test in tests:
        test_id = str(test.get("id", "unnamed"))
        query = str(test.get("query", ""))
        mode = str(test.get("mode", "auto"))
        top_n = int(test.get("top_n", 5))
        resolved, results = search_documents(query, index, mode=mode, limit=top_n, lang=str(test.get("lang", "both")))
        ids = [str(r["doc_id"]) for r in results]
        expected = [str(v) for v in test.get("expect_top_any", [])]
        ok = bool(set(ids) & set(expected)) if expected else True
        for pair in test.get("must_rank_before", []) or []:
            if not isinstance(pair, dict):
                continue
            higher = str(pair.get("higher", ""))
            lower = str(pair.get("lower", ""))
            if higher in ids and lower in ids and ids.index(higher) >= ids.index(lower):
                ok = False
        if ok:
            print(f"PASS {test_id}: mode={resolved} top={ids[:top_n]}")
        else:
            failures += 1
            print(f"FAIL {test_id}: mode={resolved} expected_any={expected} actual={ids[:top_n]}")
            for result in results[:3]:
                reasons = "; ".join(
                    f"{m['field']}/{m['method']}={m['contribution']:.2f}" for m in result.get("matches", [])[:3]
                )
                print(f"  {result['doc_id']}: {result['score']:.2f} :: {reasons}")
    print(f"SEARCH TESTS: {len(tests) - failures}/{len(tests)} PASS")
    return 1 if failures else 0


def build_parser() -> argparse.ArgumentParser:
    root = repo_root()
    parser = argparse.ArgumentParser(description="Query Scientific Ontology document index.")
    parser.add_argument("--index", default=str(root / "tools/docs_index.json"))
    parser.add_argument("--tests", default=str(root / "tools/docs_search_tests.yml"))
    sub = parser.add_subparsers(dest="command", required=True)

    search = sub.add_parser("search")
    search.add_argument("query")
    search.add_argument("--mode", choices=["auto", "term", "question"], default="auto")
    search.add_argument("--limit", type=int, default=10)
    search.add_argument("--lang", choices=["ja", "en", "both"], default="both")
    search.add_argument("--json", action="store_true")
    search.add_argument("--base-url", default=None)

    find = sub.add_parser("find")
    find.add_argument("query")
    find.add_argument("--lang", choices=["ja", "en", "both"], default="both")
    find.add_argument("--json", action="store_true")

    show = sub.add_parser("show")
    show.add_argument("doc_id")
    show.add_argument("--json", action="store_true")

    related = sub.add_parser("related")
    related.add_argument("doc_id")
    related.add_argument("--json", action="store_true")

    topics = sub.add_parser("topics")
    topics.add_argument("--json", action="store_true")

    sub.add_parser("test")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        index = load_json(Path(args.index))
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if args.command == "search":
        mode, results = search_documents(args.query, index, mode=args.mode, limit=args.limit, lang=args.lang)
        if args.json:
            print(json.dumps({"query": args.query, "mode": mode, "results": results}, ensure_ascii=False, indent=2))
        else:
            print_search(args.query, mode, results, args.lang, args.base_url)
        return 0

    if args.command == "find":
        docs = find_documents(args.query, index, args.lang)
        if args.json:
            print(json.dumps(docs, ensure_ascii=False, indent=2))
        else:
            for doc in docs:
                print(f"{doc['id']}\t{doc['title'].get('ja') or doc['title'].get('en')}\t{doc['path']}")
        return 0

    if args.command == "show":
        try:
            doc = get_doc(index, args.doc_id)
        except KeyError:
            print(f"ERROR: unknown doc_id: {args.doc_id}", file=sys.stderr)
            return 1
        if args.json:
            print(json.dumps(doc, ensure_ascii=False, indent=2))
        else:
            print_document(doc)
        return 0

    if args.command == "related":
        try:
            doc = get_doc(index, args.doc_id)
        except KeyError:
            print(f"ERROR: unknown doc_id: {args.doc_id}", file=sys.stderr)
            return 1
        payload = {
            "doc_id": doc["id"],
            "concepts": doc.get("concepts", {}),
            "relations": doc.get("relations", {}),
        }
        if args.json:
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        else:
            print(f"Document: {doc['id']}")
            for key, values in payload["concepts"].items():
                print(f"concepts.{key}: {', '.join(values)}")
            for key, values in payload["relations"].items():
                print(f"relations.{key}: {', '.join(values)}")
        return 0

    if args.command == "topics":
        if args.json:
            print(json.dumps(index.get("topics", {}), ensure_ascii=False, indent=2))
        else:
            for topic_id, labels in sorted(index.get("topics", {}).items()):
                print(f"{topic_id}\t{labels.get('ja', '')}\t{labels.get('en', '')}")
        return 0

    if args.command == "test":
        return run_tests(index, Path(args.tests))

    return 1


if __name__ == "__main__":
    raise SystemExit(main())

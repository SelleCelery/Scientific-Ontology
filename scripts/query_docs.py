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

ENTRY_LEVEL_ORDER = {
    "foundation": 0,
    "intermediate": 1,
    "advanced": 2,
    "": 3,
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


def localized_value(value: Any, lang: str, fallback: str = "") -> str:
    if isinstance(value, Mapping):
        if lang == "en":
            return str(value.get("en") or value.get("ja") or fallback)
        return str(value.get("ja") or value.get("en") or fallback)
    return str(value or fallback)


def topic_documents(index: Mapping[str, Any], topic_id: str) -> List[Dict[str, Any]]:
    docs = [
        dict(doc)
        for doc in index.get("documents", [])
        if topic_id in doc.get("discovery", {}).get("topics", [])
    ]
    docs.sort(
        key=lambda doc: (
            ENTRY_LEVEL_ORDER.get(str(doc.get("discovery", {}).get("entry_level", "")), 3),
            normalize_text(doc.get("title", {}).get("ja") or doc.get("title", {}).get("en") or doc.get("id", "")),
            str(doc.get("id", "")),
        )
    )
    return docs


def topic_card(index: Mapping[str, Any], topic_id: str) -> Dict[str, Any]:
    topics = index.get("topics", {})
    config = topics.get(topic_id, {}) if isinstance(topics, Mapping) else {}
    if not isinstance(config, Mapping):
        config = {}
    browse = config.get("browse", {}) if isinstance(config.get("browse"), Mapping) else {}
    docs = topic_documents(index, topic_id)
    counts = {"foundation": 0, "intermediate": 0, "advanced": 0, "unspecified": 0}
    for doc in docs:
        level = str(doc.get("discovery", {}).get("entry_level", ""))
        counts[level if level in {"foundation", "intermediate", "advanced"} else "unspecified"] += 1
    label = browse.get("label", {}) if isinstance(browse.get("label"), Mapping) else {}
    description = browse.get("description", {}) if isinstance(browse.get("description"), Mapping) else {}
    questions = browse.get("starter_questions", {}) if isinstance(browse.get("starter_questions"), Mapping) else {}
    return {
        "topic_id": topic_id,
        "base_label": {"ja": str(config.get("ja", "")), "en": str(config.get("en", ""))},
        "featured": bool(browse.get("enabled", False)),
        "order": int(browse.get("order", 9999)),
        "label": {
            "ja": str(label.get("ja") or config.get("ja", "")),
            "en": str(label.get("en") or config.get("en", "")),
        },
        "description": {"ja": str(description.get("ja", "")), "en": str(description.get("en", ""))},
        "starter_questions": {
            "ja": [str(v) for v in questions.get("ja", []) or []],
            "en": [str(v) for v in questions.get("en", []) or []],
        },
        "document_count": len(docs),
        "entry_level_counts": counts,
    }


def browse_topics(index: Mapping[str, Any], include_empty: bool = False) -> List[Dict[str, Any]]:
    topics = index.get("topics", {})
    cards: List[Dict[str, Any]] = []
    if not isinstance(topics, Mapping):
        return cards
    for topic_id in topics:
        card = topic_card(index, str(topic_id))
        if not card["featured"]:
            continue
        if not include_empty and int(card["document_count"]) == 0:
            continue
        cards.append(card)
    cards.sort(key=lambda card: (int(card["order"]), str(card["topic_id"])))
    return cards


def document_browse_summary(doc: Mapping[str, Any]) -> Dict[str, Any]:
    return {
        "doc_id": str(doc.get("id", "")),
        "title": dict(doc.get("title", {})),
        "path": str(doc.get("path", "")),
        "role": dict(doc.get("role", {})),
        "entry_level": str(doc.get("discovery", {}).get("entry_level", "")),
        "reader_questions": dict(doc.get("discovery", {}).get("reader_questions", {})),
    }


def browse_payload(index: Mapping[str, Any], topic_id: str | None = None) -> Dict[str, Any]:
    if topic_id is None:
        return {
            "visibility_profile": index.get("source", {}).get("visibility_profile", ""),
            "topics": browse_topics(index),
        }
    topics = index.get("topics", {})
    if not isinstance(topics, Mapping) or topic_id not in topics:
        raise KeyError(topic_id)
    return {
        "visibility_profile": index.get("source", {}).get("visibility_profile", ""),
        "topic": topic_card(index, topic_id),
        "documents": [document_browse_summary(doc) for doc in topic_documents(index, topic_id)],
    }


def print_browse(payload: Mapping[str, Any], lang: str, base_url: str | None) -> None:
    if "topics" in payload:
        cards = payload.get("topics", [])
        print(f"Browse topics ({len(cards)})")
        for card in cards:
            label = localized_value(card.get("label", {}), lang, str(card.get("topic_id", "")))
            description = localized_value(card.get("description", {}), lang)
            print(f"- {label} [{card['topic_id']}] ({card['document_count']} documents)")
            if description:
                print(f"  {description}")
            questions = card.get("starter_questions", {}).get("en" if lang == "en" else "ja", [])
            if questions:
                print(f"  Q: {questions[0]}")
        return

    card = payload.get("topic", {})
    label = localized_value(card.get("label", {}), lang, str(card.get("topic_id", "")))
    description = localized_value(card.get("description", {}), lang)
    print(f"{label} [{card.get('topic_id', '')}]")
    if description:
        print(description)
    questions = card.get("starter_questions", {}).get("en" if lang == "en" else "ja", [])
    if questions:
        print("Starter questions:")
        for question in questions:
            print(f"- {question}")
    docs = payload.get("documents", [])
    print(f"Documents ({len(docs)}):")
    current_level = None
    for doc in docs:
        level = str(doc.get("entry_level") or "unspecified")
        if level != current_level:
            current_level = level
            print(f"  [{level}]")
        title = localized_value(doc.get("title", {}), lang, str(doc.get("doc_id", "")))
        role = localized_value(doc.get("role", {}), lang)
        print(f"  - {title} ({doc['doc_id']})")
        if role:
            print(f"    {role}")
        print(f"    {result_url(str(doc['path']), base_url)}")
        doc_questions = doc.get("reader_questions", {}).get("en" if lang == "en" else "ja", [])
        if doc_questions:
            print(f"    Q: {doc_questions[0]}")


def run_tests(index: Mapping[str, Any], tests_path: Path) -> int:
    tests_data = load_yaml(tests_path)
    search_failures = 0
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
            search_failures += 1
            print(f"FAIL {test_id}: mode={resolved} expected_any={expected} actual={ids[:top_n]}")
            for result in results[:3]:
                reasons = "; ".join(
                    f"{m['field']}/{m['method']}={m['contribution']:.2f}" for m in result.get("matches", [])[:3]
                )
                print(f"  {result['doc_id']}: {result['score']:.2f} :: {reasons}")
    print(f"SEARCH TESTS: {len(tests) - search_failures}/{len(tests)} PASS")

    browse_failures = 0
    browse_tests = tests_data.get("browse_tests", []) or []
    for test in browse_tests:
        test_id = str(test.get("id", "unnamed-browse"))
        topic_id = str(test.get("topic", ""))
        try:
            payload = browse_payload(index, topic_id)
        except KeyError:
            payload = None
        ok = payload is not None
        actual_ids: List[str] = []
        if payload is not None:
            actual_ids = [str(doc.get("doc_id", "")) for doc in payload.get("documents", [])]
            expected = [str(v) for v in test.get("expect_any", [])]
            if expected and not (set(expected) & set(actual_ids)):
                ok = False
            card = payload.get("topic", {})
            if bool(test.get("require_featured", False)) and not bool(card.get("featured", False)):
                ok = False
            minimum_questions = int(test.get("minimum_starter_questions", 0))
            questions = card.get("starter_questions", {}).get(str(test.get("lang", "ja")), [])
            if len(questions) < minimum_questions:
                ok = False
        if ok:
            print(f"PASS {test_id}: topic={topic_id} docs={actual_ids[:5]}")
        else:
            browse_failures += 1
            print(f"FAIL {test_id}: topic={topic_id} docs={actual_ids[:5]}")
    if browse_tests:
        print(f"BROWSE TESTS: {len(browse_tests) - browse_failures}/{len(browse_tests)} PASS")
    return 1 if (search_failures or browse_failures) else 0



def graph_node_label(node: Mapping[str, Any], lang: str = "ja") -> str:
    if node.get("type") == "document":
        title = node.get("title", {})
        if isinstance(title, Mapping):
            return str(title.get(lang) or title.get("ja") or title.get("en") or node.get("key") or node.get("id"))
    label = node.get("label", {})
    if isinstance(label, Mapping):
        return str(label.get(lang) or label.get("ja") or label.get("en") or label.get("raw") or node.get("key") or node.get("id"))
    return str(node.get("key") or node.get("id"))


def graph_node_map(graph: Mapping[str, Any]) -> Dict[str, Mapping[str, Any]]:
    return {str(node.get("id")): node for node in graph.get("nodes", []) if isinstance(node, Mapping) and node.get("id")}


def resolve_graph_node(graph: Mapping[str, Any], query: str, node_type: str | None = None) -> str:
    nodes = graph_node_map(graph)
    if query in nodes and (node_type is None or nodes[query].get("type") == node_type):
        return query
    prefixes = ["doc", "concept", "topic", "term", "layer", "artifact"]
    for prefix in prefixes:
        candidate = f"{prefix}:{query}"
        if candidate in nodes and (node_type is None or nodes[candidate].get("type") == node_type):
            return candidate
    norm = normalize_text(query)
    matches: List[str] = []
    for node_id, node in nodes.items():
        if node_type is not None and node.get("type") != node_type:
            continue
        label_map = node.get("label", {}) if isinstance(node.get("label"), Mapping) else {}
        values = [node_id, str(node.get("key", "")), graph_node_label(node, "ja"), graph_node_label(node, "en"), str(label_map.get("raw", ""))]
        if any(normalize_text(value) == norm for value in values if value):
            matches.append(node_id)
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        raise ValueError(f"ambiguous graph node '{query}': {', '.join(matches[:8])}")
    # Bounded contains fallback for human labels.
    contains: List[str] = []
    if len(norm) >= 3:
        for node_id, node in nodes.items():
            if node_type is not None and node.get("type") != node_type:
                continue
            label_map = node.get("label", {}) if isinstance(node.get("label"), Mapping) else {}
            values = [str(node.get("key", "")), graph_node_label(node, "ja"), graph_node_label(node, "en"), str(label_map.get("raw", ""))]
            if any(norm in normalize_text(value) for value in values if value):
                contains.append(node_id)
    if len(contains) == 1:
        return contains[0]
    if len(contains) > 1:
        raise ValueError(f"ambiguous graph node '{query}': {', '.join(contains[:8])}")
    raise KeyError(query)


def graph_subgraph(graph: Mapping[str, Any], start_id: str, depth: int = 1, relation: str | None = None) -> Dict[str, Any]:
    nodes = graph_node_map(graph)
    all_edges = [edge for edge in graph.get("edges", []) if isinstance(edge, Mapping)]
    selected_nodes = {start_id}
    frontier = {start_id}
    selected_edges: List[Mapping[str, Any]] = []
    seen_edge_keys: set[Tuple[str, str, str]] = set()
    for _ in range(max(0, depth)):
        next_frontier: set[str] = set()
        for edge in all_edges:
            if relation and str(edge.get("relation")) != relation:
                continue
            source = str(edge.get("from"))
            target = str(edge.get("to"))
            if source in frontier or target in frontier:
                key = (source, str(edge.get("relation")), target)
                if key not in seen_edge_keys:
                    selected_edges.append(edge)
                    seen_edge_keys.add(key)
                if source not in selected_nodes:
                    next_frontier.add(source)
                if target not in selected_nodes:
                    next_frontier.add(target)
        selected_nodes.update(next_frontier)
        frontier = next_frontier
        if not frontier:
            break
    return {
        "root": start_id,
        "depth": depth,
        "nodes": [nodes[node_id] for node_id in sorted(selected_nodes) if node_id in nodes],
        "edges": sorted(selected_edges, key=lambda e: (str(e.get("from")), str(e.get("relation")), str(e.get("to")))),
    }


def trace_graph(graph: Mapping[str, Any], source_id: str, target_id: str, directed: bool = False, max_depth: int = 6) -> Dict[str, Any] | None:
    edges = [edge for edge in graph.get("edges", []) if isinstance(edge, Mapping)]
    adjacency: Dict[str, List[Tuple[str, Mapping[str, Any], str]]] = {}
    for edge in edges:
        source = str(edge.get("from"))
        target = str(edge.get("to"))
        adjacency.setdefault(source, []).append((target, edge, "forward"))
        if not directed:
            adjacency.setdefault(target, []).append((source, edge, "reverse"))
    queue: List[Tuple[str, List[Dict[str, Any]]]] = [(source_id, [])]
    visited = {source_id}
    while queue:
        node_id, steps = queue.pop(0)
        if node_id == target_id:
            return {"from": source_id, "to": target_id, "directed": directed, "steps": steps}
        if len(steps) >= max_depth:
            continue
        for next_id, edge, direction in adjacency.get(node_id, []):
            if next_id in visited:
                continue
            visited.add(next_id)
            queue.append((next_id, steps + [{
                "from": node_id,
                "to": next_id,
                "direction": direction,
                "relation": str(edge.get("relation")),
                "edge": edge,
            }]))
    return None


def provenance_summary(edge: Mapping[str, Any]) -> str:
    kinds = sorted({str(p.get("source_type", "")) for p in edge.get("provenance", []) if isinstance(p, Mapping)})
    return ",".join(kinds)


def print_graph_subgraph(payload: Mapping[str, Any], lang: str = "ja", limit: int = 80) -> None:
    nodes = {str(n.get("id")): n for n in payload.get("nodes", []) if isinstance(n, Mapping)}
    root = str(payload.get("root", ""))
    root_node = nodes.get(root, {})
    print(f"Root: [{root_node.get('type', '')}] {graph_node_label(root_node, lang)} <{root}>")
    edges = payload.get("edges", [])
    shown = 0
    for edge in edges:
        if shown >= limit:
            break
        source = str(edge.get("from", ""))
        target = str(edge.get("to", ""))
        if source == root:
            other = nodes.get(target, {})
            arrow = "->"
            relation = str(edge.get("relation", ""))
        elif target == root:
            other = nodes.get(source, {})
            arrow = "<-"
            relation = str(edge.get("relation", ""))
        else:
            continue
        print(f"  {arrow} {relation} {arrow} [{other.get('type', '')}] {graph_node_label(other, lang)} <{other.get('id', '')}> [{provenance_summary(edge)}]")
        shown += 1
    if int(payload.get("depth", 1)) > 1:
        print(f"Subgraph: {len(nodes)} nodes / {len(edges)} edges (use --json for the complete relation map)")
    if len(edges) > limit:
        print(f"... {len(edges) - limit} more edges omitted; use --json or --limit")


def print_trace(payload: Mapping[str, Any], graph: Mapping[str, Any], lang: str = "ja") -> None:
    nodes = graph_node_map(graph)
    print(f"Trace ({len(payload.get('steps', []))} steps, directed={payload.get('directed')}):")
    current = str(payload.get("from", ""))
    start = nodes.get(current, {})
    print(f"  [{start.get('type', '')}] {graph_node_label(start, lang)} <{current}>")
    for step in payload.get("steps", []):
        target = str(step.get("to", ""))
        node = nodes.get(target, {})
        direction = str(step.get("direction", "forward"))
        marker = "--" if direction == "forward" else "<-"
        print(f"  {marker} {step.get('relation')} ({direction}) -> [{node.get('type', '')}] {graph_node_label(node, lang)} <{target}>")


def run_graph_tests(graph: Mapping[str, Any], tests_path: Path) -> int:
    data = load_yaml(tests_path)
    edges = [edge for edge in graph.get("edges", []) if isinstance(edge, Mapping)]
    failures = 0
    tests = data.get("tests", []) or []
    for test in tests:
        test_id = str(test.get("id", "unnamed-graph"))
        try:
            if test.get("from"):
                source = resolve_graph_node(graph, str(test.get("from")))
            else:
                source = resolve_graph_node(graph, str(test.get("from_label_contains", "")), str(test.get("from_type")) if test.get("from_type") else None)
            target = resolve_graph_node(graph, str(test.get("to")))
        except Exception as exc:
            failures += 1
            print(f"FAIL {test_id}: node resolution: {exc}")
            continue
        relations = [str(test.get("relation"))] if test.get("relation") else [str(v) for v in test.get("relation_any", [])]
        ok = any(str(edge.get("from")) == source and str(edge.get("to")) == target and str(edge.get("relation")) in relations for edge in edges)
        if ok:
            print(f"PASS {test_id}: {source} --{relations}--> {target}")
        else:
            failures += 1
            print(f"FAIL {test_id}: missing {source} --{relations}--> {target}")
    path_tests = data.get("path_tests", []) or []
    for test in path_tests:
        test_id = str(test.get("id", "unnamed-path"))
        try:
            if test.get("from"):
                source = resolve_graph_node(graph, str(test.get("from")))
            else:
                source = resolve_graph_node(graph, str(test.get("from_label_contains", "")), str(test.get("from_type")) if test.get("from_type") else None)
            target = resolve_graph_node(graph, str(test.get("to")))
            payload = trace_graph(graph, source, target, directed=bool(test.get("directed", False)), max_depth=int(test.get("max_depth", 6)))
        except Exception as exc:
            payload = None
            failures += 1
            print(f"FAIL {test_id}: node/path resolution: {exc}")
            continue
        if payload is not None:
            print(f"PASS {test_id}: {source} -> {target} in {len(payload['steps'])} steps")
        else:
            failures += 1
            print(f"FAIL {test_id}: no path")
    total = len(tests) + len(path_tests)
    print(f"GRAPH TESTS: {total - failures}/{total} PASS")
    return 1 if failures else 0

def build_parser() -> argparse.ArgumentParser:
    root = repo_root()
    parser = argparse.ArgumentParser(description="Query Scientific Ontology document index.")
    parser.add_argument("--index", default=str(root / "tools/docs_index.json"))
    parser.add_argument("--tests", default=str(root / "tools/docs_search_tests.yml"))
    parser.add_argument("--graph", default=str(root / "tools/docs_graph.json"))
    parser.add_argument("--graph-tests", default=str(root / "tools/docs_graph_tests.yml"))
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

    browse = sub.add_parser("browse", help="Browse beginner-facing topic entry surfaces.")
    browse.add_argument("topic_id", nargs="?")
    browse.add_argument("--lang", choices=["ja", "en", "both"], default="ja")
    browse.add_argument("--json", action="store_true")
    browse.add_argument("--base-url", default=None)

    topics = sub.add_parser("topics")
    topics.add_argument("--json", action="store_true")

    graph = sub.add_parser("graph", help="Show a typed relation neighborhood from docs_graph.json.")
    graph.add_argument("node")
    graph.add_argument("--depth", type=int, choices=[1, 2], default=1)
    graph.add_argument("--relation", default=None)
    graph.add_argument("--lang", choices=["ja", "en"], default="ja")
    graph.add_argument("--limit", type=int, default=80)
    graph.add_argument("--json", action="store_true")

    trace = sub.add_parser("trace", help="Find a short relation path between two graph nodes.")
    trace.add_argument("source")
    trace.add_argument("target")
    trace.add_argument("--directed", action="store_true")
    trace.add_argument("--max-depth", type=int, default=6)
    trace.add_argument("--lang", choices=["ja", "en"], default="ja")
    trace.add_argument("--json", action="store_true")

    sub.add_parser("graph-test")
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

    if args.command == "browse":
        try:
            payload = browse_payload(index, args.topic_id)
        except KeyError:
            print(f"ERROR: unknown topic_id: {args.topic_id}", file=sys.stderr)
            return 1
        if args.json:
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        else:
            print_browse(payload, args.lang, args.base_url)
        return 0

    if args.command == "topics":
        if args.json:
            print(json.dumps(index.get("topics", {}), ensure_ascii=False, indent=2))
        else:
            for topic_id, labels in sorted(index.get("topics", {}).items()):
                print(f"{topic_id}\t{labels.get('ja', '')}\t{labels.get('en', '')}")
        return 0

    if args.command in {"graph", "trace", "graph-test"}:
        try:
            graph_data = load_json(Path(args.graph))
        except Exception as exc:
            print(f"ERROR: could not load graph: {exc}", file=sys.stderr)
            return 1

        if args.command == "graph":
            try:
                node_id = resolve_graph_node(graph_data, args.node)
            except Exception as exc:
                print(f"ERROR: {exc}", file=sys.stderr)
                return 1
            payload = graph_subgraph(graph_data, node_id, depth=args.depth, relation=args.relation)
            if args.json:
                print(json.dumps(payload, ensure_ascii=False, indent=2))
            else:
                print_graph_subgraph(payload, args.lang, args.limit)
            return 0

        if args.command == "trace":
            try:
                source_id = resolve_graph_node(graph_data, args.source)
                target_id = resolve_graph_node(graph_data, args.target)
            except Exception as exc:
                print(f"ERROR: {exc}", file=sys.stderr)
                return 1
            payload = trace_graph(graph_data, source_id, target_id, directed=args.directed, max_depth=args.max_depth)
            if payload is None:
                print("NO PATH")
                return 1
            if args.json:
                print(json.dumps(payload, ensure_ascii=False, indent=2))
            else:
                print_trace(payload, graph_data, args.lang)
            return 0

        if args.command == "graph-test":
            return run_graph_tests(graph_data, Path(args.graph_tests))

    if args.command == "test":
        return run_tests(index, Path(args.tests))

    return 1


if __name__ == "__main__":
    raise SystemExit(main())

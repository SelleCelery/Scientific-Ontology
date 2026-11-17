#!/usr/bin/env python3
"""Build a read-only term reference overlay; does not modify docs_graph or canon."""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import unicodedata

SCHEMA_VERSION = "0.1.0"
REL_ATTESTED = "surface_attested_in"
REL_DEFINITION = "definition_lexically_mentions"


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def dump(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes((json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8"))


def valid_path(p: str) -> bool:
    pp = PurePosixPath(p)
    return bool(p and not p.startswith("/") and "\\" not in p and ".." not in pp.parts and pp.as_posix() == p)


def ascii_word(ch: str) -> bool:
    return bool(ch and ("A" <= ch <= "Z" or "a" <= ch <= "z" or "0" <= ch <= "9" or ch == "_"))


def boundary_ok(text: str, start: int, end: int, form: str) -> bool:
    if ascii_word(form[0]) and start > 0 and ascii_word(text[start - 1]):
        return False
    if ascii_word(form[-1]) and end < len(text) and ascii_word(text[end]):
        return False
    return True


def lexical_matches(text: str, forms: list[tuple[str, str]]) -> list[dict]:
    """Find longest surface span; no semantic inference or segmentation claim."""
    by_first: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for form, term_id in forms:
        if len(form) < 2:
            continue  # A one-character headword needs explicit user selection.
        by_first[form[0]].append((form, term_id))
    for char in by_first:
        by_first[char].sort(key=lambda x: (-len(x[0]), x[0], x[1]))
    matches = []
    pos = 0
    while pos < len(text):
        best = None
        for form, term_id in by_first.get(text[pos], []):
            end = pos + len(form)
            if text.startswith(form, pos) and boundary_ok(text, pos, end, form):
                best = (form, term_id, end)
                break
        if best:
            form, term_id, end = best
            matches.append({"term_id": term_id, "surface": form, "start": pos, "end": end})
            pos = end
        else:
            pos += 1
    return matches


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def build(dictionary: Path, doc_graph: Path, repo_root: Path) -> tuple[dict, dict, dict]:
    dictionary_data = load(dictionary)
    doc_data = load(doc_graph)
    entries = dictionary_data["entries"]
    if not isinstance(entries, list) or len({str(e["id"]) for e in entries}) != len(entries):
        raise ValueError("Dictionary term IDs must be unique")
    if len({str(e["term"]) for e in entries}) != len(entries):
        raise ValueError("Dictionary headwords must be unique")

    id_to_entry = {e["id"]: e for e in entries}
    doc_by_path = {n["path"]: n for n in doc_data["nodes"] if n.get("type") in ("document", "observed_document") and n.get("path")}
    doc_nodes = {}
    term_nodes = []
    source_nodes = {}
    extractions = defaultdict(list)
    missing_sources = []
    document_texts = {}
    attestations = Counter()
    matched_source_paths = set()

    for e in entries:
        if not isinstance(e.get("definition"), str) or not e["definition"].strip():
            raise ValueError(f"Empty definition: {e['id']}")
        tid = "dictterm:" + e["id"]
        term_nodes.append({
            "id": tid, "type": "dictionary_term", "dictionary_id": e["id"],
            "label": e["term"], "group": e.get("group", "undecided"),
            "technical_adjacency": bool(e.get("technical_adjacency", False)),
            "authority": e.get("authority", "unreviewed_editorial"),
        })
        for a in e.get("source_attestations", []):
            path = str(a.get("path", ""))
            line = a.get("line")
            excerpt = str(a.get("excerpt", "")).strip()
            if not valid_path(path):
                raise ValueError(f"Invalid source path: {path}")
            if path not in document_texts:
                source = repo_root.joinpath(*PurePosixPath(path).parts)
                document_texts[path] = source.read_text(encoding="utf-8-sig").splitlines() if source.is_file() else None
            lines = document_texts[path]
            if lines is None:
                reason = "source_not_in_local_tree"
            elif not isinstance(line, int) or not (1 <= line <= len(lines)):
                reason = "line_out_of_bounds"
            elif not excerpt or excerpt not in lines[line - 1]:
                reason = "attestation_excerpt_mismatch"
            elif e["term"] not in lines[line - 1]:
                reason = "headword_surface_absent_on_line"
            else:
                reason = "verified_surface_on_line"
            attestations[reason] += 1
            if reason != "verified_surface_on_line":
                missing_sources.append({"term_id": e["id"], "path": path, "line": line, "status": reason})
                continue
            matched_source_paths.add(path)
            if path in doc_by_path:
                doc = doc_by_path[path]
                node_id = doc["id"]
                doc_nodes[node_id] = {"id": node_id, "type": "registered_document_reference", "path": path,
                                      "label": (doc.get("title") or {}).get("ja", path),
                                      "state": doc.get("state", "unknown")}
            else:
                node_id = "unregistered_source:" + sha(path.encode("utf-8"))[:18]
                source_nodes[node_id] = {"id": node_id, "type": "unregistered_source_reference", "path": path,
                                         "registration_status": "not_linked_to_document_graph"}
            exactness = "whole_line" if excerpt == lines[line - 1].strip() else "excerpt_within_line"
            extractions[(tid, node_id)].append({"source_path": path, "line": line, "span_text": e["term"],
                                                "excerpt_relation": exactness})

    att_edges = []
    for (source_id, target_id), evidence in sorted(extractions.items()):
        evidence.sort(key=lambda x: (x["source_path"], x["line"], x["span_text"]))
        att_edges.append({"from": source_id, "to": target_id, "relation": REL_ATTESTED,
                          "evidence_kind": "verified_source_line_surface_only",
                          "provenance": evidence})

    forms = []
    for e in entries:
        seen = set()
        for form in [e["term"], *(e.get("aliases") or [])]:
            if isinstance(form, str) and form and form not in seen:
                forms.append((form, e["id"]))
                seen.add(form)
    form_collisions = defaultdict(set)
    for form, entry_id in forms:
        form_collisions[unicodedata.normalize("NFC", form)].add(entry_id)
    collisions = [{"form": f, "candidate_ids": sorted(ids)} for f, ids in sorted(form_collisions.items()) if len(ids) > 1]

    def_edges = []
    for e in entries:
        span_map = defaultdict(list)
        for hit in lexical_matches(e["definition"], forms):
            # Self-reference is recorded but no definition is proved by this link.
            span_map[hit["term_id"]].append({"field": "definition", "start": hit["start"], "end": hit["end"],
                                              "matched_surface": hit["surface"]})
        for target_id, evidence in sorted(span_map.items()):
            def_edges.append({"from": "dictterm:" + e["id"], "to": "dictterm:" + target_id,
                              "relation": REL_DEFINITION, "evidence_kind": "literal_surface_not_semantic_dependency",
                              "provenance": evidence})

    nodes = sorted(term_nodes + list(doc_nodes.values()) + list(source_nodes.values()), key=lambda x: x["id"])
    edges = sorted(att_edges + def_edges, key=lambda x: (x["from"], x["relation"], x["to"]))
    allowed_ids = {n["id"] for n in nodes}
    if any(e["from"] not in allowed_ids or e["to"] not in allowed_ids for e in edges):
        raise ValueError("Unresolved reference graph endpoint")
    raw_dict = dictionary.read_bytes()
    raw_graph = doc_graph.read_bytes()

    graph = {
        "schema_version": SCHEMA_VERSION, "kind": "so.term_reference_overlay",
        "layer": "internal_research_draft_not_public_runtime",
        "sources": {"dictionary_sha256": sha(raw_dict), "document_graph_sha256": sha(raw_graph),
                    "corpus_snapshot_sha256": dictionary_data.get("source_snapshot_sha256"),
                    "evidence_verification": "current_local_files_line_and_surface"},
        "relation_types": {
            REL_ATTESTED: {"meaning": "The literal headword appears on an attested source line.",
                            "not_entails": ["sense_identity", "definition_validity", "logical_support", "canonical_ownership"]},
            REL_DEFINITION: {"meaning": "A dictionary definition literally contains another headword surface.",
                             "not_entails": ["semantic_dependency", "entailment", "inference", "truth"]},
        },
        "nodes": nodes, "edges": edges,
        "diagnostics": {"unverified_attestations": missing_sources,
                        "ambiguous_forms": collisions,
                        "unregistered_source_paths": sorted({n["path"] for n in source_nodes.values()})},
    }
    runtime_terms = []
    for e in entries:
        runtime_terms.append({
            "id": e["id"], "label": e["term"],
            "forms": list(dict.fromkeys([e["term"], *(e.get("aliases") or [])])),
            "reading": e.get("reading"), "group": e.get("group"),
            "technical_adjacency": bool(e.get("technical_adjacency", False)),
            "senses": [{"sense_id": e["id"] + ":draft", "scope": "undetermined_draft",
                        "definition": e["definition"], "authority": e.get("authority", "unreviewed_editorial"),
                        "status": e.get("status", "unreviewed"), "usage_note": e.get("usage_note", "")}],
            "source_snapshot_sha256": e.get("source_snapshot_sha256"),
        })
    runtime = {
        "schema_version": SCHEMA_VERSION, "kind": "so.term_dictionary_runtime_seed",
        "status": "unreviewed_draft_no_canonical_sense_split",
        "display_order_for_future_senses": ["so", "general", "external", "undetermined_draft"],
        "term_id_namespace": "dictterm:<dictionary-id>",
        "matching_contract": {"primary": "explicit_selection_exact_form",
                              "unselected_caret": "longest_surface_match_candidate_only",
                              "unicode": "NFC", "single_character": "selection_only",
                              "latin_identifier_boundary": True, "ambiguous_form": "return_all_candidates",
                              "meaning": "surface_only_not_sense_disambiguation"},
        "dictionary_sha256": sha(raw_dict),
        "entries": sorted(runtime_terms, key=lambda x: x["id"]),
    }
    summary = {
        "schema_version": SCHEMA_VERSION,
        "dictionary_entry_count": len(entries),
        "dictionary_groups": dict(sorted(Counter(e.get("group", "undecided") for e in entries).items())),
        "original_source_attestations": sum(attestations.values()),
        "attestation_checks": dict(sorted(attestations.items())),
        "attested_term_to_source_edges": len(att_edges),
        "attested_registered_document_count": len(doc_nodes),
        "attested_unregistered_source_count": len(source_nodes),
        "definition_lexical_edges": len(def_edges),
        "definition_self_lexical_edges": sum(e["from"] == e["to"] for e in def_edges),
        "form_collision_count": len(collisions),
        "graph_node_count": len(nodes), "graph_edge_count": len(edges),
        "unresolved_meaning_decisions": "all, unless independently reviewed; lexical links are not logical support",
        "source_limit": "scope is the supplied dictionary attestations and definition strings, not every term occurrence in repository",
    }
    return graph, runtime, summary


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dictionary", type=Path, default=Path("tools/assessment/term_dictionary/navigator_seed/dictionary_1500.json"))
    ap.add_argument("--docs-graph", type=Path, default=Path("tools/docs_graph.json"))
    ap.add_argument("--repo-root", type=Path, default=Path("."))
    ap.add_argument("--out-dir", type=Path, default=Path("tools/assessment/term_dictionary/term_reference"))
    args = ap.parse_args()
    graph, runtime, summary = build(args.dictionary, args.docs_graph, args.repo_root)
    dump(args.out_dir / "term_reference_graph.json", graph)
    dump(args.out_dir / "term_dictionary_runtime_seed.json", runtime)
    dump(args.out_dir / "term_reference_summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Build a deterministic typed relation graph for Scientific Ontology.

DN-4 stores inspectable nodes, typed edges, and provenance. Numeric centrality or
importance metrics are deliberately not part of the primary graph artifact.
"""

from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import posixpath
import re
import sys
import unicodedata
from pathlib import Path, PurePosixPath
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple
from urllib.parse import unquote

try:
    import yaml
except Exception as exc:  # pragma: no cover
    raise SystemExit("PyYAML is required: python -m pip install pyyaml") from exc

from build_docs_index import compile_index, fallback_doc_id

SCHEMA_VERSION = "0.1"
FORBIDDEN_TEXT = (
    "sandbox:/",
    "/mnt/data",
    "10_PUBLIC_GITHUB",
    "CURRENT_WORK_SPACE",
    "file_000000",
    "myfiles_browser",
)
PRIVATE_PATH_PARTS = {"99_Private_Core_Not_Included", ".git", ".github"}
MD_LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
HEADING2_RE = re.compile(r"^##\s+(.+?)\s*$")
FIELD_RE = re.compile(r"^\*\*([^*]+):\*\*\s*(.*)$")
BACKTICK_RE = re.compile(r"`([a-z0-9]+(?:_[a-z0-9]+)*)`")
PROCESS_PART_RE = re.compile(r"^(?:gate[_-]?\d+|u\d+(?:[_-][a-z0-9]+)?)", re.IGNORECASE)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_yaml(path: Path) -> Dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"YAML root must be a mapping: {path}")
    return data


def normalize_id(value: str) -> str:
    text = unicodedata.normalize("NFKC", value).casefold()
    text = re.sub(r"[^a-z0-9]+", "_", text).strip("_")
    if text:
        return text
    return f"item_{hashlib.sha1(value.encode('utf-8')).hexdigest()[:12]}"


def split_glossary_heading(title: str) -> Tuple[str, str]:
    parts = [p.strip() for p in title.split(" / ")]
    if len(parts) >= 2:
        return parts[0], " / ".join(parts[1:])
    return title, title


def is_excluded_graph_path(path_value: str) -> bool:
    parts = PurePosixPath(path_value).parts
    for part in parts:
        if part in PRIVATE_PATH_PARTS or part.startswith("000") or PROCESS_PART_RE.match(part):
            return True
    lowered = path_value.casefold()
    return any(marker.casefold() in lowered for marker in FORBIDDEN_TEXT)


def local_markdown_target(source_path: str, raw_target: str) -> str | None:
    target = raw_target.strip().strip("<>")
    if not target or target.startswith(("http://", "https://", "mailto:", "#")):
        return None
    target = unquote(target.split("#", 1)[0].split("?", 1)[0])
    if not target or not target.lower().endswith(".md"):
        return None
    if target.startswith("/"):
        normalized = posixpath.normpath(target.lstrip("/"))
    else:
        normalized = posixpath.normpath(posixpath.join(posixpath.dirname(source_path), target))
    if normalized.startswith("../") or normalized == "..":
        return None
    return PurePosixPath(normalized).as_posix()


def markdown_links(path: Path, repo_relative: str) -> Iterable[Tuple[int, str]]:
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        for match in MD_LINK_RE.finditer(line):
            target = local_markdown_target(repo_relative, match.group(1))
            if target:
                yield lineno, target


def markdown_title(path: Path) -> Dict[str, str]:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except Exception:
        return {"ja": path.stem, "en": path.stem}
    for line in lines[:80]:
        if line.startswith("# "):
            title = line[2:].strip()
            title = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", title)
            title = title.replace("`", "").strip()
            return {"ja": title, "en": title}
    return {"ja": path.stem, "en": path.stem}


class GraphBuilder:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.nodes: Dict[str, Dict[str, Any]] = {}
        self.edges: Dict[Tuple[str, str, str], Dict[str, Any]] = {}
        self.diagnostics: Dict[str, List[Dict[str, Any]]] = {
            "unresolved_document_references": [],
            "unresolved_concept_references": [],
            "observed_unregistered_documents": [],
            "excluded_references": [],
        }

    def add_node(self, node_id: str, node_type: str, **attrs: Any) -> None:
        clean = {k: v for k, v in attrs.items() if v not in (None, "", [], {})}
        incoming = {"id": node_id, "type": node_type, **clean}
        existing = self.nodes.get(node_id)
        if existing is None:
            self.nodes[node_id] = incoming
            return
        if existing.get("type") != node_type:
            raise ValueError(f"Node type conflict for {node_id}: {existing.get('type')} vs {node_type}")
        for key, value in clean.items():
            if key not in existing:
                existing[key] = value
            elif existing[key] != value:
                raise ValueError(f"Node metadata conflict for {node_id}.{key}: {existing[key]!r} vs {value!r}")

    def add_edge(
        self,
        source: str,
        relation: str,
        target: str,
        provenance_type: str,
        provenance_path: str,
        locator: str = "",
        detail: Mapping[str, Any] | None = None,
    ) -> None:
        if source not in self.nodes or target not in self.nodes:
            raise ValueError(f"Edge references unknown node: {source} --{relation}--> {target}")
        key = (source, relation, target)
        edge = self.edges.setdefault(key, {"from": source, "relation": relation, "to": target, "provenance": []})
        prov: Dict[str, Any] = {"source_type": provenance_type, "source_path": provenance_path}
        if locator:
            prov["locator"] = locator
        if detail:
            prov["detail"] = dict(detail)
        if prov not in edge["provenance"]:
            edge["provenance"].append(prov)

    def add_diag(self, kind: str, item: Mapping[str, Any]) -> None:
        value = dict(item)
        if value not in self.diagnostics[kind]:
            self.diagnostics[kind].append(value)


def layer_for_path(path_value: str, layers: Mapping[str, Any]) -> Tuple[str, Mapping[str, Any]] | None:
    best: Tuple[int, str, Mapping[str, Any]] | None = None
    for layer_id, raw in layers.items():
        if not isinstance(raw, Mapping) or str(layer_id) == "private_core_marker":
            continue
        layer_path = str(raw.get("path", ""))
        matches = ("/" not in path_value) if layer_path == "." else (path_value == layer_path or path_value.startswith(layer_path.rstrip("/") + "/"))
        if matches and (best is None or len(layer_path) > best[0]):
            best = (len(layer_path), str(layer_id), raw)
    return None if best is None else (best[1], best[2])


def observed_markdown_paths(root: Path, config: Mapping[str, Any], dedicated_paths: set[str]) -> List[str]:
    observed = config.get("observed_markdown", {}) if isinstance(config.get("observed_markdown"), Mapping) else {}
    if not bool(observed.get("enabled", False)):
        return []
    paths: set[str] = set()
    for file_name in observed.get("root_files", []) or []:
        p = root / str(file_name)
        if p.is_file():
            paths.add(PurePosixPath(str(file_name)).as_posix())
    for root_name in observed.get("roots", []) or []:
        base = root / str(root_name)
        if not base.exists():
            continue
        for p in base.rglob("*.md"):
            rel = p.relative_to(root).as_posix()
            if any(part.startswith("000") for part in PurePosixPath(rel).parts):
                continue
            if is_excluded_graph_path(rel):
                continue
            paths.add(rel)
    return sorted(path for path in paths if path not in dedicated_paths and not is_excluded_graph_path(path))


def make_observed_node(builder: GraphBuilder, root: Path, path_value: str) -> str:
    node_id = f"observed:{fallback_doc_id(path_value)}"
    if node_id not in builder.nodes:
        builder.add_node(
            node_id,
            "observed_document",
            key=fallback_doc_id(path_value),
            path=path_value,
            title=markdown_title(root / path_value),
            state="observed_unregistered",
            identity_source="path_fallback",
        )
        builder.add_diag("observed_unregistered_documents", {"node_id": node_id, "path": path_value})
    return node_id


def resolve_target_node(
    builder: GraphBuilder,
    root: Path,
    path_to_node: Dict[str, str],
    target_path: str,
    source_path: str,
    relation: str,
    locator: str = "",
) -> str | None:
    if target_path in path_to_node:
        return path_to_node[target_path]
    if is_excluded_graph_path(target_path):
        builder.add_diag("excluded_references", {
            "source_path": source_path,
            "relation": relation,
            "reason": "private_or_process_boundary",
            **({"locator": locator} if locator else {}),
        })
        return None
    abs_target = root / target_path
    if abs_target.is_file() and target_path.lower().endswith(".md"):
        node_id = make_observed_node(builder, root, target_path)
        path_to_node[target_path] = node_id
        return node_id
    builder.add_diag("unresolved_document_references", {
        "source_path": source_path,
        "target_path": target_path,
        "relation": relation,
        "reason": "missing_file",
        **({"locator": locator} if locator else {}),
    })
    return None


def parse_glossary(
    builder: GraphBuilder,
    root: Path,
    path: Path,
    repo_relative: str,
    glossary_node: str,
    path_to_node: Dict[str, str],
) -> None:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts: List[Tuple[int, str]] = []
    for i, line in enumerate(lines):
        match = HEADING2_RE.match(line)
        if not match:
            continue
        title = match.group(1).strip()
        if re.match(r"^\d+\.", title):
            continue
        starts.append((i, title))

    for pos, (start, title) in enumerate(starts):
        end = starts[pos + 1][0] if pos + 1 < len(starts) else len(lines)
        block = lines[start + 1:end]
        en_label, ja_label = split_glossary_heading(title)
        term_id = f"term:{normalize_id(en_label)}"
        if term_id in builder.nodes and builder.nodes[term_id].get("label", {}).get("raw") != title:
            term_id = f"term:{normalize_id(title)}_{hashlib.sha1(title.encode('utf-8')).hexdigest()[:8]}"
        builder.add_node(term_id, "glossary_term", key=normalize_id(en_label), label={"raw": title, "ja": ja_label, "en": en_label}, source_path=repo_relative)
        builder.add_edge(glossary_node, "contains_term", term_id, "glossary", repo_relative, locator=f"L{start + 1}")

        fields: Dict[str, List[Tuple[int, str]]] = {}
        for offset, line in enumerate(block, start + 2):
            field = FIELD_RE.match(line)
            if field:
                fields.setdefault(field.group(1).strip(), []).append((offset, field.group(2).strip()))

        for lineno, value in fields.get("Concept ID", []):
            for concept_id in BACKTICK_RE.findall(value):
                target = f"concept:{concept_id}"
                if target in builder.nodes:
                    builder.add_edge(term_id, "lexical_anchor", target, "glossary", repo_relative, locator=f"L{lineno}")
                else:
                    builder.add_diag("unresolved_concept_references", {"source": term_id, "concept_id": concept_id, "relation": "lexical_anchor"})

        field_to_relation = {
            "Public definition owner": "definition_owner_reference",
            "Public generative source": "generative_source_reference",
            "Operationalized in": "operationalized_in_reference",
        }
        for field_name, relation in field_to_relation.items():
            for lineno, value in fields.get(field_name, []):
                for match in MD_LINK_RE.finditer(value):
                    target_path = local_markdown_target(repo_relative, match.group(1))
                    if not target_path:
                        continue
                    target_node = resolve_target_node(builder, root, path_to_node, target_path, repo_relative, relation, f"L{lineno}")
                    if target_node:
                        builder.add_edge(term_id, relation, target_node, "glossary", repo_relative, locator=f"L{lineno}")


def build_graph(root: Path, manifest_path: Path, search_path: Path, graph_config_path: Path, visibility: str) -> Dict[str, Any]:
    manifest_bytes = manifest_path.read_bytes()
    search_bytes = search_path.read_bytes()
    graph_config_bytes = graph_config_path.read_bytes()
    manifest = load_yaml(manifest_path)
    search_data = load_yaml(search_path)
    graph_data = load_yaml(graph_config_path)
    config = graph_data.get("graph", {}) if isinstance(graph_data.get("graph"), Mapping) else {}
    if str(config.get("spec_version", "")) != SCHEMA_VERSION:
        raise ValueError(f"docs_graph.yml spec_version must be {SCHEMA_VERSION}")

    index = compile_index(root, manifest_path, search_path, visibility)
    builder = GraphBuilder(root)
    documents = index.get("documents", [])
    raw_docs = {str(raw.get("path", "")): raw for raw in manifest.get("documents", []) if isinstance(raw, Mapping)}
    path_to_doc_id = {str(doc["path"]): str(doc["id"]) for doc in documents}
    path_to_node: Dict[str, str] = {}

    # Registered document nodes.
    for doc in documents:
        node_id = f"doc:{doc['id']}"
        path_to_node[str(doc["path"])] = node_id
        builder.add_node(node_id, "document", key=doc["id"], path=doc["path"], title=doc.get("title", {}), layer=doc.get("layer", ""), state=doc.get("state", ""), role=doc.get("role", {}), identity_source=doc.get("id_source", ""))

    artifacts = config.get("source_artifacts", {}) if isinstance(config.get("source_artifacts"), Mapping) else {}
    dedicated_paths = {
        str(raw.get("path")) for raw in artifacts.values() if isinstance(raw, Mapping) and raw.get("path") and raw.get("parser") in {"glossary", "markdown_map"}
    }

    # Existing public Markdown not yet registered in the manifest-derived search index.
    for path_value in observed_markdown_paths(root, config, dedicated_paths):
        if path_value in path_to_node:
            continue
        path_to_node[path_value] = make_observed_node(builder, root, path_value)

    # Layer nodes and placement for all document/observed-document nodes.
    layers = manifest.get("layers", {}) if isinstance(manifest.get("layers"), Mapping) else {}
    for layer_id, raw in layers.items():
        if not isinstance(raw, Mapping) or str(layer_id) == "private_core_marker":
            continue
        builder.add_node(f"layer:{layer_id}", "layer", key=str(layer_id), path=str(raw.get("path", "")), label={"ja": str(raw.get("label_ja", "")), "en": str(raw.get("label_en", ""))})
    for path_value, node_id in sorted(path_to_node.items()):
        resolved = layer_for_path(path_value, layers)
        if resolved and f"layer:{resolved[0]}" in builder.nodes:
            source_type = "manifest" if node_id.startswith("doc:") else "filesystem"
            builder.add_edge(node_id, "placed_in", f"layer:{resolved[0]}", source_type, "tools/docs_manifest.yml" if source_type == "manifest" else path_value, locator="layer placement")

    # Topic nodes and registered document-topic relations.
    search = search_data.get("search", {}) if isinstance(search_data.get("search"), Mapping) else {}
    topics = search.get("navigation_topics", {}) if isinstance(search.get("navigation_topics"), Mapping) else {}
    for topic_id, raw in topics.items():
        if isinstance(raw, Mapping):
            builder.add_node(f"topic:{topic_id}", "topic", key=str(topic_id), label={"ja": str(raw.get("ja", "")), "en": str(raw.get("en", ""))}, browse=raw.get("browse", {}))
    for doc in documents:
        for topic_id in doc.get("discovery", {}).get("topics", []) or []:
            target = f"topic:{topic_id}"
            if target in builder.nodes:
                builder.add_edge(f"doc:{doc['id']}", "belongs_to_topic", target, "manifest", "tools/docs_manifest.yml", locator=f"documents[path={doc['path']}].discovery.topics")

    # Concept nodes: all declared ownership plus selected logical-contract concepts.
    concept_owner = manifest.get("concept_ownership", {}) if isinstance(manifest.get("concept_ownership"), Mapping) else {}
    concept_ids: set[str] = set(str(k) for k in concept_owner.keys())
    for path_value in path_to_doc_id.keys():
        raw = raw_docs.get(path_value, {})
        logical = raw.get("logical_contract", {}) if isinstance(raw.get("logical_contract"), Mapping) else {}
        for field in ("owns", "imports", "exports"):
            concept_ids.update(str(v) for v in (logical.get(field, []) or []))
        for item in logical.get("delegates", []) or []:
            if isinstance(item, Mapping) and item.get("concept"):
                concept_ids.add(str(item["concept"]))
    for concept_id in sorted(concept_ids):
        owner_path = ""
        cfg = concept_owner.get(concept_id)
        if isinstance(cfg, Mapping):
            owner_path = str(cfg.get("canonical_owner", ""))
        owner_node = path_to_node.get(owner_path)
        builder.add_node(f"concept:{concept_id}", "concept", key=concept_id, canonical_owner=owner_node)

    # Manifest ownership.
    for concept_id, cfg in concept_owner.items():
        if not isinstance(cfg, Mapping):
            continue
        owner_path = str(cfg.get("canonical_owner", ""))
        owner_node = resolve_target_node(builder, root, path_to_node, owner_path, "tools/docs_manifest.yml", "owns", f"concept_ownership.{concept_id}") if owner_path else None
        target = f"concept:{concept_id}"
        if owner_node and target in builder.nodes:
            builder.add_edge(owner_node, "owns", target, "manifest", "tools/docs_manifest.yml", locator=f"concept_ownership.{concept_id}.canonical_owner")

    # Manifest logical contracts for registered documents.
    for path_value in sorted(path_to_doc_id.keys()):
        raw = raw_docs.get(path_value, {})
        source_id = f"doc:{path_to_doc_id[path_value]}"
        logical = raw.get("logical_contract", {}) if isinstance(raw.get("logical_contract"), Mapping) else {}
        for relation in ("owns", "imports", "exports"):
            for concept_id in logical.get(relation, []) or []:
                target = f"concept:{concept_id}"
                if target in builder.nodes:
                    builder.add_edge(source_id, relation, target, "manifest", "tools/docs_manifest.yml", locator=f"documents[path={path_value}].logical_contract.{relation}")
                else:
                    builder.add_diag("unresolved_concept_references", {"source": source_id, "concept_id": str(concept_id), "relation": relation})
        for relation in ("tests", "returns_to"):
            for item in logical.get(relation, []) or []:
                if not isinstance(item, Mapping) or not item.get("target"):
                    continue
                target_path = str(item["target"])
                target_node = resolve_target_node(builder, root, path_to_node, target_path, path_value, relation)
                if target_node:
                    builder.add_edge(source_id, relation, target_node, "manifest", "tools/docs_manifest.yml", locator=f"documents[path={path_value}].logical_contract.{relation}", detail={k: v for k, v in item.items() if k != "target"})
        for item in logical.get("delegates", []) or []:
            if not isinstance(item, Mapping) or not item.get("target"):
                continue
            target_path = str(item["target"])
            target_node = resolve_target_node(builder, root, path_to_node, target_path, path_value, "delegates")
            if target_node:
                builder.add_edge(source_id, "delegates", target_node, "manifest", "tools/docs_manifest.yml", locator=f"documents[path={path_value}].logical_contract.delegates", detail={k: v for k, v in item.items() if k != "target"})
        for item in raw.get("related", []) or []:
            target_path = item.get("target") or item.get("path") if isinstance(item, Mapping) else item
            if not target_path:
                continue
            target_path = str(target_path)
            target_node = resolve_target_node(builder, root, path_to_node, target_path, path_value, "related_to")
            if target_node:
                builder.add_edge(source_id, "related_to", target_node, "manifest", "tools/docs_manifest.yml", locator=f"documents[path={path_value}].related")

    # Observed Markdown topology across registered and unregistered public documents.
    if bool(config.get("markdown_links", {}).get("enabled", True)):
        # Snapshot now; resolution may add a small number of public target stubs on demand.
        for path_value in sorted(list(path_to_node.keys())):
            source_node = path_to_node[path_value]
            abs_path = root / path_value
            if not abs_path.is_file():
                continue
            for lineno, target_path in markdown_links(abs_path, path_value):
                target_node = resolve_target_node(builder, root, path_to_node, target_path, path_value, "links_to", f"L{lineno}")
                if target_node:
                    builder.add_edge(source_node, "links_to", target_node, "markdown", path_value, locator=f"L{lineno}")

    # Dedicated source artifacts and source-specific structural relations.
    source_hashes: Dict[str, str] = {}
    glossary_cfg = artifacts.get("glossary", {}) if isinstance(artifacts.get("glossary"), Mapping) else {}
    glossary_path = str(glossary_cfg.get("path", "GLOSSARY.md"))
    glossary_abs = root / glossary_path
    if glossary_abs.exists():
        source_hashes["glossary_sha256"] = sha256_bytes(glossary_abs.read_bytes())
        glossary_node = str(glossary_cfg.get("node_id", "artifact:glossary"))
        builder.add_node(glossary_node, "source_artifact", key="glossary", path=glossary_path, label={"ja": str(glossary_cfg.get("label_ja", "用語集")), "en": str(glossary_cfg.get("label_en", "Glossary"))})
        parse_glossary(builder, root, glossary_abs, glossary_path, glossary_node, path_to_node)

    system_cfg = artifacts.get("system_map", {}) if isinstance(artifacts.get("system_map"), Mapping) else {}
    system_path = str(system_cfg.get("path", "00_Overview/Scientific_Ontology_System_Map.md"))
    system_abs = root / system_path
    if system_abs.exists():
        source_hashes["system_map_sha256"] = sha256_bytes(system_abs.read_bytes())
        system_node = str(system_cfg.get("node_id", "artifact:system_map"))
        builder.add_node(system_node, "source_artifact", key="system_map", path=system_path, label={"ja": str(system_cfg.get("label_ja", "システムマップ")), "en": str(system_cfg.get("label_en", "System Map"))})
        for lineno, target_path in markdown_links(system_abs, system_path):
            target_node = resolve_target_node(builder, root, path_to_node, target_path, system_path, "map_reference", f"L{lineno}")
            if target_node:
                builder.add_edge(system_node, "map_reference", target_node, "system_map", system_path, locator=f"L{lineno}")

    concept_cfg = artifacts.get("concept_network", {}) if isinstance(artifacts.get("concept_network"), Mapping) else {}
    concept_path = str(concept_cfg.get("path", "00_Overview/Scientific_Ontology_Concept_Network.ja.md"))
    concept_abs = root / concept_path
    concept_doc = str(concept_cfg.get("document_id", "scientific_ontology_concept_network"))
    concept_node = f"doc:{concept_doc}"
    if concept_abs.exists() and concept_node in builder.nodes:
        source_hashes["concept_network_sha256"] = sha256_bytes(concept_abs.read_bytes())
        for lineno, target_path in markdown_links(concept_abs, concept_path):
            target_node = resolve_target_node(builder, root, path_to_node, target_path, concept_path, "concept_network_reference", f"L{lineno}")
            if target_node:
                builder.add_edge(concept_node, "concept_network_reference", target_node, "concept_network", concept_path, locator=f"L{lineno}")

    nodes = sorted(builder.nodes.values(), key=lambda n: n["id"])
    edges: List[Dict[str, Any]] = []
    for key in sorted(builder.edges):
        edge = builder.edges[key]
        edge["provenance"] = sorted(edge["provenance"], key=lambda p: (str(p.get("source_type", "")), str(p.get("source_path", "")), str(p.get("locator", "")), json.dumps(p.get("detail", {}), ensure_ascii=False, sort_keys=True)))
        edges.append(edge)
    diagnostics = {key: sorted(items, key=lambda item: json.dumps(item, ensure_ascii=False, sort_keys=True)) for key, items in builder.diagnostics.items()}

    graph = {
        "schema_version": SCHEMA_VERSION,
        "source": {
            "manifest_sha256": sha256_bytes(manifest_bytes),
            "search_config_sha256": sha256_bytes(search_bytes),
            "graph_config_sha256": sha256_bytes(graph_config_bytes),
            "visibility_profile": visibility,
            **source_hashes,
        },
        "principles": list(config.get("principles", []) or []),
        "relation_types": config.get("relation_types", {}),
        "nodes": nodes,
        "edges": edges,
        "diagnostics": diagnostics,
    }
    validate_graph(graph)
    return graph


def validate_graph(graph: Mapping[str, Any]) -> None:
    if graph.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("Unexpected graph schema_version")
    node_ids: set[str] = set()
    for node in graph.get("nodes", []):
        node_id = str(node.get("id", ""))
        if not node_id or ":" not in node_id or node_id in node_ids:
            raise ValueError(f"Invalid or duplicate graph node ID: {node_id}")
        node_ids.add(node_id)
    relations = set((graph.get("relation_types") or {}).keys())
    for edge in graph.get("edges", []):
        if edge.get("from") not in node_ids or edge.get("to") not in node_ids:
            raise ValueError(f"Edge references unknown node: {edge}")
        if edge.get("relation") not in relations:
            raise ValueError(f"Unknown relation type: {edge.get('relation')}")
        if not isinstance(edge.get("provenance"), list) or not edge["provenance"]:
            raise ValueError(f"Edge lacks provenance: {edge}")
    serialized = json.dumps(graph, ensure_ascii=False)
    for marker in FORBIDDEN_TEXT:
        if marker.casefold() in serialized.casefold():
            raise ValueError(f"Forbidden local/private marker in graph: {marker}")
    if "99_Private_Core_Not_Included" in serialized:
        raise ValueError("Private-core path leaked into graph output")


def render_graph(graph: Mapping[str, Any]) -> str:
    return json.dumps(graph, ensure_ascii=False, indent=2) + "\n"


def build_parser() -> argparse.ArgumentParser:
    root = repo_root()
    parser = argparse.ArgumentParser(description="Build deterministic Scientific Ontology typed relation graph.")
    parser.add_argument("--root", default=str(root))
    parser.add_argument("--manifest", default="tools/docs_manifest.yml")
    parser.add_argument("--search-config", default="tools/docs_search.yml")
    parser.add_argument("--graph-config", default="tools/docs_graph.yml")
    parser.add_argument("--output", default="tools/docs_graph.json")
    parser.add_argument("--visibility", choices=["preview", "public"], default="preview")
    parser.add_argument("--check", action="store_true")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = Path(args.root).resolve()
    try:
        graph = build_graph(root, root / args.manifest, root / args.search_config, root / args.graph_config, args.visibility)
        rendered = render_graph(graph)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    output = root / args.output
    if args.check:
        if not output.exists():
            print(f"STALE: graph does not exist: {output}", file=sys.stderr)
            return 1
        existing = output.read_text(encoding="utf-8")
        try:
            validate_graph(json.loads(existing))
        except Exception as exc:
            print(f"INVALID: existing graph failed validation: {exc}", file=sys.stderr)
            return 1
        if existing != rendered:
            print("STALE: tools/docs_graph.json does not match current sources/configuration.", file=sys.stderr)
            diff = difflib.unified_diff(existing.splitlines(), rendered.splitlines(), fromfile="tracked", tofile="expected", lineterm="")
            for line in list(diff)[:120]:
                print(line, file=sys.stderr)
            return 1
        print(f"GRAPH CHECK PASS ({len(graph['nodes'])} nodes, {len(graph['edges'])} edges, visibility={args.visibility})")
        return 0

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(rendered, encoding="utf-8", newline="\n")
    print(f"GRAPH BUILD PASS ({len(graph['nodes'])} nodes, {len(graph['edges'])} edges, visibility={args.visibility})")
    diag = graph.get("diagnostics", {})
    print(
        "GRAPH DIAGNOSTICS "
        f"({len(diag.get('observed_unregistered_documents', []))} observed-unregistered docs, "
        f"{len(diag.get('unresolved_document_references', []))} missing refs, "
        f"{len(diag.get('unresolved_concept_references', []))} unresolved concepts, "
        f"{len(diag.get('excluded_references', []))} excluded refs)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

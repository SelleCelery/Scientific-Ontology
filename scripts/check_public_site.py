#!/usr/bin/env python3
"""Validate the built Scientific Ontology GitHub Pages artifact itself."""
from __future__ import annotations

import argparse
import json
import posixpath
import re
import sys
import urllib.parse
from pathlib import Path, PurePosixPath
from typing import Any

from public_site_common import (
    EXTERNAL_SCHEME_RE,
    MARKDOWN_LINK_RE,
    TEXT_EXTENSIONS,
    find_forbidden_keys,
    load_json,
    load_yaml,
    norm_rel,
    path_is_forbidden,
    resolve_local_target,
    sha256_file,
    strict_utf8,
    tree_records,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "tools" / "public_site.yml"


class CheckFailure(RuntimeError):
    pass


def fail_if(condition: bool, message: str) -> None:
    if condition:
        raise CheckFailure(message)


def check_local_links(site: Path, documents: list[str]) -> tuple[int, int]:
    local_links = 0
    external_links = 0
    for rel in documents:
        path = site / rel
        text = strict_utf8(path)
        for match in MARKDOWN_LINK_RE.finditer(text):
            href = match.group(2).strip()
            if not href or href.startswith("#"):
                continue
            if EXTERNAL_SCHEME_RE.match(href):
                external_links += 1
                continue
            target, _query, _fragment = resolve_local_target(rel, href)
            if target is None:
                continue
            local_links += 1
            target_path = site / target
            fail_if(not target_path.is_file(), f"broken artifact-local link: {rel}: {href!r} -> {target}")
    return local_links, external_links


def collect_public_content_paths(value: Any, found: set[str]) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if key in {"path", "document_path", "read_path"} and isinstance(child, str) and child.endswith(".md"):
                found.add(norm_rel(child))
            collect_public_content_paths(child, found)
    elif isinstance(value, list):
        for child in value:
            collect_public_content_paths(child, found)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=str(ROOT), help="repository root")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG), help="public-site config")
    parser.add_argument("--site-dir", default=None, help="built site directory; default comes from config")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    config_path = Path(args.config)
    if not config_path.is_absolute():
        config_path = root / config_path
    cfg = load_yaml(config_path)
    site = Path(args.site_dir) if args.site_dir else Path(str(cfg["site"]["output_dir"]))
    if not site.is_absolute():
        site = root / site
    site = site.resolve()

    try:
        fail_if(not site.is_dir(), f"public site directory does not exist: {site}")
        manifest_rel = norm_rel(str(cfg["artifact"]["manifest_path"]))
        manifest_path = site / manifest_rel
        fail_if(not manifest_path.is_file(), f"artifact manifest is missing: {manifest_rel}")
        manifest = load_json(manifest_path)
        fail_if(manifest.get("build_contract") != "scientific-ontology-public-site", "unexpected public-site build contract")

        actual_records = tree_records(site, exclude={manifest_rel})
        expected_records = manifest.get("files", [])
        fail_if(actual_records != expected_records, "artifact file list or SHA-256 hashes differ from public_site_manifest.json")

        required = [norm_rel(str(path)) for path in cfg.get("artifact", {}).get("required_files", [])]
        for rel in required:
            fail_if(not (site / rel).is_file(), f"required artifact file is missing: {rel}")

        actual_paths = {path.relative_to(site).as_posix() for path in site.rglob("*") if path.is_file()}
        for rel in sorted(actual_paths):
            if rel in {manifest_rel, str(cfg["artifact"]["nojekyll_path"])}:
                continue
            fail_if(path_is_forbidden(rel, cfg), f"forbidden path present in Pages artifact: {rel}")

        catalog_rel = norm_rel(str(cfg["public_data_targets"]["catalog"]))
        graph_rel = norm_rel(str(cfg["public_data_targets"]["graph"]))
        catalog = load_json(site / catalog_rel)
        graph = load_json(site / graph_rel)
        source_catalog = root / cfg["sources"]["public_catalog"]
        source_graph = root / cfg["sources"]["public_graph"]
        fail_if(
            manifest.get("source", {}).get("public_catalog_sha256") != sha256_file(source_catalog),
            "artifact was built from a different public catalog than the current repository",
        )
        fail_if(
            manifest.get("source", {}).get("public_graph_sha256") != sha256_file(source_graph),
            "artifact was built from a different public graph than the current repository",
        )
        fail_if(sha256_file(site / catalog_rel) != sha256_file(source_catalog), "artifact public catalog differs from repository source")
        fail_if(sha256_file(site / graph_rel) != sha256_file(source_graph), "artifact public graph differs from repository source")

        documents = sorted(norm_rel(str(doc.get("path", ""))) for doc in catalog.get("documents", []))
        fail_if(any(not rel for rel in documents), "public catalog contains empty document path")
        fail_if(documents != sorted(manifest.get("documents", [])), "artifact manifest document list differs from public catalog")
        for rel in documents:
            fail_if(path_is_forbidden(rel, cfg), f"forbidden document in public catalog: {rel}")
            fail_if(not (site / rel).is_file(), f"catalog document missing from artifact: {rel}")
            strict_utf8(site / rel)

        graph_documents = sorted(
            norm_rel(str(node.get("path")))
            for node in graph.get("nodes", [])
            if node.get("type") in {"document", "observed_document"} and node.get("path")
        )
        fail_if(graph_documents != documents, "public graph document paths differ from public catalog")

        forbidden_catalog_keys = set(map(str, cfg.get("safety", {}).get("forbidden_public_catalog_keys", [])))
        forbidden_graph_keys = set(map(str, cfg.get("safety", {}).get("forbidden_public_graph_keys", [])))
        catalog_hits = find_forbidden_keys(catalog, forbidden_catalog_keys)
        graph_hits = find_forbidden_keys(graph, forbidden_graph_keys)
        fail_if(bool(catalog_hits), f"developer-only keys found in public catalog: {catalog_hits[:20]}")
        fail_if(bool(graph_hits), f"developer-only keys found in public graph: {graph_hits[:20]}")

        for path in site.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in TEXT_EXTENSIONS:
                continue
            strict_utf8(path)

        root_html = strict_utf8(site / "index.html")
        fail_if("navigator/" not in root_html, "root index does not lead to Navigator")
        public_html = strict_utf8(site / "navigator/index.html")
        fail_if('data-interface="public"' not in public_html, "Navigator public shell marker is missing")
        fail_if("dev.html" in public_html or "候補レビュー" in public_html, "developer UI marker leaked into public HTML")
        fail_if((site / "navigator/dev.html").exists(), "developer shell is present in Pages artifact")
        fail_if((site / "navigator/src").exists(), "TypeScript source directory is present in Pages artifact")

        public_content = load_json(site / "navigator/public-content.json")
        public_content_paths: set[str] = set()
        collect_public_content_paths(public_content, public_content_paths)
        for rel in sorted(public_content_paths):
            fail_if(rel not in set(documents), f"public-content.json references non-catalog document: {rel}")
            fail_if(not (site / rel).is_file(), f"public-content.json target is missing: {rel}")

        local_links, external_links = check_local_links(site, documents)

        expected_counts = manifest.get("counts", {})
        fail_if(expected_counts.get("documents") != len(documents), "artifact document count mismatch")
        fail_if(expected_counts.get("graph_nodes") != len(graph.get("nodes", [])), "artifact graph node count mismatch")
        fail_if(expected_counts.get("graph_edges") != len(graph.get("edges", [])), "artifact graph edge count mismatch")

        print(
            "PUBLIC SITE ARTIFACT CHECK PASS: "
            f"{len(documents)} documents, {len(graph.get('nodes', []))} graph nodes, "
            f"{len(graph.get('edges', []))} graph edges, {local_links} local links, "
            f"{external_links} external links, {len(actual_paths)} files"
        )
        return 0
    except (CheckFailure, ValueError, KeyError, json.JSONDecodeError, UnicodeDecodeError) as exc:
        print(f"PUBLIC SITE ARTIFACT CHECK BLOCKED: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

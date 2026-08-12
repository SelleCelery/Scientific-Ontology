#!/usr/bin/env python3
"""Build the safe static GitHub Pages artifact for Scientific Ontology."""
from __future__ import annotations

import argparse
import json
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any

from public_site_common import (
    MARKDOWN_LINK_RE,
    github_blob_url,
    load_json,
    load_yaml,
    norm_rel,
    path_is_forbidden,
    resolve_local_target,
    sha256_file,
    tree_records,
    write_json,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "tools" / "public_site.yml"


class BuildError(RuntimeError):
    pass


def copy_bytes(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(source.read_bytes())


def root_index(target: str) -> str:
    target = target.strip("/") + "/"
    return f"""<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta http-equiv="refresh" content="0; url=./{target}">
  <meta name="description" content="Scientific Ontology / 存在境界論 Public Navigator">
  <title>Scientific Ontology / 存在境界論</title>
  <script>location.replace("./{target}" + location.hash);</script>
</head>
<body>
  <p><a href="./{target}">Scientific Ontology / 存在境界論 Navigator を開く</a></p>
</body>
</html>
"""


def rewrite_markdown(
    text: str,
    source_rel: str,
    root: Path,
    public_documents: set[str],
    asset_extensions: set[str],
    assets: set[str],
    rewrites: list[dict[str, str]],
    repository_url: str,
    source_ref: str,
    cfg: dict[str, Any],
) -> str:
    def replace(match):
        prefix, href, suffix = match.groups()
        target, query, fragment = resolve_local_target(source_rel, href)
        if target is None:
            return match.group(0)

        source_target = root / target
        if not source_target.exists() or not source_target.is_file():
            raise BuildError(f"broken local link in {source_rel}: {href!r} -> {target}")

        extension = source_target.suffix.lower()
        if target in public_documents:
            return match.group(0)

        if extension in asset_extensions and not path_is_forbidden(target, cfg):
            assets.add(target)
            return match.group(0)

        external = github_blob_url(repository_url, source_ref, target, query, fragment)
        rewrites.append({"source": source_rel, "target": target, "from": href, "to": external})
        return f"{prefix}{external}{suffix}"

    return MARKDOWN_LINK_RE.sub(replace, text)


def build_site(root: Path, output: Path, config_path: Path, source_ref_override: str | None = None) -> dict[str, Any]:
    cfg = load_yaml(config_path)
    release_state_path = root / cfg["sources"]["release_state"]
    release_state = load_yaml(release_state_path)
    repository_url = str(release_state.get("project", {}).get("repository_url", "")).strip()
    if not repository_url:
        raise BuildError(f"repository_url is missing in {release_state_path}")
    source_ref = source_ref_override or str(cfg.get("site", {}).get("source_ref", "main"))

    catalog_path = root / cfg["sources"]["public_catalog"]
    graph_path = root / cfg["sources"]["public_graph"]
    catalog = load_json(catalog_path)
    graph = load_json(graph_path)

    documents = catalog.get("documents", [])
    public_documents = {norm_rel(str(doc.get("path", ""))) for doc in documents}
    if "" in public_documents:
        raise BuildError("public catalog contains an empty document path")

    graph_documents = {
        norm_rel(str(node.get("path")))
        for node in graph.get("nodes", [])
        if node.get("type") in {"document", "observed_document"} and node.get("path")
    }
    if graph_documents != public_documents:
        missing_from_graph = sorted(public_documents - graph_documents)
        missing_from_catalog = sorted(graph_documents - public_documents)
        raise BuildError(
            "public catalog / graph document sets differ: "
            f"catalog-only={missing_from_graph[:10]}, graph-only={missing_from_catalog[:10]}"
        )

    for rel in sorted(public_documents):
        if path_is_forbidden(rel, cfg):
            raise BuildError(f"forbidden public document path: {rel}")
        source = root / rel
        if not source.is_file():
            raise BuildError(f"public document does not exist: {rel}")
        source.read_bytes().decode("utf-8", errors="strict")

    output = output.resolve()
    if output == root.resolve() or output in root.resolve().parents:
        raise BuildError(f"refusing unsafe output directory: {output}")
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True, exist_ok=True)

    copied_navigator: list[str] = []
    for rel in cfg["sources"].get("navigator_public_files", []):
        rel = norm_rel(str(rel))
        if path_is_forbidden(rel, cfg):
            raise BuildError(f"navigator public file is forbidden: {rel}")
        source = root / rel
        if not source.is_file():
            raise BuildError(f"navigator public file is missing: {rel}")
        copy_bytes(source, output / rel)
        copied_navigator.append(rel)

    for pattern in cfg["sources"].get("navigator_public_globs", []):
        for source in sorted(root.glob(str(pattern))):
            if not source.is_file():
                continue
            rel = source.relative_to(root).as_posix()
            if path_is_forbidden(rel, cfg):
                raise BuildError(f"navigator glob selected forbidden file: {rel}")
            copy_bytes(source, output / rel)
            copied_navigator.append(rel)

    public_data = [
        norm_rel(str(cfg["public_data_targets"]["catalog"])),
        norm_rel(str(cfg["public_data_targets"]["graph"])),
    ]
    for rel in public_data:
        copy_bytes(root / rel, output / rel)

    asset_extensions = {str(ext).lower() for ext in cfg.get("assets", {}).get("copy_extensions", [])}
    assets: set[str] = set()
    rewrites: list[dict[str, str]] = []

    for rel in sorted(public_documents):
        source = root / rel
        text = source.read_text(encoding="utf-8")
        rewritten = rewrite_markdown(
            text,
            rel,
            root,
            public_documents,
            asset_extensions,
            assets,
            rewrites,
            repository_url,
            source_ref,
            cfg,
        )
        destination = output / rel
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(rewritten, encoding="utf-8", newline="\n")

    for rel in sorted(assets):
        copy_bytes(root / rel, output / rel)

    redirect_target = str(cfg.get("site", {}).get("root_redirect_target", "navigator/"))
    (output / "index.html").write_text(root_index(redirect_target), encoding="utf-8", newline="\n")
    (output / str(cfg["artifact"]["nojekyll_path"])).write_bytes(b"")

    manifest_rel = norm_rel(str(cfg["artifact"]["manifest_path"]))
    source_payload = {
        "repository_url": repository_url,
        "source_ref": source_ref,
        "release_version": release_state.get("release", {}).get("version"),
        "release_status": release_state.get("release", {}).get("status"),
        "public_catalog_sha256": sha256_file(catalog_path),
        "public_graph_sha256": sha256_file(graph_path),
    }
    records = tree_records(output, exclude={manifest_rel})
    manifest = {
        "schema_version": "0.1",
        "build_contract": "scientific-ontology-public-site",
        "source": source_payload,
        "counts": {
            "documents": len(public_documents),
            "registered_documents": catalog.get("source", {}).get("registered_documents"),
            "provisional_documents": catalog.get("source", {}).get("provisional_documents"),
            "graph_nodes": len(graph.get("nodes", [])),
            "graph_edges": len(graph.get("edges", [])),
            "navigator_files": len(set(copied_navigator)),
            "assets": len(assets),
            "externalized_links": len(rewrites),
            "payload_files": len(records),
        },
        "documents": sorted(public_documents),
        "assets": sorted(assets),
        "externalized_links": sorted(rewrites, key=lambda item: (item["source"], item["target"], item["from"])),
        "files": records,
    }
    write_json(output / manifest_rel, manifest)
    return manifest


def tree_digest(root: Path) -> dict[str, str]:
    return {record["path"]: record["sha256"] for record in tree_records(root)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=str(ROOT), help="repository root")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG), help="public-site config")
    parser.add_argument("--output", default=None, help="artifact directory; default comes from config")
    parser.add_argument("--source-ref", default=None, help="GitHub source ref used when externalizing non-site links")
    parser.add_argument("--check", action="store_true", help="compare tracked artifact directory with a fresh deterministic build")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    config_path = Path(args.config)
    if not config_path.is_absolute():
        config_path = root / config_path
    cfg = load_yaml(config_path)
    output = Path(args.output) if args.output else Path(str(cfg["site"]["output_dir"]))
    if not output.is_absolute():
        output = root / output

    try:
        if args.check:
            if not output.exists():
                raise BuildError(f"public site artifact does not exist: {output}")
            with tempfile.TemporaryDirectory(prefix="so-public-site-") as temp_dir:
                temp_output = Path(temp_dir) / "pages"
                build_site(root, temp_output, config_path, args.source_ref)
                expected = tree_digest(temp_output)
                actual = tree_digest(output)
                if expected != actual:
                    added = sorted(set(actual) - set(expected))
                    missing = sorted(set(expected) - set(actual))
                    changed = sorted(path for path in set(actual).intersection(expected) if actual[path] != expected[path])
                    raise BuildError(
                        "PUBLIC SITE CHECK FAILED: artifact is stale or differs from deterministic build\n"
                        f"  extra={added[:20]}\n  missing={missing[:20]}\n  changed={changed[:20]}"
                    )
            print(f"PUBLIC SITE BUILD CHECK PASS: {output}")
            return 0

        manifest = build_site(root, output, config_path, args.source_ref)
        counts = manifest["counts"]
        print(
            "PUBLIC SITE BUILD PASS: "
            f"{counts['documents']} documents, {counts['assets']} assets, "
            f"{counts['externalized_links']} externalized links, {counts['payload_files']} payload files"
        )
        print(f"OUTPUT {output}")
        return 0
    except (BuildError, ValueError, KeyError, json.JSONDecodeError, UnicodeDecodeError) as exc:
        print(f"PUBLIC SITE BUILD BLOCKED: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

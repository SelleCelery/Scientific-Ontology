#!/usr/bin/env python3
"""Validate the Public / Developer Navigator interface and data boundary."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_CONTENT = ROOT / "navigator" / "public-content.json"
PUBLIC_HTML = ROOT / "navigator" / "index.html"
DEV_HTML = ROOT / "navigator" / "dev.html"
APP_SOURCE = ROOT / "navigator" / "src" / "app.ts"
LANGUAGE_CORE = ROOT / "navigator" / "src" / "language-core.ts"
READING_CORE = ROOT / "navigator" / "src" / "reader-core.ts"
READING_RUNTIME = ROOT / "navigator" / "dist" / "reader-core.js"
NAVIGATOR_STYLES = ROOT / "navigator" / "styles.css"
GRAPH = ROOT / "tools" / "docs_graph.json"
PUBLIC_GRAPH = ROOT / "tools" / "docs_public_graph.json"
PUBLIC_CATALOG = ROOT / "tools" / "docs_public_catalog.json"
REGISTRATION_WORKBENCH_PREVIEW = ROOT / "tools" / "docs_registration_workbench.preview.json"
EDITORIAL_VALIDATOR = ROOT / "scripts" / "validate_navigator_editorial_selection.py"
EDITORIAL_APPLIER = ROOT / "scripts" / "apply_navigator_editorial_selection.py"
KATEX_DIR = ROOT / "navigator" / "vendor" / "katex"
KATEX_RUNTIME = KATEX_DIR / "katex.mjs"
KATEX_CSS = KATEX_DIR / "katex.min.css"
KATEX_LICENSE = KATEX_DIR / "LICENSE"
KATEX_NOTICE = KATEX_DIR / "NOTICE.txt"

BLOCKED_MARKERS = ("99_Private_Core", "private-core", "Private_Core", "/Gate", "/U5")
DEVELOPER_ONLY_KEYS = {
    "review",
    "evidence",
    "needs_human_judgment",
    "confidence",
    "recommended_action",
    "observed_node_id",
    "candidate_source_sha256",
    "manifest_sha256",
    "search_config_sha256",
    "canonical_index_sha256",
    "graph_sha256",
    "reviewer_note",
    "reviewed_at",
    "decisions",
    "manual_candidates",
    "revision_candidates",
}
HEADER_CONTROLS = ("header-menu", "header-back", "header-top", "header-bottom")
PUBLIC_RELEASE_STATUS_MARKERS = (
    'class="release-status-banner"',
    "Living Preview",
    "最新の公開研究面",
    "https://doi.org/10.5281/zenodo.21909382",
)


def fail(message: str) -> int:
    print(f"NAVIGATOR INTERFACE CHECK FAIL: {message}", file=sys.stderr)
    return 1


def forbidden_keys(value, forbidden: set[str], found: set[str]) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if str(key) in forbidden:
                found.add(str(key))
            forbidden_keys(child, forbidden, found)
    elif isinstance(value, list):
        for child in value:
            forbidden_keys(child, forbidden, found)


def main() -> int:
    required_files = (
        PUBLIC_CONTENT,
        PUBLIC_HTML,
        DEV_HTML,
        APP_SOURCE,
        LANGUAGE_CORE,
        READING_CORE,
        READING_RUNTIME,
        NAVIGATOR_STYLES,
        GRAPH,
        PUBLIC_GRAPH,
        PUBLIC_CATALOG,
        REGISTRATION_WORKBENCH_PREVIEW,
        EDITORIAL_VALIDATOR,
        EDITORIAL_APPLIER,
        KATEX_RUNTIME,
        KATEX_CSS,
        KATEX_LICENSE,
        KATEX_NOTICE,
    )
    for path in required_files:
        if not path.is_file():
            return fail(f"missing {path.relative_to(ROOT)}")
        try:
            path.read_bytes().decode("utf-8", errors="strict")
        except UnicodeDecodeError as exc:
            return fail(f"{path.relative_to(ROOT)} is not strict UTF-8: {exc}")

    katex_css = KATEX_CSS.read_text(encoding="utf-8")
    katex_runtime = KATEX_RUNTIME.read_text(encoding="utf-8")
    navigator_styles = NAVIGATOR_STYLES.read_text(encoding="utf-8")
    if "gradio-container-" in katex_css:
        return fail("KaTeX stylesheet still carries a host-specific Gradio selector scope")

    mathml_rule = re.search(r"\.katex \.katex-mathml\{([^}]*)\}", katex_css)
    if not mathml_rule:
        return fail("KaTeX stylesheet is missing the standard .katex .katex-mathml rule")
    normalized_mathml_rule = mathml_rule.group(1).replace(" ", "")
    required_mathml_hiding = (
        "clip:rect(1px,1px,1px,1px)",
        "height:1px",
        "overflow:hidden",
        "position:absolute",
        "width:1px",
    )
    for declaration in required_mathml_hiding:
        if declaration not in normalized_mathml_rule:
            return fail(f"KaTeX MathML visual-hiding contract is incomplete: missing {declaration}")
    if "display:none" in normalized_mathml_rule or "visibility:hidden" in normalized_mathml_rule:
        return fail("KaTeX MathML must remain accessibility-visible, not display:none/visibility:hidden")

    version_match = re.search(r"\.katex \.katex-version:after\{content:\"([^\"]+)\"\}", katex_css)
    if not version_match:
        return fail("KaTeX stylesheet version marker is missing")
    katex_version = version_match.group(1)
    if katex_version not in katex_runtime:
        return fail(f"KaTeX CSS/runtime version mismatch: CSS={katex_version}")

    local_katex_assets: set[str] = set()
    for raw_url in re.findall(r"url\(([^)]+)\)", katex_css):
        ref = raw_url.strip().strip("'\"")
        if not ref or ref.startswith("data:"):
            continue
        if re.match(r"^(?:https?:)?//", ref, flags=re.I):
            return fail(f"KaTeX stylesheet introduces a network asset: {ref}")
        if ref.startswith(("/", "\\")) or re.match(r"^[A-Za-z]:", ref):
            return fail(f"KaTeX stylesheet contains a non-relative asset path: {ref}")
        resolved = (KATEX_DIR / ref).resolve()
        if not resolved.is_relative_to(KATEX_DIR.resolve()):
            return fail(f"KaTeX stylesheet escapes its vendor directory: {ref}")
        local_katex_assets.add(ref)
        if not resolved.is_file():
            return fail(f"KaTeX stylesheet references missing local asset: {ref}")
    if not local_katex_assets:
        return fail("KaTeX stylesheet contains no local font references")

    # KaTeX 0.16.x uses short internal class names. Host CSS using the same
    # generic classes can override math even when KaTeX itself is correctly
    # scoped beneath .katex. Keep the Navigator stylesheet clear of the most
    # collision-prone internal names and test real cascade behavior in Chromium.
    collision_classes = (
        "base", "rule", "strut", "vlist", "pstrut", "tag", "newline",
        "mord", "mop", "mbin", "mrel", "mopen", "mclose", "mpunct", "minner",
    )
    collision_pattern = re.compile(r"\.(?:" + "|".join(map(re.escape, collision_classes)) + r")\b")
    collisions = sorted(set(match.group(0) for match in collision_pattern.finditer(navigator_styles)))
    if collisions:
        return fail(f"Navigator stylesheet collides with KaTeX internal class name(s): {collisions}")

    data = json.loads(PUBLIC_CONTENT.read_text(encoding="utf-8"))
    if data.get("schema_version") != "0.1":
        return fail("navigator/public-content.json schema_version must be 0.1")

    layers = data.get("layers") or []
    guides = data.get("guides") or []
    if not isinstance(layers, list) or not layers:
        return fail("public-content layers must be a non-empty list")
    if not isinstance(guides, list) or not guides:
        return fail("public-content guides must be a non-empty list")

    layer_ids: set[str] = set()
    configured_paths: list[str] = []
    home_groups: dict[str, list[str]] = {"contact": [], "working": [], "core": [], "guide": []}
    for layer in layers:
        layer_id = str(layer.get("id") or "")
        if not layer_id or layer_id in layer_ids:
            return fail(f"invalid/duplicate layer id: {layer_id!r}")
        layer_ids.add(layer_id)
        group = str(layer.get("home_group") or "")
        if group not in home_groups:
            return fail(f"layer {layer_id} has invalid/missing home_group: {group!r}")
        home_groups[group].append(layer_id)
        layer_path = str(layer.get("path") or "")
        if not layer_path or not (ROOT / layer_path).is_dir():
            return fail(f"layer {layer_id} has missing repository path: {layer_path!r}")
        readme = str(layer.get("readme_path") or "")
        if readme:
            configured_paths.append(readme)

    expected_home_groups = {
        "contact": ["creative_offshoots", "visual_materials"],
        "working": ["applications", "research_notes"],
        "core": ["sat_truth", "raj_beauty", "tam_goodness"],
        "guide": ["overview"],
    }
    layer_by_id = {str(layer.get("id") or ""): layer for layer in layers}
    ordered_home_groups = {
        group: sorted(ids, key=lambda layer_id: (int(layer_by_id[layer_id].get("order", 999)), layer_id))
        for group, ids in home_groups.items()
    }
    if ordered_home_groups != expected_home_groups:
        return fail(f"reader-facing home topology mismatch: {ordered_home_groups!r}")

    guide_ids: set[str] = set()
    for guide in guides:
        guide_id = str(guide.get("id") or "")
        if not guide_id or guide_id in guide_ids:
            return fail(f"invalid/duplicate guide id: {guide_id!r}")
        guide_ids.add(guide_id)
        path_value = guide.get("path")
        if isinstance(path_value, dict):
            paths = [str(value or "") for value in path_value.values() if str(value or "")]
        else:
            paths = [str(path_value or "")] if str(path_value or "") else []
        if not paths:
            return fail(f"guide {guide_id} missing path")
        configured_paths.extend(paths)

    graph = json.loads(GRAPH.read_text(encoding="utf-8"))
    public_graph = json.loads(PUBLIC_GRAPH.read_text(encoding="utf-8"))
    if "source" in public_graph or "diagnostics" in public_graph:
        return fail("public graph exposes canonical source hashes or developer diagnostics")
    if public_graph.get("nodes") != graph.get("nodes") or public_graph.get("edges") != graph.get("edges"):
        return fail("public graph semantic projection differs from canonical graph nodes/edges")
    exposed = {
        str(node.get("path") or "")
        for node in public_graph.get("nodes", [])
        if node.get("type") in {"document", "observed_document"}
    }
    for relative in configured_paths:
        normalized = relative.replace("\\", "/")
        if any(part.startswith("000") for part in normalized.split("/")):
            return fail(f"public-content references pending/local path: {relative}")
        if any(marker in normalized for marker in BLOCKED_MARKERS):
            return fail(f"public-content references blocked path: {relative}")
        if not (ROOT / relative).is_file():
            return fail(f"public-content path does not exist: {relative}")
        if relative.endswith(".md") and relative not in exposed:
            return fail(f"public-content Markdown is outside Reader graph boundary: {relative}")

    catalog = json.loads(PUBLIC_CATALOG.read_text(encoding="utf-8"))
    leaked_catalog_keys: set[str] = set()
    forbidden_keys(catalog, DEVELOPER_ONLY_KEYS, leaked_catalog_keys)
    if leaked_catalog_keys:
        return fail(f"public catalog leaks developer-only key(s): {sorted(leaked_catalog_keys)}")
    if str(catalog.get("catalog_contract_version") or "") != "0.4":
        return fail("public catalog contract_version must be 0.4 for language-resolved presentation")
    catalog_docs = catalog.get("documents") or []
    catalog_paths = {str(doc.get("path") or "") for doc in catalog_docs}
    reading_channels = data.get("reading_channels", [])
    if not isinstance(reading_channels, list) or not reading_channels:
        return fail("public-content reading_channels must be a non-empty list")
    by_id = {str(doc.get("id") or doc.get("doc_id") or ""): doc for doc in catalog_docs}
    channel_ids: set[str] = set()
    selected_count = 0
    for channel in reading_channels:
        if not isinstance(channel, dict) or not isinstance(channel.get("id"), str) or not channel["id"].strip():
            return fail("reading channel requires a non-empty id")
        channel_id = channel["id"]
        if channel_id in channel_ids:
            return fail(f"duplicate reading channel id: {channel_id}")
        channel_ids.add(channel_id)
        for field in ("title", "description"):
            values = channel.get(field)
            if not isinstance(values, dict) or any(not isinstance(values.get(lang), str) or not values[lang].strip() for lang in ("ja", "en")):
                return fail(f"reading channel requires JA/EN {field}: {channel_id}")
        document_ids = channel.get("documents", [])
        if not isinstance(document_ids, list):
            return fail(f"reading channel documents must be a list: {channel_id}")
        seen_families: set[str] = set()
        for document_id in document_ids:
            doc = by_id.get(str(document_id or ""))
            if not doc:
                return fail(f"reading channel references a non-catalog document: {channel_id}: {document_id}")
            if str(doc.get("path") or "") not in exposed:
                return fail(f"reading channel document is outside the Reader boundary: {channel_id}: {document_id}")
            family = str((doc.get("presentation") or {}).get("family_key") or doc.get("id"))
            if family in seen_families:
                return fail(f"reading channel duplicates a JA/EN family: {channel_id}: {document_id}")
            seen_families.add(family)
            selected_count += 1
    pair_keys: set[str] = set()
    for doc in catalog_docs:
        presentation = doc.get("presentation") or {}
        language = str(presentation.get("language") or "")
        family_key = str(presentation.get("family_key") or "")
        if language not in {"ja", "en", "bilingual", "und"}:
            return fail(f"invalid public presentation language {language!r}: {doc.get('path')}")
        if not family_key:
            return fail(f"missing public presentation family_key: {doc.get('path')}")
        counterpart = str(presentation.get("counterpart_path") or "")
        if counterpart:
            if counterpart not in catalog_paths:
                return fail(f"public presentation counterpart missing from catalog: {counterpart}")
            pair_keys.add(family_key)
    expected_pairs = int((catalog.get("source") or {}).get("language_pair_families") or 0)
    if len(pair_keys) != expected_pairs:
        return fail(f"language pair family count mismatch: metadata={expected_pairs} actual={len(pair_keys)}")
    registered = [doc for doc in catalog_docs if doc.get("registration_state") == "registered"]
    provisional = [doc for doc in catalog_docs if doc.get("registration_state") == "provisional"]
    if not registered:
        return fail("public catalog has no canonical registered documents")
    for doc in provisional:
        path = str(doc.get("path") or "")
        if path not in exposed:
            return fail(f"public provisional document is outside Reader/graph boundary: {path}")
        leaked = sorted(DEVELOPER_ONLY_KEYS.intersection(doc.keys()))
        if leaked:
            return fail(f"public provisional document leaks developer-only key(s) {leaked}: {doc.get('path')}")
        if any((doc.get("concepts") or {}).get(key) for key in ("owned", "imports", "exports")):
            return fail(f"provisional document invents concept contract: {doc.get('path')}")
        if any((doc.get("relations") or {}).get(key) for key in ("related", "tests", "returns_to", "delegates")):
            return fail(f"provisional document invents typed relation contract: {doc.get('path')}")

    public_html = PUBLIC_HTML.read_text(encoding="utf-8")
    dev_html = DEV_HTML.read_text(encoding="utf-8")
    app_source = APP_SOURCE.read_text(encoding="utf-8")
    for html_name, html in (("public", public_html), ("developer", dev_html)):
        if not html.lstrip().lower().startswith("<!doctype html>"):
            return fail(f"{html_name} shell must remain in HTML5 standards mode for KaTeX")
    if 'data-interface="public"' not in public_html:
        return fail("navigator/index.html must declare data-interface=public")
    if 'data-interface="developer"' not in dev_html:
        return fail("navigator/dev.html must declare data-interface=developer")
    for marker in PUBLIC_RELEASE_STATUS_MARKERS:
        if marker not in public_html:
            return fail(f"public shell missing release-status marker: {marker}")
    for html_name, html in (("public", public_html), ("developer", dev_html)):
        for control in HEADER_CONTROLS:
            if f'id="{control}"' not in html:
                return fail(f"{html_name} shell missing fixed header control: {control}")
    for marker in ("Candidate review", "Claim audit lab", "Data audit", "docs_registration_workbench", "docs_revision_proposals", "repository_assessment_protocols"):
        if marker in public_html:
            return fail(f"public shell exposes developer marker: {marker}")

    for html_name, html in (("public", public_html), ("developer", dev_html)):
        if './vendor/katex/katex.min.css' not in html:
            return fail(f"{html_name} shell missing local KaTeX stylesheet")
    if 'import("../vendor/katex/katex.mjs")' not in app_source:
        return fail("Reader does not load the vendored KaTeX runtime")
    if 'katex.render(tex, node' not in app_source:
        return fail("Reader does not render parsed TeX through KaTeX")

    required_source_fragments = (
        'document.body.dataset.interface === "developer"',
        'fetch(PUBLIC_CATALOG_URL)',
        'isDeveloper() ? DEVELOPER_GRAPH_URL : PUBLIC_GRAPH_URL',
        'isDeveloper()\n      ? fetch(REGISTRATION_WORKBENCH_URL)',
        'fetch(PUBLIC_CONTENT_URL)',
        'collapseDocumentsForLanguage',
        'collapseDocumentsForLanguage(registeredDocs, allDocuments(), displayLang)',
        'publicLayersForHomeGroup("contact")',
        'publicLayersForHomeGroup("working")',
        'publicLayersForHomeGroup("core")',
        'publicLayersForHomeGroup("guide")',
        'collapseSearchResultsForLanguage',
        'preferredPathForLanguage',
        'publicDocumentTitle',
        'readingChannelEntries',
        'function renderReadingEditor()',
        'navigator_editorial_selection',
    )
    for fragment in required_source_fragments:
        if fragment not in app_source:
            return fail(f"runtime boundary fragment missing from app.ts: {fragment}")

    print(
        "NAVIGATOR INTERFACE CHECK PASS: "
        f"{len(layers)} reader navigation surfaces, {len(guides)} guide entrances, {len(reading_channels)} editorial channels / {selected_count} selected documents, "
        f"{len(registered)} registered + {len(provisional)} provisional public documents, "
        f"{len(pair_keys)} JA/EN presentation pairs, developer review data isolated"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

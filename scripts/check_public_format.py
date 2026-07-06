#!/usr/bin/env python3
"""
Public Markdown format checker for Scientific Ontology.

Checks:
- Markdown metadata headers against tools/Public_Format_Registry.yml
- README variants: root README, layer README, and subdirectory README
- local Markdown/image link resolution
- forbidden public patterns such as sandbox:/ and /mnt/data
- basic claim-strength / public-profile / language-commensuration consistency
- optional external URL reachability
- optional docs_manifest.yml consistency checks
- optional maintenance_rules.yml terminology and public-boundary drift checks

The checker is intentionally conservative. It reports clear mechanical failures as
ERROR and leaves interpretive issues as WARNING/INFO for human or LLM review.
"""

from __future__ import annotations

import argparse
import dataclasses
import fnmatch
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover - fallback is used when PyYAML is missing
    yaml = None


DEFAULT_FORBIDDEN_PATTERNS = [
    "chatgpt.com/g/",
    "sandbox:/",
    "/mnt/data",
    "10_PUBLIC_GITHUB",
    "file_000000",
    "myfiles_browser",
]

# Generated checker outputs and local-only files must not be treated as public
# Markdown sources. These names are skipped even when they are present at the
# repository root because batch runs may leave them behind.
DEFAULT_EXCLUDED_FILE_NAMES = {
    "public_format_report.md",
    "public_format_report.json",
    "CHECKER_USAGE.md",
    "CHECKER_EXTENSION_REPORT.md",
}

# Pattern exclusions cover Windows/browser duplicate downloads such as
# CHECKER_USAGE(4).md. These are operational checker notes, not public
# Scientific Ontology documents, and should not trigger terminology drift checks.
DEFAULT_EXCLUDED_FILE_PATTERNS = (
    "CHECKER_USAGE*.md",
    "CHECKER_EXTENSION_REPORT*.md",
)

DEFAULT_EXCLUDED_DIR_NAMES = {
    ".git",
    ".github",
    "node_modules",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".checker_reports",
    "checker_reports",
}

DEFAULT_STATUS_VALUES = {
    "readme",
    "introduction",
    "foundation",
    "foundational principle",
    "position",
    "protocol",
    "policy",
    "model",
    "frame",
    "note",
    "research note",
    "research table",
    "application note",
    "application core",
    "cross-domain ontological note",
    "annotation",
    "table",
    "index",
    "registry",
    "glossary",
    "meta",
    "draft",
    "visual note",
    "working note",
    "map",
    "roadmap",
    "citation",
    "license",
    "release notes",
}

ROOT_DOCUMENT_NAMES = {
    "README.md",
    "CITATION.md",
    "CITATION.cff",
    "RELEASE_NOTES.md",
    "Roadmap.md",
    ".zenodo.json",
    "LICENSE.md",
    "GLOSSARY.md",
    "Publication_and_Commensuration_Policy.md",
    "Translation_Note.md",
    "TERM_COLLISION_REGISTRY.md",
    "TERM_COLLISION_REGISTRY.en.md",
}

COMMON_FIXED_NAMES = {
    "Scientific_Terminology_Protocol.md",
    "Publication_and_Commensuration_Policy.md",
    "Translation_Note.md",
    "TERM_COLLISION_REGISTRY.md",
    "TERM_COLLISION_REGISTRY.en.md",
}

LAYER_DIRS = {
    "00_Overview",
    "01_Sat_Truth",
    "02_Raj_Beauty",
    "03_Tam_Goodness",
    "04_Applications",
    "05_Research_Notes",
    "06_Visual_Materials",
    "99_Private_Core_Not_Included",
}

EXTERNAL_DOMAIN_TERMS = [
    "physics",
    "physical",
    "quantum",
    "qft",
    "gravity",
    "relativity",
    "spacetime",
    "cpt",
    "feynman",
    "entropy",
    "negentropy",
    "boson",
    "particle",
    "mass",
    "medical",
    "legal",
    "safety",
    "policy",
    "procurement",
    "audit",
    "implementation",
    "ai",
    "llm",
    "物理",
    "量子",
    "重力",
    "相対論",
    "時空",
    "エントロピー",
    "ネゲントロピー",
    "ボソン",
    "粒子",
    "質量",
    "医療",
    "法務",
    "安全",
    "政策",
    "監査",
    "実装",
]

NON_CLAIM_BOUNDARY_MARKERS = [
    "not replace",
    "does not replace",
    "not a replacement",
    "not proof",
    "not empirical proof",
    "not legal advice",
    "not medical advice",
    "置き換えない",
    "代替ではない",
    "証明ではない",
    "非主張",
    "主張しない",
    "現代科学の代替ではない",
]

DEFAULT_LAYER_README_SECTIONS = [
    "1. Layer Role / 層の位置づけ",
    "2. Public Scope and Claim Profile / 公開範囲と主張強度",
    "3. Included / Not Included / 含むもの・含まないもの",
    "4. Documents / 文書一覧",
    "5. Maintenance Notes / 運用メモ",
]

DEFAULT_SUBDIRECTORY_README_SECTIONS = [
    "1. Directory Role / ディレクトリの位置づけ",
    "2. Public Scope / 公開範囲",
    "3. Documents / 文書一覧",
    "4. Maintenance Notes / 運用メモ",
]

DEFAULT_ROOT_README_SECTIONS = [
    "Public Scope / 公開範囲",
    "Repository Structure / リポジトリ構造",
]

SEVERITIES = {"error", "warning", "info"}


@dataclasses.dataclass(order=True)
class Issue:
    severity: str
    path: str
    line: int
    code: str
    message: str
    suggestion: str = ""

    def as_dict(self) -> Dict[str, Any]:
        return dataclasses.asdict(self)


@dataclasses.dataclass
class CheckResult:
    issues: List[Issue]
    checked_markdown_files: int
    checked_links: int
    external_links_checked: int
    manifest_documents_checked: int = 0
    maintenance_term_hits: int = 0

    @property
    def error_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == "error")

    @property
    def warning_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == "warning")

    @property
    def info_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == "info")


def normalize_severity(value: Any, default: str = "warning") -> str:
    sev = str(value or default).strip().lower()
    return sev if sev in SEVERITIES else default


class Registry:
    def __init__(self, data: Optional[Dict[str, Any]] = None) -> None:
        self.data = data or {}
        fr = self.data.get("format_registry", {}) if isinstance(self.data, dict) else {}
        self.fr = fr
        self.required_header_fields = set(fr.get("header", {}).get("required_fields", ["Status"]))
        aliases = fr.get("header", {}).get("accepted_aliases", {})
        self.accepted_aliases = {str(k): str(v) for k, v in aliases.items()}
        status_core = fr.get("status_values", {}).get("core", [])
        self.status_values = {str(s).strip().lower() for s in status_core} or DEFAULT_STATUS_VALUES
        forbidden = fr.get("ai_final_check", {}).get("forbidden_public_patterns", [])
        self.forbidden_patterns = [str(p) for p in forbidden] or DEFAULT_FORBIDDEN_PATTERNS
        checker_outputs = fr.get("ai_final_check", {}).get("generated_outputs", [])
        self.generated_outputs = {str(p).replace("\\", "/") for p in checker_outputs} or set(DEFAULT_EXCLUDED_FILE_NAMES)
        self.readme_variants = (
            fr.get("document_types", {}).get("readme", {}).get("variants", {})
            if isinstance(fr.get("document_types", {}).get("readme", {}), dict)
            else {}
        )
        fallback_sections = (
            fr.get("document_types", {})
            .get("readme", {})
            .get("body", {})
            .get("required_sections", [])
        )
        self.fallback_readme_required_sections = [str(s) for s in fallback_sections] or DEFAULT_LAYER_README_SECTIONS

    @classmethod
    def load(cls, path: Path, explicit: bool = False) -> Tuple["Registry", List[Issue]]:
        issues: List[Issue] = []
        if not path.exists():
            severity = "warning" if explicit else "info"
            issues.append(
                Issue(
                    severity,
                    relpath(path, path.parent.parent if path.parent.name == "tools" else path.parent),
                    1,
                    "REGISTRY_MISSING",
                    "Registry file not found; using built-in defaults.",
                    "Place Public_Format_Registry.yml at tools/Public_Format_Registry.yml or pass --registry.",
                )
            )
            return cls(None), issues
        if yaml is None:
            issues.append(
                Issue(
                    "warning",
                    str(path),
                    1,
                    "PYYAML_MISSING",
                    "PyYAML is not installed; using built-in defaults instead of reading the registry.",
                    "Install PyYAML, for example: python -m pip install pyyaml",
                )
            )
            return cls(None), issues
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
            return cls(data), issues
        except Exception as exc:
            issues.append(
                Issue(
                    "error",
                    str(path),
                    1,
                    "REGISTRY_PARSE_FAILED",
                    f"Could not parse registry YAML: {exc}",
                    "Fix YAML syntax before running format checks.",
                )
            )
            return cls(None), issues

    def classify_readme(self, relative: str, meta: Dict[str, str]) -> str:
        explicit = meta.get("README type") or meta.get("Readme type") or meta.get("README Type")
        if explicit:
            key = str(explicit).strip().lower().replace(" ", "_").replace("-", "_")
            if key in {"root_readme", "layer_readme", "subdirectory_readme"}:
                return key

        for variant_name, variant in self.readme_variants.items():
            match = variant.get("match", {}) if isinstance(variant, dict) else {}
            exact = match.get("exact_path")
            if exact and relative == str(exact):
                return str(variant_name)
            regex = match.get("path_regex")
            if regex:
                try:
                    if re.search(str(regex), relative):
                        return str(variant_name)
                except re.error:
                    continue

        parts = relative.split("/")
        if relative == "README.md":
            return "root_readme"
        if len(parts) == 2 and parts[0] in LAYER_DIRS and parts[1] == "README.md":
            return "layer_readme"
        if parts[-1] == "README.md":
            return "subdirectory_readme"
        return "readme"

    def readme_required_sections(self, readme_type: str) -> List[str]:
        variant = self.readme_variants.get(readme_type, {}) if isinstance(self.readme_variants, dict) else {}
        sections = []
        if isinstance(variant, dict):
            sections = variant.get("body", {}).get("required_sections", []) or []
        if sections:
            return [str(s) for s in sections]
        if readme_type == "root_readme":
            return DEFAULT_ROOT_README_SECTIONS
        if readme_type == "subdirectory_readme":
            return DEFAULT_SUBDIRECTORY_README_SECTIONS
        return list(self.fallback_readme_required_sections)

    def readme_requires_layer(self, readme_type: str) -> bool:
        if readme_type == "root_readme":
            return False
        variant = self.readme_variants.get(readme_type, {}) if isinstance(self.readme_variants, dict) else {}
        value = None
        if isinstance(variant, dict):
            value = variant.get("header", {}).get("Layer")
        return str(value or "required").lower() == "required"

    def readme_document_list_policy(self, readme_type: str) -> Dict[str, Any]:
        variant = self.readme_variants.get(readme_type, {}) if isinstance(self.readme_variants, dict) else {}
        if isinstance(variant, dict):
            return variant.get("document_list_policy", {}) or {}
        return {}


class Manifest:
    def __init__(self, data: Optional[Dict[str, Any]] = None) -> None:
        self.data = data or {}
        self.manifest = self.data.get("manifest", {}) if isinstance(self.data, dict) else {}
        self.layers = self.data.get("layers", {}) if isinstance(self.data, dict) else {}
        self.documents = self.data.get("documents", []) if isinstance(self.data, dict) else []
        self.coverage = str(self.manifest.get("coverage", "partial-seed"))
        self.required_fields = [str(v) for v in self.manifest.get("required_fields_for_public_documents", [])]
        self.document_type_values = {str(v) for v in self.manifest.get("document_type_values", [])}
        self.state_values = {str(v) for v in self.manifest.get("state_values", [])}
        self.check_rules = self.manifest.get("check_rules", {}) if isinstance(self.manifest, dict) else {}
        self.layer_path_by_key: Dict[str, str] = {}
        if isinstance(self.layers, dict):
            for key, value in self.layers.items():
                if isinstance(value, dict) and value.get("path") is not None:
                    self.layer_path_by_key[str(key)] = str(value.get("path"))

    @classmethod
    def load(cls, path: Path, root: Path, explicit: bool = False) -> Tuple[Optional["Manifest"], List[Issue]]:
        issues: List[Issue] = []
        relative = relpath(path, root)
        if not path.exists():
            if explicit:
                issues.append(
                    Issue(
                        "warning",
                        relative,
                        1,
                        "MANIFEST_MISSING",
                        "docs_manifest.yml was requested but not found.",
                        "Create tools/docs_manifest.yml or omit --manifest.",
                    )
                )
            return None, issues
        if yaml is None:
            issues.append(
                Issue(
                    "warning",
                    relative,
                    1,
                    "PYYAML_MISSING_FOR_MANIFEST",
                    "PyYAML is not installed; manifest checks were skipped.",
                    "Install PyYAML, for example: python -m pip install pyyaml",
                )
            )
            return None, issues
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
            return cls(data), issues
        except Exception as exc:
            issues.append(
                Issue(
                    "error",
                    relative,
                    1,
                    "MANIFEST_PARSE_FAILED",
                    f"Could not parse docs_manifest.yml: {exc}",
                    "Fix YAML syntax before running manifest checks.",
                )
            )
            return None, issues

    def rule_severity(self, rule_name: str, release_gate: bool = False, default: str = "warning") -> str:
        rule = self.check_rules.get(rule_name, {}) if isinstance(self.check_rules, dict) else {}
        key = "release_gate" if release_gate else "normal"
        if isinstance(rule, dict) and key in rule:
            return normalize_severity(rule.get(key), default)
        return normalize_severity(default)

    def layer_to_path(self, layer: str) -> Optional[str]:
        if not layer:
            return None
        if layer in self.layer_path_by_key:
            return self.layer_path_by_key[layer]
        for key, path_value in self.layer_path_by_key.items():
            if layer == path_value:
                return path_value
        return layer if layer == "." or "/" in layer or layer in LAYER_DIRS else None


class MaintenanceRules:
    def __init__(self, data: Optional[Dict[str, Any]] = None) -> None:
        self.data = data or {}
        self.root = self.data.get("maintenance_rules", {}) if isinstance(self.data, dict) else {}
        tr = self.root.get("term_rules", {}) if isinstance(self.root, dict) else {}
        self.replacements = tr.get("replacements", []) if isinstance(tr, dict) else []
        self.caution_terms = tr.get("caution_terms", []) if isinstance(tr, dict) else []
        self.term_exceptions = tr.get("exceptions", []) if isinstance(tr, dict) else []
        self.profile_rules = self.root.get("profile_rules", {}) if isinstance(self.root, dict) else {}
        pbr = self.root.get("public_boundary_rules", {}) if isinstance(self.root, dict) else {}
        self.boundary_forbidden_patterns = pbr.get("forbidden_public_patterns", []) if isinstance(pbr, dict) else []
        self.private_core_terms = pbr.get("private_core_terms", []) if isinstance(pbr, dict) else []

    @classmethod
    def load(cls, path: Path, root: Path, explicit: bool = False) -> Tuple[Optional["MaintenanceRules"], List[Issue]]:
        issues: List[Issue] = []
        relative = relpath(path, root)
        if not path.exists():
            if explicit:
                issues.append(
                    Issue(
                        "warning",
                        relative,
                        1,
                        "MAINTENANCE_RULES_MISSING",
                        "maintenance_rules.yml was requested but not found.",
                        "Create tools/maintenance_rules.yml or omit --maintenance-rules.",
                    )
                )
            return None, issues
        if yaml is None:
            issues.append(
                Issue(
                    "warning",
                    relative,
                    1,
                    "PYYAML_MISSING_FOR_MAINTENANCE_RULES",
                    "PyYAML is not installed; maintenance rules checks were skipped.",
                    "Install PyYAML, for example: python -m pip install pyyaml",
                )
            )
            return None, issues
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
            return cls(data), issues
        except Exception as exc:
            issues.append(
                Issue(
                    "error",
                    relative,
                    1,
                    "MAINTENANCE_RULES_PARSE_FAILED",
                    f"Could not parse maintenance_rules.yml: {exc}",
                    "Fix YAML syntax before running maintenance checks.",
                )
            )
            return None, issues


def relpath(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def normalize_rel(value: str) -> str:
    return str(value).replace("\\", "/").lstrip("./")


def build_excluded_paths(root: Path, registry: Registry, args: argparse.Namespace) -> set[str]:
    excluded = {normalize_rel(p) for p in getattr(registry, "generated_outputs", set())}
    for value in args.exclude_path or []:
        excluded.add(normalize_rel(value))
    for value in [args.md_log, args.json_log]:
        if value:
            try:
                excluded.add(Path(value).resolve().relative_to(root).as_posix())
            except ValueError:
                excluded.add(normalize_rel(value))
    return excluded


def is_excluded_path(path: Path, root: Path, excluded_paths: set[str]) -> bool:
    try:
        rel = path.relative_to(root).as_posix()
    except ValueError:
        return True
    parts = set(path.relative_to(root).parts)
    if parts & DEFAULT_EXCLUDED_DIR_NAMES:
        return True
    if path.name in DEFAULT_EXCLUDED_FILE_NAMES:
        return True
    if any(fnmatch.fnmatch(path.name, pattern) for pattern in DEFAULT_EXCLUDED_FILE_PATTERNS):
        return True
    if rel in excluded_paths:
        return True
    for item in excluded_paths:
        if item.endswith("/") and rel.startswith(item):
            return True
    return False


def iter_markdown_files(
    root: Path,
    include_private_marker: bool = True,
    excluded_paths: Optional[set[str]] = None,
) -> Iterable[Path]:
    excluded_paths = excluded_paths or set()
    for path in root.rglob("*.md"):
        try:
            rel_parts = set(path.relative_to(root).parts)
        except ValueError:
            continue
        if rel_parts & DEFAULT_EXCLUDED_DIR_NAMES:
            continue
        if is_excluded_path(path, root, excluded_paths):
            continue
        if not include_private_marker and "99_Private_Core_Not_Included" in rel_parts:
            continue
        yield path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def line_number_for_offset(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def parse_metadata_header(text: str) -> Tuple[Dict[str, str], Dict[str, int], int]:
    """Parse blockquote metadata in the first visible block.

    The registry says metadata is at the top. Existing public drafts often use a
    title first, then blockquote metadata. This parser accepts both patterns when
    they occur in the first 25 physical lines.
    """
    meta: Dict[str, str] = {}
    lines_by_key: Dict[str, int] = {}
    lines = text.splitlines()
    header_start = -1
    max_scan = min(25, len(lines))
    for idx in range(max_scan):
        line = lines[idx]
        if re.match(r"^>\s*[^:]+:\s*.+", line):
            header_start = idx
            break
        if line.strip() and not line.startswith("#") and not line.startswith("---"):
            continue
    if header_start == -1:
        return meta, lines_by_key, 0
    for idx in range(header_start, len(lines)):
        line = lines[idx]
        if not line.startswith(">"):
            if line.strip() == "":
                continue
            break
        m = re.match(r"^>\s*([^:]+):\s*(.*?)\s*$", line)
        if not m:
            continue
        key = m.group(1).strip()
        value = m.group(2).strip()
        meta[key] = value
        lines_by_key[key] = idx + 1
    return meta, lines_by_key, header_start + 1


def normalize_metadata(meta: Dict[str, str], registry: Registry) -> Dict[str, str]:
    normalized: Dict[str, str] = {}
    for key, value in meta.items():
        canonical = registry.accepted_aliases.get(key, key)
        normalized[canonical] = value
    return normalized


def classify_document(path: Path, root: Path, registry: Registry, meta: Optional[Dict[str, str]] = None) -> str:
    relative = relpath(path, root)
    meta = meta or {}
    status = str(meta.get("Status", "")).strip().lower()
    if path.name == "README.md":
        return registry.classify_readme(relative, meta)
    if path.parent == root and path.name in ROOT_DOCUMENT_NAMES:
        return "root_document"
    if path.name in COMMON_FIXED_NAMES:
        return "common_fixed_explanation"
    if status in {
        "registry",
        "glossary",
        "table",
        "research table",
        "index",
        "map",
        "roadmap",
        "citation",
        "license",
        "release notes",
        "policy",
        "protocol",
        "working note",
        "meta",
    }:
        return "common_fixed_explanation"
    if status in {"application note", "application core"}:
        return "application_note"
    if status == "research note" or (path.suffix.lower() == ".md" and "Research_Notes" in path.parts):
        return "research_note"
    return "assertion_document"


def status_is_accepted(status: str, accepted: set[str]) -> bool:
    value = status.strip().lower()
    if value in accepted:
        return True
    tokens = set(re.split(r"[\s/_-]+", value))
    for accepted_value in accepted:
        accepted_tokens = set(re.split(r"[\s/_-]+", accepted_value))
        if accepted_tokens and accepted_tokens <= tokens:
            return True
    return False


def has_english_rendering(text: str) -> bool:
    markers = [
        "English commensurated rendering",
        "English Commensurated Version",
        "English rendering",
        "English version",
        "# English",
        "## English",
    ]
    return any(marker.lower() in text.lower() for marker in markers)


def has_non_claim_boundary(text: str) -> bool:
    lower = text.lower()
    return any(marker.lower() in lower for marker in NON_CLAIM_BOUNDARY_MARKERS)


def contains_external_domain_claim_terms(text: str) -> bool:
    lower = text.lower()
    return any(term.lower() in lower for term in EXTERNAL_DOMAIN_TERMS)


def strip_code_fences(text: str) -> str:
    return re.sub(r"```.*?```", "", text, flags=re.DOTALL)


def extract_markdown_links(text: str) -> List[Tuple[str, int, bool]]:
    """Return (target, line, is_image)."""
    links: List[Tuple[str, int, bool]] = []
    visible_text = strip_code_fences(text)

    inline_pattern = re.compile(r"(!?)\[[^\]\n]*\]\(([^)\n]+)\)")
    for match in inline_pattern.finditer(visible_text):
        is_image = bool(match.group(1))
        raw = match.group(2).strip()
        if raw.startswith("<") and raw.endswith(">"):
            raw = raw[1:-1]
        if " " in raw and not raw.startswith(("http://", "https://")):
            raw = raw.split(" ", 1)[0]
        links.append((raw, line_number_for_offset(visible_text, match.start(2)), is_image))

    ref_pattern = re.compile(r"^\s{0,3}\[[^\]]+\]:\s+(\S+)", re.MULTILINE)
    for match in ref_pattern.finditer(visible_text):
        links.append((match.group(1).strip(), line_number_for_offset(visible_text, match.start(1)), False))
    return links


def is_external_url(target: str) -> bool:
    parsed = urllib.parse.urlparse(target)
    return parsed.scheme in {"http", "https"}


def is_ignored_link_scheme(target: str) -> bool:
    parsed = urllib.parse.urlparse(target)
    return parsed.scheme in {"mailto", "tel"}


def resolve_local_link(source: Path, target: str) -> Optional[Path]:
    if not target or target.startswith("#"):
        return None
    if is_external_url(target) or is_ignored_link_scheme(target):
        return None
    parsed = urllib.parse.urlparse(target)
    if parsed.scheme:
        return None
    unquoted = urllib.parse.unquote(parsed.path)
    if not unquoted:
        return None
    return (source.parent / unquoted).resolve()

def resolve_link_path_and_fragment(source: Path, target: str) -> Tuple[Optional[Path], str]:
    if not target:
        return None, ""
    if is_external_url(target) or is_ignored_link_scheme(target):
        return None, ""
    parsed = urllib.parse.urlparse(target)
    if parsed.scheme:
        return None, ""
    fragment = urllib.parse.unquote(parsed.fragment or "")
    unquoted_path = urllib.parse.unquote(parsed.path or "")
    if not unquoted_path:
        return source.resolve(), fragment
    return (source.parent / unquoted_path).resolve(), fragment


def github_slugify_heading(heading: str) -> str:
    # Approximate GitHub Markdown heading anchors. This intentionally keeps
    # Japanese and other Unicode word characters, removes most punctuation,
    # lowercases ASCII, converts whitespace to hyphens, and collapses hyphens.
    value = heading.strip().lower()
    value = re.sub(r"`([^`]*)`", r"\1", value)
    value = re.sub(r"<[^>]+>", "", value)
    value = re.sub(r"[^\w\s\-　-鿿぀-ヿ＀-￯]", "", value, flags=re.UNICODE)
    value = re.sub(r"[\s　]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value


def markdown_heading_anchors(text: str) -> set[str]:
    anchors: set[str] = set()
    counts: Dict[str, int] = {}
    for line in strip_code_fences(text).splitlines():
        m = re.match(r"^\s{0,3}(#{1,6})\s+(.+?)\s*#*\s*$", line)
        if not m:
            continue
        raw = m.group(2).strip()
        slug = github_slugify_heading(raw)
        if not slug:
            continue
        count = counts.get(slug, 0)
        counts[slug] = count + 1
        anchors.add(slug if count == 0 else f"{slug}-{count}")
    return anchors


def anchor_target_ok(target_file: Path, fragment: str, cache: Dict[Path, set[str]]) -> bool:
    if not fragment:
        return True
    normalized = fragment.lstrip("#").strip()
    if not normalized:
        return True
    # GitHub supports some user-content- prefixed anchors in rendered HTML.
    alternatives = {normalized, normalized.lower()}
    if normalized.startswith("user-content-"):
        alternatives.add(normalized[len("user-content-"):])
    if target_file.suffix.lower() not in {".md", ".markdown"}:
        return True
    if target_file not in cache:
        try:
            cache[target_file] = markdown_heading_anchors(read_text(target_file))
        except Exception:
            cache[target_file] = set()
    anchors = cache[target_file]
    return any(alt in anchors for alt in alternatives)


def external_url_ok(url: str, timeout: float) -> Tuple[bool, str]:
    try:
        req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "public-format-checker/0.2"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            code = getattr(resp, "status", 200)
            if 200 <= code < 400:
                return True, f"HTTP {code}"
            return False, f"HTTP {code}"
    except Exception as head_exc:
        try:
            req = urllib.request.Request(url, method="GET", headers={"User-Agent": "public-format-checker/0.2"})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                code = getattr(resp, "status", 200)
                if 200 <= code < 400:
                    return True, f"HTTP {code} after GET fallback"
                return False, f"HTTP {code} after GET fallback"
        except Exception as get_exc:
            return False, f"HEAD failed: {head_exc}; GET failed: {get_exc}"


def has_marker_near(text: str, idx: int, markers: Sequence[str], window: int) -> bool:
    if not markers:
        return False
    start = max(0, idx - window)
    end = min(len(text), idx + window)
    context = text[start:end].lower()
    return any(str(marker).lower() in context for marker in markers)


def find_term_occurrences(text: str, term: str, match_case: bool = False) -> Iterable[int]:
    if not term:
        return []
    haystack = text if match_case else text.lower()
    needle = term if match_case else term.lower()
    positions: List[int] = []
    start = 0
    while True:
        idx = haystack.find(needle, start)
        if idx < 0:
            break
        positions.append(idx)
        start = idx + max(len(needle), 1)
    return positions


def path_matches_any(relative: str, patterns: Sequence[str]) -> bool:
    if not patterns:
        return True
    normalized = normalize_rel(relative)
    return any(fnmatch.fnmatch(normalized, normalize_rel(str(pattern))) for pattern in patterns)


def regex_context_matches(text: str, idx: int, patterns: Sequence[str], window: int) -> bool:
    if not patterns:
        return False
    start = max(0, idx - window)
    end = min(len(text), idx + window)
    context = text[start:end]
    for pattern in patterns:
        try:
            if re.search(str(pattern), context, flags=re.IGNORECASE | re.DOTALL):
                return True
        except re.error:
            # Invalid exception regexes should not crash the checker. They are
            # reported by YAML review/manual review rather than treated as matches.
            continue
    return False


def term_exception_applies(
    rules: MaintenanceRules,
    relative: str,
    term: str,
    text: str,
    idx: int,
    default_window: int,
) -> Tuple[bool, bool, str]:
    """Return (is_allowed, should_report, reason) for term exception registry.

    Exceptions are intentionally data-driven. They are for cases where a
    deprecated term appears as a prohibited rendering, former-name note,
    translation warning, or checker documentation example. Such occurrences
    should not be treated as public terminology drift.
    """
    for item in getattr(rules, "term_exceptions", []) or []:
        if not isinstance(item, dict):
            continue
        item_term = str(item.get("term", ""))
        if item_term and item_term.lower() != term.lower():
            continue
        paths = [str(v) for v in item.get("paths", []) or []]
        if paths and not path_matches_any(relative, paths):
            continue
        window = int(item.get("context_window", default_window) or default_window)
        markers = [str(v) for v in item.get("allowed_near", []) or []]
        patterns = [str(v) for v in item.get("allowed_patterns", []) or []]
        marker_ok = bool(markers and has_marker_near(text, idx, markers, window))
        pattern_ok = bool(patterns and regex_context_matches(text, idx, patterns, window))
        if marker_ok or pattern_ok:
            report = bool(item.get("report", False))
            return True, report, str(item.get("reason", "Allowed by maintenance exception registry."))
    return False, False, ""


def check_maintenance_for_file(
    path: Path,
    root: Path,
    text: str,
    meta: Dict[str, str],
    doc_type: str,
    rules: Optional[MaintenanceRules],
    registry: Registry,
    args: argparse.Namespace,
) -> Tuple[List[Issue], int]:
    issues: List[Issue] = []
    hits = 0
    if rules is None:
        return issues, hits
    relative = relpath(path, root)
    visible_text = strip_code_fences(text)

    for item in rules.replacements:
        if not isinstance(item, dict):
            continue
        source = str(item.get("from", ""))
        replacement = str(item.get("use", ""))
        severity = normalize_severity(item.get("severity"), "warning")
        match_case = bool(item.get("match_case", False))
        allowed_near = [str(v) for v in item.get("allowed_near", []) or []]
        allowed_patterns = [str(v) for v in item.get("allowed_patterns", []) or []]
        report_allowed = bool(item.get("report_allowed", False))
        for idx in find_term_occurrences(visible_text, source, match_case=match_case):
            hits += 1
            allowed_by_exception, exception_report, exception_reason = term_exception_applies(
                rules, relative, source, visible_text, idx, args.term_context_window
            )
            allowed_by_rule = False
            if allowed_near and has_marker_near(visible_text, idx, allowed_near, args.term_context_window):
                allowed_by_rule = True
            if allowed_patterns and regex_context_matches(visible_text, idx, allowed_patterns, args.term_context_window):
                allowed_by_rule = True
            if allowed_by_exception or allowed_by_rule:
                if report_allowed or exception_report:
                    issues.append(
                        Issue(
                            "info",
                            relative,
                            line_number_for_offset(visible_text, idx),
                            "TERM_LEGACY_ALLOWED_BY_CONTEXT",
                            f"Legacy or deprecated term appears in an allowed context: {source}",
                            exception_reason or f"Confirm the context is really a former-name or exception note. Preferred term: {replacement}",
                        )
                    )
                continue
            issues.append(
                Issue(
                    severity,
                    relative,
                    line_number_for_offset(visible_text, idx),
                    "TERM_REPLACEMENT_REQUIRED",
                    f"Term drift detected: '{source}' should use '{replacement}'.",
                    str(item.get("reason", "Replace the term or add an allowed-context note.")),
                )
            )

    skip_caution_terms = doc_type in {"common_fixed_explanation", "root_document"} or relative.startswith("tools/")
    for item in rules.caution_terms:
        if skip_caution_terms:
            break
        if not isinstance(item, dict):
            continue
        term = str(item.get("term", ""))
        severity = normalize_severity(item.get("severity"), "warning")
        markers = [str(v) for v in item.get("expected_boundary_markers", []) or []]
        positions = list(find_term_occurrences(visible_text, term, match_case=False))
        if not positions:
            continue
        hits += len(positions)
        lower_text = visible_text.lower()
        has_doc_marker = any(marker.lower() in lower_text for marker in markers)
        if not markers or has_doc_marker:
            continue
        first = positions[0]
        issues.append(
            Issue(
                severity,
                relative,
                line_number_for_offset(visible_text, first),
                "CAUTION_TERM_BOUNDARY_MISSING",
                f"Caution term appears without expected boundary markers: {term}",
                str(item.get("note", "Add a boundary note or define the term usage.")),
            )
        )

    # Additional forbidden public patterns not already covered by registry.
    registry_patterns = set(registry.forbidden_patterns)
    for item in rules.boundary_forbidden_patterns:
        if not isinstance(item, dict):
            continue
        pattern = str(item.get("pattern", ""))
        if not pattern or pattern in registry_patterns:
            continue
        severity = normalize_severity(item.get("severity"), "error")
        start = 0
        while True:
            idx = visible_text.find(pattern, start)
            if idx < 0:
                break
            hits += 1
            issues.append(
                Issue(
                    severity,
                    relative,
                    line_number_for_offset(visible_text, idx),
                    "MAINTENANCE_FORBIDDEN_PUBLIC_PATTERN",
                    f"Forbidden public pattern from maintenance_rules.yml found: {pattern}",
                    "Remove public references to local paths, sandbox links, ChatGPT file IDs, or private workspace names.",
                )
            )
            start = idx + max(len(pattern), 1)

    for item in rules.private_core_terms:
        if not isinstance(item, dict):
            continue
        term = str(item.get("term", ""))
        if not term:
            continue
        positions = list(find_term_occurrences(visible_text, term, match_case=False))
        if not positions:
            continue
        hits += len(positions)
        handling = str(item.get("public_handling", "do not expose"))
        allowed_markers = [
            "not included",
            "does not include",
            "excluded",
            "do not include",
            "not expose",
            "non-public",
            "private core",
            "非公開",
            "含めない",
            "除外",
            "公開しない",
        ]
        for idx in positions[:3]:
            if "excluded" in handling or "marker" in handling:
                if has_marker_near(visible_text, idx, allowed_markers, args.term_context_window):
                    continue
            issues.append(
                Issue(
                    "warning",
                    relative,
                    line_number_for_offset(visible_text, idx),
                    "PRIVATE_CORE_TERM_REVIEW",
                    f"Private-core term appears in public Markdown: {term}",
                    f"Public handling rule: {handling}. Confirm this is only an exclusion marker or abstracted public boundary note.",
                )
            )

    # Profile-label drift checks.
    forbidden_profile_patterns = rules.profile_rules.get("forbidden_patterns", []) if isinstance(rules.profile_rules, dict) else []
    for item in forbidden_profile_patterns:
        if not isinstance(item, dict):
            continue
        pattern = str(item.get("pattern", ""))
        if not pattern:
            continue
        idx = visible_text.find(pattern)
        if idx >= 0:
            hits += 1
            issues.append(
                Issue(
                    normalize_severity(item.get("severity"), "warning"),
                    relative,
                    line_number_for_offset(visible_text, idx),
                    "PROFILE_LABEL_DRIFT",
                    f"Profile-label drift pattern detected: {pattern}",
                    str(item.get("reason", "Use the canonical metadata label for this document type.")),
                )
            )

    if doc_type in {"root_readme", "layer_readme", "subdirectory_readme"}:
        if "Claim strength" in meta and "Public profile" not in meta:
            issues.append(
                Issue(
                    "info",
                    relative,
                    1,
                    "README_CLAIM_STRENGTH_USED_WITHOUT_PUBLIC_PROFILE",
                    "README uses Claim strength without Public profile.",
                    "Prefer '> Public profile: Px' for README files; keep Claim strength for individual assertion documents.",
                )
            )
    elif doc_type in {"assertion_document", "research_note", "application_note"}:
        if "Public profile" in meta and "Claim strength" not in meta and contains_external_domain_claim_terms(text):
            issues.append(
                Issue(
                    "warning",
                    relative,
                    1,
                    "ASSERTION_PUBLIC_PROFILE_WITHOUT_CLAIM_STRENGTH",
                    "Assertion-like document uses Public profile but lacks Claim strength despite external-domain terms.",
                    "Add '> Claim strength: Sx/Ex/Ux' when the document makes substantive claims.",
                )
            )

    return issues, hits


def check_file(
    path: Path,
    root: Path,
    registry: Registry,
    maintenance_rules: Optional[MaintenanceRules],
    args: argparse.Namespace,
) -> Tuple[List[Issue], int, int, int, Dict[str, Any]]:
    issues: List[Issue] = []
    text = read_text(path)
    relative = relpath(path, root)
    meta_raw, meta_lines, header_start_line = parse_metadata_header(text)
    meta = normalize_metadata(meta_raw, registry)
    doc_type = classify_document(path, root, registry, meta)
    checked_links = 0
    external_checked = 0
    maintenance_hits = 0

    if not meta:
        issues.append(
            Issue(
                "error",
                relative,
                1,
                "HEADER_MISSING",
                "Markdown metadata header was not found near the top of the file.",
                "Add blockquote metadata such as '> Status: Note' near the title.",
            )
        )
    else:
        if header_start_line > 3:
            issues.append(
                Issue(
                    "info",
                    relative,
                    header_start_line,
                    "HEADER_POSITION",
                    "Metadata header is not immediately at the top; accepted, but consider keeping it directly under the title.",
                    "Keep '# Title' followed by '> Status: ...' for consistent public documents.",
                )
            )
        for required in registry.required_header_fields:
            if required not in meta:
                issues.append(
                    Issue(
                        "error",
                        relative,
                        1,
                        f"HEADER_FIELD_MISSING_{required.upper().replace(' ', '_')}",
                        f"Required metadata field '{required}' is missing.",
                        f"Add '> {required}: <document role>'.",
                    )
                )
        status = meta.get("Status")
        if status and not status_is_accepted(status, registry.status_values):
            line = meta_lines.get("Status", 1)
            issues.append(
                Issue(
                    "warning",
                    relative,
                    line,
                    "STATUS_VALUE_UNREGISTERED",
                    f"Status value '{status}' is not registered in Public_Format_Registry.yml.",
                    "Either use a registered Status value or add this role to the registry.",
                )
            )

    if doc_type in {"root_readme", "layer_readme", "subdirectory_readme", "readme"}:
        if registry.readme_requires_layer(doc_type) and "Layer" not in meta:
            issues.append(
                Issue(
                    "error",
                    relative,
                    1,
                    "README_LAYER_MISSING",
                    f"{doc_type} files require a Layer metadata field.",
                    "Add '> Layer: <directory layer name>'.",
                )
            )
        for section in registry.readme_required_sections(doc_type):
            if section not in text:
                issues.append(
                    Issue(
                        "warning",
                        relative,
                        1,
                        "README_SECTION_MISSING",
                        f"{doc_type} does not contain required section: {section}",
                        "Add the missing section or document why this README is an exception.",
                    )
                )
        policy = registry.readme_document_list_policy(doc_type)
        require_all = bool(policy.get("require_all_same_directory_files", doc_type in {"layer_readme", "subdirectory_readme", "readme"}))
        if require_all:
            siblings = sorted(p.name for p in path.parent.glob("*.md") if p.name != "README.md")
            for sibling in siblings:
                if sibling not in text:
                    issues.append(
                        Issue(
                            "warning",
                            relative,
                            1,
                            "README_DOCUMENT_LIST_STALE",
                            f"README may omit Markdown file in same directory: {sibling}",
                            "Add it to 'Documents / 文書一覧' or mark it as intentionally excluded.",
                        )
                    )

    language = meta.get("Language", "")
    language_lower = language.lower()
    if language_lower in {"ja+en", "japanese authoritative; english commensurated rendering included"}:
        if not has_english_rendering(text):
            issues.append(
                Issue(
                    "warning",
                    relative,
                    meta_lines.get("Language", 1),
                    "ENGLISH_RENDERING_NOT_DETECTED",
                    "Language metadata indicates ja+en, but an English rendering section was not detected.",
                    "Add 'English commensurated rendering' or adjust the Language metadata.",
                )
            )
    if "japanese only" in language_lower and "pending" not in language_lower:
        issues.append(
            Issue(
                "info",
                relative,
                meta_lines.get("Language", 1),
                "JAPANESE_ONLY_WITHOUT_PENDING_MARKER",
                "Japanese-only language metadata is present without an explicit commensuration-pending marker.",
                "Use 'Japanese only; English commensuration pending' if this is temporary.",
            )
        )

    external_terms = contains_external_domain_claim_terms(text)
    if external_terms:
        if doc_type in {"assertion_document", "research_note", "application_note"}:
            if "Claim strength" not in meta:
                issues.append(
                    Issue(
                        "warning",
                        relative,
                        1,
                        "CLAIM_STRENGTH_SUGGESTED",
                        "External-domain or application-facing terms were detected, but Claim strength metadata is absent.",
                        "Add '> Claim strength: Sx/Ex/Ux'. Use '> Public profile: Px' for directory navigation, not detailed claim classification.",
                    )
                )
        elif doc_type in {"layer_readme", "subdirectory_readme"}:
            if "Public profile" not in meta and "Claim strength" not in meta:
                issues.append(
                    Issue(
                        "warning",
                        relative,
                        1,
                        "PUBLIC_PROFILE_SUGGESTED",
                        "External-domain or application-facing terms were detected in a README, but Public profile metadata is absent.",
                        "Add '> Public profile: Px' or use a justified exception note.",
                    )
                )
        if doc_type not in {"root_readme", "root_document"} and not has_non_claim_boundary(text):
            issues.append(
                Issue(
                    "warning",
                    relative,
                    1,
                    "NON_CLAIM_BOUNDARY_SUGGESTED",
                    "External-domain terms were detected without an obvious non-claim boundary statement.",
                    "Add a sentence such as 'This is not a replacement for standard science' where applicable.",
                )
            )

    for pattern in registry.forbidden_patterns:
        start = 0
        while True:
            idx = text.find(pattern, start)
            if idx < 0:
                break
            issues.append(
                Issue(
                    "error",
                    relative,
                    line_number_for_offset(text, idx),
                    "FORBIDDEN_PUBLIC_PATTERN",
                    f"Forbidden public pattern found: {pattern}",
                    "Remove public references to local paths, sandbox links, ChatGPT file IDs, or private workspace names.",
                )
            )
            start = idx + max(len(pattern), 1)

    maint_issues, maintenance_hits = check_maintenance_for_file(path, root, text, meta, doc_type, maintenance_rules, registry, args)
    issues.extend(maint_issues)

    anchor_cache: Dict[Path, set[str]] = {}
    for target, line, is_image in extract_markdown_links(text):
        checked_links += 1
        if is_external_url(target):
            if args.check_external:
                external_checked += 1
                ok, detail = external_url_ok(target, args.external_timeout)
                if not ok:
                    issues.append(
                        Issue(
                            "warning",
                            relative,
                            line,
                            "EXTERNAL_LINK_UNREACHABLE",
                            f"External URL could not be reached: {target} ({detail})",
                            "Verify the URL or run again later if the target is temporarily unavailable.",
                        )
                    )
            continue
        local, fragment = resolve_link_path_and_fragment(path, target)
        if local is None:
            continue
        if not local.exists():
            code = "BROKEN_LOCAL_IMAGE" if is_image else "BROKEN_LOCAL_LINK"
            issues.append(
                Issue(
                    "error",
                    relative,
                    line,
                    code,
                    f"Local {'image' if is_image else 'link'} target does not exist: {target}",
                    "Fix the relative path, move the target file, or remove the stale link.",
                )
            )
            continue
        if args.check_anchors and fragment and not anchor_target_ok(local, fragment, anchor_cache):
            issues.append(
                Issue(
                    "warning",
                    relative,
                    line,
                    "BROKEN_MARKDOWN_ANCHOR",
                    f"Markdown anchor was not found in target: {target}",
                    "Check the heading text, GitHub-generated anchor slug, or remove the stale fragment.",
                )
            )

    file_info = {
        "relative": relative,
        "meta": meta,
        "doc_type": doc_type,
        "path": path,
        "text": text,
    }
    return issues, checked_links, external_checked, maintenance_hits, file_info


def check_release_metadata(root: Path, excluded_paths: Optional[set[str]] = None) -> List[Issue]:
    issues: List[Issue] = []
    excluded_paths = excluded_paths or set()
    root_files = [
        p
        for p in root.glob("*")
        if p.is_file()
        and p.suffix.lower() in {".md", ".cff", ".json"}
        and not is_excluded_path(p, root, excluded_paths)
    ]
    doi_map: Dict[str, List[str]] = {}
    version_map: Dict[str, List[str]] = {}
    doi_pattern = re.compile(r"10\.5281/zenodo\.\d+")
    version_pattern = re.compile(r"\bv\d+\.\d+\.\d+\b")
    for path in root_files:
        text = read_text(path)
        for doi in sorted(set(doi_pattern.findall(text))):
            doi_map.setdefault(doi, []).append(path.name)
        for version in sorted(set(version_pattern.findall(text))):
            version_map.setdefault(version, []).append(path.name)
    if len(version_map) > 1:
        issues.append(
            Issue(
                "info",
                ".",
                1,
                "MULTIPLE_VERSION_STRINGS_FOUND",
                "Multiple semantic version strings were found in root metadata files.",
                "Review release metadata manually; multiple versions can be legitimate in release history.",
            )
        )
    if len(doi_map) > 2:
        issues.append(
            Issue(
                "info",
                ".",
                1,
                "MULTIPLE_DOI_STRINGS_FOUND",
                "Several Zenodo DOI strings were found in root metadata files.",
                "Confirm whether they represent version DOI, concept DOI, and older release references.",
            )
        )
    return issues


def manifest_doc_path(doc: Dict[str, Any]) -> str:
    return str(doc.get("path", "")).strip()


def check_manifest(
    root: Path,
    manifest: Optional[Manifest],
    registry: Registry,
    file_index: Dict[str, Dict[str, Any]],
    args: argparse.Namespace,
) -> Tuple[List[Issue], int]:
    issues: List[Issue] = []
    if manifest is None:
        return issues, 0
    docs_checked = 0
    listed_paths: set[str] = set()
    release_gate = bool(args.release_gate)

    for raw_doc in manifest.documents:
        if not isinstance(raw_doc, dict):
            issues.append(
                Issue(
                    "warning",
                    "tools/docs_manifest.yml",
                    1,
                    "MANIFEST_DOCUMENT_ENTRY_INVALID",
                    "Manifest document entry is not a mapping.",
                    "Each document entry should be a YAML mapping with at least path, document_type, status, and state.",
                )
            )
            continue
        docs_checked += 1
        path_value = manifest_doc_path(raw_doc)
        line = 1
        if not path_value:
            issues.append(
                Issue(
                    "error",
                    "tools/docs_manifest.yml",
                    line,
                    "MANIFEST_DOCUMENT_PATH_MISSING",
                    "Manifest document entry is missing path.",
                    "Add path: <relative/public/path>.",
                )
            )
            continue
        listed_paths.add(path_value)
        state = str(raw_doc.get("state", "")).strip()
        doc_type = str(raw_doc.get("document_type", "")).strip()
        status = str(raw_doc.get("status", "")).strip()
        layer = str(raw_doc.get("layer", "")).strip()
        public_profile = str(raw_doc.get("public_profile", "")).strip()

        for field in manifest.required_fields:
            if field not in raw_doc or raw_doc.get(field) in {None, ""}:
                issues.append(
                    Issue(
                        "warning",
                        path_value,
                        line,
                        "MANIFEST_REQUIRED_FIELD_MISSING",
                        f"Manifest entry for {path_value} lacks required field: {field}",
                        "Complete the manifest entry or reduce manifest strictness while still in seed mode.",
                    )
                )
        if manifest.document_type_values and doc_type and doc_type not in manifest.document_type_values:
            issues.append(
                Issue(
                    "warning",
                    path_value,
                    line,
                    "MANIFEST_DOCUMENT_TYPE_UNREGISTERED",
                    f"Manifest document_type is not registered: {doc_type}",
                    "Use a registered document_type value or add it to docs_manifest.yml.",
                )
            )
        if manifest.state_values and state and state not in manifest.state_values:
            issues.append(
                Issue(
                    "warning",
                    path_value,
                    line,
                    "MANIFEST_STATE_UNREGISTERED",
                    f"Manifest state is not registered: {state}",
                    "Use public, public-candidate, planned, legacy, or deprecated unless the manifest defines another state.",
                )
            )
        if status and not status_is_accepted(status, registry.status_values):
            issues.append(
                Issue(
                    manifest.rule_severity("status_not_registered", release_gate, "warning"),
                    path_value,
                    line,
                    "MANIFEST_STATUS_NOT_REGISTERED",
                    f"Manifest status is not registered in Public_Format_Registry.yml: {status}",
                    "Add the status to Public_Format_Registry.yml or correct the manifest entry.",
                )
            )

        repo_path = root / path_value
        exists = repo_path.exists()
        if not exists:
            if state == "planned":
                issues.append(
                    Issue(
                        "info",
                        path_value,
                        line,
                        "MANIFEST_PLANNED_PATH_NOT_CREATED",
                        "Manifest path is planned and does not yet exist.",
                        "No action needed unless this document should already be public.",
                    )
                )
            else:
                issues.append(
                    Issue(
                        manifest.rule_severity("manifest_path_missing", release_gate, "warning"),
                        path_value,
                        line,
                        "MANIFEST_PATH_MISSING",
                        "Manifest lists a document path that does not exist in the repository.",
                        "Create the file, correct the path, or mark the entry as state: planned.",
                    )
                )
            continue

        file_info = file_index.get(path_value)
        if file_info:
            meta = file_info.get("meta", {})
            actual_doc_type = file_info.get("doc_type", "")
            if doc_type and actual_doc_type and doc_type != actual_doc_type:
                compatible = False
                if doc_type == "assertion_document" and actual_doc_type == "research_note":
                    compatible = True
                if not compatible:
                    issues.append(
                        Issue(
                            "warning",
                            path_value,
                            line,
                            "MANIFEST_DOCUMENT_TYPE_MISMATCH",
                            f"Manifest document_type '{doc_type}' differs from checker classification '{actual_doc_type}'.",
                            "Adjust docs_manifest.yml or add an explicit README type/document type exception if this is intentional.",
                        )
                    )
            if status and meta.get("Status") and status.strip().lower() != str(meta.get("Status")).strip().lower():
                issues.append(
                    Issue(
                        "warning",
                        path_value,
                        line,
                        "MANIFEST_STATUS_HEADER_MISMATCH",
                        f"Manifest status '{status}' differs from file header Status '{meta.get('Status')}'.",
                        "Synchronize the manifest and document header.",
                    )
                )
            header_profile = meta.get("Public profile") or meta.get("Claim profile")
            if public_profile and header_profile and public_profile != header_profile:
                issues.append(
                    Issue(
                        manifest.rule_severity("profile_mismatch", release_gate, "warning"),
                        path_value,
                        line,
                        "MANIFEST_PUBLIC_PROFILE_MISMATCH",
                        f"Manifest public_profile '{public_profile}' differs from file header profile '{header_profile}'.",
                        "Synchronize Public profile or document why the manifest uses a directory-level profile.",
                    )
                )
            if layer and meta.get("Layer"):
                meta_layer = str(meta.get("Layer"))
                layer_path = manifest.layer_to_path(layer) or layer
                if meta_layer != layer and meta_layer != layer_path:
                    issues.append(
                        Issue(
                            "info",
                            path_value,
                            line,
                            "MANIFEST_LAYER_HEADER_DIFFERS",
                            f"Manifest layer '{layer}' differs from file header Layer '{meta_layer}'.",
                            "This may be acceptable if one is a layer key and the other is a display label; otherwise synchronize them.",
                        )
                    )

        layer_path = manifest.layer_to_path(layer)
        if layer and layer_path and layer_path != ".":
            if not path_value.startswith(layer_path.rstrip("/") + "/") and path_value != layer_path.rstrip("/") + ".md":
                issues.append(
                    Issue(
                        "warning",
                        path_value,
                        line,
                        "MANIFEST_LAYER_PATH_MISMATCH",
                        f"Manifest layer '{layer}' maps to '{layer_path}', but path is outside that layer.",
                        "Correct the layer or path in docs_manifest.yml.",
                    )
                )

        for related in raw_doc.get("related", []) or []:
            related_path = root / str(related)
            if not related_path.exists():
                issues.append(
                    Issue(
                        manifest.rule_severity("related_link_missing", release_gate, "warning"),
                        path_value,
                        line,
                        "MANIFEST_RELATED_PATH_MISSING",
                        f"Manifest related path does not exist: {related}",
                        "Create the related file, correct the path, or remove the stale related entry.",
                    )
                )

    should_check_unlisted = args.manifest_check_unlisted or release_gate or manifest.coverage.lower() in {"complete", "full"}
    if should_check_unlisted:
        for rel, info in sorted(file_index.items()):
            if rel.startswith("tools/") or rel.startswith(".github/"):
                continue
            if rel not in listed_paths:
                issues.append(
                    Issue(
                        manifest.rule_severity("unlisted_public_markdown", release_gate, "warning"),
                        rel,
                        1,
                        "MANIFEST_PUBLIC_MARKDOWN_UNLISTED",
                        "Public Markdown file is not listed in docs_manifest.yml.",
                        "Add it to docs_manifest.yml, or keep manifest coverage partial and omit --manifest-check-unlisted.",
                    )
                )
    else:
        unlisted_count = len([rel for rel in file_index if rel not in listed_paths and not rel.startswith("tools/")])
        if unlisted_count:
            issues.append(
                Issue(
                    "info",
                    "tools/docs_manifest.yml",
                    1,
                    "MANIFEST_PARTIAL_COVERAGE",
                    f"Manifest coverage is partial; {unlisted_count} Markdown files are not individually checked for manifest inclusion.",
                    "Use --manifest-check-unlisted or --release-gate when preparing a release if full manifest coverage is desired.",
                )
            )

    return issues, docs_checked


def run_checks(args: argparse.Namespace) -> CheckResult:
    root = Path(args.root).resolve()
    registry_path = Path(args.registry).resolve() if args.registry else root / "tools" / "Public_Format_Registry.yml"
    registry, registry_issues = Registry.load(registry_path, explicit=bool(args.registry))
    issues: List[Issue] = list(registry_issues)

    manifest: Optional[Manifest] = None
    if not args.no_manifest:
        manifest_path = Path(args.manifest).resolve() if args.manifest else root / "tools" / "docs_manifest.yml"
        explicit_manifest = bool(args.manifest)
        manifest, manifest_load_issues = Manifest.load(manifest_path, root, explicit=explicit_manifest)
        issues.extend(manifest_load_issues)

    maintenance_rules: Optional[MaintenanceRules] = None
    if not args.no_maintenance_rules:
        maintenance_path = Path(args.maintenance_rules).resolve() if args.maintenance_rules else root / "tools" / "maintenance_rules.yml"
        explicit_maintenance = bool(args.maintenance_rules)
        maintenance_rules, maintenance_load_issues = MaintenanceRules.load(maintenance_path, root, explicit=explicit_maintenance)
        issues.extend(maintenance_load_issues)

    checked_files = 0
    checked_links = 0
    external_checked = 0
    maintenance_hits = 0
    file_index: Dict[str, Dict[str, Any]] = {}

    excluded_paths = build_excluded_paths(root, registry, args)

    for path in iter_markdown_files(root, include_private_marker=args.include_private_marker, excluded_paths=excluded_paths):
        checked_files += 1
        file_issues, file_links, file_external, file_hits, file_info = check_file(path, root, registry, maintenance_rules, args)
        issues.extend(file_issues)
        checked_links += file_links
        external_checked += file_external
        maintenance_hits += file_hits
        file_index[file_info["relative"]] = file_info

    manifest_docs_checked = 0
    manifest_issues, manifest_docs_checked = check_manifest(root, manifest, registry, file_index, args)
    issues.extend(manifest_issues)

    if args.check_release_metadata:
        issues.extend(check_release_metadata(root, excluded_paths))

    severity_order = {"error": 0, "warning": 1, "info": 2}
    issues.sort(key=lambda i: (severity_order.get(i.severity, 9), i.path, i.line, i.code))
    return CheckResult(
        issues=issues,
        checked_markdown_files=checked_files,
        checked_links=checked_links,
        external_links_checked=external_checked,
        manifest_documents_checked=manifest_docs_checked,
        maintenance_term_hits=maintenance_hits,
    )


def write_json_log(result: CheckResult, path: Path) -> None:
    payload = {
        "summary": {
            "checked_markdown_files": result.checked_markdown_files,
            "checked_links": result.checked_links,
            "external_links_checked": result.external_links_checked,
            "manifest_documents_checked": result.manifest_documents_checked,
            "maintenance_term_hits": result.maintenance_term_hits,
            "errors": result.error_count,
            "warnings": result.warning_count,
            "info": result.info_count,
        },
        "issues": [issue.as_dict() for issue in result.issues],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_markdown_log(result: CheckResult, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Public Format Check Report",
        "",
        "## Overall judgment",
        "",
        f"- Checked Markdown files: {result.checked_markdown_files}",
        f"- Checked links: {result.checked_links}",
        f"- External links checked: {result.external_links_checked}",
        f"- Manifest documents checked: {result.manifest_documents_checked}",
        f"- Maintenance term hits: {result.maintenance_term_hits}",
        f"- Errors: {result.error_count}",
        f"- Warnings: {result.warning_count}",
        f"- Info: {result.info_count}",
        "",
    ]
    for severity, title in [("error", "Blocking issues"), ("warning", "Warnings"), ("info", "Informational notes")]:
        subset = [issue for issue in result.issues if issue.severity == severity]
        lines.append(f"## {title}")
        lines.append("")
        if not subset:
            lines.append("None.")
            lines.append("")
            continue
        for issue in subset:
            lines.append(f"- `{issue.path}:{issue.line}` **{issue.code}**: {issue.message}")
            if issue.suggestion:
                lines.append(f"  - Suggested fix: {issue.suggestion}")
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def print_console_summary(result: CheckResult) -> None:
    print("Public format check")
    print(f"  Markdown files: {result.checked_markdown_files}")
    print(f"  Links: {result.checked_links}")
    print(f"  External links checked: {result.external_links_checked}")
    print(f"  Manifest documents checked: {result.manifest_documents_checked}")
    print(f"  Maintenance term hits: {result.maintenance_term_hits}")
    print(f"  Errors: {result.error_count}")
    print(f"  Warnings: {result.warning_count}")
    print(f"  Info: {result.info_count}")
    for issue in result.issues[:80]:
        print(f"{issue.severity.upper()} {issue.path}:{issue.line} {issue.code}: {issue.message}")
        if issue.suggestion:
            print(f"  suggestion: {issue.suggestion}")
    if len(result.issues) > 80:
        print(f"... {len(result.issues) - 80} more issues omitted from console output")


def emit_github_annotations(result: CheckResult) -> None:
    for issue in result.issues:
        annotation_type = "error" if issue.severity == "error" else "warning" if issue.severity == "warning" else "notice"
        msg = issue.message
        if issue.suggestion:
            msg = f"{msg} Suggested fix: {issue.suggestion}"
        msg = msg.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
        path = issue.path.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
        print(f"::{annotation_type} file={path},line={issue.line},title={issue.code}::{msg}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Check Scientific Ontology public Markdown format.")
    parser.add_argument("--root", default=".", help="Repository root. Default: current directory.")
    parser.add_argument(
        "--registry",
        default=None,
        help="Path to Public_Format_Registry.yml. Default: <root>/tools/Public_Format_Registry.yml",
    )
    parser.add_argument(
        "--manifest",
        default=None,
        help="Path to docs_manifest.yml. Default: <root>/tools/docs_manifest.yml when present.",
    )
    parser.add_argument(
        "--no-manifest",
        action="store_true",
        help="Skip docs_manifest.yml checks even if the file exists.",
    )
    parser.add_argument(
        "--manifest-check-unlisted",
        action="store_true",
        help="Warn for public Markdown files not listed in docs_manifest.yml. Off by default for partial-seed manifests.",
    )
    parser.add_argument(
        "--maintenance-rules",
        default=None,
        help="Path to maintenance_rules.yml. Default: <root>/tools/maintenance_rules.yml when present.",
    )
    parser.add_argument(
        "--no-maintenance-rules",
        action="store_true",
        help="Skip maintenance_rules.yml checks even if the file exists.",
    )
    parser.add_argument(
        "--exclude-path",
        action="append",
        default=[],
        help="Relative file or directory path to exclude from public Markdown checks. May be repeated.",
    )
    parser.add_argument(
        "--check-anchors",
        action="store_true",
        help="Also check local Markdown #heading anchors. Off by default because generated anchors can be renderer-specific.",
    )
    parser.add_argument(
        "--term-context-window",
        type=int,
        default=240,
        help="Character window used to decide whether legacy/private terms are in an allowed context.",
    )
    parser.add_argument(
        "--release-gate",
        action="store_true",
        help="Use release-gate severity for manifest checks and enable unlisted manifest checks.",
    )
    parser.add_argument("--json-log", default=None, help="Write machine-readable JSON report.")
    parser.add_argument("--md-log", default=None, help="Write human/LLM-readable Markdown report.")
    parser.add_argument(
        "--github-annotations",
        action="store_true",
        help="Emit GitHub Actions annotations for issues.",
    )
    parser.add_argument(
        "--check-external",
        action="store_true",
        help="Check HTTP/HTTPS links. Off by default to avoid flaky CI.",
    )
    parser.add_argument(
        "--external-timeout",
        type=float,
        default=8.0,
        help="Timeout in seconds for each external URL check.",
    )
    parser.add_argument(
        "--check-release-metadata",
        action="store_true",
        help="Run lightweight DOI/version consistency scan on root metadata files.",
    )
    parser.add_argument(
        "--include-private-marker",
        action="store_true",
        default=True,
        help="Include 99_Private_Core_Not_Included/ marker docs in checks. Default: on.",
    )
    parser.add_argument(
        "--no-fail-on-error",
        action="store_true",
        help="Always exit 0, even if errors are found.",
    )
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    result = run_checks(args)
    print_console_summary(result)
    if args.json_log:
        write_json_log(result, Path(args.json_log))
    if args.md_log:
        write_markdown_log(result, Path(args.md_log))
    if args.github_annotations:
        emit_github_annotations(result)
    if result.error_count and not args.no_fail_on_error:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

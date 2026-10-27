#!/usr/bin/env python3
"""Shared helpers for Scientific Ontology public-site build/check tools."""
from __future__ import annotations

import hashlib
import json
import posixpath
import re
import urllib.parse
from pathlib import Path, PurePosixPath
from typing import Any, Iterable

try:
    import yaml
except ModuleNotFoundError as exc:  # pragma: no cover
    raise SystemExit(
        "PyYAML is required. Install with: python -m pip install -r requirements-public-check.txt"
    ) from exc

MARKDOWN_LINK_RE = re.compile(r"(!?\[[^\]]*\]\()([^)]+)(\))")
EXTERNAL_SCHEME_RE = re.compile(r"^[a-z][a-z0-9+.-]*:", re.I)

TEXT_EXTENSIONS = {
    ".html",
    ".css",
    ".js",
    ".mjs",
    ".json",
    ".md",
    ".txt",
    ".yml",
    ".yaml",
    ".cff",
    ".xml",
    ".svg",
}


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data or {}


def fixed_release_metadata(release_state: dict[str, Any]) -> dict[str, str]:
    """Resolve the fixed public release shown by the Living Preview banner.

    A published current release is its own fixed release. During a later
    working/release-candidate cycle, previous_release remains the fixed release
    until the new release is published.
    """
    release = release_state.get("release") or {}
    status = str(release.get("status") or "").strip()
    if status == "published":
        version = str(release.get("display_version") or "").strip()
        zenodo = release_state.get("zenodo") or {}
        version_doi = zenodo.get("version_doi") or {}
        url = str(version_doi.get("url") or "").strip()
        if not url:
            doi = str(version_doi.get("value") or "").strip()
            url = f"https://doi.org/{doi}" if doi else ""
        source = "current_release"
    else:
        previous = release_state.get("previous_release") or {}
        version = str(previous.get("display_version") or "").strip()
        doi = str(previous.get("doi") or "").strip()
        url = str(previous.get("url") or "").strip()
        if not url and doi:
            url = f"https://doi.org/{doi}"
        source = "previous_release"

    if not version:
        raise ValueError(f"fixed release version is unavailable for release status {status!r}")
    if not url:
        raise ValueError(f"fixed release DOI URL is unavailable for {version}")
    return {"version": version, "url": url, "source": source}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def norm_rel(value: str) -> str:
    value = value.replace("\\", "/").lstrip("/")
    normalized = posixpath.normpath(value)
    if normalized in {"", "."}:
        return ""
    if normalized == ".." or normalized.startswith("../"):
        raise ValueError(f"path escapes repository root: {value!r}")
    return normalized


def resolve_local_target(source_rel: str, href: str) -> tuple[str | None, str, str]:
    """Resolve a Markdown link target.

    Returns (relative_target_or_none, query, fragment). External/anchor-only links
    return None. Query and fragment include no leading ?/#.
    """
    raw = href.strip()
    if not raw or raw.startswith("#") or EXTERNAL_SCHEME_RE.match(raw):
        return None, "", ""

    before_fragment, sep_fragment, fragment = raw.partition("#")
    before_query, sep_query, query = before_fragment.partition("?")
    try:
        decoded = urllib.parse.unquote(before_query)
    except Exception:
        decoded = before_query

    if decoded.startswith("/"):
        rel = norm_rel(decoded)
    else:
        rel = norm_rel(posixpath.join(posixpath.dirname(source_rel), decoded))
    return rel, query if sep_query else "", fragment if sep_fragment else ""


def quote_github_path(rel_path: str) -> str:
    return "/".join(urllib.parse.quote(part, safe="") for part in PurePosixPath(rel_path).parts)


def github_blob_url(repository_url: str, source_ref: str, rel_path: str, query: str = "", fragment: str = "") -> str:
    base = repository_url.rstrip("/")
    ref = "/".join(urllib.parse.quote(part, safe="") for part in source_ref.split("/"))
    url = f"{base}/blob/{ref}/{quote_github_path(rel_path)}"
    if query:
        url += "?" + query
    if fragment:
        url += "#" + urllib.parse.quote(fragment, safe="-._~%")
    return url


def path_is_forbidden(rel_path: str, cfg: dict[str, Any]) -> bool:
    rel = norm_rel(rel_path)
    safety = cfg.get("safety", {})
    parts = PurePosixPath(rel).parts

    forbidden_segments = set(map(str, safety.get("forbidden_path_segments", [])))
    if any(part in forbidden_segments for part in parts):
        return True

    forbidden_prefixes = tuple(map(str, safety.get("forbidden_path_prefixes", [])))
    if rel.startswith(forbidden_prefixes):
        return True

    forbidden_exact = set(map(str, safety.get("forbidden_exact_paths", [])))
    if rel in forbidden_exact:
        return True

    filename_prefixes = tuple(map(str, safety.get("forbidden_filename_prefixes", [])))
    if any(part.startswith(filename_prefixes) for part in parts if filename_prefixes):
        return True

    return False


def iter_files(root: Path) -> Iterable[Path]:
    for path in sorted(root.rglob("*")):
        if path.is_file():
            yield path


def file_record(path: Path, root: Path) -> dict[str, Any]:
    rel = path.relative_to(root).as_posix()
    return {"path": rel, "bytes": path.stat().st_size, "sha256": sha256_file(path)}


def tree_records(root: Path, exclude: set[str] | None = None) -> list[dict[str, Any]]:
    excluded = exclude or set()
    return [file_record(path, root) for path in iter_files(root) if path.relative_to(root).as_posix() not in excluded]


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def strict_utf8(path: Path) -> str:
    data = path.read_bytes()
    if data.startswith(b"\xef\xbb\xbf"):
        raise ValueError(f"UTF-8 BOM is not allowed: {path}")
    return data.decode("utf-8", errors="strict")


def find_forbidden_keys(value: Any, forbidden: set[str], prefix: str = "$") -> list[str]:
    found: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            next_prefix = f"{prefix}.{key}"
            if str(key) in forbidden:
                found.append(next_prefix)
            found.extend(find_forbidden_keys(child, forbidden, next_prefix))
    elif isinstance(value, list):
        for idx, child in enumerate(value):
            found.extend(find_forbidden_keys(child, forbidden, f"{prefix}[{idx}]"))
    return found

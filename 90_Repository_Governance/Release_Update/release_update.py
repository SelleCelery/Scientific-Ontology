#!/usr/bin/env python3
"""Synchronize Scientific Ontology release metadata from release_state.yml.

Human-owned files (README.md and Roadmap.md) are never rewritten.
Generated/synchronized files:
  - RELEASE_NOTES.md
  - CITATION.cff
  - CITATION.md
  - .zenodo.json

Usage:
  python release_update.py --check
  python release_update.py --dry-run
  python release_update.py --write
  python release_update.py --release-check
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover - operational error path
    raise SystemExit(
        "PyYAML is required. Install with: "
        "python -m pip install -r 90_Repository_Governance/Release_Update/requirements.txt"
    ) from exc


SCRIPT_PATH = Path(__file__).resolve()
REPO_ROOT = SCRIPT_PATH.parents[2]
STATE_PATH = SCRIPT_PATH.with_name("release_state.yml")
GENERATED_PATHS = (
    Path("RELEASE_NOTES.md"),
    Path("CITATION.cff"),
    Path("CITATION.md"),
    Path(".zenodo.json"),
)

ORCID_RE = re.compile(r"^\d{4}-\d{4}-\d{4}-\d{3}[\dX]$")
DOI_RE = re.compile(r"^10\.\d{4,9}/\S+$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$")


class ValidationError(Exception):
    pass


def load_state() -> dict[str, Any]:
    try:
        raw = STATE_PATH.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise ValidationError(f"Missing state file: {STATE_PATH}") from exc
    try:
        state = yaml.safe_load(raw)
    except yaml.YAMLError as exc:
        raise ValidationError(f"Invalid YAML in {STATE_PATH}: {exc}") from exc
    if not isinstance(state, dict):
        raise ValidationError("release_state.yml must contain a mapping at the top level")
    return state


def need(mapping: dict[str, Any], key: str, where: str) -> Any:
    if key not in mapping:
        raise ValidationError(f"Missing required key: {where}.{key}")
    return mapping[key]


def as_text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{label} must be a non-empty string")
    return value.strip()


def validate_state(state: dict[str, Any], strict_release: bool = False) -> list[str]:
    warnings: list[str] = []

    project = need(state, "project", "state")
    author = need(state, "public_author", "state")
    release = need(state, "release", "state")
    previous = need(state, "previous_release", "state")
    zenodo = need(state, "zenodo", "state")
    citation = need(state, "citation", "state")
    scope = need(state, "public_scope", "state")

    if not isinstance(project, dict) or not isinstance(author, dict) or not isinstance(release, dict):
        raise ValidationError("project, public_author, and release must be mappings")

    version = as_text(need(release, "version", "release"), "release.version")
    if not SEMVER_RE.match(version):
        raise ValidationError(f"release.version is not semantic-version shaped: {version}")

    display_version = as_text(need(release, "display_version", "release"), "release.display_version")
    if display_version != f"v{version}":
        raise ValidationError(
            f"release.display_version must equal v + release.version ({display_version} != v{version})"
        )

    title = as_text(need(release, "title", "release"), "release.title")
    if display_version not in title:
        raise ValidationError("release.title must contain release.display_version")

    display_name = as_text(need(author, "display_name", "public_author"), "public_author.display_name")
    family = as_text(need(author, "family_name", "public_author"), "public_author.family_name")
    given = as_text(need(author, "given_name", "public_author"), "public_author.given_name")
    if display_name != family + given:
        warnings.append(
            "public_author.display_name is not family_name + given_name; this is allowed but should be intentional"
        )

    orcid = as_text(need(author, "orcid", "public_author"), "public_author.orcid")
    if not ORCID_RE.match(orcid):
        raise ValidationError(f"Invalid ORCID shape: {orcid}")
    orcid_url = as_text(need(author, "orcid_url", "public_author"), "public_author.orcid_url")
    if orcid_url != f"https://orcid.org/{orcid}":
        raise ValidationError("public_author.orcid_url does not exactly match public_author.orcid")
    if author.get("romanized_name") is not None:
        raise ValidationError("romanized_name must remain null unless explicitly human-registered")

    prev_doi = as_text(need(previous, "doi", "previous_release"), "previous_release.doi")
    if not DOI_RE.match(prev_doi):
        raise ValidationError(f"Invalid previous release DOI: {prev_doi}")

    version_family_doi = as_text(need(zenodo, "version_family_doi", "zenodo"), "zenodo.version_family_doi")
    if not DOI_RE.match(version_family_doi):
        raise ValidationError(f"Invalid Zenodo version-family DOI: {version_family_doi}")

    version_doi = need(zenodo, "version_doi", "zenodo")
    if not isinstance(version_doi, dict):
        raise ValidationError("zenodo.version_doi must be a mapping")
    doi_status = as_text(need(version_doi, "status", "zenodo.version_doi"), "zenodo.version_doi.status")
    doi_value = version_doi.get("value")
    doi_url = version_doi.get("url")
    if doi_status == "pending":
        if doi_value is not None or doi_url is not None:
            raise ValidationError("pending version DOI must have null value and null url")
    elif doi_status == "assigned":
        doi_value = as_text(doi_value, "zenodo.version_doi.value")
        if not DOI_RE.match(doi_value):
            raise ValidationError(f"Invalid assigned DOI: {doi_value}")
        if doi_value == prev_doi or doi_value == version_family_doi:
            raise ValidationError("version DOI must not reuse the previous-release or version-family DOI")
        expected_url = f"https://doi.org/{doi_value}"
        if doi_url != expected_url:
            raise ValidationError(f"zenodo.version_doi.url must equal {expected_url}")
    else:
        raise ValidationError("zenodo.version_doi.status must be pending or assigned")

    pub_date = release.get("publication_date")
    if pub_date is not None:
        if not isinstance(pub_date, str) or not re.match(r"^\d{4}-\d{2}-\d{2}$", pub_date):
            raise ValidationError("release.publication_date must be null or YYYY-MM-DD")
        if int(pub_date[:4]) != int(citation.get("year")):
            raise ValidationError("release.publication_date year must match citation.year")

    allowed_status = {"preparation", "release_candidate", "published", "superseded"}
    if release.get("status") not in allowed_status:
        raise ValidationError(
            "release.status must be one of: " + ", ".join(sorted(allowed_status))
        )

    if strict_release:
        if release.get("status") != "published":
            raise ValidationError("--release-check requires release.status: published")
        if pub_date is None:
            raise ValidationError("--release-check requires release.publication_date")
        if doi_status != "assigned":
            raise ValidationError("--release-check requires an assigned version-specific DOI")

    if citation.get("orcid_policy") != "propagate_exactly":
        warnings.append("citation.orcid_policy is not propagate_exactly")

    guaranteed = need(scope, "guaranteed_inclusions", "public_scope")
    if not isinstance(guaranteed, list):
        raise ValidationError("public_scope.guaranteed_inclusions must be a list")
    for item in guaranteed:
        if not isinstance(item, dict):
            raise ValidationError("Each guaranteed inclusion must be a mapping")
        rel = as_text(need(item, "path", "guaranteed inclusion"), "guaranteed inclusion path")
        if Path(rel).name.startswith("000"):
            raise ValidationError(f"Guaranteed public inclusion uses reserved 000 prefix: {rel}")
        abs_path = REPO_ROOT / rel
        if not abs_path.exists():
            raise ValidationError(f"Guaranteed public inclusion is missing from repository: {rel}")
        expected_count = item.get("document_count_ja_core")
        if expected_count is not None:
            if not abs_path.is_dir():
                raise ValidationError(f"document_count_ja_core requires a directory path: {rel}")
            expected_count = item.get("document_count_ja_core")
            if expected_count is not None:
                if not abs_path.is_dir():
                    raise ValidationError(
                        f"document_count_ja_core requires a directory path: {rel}"
                    )

                exclusions = set(item.get("document_count_exclusions", []))

                ja_core_files = [
                    path
                    for path in abs_path.glob("*.ja.md")
                    if path.name not in exclusions
                ]

                actual_count = len(ja_core_files)

                if actual_count != int(expected_count):
                    raise ValidationError(
                        f"Japanese core document count mismatch for {rel}: "
                        f"expected {expected_count}, found {actual_count}; "
                        f"excluded support files: {', '.join(sorted(exclusions)) or 'none'}"
                    )
            if actual_count != int(expected_count):
                raise ValidationError(
                    f"Japanese core document count mismatch for {rel}: "
                    f"expected {expected_count}, found {actual_count}"
                )
        eng = item.get("english_commensuration")
        if eng and not (REPO_ROOT / eng).exists():
            raise ValidationError(f"Declared English commensuration is missing: {eng}")

    if version == "5.0.0":
        deferred = scope.get("deferred_or_excluded", [])
        dssi = next((x for x in deferred if isinstance(x, dict) and x.get("id") == "dssi_application"), None)
        if not dssi or dssi.get("status") != "not_included":
            raise ValidationError("v5.0.0 must explicitly exclude the DSSI application")
        outline = next((x for x in guaranteed if x.get("id") == "operational_outline"), None)
        if not outline or outline.get("status") != "included":
            raise ValidationError("v5.0.0 must explicitly include the Operational Outline")

    # Human-owned files are observed, never rewritten.
    readme = REPO_ROOT / "README.md"
    roadmap = REPO_ROOT / "Roadmap.md"
    for path in (readme, roadmap):
        if not path.exists():
            raise ValidationError(f"Missing human-owned release file: {path.name}")
        text = path.read_text(encoding="utf-8")
        if display_version not in text:
            raise ValidationError(f"{path.name} does not mention {display_version}")

    return warnings


def author_cff(author: dict[str, Any]) -> dict[str, Any]:
    return {
        "family-names": author["family_name"],
        "given-names": author["given_name"],
        "orcid": author["orcid_url"],
    }


def render_cff(state: dict[str, Any]) -> str:
    project = state["project"]
    author = state["public_author"]
    release = state["release"]
    zenodo = state["zenodo"]
    citation = state["citation"]
    doi = zenodo["version_doi"]
    assigned = doi["status"] == "assigned"

    message = (
        "If you use or refer to this public edition, please cite the version-specific Zenodo DOI."
        if assigned
        else "This file describes the v5.0.0 release candidate. The version-specific Zenodo DOI is pending; update release_state.yml after Zenodo assigns it and rerun the release update tool."
    )

    data: dict[str, Any] = {
        "cff-version": "1.2.0",
        "message": message,
        "title": release["title"],
        "type": citation["type_cff"],
        "authors": [author_cff(author)],
        "version": release["version"],
        "license": project["license"],
        "repository-code": project["repository_url"],
        "url": doi["url"] if assigned else project["repository_url"],
        "keywords": citation["keywords"],
    }
    if release.get("publication_date"):
        data["date-released"] = release["publication_date"]
    if assigned:
        data["doi"] = doi["value"]

    preferred: dict[str, Any] = {
        "type": citation["preferred_citation_type"],
        "authors": [author_cff(author)],
        "title": release["title"],
        "year": citation["year"],
        "version": release["version"],
    }
    if assigned:
        preferred["doi"] = doi["value"]
        preferred["url"] = doi["url"]
    else:
        preferred["url"] = project["repository_url"]
    data["preferred-citation"] = preferred

    return yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=1000)


def citation_line(state: dict[str, Any]) -> str:
    author = state["public_author"]["display_name"]
    title = state["release"]["title"]
    year = state["citation"]["year"]
    doi = state["zenodo"]["version_doi"]
    if doi["status"] == "assigned":
        return f"{author}. *{title}*. Zenodo, {year}. DOI: [{doi['value']}]({doi['url']})."
    return (
        f"{author}. *{title}*. Release candidate, {year}. "
        f"Version-specific Zenodo DOI pending. Repository: <{state['project']['repository_url']}>."
    )


def render_citation_md(state: dict[str, Any]) -> str:
    project = state["project"]
    author = state["public_author"]
    release = state["release"]
    previous = state["previous_release"]
    zenodo = state["zenodo"]
    citation = state["citation"]
    doi = zenodo["version_doi"]
    assigned = doi["status"] == "assigned"

    doi_value = doi["value"] if assigned else "pending"
    recommended = citation_line(state)
    bib_key = f"scientific_ontology_v{release['version'].replace('.', '')}_{citation['year']}"

    bib_lines = [
        f"@misc{{{bib_key},",
        f"  author       = {{{author['family_name']}, {author['given_name']}}},",
        f"  title        = {{{release['title']}}},",
        f"  year         = {{{citation['year']}}},",
        f"  version      = {{{release['version']}}},",
        f"  publisher    = {{{citation['publisher']}}},",
    ]
    if assigned:
        bib_lines.extend(
            [
                f"  doi          = {{{doi['value']}}},",
                f"  url          = {{{doi['url']}}},",
            ]
        )
    else:
        bib_lines.append(f"  url          = {{{project['repository_url']}}},")
    bib_lines.append(
        "  note         = {Public conceptual research archive and documentation release for Scientific Ontology / 存在境界論}"
    )
    bib_lines.append("}")
    bibtex = "\n".join(bib_lines)

    pending_note = ""
    if not assigned:
        pending_note = """
## Pre-publication DOI state / 公開前DOI状態

The version-specific DOI for v5.0.0 has not yet been assigned. Do not reuse the v4.3.0 DOI or the version-family DOI as the v5.0.0 version DOI.

v5.0.0の版固有DOIは、まだ発行されていません。v4.3.0のDOIまたは全版DOIを、v5.0.0の版固有DOIとして流用しないでください。

After Zenodo assigns the DOI, update only `release_state.yml` first and rerun the release update tool.

ZenodoでDOIが確定した後は、まず`release_state.yml`だけを更新し、その後Release Updateを再実行します。

---
"""
    if assigned:
        citation_guidance_en = (
            "If you use, discuss, or refer to this published public edition, "
            f"cite its version-specific Zenodo DOI: {doi['value']}."
        )
        citation_guidance_ja = (
            "この公開版を利用・参照・論評する場合は、"
            f"版固有のZenodo DOI（{doi['value']}）を使用してください。"
        )
    else:
        citation_guidance_en = (
            "If you use, discuss, or refer to a published public edition, cite its "
            "version-specific Zenodo DOI. For this release candidate, use the version "
            "and repository URL until the v5.0.0 DOI is assigned."
        )
        citation_guidance_ja = (
            "公開済みPublic Editionを利用・参照・論評する場合は、版固有のZenodo DOIを"
            "使用してください。このリリース候補については、v5.0.0のDOIが確定するまで"
            "版番号とリポジトリURLを使用します。"
        )
    return f"""# Citation

> Status: Citation / {release['status']}
> Scope: Human-readable citation guidance
> Language: English and Japanese
> Target version: {release['display_version']}
> Version-specific DOI: {doi_value}

{citation_guidance_en}

{citation_guidance_ja}

---

## Public author identity / 公開著者識別

**{author['display_name']}**
Family name / 姓: **{author['family_name']}**
Given name / 名: **{author['given_name']}**
ORCID: <{author['orcid_url']}>

The Unicode author name is intentional. No Latin-script romanization is registered in this release; do not infer one.

Unicodeの著者名表記を維持します。本公開版ではローマ字表記を登録していないため、推測したローマ字表記へ置換しません。

---

## Recommended citation

{recommended}

---

{pending_note}## BibTeX

```bibtex
{bibtex}
```

---

## Machine-readable metadata

- [`CITATION.cff`](./CITATION.cff)
- [Zenodo version family](https://doi.org/{zenodo['version_family_doi']})
{f"- [Zenodo version-specific record]({doi['url']})" if assigned else "- v5.0.0 version-specific Zenodo record: pending"}

---

## Repository

GitHub: <{project['repository_url']}>

---

## Previous public release

Previous version: **{previous['display_version']}**
Previous version DOI: [${{PREV_DOI}}](https://doi.org/${{PREV_DOI}})

---

## License

Unless otherwise stated, this public edition is licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).

For details, see [`LICENSE.md`](./LICENSE.md).
""".replace("${PREV_DOI}", previous["doi"])


def render_zenodo_json(state: dict[str, Any]) -> str:
    project = state["project"]
    author = state["public_author"]
    release = state["release"]
    previous = state["previous_release"]
    zenodo = state["zenodo"]
    citation = state["citation"]

    data: dict[str, Any] = {
        "title": release["title"],
        "upload_type": "publication",
        "publication_type": citation["publication_type_zenodo"],
        "description": release["zenodo_description_en"],
        "creators": [
            {
                "name": f"{author['family_name']}, {author['given_name']}",
                "orcid": author["orcid"],
            }
        ],
        "access_right": "open",
        "license": project["license"].lower(),
        "version": release["version"],
        "keywords": citation["keywords"],
        "language": "eng",
        "related_identifiers": [
            {
                "identifier": previous["doi"],
                "relation": zenodo["related_identifiers"]["previous_release_relation"],
                "scheme": "doi",
            },
            {
                "identifier": project["repository_url"],
                "relation": zenodo["related_identifiers"]["repository_relation"],
                "scheme": "url",
            },
        ],
        "notes": release["zenodo_notes_en"],
    }
    if release.get("publication_date"):
        data["publication_date"] = release["publication_date"]
    return json.dumps(data, ensure_ascii=False, indent=2) + "\n"


def render_release_notes(state: dict[str, Any]) -> str:
    release = state["release"]
    author = state["public_author"]
    previous = state["previous_release"]
    zenodo = state["zenodo"]
    project = state["project"]
    doi = zenodo["version_doi"]
    assigned = doi["status"] == "assigned"
    release_date = release.get("publication_date") or "Pending"
    doi_display = doi["value"] if assigned else "Pending"

    included = [h for h in release["highlights"] if h.get("status") == "included"]
    en_items = "\n".join(f"- {h['en']}" for h in included)
    ja_items = "\n".join(f"- {h['ja']}" for h in included)

    doi_paragraph = (
        f"Version-specific DOI: <{doi['url']}>"
        if assigned
        else "Version-specific DOI: **pending**. Do not reuse the v4.3.0 DOI or the version-family DOI as the v5.0.0 DOI."
    )

    included_heading = (
        "Included in this release"
        if release["status"] in {"published", "superseded"}
        else "Included in this release candidate"
    )
    included_heading_ja = (
        "今回の公開版に含むもの"
        if release["status"] in {"published", "superseded"}
        else "今回の公開候補に含むもの"
    )

    return f"""# Release Notes: Scientific Ontology (SO) / 存在境界論 Public Edition {release['display_version']}


> Status: Release notes / {release['status']}
> Scope: Public release metadata / research transition / repository change log
> Language: English-first with Japanese release summary
> Version-specific DOI: {doi_display}

Release date: {release_date}

---

## Citation state

{doi_paragraph}

Public author: **{author['display_name']}**
ORCID: <{author['orcid_url']}>

For machine-readable citation metadata, see [`CITATION.cff`](./CITATION.cff).
For human-readable citation guidance, see [`CITATION.md`](./CITATION.md).

Version-family DOI: <https://doi.org/{zenodo['version_family_doi']}>
Previous release: **{previous['display_version']}** — <https://doi.org/{previous['doi']}>

---

## Release theme

> **{release['theme']['en']}**

{release['zenodo_description_en']}

{release['display_version']} is the opening release of the v5 living series, not the completion of v5. The release deliberately carries the framework into additional domains while preserving the return path by which criticism, failed correspondence, implementation problems, and residuals can revise later v5.x work.

### {included_heading}

{en_items}

### Explicit public boundary

The DSSI application itself is **not** included in {release['display_version']}. This release includes only the DSSI public research and implementation-boundary note. Application publication is a later v5.x decision and is not promised by this release.

Files whose basenames retain the local/internal `000` prefix and non-public core materials remain outside the Public Edition.

---

## 日本語要旨

> **{release['theme']['ja']}**

{release['purpose']['ja']}

### {included_heading_ja}

{ja_items}

### 公開境界

DSSIについて{release['display_version']}に含めるのは、観測・判断・主権・責任返還を扱う研究ノートと実装境界です。アプリケーション本体は含めません。アプリ版はv5.1以降で公開条件が整った場合に別途判断し、このリリースでは公開を約束しません。

`000`接頭辞を保持するローカル／内部保留ファイルと、Public Editionの非公開Coreは公開対象外です。

---

## Release-update governance

Release-level facts for this series are owned by [`90_Repository_Governance/Release_Update/release_state.yml`](./90_Repository_Governance/Release_Update/release_state.yml).

The synchronization tool updates only:

- `RELEASE_NOTES.md`
- `CITATION.cff`
- `CITATION.md`
- `.zenodo.json`

`README.md` and `Roadmap.md` remain human-owned. The tool may validate their release references, but it does not rewrite their conceptual or directional content.

Standard flow:

```text
release_state.yml
    -> --check / --dry-run
    -> human diff review
    -> --write
    -> validation
    -> commit
```

When Zenodo assigns the version-specific DOI, update `release_state.yml` first and rerun the synchronizer. No provisional or inferred DOI is generated.

---

## License

This release continues the **CC BY 4.0** licensing policy unless an individual document states otherwise.

Repository: <{project['repository_url']}>
"""


def render_all(state: dict[str, Any]) -> dict[Path, str]:
    return {
        Path("RELEASE_NOTES.md"): render_release_notes(state),
        Path("CITATION.cff"): render_cff(state),
        Path("CITATION.md"): render_citation_md(state),
        Path(".zenodo.json"): render_zenodo_json(state),
    }


def validate_rendered(rendered: dict[Path, str]) -> None:
    for path, content in rendered.items():
        bad_lines = [
            index
            for index, line in enumerate(content.splitlines(), start=1)
            if line.endswith((" ", "\t"))
        ]
        if bad_lines:
            raise ValidationError(
                f"Generated {path} contains trailing whitespace on lines: "
                + ", ".join(map(str, bad_lines[:20]))
            )
    try:
        cff = yaml.safe_load(rendered[Path("CITATION.cff")])
    except yaml.YAMLError as exc:
        raise ValidationError(f"Generated CITATION.cff is invalid YAML: {exc}") from exc
    if not isinstance(cff, dict) or cff.get("cff-version") != "1.2.0":
        raise ValidationError("Generated CITATION.cff failed structural validation")
    try:
        zen = json.loads(rendered[Path(".zenodo.json")])
    except json.JSONDecodeError as exc:
        raise ValidationError(f"Generated .zenodo.json is invalid JSON: {exc}") from exc
    if not zen.get("creators"):
        raise ValidationError("Generated .zenodo.json has no creators")


def diff_text(path: Path, expected: str) -> str:
    target = REPO_ROOT / path
    actual = target.read_text(encoding="utf-8") if target.exists() else ""
    return "".join(
        difflib.unified_diff(
            actual.splitlines(keepends=True),
            expected.splitlines(keepends=True),
            fromfile=str(path),
            tofile=f"{path} (generated)",
        )
    )


def sync_status(rendered: dict[Path, str]) -> tuple[list[Path], list[Path]]:
    in_sync: list[Path] = []
    out_of_sync: list[Path] = []
    for path, expected in rendered.items():
        target = REPO_ROOT / path
        if target.exists() and target.read_text(encoding="utf-8") == expected:
            in_sync.append(path)
        else:
            out_of_sync.append(path)
    return in_sync, out_of_sync


def write_rendered(rendered: dict[Path, str]) -> None:
    for path, content in rendered.items():
        target = REPO_ROOT / path
        target.write_text(content, encoding="utf-8", newline="\n")
        print(f"WROTE {path}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--check", action="store_true", help="validate state and report synchronization status")
    group.add_argument("--dry-run", action="store_true", help="show generated diffs without writing")
    group.add_argument("--write", action="store_true", help="write synchronized release files")
    group.add_argument(
        "--release-check",
        action="store_true",
        help="strict publication check: requires published status, date, and assigned version DOI",
    )
    args = parser.parse_args()

    try:
        state = load_state()
        warnings = validate_state(state, strict_release=args.release_check)
        rendered = render_all(state)
        validate_rendered(rendered)
    except ValidationError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    for warning in warnings:
        print(f"WARNING: {warning}")

    in_sync, out_of_sync = sync_status(rendered)

    if args.dry_run:
        if not out_of_sync:
            print("No generated changes. Release metadata is synchronized.")
            return 0
        for path in out_of_sync:
            print(diff_text(path, rendered[path]))
        return 0

    if args.write:
        write_rendered(rendered)
        print("Release metadata synchronization complete.")
        return 0

    # --check and --release-check
    for path in in_sync:
        print(f"OK   {path}")
    for path in out_of_sync:
        print(f"DIFF {path}")
    if out_of_sync:
        print("Generated release files are not synchronized. Run --dry-run, review, then --write.")
        return 1

    if args.release_check:
        print("RELEASE CHECK PASS")
    else:
        print("CHECK PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

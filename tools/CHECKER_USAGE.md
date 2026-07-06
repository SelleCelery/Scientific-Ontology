# Public Format Checker Usage / 公開形式チェッカー運用メモ

> Status: Working note
> Scope: repository-maintenance
> Language: en
> Claim strength: S0/S1

## 1. Purpose / 目的

This checker separates mechanical public-format failures from interpretive editorial judgment.

The Python script checks what can be checked mechanically: metadata headers, README structure, local links, optional local Markdown anchors, optional external HTTP/HTTPS links, forbidden public paths, stale README document lists, public-manifest consistency, terminology drift, caution-term boundary markers, generated-report exclusion, and lightweight release metadata.

LLM or human review should handle what requires judgment: whether a warning is a real public-format drift, whether a claim boundary is sufficient, whether a deviation should be accepted as an exception, and how to rewrite the text.

## 2. Placement / 配置

Place files as follows:

```text
.github/workflows/public-format-check.yml
requirements-public-check.txt
scripts/check_public_format.py
tools/Public_Format_Registry.yml
tools/docs_manifest.yml
tools/maintenance_rules.yml
```

`Public_Format_Registry.yml` is the format schema. It defines document types, README variants, status values, metadata labels, forbidden public patterns, and review phases.

`docs_manifest.yml` is the public document ledger. It records expected public documents, their layer, status, public profile, and related files. At the initial stage, it should usually use `coverage: partial-seed` so that not every unlisted Markdown file becomes a release blocker.

`maintenance_rules.yml` is the terminology and maintenance rule file. It records public-name drift, forbidden public patterns, caution terms, private-core term handling, and claim/profile usage rules.

## 3. Local run / ローカル実行

Install dependencies:

```bash
python -m pip install -r requirements-public-check.txt
```

Run the normal checker:

```bash
python scripts/check_public_format.py \
  --root . \
  --registry tools/Public_Format_Registry.yml \
  --manifest tools/docs_manifest.yml \
  --maintenance-rules tools/maintenance_rules.yml \
  --md-log public_format_report.md \
  --json-log public_format_report.json \
  --check-release-metadata
```

Windows PowerShell form:

```powershell
python scripts\check_public_format.py `
  --root . `
  --registry tools\Public_Format_Registry.yml `
  --manifest tools\docs_manifest.yml `
  --maintenance-rules tools\maintenance_rules.yml `
  --md-log public_format_report.md `
  --json-log public_format_report.json `
  --check-release-metadata
```

If `python` is not available but the Windows Python launcher is installed, use `py`:

```powershell
py scripts\check_public_format.py `
  --root . `
  --registry tools\Public_Format_Registry.yml `
  --manifest tools\docs_manifest.yml `
  --maintenance-rules tools\maintenance_rules.yml `
  --md-log public_format_report.md `
  --json-log public_format_report.json `
  --check-release-metadata
```

External HTTP/HTTPS link checks are disabled by default because they can make CI flaky. Enable them only when needed:

```bash
python scripts/check_public_format.py \
  --root . \
  --registry tools/Public_Format_Registry.yml \
  --manifest tools/docs_manifest.yml \
  --maintenance-rules tools/maintenance_rules.yml \
  --check-external
```

Local Markdown heading-anchor checks are also optional because rendered anchor slugs can differ slightly by renderer. Enable them when reviewing navigation quality:

```bash
python scripts/check_public_format.py \
  --root . \
  --registry tools/Public_Format_Registry.yml \
  --manifest tools/docs_manifest.yml \
  --maintenance-rules tools/maintenance_rules.yml \
  --check-anchors
```

Generated checker reports and checker-operation notes are excluded from public Markdown scanning by default:

```text
public_format_report.md
public_format_report.json
CHECKER_USAGE.md
CHECKER_USAGE*.md
CHECKER_EXTENSION_REPORT.md
CHECKER_EXTENSION_REPORT*.md
.checker_reports/
checker_reports/
```

`CHECKER_USAGE*.md` covers duplicate downloaded copies such as `CHECKER_USAGE(4).md`. These files are operational notes, not public theory documents.

Use `--exclude-path <path>` for additional local-only generated files or directories.

Release-gate mode uses stricter manifest handling and checks unlisted public Markdown files:

```bash
python scripts/check_public_format.py \
  --root . \
  --registry tools/Public_Format_Registry.yml \
  --manifest tools/docs_manifest.yml \
  --maintenance-rules tools/maintenance_rules.yml \
  --release-gate \
  --check-release-metadata
```

## 4. Supported files / 対応ファイル

The checker now reads all three maintenance files directly:

```text
tools/Public_Format_Registry.yml
tools/docs_manifest.yml
tools/maintenance_rules.yml
```

You can disable the optional files when needed:

```bash
python scripts/check_public_format.py --root . --no-manifest
python scripts/check_public_format.py --root . --no-maintenance-rules
```

## 5. What is checked / チェック内容

### Public_Format_Registry.yml

- Required metadata fields such as `Status`.
- Registered `Status` values.
- README variants: `root_readme`, `layer_readme`, `subdirectory_readme`.
- Required README sections by README type.
- Whether README document lists omit same-directory Markdown files when required.
- Forbidden public patterns.
- Generated checker output exclusions.
- Language and English-commensuration markers.
- Basic public-profile and claim-strength expectations.

### docs_manifest.yml

- Manifest YAML parseability.
- Required manifest fields.
- Registered `document_type` and `state` values.
- Manifest path existence, with `state: planned` allowed.
- Manifest status vs registry status values.
- Manifest status vs file-header `Status`.
- Manifest public_profile vs file-header `Public profile` / transitional `Claim profile`.
- Manifest layer vs path consistency.
- Existence of `related` paths.
- Optional unlisted-public-Markdown checks via `--manifest-check-unlisted` or `--release-gate`.

In `coverage: partial-seed`, unlisted Markdown files are summarized as `INFO` by default rather than emitted as one warning per file.

### maintenance_rules.yml

- Replacement rules such as `Internal Time -> intrinsic time`.
- Allowed-near and allowed-pattern contexts for legacy terms such as former names or explicit prohibited-rendering notes.
- Exception entries that suppress known-safe occurrences, such as "do not translate 内在時間 as Internal Time".
- Caution terms such as `エンタングルメント` and their expected boundary markers.
- Additional forbidden public patterns.
- Private-core terms and whether they appear only as excluded-material markers.
- Profile-label drift such as `Claim profile: S...`.

## 6. Output policy / 出力方針

- `ERROR`: mechanical blockers, such as missing `Status`, broken local links, forbidden public paths, malformed YAML, private-core exposure that is not abstracted, or release-critical metadata mismatch.
- `WARNING`: likely public-format drift, such as missing claim strength, missing public profile, missing English rendering marker, stale README document lists, unregistered status values, term drift, or missing non-claim boundary language.
- `INFO`: useful review notes that should not block publication by themselves.

The Markdown report is meant to be pasted into an LLM for repair planning. The JSON report is meant for future automation.

## 7. Intended workflow / 想定運用

1. Python checks what can be checked mechanically.
2. CI stores Markdown and JSON logs.
3. LLM reads the Markdown report together with the three `tools/` YAML files.
4. LLM proposes edits and separates blocking issues from acceptable exceptions.
5. Human decides which warnings are real format drift and which deviations should remain.

## 8. README classification / README分類

README documents should not all use the same structure.

Recommended classification:

```text
README.md                                -> root_readme
00_Overview/README.md                    -> layer_readme
01_Sat_Truth/README.md                   -> layer_readme
02_Raj_Beauty/README.md                  -> layer_readme
03_Tam_Goodness/README.md                -> layer_readme
04_Applications/README.md                -> layer_readme
05_Research_Notes/README.md              -> layer_readme
06_Visual_Materials/README.md            -> layer_readme
99_Private_Core_Not_Included/README.md   -> layer_readme / private-core marker
04_Applications/*/README.md              -> subdirectory_readme
05_Research_Notes/*/README.md            -> subdirectory_readme
```

The root README is a repository entrance and should not be forced into the layer README structure.

Layer README files should include layer role, public scope, included/not included, documents, and maintenance notes.

Subdirectory README files should be lighter and may use directory role, public scope, documents, and maintenance notes.

## 9. Maintenance exceptions / 保守例外

Some deprecated or forbidden renderings must appear in public documents because the document explicitly says not to use them. These are not terminology drift.

Store such exceptions in `tools/maintenance_rules.yml`, not in Python code. Use `term_rules.exceptions` or the replacement rule's `allowed_patterns` / `allowed_near` fields. Set `report: false` or `report_allowed: false` when the occurrence should be fully suppressed.

Example purpose:

```yaml
term_rules:
  replacements:
    - from: "Internal Time"
      use: "intrinsic time"
      severity: "error"
      report_allowed: false
      allowed_near:
        - "とは訳さない"
        - "do not translate"

  exceptions:
    - term: "Internal Time"
      report: false
      paths:
        - "05_Research_Notes/Claim_Strength_Table_History_Field_Topology.md"
      allowed_patterns:
        - "`?Internal Time`?.{0,160}(とは訳さない|訳さない)"
```

This keeps the checker strict for real drift while avoiding repeated false positives for explicit non-use notes.

## 10. GitHub Actions / GitHub Actions

The provided workflow runs the normal checker on pull requests and pushes to `main`.

Manual `workflow_dispatch` supports two optional inputs:

- `release_gate`: stricter manifest checks.
- `check_external`: external HTTP/HTTPS link checks.
- `check_anchors`: local Markdown heading-anchor checks.

## 11. Practical rule / 実用上の原則

Do not use this checker to freeze inquiry.

Use it to stabilize the public boundary: links, metadata, release facts, terminology drift, and non-claim boundaries.

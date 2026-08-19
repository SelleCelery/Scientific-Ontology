# DN-6 Release Gate Report / DN-6 リリースゲート報告

> Gate: `DN-6`
> Target: `v5.0.0`
> Mode: `publication`
> Result: **PASS**

## 1. 判定

v5.0 のこのモードに必要な機械検証は通過した。既知 warning は解決済みとは扱わず、設定された上限内の技術負債として保持する。

## 2. Required checks

- **PASS** `index-fresh` — `python scripts/build_docs_index.py --visibility public --check`
- **PASS** `graph-fresh` — `python scripts/build_docs_graph.py --visibility public --check`
- **PASS** `public-graph-fresh` — `python scripts/build_public_graph.py --check`
- **PASS** `public-catalog-fresh` — `python scripts/build_public_catalog.py --check`
- **PASS** `search-browse-regression` — `python scripts/query_docs.py test`
- **PASS** `graph-regression` — `python scripts/query_docs.py graph-test`
- **PASS** `web-parity` — `node scripts/check_docs_web_parity.mjs`
- **PASS** `language-resolution` — `node scripts/check_navigator_language_resolution.mjs`
- **PASS** `reader-boundary` — `python scripts/serve_navigator.py --check`
- **PASS** `navigator-interface` — `python scripts/check_navigator_interface.py`
- **PASS** `release-metadata-sync` — `python 90_Repository_Governance/Release_Update/release_update.py --check`
- **PASS** `publication-release-check` — `python 90_Repository_Governance/Release_Update/release_update.py --release-check`
- **PASS** `public-format-release-gate` — `python scripts/check_public_format.py --release-gate --check-release-metadata --json-log <temporary-json-report>`

## 3. Data / boundary checks

- **PASS** `expected:catalog_documents` — actual=130, expected=130
- **PASS** `expected:registered_documents` — actual=30, expected=30
- **PASS** `expected:provisional_documents` — actual=100, expected=100
- **PASS** `expected:language_pair_families` — actual=39, expected=39
- **PASS** `expected:graph_nodes` — actual=313, expected=313
- **PASS** `expected:graph_edges` — actual=1916, expected=1916
- **PASS** `expected:observed_unregistered_documents` — actual=0, expected=0
- **PASS** `public-catalog-no-developer-fields` — none
- **PASS** `public-graph-no-developer-top-level-data` — none
- **PASS** `public-graph-semantic-parity` — public=313/1916, canonical=313/1916
- **PASS** `provisional-no-invented-strong-relations` — none
- **PASS** `public-format-errors-zero` — errors=0
- **PASS** `public-format-warning-codes-known` — none
- **PASS** `public-format-warning-debt-not-increased` — none

## 4. Public format warning debt

- Errors: 0
- Warnings: 119
- Info: 104

- `ASSERTION_PUBLIC_PROFILE_WITHOUT_CLAIM_STRENGTH`: 1 / ceiling 1
- `CAUTION_TERM_BOUNDARY_MISSING`: 12 / ceiling 12
- `CLAIM_STRENGTH_SUGGESTED`: 4 / ceiling 4
- `CONTRACT_EXPORT_WITHOUT_CONSUMER`: 13 / ceiling 13
- `DOCUMENT_LOCAL_CONCEPT_INFERRED`: 9 / ceiling 9
- `MANIFEST_DOCUMENT_TYPE_MISMATCH`: 17 / ceiling 17
- `MANIFEST_PUBLIC_MARKDOWN_UNLISTED`: 1 / ceiling 1
- `MANIFEST_PUBLIC_PROFILE_MISMATCH`: 2 / ceiling 2
- `MANIFEST_STATUS_HEADER_MISMATCH`: 7 / ceiling 7
- `NON_CLAIM_BOUNDARY_SUGGESTED`: 36 / ceiling 36
- `PRIVATE_CORE_TERM_REVIEW`: 3 / ceiling 3
- `PROFILE_LABEL_DRIFT`: 1 / ceiling 1
- `README_DOCUMENT_LIST_STALE`: 13 / ceiling 13

## 5. v5.1 以降へ持ち越す Developer 系

- conditional stale-source validation for apply_registration_review.py
- candidate-only / registered-revision-only / mixed review transaction tests
- ruamel.yaml development dependency declaration
- partial-apply candidate/revision reconciliation
- unified metadata editing and canonical apply workflow
- machine-generated/synchronized Markdown metadata headers
- content-hash / body-hash based metadata synchronization

## 6. Publication mode

release-candidate gate と実公開 gate は分離する。Zenodo の版固有 DOI、公開日、published status が確定するまで、それらを推測して埋めない。

```powershell
python scripts/check_dn6_release_gate.py --mode publication
```

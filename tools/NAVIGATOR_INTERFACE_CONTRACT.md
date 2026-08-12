# Navigator Public / Developer Interface Contract

> Status: Repository governance specification
> Track: Document Navigation Infrastructure
> Stage: DN-5.5A

## 1. Responsibility split

The Navigator has one shared reading/search/relation implementation and two responsibility surfaces.

```text
Public Navigator
  = read, find, and traverse registered + public-safe provisional documents

Developer Navigator
  = inspect, review, revise, and maintain the metadata feeding that public surface
```

`provisional` does not mean private. From DN-5.5 onward it means the document is already present in the canonical manifest, while metadata review remains open.

## 2. Public Navigator contract

Default entry:

```text
/navigator/
```

Reader-facing capabilities:

```text
Read
  - system-layer introductions
  - layer README entry points
  - guide-document entry points
  - topic and starter-question entry points

Search
  - explainable direct-relevance search
  - registered + public-safe provisional documents
  - no graph-centrality ranking

Relation Map
  - typed/observed relation traversal
  - relation direction remains explicit
  - relation != truth / observed link != ownership

Reader
  - strict UTF-8 Markdown reading
  - reached from Read, Search, or Relations
```

The fixed header provides common navigation controls on Public and Developer shells:

```text
Menu
Back
Top
Bottom
Language
```

The public surface must not expose developer review state, confidence, evidence excerpts, human-judgment flags, source hashes, manifest-apply controls, or private/process paths.

A provisional document may show a compact `仮登録 / Provisional` badge. That badge reports registration state only; it is not a quality or truth score.

## 3. Single-manifest public catalog

Public runtime document/search metadata is generated from the single manifest-derived index:

```text
tools/docs_manifest.yml
        ↓
tools/docs_index.json
        ↓ public-safe projection
scripts/build_public_catalog.py
        ↓
tools/docs_public_catalog.json
```

`tools/docs_registration_candidates.yml` remains a Developer/audit source after DN-5.5. It is not merged into the Public runtime catalog.

The public catalog contains:

- every document in the canonical index as `registration_state: registered`;
- every manifest document included by the active visibility profile, carrying `registration_state: registered|provisional`;
- no candidate confidence, evidence, review notes, human-judgment flags, or maintenance diagnostics.

Provisional support documents may remain readable in the catalog while `discovery.searchable: false` keeps them out of default search ranking.

Provisional projection may supply reader-facing title, role, scope, topics, aliases, reader questions, entry level, and display state. It must not create canonical concept ownership or typed logical relations.

### 3.1 UI-language document resolution

Canonical JA and EN documents remain separate manifest entries. The Public presentation layer groups counterpart files only for display/navigation.

```text
canonical identity != presentation grouping
```

`build_public_catalog.py` adds presentation-only metadata:

```text
presentation.language
presentation.family_key
presentation.counterpart_path
```

The Public Navigator must apply the following resolution rule consistently in Read, Search, layer/topic listings, relation traversal, related-document links, and Reader language switching:

```text
UI = JA
  JA counterpart -> JA
  bilingual/und  -> same document
  JA unavailable -> EN/single-language fallback

UI = EN
  EN counterpart -> EN
  bilingual/und  -> same document
  EN unavailable -> JA/single-language fallback
```

When both JA and EN variants exist, Public lists/search results collapse the pair to one logical presentation entry. Developer mode may continue to expose both canonical entries for audit. Changing the UI language while reading a paired document should resolve to the counterpart rather than merely translating chrome labels.

```text
provisional registration != completed human metadata review
provisional topic != ontological classification
provisional doc_id = canonical ledger identity with review still open
provisional role != theory rewrite
candidate evidence != public proof
```

## 4. Graph boundary

`tools/docs_graph.json` remains the canonical relation source of truth. Public runtime receives a sanitized semantic projection in `tools/docs_public_graph.json`; Developer mode may load the canonical graph with source hashes and diagnostics.

Provisional catalog metadata may improve the human-facing title/role of an existing `observed_document`, but it must not synthesize edges such as:

```text
owns
imports
exports
tests
returns_to
delegates
```

A provisional search result opens the relation map through its manifest-backed `document` node. Promotion does not invent typed logical relations: relation content still comes only from declared or observed graph provenance.

## 5. Developer Navigator contract

Development entry:

```text
/navigator/dev.html
```

Developer mode uses the same Public catalog/search/graph base and adds:

```text
Unified Review Pool
  - provisionally registered documents
  - registered revision proposals

Data Audit
  - catalog / graph / candidate coverage
  - maintenance diagnostics

Review operations
  - approve
  - approve with edits
  - hold
  - reject
  - manual candidate
  - ad-hoc registered revision
```

Registered reader-question audit proposals are projected for Developer use through:

```text
tools/docs_registered_reader_question_review.yml
  -> scripts/build_registered_reader_question_review_preview.py
  -> tools/docs_registered_reader_question_review.preview.json
```

They are revision seeds only. The current canonical registered document remains active until an approved review transaction is explicitly applied.

## 6. Review persistence and export

In-progress review state may autosave to browser `localStorage`.

File creation is explicit only:

```text
browser local state
  -- user clicks Export review --> docs_registration_review.json
```

The browser does not automatically download review files and does not write repository files.

The exported review transaction records source hashes, candidate decisions, registered revision decisions, manual candidates, and before/after snapshots. Schema 0.2 binds the transaction to both the candidate ledger and registered revision seed.

## 7. Write authority

```text
docs_manifest.yml
  UI read: indirect
  UI write: forbidden
  repository apply: explicit only

docs_registration_candidates.yml
  UI read: indirect via preview/public projection
  UI write: forbidden

docs_index.json / docs_graph.json
  canonical/generated Developer read models; hand edit forbidden

docs_public_catalog.json / docs_public_graph.json
  generated Public read models; source hashes, diagnostics, and review internals removed; hand edit forbidden

docs_registration_candidates.preview.json
  generated Developer read model; hand edit forbidden

docs_registered_reader_question_review.preview.json
  generated Developer revision-seed read model; hand edit forbidden

localStorage / docs_registration_review.json
  review transaction state; non-canonical
```

Canonical manifest application occurs only through repository-side tooling after validation and dry-run.

## 8. Public information architecture

The public Navigator has three permanent entry surfaces plus Reader detail views.

```text
Read
Search
Relation Map

Reader = detail view reached from them
```

The old standalone Explore concept is folded into Read. Topic discovery remains available within the reader entrance.

Layer pages may list both registered and provisional public documents. Guide cards answer why a reader may want to open the document rather than merely exposing filenames.

## 9. Runtime inputs

Public runtime:

```text
tools/docs_public_catalog.json
tools/docs_public_graph.json
navigator/public-content.json
```

Developer runtime additionally loads:

```text
tools/docs_graph.json
tools/docs_registration_candidates.preview.json
tools/docs_registered_reader_question_review.preview.json
browser-local review state
```

The default public shell must not fetch either Developer preview artifact.

## 10. Canonical flow

```text
Public Markdown
      ↓
canonical docs_manifest.yml
  registered + provisional
      ↓
docs_index.json + docs_graph.json
      ↓
Public catalog + sanitized public graph + language presentation projection
      ↓
Public Navigator

Candidate/revision ledgers
      ↓
Developer review (v5.1+ completion path)
      ↓ explicit validate/apply
canonical docs_manifest.yml
```

This separates public usefulness from human-audit throughput while recording the provisional status canonically in the manifest.

## 11. DN-6 release boundary

DN-6 should verify at minimum:

```text
public catalog is fresh
canonical index is fresh
graph is fresh
public graph is fresh and contains no source hashes or diagnostics
public catalog contains no developer-only candidate metadata or source hashes
provisional entries invent no concept ownership or typed logical relations
public shell has no Developer preview dependency
private/process paths do not leak
UTF-8 Reader boundary passes
search regression passes
relation graph regression passes
public-content paths exist and are readable
JA/EN counterpart resolution passes and Public does not surface the opposite-language variant when a requested-language counterpart exists
```

The Developer Navigator is repository-maintenance tooling. It may exist in the repository distribution while remaining clearly separated from the default public entry.

## 12. Non-claims

```text
reader-friendly copy != canonical definition
search score != truth
relation map != evidence ranking
layer placement != ontological proof
provisional registration != completed metadata review
review approval != automatic manifest write
```

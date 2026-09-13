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
  - local KaTeX rendering for supported TeX math
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

Claim Assessment Lab
  - experimental frozen-protocol execution
  - export/import execution packs
  - optional local runner through an explicit server-side adapter
  - claim-level before/after human review
  - no direct canonical write

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

Registration review uses one Developer-only read model:

```text
tools/docs_manifest.yml --------------------┐
                                             ├─> scripts/build_registration_workbench_preview.py
tools/docs_revision_proposals.yml ----------┘
                                                   ↓
                                  tools/docs_registration_workbench.preview.json
```

`provisional` review reads the current manifest state. Registered-document metadata proposals live in the generic revision-proposal source. The browser does not write either source. The current canonical document remains active until an approved review transaction is validated and explicitly applied repository-side.

Experimental claim assessment is loaded separately from:

```text
tools/assessment/repository_assessment_protocols.yml
  -> scripts/build_repository_assessment_protocols_preview.py
  -> tools/assessment/repository_assessment_protocols.preview.json
  -> Developer Navigator / Claim Assessment Lab
```

The Assessment Lab is intentionally non-canonical. A protocol revision is frozen for a run, applied across the complete selected fixture without mid-run repair, and then reviewed. The current v0.2 surface separates `document_profile`, `representative_claims`, `claim_hotspots`, and `nonclaim_boundaries`: document profiles are the primary review unit, hotspot classifications are local-only, and explicit nonclaims do not receive S/E. Its transaction model mirrors the existing review surface (`before / after`, `approve / approve_with_edits / hold / reject`) so a mature protocol can later be promoted without making the experimental lab itself authoritative.

## 6. Review persistence and export

In-progress review state may autosave to browser `localStorage`.

File creation is explicit only:

```text
browser local state
  -- user clicks Export review --> docs_registration_review.json
```

The browser does not automatically download review files and does not write repository files.

The exported review transaction records source hashes, provisional decisions, registered revision decisions, manual candidates, and before/after snapshots. Schema 0.3 binds the transaction to the current manifest/graph and the generic revision-proposal source.

## 7. Write authority

```text
docs_manifest.yml
  UI read: indirect
  UI write: forbidden
  repository apply: explicit only

docs_revision_proposals.yml
  UI read: indirect via Developer preview
  UI write: forbidden
  role: partial metadata revision proposals, not a second manifest

docs_index.json / docs_graph.json
  canonical/generated Developer read models; hand edit forbidden

docs_public_catalog.json / docs_public_graph.json
  generated Public read models; source hashes, diagnostics, and review internals removed; hand edit forbidden

docs_registration_workbench.preview.json
  generated Developer read model derived from manifest + revision proposals; hand edit forbidden

localStorage / docs_registration_review.json
  registration review transaction state; non-canonical

tools/assessment/repository_assessment_protocols.yml
  experimental frozen-protocol ledger; Developer-only input

tools/assessment/repository_assessment_protocols.preview.json
  generated Developer read model; hand edit forbidden

repository_assessment_execution.json / repository_assessment_run.json / repository_assessment_review.json
  experimental representative-claim / hotspot assessment artifacts; non-canonical
```

Canonical manifest application occurs only through repository-side tooling after validation and dry-run. When a generic revision proposal is explicitly resolved as approve/reject and applied, repository-side tooling also consumes that resolved proposal from the active proposal ledger; `hold` remains active.

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
tools/docs_registration_workbench.preview.json
tools/assessment/repository_assessment_protocols.preview.json
/api/assessment/runner status (Developer local server only)
browser-local review state
```

The default public shell must not fetch Developer preview artifacts or the assessment runner endpoint.

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

manifest-backed provisional set + generic revision proposals
      ↓
Developer review
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

## Reading-first presentation

Public Navigator is a reading surface, not a repository inspection surface.
The first visible content of a Reader view is the localized document title and
then the prose itself. Paths, filenames, document IDs, registration state,
claim-strength labels, authority labels, scope, and public-handling metadata are
not part of the initial Public reading surface. Developer inspection retains the
technical identity and source bytes.

This is presentation masking, not secrecy. Source files and generated public
catalogs can still contain paths and metadata needed for repository operation.
The Public UI must not substitute a filename/path/ID when a localized display
title is unavailable; it uses a neutral Document label instead. A single-language
document keeps an explicit body-language fallback notice so an English display
title never implies that an English body exists.

In source Markdown links, a label consisting only of a filename, path, or ID may
be replaced for display by the localized catalog title. Authored descriptive
labels, prose, code examples, source bytes, and link identity are not rewritten.

### Reading controls and source metadata

The Public Reader removes a recognized opening repository-metadata quote from
its rendered prose. The current recognized fields include Document ID, Status,
State, Scope, Language, Claim strength, Layer, Authority, Public profile, Public
handling, Primary question, Search terms, Document role, Publication layer, and
Maturity. This rule applies only when a block consists of repository-header
fields; ordinary quotations are not hidden. The source Markdown is not edited by
this presentation step.

Reader controls are intentionally compact. The current surface provides:

- heading-based contents;
- three text sizes;
- system, light, dark, and paper reading themes;
- a copy-link action that retains the UI language;
- a contextual action for text selected in the article, allowing the reader to
  send an unfamiliar phrase directly to Navigator search without retyping it.

The selected-text action appears only after a selection. Reading controls must
not permanently occupy the prose area. Reader preferences use dedicated
versioned local-storage keys and failure to persist a preference must not block
reading. No account, analytics, external annotation service, or canonical write
is introduced by these controls.

### TeX math rendering

The Reader recognizes inline `$...$` and `\(...\)` math, plus display `$$...$$`
and `\[...\]` blocks, outside fenced/inline code. Math is rendered with a
repository-vendored KaTeX runtime and local font assets; no CDN or runtime
network request is required. The TeX source remains the Markdown source of
record. If KaTeX cannot be loaded or rejects an expression, the Reader shows the
original delimiters and TeX text rather than dropping or silently rewriting the
expression.

KaTeX output remains `htmlAndMathml` with `trust: false`. The HTML branch is the
visual representation and is `aria-hidden`; the MathML branch remains available
to accessibility technology but must be visually clipped by the vendored
KaTeX stylesheet. The vendor CSS must use KaTeX's ordinary unscoped selector
semantics and must not inherit a host-specific wrapper such as a Gradio container.
Because removing a host wrapper lowers selector specificity, browser regression
tests also verify that KaTeX internal classes do not leak onto similarly named
Navigator elements, that inline/display layout remains stable, and that print
media does not reveal the MathML branch as a second visible formula. Local font
references must resolve inside `navigator/vendor/katex/`; remote font/CDN URLs
are not allowed.

TeX delimiters are presentation syntax, not metadata. The Reader does not
reinterpret formulas as stronger claims, and code spans/fences remain literal.
For subscripts and superscripts, source Markdown should use ordinary TeX syntax
such as `$\Omega_t$`; `\_` means a literal underscore in TeX and is not a
subscript operator.

When switching language editions, section fragments are cleared rather than
assuming JA/EN headings are structurally identical. The article `lang` attribute
follows the body actually shown.

### Reader home topology

The Public home is organized by reading role, not repository numbering. Repository
paths keep their numeric prefixes for identity and maintenance, but those numbers
do not define the reader-facing order and are not presented as a progression.

The v5.1 home order is:

1. **Contact** — `07_Creative_Offshoots`, then `06_Visual_Materials`. These are
   encounter surfaces: outward expression/operation and visual compression. They
   are intended to create contact before requiring a sequential theory reading.
2. **Canonical entrances** — root `README.md` and the System Map. These establish
   what the repository is and how the whole is arranged.
3. **Editorial reading channels** — Featured and Recommended remain explicit
   editorial selections and do not become canonical authority by placement.
4. **Working domains** — Applications and Research Notes.
5. **Core system** — Truth, Beauty, and Goodness.
6. **System guide** — Overview. Overview is a guide to how the system can be read,
   not a mandatory first chapter.

`navigator/public-content.json` owns this reader-facing grouping through
`home_group`. The grouping does not rename repository directories, change
canonical identity, or alter document authority. Public and Developer layer
pages use the selected UI language to collapse an explicit JA/EN pair into one
logical document card; Developer mode retains physical paths inside document
detail/audit surfaces rather than duplicating the pair as two primary cards.

### Editorial reading channels

Top-page reading recommendations are editor-controlled, not hard-coded in the
application and not inferred from layer 07. `navigator/public-content.json`
contains `reading_channels`. A channel owns presentation copy, order, layout,
enabled state, and an ordered list of public-catalog document IDs.

The initial channels are:

- `featured`: documents the editor explicitly wants to put forward now;
- `recommended`: an editor-curated reading sequence;
- `explore`: an optional channel for deliberately distant or cross-layer reading.

A channel may be empty. An empty channel renders no fabricated recommendation.
Any public-catalog document is eligible, including root/layer/subdirectory
README documents and documents from 07_Creative_Offshoots. Newly cataloged public
documents become selectable without changing Navigator application code.

The stored selection identifies a public-catalog document. At runtime, its
JA/EN counterpart is resolved to the reader's UI language when a counterpart
exists. The same language family cannot be duplicated inside one channel.
Editorial selection does not change titles, publication eligibility, claim
strength, authority, registration state, or canonical metadata.

A future `popular` or personalized channel requires real observations, a defined
measurement, and a privacy/retention decision. Graph centrality, claim strength,
layer placement, editor choice, or fabricated counters must not be presented as
popularity.

### Developer editorial transaction

Developer Navigator provides a Reading editor. It lists every document in the
current Public catalog, including README documents, and lets the developer:

- enable/disable a configured reading channel;
- select documents;
- reorder or remove selected documents;
- filter the full catalog by readable title, document type, or path;
- export/import `navigator_editorial_selection/0.1` JSON.

Browser state is non-canonical and never writes `navigator/public-content.json`
directly. The exported transaction contains an exact `before` binding to the
current `reading_channels` and a proposed `after` value. Repository-side tools
validate that binding and allow only `enabled` and `documents` to change:

```text
Developer Reading editor
  -> navigator_editorial_selection.json
  -> scripts/validate_navigator_editorial_selection.py
  -> scripts/apply_navigator_editorial_selection.py       # dry-run
  -> scripts/apply_navigator_editorial_selection.py --apply
  -> navigator/public-content.json / reading_channels only
```

The validator rejects stale `before` state, unknown document IDs, changed channel
semantics, duplicate document IDs, and duplicate JA/EN families. Apply is
explicit; build, commit, push, and publication remain separate operations.

### Extension boundaries

Reader annotations/reviews and Developer claim assessment are different data and
authority surfaces. Future bookmarks, highlights, notes, and reader reviews must
not mutate canonical metadata or approve S/E. Stable document identity plus
edition/source context is required before synchronized annotations are added;
orphaned notes should be preserved when source text changes instead of silently
reattaching to different prose.

Recommendation sources should remain distinguishable: editor-selected, relation-
based, intentionally distant, popularity-based, and personalized recommendations
are not interchangeable. No graph edge is not proof of conceptual unrelatedness.
Reader notes are not implicit consent for personalized recommendation.

Reader-facing prose in 07 can be used as an entrance, but the recommendation
system is layer-agnostic. A less formal document does not become a canonical
definition merely because it is featured.

### Checks

```text
tsc -p navigator/tsconfig.json
node scripts/check_navigator_reading.mjs
python scripts/check_navigator_interface.py
node scripts/check_navigator_language_resolution.mjs
python scripts/check_registration_workbench.py
python scripts/serve_navigator.py --check
python scripts/build_public_site.py
python scripts/check_public_site.py
python scripts/build_public_site.py --check
```

Repository-side editorial transaction checks:

```text
python scripts/validate_navigator_editorial_selection.py navigator_editorial_selection.json
python scripts/apply_navigator_editorial_selection.py navigator_editorial_selection.json
# explicit apply only after reviewing dry-run:
python scripts/apply_navigator_editorial_selection.py navigator_editorial_selection.json --apply
```

Optional local browser fixtures:

```text
python scripts/check_navigator_reader_browser.py --browser <chromium-executable>
```

The browser fixture uses the real HTML/CSS/compiled modules with explicit local
fetch/storage/clipboard test doubles. It verifies Public metadata masking,
localized title presentation, single-language fallback, reading themes, selected-
text search, mobile layout, and Developer selection from the complete Public
catalog. It also runs a self-contained KaTeX CSS/runtime acceptance fixture that
checks single visual rendering, accessible MathML retention, `trust: false`,
selector non-leakage, inline/display layout, mobile overflow, and print behavior.
Font-path closure and absence of remote CSS assets are checked statically by
`check_navigator_interface.py`. It does not validate HTTP deployment or real
browser-storage persistence; served-page acceptance remains a separate local
check.

## v5.1 frozen metadata projection boundary

Metadata flows only as `docs_manifest.yml -> docs_index.json -> public catalog -> Reader`. Source headers may be hidden by recognizing their display keys but are not a runtime metadata source. The body is not rewritten or rescored for display.

Public projection uses allowlists. Unreviewed/hold assessment state may be shown, but candidate scores, raw audit records, evidence hashes, confidence, reviewer notes and reinvestigation prompts are not public fields. Only an explicitly approved, source-bound representative and explicitly reviewed local hotspots may carry S/E. A source's older header S/E is not promoted through this path.

Developer registration remains `preview -> explicit review export -> validation -> dry-run -> explicit apply`. A metadata approval is not an assessment approval. Local runner POST calls are not canonical writes; browser-to-manifest writes remain forbidden. CLI and GUI exports use the same existing review schema; no second metadata owner is introduced.

The optional metadata panel, direct source display and default reading are distinct. Public masking must preserve subtitle and prose. Language switching must follow declared counterpart identity rather than merely identical filenames. `full`, `partial` and `digest` must not collapse into one completion state.

Freeze verification: `check_navigator_interface.py`, `check_navigator_language_resolution.mjs`, `check_navigator_reading.mjs`, `check_navigator_reader_browser.py`, and `check_document_contract.py`. The interface/reading checks also verify the local KaTeX runtime, stylesheet/font closure, delimiter parsing, and raw-TeX fallback contract. Count assertions derive from the current catalog; author-retired fixtures are excluded explicitly. This freeze does not certify every possible user interaction or future browser version.

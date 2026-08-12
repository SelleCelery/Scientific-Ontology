# Navigator Public / Developer Interface Contract

> Status: Repository governance contract
> Track: Document Navigation Infrastructure
> Stage: DN-5.4A / DN-5.4B
> Scope: public Navigator / developer Navigator / data boundaries / release handoff

## 1. Purpose

The Navigator has two different responsibilities that must not be collapsed into one visible interface.

```text
Public Navigator
  = read, find, and traverse the public document system

Developer Navigator
  = inspect, review, and maintain the data that will later feed the public system
```

The public interface is a release-facing artifact. The developer interface is repository-maintenance tooling.

Both may share implementation code and the same canonical document/search/graph contracts, but public runtime behavior must not require developer-only candidate or audit data.

## 2. Public Navigator contract

Default entry:

```text
/navigator/
```

The public surface exposes only reader-facing functions:

```text
Home / Read
  - system-layer introductions
  - layer README entry points
  - guide-document entry points
  - topic and starter-question entry points

Search
  - explainable direct-relevance search
  - no graph-centrality ranking

Relation Map
  - typed one-hop relations
  - relation direction remains explicit
  - relation != truth / observed link != ownership

Reader
  - strict UTF-8 Markdown reading
  - links back to relations and nearby documents
```

The Reader is a detail view reached from the public surfaces, not a permanent top-level tab.

The public surface must not expose as ordinary reader UI:

```text
candidate review state
candidate confidence
manifest hashes
registration diagnostics
observed-vs-registered maintenance counts
private/process paths
review controls
manifest apply controls
internal release-process markers
```

A local release-preparation build may display a compact `preview` notice when its generated public read model is not yet `visibility_profile: public`, but it must not expose the underlying manifest hash or candidate ledger through that notice.

## 3. Developer Navigator contract

Development entry during DN-5.x:

```text
/navigator/dev.html
```

The developer surface may add maintenance information and controls on top of the same reader/search/relation base.

DN-5.4A established the inspection surfaces:

```text
Candidate Review
Data Audit
registered / observed state
candidate evidence and confidence
search / graph maintenance diagnostics
```

DN-5.4B adds the Developer Registration Workbench on that surface:

```text
approve / approve-with-edits / hold / reject
local review progress
review JSON export / import
manual candidate queue
registered-document revision queue
stale-source refusal
Python validation and manifest dry-run / explicit apply
```

The browser itself still has no manifest write API. It produces an explicit review transaction. Canonical manifest application occurs only through repository-side tooling after validation.

## 4. Data boundary

Public runtime inputs:

```text
tools/docs_index.json
  = generated document/search read model

tools/docs_graph.json
  = generated typed-relation read model

navigator/public-content.json
  = reader-facing presentation copy for layer and guide entrances
```

Developer-only runtime inputs may additionally include:

```text
tools/docs_registration_candidates.preview.json
browser-local registration review state
imported / exported registration review transactions
candidate / audit diagnostics
```

The default public Navigator must not fetch the candidate-preview artifact.

`navigator/public-content.json` is presentation metadata, not a concept-definition owner. It may summarize an existing layer README or explain why a guide document is useful, but it must not create theory claims, concept ownership, or search associations.

## 5. Canonical flow

Developer output is not copied manually into a second public database.

```text
Observed documents
    ↓
Candidate data
    ↓ human review
Canonical docs_manifest.yml
    ↓
    ├─ build_docs_index.py → docs_index.json
    └─ build_docs_graph.py → docs_graph.json
                           ↓
                    Public Navigator
```

Candidate metadata reaches the public Navigator only after an explicit accepted change has entered the canonical manifest or another public source owned by the existing architecture.

## 6. Public information architecture

The public Navigator uses four reader-facing capabilities.

### 6.1 Home / Read

The home surface answers `Where can I start?` without requiring the reader to know repository terminology.

It combines:

- system layers and their README entrances;
- guide documents and the purpose for reading each one;
- controlled topics and starter questions as compact secondary entrances;
- a prominent search box.

The old standalone `Explore` tab is therefore folded into Home / Read. Topic discovery remains available but does not need to present itself as a separate subsystem.

### 6.2 Search

Search continues to use the DN-3 explainable score contract. The public UI may translate field/method names into reader-facing labels, but the underlying score contributions remain inspectable.

### 6.3 Relation Map

The public relation map prioritizes legibility over exposing internal IDs. Relation labels may be rendered in reader-facing language while preserving the exact relation type in the generated graph.

### 6.4 Reader

The Reader remains the normal document-reading path. Raw Markdown is a secondary source/authoring route rather than the primary public path.

## 7. Public layer pages

A layer page should present:

```text
layer name
short role / invitation
README entry
currently registered public-navigation documents
related topic entrances when available
```

Observed-only and candidate documents are not presented as a separate public maintenance category. During development they remain inspectable from the developer surface.

Layer-introduction copy is derived from the corresponding layer README and maintained in `navigator/public-content.json` for concise reader-facing presentation.

## 8. Guide-document pages

Guide cards answer `Why would I read this?` rather than only exposing filenames.

Initial guide entrances:

- repository README;
- Scientific Ontology Operational Outline;
- Scientific Ontology System Map;
- Scientific Ontology Concept Network;
- Glossary.

The list may grow later, but it must remain an editorial entrance rather than a duplicate complete file registry.

## 9. Release boundary for DN-6

DN-6 should treat the Public Navigator as a release artifact and verify at minimum:

```text
public visibility profile only
no candidate-preview dependency
no developer/audit surface in the public entry
no private/process path leakage
UTF-8 strict Reader boundary
stale index check PASS
stale graph check PASS
search regression PASS
relation graph regression PASS
public-content paths exist and are readable
broken public navigation links absent
```

The Developer Navigator is maintenance tooling and does not need to be included in the final public release package. If it is included in a repository distribution, it must remain clearly separated from the default public entry.

## 10. Non-claims

The Navigator is an interface over repository contracts. Its visual prominence does not create theoretical authority.

```text
reader-friendly copy != canonical definition
search score != truth
relation map != evidence ranking
layer placement != ontological proof
candidate state != public registration
```


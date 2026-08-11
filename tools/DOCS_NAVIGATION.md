# Document Navigation Infrastructure

> Status: Repository governance specification
> Scope: public document navigation / manifest-derived index / explainable search / topic discovery

## 1. Responsibility model

```text
Markdown headers
  = minimum human-facing metadata needed before reading

tools/docs_manifest.yml
  = document identity, public role, typed relations, concept ownership,
    and curated document-level discovery metadata

tools/docs_search.yml
  = search behavior, controlled topic registry, beginner-facing topic surfaces,
    query expansions, normalization, weights, and thresholds

scripts/build_docs_index.py
  = deterministic compiler

tools/docs_index.json
  = generated read model; never hand-edited

scripts/query_docs.py
  = Python reference client, browse client, and regression runner
```

The later TypeScript/HTML client must consume the same JSON and navigation/search contract. It must not create a second search database.

## 2. Document-level discovery schema

The manifest extension remains limited to:

```yaml
doc_id: stable_lower_snake_case

discovery:
  topics: []
  aliases:
    ja: []
    en: []
  reader_questions:
    ja: []
    en: []
  entry_level: foundation | intermediate | advanced
```

`topics` are controlled navigation categories, not ontological classes. `aliases` are useful entry expressions, not declarations of strict synonymy. `reader_questions` are ordinary questions that the specific document can genuinely help answer.

Do not add generic search keywords. Do not rewrite `scope` or `role` as search-engine prose.

## 3. Topic discovery surface

DN-3.5 makes topic browsing a first-class entry beside free-text search. It addresses readers who know that they want to explore the repository but cannot yet formulate a useful search query.

The root README remains the editorial entrance that explains how to read the project. Topic browsing is an operational entrance inside that public system: it helps a reader choose where to go next. It does not replace the README or become a concept-definition owner.

The intended entry surfaces are therefore:

```text
README     -> understand what kind of project this is
Browse     -> see what can be explored without knowing terminology
Search     -> look for a question or term already in hand
```

A controlled topic may optionally expose beginner-facing browse metadata in `tools/docs_search.yml`:

```yaml
navigation_topics:
  meaning:
    ja: "意味"
    en: "Meaning"
    browse:
      enabled: true
      order: 30
      label:
        ja: "意味・意味生成から入る"
        en: "Start with meaning and meaning formation"
      description:
        ja: "..."
        en: "..."
      starter_questions:
        ja:
          - "意味はどうやって成立するの？"
        en:
          - "How does meaning form?"
```

The base `ja` / `en` labels remain search and filter labels. `browse.label` is presentation text for an entry card and must not silently broaden concept identity.

`starter_questions` and document `reader_questions` have different owners:

```text
starter_questions
  = questions that help a reader enter a topic

reader_questions
  = questions that a specific document can genuinely help answer
```

A topic may appear in several documents, and a document may belong to several topics. This is navigation, not a strict hierarchy or ontology.

A UI may use a `starter_question` as a ready-made search query, but the question remains an entry prompt. It does not become a claim that every document under the topic answers that question.

## 4. Search boundary

```text
search association != conceptual identity
ranking != truth
related != evidence
fuzzy match != concept ownership
```

Query-expansion groups are search-only associations. They do not redefine concepts or document ownership.

Topic browsing does not create a truth ranking. DN-3.5 orders documents inside a topic only by the explicit `entry_level` and stable document identity. Structural authority and centrality are deferred to DN-4.

## 5. Visibility

`preview` includes manifest documents in `public` and `public-candidate` states. `public` includes only `public` documents.

The builder never indexes `planned`, `legacy`, `deprecated`, `000*`, private-core material, Gate/U support artifacts, local workspace paths, or private implementation identifiers.

The tracked prototype index is a preview artifact during release preparation. DN-6 must prevent a preview index from being mistaken for a public release artifact.

## 6. Build and check

```bash
python scripts/build_docs_index.py
python scripts/build_docs_index.py --check
```

The build is deterministic. The JSON contains source hashes and no generation timestamp.

## 7. Query and browse commands

Search and direct navigation:

```bash
python scripts/query_docs.py search "meaning formation"
python scripts/query_docs.py search "AI judgment" --mode question --limit 5
python scripts/query_docs.py find "Literature as Worldmaking"
python scripts/query_docs.py show meaning_generation_model
python scripts/query_docs.py related meaning_generation_model
```

Discovery without a prior query:

```bash
python scripts/query_docs.py browse
python scripts/query_docs.py browse meaning
python scripts/query_docs.py browse language --lang ja
python scripts/query_docs.py topics
```

`browse` with no topic shows only featured topic entry surfaces that currently contain indexed documents. `topics` remains the lower-level registry view.

Use `--json` for machine-readable output. Use `--base-url` only at query time; repository URLs are not embedded into the index.

## 8. Browse output contract

The topic-card view exposes:

```text
topic_id
base label
browse label
description
starter questions
document count
entry-level counts
```

A topic page exposes the same topic metadata plus matching documents with:

```text
doc_id
title
path
role
entry_level
reader_questions
```

This is sufficient for a later static TypeScript/HTML client to render an entry-card -> topic -> document path without introducing another database.

## 9. Result explanation

Each search result includes field, match method, strength, weight, contribution, source text, and activated query-expansion group when applicable. Human output shows the strongest reasons; JSON output keeps the full diagnostic object.

Browse results are not scored as search hits. Their ordering is an explicit navigation rule and remains inspectable.

## 10. Regression checks

```bash
python scripts/query_docs.py test
```

The test runner checks both search regressions and featured-topic browse regressions. Browse tests verify that starter questions exist and that expected seed documents remain reachable from each featured topic.

## 11. Current limitations

DN-3.5 intentionally excludes morphology analyzers, full-text indexing, BM25, embeddings, LLM reranking, graph centrality, link authority, and browser UI. Japanese fuzzy recall remains a bounded character n-gram fallback after exact, containment, curated discovery, and query-expansion paths.

The current topic surface is a seed navigation layer, not a complete classification of the repository.

## 12. Transition from DN-3.5 to DN-4

DN-3.5 established Search / Browse / Topic entry surfaces. DN-4 now adds an inspectable structural relation graph while keeping structural relations distinct from direct query relevance. Numeric centrality and browser rendering remain downstream concerns.

## 13. DN-4 Typed Relation Graph

DN-4 adds a relation graph without changing DN-3 direct search relevance.

```text
tools/docs_manifest.yml
GLOSSARY.md
Scientific_Ontology_System_Map.md
Scientific_Ontology_Concept_Network.ja.md
public Markdown links
        ↓
scripts/build_docs_graph.py
        ↓
tools/docs_graph.json
```

The primary artifact is the graph itself: nodes, typed edges, and provenance. Counts, centrality, importance, or trust scores are not the graph and are not generated in DN-4 v0.1.

The graph keeps these distinctions:

```text
relation != truth
relation != evidence
search relevance != structural relation
observed link != conceptual ownership
multiple provenance records != automatic trust score
```

### 13.1 Node types

- `document`: manifest/index registered public or public-candidate document.
- `observed_document`: existing public Markdown that is visible in repository topology but is not yet registered in the manifest-derived search index. It receives only path-derived observational identity; it does not gain concept ownership, discovery metadata, or canonical identity.
- `concept`: machine-readable concept identifier from ownership/logical contracts.
- `topic`: controlled DN-3.5 navigation topic.
- `layer`: top-level repository layer.
- `glossary_term`: human-facing lexical entry from `GLOSSARY.md`.
- `source_artifact`: structural source such as the Glossary or System Map when it is not represented as a manifest document.

`observed_document` exists so that the graph can preserve actual public Markdown link topology before manifest coverage becomes complete. Promotion into the searchable public ledger still requires explicit manifest work.

### 13.2 Typed edges

Declared manifest relations:

```text
owns
imports
exports
tests
returns_to
delegates
related_to
```

Navigation and placement:

```text
placed_in
belongs_to_topic
```

Observed/structural relations:

```text
links_to
lexical_anchor
definition_owner_reference
generative_source_reference
operationalized_in_reference
contains_term
map_reference
concept_network_reference
```

Every edge keeps provenance, including source type, source path, source location where available, and manifest payload/evidence where present.

If the same semantic edge is supported by several sources, the graph retains several provenance records instead of collapsing them into a scalar confidence value.

### 13.3 Build and inspect

```bash
python scripts/build_docs_graph.py
python scripts/build_docs_graph.py --check
python scripts/query_docs.py graph-test
```

Inspect a one-hop neighborhood:

```bash
python scripts/query_docs.py graph meaning_generation_model
python scripts/query_docs.py graph "Boundary / 境界"
```

Inspect a two-hop subgraph as JSON for a later browser relation map:

```bash
python scripts/query_docs.py graph meaning_generation_model --depth 2 --json
```

Find an inspectable route between nodes:

```bash
python scripts/query_docs.py trace meaning meaning_generation
```

The default trace is undirected for exploration because a reader may move from topic to document to owned concept even when an edge is declared in the opposite direction. `--directed` is available when direction itself is the question.

### 13.4 Coverage diagnostics

DN-4 distinguishes manifest-registered documents from public Markdown observed only through repository structure.

`docs_graph.json` therefore reports:

- observed but unregistered public documents;
- genuinely missing document references;
- unresolved concept IDs;
- references intentionally excluded by private/process boundaries.

Private-core paths are not written into the graph output, including diagnostics.

### 13.5 Metrics remain deferred

DN-4 v0.1 does not calculate PageRank, betweenness, authority, trust, or structural-importance scores.

Such metrics can always be derived later from `nodes + edges`. The reverse is not possible: a count such as `inbound_links: 11` cannot reconstruct which eleven relations produced it.

Therefore the relation map is canonical for DN-4; numeric summaries are optional derived views for later work.

## 14. Next boundary

DN-5 may render `docs_index.json` and `docs_graph.json` through the same TypeScript/HTML navigation client.

The first browser graph should be local and inspectable rather than a full-repository hairball: one selected node, its typed one-hop relations, optional two-hop expansion, provenance inspection, and direct document opening.

Application/tool launch manifests remain a separate future responsibility and are not folded into the document graph in DN-4.

## 14. DN-5 Browser Client and Python / TypeScript parity

DN-5 adds a dependency-free static browser client under `navigator/`.
It consumes the existing generated read models directly:

```text
tools/docs_index.json  ─┐
                        ├─> navigator/dist/app.js -> browser UI
tools/docs_graph.json  ─┘
```

The browser does not create or maintain a second search database. Search, topic browsing, and graph traversal are implemented in TypeScript against the same JSON contracts used by the Python reference client.

### 14.1 Browser surfaces

The first browser client deliberately separates four surfaces:

```text
Explore
  topic cards + repository/system layers

Search
  direct relevance + inspectable match reasons

Relations
  one-hop typed relation map + provenance list

Data audit
  manifest/index/graph coverage and diagnostics
```

`Explore` includes system-layer navigation such as `01_Sat_Truth`, `02_Raj_Beauty`, `03_Tam_Goodness`, applications, and research notes. This is repository placement, not a claim that those folders are a strict ontological hierarchy.

The relation map renders actual typed edges. It does not calculate centrality or turn link counts into importance scores. Observed-but-unregistered Markdown remains visibly distinct from manifest-registered documents.

### 14.2 Data alignment

At runtime the client compares the manifest hash embedded in `docs_index.json` with the manifest hash embedded in `docs_graph.json`. A mismatch is shown as a browser warning rather than silently merging stale artifacts.

The `Data audit` surface exists specifically so that UI inspection can return to the underlying data contract. It exposes registered vs observed-only documents by layer and the graph diagnostics without promoting observed files into canonical document identity.

### 14.3 TypeScript source and tracked JavaScript

```text
navigator/src/search-core.ts
navigator/src/graph-core.ts
navigator/src/app.ts
navigator/dist/*.js
```

The compiled JavaScript is tracked so the static client has no build dependency at runtime. TypeScript is the human-maintained browser reference source.

Rebuild when `navigator/src/*.ts` changes:

```bash
tsc -p navigator/tsconfig.json
```

### 14.4 Python / TypeScript parity

Run:

```bash
node scripts/check_docs_web_parity.mjs
```

The parity runner compares the TypeScript implementation with the Python reference client across:

- all current search regression queries;
- all current topic-browse regressions;
- graph one-hop neighborhoods used by graph regression cases;
- graph trace regression cases.

Parity means implementation equivalence for the current contract and corpus. It is not a claim that JavaScript provides a universal byte-for-byte implementation of Python Unicode `casefold` for every possible future language character. Any future normalization expansion must be added to the cross-client regression corpus before being relied on.

### 14.5 Local preview

Because the client fetches generated JSON and source Markdown rather than embedding copies, open it over HTTP. The preferred server is the repository helper that declares UTF-8 explicitly for text resources:

```bash
python scripts/serve_navigator.py
```

Then open:

```text
http://127.0.0.1:8000/navigator/
```

`python -m http.server 8000` remains usable for the Navigator shell, and the DN-5.1 Reader still performs strict byte-level UTF-8 decoding, but raw Markdown tabs may depend on browser charset inference because the generic server does not guarantee an explicit UTF-8 charset for every Markdown response.

Opening `navigator/index.html` directly through `file://` is not supported because browser fetch restrictions vary.

### 14.6 DN-5 boundary

DN-5 does not:

- add a framework or package-manager dependency;
- introduce a second search index;
- add graph centrality to direct relevance;
- promote observed-only documents into the manifest;
- create application-download or launch registries;
- modify theory prose to make the UI look cleaner.

The UI is intentionally an inspection surface. Data defects or incomplete navigation metadata revealed by the UI should be corrected upstream in the manifest, search config, graph source, Glossary, Map, or theory document that owns them.

## 15. DN-5.1 Reader Boundary

DN-5.1 adds an in-Navigator Markdown Reader so ordinary reading does not depend on a browser guessing the encoding of a raw `.md` response.

The standard path is:

```text
Navigator link
  -> fetch source bytes
  -> TextDecoder("utf-8", { fatal: true })
  -> safe local Markdown rendering
```

The Reader does not silently replacement-decode invalid bytes. A strict UTF-8 failure is presented as an error and the source must be inspected upstream. This preserves the distinction between a readable document and a damaged or incorrectly encoded source.

The Reader accepts only Markdown paths already exposed as `document` or `observed_document` nodes by the current public index/graph boundary. It does not turn an arbitrary repository path into a browser-readable document and it rejects known private/pending path markers.

Document cards now separate:

```text
Read       = Navigator Reader; normal reading path
Raw file   = direct source response; diagnostic/authoring path
```

Internal Markdown links that resolve to another currently exposed document stay inside the Reader. External links remain external. The renderer constructs DOM nodes rather than trusting raw Markdown as HTML.

The local server helper provides explicit text media types such as:

```text
.md    -> text/markdown; charset=utf-8
.html  -> text/html; charset=utf-8
.css   -> text/css; charset=utf-8
.js    -> text/javascript; charset=utf-8
.json  -> application/json; charset=utf-8
.yml   -> text/yaml; charset=utf-8
```

Run the Reader/source-boundary check with:

```bash
python scripts/serve_navigator.py --check
```

This strict-decodes every Markdown document currently exposed by `docs_index.json` / `docs_graph.json` and validates the explicit UTF-8 MIME mappings. It is a source-integrity check for the Reader boundary, not a substitute for the repository's broader public-format/mojibake checker.

DN-5.1 intentionally does not edit theory prose, promote observed documents, add application registries, or treat visual rendering as evidence that source content is correct. UI-discovered content defects still return to the owning data/document layer.

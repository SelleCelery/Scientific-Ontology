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

## 12. Future boundary

DN-4 may add a structural graph using Glossary anchors, System Map placement, Concept Network relations, Markdown links, and typed manifest relations. Structural authority, centrality, corroboration, and change-impact signals must remain distinct from direct query relevance. They may later help arrange topic pages, but must not silently turn navigation prominence into truth or concept ownership.

DN-5 may add a static TypeScript/HTML client. Search, topic cards, topic pages, and golden tests must consume the same `docs_index.json` contract as the Python reference client.

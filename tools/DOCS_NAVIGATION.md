# Document Navigation Infrastructure

> Status: Repository governance specification
> Scope: public document navigation / manifest-derived index / explainable search
> Authority: Operational contract for DN-2 schema and DN-3 reference search prototype

## 1. Responsibility model

```text
Markdown headers
  = minimum human-facing metadata needed before reading

tools/docs_manifest.yml
  = document identity, public role, typed relations, concept ownership,
    and curated discovery metadata

tools/docs_search.yml
  = search behavior, field weights, controlled topics, query expansions,
    normalization, and thresholds

scripts/build_docs_index.py
  = deterministic compiler

tools/docs_index.json
  = generated read model; never hand-edited

scripts/query_docs.py
  = Python reference client and search regression runner
```

The later TypeScript/HTML client must consume the same JSON and search contract. It must not create a second search database.

## 2. Discovery schema

The v0.1 manifest extension is limited to:

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

`topics` are controlled navigation categories, not ontological classes. `aliases` are useful entry expressions, not declarations of strict synonymy. `reader_questions` must be questions the document can genuinely help answer.

Do not add generic search keywords in v0.1. Do not rewrite `scope` or `role` as search-engine prose.

## 3. Search boundary

```text
search association != conceptual identity
ranking != truth
related != evidence
fuzzy match != concept ownership
```

Query-expansion groups are search-only associations. They do not redefine concepts or document ownership.

## 4. Visibility

`preview` includes manifest documents in `public` and `public-candidate` states. `public` includes only `public` documents.

The builder never indexes `planned`, `legacy`, `deprecated`, `000*`, private-core material, Gate/U support artifacts, local workspace paths, or private implementation identifiers.

The tracked prototype index is a preview artifact during release preparation. DN-6 must prevent a preview index from being mistaken for a public release artifact.

## 5. Build and check

```bash
python scripts/build_docs_index.py
python scripts/build_docs_index.py --check
```

The build is deterministic. The JSON contains source hashes and no generation timestamp.

## 6. Query commands

```bash
python scripts/query_docs.py search "meaning formation"
python scripts/query_docs.py search "AI judgment" --mode question --limit 5
python scripts/query_docs.py find "Literature as Worldmaking"
python scripts/query_docs.py show meaning_generation_model
python scripts/query_docs.py related meaning_generation_model
python scripts/query_docs.py topics
python scripts/query_docs.py test
```

Use `--json` for machine-readable results. Use `--base-url` only at query time; repository URLs are not embedded into the index.

## 7. Result explanation

Each search result includes field, match method, strength, weight, contribution, source text, and activated query-expansion group when applicable. Human output shows the strongest reasons; JSON output keeps the full diagnostic object.

## 8. Current limitations

DN-3 intentionally excludes morphology analyzers, full-text indexing, BM25, embeddings, LLM reranking, graph centrality, and browser UI. Japanese fuzzy recall uses bounded character n-grams only after exact, containment, curated discovery, and query-expansion paths.

## 9. Future boundary

DN-4 may add a structural graph using Glossary anchors, System Map placement, Concept Network relations, Markdown links, and typed manifest relations. Structural authority and centrality must remain distinct from direct query relevance.

DN-5 may add a static TypeScript/HTML client. Python and TypeScript must share golden search tests over the same `docs_index.json` contract.

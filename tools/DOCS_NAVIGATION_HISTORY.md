# Document Navigation Infrastructure — Design History

> Status: Historical record / non-normative
>
> Scope: DN-3.5 through DN-6 design transitions
>
> Current authority: [`DOCS_NAVIGATION.md`](./DOCS_NAVIGATION.md)

## 1. Role of this document / この文書の役割

この文書は、存在境界論の文書ナビゲーション基盤が、どの問題を受けてどの境界を追加したかを保持する。

ここにある段階名、旧画面名、将来形の記述は、現在の実行手順ではない。現行の構成、コマンド、責任分界は `DOCS_NAVIGATION.md` を正本とする。

完全な旧文面、個々のdiff、当時の実装細部はGit履歴が保持する。この文書は、それらへ戻るための設計索引である。

## 2. DN-3.5 — Search and topic entrances

### Problem

用語を知る読者だけが検索でき、何を検索すべきか分からない読者の入口が不足していた。

### Introduced

- free-text SearchとTopic Browseの分離
- controlled navigation topics
- beginner-facing `browse.label` とdescription
- topic-owned `starter_questions`
- document-owned `reader_questions`
- explainable search reasons

### Preserved boundary

```text
topic association != ontological class
search ranking      != truth
starter question    != claim that every topic document answers it
```

### Current destination

- `tools/docs_search.yml`
- `tools/docs_manifest.yml > discovery`
- `scripts/query_docs.py`
- Public Navigatorの問い・トピック入口

## 3. DN-4 — Typed relation graph

### Problem

Search relevanceだけでは、文書・概念・層・用語の構造関係とprovenanceを保持できなかった。

### Introduced

- typed nodes and edges
- manifest-declared relations
- observed Markdown topology
- provenance-preserving edge records
- graph query and trace
- coverage diagnostics

### Deferred

- PageRank
- betweenness
- authority/trust score
- relation countからのimportance inference

### Current destination

- `scripts/build_docs_graph.py`
- `tools/docs_graph.json`
- `scripts/build_public_graph.py`
- `tools/docs_public_graph.json`
- Relation Map

## 4. DN-5 — Browser client and parity

### Problem

Python CLIだけでは公開読解面にならず、別実装を作ると検索・関係契約が分岐する危険があった。

### Introduced

- dependency-free static browser client
- TypeScript source and tracked JavaScript output
- Python/TypeScript parity checks
- Search、topic、graphを同じread modelから表示

### Superseded UI assumption

初期の独立 `Explore` tabは、後にPublicの `Read` へ統合された。

### Current destination

- `navigator/src/*.ts`
- `navigator/dist/*.js`
- `scripts/check_docs_web_parity.mjs`

## 5. DN-5.1 — Reader boundary

### Problem

raw Markdownをブラウザで直接開くと、charset推測やブラウザ差によって読解品質が不安定になった。

### Introduced

- in-Navigator Markdown Reader
- byte fetch + fatal UTF-8 decode
- exposed document pathだけを読むallowlist
- safe DOM construction
- Reader内の内部文書遷移
- explicit UTF-8 media types in local server

### Preserved boundary

```text
visual rendering success != source integrity proof
Reader access             != arbitrary repository access
```

### Current destination

- `navigator/src/app.ts`
- `scripts/serve_navigator.py`
- `python scripts/serve_navigator.py --check`

## 6. DN-5.3 — Registration candidate preview

### Problem

manifest未登録文書の昇格候補を、canonical registrationと混同せずに検討する面が必要だった。

### Introduced

- candidate ledger
- proposed identity、role、scope、layer、discovery metadata
- confidenceとhuman-judgment items
- evidence excerpts
- candidate preview JSON

### Preserved boundary

```text
candidate record != completed human review
candidate role   != theory rewrite
candidate evidence != proof of concept ownership
```

### Current destination

Candidate previewはDeveloper review/audit sourceとして残る。Public runtimeの文書catalogはcandidate previewを直接利用しない。

## 7. DN-5.4A — Public / Developer split

### Problem

読者向けUIとrepository maintenance UIが同じ面にあり、公開情報と診断情報の境界が弱かった。

### Introduced

```text
/navigator/          = Public Navigator
/navigator/dev.html  = Developer Navigator
```

Publicは読解、検索、関係探索を担当し、Developerはcandidate review、Data Audit、maintenance stateを担当する。

詳細契約は `NAVIGATOR_INTERFACE_CONTRACT.md` へ移された。

## 8. DN-5.4B/C — Explicit review transactions

### Problem

ブラウザ上の判断がcanonical manifest更新と曖昧に接続される危険があった。

### Introduced

- approve / approve with edits / hold / reject
- local progress persistence
- explicit review JSON export/import
- validation and dry-run
- explicit repository-side manifest application
- registered document revision proposals

### Preserved boundary

ブラウザはmanifestを直接書き換えない。local stateはcanonicalではない。

### Current destination

- `DOCS_REGISTRATION_WORKBENCH.md`
- registration review schemas and validators
- apply scripts

## 9. DN-5.5 — Provisional documents in canonical manifest

### Problem

Publicで有用な文書がcandidate ledgerにしか存在せず、Public catalogのidentityとreview stateが分離していた。

### Introduced

- `registration_state: provisional`
- registered + provisionalを単一manifestからPublic catalogへ投影
- language counterpart presentation metadata
- registered revision proposalsとprovisional reviewの統合

### Important transition

100件の候補はmanifest-backed canonical identityを得た。これはmetadata review完了や強いtyped relationの付与を意味しない。

### Current destination

- `tools/docs_manifest.yml`
- `scripts/build_public_catalog.py`
- `tools/docs_public_catalog.json`
- unified Developer review pool

## 10. DN-6 — Release integration gate

### Problem

個別buildが成功しても、stale artifact、Public/Developer leakage、language resolution failure、release metadata mismatchが残る可能性があった。

### Introduced

- deterministic freshness checks
- search and graph regressions
- Python/TypeScript parity
- Japanese/English counterpart resolution
- Reader/source boundary check
- Navigator interface check
- release metadata synchronization check
- public-format gate
- expected document/graph counts
- preview and publication modes

### Current destination

- `scripts/check_dn6_release_gate.py`
- `tools/dn6_release_gate.yml`
- `DN6_RELEASE_INTEGRATION.ja.md`
- `DN6_RELEASE_GATE_REPORT.ja.md`

## 11. Superseded statements / 廃止・吸収された記述

次は現行仕様として読まない。

- 「browser UIは将来実装」：実装済み。
- 「DN-5 may render...」：実装済み。
- 独立 `Explore` tab：Public `Read` に統合済み。
- candidate previewがPublic catalogを供給する構成：単一manifest projectionへ移行済み。
- preview artifactを正式公開物として扱う想定：publication gateが拒否する。
- `tsc` が環境に常設されている前提：version-pinned `npx` / `npx.cmd` 手順へ変更。

## 12. Return points / 履歴から現在へ戻る

| Historical question | Current authority |
|---|---|
| 現在のbuild・check手順 | `DOCS_NAVIGATION.md` |
| Public/Developer責任分界 | `NAVIGATOR_INTERFACE_CONTRACT.md` |
| 登録・review作業 | `DOCS_REGISTRATION_WORKBENCH.md` |
| reader questionの基準 | `READER_QUESTION_POLICY.md` |
| DN-6 release gate | `DN6_RELEASE_INTEGRATION.ja.md` |
| Pages artifact | `PUBLIC_SITE_BUILD.ja.md` |

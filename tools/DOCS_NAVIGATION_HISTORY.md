# Document Navigation Infrastructure — Design History

> Status: Historical record / non-normative
>
> Scope: DN-2 through DN-6 design transitions
>
> Current authority: [`DOCS_NAVIGATION.md`](./DOCS_NAVIGATION.md)

## 1. Role of this document / この文書の役割

この文書は、存在境界論の文書ナビゲーション基盤が、どの問題を受けてどの境界を追加したかを保持する。

ここにあるDN段階名、旧画面名、旧件数、将来形の記述は、現在の実行手順ではない。現行の構成、コマンド、責任分界は `DOCS_NAVIGATION.md`、`NAVIGATOR_INTERFACE_CONTRACT.md`、`PUBLIC_SITE_BUILD.ja.md`、各現行schema/config/scriptを正本とする。

完全な旧文面、個々のdiff、当時の実装細部はGit履歴が保持する。この文書は、それらへ戻るための設計索引である。

## 2. DN-2 — Schema contract / 単一台帳と生成read modelの分離

### Problem

文書identity、役割、探索metadataを複数の生成物へ分散させると、どれが人間管理の正本か分からなくなる。

### Introduced

- human-managed `tools/docs_manifest.yml`
- stable `doc_id`
- document role / scope / discovery metadata
- manifestから生成するread model
- generated indexを第二のSSOTにしない原則

### Preserved boundary

```text
manifest = human-managed contract
index    = generated read model

registration != concept ownership
generated artifact != source of truth
```

### Current destination

- `tools/docs_manifest.yml`
- `tools/docs_index.json`
- `scripts/build_docs_index.py`

## 3. DN-3 — Search prototype / 検索可能性と真理判断の分離

### Problem

SO固有語彙を知らない読者が、自然な問いから文書へ入る経路が不足していた。

### Introduced

- `topics`
- `aliases`
- `reader_questions`
- `entry_level`
- search regression tests
- query expansionを検索専用associationとして扱う設計

### Preserved boundary

```text
search association != conceptual identity
ranking            != truth
```

### Current destination

- `tools/docs_search.yml`
- `tools/docs_search_tests.yml`
- `scripts/query_docs.py`

## 4. DN-3.5 — Search and topic entrances

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

## 5. DN-4 — Typed relation graph

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

## 6. DN-5 — Browser client and parity

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

## 7. DN-5.1 — Reader boundary

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

## 8. DN-5.2 — Text normalization / 編集環境差による破損の抑制

### Problem

Windowsを含む複数環境で、改行・encoding・書き戻し方法の差がMarkdownや生成物の不要な差分・文字破損を生み得た。

### Introduced

- repository textのLF基準
- PowerShell script等の必要な例外
- `.gitattributes`による行末契約
- generated writer側での安定した改行出力
- byte-safeな編集・検査を優先する運用

### Historical note

当時は`.editorconfig`も補助的に使ったが、恒久的なSO仕様そのものではない。現在の実効契約はrepository設定と各builder/checkerを正本とする。

## 9. DN-5.3 — Registration candidate preview

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
candidate record   != completed human review
candidate role     != theory rewrite
candidate evidence != proof of concept ownership
```

### Historical transition

Candidate previewは、manifestへ一括昇格する前段のreview surfaceとして導入された。その後、多くのcandidateが`registration_state: provisional`としてmanifest-backed identityを得たため、candidate ledgerを恒久的な現在データとして扱う必要性は低下した。

## 10. Reader question normalization / 問いの責務の明確化

### Problem

candidate reviewを進める過程で、`reader_questions`が要約・同義語・複数論点の詰め合わせへ広がると、検索入口としての責務が曖昧になることが分かった。

### Introduced

基本規則を、原則として「一問 = 一概念、または一つの明示的関係」とした。

### Preserved boundary

```text
reader question != document summary
reader question != synonym dictionary
search-engine quirk != human wording authority
```

### Current destination

- `READER_QUESTION_POLICY.md`

## 11. DN-5.4A — Public / Developer split

### Problem

読者向けUIとrepository maintenance UIが同じ面にあり、公開情報と診断情報の境界が弱かった。

### Introduced

```text
/navigator/          = Public Navigator
/navigator/dev.html  = Developer Navigator
```

Publicは読解、検索、関係探索を担当し、Developerはreview、Data Audit、maintenance stateを担当する。

詳細契約は `NAVIGATOR_INTERFACE_CONTRACT.md` へ移された。

## 12. DN-5.4B/C — Explicit review transactions

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

ブラウザ上のlocal stateはcanonicalではない。review approvalも、それ自体ではmanifest writeではない。

### Current destination

- `DOCS_REGISTRATION_WORKBENCH.md`
- registration review schemas and validators
- apply scripts

## 13. DN-5.5 — Provisional documents in canonical manifest

### Problem

Publicで有用な文書がcandidate ledgerにしか存在せず、Public catalogのidentityとreview stateが分離していた。

### Introduced

- `registration_state: provisional`
- registered + provisionalを単一manifestからPublic catalogへ投影
- language counterpart presentation metadata
- registered revision proposalsとprovisional reviewの統合

### Important transition

候補文書はmanifest-backed canonical identityを得た。これはmetadata review完了や強いtyped relationの付与を意味しない。

### Preserved boundary

```text
canonical identity != concept ownership
provisional         != low quality
registration        != strong relation approval
```

### Current destination

- `tools/docs_manifest.yml`
- `scripts/build_public_catalog.py`
- `tools/docs_public_catalog.json`
- Developer review surface

## 14. DN-5.5A — JA/EN presentation resolution

### Problem

JA/ENのcanonical document identityを保ったままPublic UIを切り替えると、UI言語と異なる本文へ遷移したり、同一内容のcounterpartが二重表示されたりする場合があった。

### Introduced

- JA/EN canonical identityの維持
- presentation familyとしてのcounterpart grouping
- UI languageに適合するvariantの優先
- counterpartがない場合のsingle-language fallback
- Read / Search / Browse / Relations / language switchで同じ解決規則を使用

### Preserved boundary

```text
presentation grouping != canonical identity merge
UI language           != source-language rewrite
```

### Current destination

- `NAVIGATOR_INTERFACE_CONTRACT.md`
- `scripts/check_navigator_language_resolution.mjs`

## 15. DN-6 — Release integration boundary

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
- expected inventory/graph sanity checks
- Public catalog / Public graph sanitation
- release-candidate modeとpublication modeの分離
- known warning debtの上限管理

### Preserved boundary

```text
release-candidate ready != publication complete
known warning debt       != resolved warning
publication fact         != value inferred by repository tooling
Public read model        != Developer diagnostics
```

### Historical reason for the warning ceiling

既知warningを「解決済み」と見せずに残しつつ、新規warningや未知warningが黙って増えることを防ぐため、warning codeごとの既知上限をgateで扱う設計を採用した。warningが減ることは許容し、未知codeや上限超過はblockする。

### Current destination

- `DOCS_NAVIGATION.md` のbuild/check/release gate節
- `NAVIGATOR_INTERFACE_CONTRACT.md` のPublic/Developer・release boundary
- `PUBLIC_SITE_BUILD.ja.md` の公開artifact契約
- release gate config / checker

## 16. README and Navigator entrance split / 編集入口と運用入口

### Design decision

READMEとNavigatorは競合させない。

```text
README
  = editorial entrance
  = 何を読む体系なのかを示す

Public Navigator
  = operational entrance
  = 実際に読む / 探す / 関係を辿る
```

この役割分離は現在のroot READMEにも反映されている。

## 17. Superseded statements / 廃止・吸収された記述

次は現行仕様として読まない。

- 「browser UIは将来実装」：実装済み。
- 「DN-5 may render...」：実装済み。
- 独立 `Explore` tab：Public `Read` に統合済み。
- candidate previewがPublic catalogを供給する構成：単一manifest projectionへ移行済み。
- candidate ledgerを恒久的な現在データとして扱う想定：v5.1整理対象。
- preview artifactを正式公開物として扱う想定：publication gateが拒否する。
- `tsc` が環境に常設されている前提：version-pinned `npx` / `npx.cmd` 手順へ変更。
- DN-6を恒久的な段階名として扱う想定：release gate機能は残すが、段階番号は将来一般名へ移す。

## 18. v5.0で意図的に未完了とした領域

v5.0ではPublic読解基盤をrelease対象とし、Developer側のmetadata/CMS機能は完成条件から分離した。

当時の持ち越しには、登録reviewのstale-source validation、partial apply reconciliation、統一metadata編集、registered/provisional transition、Markdown headerの機械生成・最小化、content hashによる同期などが含まれた。

これは現行v5.1の作業指示ではなく、「なぜ管理システム系の課題がv5.1へ残ったか」を示す形成史である。現行のv5.1方針は最新のassessment / governance / workbench契約を優先する。

## 19. Return points / 履歴から現在へ戻る

| Historical question | Current authority |
|---|---|
| 現在のbuild・check・release手順 | `DOCS_NAVIGATION.md` |
| Public/Developer責任分界、JA/EN presentation | `NAVIGATOR_INTERFACE_CONTRACT.md` |
| 登録・review作業 | `DOCS_REGISTRATION_WORKBENCH.md` |
| reader questionの基準 | `READER_QUESTION_POLICY.md` |
| Public Pages artifact | `PUBLIC_SITE_BUILD.ja.md` |
| release gateの実装詳細 | 現行release gate config / checker |
| DN-2〜DN-6の形成理由 | この文書 |

## 20. Invariants carried forward / 形成史から残った不変項

```text
search association != conceptual identity
ranking != truth
related != evidence
manifest registration != concept ownership
provisional != low quality
UI presentation != canonical definition
Public read model != source of truth
Developer review != automatic write
release-candidate ready != publication complete
```

DN系は、文書を「自動で正しく分類する装置」ではない。

文書の読みやすさ、探索可能性、関係追跡可能性を高めながら、判断の所有点と返路を残すためのインフラとして形成された。

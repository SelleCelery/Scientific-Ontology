# Document Navigation Infrastructure（DN）進行状況・成果記録

## 0. 文書の目的

本書は、Scientific Ontology v5.0で進めたDocument Navigation Infrastructure（DN）系の開発経路を、開発者が後から再構成できるように記録する。

DN系の目的は単なるUI制作ではない。

```text
文書identity
→ discovery metadata
→ search
→ browse
→ typed relation graph
→ reader
→ public presentation
→ provisional registration
→ release gate
```

を一続きの公開読解基盤として構成することにある。

DN-5後半でDeveloper metadata workbenchも試作したが、v5.0ではPublic利用を本線とし、管理CMSとしての完成はv5.1以降へ分離した。

---

## 1. 全体進行

| Stage | 主題 | 到達状態 |
|---|---|---|
| DN-2 | Schema Contract | 完了 |
| DN-3 | Search Prototype | 完了 |
| DN-3.5 | Discovery Surface / Browse | 完了 |
| DN-4 | Typed Relation Graph | 完了 |
| DN-5 | Browser Client | 完了 |
| DN-5.1 | Reader Boundary / UTF-8 | 完了 |
| DN-5.2 | LF / text normalization | 完了 |
| DN-5.3 | Registration Candidate Preview | 完了 |
| DN-5.4A | Public / Developer Interface Separation | 完了 |
| DN-5.4B | Developer Registration Workbench | 基礎実装済み・完成はv5.1+ |
| DN-5.4C | Provisional Public + Unified Review | Public側完了・Developer残件はv5.1+ |
| DN-5.5 | 100候補のmanifest provisional promotion | 完了 |
| DN-5.5A | Public JA/EN Language Resolution | 完了 |
| DN-6 | Release Integration / Release Gate | v5.0 release-candidate gateとして完了 |

---

## 2. DN-2 — Schema Contract

### 目的

文書ごとのidentity、役割、探索metadataを人間管理の単一台帳へ置く。

Canonical source:

```text
tools/docs_manifest.yml
```

### 成果

- stable `doc_id`
- `topics`
- `aliases`
- `reader_questions`
- `entry_level`
- document relation contract
- generated indexを第二のSSOTにしない原則

初期seedは15文書から開始し、generated preview indexは28文書まで拡張した。

基本原則:

```text
manifest = human-managed contract
index    = generated read model
```

---

## 3. DN-3 — Search Prototype

### 目的

ReaderがSO固有語彙を完全に知っていなくても、自然な問いから文書へ入れる検索面を作る。

主要ファイル:

```text
tools/docs_search.yml
tools/docs_search_tests.yml
tools/docs_index.json
scripts/build_docs_index.py
scripts/query_docs.py
```

### 成果

Search metadataを次へ限定した。

```text
topics
aliases
reader_questions
entry_level
```

Query expansionは検索専用associationであり、concept identityではない。

```text
search association != conceptual identity
ranking != truth
```

Regression:

```text
11/11 PASS
```

---

## 4. DN-3.5 — Discovery Surface

### 問題

検索だけでは、初見readerは「何を検索すればいいか」自体が分からない。

### 解決

```text
README = editorial entrance
Browse = discovery entrance
Search = query entrance
```

Featured topic entrances:

- overview
- boundary
- meaning
- language
- ai
- ethics
- science
- literature

Topic `starter_questions`とdocument `reader_questions`を分離した。

Regression:

```text
Browse 8/8 PASS
Search 11/11 PASS
```

---

## 5. DN-4 — Typed Relation Graph

### 問題

「リンク数」「中心性」だけでは文書関係そのものを表せない。

### 方針

Graph truthを次で定義した。

```text
nodes
+
typed edges
+
provenance
```

Canonical graph:

```text
tools/docs_graph.json
```

主要node type:

- document
- observed_document
- concept
- glossary_term
- topic
- layer
- source_artifact

主要relation:

- owns
- imports
- exports
- tests
- returns_to
- delegates
- links_to
- lexical_anchor
- belongs_to_topic
- placed_in
- definition_owner_reference
- map_reference
- concept_network_reference

初期DN-4時点:

```text
305 nodes
1371 edges
28 document
100 observed_document
```

Graph regression:

```text
9/9 PASS
```

Centralityはsearch relevanceへ混ぜなかった。

---

## 6. DN-5 — Browser Client

### 目的

Python CLIで成立した検索・Browse・Graph contractを、browser上で読者が操作できる形へ投影する。

Runtime:

```text
navigator/
```

初期surface:

- Explore
- Search
- Relations
- Data Audit

後にPublic向け情報設計で再編した。

重要な原則:

```text
browser UI != second search database
TypeScript client == same data contract consumer
```

Python / TypeScript parity testを導入した。

---

## 7. DN-5.1 — Reader Boundary

### 問題

`python -m http.server`等の環境ではMarkdownのcharset推定により、日本語本文がmojibakeする場合があった。

### 解決

- browser Readerで`arrayBuffer`
- `TextDecoder("utf-8", {fatal:true})`
- formal local server `scripts/serve_navigator.py`
- Markdown MIMEに`charset=utf-8`
- private / pending path boundary

結果:

```text
UTF-8 Reader check: 128 files PASS
```

---

## 8. DN-5.2 — LF Normalization

Cross-platform repository text contractを整理した。

- Markdown / YAML / JSON / JS / TS / HTML / CSS等: LF
- PowerShell `.ps1`: CRLF例外
- `.gitattributes`
- `.editorconfig`
- generated writerのLF固定

Windows PowerShell 5.1によるUTF-8破壊を避け、byte-safe Python修正を標準化した。

---

## 9. DN-5.3 — Registration Candidates

### 問題

Graphが100の`observed_document`を認識している一方、manifest/searchは28文書しか持っていなかった。

### 解決

100文書についてcandidate metadataを生成した。

```text
tools/docs_registration_candidates.yml
```

Generated preview:

```text
tools/docs_registration_candidates.preview.json
```

Candidateは当初canonical manifestへ入れず、Developer review対象とした。

```text
candidate != canonical identity
candidate evidence != concept ownership
```

Validation:

```text
100/100 PASS
```

---

## 10. Reader Question normalization

Candidate review過程で、reader questionを短文化しただけでなく、責務を再定義した。

基本規則:

> 一問 = 一概念、または一つの明示的関係

例:

```text
主張強度とは何か
公開レイヤーとは何か
主張強度と公開レイヤーはどう関係するか
```

`reader_questions`を要約や同義語辞書にしない。

検索器のquirkへ人間の文章を最適化しない。

---

## 11. DN-5.4A — Public / Developer Separation

Default entry:

```text
/navigator/
```

Developer entry:

```text
/navigator/dev.html
```

Public top-level:

```text
読む
検索
関係マップ
```

Readerはdetail view。

Developerのみcandidate review / data auditを持つ。

Public presentation copy:

```text
navigator/public-content.json
```

これはpresentation metadataであり、concept ownerではない。

Formal contract:

```text
tools/NAVIGATOR_INTERFACE_CONTRACT.md
```

---

## 12. DN-5.4B — Developer Registration Workbench

Developer側で以下を試作した。

- approve
- approve with edits
- hold
- reject
- role / scope / topics / aliases / reader questions編集
- localStorage autosave
- explicit review JSON export
- import / resume
- manual candidate
- registered revision candidate
- dry-run / explicit manifest apply

Review transaction:

```text
docs_registration_review.json
```

ただし、この系統には次の未完了事項が残った。

- source hash validationがwhole-set単位で粗い
- partial apply後reconciliation未実装
- `ruamel.yaml`依存未統合
- registered revision seedのstale handling

これらはv5.0公開を止めず、v5.1+へ送る判断をした。

---

## 13. DN-5.4C — Provisional Public / Unified Review

Human audit throughputとPublic usefulnessを切り離す方針へ変更した。

仮登録文書をPublic runtimeへ使えるようにしつつ、Developer review内部情報をPublicへ出さない構造を作った。

この時点ではPublic catalogがregistered + provisionalを合成した。

同時に固定navigationを追加した。

```text
Menu
Back
Top
Bottom
Language
```

---

## 14. DN-5.5 — Manifest Provisional Promotion

### 方針転換

CandidateがPublicに使えることを確認した後、100文書をmanifestへcanonical provisional registrationした。

```text
28 registered
100 provisional
= 128 manifest-backed public documents
```

これによりPublic runtimeからcandidate ledger合成を除去した。

```text
docs_manifest.yml
      ↓
docs_index.json
      ↓
docs_public_catalog.json
```

Graphも100 observed_documentをmanifest-backed documentへ昇格した。

Current graph:

```text
305 nodes
1810 edges
observed_unregistered_documents = 0
```

ただし、provisional promotionから`owns / imports / exports / tests / returns_to / delegates`は生成していない。

---

## 15. DN-5.5A — Public Language Resolution

### 問題

EN UIでもJA document identityへ遷移し、日本語本文が開く場合があった。

### 解決

Canonical identityとpresentation groupingを分離した。

```text
canonical JA doc + canonical EN doc
          ↓
Public language family
          ↓
UI languageに適合するvariantを表示
```

対象:

- Browse
- Topic
- Search
- Reader
- language toggle
- Relation Map
- Related documents

Current:

```text
128 canonical documents
39 JA/EN pairs
89 logical presentation entries / UI language
```

Regression:

```text
NAVIGATOR LANGUAGE RESOLUTION PASS
```

---

## 16. DN-6 — Release Integration / Release Gate

DN-6では、Public runtimeとDeveloper runtimeのデータ境界を最終固定した。

### 16.1 Public graph projection

Canonical graphにはbuild provenanceとdiagnosticsが必要だが、Public browserには不要である。

そこで:

```text
docs_graph.json
  = canonical / Developer

docs_public_graph.json
  = Public semantic projection
```

と分離した。

Public graphにはnode/edge semanticsだけを残す。

### 16.2 Public catalog sanitation

Public catalogからsource hashとreview/internal fieldsを除去した。

### 16.3 Release gate automation

```text
tools/dn6_release_gate.yml
scripts/check_dn6_release_gate.py
```

を追加した。

Gateはgenerated artifact freshness、search/graph/language regression、Reader boundary、Public/Developer separation、release metadata、public-format checker、Public data sanitationをまとめて実行する。

### 16.4 Warning debt ceiling

Public-format warningを「解決済み」に見せない。

一方、新規warning増加を黙認しない。

Known warning codeごとに上限を固定し、未知codeまたは上限超過をrelease blockerにした。

### 16.5 Release candidateと実公開の分離

```text
release_candidate gate
  = repository/public interfaceの公開準備確認

publication gate
  = published status + date + version DOI
```

DOIと公開日は外部で確定する事実なので、DN-6は推測しない。

---

## 17. v5.0で成立したDN公開基盤

最終的なPublic data flow:

```text
Public Markdown
      ↓
tools/docs_manifest.yml
  28 registered
 100 provisional
      ↓
  build_docs_index.py
      ↓
tools/docs_index.json
      ↓
  build_public_catalog.py
      ↓
tools/docs_public_catalog.json

Public Markdown / manifest / glossary / maps / links
      ↓
  build_docs_graph.py
      ↓
tools/docs_graph.json
      ↓
  build_public_graph.py
      ↓
tools/docs_public_graph.json

catalog + public graph + public-content
      ↓
Public Navigator
```

Reader-facing operations:

```text
Read
Browse
Search
Relations
JA/EN counterpart resolution
```

---

## 18. v5.1以降のDN開発線

v5.1以降ではDNを「読むための基盤」から「文書metadataを維持するCMS的基盤」へ拡張できる。

候補:

- UI metadata editor
- canonical manifest update transaction
- item-level stale validation
- partial apply reconciliation
- registered/provisional promotion workflow
- Markdown header machine generation
- header schemaの最小化
- body hash / content hash
- metadata/header sync checker

長期方向:

```text
本文はMarkdownとして人間/LLMが書く
        ↓
metadataはcanonical ledgerで管理
        ↓
最終headerはmachine projection
```

Headerは理論本文の意味所有点ではなく、identity / state / synchronization markerへ縮小できる。

---

## 19. 保守者が忘れてはいけない不変項

```text
search association != conceptual identity
ranking != truth
related != evidence
manifest registration != concept ownership
provisional != low quality
UI presentation != canonical definition
Public read model != source of truth
Developer review != automatic write
```

DN系は、文書を「自動で正しく分類する装置」ではない。

文書の読みやすさ、探索可能性、関係追跡可能性を高めながら、判断の所有点と返路を残すためのインフラである。

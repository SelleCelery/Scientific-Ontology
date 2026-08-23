# DN-6 Release Integration / Release Gate 技術仕様

## 0. 目的

DN-6は、新機能を増やす段階ではない。

DN-2〜DN-5.5Aで構築した文書identity、検索、Browse、Typed Relation Graph、Reader、Public Navigator、manifest仮登録、JA/EN解決を、**v5.0の公開候補として一つの検証可能な状態へ固定する**ためのrelease integrationである。

この段階では、Developer Workbenchの完成をv5.0の公開条件にしない。

```text
Public release path
  = v5.0 blocker

Developer metadata/CMS path
  = v5.1+ maintenance path
```

DN-6が保証するのは「既知の課題がすべて解決済み」ということではない。

保証するのは、公開面を壊す機械的な不整合をblockし、残っているwarningを既知の技術負債として明示した状態で、release-candidateを再現可能に判定できることである。

---

## 1. v5.0公開候補の文書状態

Canonical document ledger:

```text
tools/docs_manifest.yml
```

現在の公開候補inventory:

```text
128 public documents
  28 registration_state: registered
 100 registration_state: provisional
```

`provisional`はcanonical ledgerの外にいるという意味ではない。

DN-5.5以降は、100文書もmanifestへ正式にidentityを持つ。ただし、navigation metadataの人間監査が継続中であることを`registration_state: provisional`として記録する。

したがって、v5.0のPublic runtimeはcandidate ledgerを合成しない。

```text
docs_manifest.yml
      ↓
docs_index.json
      ↓
docs_public_catalog.json
      ↓
Public Navigator
```

Candidate ledgerはv5.1以降の監査・修正材料として残す。

---

## 2. Public / Developer runtime data boundary

DN-6では、Public browserへDeveloper用source hashやgraph diagnosticsを渡さないよう、graphを二層化する。

Canonical / Developer graph:

```text
tools/docs_graph.json
```

Public graph projection:

```text
tools/docs_public_graph.json
```

生成経路:

```text
docs_graph.json
      ↓
scripts/build_public_graph.py
      ↓
docs_public_graph.json
```

Public graphに残すもの:

- graph principles
- relation type definitions
- nodes
- typed edges

Public graphから除くもの:

- source hashes
- graph diagnostics

Public runtime:

```text
tools/docs_public_catalog.json
tools/docs_public_graph.json
navigator/public-content.json
```

Developer runtimeは追加で次を使用できる。

```text
tools/docs_graph.json
tools/docs_registration_candidates.preview.json
tools/docs_registered_reader_question_review.preview.json
browser localStorage
```

---

## 3. Public catalog sanitation

`tools/docs_public_catalog.json`は、manifest由来のPublic search/read modelである。

DN-6ではPublic catalogから次を除く。

- `manifest_sha256`
- `search_config_sha256`
- `canonical_index_sha256`
- candidate source hash
- graph source hash
- confidence
- evidence
- `needs_human_judgment`
- review note / decision
- manual/revision candidate transaction data

Publicに残してよいmetadataは、読者が文書を発見・選択・読むために必要なものに限定する。

例:

- title
- path
- role
- scope
- topics
- aliases
- reader questions
- entry level
- registration state
- JA/EN presentation metadata

---

## 4. Provisional registrationの強い関係を自動生成しない

100 provisional文書をmanifestへ入れたことで、graph上のnodeはcanonical `document`になる。

しかし、登録しただけで次のrelationを生成してはならない。

```text
owns
imports
exports
tests
returns_to
delegates
```

DN-6 gateは、provisional文書がこれらのstrong relationのsourceになっていないことを機械検証する。

許容されるのは、既存の根拠から生成されるplacement / topic / Markdown link等である。

```text
canonical identity != concept ownership
manifest registration != theory relation approval
```

---

## 5. JA/EN presentation boundary

Canonical manifest上では、JA文書とEN文書は別document identityを保ってよい。

Public presentationではlanguage familyとしてcollapseし、現在のUI言語に対応するcounterpartを優先する。

EN UI:

```text
EN counterpart exists -> ENを開く
bilingual             -> その文書を開く
JA only               -> JA fallbackを明示
```

JA UIでは逆になる。

Current release-candidate state:

```text
128 canonical documents
39 JA/EN counterpart families
89 logical presentation entries per UI language
```

検証:

```powershell
node scripts/check_navigator_language_resolution.mjs
```

---

## 6. DN-6 Release Gate

Gate設定:

```text
tools/dn6_release_gate.yml
```

Gate runner:

```text
scripts/check_dn6_release_gate.py
```

Public graph builder:

```text
scripts/build_public_graph.py
```

### 6.1 Release-candidate mode

通常のDN-6判定:

```powershell
python scripts/check_dn6_release_gate.py
```

Reportも更新する場合:

```powershell
python scripts/check_dn6_release_gate.py --write-report
```

### 6.2 Publication mode

Zenodo DOIと公開日が実際に確定した後だけ使用する。

```powershell
python scripts/check_dn6_release_gate.py --mode publication
```

Publication modeは追加で:

```text
release.status = published
publication_date != null
version-specific DOI = assigned
```

を要求する。

未確定のDOIや公開日を推測して埋めてはいけない。

---

## 7. Required checks

Release-candidate gateは少なくとも次をblockerとして扱う。

```text
build_docs_index.py --check
build_docs_graph.py --check
build_public_graph.py --check
build_public_catalog.py --check
query_docs.py test
query_docs.py graph-test
check_docs_web_parity.mjs
check_navigator_language_resolution.mjs
serve_navigator.py --check
check_navigator_interface.py
release_update.py --check
check_public_format.py --release-gate --check-release-metadata
```

加えてrunner自身が以下を検証する。

- catalog count = 128
- registered = 28
- provisional = 100
- language-pair families = 39
- graph nodes = 306
- graph edges = 1862
- observed unregistered documents = 0
- Public catalogにDeveloper-only keyがない
- Public graphに`source` / `diagnostics`がない
- Public graphのnodes/edgesがcanonical graphと一致する
- provisional文書にstrong logical relationが自動付与されていない

---

## 8. Public Format warningの扱い

v5.0ではwarningを「全部修正してから公開」としない。

一方、warningを無視もしない。

DN-6ではwarning codeごとに既知の上限を`tools/dn6_release_gate.yml`へ記録する。

Gate policy:

```text
Errors > 0
  -> BLOCK

unknown warning code
  -> BLOCK

known warning count > recorded ceiling
  -> BLOCK

known warning count <= ceiling
  -> PASS with known debt
```

つまり、既存warningは未解決のまま記録しつつ、新しいwarning debtが黙って増えることを防ぐ。

Warningが減ることは許容する。

---

## 9. Release metadata integration

Release-level factsのSSOT:

```text
90_Repository_Governance/Release_Update/release_state.yml
```

同期:

```powershell
python 90_Repository_Governance/Release_Update/release_update.py --check
python 90_Repository_Governance/Release_Update/release_update.py --dry-run
python 90_Repository_Governance/Release_Update/release_update.py --write
```

DN-6ではPublic Navigatorをv5.0 included featureとしてrelease stateへ記録する。

README / Roadmapはhuman-ownedであり、release update scriptが概念本文を書き換えない。

---

## 10. READMEとNavigatorの役割

v5.0では二つを競合させない。

```text
README
  = editorial entrance
  = 何を読む体系なのか

Public Navigator
  = operational entrance
  = 実際に読む / 探す / 関係を辿る
```

Local launch:

```powershell
python scripts/serve_navigator.py
```

```text
http://127.0.0.1:8000/navigator/
```

外部hosting/GitHub Pages構成は、実際のdeployment先が決まらない限りDN-6で推測しない。

---

## 11. v5.1以降へ明示的に持ち越すもの

以下はv5.0 release blockerではない。

- `apply_registration_review.py`のconditional stale-source validation
- candidate-only / registered-revision-only / mixed transaction test
- `ruamel.yaml`のDeveloper依存宣言
- partial apply後のcandidate/revision reconciliation
- Developer UIでの統一metadata編集
- registered/provisional state transition workflow
- Markdown headerの機械生成・同期
- body/content hashによるmetadata同期
- headerの最小化設計

特にheader運用は、将来的に次の方向を推奨する。

```text
人間 / LLM
   ↓
Markdown本文を書く
   ↓
metadata systemがcanonical metadataを保持
   ↓
必要なheaderだけ機械投影
```

Markdown本文をmetadata入力フォームとして酷使しない。

---

## 12. DN-6完了条件

Release-candidateとしてのDN-6完了条件:

```text
[ ] 128 manifest-backed documents
[ ] 28 registered + 100 provisional
[ ] Public catalog fresh
[ ] Public graph fresh / sanitized
[ ] canonical graph fresh
[ ] search 11/11
[ ] browse 8/8
[ ] graph tests 9/9
[ ] Python/TypeScript parity PASS
[ ] JA/EN resolution PASS
[ ] UTF-8 Reader PASS
[ ] Public/Developer boundary PASS
[ ] release metadata sync PASS
[ ] public-format errors = 0
[ ] warning debt does not exceed recorded ceiling
[ ] v5.1 deferred work documented
```

Publicationそのものは別条件である。

```text
release-candidate ready
      !=
Zenodo publication complete
```

版固有DOIと公開日が確定した後、publication modeを通して最終公開する。

# Document Navigation Infrastructure

> Status: Current repository governance specification
>
> Scope: Public Navigator / Developer Navigator / manifest-derived navigation / search / relation graph / Reader
>
> Historical record: [`DOCS_NAVIGATION_HISTORY.md`](./DOCS_NAVIGATION_HISTORY.md)

## 1. Purpose / 目的

この文書は、存在境界論の公開文書ナビゲーションについて、**現在有効な責任分界と実行手順**だけを定める。

設計の変遷、旧DN段階の説明、廃止済みの前提は、現行手順と混在させない。履歴は `DOCS_NAVIGATION_HISTORY.md` に保持する。

文書ナビゲーションは、理論本文とは別の公開インターフェースである。検索順位、関係数、トピック所属、仮登録状態を、真理・重要度・証拠・概念所有へ読み替えてはならない。

```text
search association != conceptual identity
ranking            != truth
related            != evidence
relation count      != importance
provisional         != low quality
```

## 2. Current architecture / 現行構成

```text
Markdown documents + tools/docs_manifest.yml + tools/docs_search.yml
                              │
                              ├─ scripts/build_docs_index.py
                              │      └─ tools/docs_index.json
                              │
                              ├─ scripts/build_docs_graph.py
                              │      └─ tools/docs_graph.json
                              │
                              ├─ scripts/build_public_catalog.py
                              │      └─ tools/docs_public_catalog.json
                              │
                              └─ scripts/build_public_graph.py
                                     └─ tools/docs_public_graph.json

tools/docs_public_catalog.json ─┐
tools/docs_public_graph.json   ─┼─ Public Navigator
navigator/public-content.json  ─┘

tools/docs_index.json                         ─┐
tools/docs_graph.json                         ─┼─ Developer Navigator
registration/review preview artifacts         ─┘
```

TypeScript/HTMLクライアントは、Python側と同じ生成済みread modelを利用する。ブラウザ専用の第二検索データベースを作ってはならない。

## 3. Ownership / 所有点

| File | Owns | Editing rule |
|---|---|---|
| Markdown headers | Legacy/source-local descriptive metadata; not the current assessment authority | Preserve existing source; current metadata belongs to manifest |
| `tools/docs_manifest.yml` | 文書identity、公開役割、配置、型付き関係、概念所有、文書別discovery | canonical。生成物から逆編集しない |
| `tools/docs_search.yml` | controlled topics、検索展開、正規化、重み、閾値、topic入口 | 検索・発見だけを所有する |
| `navigator/public-content.json` | Public Navigatorの接触面・正式入口・作業領域・体系核・案内面の配置、案内文書カード、入口文、編集者選択の読書channel | 理論定義・S/E・検索関連・人気指標を所有しない |
| `tools/docs_index.json` | manifest-derived canonical read model | 生成物。手編集禁止 |
| `tools/docs_graph.json` | canonical typed relation graph | 生成物。手編集禁止 |
| `tools/docs_public_catalog.json` | Public用文書・検索projection | 生成物。手編集禁止 |
| `tools/docs_public_graph.json` | Public用semantic graph projection | 生成物。手編集禁止 |
| `navigator/src/*.ts` | ブラウザ実装の人間管理ソース | 編集対象 |
| `navigator/dist/*.js` | 配信用JavaScript | TypeScriptから生成し、追跡する |

より詳細なPublic/Developer責任分界は [`NAVIGATOR_INTERFACE_CONTRACT.md`](./NAVIGATOR_INTERFACE_CONTRACT.md) が所有する。

## 4. Public and Developer boundary / 公開境界

### 4.1 Public Navigator

```text
/navigator/
```

Public Navigatorは次を提供する。

Repositoryの数値prefixはidentityと保守のために保持するが、Public Navigatorの読書順序には使わない。v5.1では、外向き表現と視覚資料を最上段の接触面、READMEとSystem Mapを正式入口、Applications/Research Notesを作業領域、Truth/Beauty/Goodnessを体系核、Overviewを体系の読み方案内として配置する。

- 編集者が選択できる注目・おすすめ・寄り道の読書channel（READMEを含む全Public文書が候補）
- 読者役割に応じた入口配置（接触面／正式入口／作業領域／体系核／案内）
- 目的別の案内文書
- 問い・トピック・検索からの入口
- 型付き関係の探索
- strict UTF-8 Reader

Public runtimeが読み込めるのは、原則として次の三ファイルである。

```text
tools/docs_public_catalog.json
tools/docs_public_graph.json
navigator/public-content.json
```

Public画面へ次を出してはならない。

- candidate evidence、confidence、review decision
- manifest/source hash
- Developer診断情報
- maintenance ID
- private/pending path
- Developer Navigatorを既定入口にする導線

Publicの初期読書面では、registration state、S/E、Authority、Scope等のrepository metadataを本文より先に表示しない。必要な管理情報はDeveloper側で確認する。

### 4.2 Developer Navigator

```text
/navigator/dev.html
```

Developer Navigatorは次を扱う。

- canonical index/graphの監査
- registration candidate review
- registered document revision proposals
- approve / edit / hold / rejectの作業状態
- 明示的なreview JSON export/import
- manifest反映前のvalidationとdry-run
- Public catalog全文書からの注目・おすすめ・寄り道channel編集
- editorial selection JSONのexport/import（repositoryへは直接書かない）

ブラウザは `tools/docs_manifest.yml` を直接書き換えない。登録作業は [`DOCS_REGISTRATION_WORKBENCH.md`](./DOCS_REGISTRATION_WORKBENCH.md) に従う。

## 5. Document discovery contract / 文書発見契約

manifestの文書別discoveryは、次の範囲に限定する。

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
  visibility: canonical | secondary
  searchable: true
```

- `topics`：ナビゲーション分類。存在論的クラスではない。
- `aliases`：検索入口。厳密な同義宣言ではない。
- `reader_questions`：その文書が実際に応答可能な問い。
- `entry_level`：読解入口の深さ。重要度や権威ではない。
- `visibility`：Public表示上の配置。
- `searchable`：検索対象の可否。

一般的なSEOキーワードを追加してはならない。`scope` や `role` を検索用宣伝文へ書き換えてはならない。

## 6. Topic and search contract / トピックと検索

`tools/docs_search.yml` のcontrolled topicは、用語を知らない読者の入口を作る。

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

```text
starter_questions = topicへ入るための問い
reader_questions  = 特定文書が応答可能な問い
```

検索結果は、field、match method、strength、weight、contribution、source text、query expansionを説明可能な形で保持する。検索結果の順位を、真理・中心性・証拠強度へ変換してはならない。

## 7. Typed relation graph / 型付き関係グラフ

主なnode type：

- `document`
- `observed_document`
- `concept`
- `topic`
- `layer`
- `glossary_term`
- `source_artifact`

主なedge type：

```text
owns
imports
exports
tests
returns_to
delegates
related_to
placed_in
belongs_to_topic
links_to
lexical_anchor
definition_owner_reference
generative_source_reference
operationalized_in_reference
contains_term
map_reference
concept_network_reference
```

すべてのedgeはprovenanceを保持する。同じ意味関係に複数の根拠源があっても、単一のtrust scoreへ圧縮しない。

relation graphは関係を保持する。PageRank、betweenness、authority、trust、importance scoreはcanonical graphの責任ではない。

## 8. Visibility profiles / 可視性プロファイル

| Profile | Included documents | Use |
|---|---|---|
| `preview` | `public` + `public-candidate` | release preparation |
| `public` | publication cutで公開対象と確定した文書 | published release |

生成器は、`planned`、`legacy`、`deprecated`、`000*`、private core、Gate/U支援物、ローカルパス、非公開実装識別子をPublic indexへ入れてはならない。

Public shellが `preview` を読む場合は、公開準備中であることを短く表示する。正式公開物では `public` profileを使用し、DN-6 publication gateで検証する。

## 9. Build / 生成

リポジトリルートで実行する。

### 9.1 Preview read models

```powershell
python scripts/build_docs_index.py --visibility preview
python scripts/build_docs_graph.py --visibility preview
python scripts/build_public_catalog.py
python scripts/build_public_graph.py
```

### 9.2 Publication read models

```powershell
python scripts/build_docs_index.py --visibility public
python scripts/build_docs_graph.py --visibility public
python scripts/build_public_catalog.py
python scripts/build_public_graph.py
```

### 9.3 TypeScript build

`navigator/src/*.ts` を変更した場合は、`navigator/dist/*.js` を再生成する。

Linux、macOS、GitHub Actions：

```bash
npx --yes --package=typescript@5.8.3 -- tsc -p navigator/tsconfig.json
```

Windows PowerShell：

```powershell
npx.cmd --yes --package=typescript@5.8.3 -- tsc -p navigator/tsconfig.json
```

PowerShellでは `npx` が `npx.ps1` に解決され、ローカルExecution Policyによって拒否されることがある。`npx.cmd` を使用すれば、システム全体のExecution Policyを変更する必要はない。

生成後、`navigator/src` と `navigator/dist` の対応をdiffで確認する。

## 10. Check / 検査

### 10.1 Generated read-model checks

Preview：

```powershell
python scripts/build_docs_index.py --visibility preview --check
python scripts/build_docs_graph.py --visibility preview --check
python scripts/build_public_catalog.py --check
python scripts/build_public_graph.py --check
```

Publication：

```powershell
python scripts/build_docs_index.py --visibility public --check
python scripts/build_docs_graph.py --visibility public --check
python scripts/build_public_catalog.py --check
python scripts/build_public_graph.py --check
```

### 10.2 Regression and boundary checks

```powershell
python scripts/query_docs.py test
python scripts/query_docs.py graph-test
node scripts/check_docs_web_parity.mjs
node scripts/check_navigator_language_resolution.mjs
python scripts/serve_navigator.py --check
python scripts/check_navigator_interface.py
```

Windows PowerShellで `node` 自体が利用できない場合はNode.jsの導入を確認する。`npx.ps1` のExecution Policy問題とは分けて扱う。

### 10.3 Release gates

Release candidate：

```powershell
python scripts/check_dn6_release_gate.py --mode release_candidate
```

Publication：

```powershell
python scripts/check_dn6_release_gate.py --mode publication
```

publication modeは、公開日、版固有DOI、`release.status: published`、公開用read model、Public/Developer境界を追加検査する。

Release gateは既知warningを「解決済み」とは扱わない。既知codeごとの許容上限以内であれば技術負債として明示的に保持し、未知warningまたは既知上限の超過はblockする。warningが減ることは許容する。

```text
release-candidate ready != publication complete
known warning debt       != resolved warning
```

## 11. Query and inspection / CLI確認

検索：

```powershell
python scripts/query_docs.py search "meaning formation"
python scripts/query_docs.py search "AI judgment" --mode question --limit 5
python scripts/query_docs.py find "Literature as Worldmaking"
python scripts/query_docs.py show meaning_generation_model
python scripts/query_docs.py related meaning_generation_model
```

トピック：

```powershell
python scripts/query_docs.py browse
python scripts/query_docs.py browse meaning
python scripts/query_docs.py browse language --lang ja
python scripts/query_docs.py topics
```

関係グラフ：

```powershell
python scripts/query_docs.py graph meaning_generation_model
python scripts/query_docs.py graph "Boundary / 境界"
python scripts/query_docs.py graph meaning_generation_model --depth 2 --json
python scripts/query_docs.py trace meaning meaning_generation
```

機械可読出力には `--json` を使う。URLはquery時の `--base-url` で与え、生成indexへ埋め込まない。

## 12. Local preview / ローカル確認

NavigatorはJSONとMarkdownをfetchするため、`file://` で直接開かない。

```powershell
python scripts/serve_navigator.py
```

Public Navigator：

```text
http://127.0.0.1:8000/navigator/
```

Developer Navigator：

```text
http://127.0.0.1:8000/navigator/dev.html
```

`serve_navigator.py` はMarkdown、HTML、CSS、JavaScript、JSON、YAMLへ明示的なUTF-8 media typeを与える。Readerは `TextDecoder("utf-8", { fatal: true })` を使用し、不正なbyte列をreplacement decodeしない。

## 13. Registration and review / 登録・レビュー

Public catalogは、manifestにある `registered` と `provisional` の両方を扱える。

```text
provisional registration
  -> human metadata review
  -> explicit review transaction
  -> repository-side validation / apply
  -> registered または provisional維持
```

仮登録文書のcanonical identityは、すでに `tools/docs_manifest.yml` にある。Developer Navigatorはmanifestをread sourceとして利用してよいが、ブラウザから直接書き込まない。

Developer reviewは次の一つのread modelへ集約する。

```text
tools/docs_manifest.yml --------------------┐
                                             ├─> scripts/build_registration_workbench_preview.py
tools/docs_revision_proposals.yml ----------┘
                                                   ↓
                                  tools/docs_registration_workbench.preview.json
```

preview JSONは生成物であり、手編集しない。ブラウザのlocal stateもcanonicalではない。export、repository-side validation、dry-run、明示的manifest適用を経て初めてcanonical変更となる。

登録済み文書の改訂提案はgenericな `docs_revision_proposals.yml` に保持し、一回限りのreview seedを恒久inputにはしない。

詳細は次を参照する。

- [`DOCS_REGISTRATION_WORKBENCH.md`](./DOCS_REGISTRATION_WORKBENCH.md)
- [`READER_QUESTION_POLICY.md`](./READER_QUESTION_POLICY.md)

## 14. Change routing / どこを直すか

| Observed problem | Return to |
|---|---|
| title、status、scope、role、配置 | owning Markdown / `docs_manifest.yml` |
| topic、alias、reader question | `docs_manifest.yml` または `docs_search.yml` |
| concept ownership、typed relation | `docs_manifest.yml`、Glossary、System Map、Concept Network |
| Public入口文、層説明、guide card、読書channel | `navigator/public-content.json`（channel文書選択はDeveloper editor→明示的repository-side applyでも更新可） |
| Search/graph behavior | `navigator/src/*-core.ts` とPython reference implementation |
| UI layout、Reader、route | `navigator/src/app.ts` |
| PublicにDeveloper情報が出る | projection builder / interface boundary |
| 文字化け、UTF-8 failure | source Markdownまたは配信media type |
| generated JSON/JSの差分 | source/configへ戻して再生成 |

UIをきれいに見せるために、理論本文やcanonical metadataを下流から書き換えてはならない。

## 15. Current non-goals / 非目的

現行基盤は次をcanonical責任にしない。

- search rankingをtruth、authority、importanceへ変換すること
- graph centralityやtrust scoreをcanonical dataへ埋め込むこと
- embeddingまたはLLM rerankingを無検査で導入すること
- Public Navigatorからmanifestを直接更新すること
- candidate evidenceをPublicへ公開すること
- UI都合で理論本文を変更すること
- application/download/launch registryをdocument graphへ混在させること

新しい検索・正規化・言語処理を導入する場合は、Python/TypeScript双方へ実装し、回帰corpusへ追加してから利用する。

## 16. Related contracts / 関連文書

- [`NAVIGATOR_INTERFACE_CONTRACT.md`](./NAVIGATOR_INTERFACE_CONTRACT.md)
- [`DOCS_REGISTRATION_WORKBENCH.md`](./DOCS_REGISTRATION_WORKBENCH.md)
- [`READER_QUESTION_POLICY.md`](./READER_QUESTION_POLICY.md)
- [`PUBLIC_SITE_BUILD.ja.md`](./PUBLIC_SITE_BUILD.ja.md)
- [`DOCS_NAVIGATION_HISTORY.md`](./DOCS_NAVIGATION_HISTORY.md)

## 17. v5.1 metadata ownership and feature freeze

`tools/docs_manifest.yml` with `metadata_contract: document-contract/1.0` is the current owner of identity, placement, document role, language relation, catalog membership and approved assessment summary. `tools/docs_manifest.schema.json` and `scripts/validate_docs_manifest.py` implement this contract.

- `state` remains publication availability, not maturity, validity or assessment approval. `registration_state` remains provisional/registered. `document_role` describes function. None is inferred from the other.
- `discovery.primary_question` is an explicit language-keyed field; null means not selected. Existing `reader_questions` and 28 active revision proposals are retained, not silently approved. Search terms come from existing `topics` and `aliases`, not a new competing header field.
- `language_relation` distinguishes authority, full/partial commensuration, integrated bilingual text, digest and support. The joint root-README interface is the only coauthority exception. A paired English document is not independently re-scored.
- `managed_assets` holds fixed research sources, evidence, historical supports and internal supports. These are not catalog documents and receive no current claim profile. Exact-byte sources are checked against the specified source binding. A current snapshot hash does not repair or certify a historical manifest.
- `retired_documents` records author retirement and superseded paths. A retired current path cannot be restored merely to pass a build. A moved document keeps its surviving identity.
- `external_artifacts` and `artifact_relations` provide typed reference edges only: operationalized_in, implemented_as, archived_at. They are not a software launcher, download manager, or proof relation. Live availability is not implied by a supplied URL.

Legacy S/E/P/V labels remain provenance rather than values converted into the new scale. New assessments remain unreviewed or hold until explicitly reviewed. Hotspot values never determine the representative score by maximum or average.

The Public reader hides recognized source header blocks as a presentation operation. It does not parse them into assessment metadata. Optional collapsed metadata after the text is read only from the sanitized generated catalog. The original Markdown and Developer reading remain available; this is not a confidentiality boundary.

The v5.1 UI scope is frozen at existing reading/search/graph/language/theme functions, existing registration/assessment review surfaces, and the optional read-model metadata panel. No new evaluation CMS, automatic claim assessor or forced language translation is part of this freeze.

Rebuild current projections using `python scripts/rebuild_document_read_models.py`. It builds locally from current canonical inputs, verifies the public artifact, and restores derived outputs on failure. Do not copy hash-bound read models from an older AI snapshot. A successful local build is not release approval.

Two Volume I CSV assets had CRLF working-copy bytes but LF blobs already stored in rc004 HEAD. Their metadata preserves the original snapshot digest and an explicitly bound `git_lf_sha256`, verified to differ only in line endings. Only these declared provenance assets accept those two exact representations; other modifications fail. Fixed Optional Axiom source remains strictly exact-byte. Historical MANIFEST values are neither normalized nor reissued.

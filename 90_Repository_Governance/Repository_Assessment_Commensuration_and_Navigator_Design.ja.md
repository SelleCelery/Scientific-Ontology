# Repository Assessment, Commensuration, and Navigator Design
# 文書評価・通約・Navigator再編の設計ノート

> Layer: 90_Repository_Governance
> Status: Working Design Note
> Role: Governance design / migration rationale
> Maturity: Working draft; candidate metadata, not yet governed by Metadata Assessment Policy
> Scope: document metadata / assessment history / commensuration / language-game interfaces / manifest / Navigator / header projection / return paths
> Language: Japanese authoritative; English commensuration not yet planned
> Authority: None. This document records the current design direction and does not replace existing policies, canonical theory documents, or domain authority.
> Baseline: Scientific Ontology Public Edition v5.0.0 plus post-release working changes, inspected 2026-08-21

---

## 0. この文書の目的

本文書は、存在境界論そのものの新しい理論を定義するための文書ではない。

目的は、公開リポジトリにおける文書評価、通約、評価履歴、機械可読メタデータ、Markdownヘッダー、Navigator、公開・開発インターフェースの関係を整理し、今後の改修で何を一つの尺度へ圧縮し、何を履歴として保持するかを明示することである。

今回の改修では、既存の `Claim_Strength_and_Publication_Layer_Table`、`Publication_and_Commensuration_Policy`、`docs_manifest.yml`、Public / Developer Navigator、言語・意味・通信位相研究から得られた知見を一つの文書へ統合し直すこと自体を目的としない。

むしろ、それぞれの責務を分離し、次の状態へ移行するための設計基準点を置く。

```text
Document body
  = 内容の正本または研究本文

Governance policies
  = 評価基準・公開・通約・変更権限

Canonical metadata ledger
  = 文書ごとの現在状態

Evaluation history
  = 実際に何を、いつ、なぜ、どう評価したか

Generated projections
  = Markdown header / index / graph / Navigator / public catalog
```

本文書自体も監査対象であり、後続の実装・評価によって修正、分割、廃止できる。

---

## 1. 現在の問題

### 1.1 一つの `Status` が複数の意味を背負っている

現行文書では、`Policy`、`Model`、`Foundational principle`、`First Draft`、`README` などが同じ `Status` 欄へ入る場合がある。

しかし、これらは同じ問いへ答えていない。

- 文書はいま運用上有効か。
- 文書は何の役割を持つか。
- 文書の記述はどこまで安定しているか。
- 文書はどの程度強い主張を行うか。
- どの検査を受けたか。

これらを一つの欄へ入れると、たとえば「基底原則である」と「文章が成熟している」が暗黙に同一視される。

### 1.2 Claim Strength と Verification が別種の情報を圧縮している

Claim Strength は、命題がどの程度強いコミットメントを行うかを短く表示するために有用である。

一方、現行の Verification Stage は、概念整合、反例照合、Toy Model、実地評価、数理化、外部予測比較など異質な検査を一列へ並べている。

対象領域によって必要な検査は異なる。倫理モデル、通約プロトコル、数学的構成、物理近接仮説、AI運用では、同じ順序で検証が進むとは限らない。

したがって、Verification を単一コードへ縮約すると、検査内容そのものより一覧表示が優先される危険がある。

### 1.3 Publication and Commensuration Policy が責務を抱えすぎている

現行Policyは、正本言語、英語通約、概念所有、主張強度、公開レイヤー、Rendering Distance、用語衝突、非主張境界、private boundary、manifestとの関係まで広く扱っている。

このまま各思想、学派、専門分野、言語ゲームを追加分類すると、Policyが対象領域の百科事典へ近づく。

必要なのは対象名の網羅ではなく、異なる記述体系が接触するときに何を保持し、何を変形し、何を残差として残し、どこへ返すかを扱う少数の運用原則である。

### 1.4 Navigator が読解支援と管理基盤の間にいる

現行Navigatorは、Public Navigatorによる読解・検索・関係探索と、Developer Navigatorによるregistration review、監査、review transactionをすでに分離している。

この基盤は、今後の文書管理へ拡張できる。

ただし、理論本文、canonical metadata、評価履歴、検索用discovery、生成された表示を明確に分離しなければ、Navigatorが第二の正本になる危険がある。

---

## 2. 基本方針

### 2.1 文書内容と文書管理を分ける

文書本文は、その文書が所有する内容を保持する。

管理系は、その内容を再定義せず、現在の役割、成熟、主張強度、公開状態、評価履歴、関係、発見情報を追跡する。

```text
metadata describes the document
metadata does not become the document
```

### 2.2 必要な圧縮だけを残す

すべてを非圧縮の履歴にすると一覧性を失う。逆に、すべてをコードへ縮約すると評価根拠を失う。

本設計では、即時の選別やリスク認識に実務的価値がある情報だけを短い分類へ圧縮する。

現時点では、少なくとも `Claim Strength` はその候補である。

一方、評価は履歴を一次情報とし、必要な表示だけを後から生成する。

### 2.3 評価可能性と常時深度監査を区別する

文書、プロンプト、通約、AI出力、運用結果はすべて監査対象になりうる。

しかし、すべてを常時同じ深度で監査すると、監査自体が処理を支配する。

したがって、監査可能性は常時保持し、深度監査は影響、未知性、強い主張、外部領域接触、公開判断、異常、Return発生などの条件に応じて起動する。

---

## 3. 文書メタデータの分離案

現時点では、次の軸を独立して管理する方向を採る。

### 3.1 Status

文書の現在の運用状態を表す。

これは内容の重要性、成熟度、役割を表さない。

候補例：

- Active
- Hold
- Superseded
- Deprecated
- Archived

最終語彙は `Metadata Assessment Policy` で定める。

### 3.2 Role

文書が何の仕事をするかを表す。

候補例：

- Principle
- Model
- Frame
- Protocol
- Policy
- Research Note
- Application
- Overview
- Reference
- Annotation
- Index / Navigation

Roleと定義所有は同一ではない。概念所有はmanifest内の所有契約で別途管理する。

### 3.3 Maturity

文書内容がどこまで安定し、照合・変更管理可能になっているかを表す。

Maturityは真理性、普遍性、重要性を表さない。

暫定的には、Seed / Exploratory / Structured Draft / Reviewable / Stable / Maintained Baseline のような段階を候補とする。

最終的な昇格条件は `Metadata Assessment Policy` で定める。

### 3.4 Claim Strength

命題がどの程度強く対象へコミットしているかを短く示す。

Claim Strengthは、検証済み度、成熟度、公開価値を表さない。

短い縮約を維持する理由は、次にある。

- 強い主張を高速に検出できる。
- 外部専門領域との接触時に追加監査を起動できる。
- Navigatorで高強度・低成熟・評価不足の組合せを発見できる。
- 公開・通約時に無標識な主張強化を検出できる。

ただし、文書全体を一つの値へ押し込めない。必要なら `core` と `max`、または節・claim単位の例外を持つ。

### 3.5 Evaluation History

現行の Verification Stage は、canonical metadata上の単一進捗コードとしては廃止候補とする。

代わりに、評価を履歴として保持する。

最低限、各評価記録は次を持つ。

```yaml
evaluation_record:
  id: stable_id
  date: YYYY-MM-DD
  target: document_or_claim
  reason: why_this_was_evaluated
  mode: evaluation_method
  method: what_was_done
  evidence: references_or_artifacts
  observed: what_was_observed
  assessment: how_it_was_interpreted
  decision: operational_decision
  residuals: unresolved_differences
  next_action: optional
```

`observed`、`assessment`、`decision` を分ける。

評価理由や判断は完全な客観ではない。しかし履歴を保持すれば、後から別の主体が再評価できる。

したがって目標は「評価を客観的な一数値にすること」ではなく、評価を監査可能にすることである。

---

## 4. Verification Code を縮約しない理由

現行Vコードには一覧性という実務上の利点がある。

しかし、概念整合、反例照合、Toy Model、実地評価、形式化、シミュレーション、外部予測比較は、同じ一本道上の段階とは限らない。

また同じ `V3` でも、自己評価、少数事例、対照実験、大規模データ、外部独立評価では証拠構造が異なる。

したがって、評価履歴を一次情報とする。

Navigator上で必要なら、次のような縮約表示を生成してよい。

```text
Last evaluated: 2026-08-21
Evaluation records: 4
Modes: consistency / counterexample / controlled comparison
Open findings: 2
```

この表示はcanonicalな証明段階ではなく、評価履歴から生成される索引である。

旧V互換値が移行上必要な場合も、手入力値ではなく派生表示として扱う。

---

## 5. 評価モードは序列ではなく語彙として持つ

評価方法は対象に応じて選択する。

候補例：

- conceptual_consistency
- cross_document_consistency
- external_mapping
- counterexample_review
- adversarial_review
- constructive_test
- operational_evaluation
- controlled_comparison
- formalization
- simulation
- empirical_evaluation
- external_review
- predictive_comparison
- publication_review
- commensuration_review

この一覧は専門分野の方法論を所有するためのものではない。

外部領域の主張を評価するときは、その領域自身の証拠条件、標準、法令、仕様、実証方法が優先する。

---

## 6. 通約を証明対象ではなく運用原則として扱う

通約は、それ自体を世界の普遍法則として証明することを前提にしない。

異なる言語、理論、専門、制度、創作、AI、人間の問いが接触するときに、無理な同一化と無意味な切断の両方を避けるための運用原則として採用する。

その性能は運用によって評価する。

```text
use
  -> observe difference
  -> evaluate
  -> revise / restrict / suspend
  -> reuse
```

ここでは次を区別する。

- 通約原則を採用すること。
- 通約によって得られた個別命題が正しいこと。
- 外部専門領域について経験的・形式的主張を行うこと。
- 通約を使ったAIが実際に性能向上すること。

これらは別々の評価対象である。

### 6.1 成功は真理証明ではない

通約手順が有用であっても、その有用性をSO全体の真理性の証明へ使わない。

### 6.2 運用上の敗北は採用理由を弱める

一方、通常の翻訳、要約、専門家による再定式化、既存手法より継続的に悪い結果を出す場合、その運用原則を維持する理由は弱くなる。

候補となる敗北条件：

- 元の問いをむしろ失う。
- 専門接続精度を下げる。
- 偽の同一化を増やす。
- 残差保持コストが利益を上回る。
- 常時過剰説明・遅延を生む。
- SOなし対照条件の方が反復して良い。

運用上の有効性と存在論的真理を同一視しない。

---

## 7. 言語・意味・通信位相研究から抽象化するもの

v5で追加された言語研究線は、通約を単なる翻訳としてではなく、差分、残差、返路、概念所有、非主張境界を保持する再構成として研究している。

また、通信一般の研究線は、シームレスな認識を有限な通信・記録・責任処理へ落とす際に暫定的な切断が必要であり、その切断の損失を保持する必要を扱っている。

Policyへ持ち上げるのは、各研究ノートの高密度語彙そのものではなく、そこから抽象化できる運用条件とする。

暫定的には、通約を次の流れとして扱える。

```text
Difference
  -> Articulation
  -> Relation / Operation
  -> Reconstruction in another local system
  -> Residual
  -> Return
```

この構造は今後の監査対象であり、現時点で普遍理論として確定しない。

---

## 8. 言語ゲームを固定分類しない

ストア派、エピクロス派、否定神学、中観、ヘーゲル型、量子場、法学、経済学などを、SO側で網羅的な分類表へ登録しない。

対象名を増やすほど、Policyが専門分類の所有者になり、分類維持コストと誤同定リスクが増える。

言語ゲームは、必要な接触時に局所的な運用条件として記述する。

最低限、次の問いで足りる可能性がある。

| Interface question | 意味 |
|---|---|
| Foreground | 何を問題・対象・差分として前景化するか |
| Articulation | 何を一つの対象・命題・事象として切り出すか |
| Relation | 何と何を、どの関係で結べるか |
| Allowed operation | 何を正当な推論・計算・観測・解釈・引用とするか |
| Warrant | 何を証拠・理由・権威として受け入れるか |
| Closure | 何をもって証明・理解・合意・解決とするか |
| Residual / Return | 入らなかった差分をどう保持し、どこへ戻すか |

これは対象領域をSOへ分類する表ではない。

接触時に「こちらの問いがどこまで相手の運用条件で再構成可能か」を確認するためのインターフェースである。

---

## 9. 専門性との境界

専門用語は単なる排他装置ではない。多くの場合、長い定義、前提、証拠条件、操作可能性を圧縮している。

したがって、専門語を知らない問いをそのまま専門的に妥当と見なしてはならない。

同時に、専門語を使用できないことと、問い自体が無意味であることも同一ではない。

本プロジェクトが狙う接続は、専門家を代替することでも、専門領域をSOの下位に置くことでもない。

```text
unformed question
  -> preserve original pressure
  -> expose hidden distinctions
  -> propose candidate domain formulations
  -> mark non-identity and uncertainty
  -> submit to domain-specific validation
  -> preserve what remains untranslated
```

対象領域の定義、証拠条件、法令、標準、数理、実証方法が必要な地点では、それらがSOより優先する。

SOまたはAIは、問いの輸送と差分保持を支援できるが、専門領域の成立条件を所有しない。

---

## 10. Publication and Commensuration Policy の将来像

現行Policyは、今後の改修で責務を縮小する候補である。

最終的には、少なくとも次の領域へ集中させる。

1. **Authority**
   - 正本言語
   - 通約文書との優先関係
   - 概念所有
   - 外部領域の定義権限

2. **Publication**
   - 公開、保留、非公開、分割
   - 公開時に保持すべき非主張境界

3. **Commensuration Contract**
   - 何を保存するか
   - 何を変形可能とするか
   - 何を無標識に変更してはならないか

4. **Residual and Return**
   - 通約不能差分
   - 誤読
   - 外部批判
   - 正本への返路

5. **Machine Projection Boundary**
   - manifest
   - Markdown header
   - Glossary / registry
   - generated catalog / graph / Navigator

Maturity、Claim Strength、評価履歴の判定規則は `Metadata Assessment Policy` 側へ移す。

個別専門分野の詳細な接続規則は、必要な場合だけ別のdomain-specific protocolへ置く。

---

## 11. `Claim_Strength_and_Publication_Layer_Table` の扱い

新しい `Metadata Assessment Policy` が確立し、manifestと生成物が移行した後、現行 `Claim_Strength_and_Publication_Layer_Table` は統治正本としての役割を終了できる。

ただし即時削除しない。

移行期間中は、旧ラベルの意味と新管理方式の対応を確認するためのmigration referenceとして保持する。

移行完了後は、たとえば次の状態へ送る。

```text
Status: Superseded
Superseded by:
  - Metadata Assessment Policy
  - Publication and Commensuration Policy
  - canonical metadata ledger / evaluation records
```

過去リリースの読解可能性を残すため、履歴から消去しない。

---

## 12. manifest を canonical metadata ledger にする

`tools/docs_manifest.yml` は、文書内容ではなく文書管理状態のSingle Source of Truthへ寄せる。

候補責務：

- stable document identity
- path / language relation
- Status
- Role
- Maturity
- Claim Strength
- public state / publication profile
- concept ownership / typed logical relations
- discovery metadata
- evaluation record references
- body snapshot hash
- metadata assessment date / assessor provenance

評価本文をmanifestへ大量に埋め込む必要はない。

評価記録が増える場合は別ledgerへ分離し、manifestは現在状態と参照だけを保持する。

```text
docs_manifest.yml
  -> current canonical metadata

evaluation ledger(s)
  -> chronological assessment evidence
```

---

## 13. Markdown header は機械投影へ移す

正本文書のヘッダーを人間が個別に同期し続ける方式は、文書数増加に伴ってdriftを起こす。

将来的には、管理対象ヘッダーをmanifestから生成する。

```text
canonical metadata ledger
  -> deterministic header renderer
  -> managed Markdown header block
```

本文の意味内容は変更しない。

### 13.1 Metadata-only update の不変条件

AIまたはツールへ「ヘッダーのみ変更」を委任するときは、本文の同一性を機械的に検査する。

候補手順：

1. managed metadata blockを除いた本文hashを計算する。
2. header projectionを更新する。
3. 更新後に本文hashを再計算する。
4. hashが変わった場合は失敗とする。
5. header diffだけをreview対象として提示する。

これにより、AIへ大量文書の機械作業を委任しつつ、内容本文への無意図な変更を検出できる。

---

## 14. Navigator を管理ツールへ回収する

現在のPublic / Developer Navigator分離は維持する。

Public Navigatorは読者のための入口であり続ける。

Developer Navigatorを、canonical metadataと評価履歴を扱う管理ワークスペースへ拡張する。

### 14.1 Public Navigator

引き続き次を中心とする。

- 読解入口
- search / topic
- language counterpart resolution
- typed relation traversal
- public reader

MaturityやClaim Strengthを表示する場合も、ランキングや真理スコアとして提示しない。

### 14.2 Developer Navigator

将来的な管理対象候補：

- Status / Role / Maturity / Claim Strength
- registration state
- publication state
- concept ownership / typed relations
- latest evaluation date
- evaluation modes
- open findings / residuals
- Return / Drift records
- metadata consistency diagnostics
- header projection preview
- metadata-only diff
- body-hash verification
- migration queue

### 14.3 Navigatorは直接正本を書かない

既存契約を維持する。

ブラウザUIは、canonical ledgerを直接変更しない。

```text
Navigator review state
  -> explicit review transaction
  -> validation / dry-run
  -> explicit repository apply
  -> regenerate projections
```

これにより、UIの操作ミスやブラウザ状態をそのまま正本変更へしない。

---

## 15. Navigatorで必要になる主要ビュー

### 15.1 Corpus Dashboard

文書群全体の状態を確認する。

例：

- Role分布
- Maturity分布
- Claim Strength分布
- 未評価期間
- open finding数
- provisional registration
- public / hold / deprecated

### 15.2 Document Inspector

一文書について、本文を再定義せず次を表示する。

- canonical metadata
- concept ownership / relations
- assessment history
- current residuals
- linked Return records
- generated header preview
- source body hash

### 15.3 Review Queue

機械検査または人間・AI監査によって見つかった候補を処理する。

- metadata mismatch
- maturity reassessment candidate
- strong claim without recent assessment
- public claim with open blocking finding
- stale header projection
- missing return path

### 15.4 Evaluation Timeline

Vコードの代わりに、評価履歴そのものを時系列で表示する。

必要なら表示上だけ集約する。

### 15.5 Migration Workspace

旧metadataから新metadataへの移行を管理する。

- current header
- manifest current state
- proposed normalized metadata
- change rationale
- header-only diff
- body unchanged verification

---

## 16. AIに任せる範囲

AIは、次を支援できる。

- 文書本文を読んだMaturity / Claim Strength候補の提示
- Status / Role候補の分類
- 既存metadataとの不一致検出
- 評価理由の構造化
- 反例候補・未解決点の抽出
- header projection
- 大量文書のmetadata-only migration

ただし、AIの判定を自動的な正本変更にしない。

特に次は人間または明示的review transactionを経る。

- concept ownershipの変更
- canonical roleの変更
- Maturityの重要な昇格
- Claim Strengthの降格・昇格
- publication boundaryの変更
- policyの変更

AIの利点は判断主体を置換することではなく、比較可能な候補と監査材料を増やすことに置く。

---

## 17. 実装順序

本設計は一括置換しない。

### Phase 0 — Baseline fixation

- 現行ZIP / working treeのhashを保存する。
- 現行manifest、Navigator、checker、Claim Tableをbaselineとして固定する。

### Phase 1 — Governance design

- 本Design Noteをレビューする。
- `Metadata Assessment Policy` を作成する。
- `Publication and Commensuration Policy` の責務縮小案を作る。
- Evaluation Recordのschemaを確定する。

### Phase 2 — Schema prototype

- manifest次期schemaを別versionとして作る。
- 既存fieldを即時削除せずmigration mappingを持つ。
- 代表10〜15文書で試験する。

### Phase 3 — Navigator recovery

- Developer Navigatorへmetadata assessmentとevaluation historyを統合する。
- review transactionを新schemaへ対応させる。
- Public Navigatorには必要最小限だけ投影する。

### Phase 4 — Header projection pilot

- 少数文書にmanaged header blockを導入する。
- body hashで本文不変を検証する。
- AIによるheader-only migrationを試験する。

### Phase 5 — Corpus migration

- 全文書を新schemaへ移行する。
- headerを生成する。
- index / graph / public catalog / Navigatorを再生成する。
- release gateを実行する。

### Phase 6 — Legacy retirement

- `Claim_Strength_and_Publication_Layer_Table` をSupersededへ移す。
- 旧Vコードをcanonical metadataから外す。
- 移行履歴と互換説明を残す。

---

## 18. この設計の監査条件

この管理方式自体も評価対象である。

少なくとも次を監査する。

- metadata入力負荷は本当に減ったか。
- AIによる分類が人間の修正作業を増やしていないか。
- Maturity / Claim Strengthのコードが自己目的化していないか。
- Evaluation Historyが過剰ログ化していないか。
- Navigatorが理論本文より強い権威を持っていないか。
- 通約原則が通常の翻訳・専門家照合より悪い場面を残せているか。
- 専門領域の定義権限をSOへ吸収していないか。
- header projectionが本文変更を起こしていないか。
- Return / residualが実際に後続判断へ使われているか。

「管理情報を増やすこと」自体を成功条件にしない。

成功条件は、文書管理のdriftを減らし、理論内容の監査可能性を上げ、手作業を減らしながら、必要な差分を失わないことである。

---

## 19. 未確定事項

現時点では次を確定しない。

1. Statusの正式語彙。
2. Roleの正式語彙。
3. Maturityの段階数と昇格条件。
4. Claim Strengthの新版定義。
5. Evaluation modeの最終controlled vocabulary。
6. Evaluation ledgerをmanifest内に置くか別ファイルへ分離するか。
7. Claim単位評価をいつ導入するか。
8. Publication ProfileをどのPolicyが最終所有するか。
9. 言語ゲーム・インターフェースをPolicy本文へ置くか、独立Protocolへ置くか。
10. managed Markdown header blockの具体形式。
11. body hashの正規化方式。
12. Navigatorからどの変更までreview transactionとして扱うか。

これらは、Policy作成とprototypeの結果を受けて確定する。

---

## 20. 次の安定した返り先

次の作業対象は、理論本文の一括修正ではない。

1. `Metadata Assessment Policy` の正式な判定基準。
2. 言語・意味・通信位相研究を踏まえた、縮小版 `Publication and Commensuration Policy` の責務設計。
3. Evaluation Record schema。
4. 次期 `docs_manifest.yml` schema prototype。
5. Developer Navigatorの管理ワークスペース化。

この順序で進め、各段階で現行版とのA/Bまたはmigration diffを残す。

---

## 21. 非主張境界

本文書は次を主張しない。

- MaturityやClaim Strengthが文書の真理性を測定する。
- 評価履歴を増やせば客観性が保証される。
- 通約が異なる思想・科学・言語を完全に統一できる。
- SOが専門領域の定義権限を代替できる。
- Navigatorが理論判断を自動化すべきである。
- AIが文書の正本権限を持つべきである。
- 現在の設計案が最終形である。

本文書が置くのは、今後の管理機構を設計・評価するための作業上の基準点である。

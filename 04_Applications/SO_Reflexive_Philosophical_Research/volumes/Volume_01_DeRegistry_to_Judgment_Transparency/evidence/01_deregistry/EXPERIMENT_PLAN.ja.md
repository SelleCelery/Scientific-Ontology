# 選択公理モジュールの固有分類依存解除実験
## Optional Axiom Module De-Registry Experiment

> Status: Working Research / Experiment Plan
> Layer: 05_Research_Notes / local workbench (`000*`; not public index)
> Role: Experimental protocol and research record
> Authority: None. This document does not define SO canon, publication policy, or metadata policy.
> Language: Japanese authoritative; English commensuration not planned at this stage
> Started: 2026-08-21
> Test corpus: `fixtures/0001Optional_Axiom_Modules.md`
> Test corpus SHA-256: `20c3fa4f3c82719cf3716b4a52974b433c945143434ffb1a5a47b779fa8ae136`

---

## 0. 研究上の位置づけ

本実験は、旧「選択公理モジュール」を整理・校訂すること自体を目的としない。

旧モジュールは、哲学、宗教、科学、倫理、美学、政治、戦略、死生観、SO内部の応用形而上学など、多数の固有名・分類・類似系列を同一フォーマットへ登録した観点アトラスである。そのため、次の問いを試す高密度なテストコーパスとして扱える。

> 固有の思想名、学派名、専門分野名、分類レジストリを評価ロジックから外しても、命題の責務、適用範囲、主張強度、外部権限依存、公開判断、通約残差を扱えるか。

本実験で「De-Registry / 固有分類依存解除」と呼ぶのは、固有名や歴史的出典を消去することではない。

固有名・出典・歴史は **provenance / 再接続情報** として保持する。一方、それらを、主張強度や公開可否を決めるための必須分類キーとして使用しないことを試す。

したがって目標は、

```text
固有名を消すこと
```

ではなく、

```text
固有名を評価権限から外す
        ↓
命題・責務・範囲・成立条件で評価する
        ↓
必要時に出典・歴史・専門体系へ再接続する
```

ことである。

本作業の成功・失敗・残差そのものを、存在境界論における通約、圧縮、返路、偽閉鎖、言語ゲーム依存の研究データとして保存する。

---

## 1. 既存資料との関係

### 1.1 テストコーパス

`fixtures/0001Optional_Axiom_Modules.md` は固定入力であり、実験中は本文を修正しない。

この文書には、各エントリについて概ね次が含まれる。

- 公理文
- 解説
- 論理的起源と分岐点
- 関心 / 捨象
- 価値 / コスト
- 歴史的背景と物語
- 属する、あるいは類似する思想系列

この形式は大量の固有分類を持つため、レジストリ依存の有無を検査するのに適する。

### 1.2 現行正本

現行の `03_Tam_Goodness/Optional_Axiom_Modules_as_Cognitive_Bridge.ja.md` は、旧アトラスをそのまま正本化せず、関心・捨象・価値・コスト、Core Invariant、Operational Drift、残差処理などへ抽象化している。

本実験は現行正本を修正するための直接作業ではない。旧アトラスを使って、現行抽象化をさらに一般化できるか、また何を失うかを検査する。

### 1.3 言語・意味・通信位相研究

通約は、語彙一致や同一化ではなく、差分、概念所有、非主張境界、残差、返路を保持した再構成として扱う。

本実験は、この通約原則を「思想一覧」ではなく実際の異種観点データへ適用したとき、どこまで作動するかを見る運用評価でもある。

### 1.4 Metadata / Publication再設計との関係

本実験は、将来の `Metadata Assessment Policy` と `Publication and Commensuration Policy` の前段実験である。

特に次を検査する。

- Sコードを専門語や分野名なしで判定できるか。
- E/Uによる減速を、固有の「危険分野リスト」なしで行えるか。
- Rコードを廃止しても、通約上必要な差分をEvaluation / Residual記録へ保持できるか。
- Vコードを用いず、評価日、評価理由、方法、結果、残差を履歴として残せるか。

---

## 2. 研究質問

### RQ-1｜分類非依存性

思想名、学派名、専門分野名、既存カテゴリを隠しても、命題の責務と適用範囲からS/E/U/Pを暫定判定できるか。

### RQ-2｜ラベル効果

固有名を再表示したとき、判定がどれだけ変化するか。

変化した場合、それは、

- 正当な外部権限情報が回復したためか、
- 単に「量子」「宗教」「政治」「オカルト」等の語彙に引っ張られたためか、

を分離できるか。

### RQ-3｜再接続可能性

固有分類を評価ロジックから外した後でも、必要な場合に元の歴史、出典、専門領域へ戻れるか。

### RQ-4｜圧縮損失

固有名・カテゴリを外すことで失われる情報は何か。

その損失は、

- 評価上不要な装飾、
- provenanceとして必要な情報、
- 命題の成立条件そのもの、

のどれか。

### RQ-5｜通約の非同一化

異なる体系が似た構造を持つとき、同一化せずに比較できるか。また、同じ語を使う体系が異なる責務を持つとき、同一カテゴリへ畳み込まずに保持できるか。

### RQ-6｜専門権限の境界

外部専門領域についてSO側が判断できない部分を、新カテゴリ追加ではなく `external_authority_required` 等の権限情報として検出できるか。

### RQ-7｜SO自己適用

同じ手順を、SO自身の統合命題・応用形而上学的命題へ適用した場合にも、他体系と同じ減速・残差処理を行えるか。

---

## 3. 仮説

### H1｜初期評価は固有名なしでも可能

命題本文、責務、適用範囲、断言形式が保持されていれば、初期S/E/U/P判定に固有の思想分類は必須ではない。

### H2｜固有名は評価キーではなく再接続キーとして有用

固有名、学派名、専門分野名、歴史的背景は、評価値を直接決めるより、出典確認、専門的再検査、履歴復元のためのprovenanceとして有用である。

### H3｜Sの語彙汚染を検出できる

同一に近い責務・範囲を持つ命題を異なる語彙で表現した場合、S判定が大きく変わるなら、S判定器が語彙または分野ラベルに汚染されている可能性が高い。

### H4｜一部の文脈は剥離できない

固有文脈を外すと命題の責務または成立条件が失われる事例が存在する。その場合、無理に一般化せず `context_required` として残す方がよい。

### H5｜運用上の成功は理論的真理を証明しない

De-Registry方式が管理・通約・公開判断で有効でも、それ自体がSOの存在論的命題を証明するものではない。

---

## 4. 操作上の定義

### 4.1 Registry dependency / レジストリ依存

ある判定を行うために、「この命題は物理学だから」「これは中観だから」「これは宗教だから」のような固有カテゴリが不可欠になっている状態。

### 4.2 Provenance dependency / 出典依存

命題の意味、責務、成立条件、外部権限を正確に理解するため、出典または歴史的文脈への再接続が必要な状態。

Registry dependencyとProvenance dependencyは同一ではない。

### 4.3 Label effect / ラベル効果

ラベル非表示条件とラベル再表示条件で、S/E/U/P、責務判定、外部権限判定が変化すること。

### 4.4 Legitimate context correction / 正当な文脈補正

ラベル再表示によって、出典、引用関係、専門上の定義権限、発話者の責務が判明し、判定変更に理由がある場合。

### 4.5 Label contamination / ラベル汚染

追加された語彙・学派名・分野名だけを根拠として判定が変わり、命題の責務・範囲・成立条件の変化で説明できない場合。

---

## 5. 暫定評価モデル

本節はMetadata Assessment Policyを確定するものではない。本実験のための暫定判定器であり、結果によって変更する。

### 5.1 判定順

1. 命題単位を切り出す。
2. 命題の所有関係を確認する。
3. 責務と適用範囲を確認する。
4. 断言形式からSを暫定判定する。
5. Sから `P_base` を置く。
6. Eで認識・批判リスクによる減速を行う。
7. Uで応用・安全リスクによる抽象化または非公開化を行う。
8. `P_final` を決める。
9. 評価理由・日付・残差を記録する。

暫定式：

```text
P_final = decelerate(P_base(S), E, U)
```

Rは使用しない。

### 5.2 S判定の暫定規則

| S | 判定対象 |
|---|---|
| S0 | 用語、分類、記録、運用上の約束のみ |
| S1 | 明示範囲内の記述、類比、ヒューリスティック |
| S2 | 特定フレーム内部での再解釈、モデル化 |
| S3 | 条件付きの一般構造、関係、規則性の主張 |
| S4 | 異なる対象・記述体系を越える対応、機構、因果、生成関係の主張 |
| S5 | 同一性、普遍性、外部実在、強い因果、既存領域の置換・競合を伴う主張 |

専門語そのものをS判定根拠にしない。

### 5.3 所有関係の暫定値

```text
owned
imported
paraphrased
comparison_target
derived
mixed
unresolved
```

外部体系の説明部分と、SO側がそこから導出した部分を可能な限り分ける。

### 5.4 外部権限依存

```text
none
source_check_required
domain_authority_required
context_required
unresolved
```

`domain_authority_required` は、専門性をSOが所有することを意味しない。むしろ、SO側だけでは判定を完了できないことを明示する。

---

## 6. 実験条件

### Condition A｜Source-visible / 原記録条件

元のID、思想名、学派・分野、歴史的背景、類似思想を含めて読む。

これは旧方式の基準条件である。

### Condition B｜Label-blind / 固有分類遮蔽条件

次を隠す。

- IDに含まれる分野分類
- 思想名・学派名・人物名
- 「存在論」「認識論」「政治」等の大分類
- 類似思想系列
- 評価を誘導する歴史的物語

一方、命題そのものの意味を破壊しないため、必要な対象語、条件、関係は残す。

### Condition C｜Provenance-restored / 再接続条件

Bの判定後に、固有名、出典、歴史、専門領域を再接続する。

A/B/C間の判定差を記録する。

### Condition D｜Re-rendering challenge / 再表現試験

同じ責務・範囲を維持した命題を、

- 一般語
- 哲学語
- 科学近接語
- 神話・物語語

などへ再表現し、S/E/U/Pが語彙だけで不必要に変動しないかを見る。

再表現によって責務または成立条件まで変化した場合は、同一命題として扱わない。

---

## 7. 初期サンプル

初期試験は、旧アトラスから性質の異なる12件を抽出し、加えてSO内部統合命題1件を自己適用対照として使う。

暫定候補：

1. O-1.2 物理主義的同一説
2. O-6 カント的二世界論
3. O-8 相対性理論
4. E-3 現象学
5. E-7 否定神学的アプローチ
6. E-9 量子力学
7. G-3 空の思想
8. ET-3 功利主義
9. A-1 美的超越論
10. S-8 法家思想
11. S-11 民主主義
12. TR-1 転生
13. SYN-1.1 応用形而上学（SO自己適用対照）

この選択は代表性の証明ではない。語彙、成立条件、権限、経験主張、規範主張の差を意図的に広く取るための初期ストレステストである。

---

## 8. 1ケースの処理手順

### Step 1｜Source snapshot

原文の対象箇所を変更せず保存し、source IDを付ける。

### Step 2｜Atomic proposition extraction

一つのエントリを一つの命題と仮定しない。

- 外部体系の説明
- SO側の再解釈
- 歴史的説明
- 価値評価
- コスト評価
- 類似性判断

を可能な範囲で別命題へ切る。

### Step 3｜Observer / evaluator separation

次を分離する。

```text
source_claim
source_self_description
SO_interpretation
evaluator_assessment
publication_decision
```

特に「価値」「コスト」「捨象」が、元体系自身の明示なのか、SO側からの評価なのかを記録する。

### Step 4｜Blind transformation

固有分類を外し、一般記録へ変換する。

### Step 5｜Blind assessment

S/E/U/P、ownership、authority dependencyを暫定評価する。

### Step 6｜Unblind / provenance restore

原ラベルと出典情報を戻す。

### Step 7｜Delta analysis

判定差を、

- legitimate context correction
- label contamination
- insufficient context
- no material change

へ分類する。

### Step 8｜Residual return

一般スキーマで扱えなかった差分を記録し、

- スキーマ修正候補
- Metadata Policy候補
- Commensuration Policy候補
- 外部専門確認
- 旧アトラス固有の物語情報

のいずれかへ返す。

---

## 9. ケース記録の最小スキーマ

```yaml
case_id: DR-CASE-0001
source:
  corpus: 0001Optional_Axiom_Modules
  source_id: O-1.2
  source_label: "..."

proposition:
  source_text: "..."
  normalized_statement: "..."

ownership:
  relation: imported | paraphrased | owned | derived | mixed | unresolved
  authority_dependency: none | source_check_required | domain_authority_required | context_required | unresolved

scope:
  subject: "..."
  domain_of_application: "..."
  conditions: []
  exclusions: []

assessment_blind:
  date: YYYY-MM-DD
  S: S0-S5
  E: E0-E3
  U: U0-U4
  P_base: P0-P3
  P_final: P0-P3
  reasons: []

assessment_unblinded:
  date: YYYY-MM-DD
  changed: true | false
  changes: []
  reason_class: legitimate_context_correction | label_contamination | insufficient_context | no_material_change

perspective_reading:
  foreground: []
  background_or_abstraction: []
  preserved_or_valued: []
  cost_or_externalization: []
  evaluator_position: source | SO | current_evaluator | unresolved

residuals: []
return_targets: []
```

このスキーマは確定仕様ではない。実験対象である。

---

## 10. 評価指標

### 10.1 Category creation count

新しいケースを処理するために、新しい固定分野カテゴリを追加した回数。

目標はゼロに近いことであり、ゼロを絶対条件とはしない。

### 10.2 Label sensitivity

B→CでS/E/U/Pが変化したケース数と変更幅。

変更理由が責務・権限・範囲で説明できなければlabel contamination候補とする。

### 10.3 Reconstructability

一般記録から、元命題の責務・適用範囲・非主張境界をどこまで再構成できるか。

暫定3段階：

- 2: 中心責務と主要境界を再構成できる
- 1: 一部の重要差分が失われる
- 0: 固有文脈なしでは別命題になる

### 10.4 Residual capture rate

無理に分類せず `residuals` または `context_required` として残せた重要差分の割合。

高ければ常に良いわけではない。残差過剰保持も記録する。

### 10.5 External-authority detection

外部専門知が必要な命題について、SO側だけで閉鎖せず `domain_authority_required` を立てられたか。

### 10.6 Compression loss ledger

ラベル除去で失われた情報を、次へ分類する。

```text
no_material_loss
provenance_loss
historical_context_loss
normative_context_loss
domain_condition_loss
semantic_core_loss
unresolved
```

### 10.7 Operational cost

1ケース当たりの記録量、判定の複雑さ、再検査回数を記録する。

一般化のために管理コストが増えすぎる場合は失敗として扱う。

---

## 11. 成功条件

本実験は、次の傾向が得られればDe-Registry方式を次段へ進める。

1. 新しい思想・分野を追加してもschema追加がほぼ不要。
2. 固有名なしでもS/E/U/Pの初期判定が大きく崩れない。
3. ラベル再表示による変更が、主に正当な権限・文脈補正として説明できる。
4. 固有名・歴史をprovenanceとして再接続できる。
5. 専門領域の検証権限をSOが奪わずに済む。
6. 同じ語の異義、異なる語の構造類似を、同一化せず記録できる。
7. SO自身の高強度命題にも同じ減速規則を適用できる。
8. 管理コストが既存registry方式を著しく上回らない。

---

## 12. 失敗・停止条件

次の場合は、一般化を止めてschemaを再検討する。

- 固有カテゴリなしでは多数の命題が意味を失う。
- `context_required` がほぼ全件になり、一般化の実用性がない。
- S/E/U判定がラベル遮蔽で不安定になりすぎる。
- 再接続後に元の責務へ戻れない。
- 「残差」と記録するだけで、実質的に何も判定しなくなる。
- schemaが旧registryより複雑になり、運用コストだけが増える。
- SO内部命題にだけ例外規則を作らないと維持できない。

停止は研究失敗ではない。どこまで抽象化できないかを示す結果として記録する。

---

## 13. 実験フェーズ

### Phase 0｜Protocol freeze

- 本計画を固定する。
- テストコーパスhashを固定する。
- ケース記録テンプレートを固定する。
- 正本文書は変更しない。

### Phase 1｜Pilot extraction

まず4件で実施する。

候補：

- O-8 相対性理論
- E-7 否定神学的アプローチ
- G-3 空の思想
- S-8 法家思想

異なる成立条件を持つ4件で、命題分解とblind schemaが実用になるかを見る。

### Phase 2｜12+1 case run

初期サンプル全体へ適用し、B/C差を集計する。

### Phase 3｜Adversarial re-rendering

同じ責務を異なる語彙へ移したときのS/E/U/P変動を検査する。

ここでは特に、

- 観測
- 法
- 空 / 無
- 情報
- 自由
- 客観 / 主観

など、複数言語ゲームで意味が変形しやすい語を使う。

### Phase 4｜Policy extraction

実験結果からのみ、次を抽出する。

- Metadata Assessment Policyに必要な機械判定規則
- Publication and Commensuration Policyに必要な最小通約契約
- 不要になったR/V/固定registry項目
- provenanceとして残すべき情報

### Phase 5｜Navigator implementation test

結果が安定した場合のみ、Developer Navigatorへ、

- claim records
- S/E/U/P
- evaluation history
- provenance
- residuals
- return targets

を表示・編集・比較する機能を試験実装する。

Navigator実装の都合で理論上の分類を増やさない。

---

## 14. 評価履歴の原則

Vコードは本実験では使用しない。

各評価について、最低限次を残す。

- Date
- Target
- Reason
- Method
- Observed
- Assessment
- Decision
- Residual
- Recheck condition

`Observed / Assessment / Decision` を分離する。

評価履歴は「正しさの証明」ではなく、後から再検査できる判断記録である。

---

## 15. 研究上の非主張境界

本実験は、次を主張しない。

- 旧アトラスに記載された哲学史・宗教史・科学史の説明が正確である。
- 各思想が本実験の抽出内容へ還元できる。
- 固有名や歴史的文脈が不要である。
- 専門性が不要である。
- SOが外部専門領域の判定権限を持つ。
- 一般schemaがあらゆる言語ゲームを完全に表現できる。
- 運用上うまくいったことがSOの存在論的正しさを証明する。

逆に、固有文脈なしでは保持できない差分が見つかった場合、それを一般化の失敗として消去せず、研究結果として保持する。

---

## 16. 研究成果の返送先

結果は自動的に正本へ統合しない。

候補返送先：

```text
実験記録
  ├─ metadata判定規則
  │    → Metadata Assessment Policy
  ├─ 通約・provenance・残差
  │    → Publication and Commensuration Policy
  ├─ 言語・通信上の知見
  │    → Language, Meaning, and Communication Phase Studies
  ├─ 選択公理モジュールの役割変更
  │    → Optional Axiom Modules as Cognitive Bridge
  ├─ 管理UI要件
  │    → Developer Navigator
  └─ 理論と衝突する事例
       → Return / Conflict / Research Note
```

昇格条件は、複数ケースで再現し、SOなしでも管理上の利益を説明でき、利益と副作用の双方が記録されていることとする。

---

## 17. 最初の実行単位

最初の実験はPhase 1の4件のみとする。

1. 原文命題の分解
2. 固有分類遮蔽版の生成
3. blind assessment
4. provenance復元
5. 判定差分の記録
6. schema残差の抽出

この4件を終えるまでは、正本文書、manifest、Navigatorを変更しない。

この制約により、ツール実装が先に概念を固定することを避ける。

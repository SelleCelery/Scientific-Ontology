# Three-Layer Transformation Topology Protocol
## 三層記述・変換トポロジー監査プロトコル

> Status: Experimental research protocol / no canonical authority
> Run mode: Continuation of the immediately preceding Luna Topology-first session
> Language: Japanese authoritative / English commensuration
> Scope: Procedure only. Do not infer, optimize for, confirm, or refute any expected conclusion.

---

## 0. 実行原則 / Execution principle

このrunでは、4ケースについて次の三層を分離して記録する。

A. `domain-authoritative description`
B. `Optional Axiom description`
C. `SO-derived interpretation`

監査対象は主として二つの変換である。

- Edge AB: A -> B
- Edge BC: B -> C

必要な場合のみ、AからCへの直接的な権威・根拠移送が起きていないかを `A -> C bypass check` として記録する。

このrunでは **S / E / U / V / P を使用しない。**
過去のSol/Luna結果、前runの得点、分布、結論を判定基準にしない。

本体は次の5軸のみである。

1. **接点整合性 / Anchor Integrity**
2. **位相整合性 / Phase Integrity**
3. **経路可読性 / Path Legibility**
4. **返路実効性 / Return Reachability**
5. **開放端保持 / Open-End Retention**

逸脱のprimitiveは次の4つのみとする。

- **Cut**
- **False Link**
- **Both**
- **Unresolved**

`Named pattern` は任意の検索補助であり、判定本体ではない。名前がない異常を消してはならない。

---

## 1. 4ケース / Cases

Manifest順に処理する。

1. G-3 空の思想（ナーガールジュナ）
2. S-8 法家思想（韓非子）
3. E-9 量子力学（観測理論として）
4. ST-2 クラウゼヴィッツの戦争論

4ケースを一つの連続runとして処理する。途中で横断的な再較正をしない。Cross-case auditはCase 4終了後にのみ行う。

---

## 2. Layer A: domain-authoritative description

### 2.1 意味

`domain-authoritative` は「その主張が究極的に真である」ことを意味しない。
その対象領域・思想・理論を、その領域自身の語彙と責務の下で記述するために、相対的に高い出典責任を持つ資料へ接続した記述を意味する。

`authoritative` というラベル自体を根拠として使用してはならない。

### 2.2 Source acquisition

Layer Aを作る前に、`Source Provenance Ledger`を作成して凍結する。

原則として、可能な範囲で次を組み合わせる。

- primary / canonical source, または対象体系自身の一次資料
- specialist secondary source, scholarly reference, standard reference, official/disciplinary source

ただし、一次資料の翻訳・版・解釈自体に争いがある場合は、その争いを保持する。

外部Web・資料アクセスが利用できない場合、モデルの一般知識だけを`domain-authoritative`として埋めてはならない。`source unavailable / unresolved` と記録する。

### 2.3 Source Provenance Ledger

各sourceについて記録する。

```text
Source ID:
Source type:
Author / institution:
Work / page / section if available:
What this source is being used to support:
Native terms that must not be flattened:
Known interpretive disagreement or scope limit:
Access status:
```

### 2.4 Layer A composition rules

- SO語彙へ翻訳してはならない。
- Optional Axiomの語彙へ寄せてはならない。
- 後段の比較が容易になるように内容を単純化してはならない。
- 複数の有力解釈がある場合、単一の「正解」に合成しない。
- 各proposition atomにSource IDを付ける。
- source label / discipline name / famous author name は、それ自体ではwarrantにならない。
- 引用ではなく原則として要約を用い、意味上必要なnative termsを保持する。

Layer Aを完成したら凍結する。B/Cを見てAを書き換えてはならない。

---

## 3. Layer B: Optional Axiom description

Layer Bは、現在の固定fixture `0001Optional_Axiom_Modules.md` 内の該当ケースから抽出する。

### Rules

- 前runのLuna要約をLayer Bとして再利用しない。fixture本文から再抽出する。
- 原文の言い回しを、domain sourceに合わせて補正しない。
- 「公理」「解説」「物語」「価値」「コスト」「論理的起源」「類似系列」等の原文上の役割を可能な限り保持する。
- Optional Axiom本文に外部体系の紹介とrepository側の追加解釈が混在している場合、無理にきれいに分離しない。混在箇所をclaim ID付きで残す。
- Bは「外部体系の正しい要約」ではなく、**Optional Axiomが実際にどう記述したか**の層である。

Layer Bを完成したら凍結する。

---

## 4. Layer C: SO-derived interpretation

Layer Cは、新たにSO的解釈を創作する層ではない。

Layer Bまたは該当Optional Axiomエントリに含まれるうち、repository / SO側が外部体系から追加したと判断できる次のものを抽出する。

- SO内部概念への接続
- 他の公理・理論への対応づけ
- 現代化・システム化・存在論化・運用化
- 外部体系から導いた価値・コスト・処方・社会的含意
- 「裏付け」「統合」「起源」「同型」「支える」等の橋渡し主張

### Rules

- CがBから明確に分離できない場合、`mixed / unresolved boundary` と記録する。
- Cを外部体系自身の主張へ戻してはならない。
- SO由来と確定できないものをSO由来として断定しない。
- 新しいSO解釈を追加しない。

Layer Cを完成したら凍結する。

---

## 5. Layer identity record / 三層の責務記録

各Layerについて次を記録する。

```text
Layer:
Claim IDs:
Text/description producer:
Represented voice/system:
Who is responsible for the wording:
Who is responsible for the claim as a claim:
Warrant mode visible in the text:
Scope / closure condition visible in the text:
Unresolved attribution:
```

### Important

`Who is responsible for the wording` と `Who is responsible for the claim as a claim` を同一視しない。

出典が明示されていること、固有名が付いていること、専門分野名が付いていることは、導出の成立を自動的に保証しない。

---

## 6. Edge audit / 変換監査

各ケースについて、Layerを凍結した後、次の順に監査する。

1. Edge AB: `domain-authoritative description -> Optional Axiom description`
2. Edge BC: `Optional Axiom description -> SO-derived interpretation`
3. A -> C bypass check, only if needed

各Edgeは独立して監査する。BCの問題を理由にABを書き換えてはならない。

### 6.1 接点整合性 / Anchor Integrity

問うこと：

- 変換後のclaimは、変換前のどのclaimへ接続しているか特定できるか。
- 出典、人物名、学派名、分野名が、内容上の接続を代替していないか。
- 権威あるsourceとの接触が、SO側の追加主張の権威へ転送されていないか。
- native termを別の概念へ置換した場合、その置換が明示されているか。
- A/B/Cの責務主体が途中で入れ替わっていないか。

### 6.2 位相整合性 / Phase Integrity

問うこと：

- 記述、引用、要約、解釈、比較、類推、因果、存在主張、規範、処方を無標識で移動していないか。
- `この体系ではXとされる` が `Xである` へ変換されていないか。
- 類似・比較が、同一性・導出・裏付けへ昇格していないか。
- 歴史的記述が現代的処方へ、形式理論が存在論へ、戦略記述が運用原理へ移る場合、そのphase transitionが見えるか。

### 6.3 経路可読性 / Path Legibility

問うこと：

- A -> B、B -> Cで何を保持し、圧縮し、追加し、捨象したか再構成できるか。
- claim IDを辿って変換経路を説明できるか。
- source citationが「参照」なのか「証拠」なのか「比較先」なのか判別できるか。
- 中間変換を省略して結論だけが残っていないか。

### 6.4 返路実効性 / Return Reachability

問うこと：

- BまたはCへの異議が、Aのsource、Bの表現、CのSO-derived bridgeのどこへ戻るべきか特定できるか。
- domain sourceとの不一致が発見されたとき、Optional Axiom記述を修正する経路があるか。
- SO-derived interpretationへの異議が、外部体系そのものを否定する形へ誤配送されないか。
- source disagreementがある場合、どのLayerを再開するか明示できるか。

### 6.5 開放端保持 / Open-End Retention

問うこと：

- Aの解釈争い、Bの混在、Cの導出不足を未解決のまま保持できるか。
- 「出典がある」ことを残差解消として扱っていないか。
- domain sourceとの差を、SOの深さ・統合力の証拠へ自動変換していないか。
- 名前の付かない変形を残せるか。

### Axis state

各軸に `intact / strained / failed / unresolved` の観測状態と短い根拠を付ける。
これはランキングではなく、そのEdge上の観測状態である。

---

## 7. Anomaly raw record

異常を検出した場合、primitive分類より先に生ログを固定する。

```text
Observed anomaly:
Affected nodes:
Expected path:
Observed path:
Possible cut:
Possible false connection:
Named pattern: optional
Unresolved difference:
Return point:
```

### Expected path rule

`Expected path` は「評価者が好む理論」を意味しない。
現在のclaimを成立させるために最低限必要となる、明示的な帰属・位相変換・根拠・返路を記述する。

「別の哲学ならこう言う」「現代科学ではこうだ」という置換をExpected pathにしてはならない。

---

## 8. Primitive projection

生ログを凍結した後だけ、各異常を次のいずれかへ投影する。

- **Cut** — 必要な接続、導出、変換、返路が失われている。
- **False Link** — 保証されていない接続、同一視、権威移送、責務移送が成立済みとして扱われている。
- **Both** — CutとFalse Linkが同じ異常に関与する。
- **Unresolved** — 異常は観測できるが、上の三つへ無理なく投影できない。

複数異常を一つへまとめない。
ケース全体を単一primitiveにする必要はない。

---

## 9. A -> C bypass check

次の場合のみ行う。

- CがAのsource authorityを直接参照しているように見える
- Bで行われた変形を経由せず、AがCの裏付けとして利用されている
- citation / school name / scientific authorityが、SO-derived claimのwarrantに見える

記録形式：

```text
A -> C bypass suspected: yes / no / unresolved
A node(s):
C node(s):
Explicit bridge present:
What B changed before C used A:
Topology observation:
Anomaly raw record if needed:
Primitive if needed:
```

`yes`自体を違反ラベルとはしない。明示的なbridgeがあれば正常な直接参照もあり得る。

---

## 10. Citation / label handling rule

出典・固有名・学派名・分野名について、次だけを守る。

- citationはprovenanceを与え得るが、導出を自動的には与えない。
- labelは対象識別を助け得るが、claim strengthや妥当性を自動的には与えない。
- source authorityは、そのsourceが責任を負うscopeを越えて転送しない。
- ある言語ゲーム内部のwarrantを、別の言語ゲームのwarrantへ無標識で変換しない。
- ただし、異なる言語ゲーム間の変換そのものを禁止しない。変換経路を記録する。

---

## 11. Per-case output template

```text
Case:

0. Source Provenance Ledger [FREEZE]
- Source A1:
- Source A2:
- disagreement / scope limit:

1. Layer A — domain-authoritative description [FREEZE]
A1:
A2:
...
Layer identity record:

2. Layer B — Optional Axiom description [FREEZE]
B1:
B2:
...
Layer identity record:

3. Layer C — SO-derived interpretation [FREEZE]
C1:
C2:
...
Layer identity record:

4. Lineage map [FREEZE]
A node(s) -> B node(s):
B node(s) -> C node(s):
Unmapped node(s):

5. Edge AB topology [FREEZE]
Anchor Integrity
- state:
- observation:
Phase Integrity
- state:
- observation:
Path Legibility
- state:
- observation:
Return Reachability
- state:
- observation:
Open-End Retention
- state:
- observation:

AB anomaly raw record(s):
...
AB primitive projection(s):
...

6. Edge BC topology [FREEZE]
Anchor Integrity
- state:
- observation:
Phase Integrity
- state:
- observation:
Path Legibility
- state:
- observation:
Return Reachability
- state:
- observation:
Open-End Retention
- state:
- observation:

BC anomaly raw record(s):
...
BC primitive projection(s):
...

7. A -> C bypass check, if needed
...

8. Return
- source-level return point:
- Optional-Axiom-level return point:
- SO-derived-level return point:
- unresolved transformation:

9. Japanese authoritative record

10. English commensuration
```

---

## 12. Run constraints

- Case orderはManifestに従う。
- 同一セッション内で4ケースを連続処理する。
- Case 4終了前にcross-case normalizationをしない。
- 前runのTopology判定・S/E/U/V/Pをコピーしない。
- Layer Bは必ず固定fixtureから再抽出する。
- Layer AをLayer B/Cに合わせて書き換えない。
- Layer Cをdomain sourceへ合わせて正常化しない。
- domain-authoritative sourceを「真理の最終裁定者」として扱わない。
- source disagreementは消さない。
- SOに不利な差分も、外部体系に不利な差分も同じ形式で記録する。
- 逸脱を発見しても、対象体系そのものの誤りと即断しない。どのEdgeで発生したかを先に確定する。
- 名前を付けられない異常を捨てない。
- 4 primitive以外の新しいclassificationをこのrun中に作らない。

---

## 13. Cross-case audit after Case 4 only

再採点・再分類を先に行わず、変換経路を比較する。

### A. Layer separation
- A/B/Cが各ケースで同じ責務原理により分離されたか。
- BのSO由来成分を外部体系の声へ戻していないか。
- Cを新規創作していないか。

### B. Source-authority transfer
- citation / author / discipline labelが導出を代替したケースはあるか。
- Aのsource authorityがB/Cへ無標識で転送されたケースはあるか。
- `domain-authoritative` という評価者側ラベル自体がauthority cueになっていないか。

### C. Language-game transparency
- 各Layerで何がwarrantとして働いているか可読か。
- warrant modeがLayer間で変わった場所を特定できるか。
- 一つの言語ゲームのclosure conditionが別のLayerへ無標識で輸送されていないか。

### D. Transformation locality
- 観測された異常を、外部体系そのものではなくAB/BC/bypassのどこへ局在できるか。
- 同種の変換には同じprimitiveを適用したか。

### E. Residual preservation
- source disagreement、translation ambiguity、mixed attribution、unnamed anomalyを保持したか。
- 分類できたことを解決済みと扱っていないか。

### F. Final summary
次だけを報告する。

- 各CaseのAB/BC 5軸状態
- Cut / False Link / Both / Unresolvedのanomaly件数
- A -> C bypass suspected cases
- source/citation/labelがprovenanceとして機能した例
- source/citation/labelがwarrantまたはauthority transferとして機能した可能性のある例
- Layer間でwarrant modeが変化した箇所
- 名前を付けずに残した異常
- post-run correctionがある場合、original recordを上書きせず併記

S/E/U/V/Pは報告しない。

---

## English commensuration — minimal execution summary

For each of the four cases, freeze three distinct layers: (A) a source-grounded domain-authoritative description, (B) the actual Optional Axiom description extracted from the fixed fixture, and (C) only the SO/repository-derived interpretation already present in that material. Audit transformation edges A->B and B->C using only Anchor Integrity, Phase Integrity, Path Legibility, Return Reachability, and Open-End Retention. Record anomalies before classification, then project only to Cut, False Link, Both, or Unresolved. Do not use S/E/U/V/P. Do not treat citations, names, disciplines, or the label “authoritative” as automatic warrant. Preserve disagreements, mixed attribution, and unnamed anomalies. Perform cross-case comparison only after all four cases are complete.

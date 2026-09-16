# Scientific Terminology Protocol / 科学語彙接続プロトコル

> Status: Protocol
> Scope: terminology-control
> Language: ja+en
> Claim strength: S0/S1

本文書は、**存在境界論｜Scientific Ontology** が既存科学から借りる語彙をどのように扱うかを定める。

標準科学の定義を無断で上書きしない。
標準科学の定義を置き換えるものではない。
存在境界論内で異なる意味で用いる場合は、その差異を明示する。

## 1. 定義は公開境界の道具である

本リポジトリにおける定義は、探求を固定するためのものではない。思考を狭めるためのものでも、今後の表現をすべて既定語彙へ従属させるためのものでもない。

目的は、伝達可能性を確保することである。

語を定義するのは、読者が何を読んでいるのか、どこで既存語彙と衝突するのか、その主張がどの強度に属するのかを確認できるようにするためである。

定義は公開境界の道具であり、思考の檻ではない。

## 2. 基本原則

### 標準科学の定義を尊重する

エントロピー、因果、質量、スピン、CPT、ファインマンダイアグラム、時空、エンタングルメントなどは、既存科学内で強い定義・計算体系・検証文脈を持つ。

存在境界論は、それを勝手に上書きしない。SO側で非標準な「エンタングルメント」表現を用いる場合は、量子論上のエンタングルメントと同一視しない。

### 読み替えは明示する

標準語を読み替える場合は、読み替えであると明示する。

たとえば「ファインマンダイアグラムを履歴トポロジーとして読む」は、標準QFTの計算道具としてのファインマンダイアグラムを否定しない。そのうえで、相互作用履歴を頂点・辺・経路・ループとして読む存在論的再解釈である、と明記する。

### SO内部定義を明示する

内在時間、ネゲントロピー経済、履歴対応、意味電位、情報履歴質量密度などは、ここで用いる意味において標準科学の定義ではない。

これらを用いる場合は、**Scientific Ontology 内部定義** または **Scientific Ontology 上の概念語** であることを明示する。

### 誤読を招く場合は新語を作る

既存科学の強いタームが、意図しない専門分野上の意味へ読者を引き寄せる場合は、新語またはより慎重な表現を用いる。

たとえば「時空を超える」は危険である。より安全な表現は「外的時空の因果順序に還元されない」である。

### 限定条件を提示する

科学的因果は強力である。本プロジェクトでは、それを外的時空内で高度に安定化した履歴対応として尊重する。

存在境界論は、その因果が安定するための前提を点検する。観測、対象化、観測者履歴、意味変化、責任回収、価値保存、未解決残差の再浮上である。

### 主張領域を混同しない

物理主張、情報主張、認識主張、倫理主張、創作比喩を、黙って混ぜてはならない。

同じ「場」という言葉でも、物理場、情報場、履歴場、社会場、創作上の場は違う。接続はできるが、論証なしに同一視してはならない。

## 3. 用語操作分類

| 操作 | 使う場面 | 表記例 | 主張強度 |
|---|---|---|---|
| 標準借用 | 科学の定義をそのまま使う | 標準物理におけるエントロピー | S0-S1 |
| 構造アナロジー | 似た構造を比喩的に使う | エントロピーに似た拡散 | S1-S2 |
| 存在論的再解釈 | 標準概念を別のFRAMEで読み直す | 履歴場トポロジーでは〜として読む | S2-S3 |
| 限定条件提示 | 科学的説明の適用範囲を示す | 科学的因果は時空内で安定化した履歴対応を扱う | S2-S3 |
| SO再定義 | 標準語を借りて別定義で使う | SO定義における内在時間 | S3-S4 |
| 形式化候補 | 変数・演算・評価指標へ落とす | HFC方程式、意味電位場 | S4 |
| 物理接続候補 | 既存物理と比較可能な強い仮説 | 重力＝同期遅延 | S4-S5 |
| 創作退避 | 理論ではなく比喩・物語装置として使う | 天体構造と精神構造の写像 | S1-S2 |

## 4. 中核注意

Scientific Ontology は、既存科学を否定したり置き換えたりする体系ではない。

ここで行うのは、科学的概念の再解釈、適用条件の明示、観測者履歴や意味生成、境界条件、未解決残差を含む補助的FRAMEの提示である。

既存科学において定義済みの用語を使う場合、その標準定義を尊重する。標準定義とは異なる意味で用いる場合は、Scientific Ontology 内部での定義であることを明示する。

したがって、本体系における「時空を超える」「ネゲントロピー」「履歴場」「内在時間」などの語は、物理的な超光速通信、物理的時間旅行、または過去改変を意味しない。

それらは、外的時空の因果順序だけでは記述しきれない履歴対応、意味変化、責任、価値、未解決残差の再浮上を扱うための存在論的タームである。

## 5. 外部参照と別位相解釈を分ける

科学語彙接続では、標準定義の誤記と、標準定義を保持したうえでの別位相解釈を同じ問題として扱わない。

### 5.1 EXT-REFERENCE-MISSTATEMENT / 外部参照誤記

外部体系`X`の事実・定義`q_X`をSOが表現したものを`Rep_SO(q_X)`とすると、

```text
Rep_SO(q_X) ≢ q_X
```

である場合、`EXT-REFERENCE-MISSTATEMENT`である。

標準初手は`CORRECT-REFERENCE`とする。まずSO側の借用表現を局所修正し、その後にSO hypothesis、対応、bridge claimを再評価する。

これは、外部体系がSO全体を自動的に反証したという意味ではない。同時に、SO独自解釈を理由に借用元の定義誤記を温存してよいという意味でもない。

### 5.2 SAME-FACT-ALT-INTERPRETATION / 同一事実・異位相解釈

共有している事実集合を`F`とし、外部体系とSOがそれぞれ`I_{phi_X}(F)`、`I_{phi_SO}(F)`として読む場合、

```text
I_{phi_SO}(F) != I_{phi_X}(F)
```

であっても、事実集合と標準定義が保持されているなら、直ちに参照誤記ではない。

この場合の標準初手は`COMMENSURATION-INTAKE`であり、fact / interpretation / derivation / bridge claimを区別できる接触面を共有できるか確認する。

非標準であることだけを理由に撤回しない。逆に「別位相だから」という理由で既知事実との真正な衝突を無効化しない。

### 5.3 AssessmentとPublicationを分ける

外部未確立、外部非導出、外部既知事実衝突、SO内部非導出、SO内部defeater、外部参照誤記、別位相解釈、相互bridge係争は、Repository Assessment Protocolのfinding typeとして扱う。

公開上の誤読、操作、安全、保全性、private boundaryはPublication / Safety governanceで扱う。

したがって、旧`E / Epistemic Risk`を科学語彙の真偽判定や公開可否の単一尺度として使用しない。

参照先：

- [`../Assessment/Repository_Assessment_Protocol.ja.md`](../Assessment/Repository_Assessment_Protocol.ja.md)
- [`../Assessment/Repository_Assessment_Protocol.en.md`](../Assessment/Repository_Assessment_Protocol.en.md)
- [`../Publication_and_Commensuration_Policy.md`](../Publication_and_Commensuration_Policy.md)

## 6. 用語衝突管理表との関係

本プロトコルは、科学語彙をどのように扱うかを定める。

用語衝突管理表は、実際の公開語が既存の言語ゲームとどこで衝突するかを記録する。

参照先：

## 7. 要約

本プロトコルの要点は単純である。

1. 標準科学の定義を尊重する。
2. 読み替えは明示する。
3. Scientific Ontology 内部定義を明示する。
4. 既存語が誤読を招く場合は新語を作る。
5. 限定条件を提示する。
6. 物理・情報・認識・倫理・創作の主張領域を混同しない。
7. 外部参照誤記と、同一事実への別位相解釈を区別する。
8. Assessment findingとPublication / Safety handlingを区別する。

---

## English commensurated rendering

This document defines how **存在境界論｜Scientific Ontology** uses terms borrowed from established sciences.

It does not redefine scientific terms without notice.
It does not claim to replace standard scientific definitions.
When Scientific Ontology uses a term differently, the difference must be stated explicitly.

## 1. Definitions Are Boundary Tools

Definitions in this repository are not meant to freeze inquiry, narrow thought, or force every later expression into a fixed vocabulary.

Their purpose is communicability.

Terms are defined so that readers can understand what is being said, where existing terminology may collide, and which claim-strength level a statement belongs to.

Definitions are public boundary tools. They are not cages for thought.

## 2. Core Principles

### 2.1 Respect Standard Scientific Definitions

Terms such as entropy, causality, mass, spin, CPT, Feynman diagram, spacetime, and entanglement have strong definitions, mathematical systems, and verification contexts within established sciences.

Scientific Ontology does not overwrite those definitions. Where SO uses non-standard "entanglement" language, it must not be identified with quantum entanglement.

### 2.2 Mark Reinterpretation Explicitly

When a standard term is reinterpreted, the reinterpretation must be stated as such.

For example, reading a Feynman diagram as a history-topological figure does not deny the standard QFT use of Feynman diagrams as calculation tools. It is an ontological reinterpretation of interaction history through vertices, edges, paths, and loops.

### 2.3 Define SO-Specific Usage

Terms such as intrinsic time, negentropy economy, history correspondence, semantic potential, and information-history mass density are not standard scientific terms in the sense used here.

When such terms are used, the document should state that they are **Scientific Ontology internal definitions** or **Scientific Ontology conceptual terms**.

### 2.4 Create New Terms When Existing Terms Mislead

When an existing scientific term strongly pulls the reader toward an unintended disciplinary meaning, a new term or more careful phrase should be used.

For example, “beyond spacetime” is risky. A safer expression is “not reducible to external spacetime causal order.”

### 2.5 State Boundary Conditions

Scientific causality is powerful. In this project, it is respected as a highly stabilized form of history correspondence within external spacetime.

Scientific Ontology examines the assumptions under which such causality becomes stable: observation, objectification, observer history, meaning change, responsibility recovery, value preservation, and the reappearance of unresolved residuals.

### 2.6 Do Not Collapse Claim Domains

Physical claims, informational claims, epistemological claims, ethical claims, and creative metaphors must not be silently mixed.

The same word “field” may refer to a physical field, information field, history-field, social field, or creative field. They may be connected, but they must not be treated as identical without argument.

## 3. Usage Classes

| Operation | When to use | Example wording | Claim strength |
|---|---|---|---|
| Standard borrowing | Using a scientific term in its established sense | entropy in standard physics | S0-S1 |
| Structural analogy | Comparing similar structure without identity claim | diffusion-like behavior | S1-S2 |
| Ontological reinterpretation | Reading an established concept through an SO frame | in History-Field Topology, this may be read as... | S2-S3 |
| Boundary-condition statement | Clarifying the scope of scientific explanation | scientific causality handles stabilized history correspondence within spacetime | S2-S3 |
| SO internal definition | Using a term in a defined SO-specific sense | intrinsic time in Scientific Ontology | S3-S4 |
| Formalization candidate | Candidate variables, operations, or evaluation criteria | HFC equation, semantic potential field | S4 |
| Physical correspondence candidate | Strong hypothesis that may face existing physics | gravity as synchronization delay | S4-S5 |
| Creative or literary use | Metaphor or story device, not theory claim | cosmological structure as literary figure | S1-S2 |

| 操作 | 使う場面 | 表記例 | 主張強度 |
|---|---|---|---|
| 標準借用 | 科学の定義をそのまま使う | 標準物理におけるエントロピー | S0-S1 |
| 構造アナロジー | 似た構造を比喩的に使う | エントロピーに似た拡散 | S1-S2 |
| 存在論的再解釈 | 標準概念を別のFRAMEで読み直す | 履歴場トポロジーでは〜として読む | S2-S3 |
| 限定条件提示 | 科学的説明の適用範囲を示す | 科学的因果は時空内で安定化した履歴対応を扱う | S2-S3 |
| SO再定義 | 標準語を借りて別定義で使う | SO定義における内在時間 | S3-S4 |
| 形式化候補 | 変数・演算・評価指標へ落とす | HFC方程式、意味電位場 | S4 |
| 物理接続候補 | 既存物理と比較可能な強い仮説 | 重力＝同期遅延 | S4-S5 |
| 創作退避 | 理論ではなく比喩・物語装置として使う | 天体構造と精神構造の写像 | S1-S2 |

## 4. Core Warning

Scientific Ontology is not a system for denying or replacing established science.

It offers scientific concept reinterpretation, scope clarification, and auxiliary frames that include observer history, meaning generation, boundary conditions, and unresolved residuals.

When a term already has a standard scientific definition, that definition must be respected. When a term is used differently, the document must state that the usage is internal to Scientific Ontology.

Therefore, terms such as “beyond spacetime,” “negentropy,” “history-field,” and “intrinsic time” do not imply superluminal communication, physical time travel, or alteration of the past.

They are ontological terms for history correspondence, meaning change, responsibility, value, and unresolved residuals that cannot be fully described by external spacetime causal order alone.

## 5. Separate External Reference Integrity from Alternate Interpretation

Scientific terminology contact must not collapse a misstatement of a standard definition into a different interpretation that preserves the standard definition.

### 5.1 EXT-REFERENCE-MISSTATEMENT

Let `q_X` be a fact or definition owned by external system `X`, and `Rep_SO(q_X)` be Scientific Ontology's representation of it.

```text
Rep_SO(q_X) ≢ q_X
```

When this holds, record `EXT-REFERENCE-MISSTATEMENT`.

The default first action is `CORRECT-REFERENCE`: locally correct SO's borrowed representation first, then reassess the SO hypothesis, correspondence, or bridge claim.

This does not mean that the external system has automatically falsified Scientific Ontology as a whole. It also does not permit SO to preserve a borrowed-definition error by appealing to its own interpretation.

### 5.2 SAME-FACT-ALT-INTERPRETATION

Let `F` be a shared fact set, read by the external system and SO as `I_{phi_X}(F)` and `I_{phi_SO}(F)`.

```text
I_{phi_SO}(F) != I_{phi_X}(F)
```

If the fact set and standard definitions are preserved, this difference is not automatically a reference misstatement.

The default first action is `COMMENSURATION-INTAKE`: establish whether fact, interpretation, derivation, and bridge claim can be distinguished on a shared contact surface.

Do not withdraw a hypothesis merely because its interpretation is non-standard. Conversely, do not use "alternate interpretation" to erase a genuine conflict with established facts.

### 5.3 Separate Assessment from Publication

External non-establishment, external non-derivability, external fact conflict, SO non-derivability, SO defeaters, external reference misstatement, alternate interpretation, and reciprocal bridge dispute are finding types owned by the Repository Assessment Protocol.

Risks of public misreading, operational misuse, safety, integrity, and private-boundary exposure belong to Publication / Safety governance.

The legacy `E / Epistemic Risk` must therefore not be used as a single truth or publication scale for scientific terminology.

See:

- [`../Assessment/Repository_Assessment_Protocol.ja.md`](../Assessment/Repository_Assessment_Protocol.ja.md)
- [`../Assessment/Repository_Assessment_Protocol.en.md`](../Assessment/Repository_Assessment_Protocol.en.md)
- [`../Publication_and_Commensuration_Policy.md`](../Publication_and_Commensuration_Policy.md)

## 6. Relation to Term Collision Registry

This protocol defines how scientific vocabulary should be handled.

The term collision registries record where actual public terms collide with existing language games.

Use:

- [`TERM_COLLISION_REGISTRY.ja.md`](TERM_COLLISION_REGISTRY.ja.md) for Japanese canonical terms;
- [`TERM_COLLISION_REGISTRY.en.md`](TERM_COLLISION_REGISTRY.en.md) for English renderings.

- 日本語正本語: [`TERM_COLLISION_REGISTRY.ja.md`](TERM_COLLISION_REGISTRY.ja.md)
- 英語通約語: [`TERM_COLLISION_REGISTRY.en.md`](TERM_COLLISION_REGISTRY.en.md)

## 7. Summary

The protocol is simple:

1. Respect standard scientific definitions.
2. Mark reinterpretations explicitly.
3. Define Scientific Ontology internal usage.
4. Create new terms when existing terms mislead.
5. State boundary conditions.
6. Do not collapse physical, informational, epistemological, ethical, and creative claim domains.
7. Distinguish epistemic risk from application and safety risk.

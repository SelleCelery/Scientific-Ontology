# Scientific Ontology System Map / 存在境界論 体系マップ

> Layer: 00_Overview  
> Status: Map  
> Scope: repository architecture / operational orientation / conceptual layers / public boundary / governance / research dynamics
> Language: ja+en  
> Public profile: P0-P1  
> Claim strength: Repository and concept-architecture map; not an empirical claim  
> Authority: Human-readable system map; current file relations are maintained in `tools/docs_manifest.yml`

---

# 日本語正本

## 0. この体系マップの役割

本文書は、**存在境界論｜Scientific Ontology** の公開リポジトリを、次の三つの側面から示す体系マップである。

1. **概念体系**：各層が、構造、通信内容、規約、応用、研究ノートとして何を担当するか。
2. **公開体系**：どの文書が公開入口、正本、通約、主張強度管理、用語管理を担当するか。
3. **リポジトリ体系**：文書、メタファイル、チェッカー、非公開境界がどこに配置されるか。

本文書は個別概念の詳細定義を所有しない。概念の公開定義所有者と文書関係は、[`GLOSSARY.md`](../GLOSSARY.md)および[`tools/docs_manifest.yml`](../tools/docs_manifest.yml)で管理する。

公開対象の判定は、原則としてルートの[`.gitignore`](../.gitignore)に従う。

---

## 1. 公開体系の中心定義

存在境界論は、存在そのものを直接所有し、最終的に記述し尽くす体系ではない。

公開上、実在的に扱う中心対象は、次である。

- 境界
- 接触
- 履歴
- 返り
- 残差・残渣
- 後続条件
- 再照合可能性

これらを通じて、存在がどのように現れ、認識され、意味を持ち、他の存在、制度、環境、未来へ作用するかを記述する。

存在境界論は、主観側、客観側、横断研究、その他の異なる言語ゲームのどれか一つを最終言語として選ぶことから始めない。それぞれの成立条件、観測範囲、主張強度、限界を保持したまま、境界へ持ち寄って照合できる場を整えること自体を研究対象とする。通約は同一化ではなく、差異、非同一性、残差、返路を追跡可能にする操作である。

また、v5系開始時に追加された[`Scientific_Ontology_Operational_Outline.ja.md`](./Scientific_Ontology_Operational_Outline.ja.md)は、境界事件、作用、返り、責任分界、可動性という運用方向を提示する。これは新しい上位公理ではなく、既存概念を外部実装へ持ち出すための全体方針である。

公開体系では、境界認識批判から認識生成、言語・意味・通信位相の横断基盤、認識運用、実装、返送へ至る次の連続を明示する。

```text
境界認識批判
  ↓
境界認識生成
  ↓
言語・意味・通信位相の横断基盤
  ↓
境界認識運用
  ↓
目的・通信・組織への実装
  ↓
倫理・社会設計・平和仕様
  ↓
残差・異議・実装結果の返送
```

---

## 2. リポジトリ全体の構造

公開リポジトリは、次の四領域に分かれる。

| 領域 | 主な場所 | 役割 |
|---|---|---|
| 公開入口 | ルート、`00_Overview` | 全体説明、読解経路、概念地図、Roadmap、Glossary |
| 理論・応用本文 | `01`–`06` | 基礎構造、通信内容、規約、応用、研究ノート、視覚資料 |
| リポジトリ統治 | `90_Repository_Governance`、`tools`、`scripts`、`.github` | 通約、用語衝突、形式、文書関係、検査 |
| 公開境界 | `99_Private_Core_Not_Included`、`.gitignore` | 非公開中核と公開除外対象の境界表示 |

---

## 3. 公開リポジトリ構造

以下は、`.gitignore`で除外される000系草稿、ローカル環境、キャッシュ、検査出力、作業メモを含まない公開構造である。

```text
.
├─ README.md
├─ GLOSSARY.md
├─ Roadmap.md
├─ RELEASE_NOTES.md
├─ CITATION.md
├─ CITATION.cff
├─ LICENSE.md
├─ .zenodo.json
├─ .gitattributes
├─ .gitignore
├─ requirements-public-check.txt
│
├─ 00_Overview/
│  ├─ README.md
│  ├─ Scientific_Ontology_Operational_Outline.ja.md
│  ├─ Scientific_Ontology_Operational_Outline.en.md
│  ├─ Scientific_Ontology_System_Map.md
│  ├─ Scientific_Ontology_Concept_Network.ja.md
│  ├─ Scientific_Ontology_Concept_Network.en.md
│  ├─ Truth_Management_and_Boundary_PDCA.ja.md
│  ├─ Truth_Management_and_Boundary_PDCA.en.md
│  ├─ Claim_Strength_and_Publication_Layer_Table.ja.md
│  ├─ Claim_Strength_and_Publication_Layer_Table.en.md
│  ├─ Physics_Correspondence_Policy.ja.md
│  └─ Physics_Correspondence_Policy.en.md
│
├─ 01_Sat_Truth/
│  ├─ README.md
│  ├─ AMP_Introduction.md
│  ├─ Four_Axioms_of_Existence.md
│  ├─ Meaning_Generation_Model.md
│  ├─ Boundary_Realism_Principle.md
│  ├─ Boundary_Epistemological_Critique.ja.md
│  ├─ Boundary_Epistemological_Critique.en.md
│  ├─ Boundary_Epistemological_Critique_Annotations.ja.md
│  └─ Boundary_Epistemological_Critique_Annotations.en.md
│
├─ 02_Raj_Beauty/
│  ├─ README.md
│  ├─ HFC_Introduction.md
│  ├─ History_Field_Topology.md
│  ├─ Scientific_Ontology_and_Science.md
│  ├─ Entropy_Attributed_Difference_and_Cognitive_Axis_Formation.ja.md
│  └─ Entropy_Attributed_Difference_and_Cognitive_Axis_Formation.en.md
│
├─ 03_Tam_Goodness/
│  ├─ README.md
│  ├─ Boundary_Ethics_Model.md
│  ├─ Meaning_as_Return_Orbit.md
│  ├─ Optional_Axiom_Modules_as_Cognitive_Bridge.ja.md
│  └─ Optional_Axiom_Modules_as_Cognitive_Bridge.en.md
│
├─ 04_Applications/
│  ├─ README.md
│  ├─ AI_Adaptation/
│  │  ├─ README.md
│  │  ├─ Application_Boundary_Theory_Core.md
│  │  ├─ AI_Usefulness_as_a_Boundary_Function.md
│  │  ├─ AI_Boundary_Interface_and_Synchronous_Understanding.md
│  │  └─ AI_Personality_as_Response_Structure.md
│  └─ Social_Boundary_Design/
│     ├─ README.md
│     ├─ AI_Adoption_Collation_Checklist.md
│     ├─ Specification_for_Peace.ja.md
│     └─ Specification_for_Peace.en.md
│
├─ 05_Research_Notes/
│  ├─ README.md
│  ├─ Research_Notes_Index.md
│  ├─ Cognitive_Dynamics_Communication_Studies/
│  │  ├─ README.md
│  │  ├─ Cognitive_Dynamics_Communication_Model.ja.md
│  │  ├─ Cognitive_Dynamics_Communication_Model.en.md
│  │  ├─ Compression_of_Existence_Phases.ja.md
│  │  ├─ Compression_of_Existence_Phases.en.md
│  │  ├─ Boundary_Diplomacy_and_Port_Allocation.ja.md
│  │  ├─ Boundary_Diplomacy_and_Port_Allocation.en.md
│  │  ├─ Organizational_Boundary_and_Port_Model.ja.md
│  │  └─ Organizational_Boundary_and_Port_Model.en.md
│  ├─ Cross_Domain_Ontological_Notes/
│  │  ├─ README.md
│  │  ├─ Asymmetry_Stabilization_and_ReCollation.ja.md
│  │  ├─ Asymmetry_Stabilization_and_ReCollation.en.md
│  │  ├─ Return_Ethics_and_Retaliation_Conversion.ja.md
│  │  ├─ Return_Ethics_and_Retaliation_Conversion.en.md
│  │  ├─ Narrative_Truth_and_Structural_Reading.ja.md
│  │  ├─ Narrative_Truth_and_Structural_Reading.en.md
│  │  ├─ Consent_Boundary_and_Sentence_Bit_Asymmetry.ja.md
│  │  └─ Consent_Boundary_and_Sentence_Bit_Asymmetry.en.md
│  ├─ Language_Meaning_and_Communication_Phase_Studies/
│  │  ├─ README.md
│  │  ├─ Grammar_as_a_Meaning_Pressure_Channel.ja.md / .en.md
│  │  ├─ Meaning_as_Collation_and_Return_Path.ja.md / .en.md
│  │  ├─ Compressed_Experience_Qualia_and_Literature.ja.md / .en.md
│  │  ├─ AI_Language_Generation_and_Grammatical_Frames.ja.md / .en.md
│  │  ├─ Speech_as_Sequential_Decompression.ja.md / .en.md
│  │  ├─ Intension_Extension_and_False_Extension.ja.md / .en.md
│  │  ├─ Semantic_Network_Topology_and_Commensuration_Bandwidth.ja.md / .en.md
│  │  ├─ Commensuration_as_Cross_Grammatical_Collation.ja.md / .en.md
│  │  ├─ Linguistic_Frame_Differences_between_Japanese_and_English.ja.md / .en.md
│  │  └─ Return_Intake_Log.ja.md / .en.md
│  ├─ Physical_Cosmological_Notes/
│  │  ├─ README.md
│  │  ├─ Intrinsic_Time_Standard_Model_Correspondence.ja.md
│  │  ├─ Intrinsic_Time_Standard_Model_Correspondence.en.md
│  │  ├─ Ontological_History_of_the_Universe.ja.md
│  │  ├─ Ontological_History_of_the_Universe.en.md
│  │  ├─ Cosmological_Topological_Dynamics.ja.md
│  │  ├─ Cosmological_Topological_Dynamics.en.md
│  │  ├─ PINGER_Hypothesis_and_History_Field_Topology.ja.md
│  │  ├─ PINGER_Hypothesis_and_History_Field_Topology.en.md
│  │  ├─ Chaos_Theory_and_Logical_Depth_Axis.ja.md
│  │  └─ Chaos_Theory_and_Logical_Depth_Axis.en.md
│  ├─ Social_Boundary_Notes/
│  │  ├─ README.md
│  │  ├─ AI_Adoption_as_Synchronization_Closure.md
│  │  ├─ DSSI_Observation_Judgment_Sovereignty_and_Responsibility_Return.ja.md
│  │  ├─ DSSI_Observation_Judgment_Sovereignty_and_Responsibility_Return.en.md
│  │  ├─ Negentropy_Economy_Principles.ja.md
│  │  ├─ Negentropy_Economy_Principles.en.md
│  │  ├─ Negentropy_Economy_and_Meaning_Generation.ja.md
│  │  └─ Negentropy_Economy_and_Meaning_Generation.en.md
│  ├─ AI_Personality_Notes/
│  │  ├─ README.md
│  │  ├─ History_Loop_Radius_and_Return_Stability.md
│  │  └─ Logical_Sandbox_and_Negentropy_Model.md
│  └─ Literary_Ontological_Notes/
│     ├─ README.md
│     ├─ reading-blue-light.ja.md
│     ├─ reading-blue-light.en.md
│     ├─ Meifu_Bureau_Reincarnation_and_Belief_Gravity.md
│     ├─ Literature_as_Worldmaking.ja.md
│     └─ Literature_as_Worldmaking.en.md
│
├─ 06_Visual_Materials/
│  ├─ README.md
│  ├─ Scientific_Ontology_Conceptual_Poster.ja.png
│  ├─ Scientific_Ontology_Conceptual_Poster.en.png
│  └─ Scientific_Ontology_Conceptual_Poster_Note.md
│
├─ 90_Repository_Governance/
│  ├─ README.md
│  ├─ Publication_and_Commensuration_Policy.md
│  ├─ Translation_Note.md
│  ├─ Release_Update/
│  │  ├─ UPDATE_PACK.md
│  │  ├─ release_state.yml
│  │  ├─ release_update.py
│  │  └─ requirements.txt
│  └─ Terminology/
│     ├─ README.md
│     ├─ Scientific_Terminology_Protocol.md
│     ├─ TERM_COLLISION_REGISTRY.ja.md
│     └─ TERM_COLLISION_REGISTRY.en.md
│
├─ 99_Private_Core_Not_Included/
│  └─ README.md
│
├─ tools/
│  ├─ Public_Format_Registry.yml
│  ├─ docs_manifest.yml
│  ├─ maintenance_rules.yml
│  └─ CHECKER_USAGE.md
├─ scripts/
│  └─ check_public_format.py
└─ .github/workflows/
   └─ public-format-check.yml
```

---

## 4. ルート直下の役割

ルートは、理論本文の置き場ではなく、リポジトリ全体へ入るための公開インターフェースである。

| 文書 | 役割 |
|---|---|
| [`README.md`](../README.md) | 初見読者向けの入口、体系の中心的な研究運動、目的別読解経路 |
| [`GLOSSARY.md`](../GLOSSARY.md) | 標準語、英語通約、概念系譜、公開定義所有者の人間可読インターフェース |
| [`Roadmap.md`](../Roadmap.md) | 研究動態、現在地、次の反証・実装課題 |
| [`RELEASE_NOTES.md`](../RELEASE_NOTES.md) | 版ごとの変更記録 |
| [`CITATION.md`](../CITATION.md) / [`CITATION.cff`](../CITATION.cff) | 人間向け・機械向け引用情報 |
| [`LICENSE.md`](../LICENSE.md) | 利用条件 |
| [`.zenodo.json`](../.zenodo.json) | Zenodo向けメタデータ |

Glossaryは統治文書の一種でもあるが、公開概念の横断入口として発見可能性が高いため、ルートに置く。

---

## 5. `00_Overview` — 公開体系の地図と研究動態

`00_Overview`は、理論本文より前に、現在の公開体系をどのように読むかを示す層である。

中心的な役割は次である。

- 存在境界論全体の運用方針を示す。
- 概念体系の入口を示す。
- リポジトリ構造を示す。
- 研究動態と目的循環を示す。
- 主張強度、公開層、未確定性を管理する。
- 物理近接語彙との接続条件を示す。

主要文書：

- [`Scientific_Ontology_Operational_Outline.ja.md`](./Scientific_Ontology_Operational_Outline.ja.md)：v5系開始時に自覚された全体運用方針。新しい上位公理ではなく、外部実装へ向けた運用方向を示す。
- [`Scientific_Ontology_Concept_Network.ja.md`](./Scientific_Ontology_Concept_Network.ja.md)：概念配置、読解経路、定義所有、返路、アポリアの入口。
- [`Scientific_Ontology_System_Map.md`](./Scientific_Ontology_System_Map.md)：リポジトリと概念層の体系配置。
- [`Truth_Management_and_Boundary_PDCA.ja.md`](./Truth_Management_and_Boundary_PDCA.ja.md)：第一義、共有、世界形成、Boundary PDCAを通じた研究・運用循環。
- [`Claim_Strength_and_Publication_Layer_Table.ja.md`](./Claim_Strength_and_Publication_Layer_Table.ja.md)：主張強度、証拠強度、未確定性、公開層の管理。
- [`Physics_Correspondence_Policy.ja.md`](./Physics_Correspondence_Policy.ja.md)：物理近接語彙と標準物理学の非同一性を管理する方針。

`00_Overview`は単なるメタ説明ではない。基礎概念がどのように認識、研究動態、実装へ展開するかを示す上位の読解面として機能する。

---

## 6. `01`–`03` — 中核三層の構造的役割

`01_Sat_Truth`、`02_Raj_Beauty`、`03_Tam_Goodness`は、主題別フォルダというより、通信体系における異なる責務を持つ。

| 層 | 通信構造上の役割 | 公開体系で前景化する役割 | 文書が置かれやすい理由 |
|---|---|---|---|
| `01_Sat_Truth` | ネットワーク構造と成立条件 | 境界認識批判 | 形而上学、公理、存在・観測・意味・知の成立条件を扱うため |
| `02_Raj_Beauty` | 通信内容、事象流、受容と読み方 | 境界認識生成 | 履歴、差分、注意、抽象化、同期、認識軸の形成を扱うため |
| `03_Tam_Goodness` | 通信規約、管理、閉鎖、再開、返送 | 境界認識運用 | 倫理、通約、保留、偽閉鎖回避、非破壊的管理を扱うため |

### 6.1 `01_Sat_Truth` — ネットワーク構造と成立条件

この層は、何が流れるかより前に、接触、観測、意味、知が成立しうる構造を扱う。

形而上学的根を直接前景化するだけでなく、境界実在性と境界認識批判を通じて、観測可能な境界条件へ記述を寄せる。

### 6.2 `02_Raj_Beauty` — 通信内容と読みの生成

この層は、構造を流れる履歴、差分、意味圧、同期・非同期と、それらがどのように受け取られ、認識方向として安定するかを扱う。

`Entropy_Attributed_Difference_and_Cognitive_Axis_Formation`は、境界認識批判の後に、認識軸がどのように生成・安定・変形するかを記述する。

### 6.3 `03_Tam_Goodness` — 通信規約と管理

この層は、通信内容の正しさだけでなく、何を受け入れ、保留し、閉じ、再開し、返送するかを扱う。

`Optional_Axiom_Modules_as_Cognitive_Bridge`は、異なる認識形式を同一化も切断もせず、比較、通約、条件付き接続するための運用構造を提供する。

---

## 7. `04_Applications` — 公開応用インターフェース

`04_Applications`は、中核三層の概念を、公開可能な設計思想、評価枠、チェックリスト、仕様書へ接続する。

### `AI_Adaptation`

AIを、判断代行主体ではなく、判断可能性を維持する境界インターフェースとして扱う。

主な対象：

- AI有用性
- AI境界インターフェース
- 応答構造としてのAI人格
- 応用境界理論

### `Social_Boundary_Design`

AIや制度を採用する社会側の境界、責任、照合、平和条件を扱う。

主な対象：

- AI導入照合チェックリスト
- 責任境界と再照合可能性
- 平和プロトコル・平和仕様

この層は、実装コード、製品仕様、法的助言、個別組織の非公開運用手順を含まない。

---

## 8. `05_Research_Notes` — 強い命題を境界条件つきで保持する層

`05_Research_Notes`は、公開基礎層へ直接入れるには主張強度または誤読リスクが高いが、捨てずに保持すべき研究線を置く。

### `Language_Meaning_and_Communication_Phase_Studies`

言語、意味、文法、発話、通約、意味ネットワーク、AI言語生成を、返路を含む通信位相として扱う横断研究線。v5系では最初のLiving Canonical運用線として、変更履歴とReturn Intakeを明示的に持つ。

この研究線は、意味生成モデルを置換しない。言語的意味を局所所有し、既存の意味、HFC、認識論、AI応用へ残差を返す。

### `Cognitive_Dynamics_Communication_Studies`

認識が通信的にはシームレスでありながら、実際の運用では存在相、ポート、容量、責任へ離散化される構造を扱う。

この研究線は、認識動態から組織境界、責任境界、境界外交、平和仕様へ接続する。

### `Cross_Domain_Ontological_Notes`

非対称性、返りの倫理、報復変換、物語的真理、同意境界とsentence/bit非対称など、複数分野を横断する存在論的読解を置く。

### `Physical_Cosmological_Notes`

内在時間、宇宙史、PINGER仮説、カオス理論、論理-深度軸など、物理・宇宙論近接の高強度仮説を置く。

### `Social_Boundary_Notes`

AI導入、ネゲントロピー経済、意味生成、社会境界、DSSIの観測・判断主権・責任返還に関する研究ノートを置く。DSSIアプリケーション本体はv5.0には含まれない。

### `AI_Personality_Notes`

AI人格、履歴ループ、帰還安定性、論理サンドボックスを研究ノートとして扱う。

### `Literary_Ontological_Notes`

文学を証拠として使用するのではなく、境界、履歴、意味、信念重力、世界制作としての文学を読む存在論的読解として扱う。

各文書の詳細は、[`Research_Notes_Index.md`](../05_Research_Notes/Research_Notes_Index.md)を参照する。

---

## 9. `06_Visual_Materials` — 視覚的公開入口

この層は、概念ポスターと読解注記を置く。

視覚資料は、理論本文、実証資料、形式的証明の代替ではない。概念体系へ複数方向から入るための補助インターフェースである。

---

## 10. `90_Repository_Governance` — リポジトリ統治

この領域は研究本文ではなく、公開・通約・用語・概念所有・衝突管理を統治する。

| 文書 | 役割 |
|---|---|
| [`Publication_and_Commensuration_Policy.md`](../90_Repository_Governance/Publication_and_Commensuration_Policy.md) | 正本関係、通約保存契約、言語形式、概念所有と系譜 |
| [`Translation_Note.md`](../90_Repository_Governance/Translation_Note.md) | 文書横断で反復する英語通約判断 |
| [`Scientific_Terminology_Protocol.md`](../90_Repository_Governance/Terminology/Scientific_Terminology_Protocol.md) | 科学語彙、SO定義、標準定義、限定条件の運用規約 |
| [`TERM_COLLISION_REGISTRY.ja.md`](../90_Repository_Governance/Terminology/TERM_COLLISION_REGISTRY.ja.md) | 日本語正本語の衝突面 |
| [`TERM_COLLISION_REGISTRY.en.md`](../90_Repository_Governance/Terminology/TERM_COLLISION_REGISTRY.en.md) | 英語通約語の衝突面 |

役割分担は次である。

```text
GLOSSARY.md
  現在の標準語と人間可読な概念系譜

Publication and Commensuration Policy
  正本・通約・所有・公開境界の原則

Term Collision Registries
  既存語彙との衝突面と誤読方向

Translation Note
  反復的な通約判断

tools/*.yml
  機械可読な形式・関係・保守規則
```

---

### Release Update / リリース更新

`90_Repository_Governance/Release_Update`は、版ごとの公開事実を`release_state.yml`へ集約し、`release_update.py`によって`RELEASE_NOTES.md`、`CITATION.cff`、`CITATION.md`、`.zenodo.json`を同期する。README、Roadmap、Concept Network、System Map、Glossary等の意味内容は自動生成せず、人間所有の構造文書としてレビューする。

## 11. `tools`・`scripts`・`.github` — 機械可読統治と検査

| ファイル | 役割 |
|---|---|
| [`tools/Public_Format_Registry.yml`](../tools/Public_Format_Registry.yml) | 文書種別、メタデータ、言語形式、公開チェック構造 |
| [`tools/docs_manifest.yml`](../tools/docs_manifest.yml) | 文書一覧、概念所有、imports、exports、tests、returns、delegates |
| [`tools/maintenance_rules.yml`](../tools/maintenance_rules.yml) | 用語置換、競合防止、公開境界、警告条件 |
| [`scripts/check_public_format.py`](../scripts/check_public_format.py) | Markdown、リンク、メタデータ、関係の公開前検査 |
| [`.github/workflows/public-format-check.yml`](../.github/workflows/public-format-check.yml) | push・pull request時の自動検査 |

機械可読ファイルは理論本文を置き換えない。本文と機械可読記録に差異が生じた場合、その差異自体を照合対象とする。

---

## 12. `99_Private_Core_Not_Included` — 非公開境界の標識

このディレクトリは、非公開中核の内容を説明する場所ではない。

公開リポジトリが、AMP Core全文、ITS理論全文、非公開ランタイム、人格Core、内部評価、詳細な実装・運用パラメータを含まないことを示す境界標識である。

非公開素材の題名、パス、対応表、索引を増やしてはならない。

---

## 13. 研究動態と返路

この体系は、上から下へ一方向に適用される階層ではない。

```text
01 構造と成立条件
  ↓
02 差分・履歴・認識方向
  ↓
05 横断基盤：言語・意味・通信位相
  ↓
03 規約・倫理・通約・管理
  ↓
04 公開応用
  ↓
05 高強度研究・横断研究
  ↓
実装結果・批判・残差
  ↓
00 概念ネットワーク・Truth Management
  ↓
01–03の正本所有文書へ返送
```

研究動態とは、根拠へ深く降りることで、表層において記述、比較、実装、再照合できる領域を増やす運動である。v5系では、この循環を代謝型に明示し、研究ノートを他領域へ持ち出した結果、批判、失敗、残差、実装上の盲点が返れば、その返りを上流文書の更新理由として扱う。

倫理は、その運動の外部に置かれた応用ではない。壊さずに接触し、全面切断せずに停止し、差異を同一化せずに通信する必要が、認識、ポート、責任、組織の記述解像度を引き上げる。

---

## 14. 公開除外規則

`.gitignore`に従い、次は公開構造へ含めない。

- basenameが`000`で始まる草稿・作業ファイル
- `.venv/`、`venv/`
- `__pycache__/`、`*.pyc`等のキャッシュ
- `public_format_report.md`、`public_format_report.json`
- ローカルIDE・OS・一時ファイル
- checker拡張作業メモ、YAMLリファクタリング作業メモ
- 非公開中核、内部ログ、詳細な実装・運用資料

000系ファイルが配布前ZIPに一時的に含まれていても、公開追跡・公開アーカイブへは含めない。

---

## 15. 読解入口

目的別の入口は次である。

- 全体を短時間で把握する：[`README.md`](../README.md) → [`Scientific_Ontology_Operational_Outline.ja.md`](./Scientific_Ontology_Operational_Outline.ja.md) → [`Scientific_Ontology_Concept_Network.ja.md`](./Scientific_Ontology_Concept_Network.ja.md)
- 基底を読む：[`Four_Axioms_of_Existence.md`](../01_Sat_Truth/Four_Axioms_of_Existence.md) → [`Boundary_Realism_Principle.md`](../01_Sat_Truth/Boundary_Realism_Principle.md)
- 境界認識を読む：境界認識批判 → 認識軸生成 → 選択公理モジュール → Truth Management
- 言語・意味・通信位相を読む：[`Language, Meaning, and Communication Phase Studies`](../05_Research_Notes/Language_Meaning_and_Communication_Phase_Studies/README.md) → 個別9研究 → Return Intake
- 倫理・組織・平和を読む：Cognitive Dynamics → Port Allocation → Organizational Boundary → Specification for Peace
- 物理近接研究を読む：Physics Correspondence Policy → Physical Cosmological Notes
- 公開・通約規則を確認する：Glossary → Publication and Commensuration Policy → Term Collision Registries

---

## 16. 保守原則

このSystem Mapは、文書を追加するたびに完全な理論説明を書き換えるための一覧ではない。

更新が必要なのは、次の場合である。

- ディレクトリの構造的責務が変わる。
- 公開入口または読解経路が変わる。
- 新しい研究領域が独立ディレクトリになる。
- 統治文書または機械可読メタファイルの配置が変わる。
- 公開境界または`.gitignore`の公開許可構造が変わる。

個別ファイルの追加・削除は、各README、manifest、Release Notesで管理する。

ただし、全体運用方針、新しい横断研究線、公開入口の変更が生じた場合は、ルートREADME、Roadmap、`00_Overview/README.md`、Concept Network、System Map、Glossary、Research Notes Indexを一つの構造更新単位としてレビューする。

---

# English Commensurated Version

## 0. Role of This System Map

This document presents the public repository of **Scientific Ontology** from three perspectives.

1. **Conceptual system:** what each layer is responsible for as structure, communicative content, protocol, application, or research note.
2. **Publication system:** which documents serve as public entrances, authoritative sources, commensurated renderings, claim-strength controls, and terminology interfaces.
3. **Repository system:** where documents, metadata files, validation tools, and private-boundary notices are located.

This document does not own the detailed definitions of individual concepts. Human-readable public definition ownership and conceptual lineage are maintained in [`GLOSSARY.md`](../GLOSSARY.md), while machine-readable document relations are maintained in [`tools/docs_manifest.yml`](../tools/docs_manifest.yml).

Public inclusion is governed in principle by the root [`.gitignore`](../.gitignore).

---

## 1. Central Public Position

Scientific Ontology does not claim to possess existence itself or to describe it exhaustively and finally.

Its central public objects are:

- boundary;
- contact;
- history;
- return;
- residual and residue;
- downstream condition; and
- re-collatability.

Through these concepts, the system describes how existence appears, becomes recognized, acquires meaning, and affects other existences, institutions, environments, and futures.

Scientific Ontology does not begin by selecting a subjective account, an objective account, cross-domain research, or any other language game as the final language. It attempts to maintain a field in which different language games can be brought to the boundary while preserving their conditions of validity, observational scope, claim strength, and limits. Commensuration is not identification; it keeps difference, non-identity, residuals, and return paths traceable.

The [`Scientific_Ontology_Operational_Outline.en.md`](./Scientific_Ontology_Operational_Outline.en.md), added at the opening of the v5 series, presents an operational direction through boundary events, action, return, responsibility partition, and mobility. It is not a new superior axiom but a whole-system orientation for carrying existing concepts into external implementation.

The public architecture makes the following continuity explicit:

```text
critique of boundary cognition
  ↓
formation of boundary cognition
  ↓
cross-cutting foundation: language / meaning / communication phase
  ↓
operation of boundary cognition
  ↓
implementation in purpose, communication, and organization
  ↓
ethics, social design, and peace specification
  ↓
return of residuals, objections, and implementation results
```

---

## 2. Overall Repository Architecture

The public repository is divided into four broad regions.

| Region | Main location | Responsibility |
|---|---|---|
| Public entrance | Root and `00_Overview` | General orientation, reading routes, concept maps, Roadmap, and Glossary |
| Theory and application body | `01`–`06` | Foundational structure, communicative content, protocols, applications, research notes, and visual materials |
| Repository governance | `90_Repository_Governance`, `tools`, `scripts`, and `.github` | Commensuration, terminology collision, format, document relations, and validation |
| Public boundary | `99_Private_Core_Not_Included` and `.gitignore` | Boundary marking excluded and private materials |

---

## 3. Public Repository Structure

The following tree represents the public structure and excludes `000*` working drafts, local environments, caches, generated validation output, and maintenance notes excluded through `.gitignore`.

```text
.
├─ README.md
├─ GLOSSARY.md
├─ Roadmap.md
├─ RELEASE_NOTES.md
├─ CITATION.md
├─ CITATION.cff
├─ LICENSE.md
├─ .zenodo.json
├─ .gitattributes
├─ .gitignore
├─ requirements-public-check.txt
│
├─ 00_Overview/
│  ├─ README.md
│  ├─ Scientific_Ontology_Operational_Outline.ja.md
│  ├─ Scientific_Ontology_Operational_Outline.en.md
│  ├─ Scientific_Ontology_System_Map.md
│  ├─ Scientific_Ontology_Concept_Network.ja.md
│  ├─ Scientific_Ontology_Concept_Network.en.md
│  ├─ Truth_Management_and_Boundary_PDCA.ja.md
│  ├─ Truth_Management_and_Boundary_PDCA.en.md
│  ├─ Claim_Strength_and_Publication_Layer_Table.ja.md
│  ├─ Claim_Strength_and_Publication_Layer_Table.en.md
│  ├─ Physics_Correspondence_Policy.ja.md
│  └─ Physics_Correspondence_Policy.en.md
│
├─ 01_Sat_Truth/
│  ├─ README.md
│  ├─ AMP_Introduction.md
│  ├─ Four_Axioms_of_Existence.md
│  ├─ Meaning_Generation_Model.md
│  ├─ Boundary_Realism_Principle.md
│  ├─ Boundary_Epistemological_Critique.ja.md
│  ├─ Boundary_Epistemological_Critique.en.md
│  ├─ Boundary_Epistemological_Critique_Annotations.ja.md
│  └─ Boundary_Epistemological_Critique_Annotations.en.md
│
├─ 02_Raj_Beauty/
│  ├─ README.md
│  ├─ HFC_Introduction.md
│  ├─ History_Field_Topology.md
│  ├─ Scientific_Ontology_and_Science.md
│  ├─ Entropy_Attributed_Difference_and_Cognitive_Axis_Formation.ja.md
│  └─ Entropy_Attributed_Difference_and_Cognitive_Axis_Formation.en.md
│
├─ 03_Tam_Goodness/
│  ├─ README.md
│  ├─ Boundary_Ethics_Model.md
│  ├─ Meaning_as_Return_Orbit.md
│  ├─ Optional_Axiom_Modules_as_Cognitive_Bridge.ja.md
│  └─ Optional_Axiom_Modules_as_Cognitive_Bridge.en.md
│
├─ 04_Applications/
│  ├─ README.md
│  ├─ AI_Adaptation/
│  │  ├─ README.md
│  │  ├─ Application_Boundary_Theory_Core.md
│  │  ├─ AI_Usefulness_as_a_Boundary_Function.md
│  │  ├─ AI_Boundary_Interface_and_Synchronous_Understanding.md
│  │  └─ AI_Personality_as_Response_Structure.md
│  └─ Social_Boundary_Design/
│     ├─ README.md
│     ├─ AI_Adoption_Collation_Checklist.md
│     ├─ Specification_for_Peace.ja.md
│     └─ Specification_for_Peace.en.md
│
├─ 05_Research_Notes/
│  ├─ README.md
│  ├─ Research_Notes_Index.md
│  ├─ Cognitive_Dynamics_Communication_Studies/
│  │  ├─ README.md
│  │  ├─ Cognitive_Dynamics_Communication_Model.ja.md
│  │  ├─ Cognitive_Dynamics_Communication_Model.en.md
│  │  ├─ Compression_of_Existence_Phases.ja.md
│  │  ├─ Compression_of_Existence_Phases.en.md
│  │  ├─ Boundary_Diplomacy_and_Port_Allocation.ja.md
│  │  ├─ Boundary_Diplomacy_and_Port_Allocation.en.md
│  │  ├─ Organizational_Boundary_and_Port_Model.ja.md
│  │  └─ Organizational_Boundary_and_Port_Model.en.md
│  ├─ Cross_Domain_Ontological_Notes/
│  │  ├─ README.md
│  │  ├─ Asymmetry_Stabilization_and_ReCollation.ja.md
│  │  ├─ Asymmetry_Stabilization_and_ReCollation.en.md
│  │  ├─ Return_Ethics_and_Retaliation_Conversion.ja.md
│  │  ├─ Return_Ethics_and_Retaliation_Conversion.en.md
│  │  ├─ Narrative_Truth_and_Structural_Reading.ja.md
│  │  ├─ Narrative_Truth_and_Structural_Reading.en.md
│  │  ├─ Consent_Boundary_and_Sentence_Bit_Asymmetry.ja.md
│  │  └─ Consent_Boundary_and_Sentence_Bit_Asymmetry.en.md
│  ├─ Language_Meaning_and_Communication_Phase_Studies/
│  │  ├─ README.md
│  │  ├─ Grammar_as_a_Meaning_Pressure_Channel.ja.md / .en.md
│  │  ├─ Meaning_as_Collation_and_Return_Path.ja.md / .en.md
│  │  ├─ Compressed_Experience_Qualia_and_Literature.ja.md / .en.md
│  │  ├─ AI_Language_Generation_and_Grammatical_Frames.ja.md / .en.md
│  │  ├─ Speech_as_Sequential_Decompression.ja.md / .en.md
│  │  ├─ Intension_Extension_and_False_Extension.ja.md / .en.md
│  │  ├─ Semantic_Network_Topology_and_Commensuration_Bandwidth.ja.md / .en.md
│  │  ├─ Commensuration_as_Cross_Grammatical_Collation.ja.md / .en.md
│  │  ├─ Linguistic_Frame_Differences_between_Japanese_and_English.ja.md / .en.md
│  │  └─ Return_Intake_Log.ja.md / .en.md
│  ├─ Physical_Cosmological_Notes/
│  │  ├─ README.md
│  │  ├─ Intrinsic_Time_Standard_Model_Correspondence.ja.md
│  │  ├─ Intrinsic_Time_Standard_Model_Correspondence.en.md
│  │  ├─ Ontological_History_of_the_Universe.ja.md
│  │  ├─ Ontological_History_of_the_Universe.en.md
│  │  ├─ Cosmological_Topological_Dynamics.ja.md
│  │  ├─ Cosmological_Topological_Dynamics.en.md
│  │  ├─ PINGER_Hypothesis_and_History_Field_Topology.ja.md
│  │  ├─ PINGER_Hypothesis_and_History_Field_Topology.en.md
│  │  ├─ Chaos_Theory_and_Logical_Depth_Axis.ja.md
│  │  └─ Chaos_Theory_and_Logical_Depth_Axis.en.md
│  ├─ Social_Boundary_Notes/
│  │  ├─ README.md
│  │  ├─ AI_Adoption_as_Synchronization_Closure.md
│  │  ├─ DSSI_Observation_Judgment_Sovereignty_and_Responsibility_Return.ja.md
│  │  ├─ DSSI_Observation_Judgment_Sovereignty_and_Responsibility_Return.en.md
│  │  ├─ Negentropy_Economy_Principles.ja.md
│  │  ├─ Negentropy_Economy_Principles.en.md
│  │  ├─ Negentropy_Economy_and_Meaning_Generation.ja.md
│  │  └─ Negentropy_Economy_and_Meaning_Generation.en.md
│  ├─ AI_Personality_Notes/
│  │  ├─ README.md
│  │  ├─ History_Loop_Radius_and_Return_Stability.md
│  │  └─ Logical_Sandbox_and_Negentropy_Model.md
│  └─ Literary_Ontological_Notes/
│     ├─ README.md
│     ├─ reading-blue-light.ja.md
│     ├─ reading-blue-light.en.md
│     ├─ Meifu_Bureau_Reincarnation_and_Belief_Gravity.md
│     ├─ Literature_as_Worldmaking.ja.md
│     └─ Literature_as_Worldmaking.en.md
│
├─ 06_Visual_Materials/
│  ├─ README.md
│  ├─ Scientific_Ontology_Conceptual_Poster.ja.png
│  ├─ Scientific_Ontology_Conceptual_Poster.en.png
│  └─ Scientific_Ontology_Conceptual_Poster_Note.md
│
├─ 90_Repository_Governance/
│  ├─ README.md
│  ├─ Publication_and_Commensuration_Policy.md
│  ├─ Translation_Note.md
│  ├─ Release_Update/
│  │  ├─ UPDATE_PACK.md
│  │  ├─ release_state.yml
│  │  ├─ release_update.py
│  │  └─ requirements.txt
│  └─ Terminology/
│     ├─ README.md
│     ├─ Scientific_Terminology_Protocol.md
│     ├─ TERM_COLLISION_REGISTRY.ja.md
│     └─ TERM_COLLISION_REGISTRY.en.md
│
├─ 99_Private_Core_Not_Included/
│  └─ README.md
│
├─ tools/
│  ├─ Public_Format_Registry.yml
│  ├─ docs_manifest.yml
│  ├─ maintenance_rules.yml
│  └─ CHECKER_USAGE.md
├─ scripts/
│  └─ check_public_format.py
└─ .github/workflows/
   └─ public-format-check.yml
```

---

## 4. Role of Root-Level Files

The repository root is not the primary location of theoretical documents. It is the public interface through which readers enter the repository as a whole.

| Document | Responsibility |
|---|---|
| [`README.md`](../README.md) | Entry point for new readers, the system's central research movement, and purpose-specific reading routes |
| [`GLOSSARY.md`](../GLOSSARY.md) | Human-readable interface for canonical terms, English commensurations, conceptual lineage, and Public definition owners |
| [`Roadmap.md`](../Roadmap.md) | Research dynamics, current position, and future falsification and implementation tasks |
| [`RELEASE_NOTES.md`](../RELEASE_NOTES.md) | Version-specific change record |
| [`CITATION.md`](../CITATION.md) / [`CITATION.cff`](../CITATION.cff) | Human-readable and machine-readable citation information |
| [`LICENSE.md`](../LICENSE.md) | Terms of use |
| [`.zenodo.json`](../.zenodo.json) | Zenodo metadata |

The Glossary is also a governance document, but it remains at the root because it is a highly discoverable cross-repository entrance to the public conceptual vocabulary.

---

## 5. `00_Overview` — Map of the Public System and Research Dynamics

`00_Overview` explains how the current public system should be read before readers enter the main theoretical body.

Its central responsibilities are to:

- provide an entrance to the conceptual system;
- map the repository structure;
- show research dynamics and purpose-return cycles;
- govern claim strength, publication layer, and uncertainty; and
- state the conditions under which physics-adjacent vocabulary is used.

Principal documents include:

- [`Scientific_Ontology_Concept_Network.en.md`](./Scientific_Ontology_Concept_Network.en.md): concept placement, reading routes, definition ownership, return paths, and aporia entry points.
- [`Scientific_Ontology_System_Map.md`](./Scientific_Ontology_System_Map.md): architecture of the repository and conceptual layers.
- [`Truth_Management_and_Boundary_PDCA.en.md`](./Truth_Management_and_Boundary_PDCA.en.md): research and operational cycles through First Purpose, sharing, world formation, and Boundary PDCA.
- [`Claim_Strength_and_Publication_Layer_Table.en.md`](./Claim_Strength_and_Publication_Layer_Table.en.md): claim strength, evidence strength, uncertainty, and publication-layer governance.
- [`Physics_Correspondence_Policy.en.md`](./Physics_Correspondence_Policy.en.md): policy governing the non-identity between physics-adjacent vocabulary and standard physics.

`00_Overview` is not merely metadata. It serves as the higher-order reading surface that shows how foundational concepts expand into cognition, research dynamics, and implementation.

---

## 6. `01`–`03` — Structural Responsibilities of the Three Core Layers

`01_Sat_Truth`, `02_Raj_Beauty`, and `03_Tam_Goodness` are not primarily topical folders. They have distinct responsibilities within a communication architecture.

| Layer | Role in the communication structure | Role foregrounded in the public system | Why these documents tend to be placed here |
|---|---|---|---|
| `01_Sat_Truth` | Network structure and conditions of formation | Critique of boundary cognition | It addresses metaphysics, axioms, and the conditions under which existence, observation, meaning, and knowledge become possible |
| `02_Raj_Beauty` | Communicative content, event-flow, reception, and modes of reading | Formation of boundary cognition | It addresses history, difference, attention, abstraction, synchronization, and the formation of cognitive axes |
| `03_Tam_Goodness` | Communication protocols, governance, closure, reopening, and return | Operation of boundary cognition | It addresses ethics, commensuration, suspension, prevention of false closure, and non-destructive governance |

### 6.1 `01_Sat_Truth` — Network Structure and Conditions of Formation

This layer addresses the structure within which contact, observation, meaning, and knowledge can occur, prior to asking what content flows through that structure.

It does not merely foreground metaphysical roots. Through Boundary Realism and Boundary Epistemological Critique, it moves public description toward boundary conditions that can be observed, challenged, and compared.

### 6.2 `02_Raj_Beauty` — Communicative Content and the Formation of Reading

This layer addresses histories, differences, meaning pressure, synchronization and asynchrony, and the ways in which these are received and stabilized as directions of cognition.

`Entropy_Attributed_Difference_and_Cognitive_Axis_Formation` describes how cognitive axes are formed, stabilized, and transformed after boundary critique has exposed the conditions of cognition.

### 6.3 `03_Tam_Goodness` — Communication Protocols and Governance

This layer addresses not only whether communicative content is correct, but also what may be admitted, suspended, closed, reopened, transformed, and returned.

`Optional_Axiom_Modules_as_Cognitive_Bridge` provides an operational structure for comparing, commensurating, and conditionally connecting distinct cognitive forms without forcing identity or total severance.

---

## 7. `04_Applications` — Public Application Interfaces

`04_Applications` connects the concepts of the three core layers to publicly usable design principles, evaluation frames, checklists, and specifications.

### `AI_Adaptation`

This area treats AI not as a substitute decision-maker, but as a boundary interface that preserves the possibility of human judgment.

Its principal concerns include:

- AI usefulness;
- AI boundary interfaces;
- AI personality as response structure; and
- application-boundary theory.

### `Social_Boundary_Design`

This area addresses the boundaries, responsibilities, collation procedures, and peace conditions of the social systems that adopt AI and other institutional technologies.

Its principal concerns include:

- AI adoption collation checklists;
- responsibility boundaries and re-collatability; and
- peace protocols and peace specifications.

This layer does not include implementation code, product specifications, legal advice, or private operational procedures for particular organizations.

---

## 8. `05_Research_Notes` — Retaining Stronger Propositions under Explicit Boundary Conditions

`05_Research_Notes` retains research lines whose claim strength or misreading risk is too high for direct placement in the public foundational layers, but which should not be discarded.

### `Language_Meaning_and_Communication_Phase_Studies`

A cross-cutting research line treating language, meaning, grammar, speech, commensuration, semantic networks, and AI language generation as communication phases with return paths. In the v5 series it is the first line to operate explicitly as a living-canonical research surface with change history and Return Intake.

It does not replace the Meaning Generation Model. It owns only local linguistic-meaning questions and returns residuals to meaning, HFC, epistemology, and AI application documents.

### `Cognitive_Dynamics_Communication_Studies`

This area examines how cognition can be communicatively seamless while practical operation requires discretization into phases, ports, capacities, and responsibilities.

It connects cognitive dynamics to organizational boundaries, responsibility boundaries, boundary diplomacy, and peace specifications.

### `Cross_Domain_Ontological_Notes`

This area contains cross-domain ontological readings of asymmetry, return ethics, retaliation conversion, narrative truth, and the consent boundary under sentence/bit asymmetry.

### `Physical_Cosmological_Notes`

This area contains higher-claim-strength, physics- and cosmology-adjacent hypotheses involving intrinsic time, cosmic history, the PINGER hypothesis, chaos theory, and the Logical-Depth Axis.

### `Social_Boundary_Notes`

This area contains research notes on AI adoption, negentropy economy, meaning generation, social boundaries, and DSSI research on observation, judgment sovereignty, and responsibility return. The DSSI application itself is not included in v5.0.

### `AI_Personality_Notes`

This area treats AI personality, history loops, return stability, and logical sandboxes as research-note subjects.

### `Literary_Ontological_Notes`

This area does not use literature as empirical proof. It uses ontological reading to examine boundaries, history, meaning, belief gravity, and literature as worldmaking.

For document-level details, see [`Research_Notes_Index.md`](../05_Research_Notes/Research_Notes_Index.md).

---

## 9. `06_Visual_Materials` — Visual Public Entrance

This area contains conceptual posters and reading notes.

Visual materials are not substitutes for theoretical documents, empirical evidence, or formal proof. They are supplementary interfaces that provide multiple points of entry into the conceptual system.

---

## 10. `90_Repository_Governance` — Repository Governance

This area contains governance documents rather than research-body documents. It governs publication, commensuration, terminology, concept ownership, and collision management.

| Document | Responsibility |
|---|---|
| [`Publication_and_Commensuration_Policy.md`](../90_Repository_Governance/Publication_and_Commensuration_Policy.md) | Authoritative-language relations, preservation contract, language formats, concept ownership, and lineage |
| [`Translation_Note.md`](../90_Repository_Governance/Translation_Note.md) | Recurring cross-document English commensuration decisions |
| [`Scientific_Terminology_Protocol.md`](../90_Repository_Governance/Terminology/Scientific_Terminology_Protocol.md) | Operational protocol for scientific vocabulary, SO definitions, standard definitions, and limiting conditions |
| [`TERM_COLLISION_REGISTRY.ja.md`](../90_Repository_Governance/Terminology/TERM_COLLISION_REGISTRY.ja.md) | Collision surfaces involving Japanese authoritative terms |
| [`TERM_COLLISION_REGISTRY.en.md`](../90_Repository_Governance/Terminology/TERM_COLLISION_REGISTRY.en.md) | Collision surfaces involving English commensurated terms |

Their responsibilities are separated as follows.

```text
GLOSSARY.md
  current canonical vocabulary and human-readable conceptual lineage

Publication and Commensuration Policy
  principles governing authoritative texts, commensuration, ownership, and public boundaries

Term Collision Registries
  collision surfaces and likely misreadings in established vocabulary

Translation Note
  recurring commensuration decisions

tools/*.yml
  machine-readable format, relationship, and maintenance rules
```

---

### Release Update

`90_Repository_Governance/Release_Update` centralizes release facts in `release_state.yml`. `release_update.py` synchronizes `RELEASE_NOTES.md`, `CITATION.cff`, `CITATION.md`, and `.zenodo.json`. It does not generate the substantive meaning of the README, Roadmap, Concept Network, System Map, or Glossary; those remain human-owned structural documents.

## 11. `tools`, `scripts`, and `.github` — Machine-Readable Governance and Validation

| File | Responsibility |
|---|---|
| [`tools/Public_Format_Registry.yml`](../tools/Public_Format_Registry.yml) | Document types, metadata, language formats, and public-validation structure |
| [`tools/docs_manifest.yml`](../tools/docs_manifest.yml) | Document inventory, concept ownership, imports, exports, tests, returns, and delegations |
| [`tools/maintenance_rules.yml`](../tools/maintenance_rules.yml) | Terminology replacement, conflict prevention, publication boundaries, and warning conditions |
| [`scripts/check_public_format.py`](../scripts/check_public_format.py) | Pre-publication validation of Markdown, links, metadata, and document relations |
| [`.github/workflows/public-format-check.yml`](../.github/workflows/public-format-check.yml) | Automated validation on pushes and pull requests |

Machine-readable files do not replace theoretical documents. If prose and machine-readable records diverge, the divergence itself becomes an object of collation.

---

## 12. `99_Private_Core_Not_Included` — Marker of the Private Boundary

This directory is not a place for explaining the private core.

It marks that the public repository does not include the full AMP Core, the full ITS Theory, private runtimes, personality cores, internal evaluation, or detailed implementation and operational parameters.

It must not accumulate titles, paths, correspondence tables, or indexes of private materials.

---

## 13. Research Dynamics and Return Paths

This system is not a hierarchy applied in only one direction from top to bottom.

```text
01 structure and conditions of formation
  ↓
02 difference, history, and cognitive direction
  ↓
03 protocols, ethics, commensuration, and governance
  ↓
04 public applications
  ↓
05 stronger and cross-domain research
  ↓
implementation results, criticism, and residuals
  ↓
00 concept network and Truth Management
  ↓
return to canonical owner documents in 01–03
```

Research dynamics is the movement through which inquiry descends into the grounds of cognition and thereby expands what can be described, compared, implemented, and re-collated at the public surface.

Ethics is not an external application added after the theory. The need to make contact without destruction, stop without total severance, and communicate across difference without forced identity drives higher-resolution descriptions of cognition, ports, responsibility, and organization.

---

## 14. Public Exclusion Rules

Under `.gitignore`, the public structure excludes:

- draft and work files whose basename begins with `000`;
- `.venv/`, `venv/`, and other local virtual environments;
- `__pycache__/`, `*.pyc`, and other caches;
- `public_format_report.md` and `public_format_report.json`;
- local IDE, OS, temporary, and backup files;
- checker-extension and YAML-refactoring work notes; and
- private cores, internal logs, and detailed implementation or operational materials.

A `000*` file may temporarily appear in a working ZIP, but it is not part of the publicly tracked repository or release archive.

---

## 15. Reading Entrances

Purpose-specific entrances are as follows.

- For a rapid overview: [`README.md`](../README.md) → [`Scientific_Ontology_Concept_Network.en.md`](./Scientific_Ontology_Concept_Network.en.md)
- For foundational concepts: [`Four_Axioms_of_Existence.md`](../01_Sat_Truth/Four_Axioms_of_Existence.md) → [`Boundary_Realism_Principle.md`](../01_Sat_Truth/Boundary_Realism_Principle.md)
- For boundary cognition: Boundary Epistemological Critique → Cognitive Axis Formation → Optional Axiom Modules → Truth Management
- For ethics, organization, and peace: Cognitive Dynamics → Port Allocation → Organizational Boundary → Specification for Peace
- For physics-adjacent research: Physics Correspondence Policy → Physical Cosmological Notes
- For publication and commensuration rules: Glossary → Publication and Commensuration Policy → Term Collision Registries

---

## 16. Maintenance Principles

This System Map is not a file-by-file inventory that must be conceptually rewritten whenever an individual document is added.

It should be revised when:

- the structural responsibility of a directory changes;
- public entrances or reading routes change;
- a research line becomes an independent directory;
- the location of governance documents or machine-readable metadata changes; or
- public-boundary or `.gitignore` inclusion rules change.

Ordinary additions and removals of individual files should be maintained in directory READMEs, `docs_manifest.yml`, and release notes.

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

公開リポジトリは、現在、次の五領域として読むのが最も安定している。

| 領域 | 主な場所 | 役割 |
|---|---|---|
| 公開入口 | ルート、`00_Overview` | 全体説明、概念地図、運用方針、Roadmap、Glossary、読解経路 |
| 中核・応用・研究本文 | `01`–`06` | 基礎三層、応用、研究ノート、視覚資料 |
| 外部接触・表現実験 | `07_Creative_Offshoots` | 文学・創作・比較的世界制作など、定義所有の外側で起きる接触と残差の観測 |
| リポジトリ統治 | `90_Repository_Governance`、`tools`、`scripts`、`.github`、`navigator` | 通約、用語衝突、文書契約、登録、検査、公開投影 |
| 公開境界 | `99_Private_Core_Not_Included`、`.gitignore` | 非公開資料、作業草稿、公開除外対象との境界表示 |

ここで`navigator`は公開文書を読むための投影面であり、概念定義や登録判断の所有者ではない。現在の文書同一性、正本・通約関係、概念所有、imports / exports / returnsなどの機械可読な関係は[`tools/docs_manifest.yml`](../tools/docs_manifest.yml)を基準とする。

---

## 3. 公開リポジトリ構造

System Mapは、個別ファイルを一つずつ固定する目録ではなく、**どの領域が何を担当し、どこへ返すか**を示す。正確な文書一覧はmanifestと各READMEへ委ね、ここでは変化しにくい構造だけを示す。

```text
.
├─ README.md / GLOSSARY.md / Roadmap.md / RELEASE_NOTES.md
├─ CITATION.md / CITATION.cff / LICENSE.md / .zenodo.json
│
├─ 00_Overview/
│  ├─ Operational Outline
│  ├─ Concept Network
│  ├─ System Map
│  ├─ Truth Management and Boundary PDCA
│  ├─ Claim Strength and Publication-Layer Table
│  └─ Physics Correspondence Policy
│
├─ 01_Sat_Truth/                 # 成立条件、存在・意味・実在性
├─ 02_Raj_Beauty/               # 履歴、差異、認識生成、通信
├─ 03_Tam_Goodness/             # 返り、責任、倫理、条件付き接続
│
├─ 04_Applications/
│  ├─ AI_Adaptation/
│  ├─ Social_Boundary_Design/
│  └─ SO_Reflexive_Philosophical_Research/
│     ├─ research context / open questions (ja + en)
│     ├─ sources/README.md
│     │    # 公開するのはsource identity / hash / provenance / role。
│     │    # exact historical bytesは公開リポジトリに含めない。
│     └─ volumes/Volume_01_DeRegistry_to_Judgment_Transparency/
│          # timeline / chronicle / transmissions / topology
│          # evidence map / residuals / digest
│          # historical attestation / current attested checksum / evidence
│
├─ 05_Research_Notes/
│  ├─ Language_Meaning_and_Communication_Phase_Studies/
│  ├─ Cognitive_Dynamics_Communication_Studies/
│  ├─ Correctness_Logic_and_Structural_Studies/
│  ├─ Cross_Domain_Ontological_Notes/
│  ├─ Physical_Cosmological_Notes/
│  ├─ Social_Boundary_Notes/
│  ├─ AI_Personality_Notes/
│  └─ Literary_Ontological_Notes/
│
├─ 06_Visual_Materials/
│
├─ 07_Creative_Offshoots/
│  └─ Literary_Essays/
│
├─ 90_Repository_Governance/
│  ├─ Publication and Commensuration Policy
│  ├─ Translation Note
│  ├─ Terminology/
│  ├─ Assessment/                 # candidate protocol; public authorityではない
│  └─ Release_Update/
│
├─ 99_Private_Core_Not_Included/
│
├─ navigator/                     # public/developer projection surface
├─ tools/                         # manifest / registry / maintenance / generated read models
├─ scripts/                       # validators / builders / release helpers
└─ .github/workflows/             # automated checks and deployment
```

この図に個別文書が現れないことは、公開対象外であることを意味しない。文書の現在状態はmanifest、各層のREADME、Navigatorのread modelで照合する。逆に、System Mapへ名前があることだけで、定義所有や公開登録が成立するわけでもない。

---

## 4. ルート直下の役割

ルートは理論本文の置き場ではなく、リポジトリ全体へ入るための公開インターフェースである。

| 文書 | 役割 |
|---|---|
| [`README.md`](../README.md) | 初見読者向けの入口、体系の要約、目的別読解経路 |
| [`GLOSSARY.md`](../GLOSSARY.md) | 標準語、英語通約、概念系譜、公開定義所有者の人間可読インターフェース |
| [`Roadmap.md`](../Roadmap.md) | 研究動態、現在地、次の反証・実装課題 |
| [`RELEASE_NOTES.md`](../RELEASE_NOTES.md) | 版ごとの変更記録 |
| [`CITATION.md`](../CITATION.md) / [`CITATION.cff`](../CITATION.cff) | 人間向け・機械向け引用情報 |
| [`LICENSE.md`](../LICENSE.md) | 利用条件 |
| [`.zenodo.json`](../.zenodo.json) | Zenodo向けメタデータ |

Glossaryは統治文書の一種でもあるが、公開概念の横断入口として発見可能性が高いためルートに置く。README、Release Notes、Citation類はリリース面でもあるため、体系内部の構造変更が固まってから最終同期する。

---

## 5. `00_Overview` — 公開体系の地図と研究動態

`00_Overview`は、個別概念を上書きする上位理論ではない。既存文書の責務、接続、読解順序、主張強度、外部実装への運用方向を横断的に示す。

主な役割は次の通りである。

- Operational Outline：境界事件、作用、返り、責任分界、可動性という運用方向。
- Concept Network：概念所有者を横断した関係、読解経路、返路。
- System Map：リポジトリと公開体系の構造。
- Truth Management：目的、共有、世界形成、Boundary CA。
- Claim Strength Table：主張強度、公開層、検証責任。
- Physics Correspondence Policy：物理近接語彙との接触条件と誤読防止。

SO自身の判断履歴を監査する`04_Applications/SO_Reflexive_Philosophical_Research`、形式化候補を扱う`05_Research_Notes/Correctness_Logic_and_Structural_Studies`、外部表現との接触を扱う`07_Creative_Offshoots`が構造的に活動し始めた場合、Overviewはそれらを定義し直すのではなく、接続と返路を更新する。

---

## 6. `01`–`03` — 中核三層の構造的役割

三層は固定的な学問区分ではなく、同じ問題を異なる位相から読むための主要軸である。

### 6.1 `01_Sat_Truth` — 成立条件と実在性

存在、観測、意味、境界実在論、認識批判など、何を出発点として扱えるかを担当する。

### 6.2 `02_Raj_Beauty` — 履歴・差異・認識生成

履歴場、通信、差異、認識軸形成、科学との接触など、関係がどう動き、形を得るかを担当する。

### 6.3 `03_Tam_Goodness` — 返り・責任・条件付き接続

境界倫理、意味の返還軌道、異なる認識形式の条件付き接続など、接触後に何を返し、どう壊さずに接続を維持するかを担当する。

`Optional_Axiom_Modules_as_Cognitive_Bridge`は公開された橋渡し構造を扱う。歴史的sourceの同一性・hash・研究上の役割は公開できるが、撤退判断されたexact source bytesを公開定義の根拠として再配置しない。

---

## 7. `04_Applications` — 公開応用インターフェース

`04_Applications`は、中核三層の概念を公開可能な設計思想、評価枠、チェックリスト、仕様、自己監査へ接続する。

### `AI_Adaptation`

AIを判断代行主体として固定するのではなく、判断可能性、履歴、境界、返路をどう保つかという応用面を扱う。

### `Social_Boundary_Design`

AIや制度を採用する社会側の責任境界、再照合可能性、平和条件を扱う。

### `SO_Reflexive_Philosophical_Research`

SOが外部だけでなく、**自らの研究判断・分類・公開判断へ同じ境界監査を返す**ための再帰的応用面である。

Volume Iは、De-Registryから判断透明性、Topology-first監査、三層変換監査へ至る方法史を、成功だけに整形せず保持する。historical checksumは当時の記録として保持し、2026年現在の受理判断とは別にattestationを置く。旧sourceはidentity、historical filename、SHA-256、provenance、実験上の役割を公開できるが、exact bytesはprivateに保持し、公開Repositoryには含めない。

ここでいう**判断透明性**は、判断の正しさを保証する概念ではない。接触、位相、経路、返路、open endを再構成可能にし、異議、再評価、修正が実際の変更点へ届く状態を指す。

---

## 8. `05_Research_Notes` — 強い命題と発展中の研究線

`05_Research_Notes`は、公開基礎層へ直接入れるには主張強度、専門依存、誤読リスク、成熟度のいずれかが十分に安定していないが、返路を保ったまま研究すべき線を置く。

### 8.1 `Language_Meaning_and_Communication_Phase_Studies`

言語、意味、文法、発話、通約、意味ネットワーク、AI言語生成を、返路を含む通信位相として扱う横断研究線。意味生成モデルを置換せず、言語的意味に局所責任を持つ。

### 8.2 `Cognitive_Dynamics_Communication_Studies`

連続的な認識と、実運用で必要になる存在相、ポート、容量、責任への離散化を扱い、組織境界、境界外交、平和仕様へ接続する。

### 8.3 `Correctness_Logic_and_Structural_Studies`

正しさ、論理、構造表現、閉包、冗長性、frontier、認識軸、有限資源計算などを、既存SO概念を**再定義せず**形式・計算表現へ通約できるか検討する研究線である。

現時点ではREADMEが研究入口であり、`Spine`を含む形式化候補はcanonical definitionではない。形式化が有用でも、その写像で失われた条件や残差は元の概念所有者へ返す。

### 8.4 その他の研究線

- `Cross_Domain_Ontological_Notes`：非対称性、返りの倫理、物語、同意境界などの横断読解。
- `Physical_Cosmological_Notes`：物理・宇宙論近接の高強度仮説と対応候補。
- `Social_Boundary_Notes`：AI導入、社会境界、価値循環、DSSIに関する研究。
- `AI_Personality_Notes`：AI人格、履歴ループ、帰還安定性、論理サンドボックス。
- `Literary_Ontological_Notes`：文学を証拠化せず、世界制作、履歴、信念、境界の研究面として読む。

DSSIの実装コードはSOリポジトリへ同梱しない。外部公開されたConnectBits / DSSI実装から得られる結果は、SO側では応用の証明としてではなく、観測・責任・返路に関する研究入力として受け取る。

文書単位の詳細は[`Research_Notes_Index.md`](../05_Research_Notes/Research_Notes_Index.md)を参照する。

---

## 9. `06_Visual_Materials` — 視覚的公開入口

この層は概念ポスターと読解注記を置く。

視覚資料は理論本文、実証資料、形式的証明の代替ではない。概念体系へ複数方向から入るための補助インターフェースである。

---

## 10. `07_Creative_Offshoots` — 外部接触と表現実験

`07_Creative_Offshoots`は、中核概念の新しい定義所有者ではない。文学、創作、比較的世界制作その他の表現面で、SOの公開概念が外部の語彙・形式・感性と接触したとき、何が見え、何が失われ、どの残差が返るかを観測する層である。

現在は`Literary_Essays`が公開接触面として置かれている。この層の正式なREADME、公開境界、返送規約は次の構造整理で確定する。したがって本System Mapは07の存在と役割だけを先に可視化し、未確定の定義権限を先取りしない。

---

## 11. `90_Repository_Governance` — リポジトリ統治

この領域は研究本文ではなく、公開、通約、用語、概念所有、評価、リリース整合を統治する。

| 文書・領域 | 役割 |
|---|---|
| [`Publication_and_Commensuration_Policy.md`](../90_Repository_Governance/Publication_and_Commensuration_Policy.md) | 正本関係、通約保存契約、言語形式、概念所有、系譜 |
| [`Translation_Note.md`](../90_Repository_Governance/Translation_Note.md) | 文書横断で反復する英語通約判断 |
| [`Scientific_Terminology_Protocol.md`](../90_Repository_Governance/Terminology/Scientific_Terminology_Protocol.md) | 科学語彙とSO内部語彙の接触規約 |
| `Terminology/TERM_COLLISION_REGISTRY.*` | 成立済み語彙の衝突面と誤読候補 |
| [`Repository_Assessment_Commensuration_and_Navigator_Design.ja.md`](../90_Repository_Governance/Repository_Assessment_Commensuration_and_Navigator_Design.ja.md) | assessment、通約、Navigatorを一つの設計面として読む統治上の設計記録 |
| [`Assessment/Repository_Assessment_Protocol.ja.md`](../90_Repository_Governance/Assessment/Repository_Assessment_Protocol.ja.md) | repository assessmentの候補protocol。候補であり、公開概念の定義権限を自動取得しない |
| `Release_Update/` | release factsの集中管理とrelease-facing metadataの同期 |

`GLOSSARY.md`は現在の標準語と公開定義所有を人間可読に示し、`docs_manifest.yml`は文書契約を機械可読に示す。両者の差は一方を自動的に正解とみなして隠すのではなく、照合対象とする。

---

## 12. `tools`・`scripts`・`.github`・`navigator` — 機械可読統治と公開投影

| 領域 | 役割 |
|---|---|
| [`tools/Public_Format_Registry.yml`](../tools/Public_Format_Registry.yml) | 文書型、metadata、language format、公開検査構造 |
| [`tools/docs_manifest.yml`](../tools/docs_manifest.yml) | 文書inventory、正本・通約関係、概念所有、imports / exports / returns / delegations |
| [`tools/maintenance_rules.yml`](../tools/maintenance_rules.yml) | 用語置換、衝突防止、公開境界、warning条件 |
| `tools/docs_index.json` / `docs_graph.json` / public projections | manifest等から生成されるread model |
| [`scripts/check_public_format.py`](../scripts/check_public_format.py) | Markdown、リンク、metadata、文書関係の公開前検査 |
| `scripts/validate_docs_manifest.py` / contract / Navigator checks | manifest契約、文書契約、UI投影の回帰検査 |
| `.github/workflows/` | push / pull request / deployment時の自動検査 |
| `navigator/` | Public / Developer readerの投影面。定義所有・登録承認を行うauthorityではない |

生成read modelとNavigatorは、公開体系を読みやすくするための投影である。表示上の便利さから理論権限を逆流させない。

---

## 13. `99_Private_Core_Not_Included` — 非公開境界の標識

このディレクトリは、非公開中核を説明する場所ではない。

公開リポジトリに含めないsource body、private runtime、人格中核、内部評価、詳細な実装・運用パラメータ等が存在しうることと、公開体系がそれらへ依存して読者に不可視の権威を要求してはならないことを示す。

ここへ非公開資料の詳細なタイトル、path、対応表、索引を蓄積しない。

---

## 14. 研究動態と返路

この体系は、上から下へ一方向に適用される階層ではない。

```text
01–03  中核三層
  ↓
04     公開応用・自己監査
  ↓
05     発展研究・形式化候補
  ↓
06     視覚的公開入口
  ↓
07     外部表現・創作との接触
  ↓
実装結果・批判・誤読・残差・異議
  ↓
00     Concept Network / Truth Management / System Map
  ↓
各canonical owner、応用、研究線へ返送
```

返路は「下位の結果を上位理論へ取り込んで同化する」ためだけにあるのではない。既存定義を変更しない、局所仮説として保持する、公開層へ移さない、といった判断も返りの一種である。

SO Reflexive Philosophical Researchは、この返路をSO自身の判断へ適用する。Correctness / Logic / Structural Studiesは、形式化が原概念を取りこぼす地点を返す。Creative Offshootsは、表現へ出たときに発生する可視性、誤読、創造的変形、残差を返す。

---

## 15. 公開除外規則

`.gitignore`その他の公開境界規則により、少なくとも次を公開release対象から除外する。

- basenameが`000`で始まる草稿・作業ファイル。
- `.venv/`、`venv/`その他のlocal environment。
- `__pycache__/`、`*.pyc`その他のcache。
- checker output、local IDE / OS / temporary / backup files。
- private source body、internal log、非公開中核、詳細な運用資料。
- private-bearingなpre-withdrawal snapshotやGit backup。

作業ZIPに存在すること、ローカルに保存されること、公開releaseへ含まれることは別の状態である。公開可否はmanifest、ignore規則、release packaging、human reviewを合わせて判定する。

---

## 16. 読解入口

目的別の入口は次の通りである。

- 全体像：[`README.md`](../README.md) → [`Scientific_Ontology_Concept_Network.ja.md`](./Scientific_Ontology_Concept_Network.ja.md)
- 基礎概念：`Four_Axioms_of_Existence` → `Boundary_Realism_Principle`
- 認識と意味：Boundary Epistemological Critique → Cognitive Axis Formation → Optional Axiom Modules → Truth Management
- 倫理・組織・平和：Cognitive Dynamics → Port Allocation → Organizational Boundary → Specification for Peace
- 判断・自己監査：[`SO_Reflexive_Philosophical_Research`](../04_Applications/SO_Reflexive_Philosophical_Research/README.md) → Judgment Transparency Topology → Historical Attestation
- 正しさ・形式化：[`Correctness_Logic_and_Structural_Studies`](../05_Research_Notes/Correctness_Logic_and_Structural_Studies/README.md)
- 表現・創作接触：[`Questions, Boundaries, and Peace`](../07_Creative_Offshoots/Literary_Essays/Questions_Boundaries_and_Peace.ja.md)
- 物理近接研究：Physics Correspondence Policy → Physical Cosmological Notes
- 公開・通約規則：Glossary → Publication and Commensuration Policy → Term Collision Registries

---

## 17. 保守原則

System Mapは、個別文書を追加するたびに完全な一覧を書き換えるための文書ではない。

更新が必要なのは、主として次の場合である。

- ディレクトリの構造的責務が変わる。
- 公開入口または読解経路が変わる。
- 新しい研究線・応用面・外部接触面が独立した責務を持つ。
- governance、machine-readable metadata、Navigatorの責務が変わる。
- public/private boundaryまたはrelease packagingの規則が変わる。

個別ファイルの追加・削除は各README、`docs_manifest.yml`、generated read model、Release Notesで管理する。

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

The public repository is currently most stable when read as five regions.

| Region | Main location | Responsibility |
|---|---|---|
| Public entrance | root, `00_Overview` | whole-system explanation, concept maps, operational orientation, Roadmap, Glossary, reading routes |
| Core, application, and research body | `01`–`06` | three core layers, applications, research notes, visual materials |
| Outward contact and expressive experiments | `07_Creative_Offshoots` | observing contact and residuals in literature, creative work, comparative worldmaking, and related forms outside definition ownership |
| Repository governance | `90_Repository_Governance`, `tools`, `scripts`, `.github`, `navigator` | commensuration, terminology collision, document contracts, registration, validation, public projection |
| Public boundary | `99_Private_Core_Not_Included`, `.gitignore` | marking the boundary against non-public material, working drafts, and excluded artifacts |

`navigator` is a projection surface for reading public documents; it does not own conceptual definitions or registration decisions. Current machine-readable document identity, authoritative/commensurated relations, concept ownership, and imports / exports / returns are governed through [`tools/docs_manifest.yml`](../tools/docs_manifest.yml).

---

## 3. Public Repository Structure

The System Map is not a frozen file-by-file inventory. It shows **which region performs which responsibility and where its results return**. Exact document inventory is delegated to the manifest and directory READMEs; this map keeps only the more stable topology.

```text
.
├─ README.md / GLOSSARY.md / Roadmap.md / RELEASE_NOTES.md
├─ CITATION.md / CITATION.cff / LICENSE.md / .zenodo.json
│
├─ 00_Overview/
│  ├─ Operational Outline
│  ├─ Concept Network
│  ├─ System Map
│  ├─ Truth Management and Boundary PDCA
│  ├─ Claim Strength and Publication-Layer Table
│  └─ Physics Correspondence Policy
│
├─ 01_Sat_Truth/                 # conditions of formation, existence, meaning, reality
├─ 02_Raj_Beauty/               # history, difference, cognitive formation, communication
├─ 03_Tam_Goodness/             # return, responsibility, ethics, conditional connection
│
├─ 04_Applications/
│  ├─ AI_Adaptation/
│  ├─ Social_Boundary_Design/
│  └─ SO_Reflexive_Philosophical_Research/
│     ├─ research context / open questions (ja + en)
│     ├─ sources/README.md
│     │    # public: source identity / hash / provenance / role
│     │    # exact historical bytes are not included in the public repository
│     └─ volumes/Volume_01_DeRegistry_to_Judgment_Transparency/
│          # timeline / chronicle / transmissions / topology
│          # evidence map / residuals / digest
│          # historical attestation / current attested checksum / evidence
│
├─ 05_Research_Notes/
│  ├─ Language_Meaning_and_Communication_Phase_Studies/
│  ├─ Cognitive_Dynamics_Communication_Studies/
│  ├─ Correctness_Logic_and_Structural_Studies/
│  ├─ Cross_Domain_Ontological_Notes/
│  ├─ Physical_Cosmological_Notes/
│  ├─ Social_Boundary_Notes/
│  ├─ AI_Personality_Notes/
│  └─ Literary_Ontological_Notes/
│
├─ 06_Visual_Materials/
│
├─ 07_Creative_Offshoots/
│  └─ Literary_Essays/
│
├─ 90_Repository_Governance/
│  ├─ Publication and Commensuration Policy
│  ├─ Translation Note
│  ├─ Terminology/
│  ├─ Assessment/                 # candidate protocol; not automatic public authority
│  └─ Release_Update/
│
├─ 99_Private_Core_Not_Included/
│
├─ navigator/                     # public/developer projection surface
├─ tools/                         # manifest / registry / maintenance / generated read models
├─ scripts/                       # validators / builders / release helpers
└─ .github/workflows/             # automated checks and deployment
```

The absence of an individual document from this diagram does not mean that it is excluded from publication. Current document state is collated through the manifest, layer READMEs, and Navigator read models. Conversely, being named in this System Map does not by itself grant definition ownership or registration status.

---

## 4. Role of Root-Level Files

The root is a public interface into the repository rather than a location for substantive theory documents.

| Document | Responsibility |
|---|---|
| [`README.md`](../README.md) | first public entrance, whole-system summary, purpose-specific reading routes |
| [`GLOSSARY.md`](../GLOSSARY.md) | human-readable interface for standard terms, English commensuration, conceptual lineage, and public definition ownership |
| [`Roadmap.md`](../Roadmap.md) | research dynamics, current position, next falsification and implementation tasks |
| [`RELEASE_NOTES.md`](../RELEASE_NOTES.md) | release-by-release change record |
| [`CITATION.md`](../CITATION.md) / [`CITATION.cff`](../CITATION.cff) | human-readable and machine-readable citation information |
| [`LICENSE.md`](../LICENSE.md) | terms of use |
| [`.zenodo.json`](../.zenodo.json) | Zenodo metadata |

The Glossary is also a governance document, but remains at the root because it is a high-discoverability cross-system entrance. The README, Release Notes, and citation files are release-facing surfaces and should receive their final synchronization after internal structural alignment has stabilized.

---

## 5. `00_Overview` — Map of the Public System and Research Dynamics

`00_Overview` is not a superior theory that overwrites local concept owners. It shows responsibilities, connections, reading order, claim strength, and operational orientation across existing documents.

Its primary responsibilities are:

- Operational Outline: boundary events, action, return, responsibility partition, and mobility.
- Concept Network: cross-owner relations, reading routes, and return paths.
- System Map: repository and publication architecture.
- Truth Management: purpose, sharing, world formation, and Boundary CA.
- Claim Strength Table: claim strength, publication layer, and validation responsibility.
- Physics Correspondence Policy: conditions and safeguards for contact with physics-adjacent vocabulary.

When `04_Applications/SO_Reflexive_Philosophical_Research`, `05_Research_Notes/Correctness_Logic_and_Structural_Studies`, or `07_Creative_Offshoots` becomes structurally active, Overview documents should update the connections and return paths rather than redefining the local material.

---

## 6. `01`–`03` — Structural Responsibilities of the Three Core Layers

The three layers are not fixed academic compartments. They are major axes for reading the same problem through different phases.

### 6.1 `01_Sat_Truth` — Conditions of Formation and Reality

This layer addresses existence, observation, meaning, Boundary Realism, and epistemological critique: what may be treated as a starting condition and under what limits.

### 6.2 `02_Raj_Beauty` — History, Difference, and Cognitive Formation

This layer addresses history-fields, communication, difference, cognitive-axis formation, and contact with science: how relations move and acquire form.

### 6.3 `03_Tam_Goodness` — Return, Responsibility, and Conditional Connection

This layer addresses boundary ethics, meaning as return orbit, and conditional connection among different cognitive forms: what must be returned after contact and how connection can continue without destructive identification.

`Optional_Axiom_Modules_as_Cognitive_Bridge` is the public bridge document. Historical source identity, hash, and research role may remain public, but exact source bytes withdrawn from the public repository are not reintroduced as an invisible definition authority.

---

## 7. `04_Applications` — Public Application Interfaces

`04_Applications` connects the three core layers to publicly usable design ideas, evaluation frames, checklists, specifications, and reflexive audit.

### `AI_Adaptation`

This area treats AI not as a fixed substitute for human judgment but as an application surface for preserving conditions of judgment, history, boundaries, and return paths.

### `Social_Boundary_Design`

This area addresses responsibility boundaries, re-collatability, and peace conditions on the social side of AI and institutional adoption.

### `SO_Reflexive_Philosophical_Research`

This is the recursive application surface through which SO returns the same boundary audit to **its own research judgments, classifications, and publication decisions**.

Volume I preserves the methodological history from De-Registry to judgment transparency, topology-first auditing, and three-layer transformation auditing without rewriting it as a linear success story. Historical checksums remain records of their period, while a separate attestation records present acceptance. For the old source, identity, historical filename, SHA-256, provenance, and experimental role may remain public; exact bytes are retained privately and are not included in the public repository.

**Judgment Transparency** does not guarantee correctness. It means keeping contacts, phases, paths, return paths, and open ends reconstructable so that objection, reassessment, and correction can reach the actual points of change.

---

## 8. `05_Research_Notes` — Stronger Propositions and Developing Research Lines

`05_Research_Notes` retains lines whose claim strength, specialist dependence, misreading risk, or maturity is not yet stable enough for direct placement in the public foundational layers, while preserving return paths for continued work.

### 8.1 `Language_Meaning_and_Communication_Phase_Studies`

A cross-cutting line treating language, meaning, grammar, speech, commensuration, semantic networks, and AI language generation as communication phases with return paths. It does not replace the Meaning Generation Model and owns only local linguistic questions.

### 8.2 `Cognitive_Dynamics_Communication_Studies`

This line studies the relation between communicatively continuous cognition and the practical discretization into phases, ports, capacities, and responsibilities, connecting cognition to organizational boundaries, boundary diplomacy, and peace specification.

### 8.3 `Correctness_Logic_and_Structural_Studies`

This line asks how correctness, logic, structural representation, closure, redundancy, frontiers, cognitive axes, and finite-resource computation can be commensurated into formal or computational representations **without redefining existing SO concepts**.

At present its README is the research entrance. Formalization candidates including `Spine` are not canonical definitions. Even when a formalization proves useful, conditions or residuals lost in the mapping must be returned to the original concept owners.

### 8.4 Other Research Lines

- `Cross_Domain_Ontological_Notes`: asymmetry, return ethics, narrative, consent boundaries, and other cross-domain readings.
- `Physical_Cosmological_Notes`: higher-claim-strength physics- and cosmology-adjacent hypotheses and correspondence candidates.
- `Social_Boundary_Notes`: AI adoption, social boundaries, value circulation, and DSSI-related research.
- `AI_Personality_Notes`: AI personality, history loops, return stability, and logical sandboxes.
- `Literary_Ontological_Notes`: literature read as worldmaking, history, belief, and boundary rather than empirical proof.

DSSI implementation code is not bundled in the SO repository. Results returned from the externally released ConnectBits / DSSI implementation are treated on the SO side as research input about observation, responsibility, and return paths, not as proof of the theory.

See [`Research_Notes_Index.md`](../05_Research_Notes/Research_Notes_Index.md) for document-level detail.

---

## 9. `06_Visual_Materials` — Visual Public Entrance

This area contains conceptual posters and reading notes.

Visual materials are not substitutes for theoretical documents, empirical evidence, or formal proof. They provide supplementary points of entry into the conceptual system.

---

## 10. `07_Creative_Offshoots` — Outward Contact and Expressive Experiments

`07_Creative_Offshoots` is not a new definition owner for core concepts. It observes what becomes visible, what is lost, and which residuals return when SO's public concepts contact external vocabularies, forms, and sensibilities through literature, creative work, comparative worldmaking, and related expression.

`Literary_Essays` is currently present as the public contact surface. A formal README, publication boundary, and return protocol for this layer will be settled in the next structural pass. This System Map therefore makes the existence and function of 07 visible without pre-empting authority that has not yet been assigned.

---

## 11. `90_Repository_Governance` — Repository Governance

This region contains governance rather than substantive research. It governs publication, commensuration, terminology, concept ownership, assessment, and release alignment.

| Document or area | Responsibility |
|---|---|
| [`Publication_and_Commensuration_Policy.md`](../90_Repository_Governance/Publication_and_Commensuration_Policy.md) | authoritative-language relations, preservation contract, language formats, concept ownership, lineage |
| [`Translation_Note.md`](../90_Repository_Governance/Translation_Note.md) | recurring cross-document English commensuration decisions |
| [`Scientific_Terminology_Protocol.md`](../90_Repository_Governance/Terminology/Scientific_Terminology_Protocol.md) | contact protocol between scientific vocabulary and SO-internal vocabulary |
| `Terminology/TERM_COLLISION_REGISTRY.*` | collision surfaces and misreading candidates in established vocabulary |
| [`Repository_Assessment_Commensuration_and_Navigator_Design.ja.md`](../90_Repository_Governance/Repository_Assessment_Commensuration_and_Navigator_Design.ja.md) | governance design record connecting assessment, commensuration, and Navigator |
| [`Assessment/Repository_Assessment_Protocol.ja.md`](../90_Repository_Governance/Assessment/Repository_Assessment_Protocol.ja.md) | candidate repository-assessment protocol; candidacy does not automatically grant public conceptual authority |
| `Release_Update/` | centralized release facts and synchronization of release-facing metadata |

`GLOSSARY.md` gives a human-readable view of current standard terms and public definition ownership; `docs_manifest.yml` gives a machine-readable view of document contracts. A disagreement between them is itself a collation target rather than a reason to silently treat either representation as infallible.

---

## 12. `tools`, `scripts`, `.github`, and `navigator` — Machine-Readable Governance and Public Projection

| Area | Responsibility |
|---|---|
| [`tools/Public_Format_Registry.yml`](../tools/Public_Format_Registry.yml) | document types, metadata, language formats, public-validation structure |
| [`tools/docs_manifest.yml`](../tools/docs_manifest.yml) | inventory, authoritative/commensurated relations, concept ownership, imports / exports / returns / delegations |
| [`tools/maintenance_rules.yml`](../tools/maintenance_rules.yml) | terminology replacement, collision prevention, publication boundaries, warning conditions |
| `tools/docs_index.json` / `docs_graph.json` / public projections | generated read models derived from governance sources |
| [`scripts/check_public_format.py`](../scripts/check_public_format.py) | pre-publication validation of Markdown, links, metadata, and document relations |
| `scripts/validate_docs_manifest.py` / contract / Navigator checks | regression checks for manifest contracts, document contracts, and UI projection |
| `.github/workflows/` | automated checks and deployment on repository events |
| `navigator/` | Public / Developer reader projection; not an authority for definition ownership or registration approval |

Generated read models and Navigator make the public system easier to inspect. Presentation convenience must not be allowed to flow backward into theoretical authority.

---

## 13. `99_Private_Core_Not_Included` — Marker of the Private Boundary

This directory is not a place for explaining non-public core material.

It marks both that non-public source bodies, private runtimes, personality-core material, internal evaluation, and detailed implementation or operational parameters may exist, and that the public system must not require readers to accept invisible authority derived from them.

Detailed private titles, paths, correspondence tables, or indexes should not accumulate here.

---

## 14. Research Dynamics and Return Paths

This system is not a one-way hierarchy applied from top to bottom.

```text
01–03  three core layers
  ↓
04     public applications and reflexive audit
  ↓
05     developing research and formalization candidates
  ↓
06     visual public entrance
  ↓
07     contact with external expression and creative work
  ↓
implementation results / criticism / misreading / residuals / objections
  ↓
00     Concept Network / Truth Management / System Map
  ↓
return to canonical owners, applications, and research lines
```

A return path does not exist only to assimilate lower-layer results into a higher theory. Deciding not to change an existing definition, retaining a result as a local hypothesis, or keeping material outside the public layer are also legitimate outcomes of return.

SO Reflexive Philosophical Research applies the return path to SO's own judgments. Correctness / Logic / Structural Studies returns points where formalization loses conditions present in the original concepts. Creative Offshoots returns visibility, misreading, creative transformation, and residuals produced when concepts leave their definition-owning contexts.

---

## 15. Public Exclusion Rules

Public releases exclude at least the following under `.gitignore` and related boundary rules:

- drafts and working files whose basename begins with `000`;
- `.venv/`, `venv/`, and other local environments;
- `__pycache__/`, `*.pyc`, and other caches;
- checker output and local IDE / OS / temporary / backup files;
- private source bodies, internal logs, non-public core material, and detailed operational material; and
- private-bearing pre-withdrawal snapshots and Git backups.

Presence in a working ZIP, local preservation, and inclusion in a public release are different states. Publication is determined through the manifest, ignore rules, release packaging, and human review together.

---

## 16. Reading Entrances

Purpose-specific entrances are as follows.

- Whole-system orientation: [`README.md`](../README.md) → [`Scientific_Ontology_Concept_Network.en.md`](./Scientific_Ontology_Concept_Network.en.md)
- Foundational concepts: `Four_Axioms_of_Existence` → `Boundary_Realism_Principle`
- Cognition and meaning: Boundary Epistemological Critique → Cognitive Axis Formation → Optional Axiom Modules → Truth Management
- Ethics, organization, and peace: Cognitive Dynamics → Port Allocation → Organizational Boundary → Specification for Peace
- Judgment and reflexive audit: [`SO_Reflexive_Philosophical_Research`](../04_Applications/SO_Reflexive_Philosophical_Research/README.md) → Judgment Transparency Topology → Historical Attestation
- Correctness and formalization: [`Correctness_Logic_and_Structural_Studies`](../05_Research_Notes/Correctness_Logic_and_Structural_Studies/README.md)
- Expressive and creative contact: [`Questions, Boundaries, and Peace`](../07_Creative_Offshoots/Literary_Essays/Questions_Boundaries_and_Peace.en.md)
- Physics-adjacent research: Physics Correspondence Policy → Physical Cosmological Notes
- Publication and commensuration rules: Glossary → Publication and Commensuration Policy → Term Collision Registries

---

## 17. Maintenance Principles

The System Map is not intended to be rewritten as a complete inventory whenever an individual document is added.

It should be revised primarily when:

- a directory's structural responsibility changes;
- public entrances or reading routes change;
- a research line, application surface, or outward-contact surface acquires an independent responsibility;
- responsibilities of governance, machine-readable metadata, or Navigator change; or
- the public/private boundary or release-packaging rules change.

Ordinary additions and removals of individual files should be managed in directory READMEs, `docs_manifest.yml`, generated read models, and release notes.

When a whole-system operating policy, cross-cutting research line, or public entrance changes, the root README, Roadmap, `00_Overview/README.md`, Concept Network, System Map, Glossary, and Research Notes Index should be reviewed as one structural update unit.

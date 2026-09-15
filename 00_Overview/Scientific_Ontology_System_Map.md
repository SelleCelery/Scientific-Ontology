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

ここで境界は、隔てる線や壁だけではない。異なる履歴、主体、制度、意味、環境が接触し、通過、拒否、変換、保持、返送を起こす**通路・緩衝地帯**でもある。存在境界論は、この緩衝地帯を主要な観測面として扱う。

この観測には、公開体系上の広い意味での**応用形而上学**を主に用いる。応用形而上学は、存在、時間、可能性、認識、意味、物質、非存在などを最初から別々の専門領域へ閉じず、必要なかぎり最も大きな境界を取って構造を問う方向である。一方、[`Boundary_Realism_Principle.md`](../01_Sat_Truth/Boundary_Realism_Principle.md)は、その広がりをそのまま確認済み実在へ昇格させないための公開上の責任境界を置く。

したがって、応用形而上学と境界実在論は競合する二体系ではない。前者が問いの境界を広く取り、後者が人間側の確認可能性と主張責任を制約する。この往復が、Sat / Truthを中心とする中核三相の構造規定へつながる。

存在境界論は、主観側、客観側、横断研究、その他の異なる言語ゲームのどれか一つを最終言語として選ぶことから始めない。それぞれの成立条件、観測範囲、主張強度、限界を保持したまま、境界へ持ち寄って照合できる場を整えること自体を研究対象とする。通約は同一化ではなく、差異、非同一性、残差、返路を追跡可能にする操作である。

また、v5系開始時に追加された[`Scientific_Ontology_Operational_Outline.ja.md`](./Scientific_Ontology_Operational_Outline.ja.md)は、境界事件、作用、返り、責任分界、可動性という運用方向を提示する。これは新しい上位公理ではなく、既存概念を外部実装へ持ち出すための全体方針である。

公開体系では、元型、内在的批判・拡張、応用、レンダリング、外部曝露を一方向の階段にせず、相互に返路を持つ異なる機能として分ける。

---

## 2. リポジトリ全体の構造

公開リポジトリは、現在、次の領域として読むのが最も安定している。

| 領域 | 主な場所 | 役割 |
|---|---|---|
| 公開入口 | ルート、`00_Overview` | 全体説明、概念地図、運用方針、Roadmap、Glossary、読解経路 |
| 元型・生成核 | `01_Sat_Truth`–`03_Tam_Goodness` | 最広域の構造規定、通信動態、規約・意味構築を三相として扱う中核 |
| スピンアウト・応用 | `04_Applications` | 01–03と必要に応じて05を、心理・経済・政治・AI・制度・設計・実践へ持ち出す |
| 内在的批判・拡張 | `05_Research_Notes` | SOの共有文法の内側から元型を批判・拡張し、強い仮説や分野横断研究を保持する |
| レンダリング研究 | `06_Visual_Materials` | 01–05を別の知覚・表現形式へ写し、保持と損失を照合する |
| 外部・異質系への曝露 | `07_Creative_Offshoots` | とくに01–03を共有文法の外へ晒し、通約失敗、反論、反証候補、残差を受け取る |
| リポジトリ統治 | `90_Repository_Governance`、`tools`、`scripts`、`.github`、`navigator` | 通約、用語衝突、文書契約、登録、検査、公開投影 |
| 公開境界 | `99_Private_Core_Not_Included`、`.gitignore` | 非公開資料、作業草稿、公開除外対象との境界表示 |

ここで`navigator`は公開文書を読むための投影面であり、概念定義や登録判断の所有者ではない。現在の文書同一性、正本・通約関係、概念所有、imports / exports / returnsなどの機械可読な関係は[`tools/docs_manifest.yml`](../tools/docs_manifest.yml)を基準とする。

この区分は成熟度や重要度の序列ではない。04–07は、01–03からの**距離と機能**の違いを表す。v5.1では既存配置の全面移動を行わず、役割境界を先に固定する。

---

## 3. 公開リポジトリ構造

System Mapは、個別ファイルを一つずつ固定する目録ではなく、**どの領域が何を担当し、どこへ返すか**を示す。正確な文書一覧はmanifestと各READMEへ委ね、ここでは変化しにくい構造だけを示す。

```text
.
├─ README.md / GLOSSARY.md / Roadmap.md / RELEASE_NOTES.md
├─ CITATION.md / CITATION.cff / LICENSE.md / .zenodo.json
│
├─ 00_Overview/                  # 公開地図・運用・主張強度・対応方針
│
├─ 01_Sat_Truth/                # 構造規定・応用形而上学・実在性・認識/真理条件
├─ 02_Raj_Beauty/               # 通信・履歴・差分・動態・エネルギー的対応語彙
├─ 03_Tam_Goodness/             # 公理・規約・通約・意味構築・返路・倫理
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
│          # historical method record / attestation / evidence / residuals
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
├─ 06_Visual_Materials/          # 01–05のレンダリング研究
│
├─ 07_Creative_Offshoots/
│  ├─ Literary_Essays/          # 読み物・表現からの外部接触
│  └─ Adversarial_Exposure/     # 異質な対象への曝露・監査・残差返送
│
├─ 90_Repository_Governance/
│  ├─ Publication and Commensuration Policy
│  ├─ Translation Note
│  ├─ Terminology/
│  ├─ Assessment/               # candidate protocol; public authorityではない
│  └─ Release_Update/
│
├─ 99_Private_Core_Not_Included/
│
├─ navigator/                   # public/developer projection surface
├─ tools/                       # manifest / registry / maintenance / generated read models
├─ scripts/                     # validators / builders / release helpers
└─ .github/workflows/           # automated checks and deployment
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

## 6. `01`–`03` — 元型三相の構造的役割

三層は固定的な学問区分ではなく、存在境界論が境界を読むための**元型的な三相**である。同じ文書・問題が複数相へ接触しうるため、ディレクトリ配置を排他的な分類として読まない。

### 6.1 `01_Sat_Truth` — 構造規定と最広域境界

Sat / Truthは、存在境界論が最も大きく境界を取り、構造そのものを規定する位相である。公開上は応用形而上学を主要な探索姿勢とし、Boundary Realismによってその主張可能域を制約する。

存在・実在性だけでなく、認識が成立する条件、真理条件、意味成立、観測、正しさの暫定的成立と再開可能性がここへ派生する。これは「形而上学なら何でも01」という意味ではなく、構造を何によって成立させるかという問いが中心である。

### 6.2 `02_Raj_Beauty` — 通信・差分・動態

Raj / Beautyは、境界を横断して何が動き、どの履歴と差分を作り、どの方向へ認識を形成するかを扱う位相である。通信、履歴場、差分、同期・非同期、認識軸形成が中心になる。

エントロピー、エネルギー、エクセルギー、熱、圧などの語彙は、境界での移動・散逸・利用可能性を読む接触語彙としてこの位相へ寄る。ただし、個別文書で形式的対応を明示しない限り、SO内部の用法を標準物理量と同一視しない。強い物理・宇宙論仮説の本体は05へ隔離する。

### 6.3 `03_Tam_Goodness` — 公理・規約・意味構築

Tam / Goodnessは、認識された差分を、何を受け入れ、保留し、接続し、閉じ、再び開くかという規約へ組織する位相である。認識形式から生じる公理、通信規約、通約、意味構築、仮閉鎖、返路、責任、境界倫理がここへ寄る。

倫理は後付けの道徳装飾ではない。異なる認識形式や履歴を接触させたあと、破壊的同一化や切断へ崩さず、意味と責任をどのように運用するかというプロトコル条件として現れる。

三相は、真・美・善を固定的に分割する序列でも、専門分野の棚でもない。**Satが構造を規定し、Rajが境界横断の運動を扱い、Tamがその運動を公理・規約・意味として運用可能にする**、という主たる機能差として読む。

---

## 7. `04_Applications` — スピンアウトと公開応用

`04_Applications`は、01–03の元型と、必要に応じて05で育った批判・拡張を、心理、経済、政治、AI、組織、制度、社会設計、インターフェースなどへスピンアウトさせる。

ここでは、存在の根源性そのものより、理論を別の対象領域へ持ち出したときに、どの判断・設計・責任・返路が必要になるかが主題になる。したがって、04は05より「完成している」層でも、05の単純な下流でもない。安定した元型から直接応用する場合と、05の拡張を受けて応用する場合がある。

- `AI_Adaptation`：AI側の応答構造と境界機能。
- `Social_Boundary_Design`：社会側の責任境界、照合、制度、平和条件。
- `SO_Reflexive_Philosophical_Research`：SO自身の判断生成・分類・公開判断へ境界監査を返す再帰的応用面。

Volume Iは、De-Registryから判断透明性、Topology-first監査、三層変換監査へ至る方法史を、成功だけに整形せず保持する。historical checksumは当時の記録として保持し、2026年現在の受理判断とは別にattestationを置く。旧sourceはidentity、historical filename、SHA-256、provenance、実験上の役割を公開できるが、exact bytesはprivateに保持し、公開Repositoryには含めない。

ここでいう**判断透明性**は、判断の正しさを保証する概念ではない。接触、位相、経路、返路、open endを再構成可能にし、異議、再評価、修正が実際の変更点へ届く状態を指す。

---

## 8. `05_Research_Notes` — 元型への内在的批判と拡張

`05_Research_Notes`は、01–03の元型をSOの共有文法の内側から批判し、拡張する研究面である。公開基礎へ直ちに統合するには主張強度、専門依存、誤読リスク、成熟度のいずれかに距離がある研究線を、返路を保ったまま置く。

Research Notesへの配置は、重要度が低いことや未成熟であることを意味しない。基礎性、成熟度、主張強度、公開層は別軸である。05で育った研究は、定義ownerへ返ることも、04へスピンアウトすることも、06でレンダリングを試すこともある。また07から返った外部残差が継続研究になる場合の主要な受け皿でもある。

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

## 9. `06_Visual_Materials` — レンダリング研究

`06_Visual_Materials`は、01–05までの概念・研究を別の知覚・表現形式へ写すレンダリング研究面である。現在の公開成果物は概念ポスターと読解注記を中心とする。

視覚資料は理論本文、実証資料、形式的証明の代替ではない。図にしたことで何が見えやすくなり、何が圧縮され、どの条件・留保・主張強度を本文へ戻さなければならないかまでを扱う。

06は原文書との対応を維持することを主目的とし、共有文法そのものを外す07とは区別する。

---

## 10. `07_Creative_Offshoots` — 外部・異質系への曝露

`07_Creative_Offshoots`は、中核概念の新しい定義所有者ではない。とくに01–03の元型を、SOの共有文法を前提にしない異質な語彙、価値体系、世界観、生活上の問い、反論、表現形式へ曝露する外部接触面である。

05が共有文法の内側から元型を批判・拡張するのに対し、07は共有そのものを仮定しない。そのため、理解不能、通約失敗、前提衝突、理解後の反論、反例・反証候補、適用限界、価値衝突を可能な範囲で分けて保持し、区別できないものは未分類の残差として残す。

現在は二つの接触面を持つ。

- `Literary_Essays`：読み物・表現から入り、理論を先に要求せず接触を起こす。
- `Adversarial_Exposure`：公開元型をBusiness、対人関係、履歴継承などの異質な対象へ持ち出し、監査と残差返送を行う。

外部通約は普及だけのためではなく、SO内部では生成しにくいdefeaterや摩擦を受け取るIngressでもある。ただし、外部から来たという理由だけで優先せず、05または該当definition ownerで再照合する。

07から生じた研究が独自の語彙・方法・対象を持って自立した場合、将来別領域へスピンアウトする可能性は残すが、08という層を現時点では作らない。

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

この体系は、上から下へ一方向に適用される階層ではない。01–03を元型的な生成核とし、その周囲に異なる機能の接触面を置く。

```text
                         ┌────────────→ 07 外部・異質系への曝露
                         │                  │
01–03 元型・生成核 ─────┼→ 05 内在的批判・拡張 ──┐
     │                   │          │              │
     │                   └──────────┴→ 04 応用・スピンアウト
     │                                      │
     └──────────── 01–05 ───────────────→ 06 レンダリング研究
                                                │
                 反論・失敗・圧縮損失・残差・異議
                                                ↓
                              05 / canonical owner / 04へ返送
```

返路は「下位の結果を上位理論へ取り込んで同化する」ためだけにあるのではない。既存定義を変更しない、局所仮説として保持する、公開層へ移さない、理解不能と反証を分離したまま保留する、といった判断も返りの一種である。

SO Reflexive Philosophical Researchは、この返路をSO自身の判断へ適用する。Correctness / Logic / Structural Studiesは、形式化が原概念を取りこぼす地点を返す。Visual Materialsは、レンダリングで失われた条件をsourceへ返す。Creative Offshootsは、共有文法の外へ出たときに発生する通約失敗、反論、反証候補、創造的変形、残差を返す。

v5.1では役割境界を明示するが、既存文書の全面的な再配置は行わない。カテゴリー混在の監査は後続の独立工程とする。

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
- 外部接触・異質系への曝露：[`07_Creative_Offshoots`](../07_Creative_Offshoots/README.md) → [`自動運転された正しさを止めるために`](../07_Creative_Offshoots/Adversarial_Exposure/自動運転された正しさを止めるために.ja.md) / [`問いを閉じず、境界を踏まないために`](../07_Creative_Offshoots/Literary_Essays/Questions_Boundaries_and_Peace.ja.md)
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

Scientific Ontology does not claim to possess existence itself or exhaustively describe its final nature.

Its principal public objects include:

- boundaries;
- contact;
- history;
- return;
- residuals and residue;
- downstream conditions; and
- re-collatability.

A boundary is not only a dividing line or wall. It is also a **passage and buffer zone** where distinct histories, agents, institutions, meanings, and environments meet and where admission, rejection, transformation, retention, and return occur. Scientific Ontology treats this buffer zone as a principal surface of observation.

For that purpose it primarily uses **applied metaphysics** in a broad public sense: a direction of inquiry that takes the widest workable boundary across existence, time, possibility, cognition, meaning, matter, and nonexistence before closing them into separate specialist domains. [`Boundary_Realism_Principle.md`](../01_Sat_Truth/Boundary_Realism_Principle.md), however, places the public responsibility boundary that prevents this reach from being silently promoted into confirmed reality.

Applied metaphysics and Boundary Realism are therefore not competing systems. The former takes a wide boundary for inquiry; the latter constrains what humans may responsibly claim to have confirmed. Their movement back and forth informs the structural determination expressed through the three core phases, centered on Sat / Truth.

Scientific Ontology does not begin by selecting the subjective, objective, cross-disciplinary, religious, literary, institutional, or scientific language game as its final language. It attempts to retain the conditions, observational range, claim strength, and limits of each while creating a boundary surface on which they can be collated. Commensuration is not identity; it makes transformation, difference, residuals, and return paths traceable.

The [`Scientific Ontology Operational Outline`](./Scientific_Ontology_Operational_Outline.en.md) provides a high-level orientation around boundary events, effects, return, responsibility boundaries, and mobility. It is not a new superior axiom but a way of carrying existing concepts toward external operation.

The public system therefore distinguishes the archetypal core, internal critique and extension, application, rendering, and external exposure as different functions with return paths rather than as a one-way ladder.

---

## 2. Overall Repository Architecture

The public repository is most stably read through the following regions.

| Region | Main location | Responsibility |
|---|---|---|
| Public entrance | root, `00_Overview` | overall explanation, maps, operating orientation, Roadmap, Glossary, reading routes |
| Archetypal / generative core | `01_Sat_Truth`–`03_Tam_Goodness` | the three phases of broad structural determination, communication dynamics, and protocol / meaning construction |
| Spinout and application | `04_Applications` | carries 01–03 and, where needed, 05 into psychology, economics, politics, AI, institutions, design, and practice |
| Internal critique and extension | `05_Research_Notes` | critiques and extends the archetype within a shared SO grammar while retaining strong hypotheses and cross-domain research |
| Rendering research | `06_Visual_Materials` | projects 01–05 into other perceptual and expressive forms and collates what is retained or lost |
| External / heterogeneous exposure | `07_Creative_Offshoots` | exposes especially 01–03 outside the shared grammar and receives failed commensuration, objections, candidate refutations, and residuals |
| Repository governance | `90_Repository_Governance`, `tools`, `scripts`, `.github`, `navigator` | commensuration, terminology collision, document contracts, registration, checking, public projection |
| Public boundary | `99_Private_Core_Not_Included`, `.gitignore` | marks the boundary against private material, working drafts, and excluded public-release content |

`navigator` is a projection surface for reading the public documents, not an owner of definitions or registration judgments. Machine-readable document identity, language relations, concept ownership, imports, exports, returns, and delegations are governed by [`tools/docs_manifest.yml`](../tools/docs_manifest.yml).

These regions are not ranks of maturity or importance. Layers 04–07 differ mainly by **distance and function** relative to the archetypal core. v5.1 fixes these role boundaries without performing a comprehensive migration of existing documents.

---

## 3. Public Repository Structure

The System Map is not a fixed inventory of every file. It shows **which region is responsible for what and where results return**. Exact inventories belong to the manifest and directory READMEs.

```text
.
├─ README.md / GLOSSARY.md / Roadmap.md / RELEASE_NOTES.md
├─ CITATION.md / CITATION.cff / LICENSE.md / .zenodo.json
│
├─ 00_Overview/                  # public maps, operation, claim strength, correspondence policy
│
├─ 01_Sat_Truth/                # structural determination, applied metaphysics, reality, cognition/truth conditions
├─ 02_Raj_Beauty/               # communication, history, difference, dynamics, energetic correspondence vocabulary
├─ 03_Tam_Goodness/             # axioms, protocols, commensuration, meaning construction, return, ethics
│
├─ 04_Applications/
│  ├─ AI_Adaptation/
│  ├─ Social_Boundary_Design/
│  └─ SO_Reflexive_Philosophical_Research/
│     ├─ research context / open questions (ja + en)
│     ├─ sources/README.md
│     │    # public: source identity / hash / provenance / role
│     │    # exact historical bytes remain outside the public repository
│     └─ volumes/Volume_01_DeRegistry_to_Judgment_Transparency/
│          # historical method record / attestation / evidence / residuals
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
├─ 06_Visual_Materials/          # rendering research over 01–05
│
├─ 07_Creative_Offshoots/
│  ├─ Literary_Essays/          # outward contact through readable expression
│  └─ Adversarial_Exposure/     # heterogeneous exposure, audit, residual return
│
├─ 90_Repository_Governance/
│  ├─ Publication and Commensuration Policy
│  ├─ Translation Note
│  ├─ Terminology/
│  ├─ Assessment/               # candidate protocol; not public authority
│  └─ Release_Update/
│
├─ 99_Private_Core_Not_Included/
│
├─ navigator/                   # public/developer projection surface
├─ tools/                       # manifest / registry / maintenance / generated read models
├─ scripts/                     # validators / builders / release helpers
└─ .github/workflows/           # automated checks and deployment
```

Absence from this diagram does not imply exclusion from publication. Current document state is checked through the manifest, directory READMEs, and Navigator read models. Conversely, mention here does not itself establish definition ownership or registration.

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

## 6. `01`–`03` — Structural Responsibilities of the Three Archetypal Phases

The three layers are not fixed academic disciplines but **archetypal phases** through which Scientific Ontology reads boundaries. A document or problem may touch more than one phase; directory placement is not an exclusive classification.

### 6.1 `01_Sat_Truth` — Structural Determination and the Widest Boundary

Sat / Truth is the phase in which Scientific Ontology takes its widest boundary and asks what structure is being posited. Publicly, applied metaphysics provides the main exploratory orientation while Boundary Realism constrains the range of responsible claims.

Questions of existence and reality therefore sit alongside the conditions of cognition, truth, meaning, observation, and provisional correctness. This does not mean that every metaphysical speculation belongs in 01; the central question is what makes a structure count as formed and publicly assertable.

### 6.2 `02_Raj_Beauty` — Communication, Difference, and Dynamics

Raj / Beauty asks what moves across a boundary, what histories and differences are produced, and how cognitive direction forms. Communication, history-fields, difference, synchronization and desynchronization, and cognitive-axis formation are central.

Entropy, energy, exergy, heat, and pressure may appear here as contact vocabulary for movement, dissipation, and availability. Unless a local document explicitly establishes a formal correspondence, SO usage is not identified with standard physical quantities. Stronger physical and cosmological hypotheses remain isolated in 05.

### 6.3 `03_Tam_Goodness` — Axioms, Protocols, and Meaning Construction

Tam / Goodness organizes recognized differences into rules for what may be admitted, suspended, connected, closed, reopened, or returned. Cognitive axioms, communication protocols, commensuration, meaning construction, provisional closure, return paths, responsibility, and boundary ethics gather here.

Ethics is not a moral ornament added afterward. It appears as a protocol condition for operating across distinct cognitive forms and histories without collapsing into destructive identity or severance.

The three phases are neither a ranking of Truth, Beauty, and Goodness nor a set of disciplinary shelves. Their principal distinction is functional: **Sat determines structure, Raj treats boundary-crossing movement, and Tam makes that movement operable as axiom, protocol, and meaning**.

---

## 7. `04_Applications` — Spinout and Public Application

`04_Applications` carries the archetype of 01–03 and, where needed, critiques or extensions developed in 05 into psychology, economics, politics, AI, organizations, institutions, social design, and interfaces.

Its main question is no longer ontological fundamentality itself but what conditions of judgment, design, responsibility, and return are required when the theory enters another domain. Layer 04 is therefore neither “more complete” than 05 nor simply downstream from it. Stable core concepts may spin out directly, while other applications may depend on extensions developed in 05.

- `AI_Adaptation`: response structures and boundary functions on the AI side.
- `Social_Boundary_Design`: responsibility boundaries, collation, institutions, and conditions of peace on the social side.
- `SO_Reflexive_Philosophical_Research`: a recursive application surface returning boundary audit to SO's own judgments, classifications, and publication decisions.

Volume I preserves the methodological history from De-Registry through judgment transparency, topology-first auditing, and three-layer transformation audit without rewriting it as an uninterrupted success. Historical checksums remain historical; present acceptance is separately attested. Source identity, historical filename, SHA-256, provenance, and experimental role may be public while exact historical bytes remain private.

**Judgment transparency** does not guarantee correct judgment. It means that contact, phase, route, return path, and open ends remain reconstructable so that objections and revisions can reach the actual point of change.

---

## 8. `05_Research_Notes` — Internal Critique and Extension of the Archetype

`05_Research_Notes` is the research surface for critiquing and extending the archetype of 01–03 from within enough of SO's shared grammar to make the disagreement traceable. It retains research lines whose claim strength, specialist dependence, misreading risk, or maturity makes immediate integration into the public foundations inappropriate.

Placement in Research Notes does not imply low importance or immaturity. Fundamentality, maturity, claim strength, and publication layer are separate axes. Work developed in 05 may return to a concept owner, spin out into 04, be tested through rendering in 06, or receive residuals first exposed in 07.

### 8.1 `Language_Meaning_and_Communication_Phase_Studies`

A cross-cutting research line treating language, meaning, grammar, speech, commensuration, semantic networks, and AI language generation as communication phases with return paths. It does not replace the Meaning Generation Model and holds local responsibility for linguistic meaning.

### 8.2 `Cognitive_Dynamics_Communication_Studies`

Studies continuous cognition together with the operational discretization needed for existence phases, ports, capacity, and responsibility, connecting to organizational boundaries, boundary diplomacy, and peace specifications.

### 8.3 `Correctness_Logic_and_Structural_Studies`

Studies whether correctness, logic, structural representation, closure, redundancy, frontier, cognitive axes, and finite-resource computation can be commensurated into formal and computational expressions **without redefining existing SO concepts**.

At present the README is the research entrance. Formalization candidates including `Spine` are not canonical definitions. Even useful formalization must return conditions and residuals lost in the mapping to the original concept owners.

### 8.4 Other research lines

- `Cross_Domain_Ontological_Notes`: asymmetry, return ethics, narrative, consent boundaries, and other cross-domain readings.
- `Physical_Cosmological_Notes`: stronger physics- and cosmology-adjacent hypotheses and correspondence candidates.
- `Social_Boundary_Notes`: AI adoption, social boundaries, value circulation, and DSSI-related research.
- `AI_Personality_Notes`: AI personality, history loops, return stability, and logical sandboxes.
- `Literary_Ontological_Notes`: literature read as worldmaking, history, belief, and boundary rather than empirical proof.

DSSI implementation code is not bundled in the SO repository. Results returned from the externally released ConnectBits / DSSI implementation are treated on the SO side as research input about observation, responsibility, and return paths, not as proof of the theory.

See [`Research_Notes_Index.md`](../05_Research_Notes/Research_Notes_Index.md) for document-level detail.

---

## 9. `06_Visual_Materials` — Rendering Research

`06_Visual_Materials` is the rendering-research surface for projecting concepts and research from 01–05 into other perceptual and expressive forms. Its current public artifacts are primarily conceptual posters and reading notes.

Visual materials are not substitutes for theoretical texts, empirical evidence, or formal proof. The task includes asking what becomes visible through rendering, what is compressed away, and which conditions, reservations, and claim-strength information must return to the source text.

Layer 06 primarily preserves correspondence with its sources and is therefore distinct from 07, which intentionally removes the assumption of shared grammar.

---

## 10. `07_Creative_Offshoots` — External and Heterogeneous Exposure

`07_Creative_Offshoots` is not a new definition owner for core concepts. It is an external-contact surface that exposes especially the archetype of 01–03 to vocabularies, value systems, worldviews, practical questions, objections, and expressive forms that do not presuppose SO's shared grammar.

Where 05 critiques and extends the archetype from inside a shared grammar, 07 does not assume that sharing. It therefore retains, as far as possible, distinctions among incomprehension, failed commensuration, premise collision, objection after understanding, counterexample or candidate refutation, limits of application, and value conflict. Differences that cannot yet be classified remain residuals.

It currently contains two contact surfaces:

- `Literary_Essays`: contact through readable expression without requiring prior mastery of the theory.
- `Adversarial_Exposure`: exposure of public archetypes to heterogeneous subjects such as Business, interpersonal relations, and inherited histories, followed by audit and residual return.

Outward commensuration is not only dissemination. It is also an Ingress for defeaters and friction that are difficult to generate inside SO's own grammar. External origin gives such input no automatic priority; it returns to 05 or the relevant definition owner for re-collation.

A line born in 07 may eventually spin out into an independent region if it develops its own stable vocabulary, method, and object domain. No layer called 08 is established at present.

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

This system is not a one-way hierarchy. Layers 01–03 form an archetypal generative core around which several distinct contact functions operate.

```text
                         ┌────────────→ 07 external / heterogeneous exposure
                         │                  │
01–03 archetypal core ───┼→ 05 internal critique / extension ──┐
     │                   │          │                           │
     │                   └──────────┴→ 04 application / spinout
     │                                      │
     └──────────── 01–05 ───────────────→ 06 rendering research
                                                │
                   objections / failures / rendering loss / residuals
                                                ↓
                                return to 05 / canonical owner / 04
```

A return path is not only a mechanism for absorbing lower-layer results into higher theory. Non-revision, local retention as a hypothesis, continued exclusion from the public layer, or suspension while incomprehension is distinguished from refutation can all be legitimate return outcomes.

SO Reflexive Philosophical Research applies return to SO's own judgment process. Correctness / Logic / Structural Studies returns points where formalization loses conditions from source concepts. Visual Materials returns conditions lost through rendering. Creative Offshoots returns failed commensuration, objections, candidate refutations, creative deformation, and residuals exposed outside the shared grammar.

v5.1 makes these role boundaries explicit without performing a comprehensive migration of existing documents. Category-mixing audit remains a later independent task.

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
- External contact and heterogeneous exposure: [`07_Creative_Offshoots`](../07_Creative_Offshoots/README.en.md) → [`Stopping Correctness on Autopilot`](../07_Creative_Offshoots/Adversarial_Exposure/Stopping_Correctness_on_Autopilot.en.md) / [`Questions, Boundaries, and Peace`](../07_Creative_Offshoots/Literary_Essays/Questions_Boundaries_and_Peace.en.md)
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

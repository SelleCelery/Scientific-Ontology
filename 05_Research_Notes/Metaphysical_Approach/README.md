# Metaphysical Approach / 形而上学的アプローチ

> Layer: 05_Research_Notes / Metaphysical_Approach
> Status: README
> Scope: generative metaphysics / formation provenance / historical computation / physics-adjacent correspondence / audit engineering / falsification and return
> Language: Japanese authoritative; English commensuration available
> Public profile: P2
> Authority: Directory navigation and research-line boundary contract; not a public concept-definition owner

---

# 日本語正本

英語通約: [`README.en.md`](README.en.md)

## 1. Directory Role / ディレクトリの位置づけ

本ディレクトリは、AMP、ITS、Gödel系の形成資料から供給されてきた生成像を、現在の存在境界論へ無標識に逆投影せず、**生成形而上学、履歴、物理近接対応、監査・正しさの工学化を相互に照合する研究面**として保持する。

ここで扱う文書は、一つの完成した形而上学正本を構成するものではない。旧AMP/ITSの強い主張、現在の生成形而上学候補、物理近接仮説、監査理論、実装仕様を、それぞれの主張強度と成立履歴を保ったまま並置し、何を後続の正本候補へ返せるかを検討する。

特に、次の二層を区別する。

1. **生成形而上学・形成源・物理近接研究**

   分化、関係の持続、論理形成、固定・回収、時間、観測、自己参照へ至る生成経路と、その形成源・歴史計算・物理近接対応を扱う。

2. **Engineering Research on Correctness**

   正しさ、閉鎖、矛盾、Spine、余剰、論理平面、監査α・βを、論理・構造・計算へ通約し、実装可能性と失われる差分を検査する。

後者は前者から自動的に導出されるものではなく、前者を証明するものでもない。また、監査実装が成功しても、生成形而上学またはSO正本の妥当性が証明されたとは扱わない。

### 構造上の位置

```text
旧AMP / ITS / Gödel系形成資料
  ↓ 形成源として参照
Metaphysical Approach
  ├─ 生成形而上学・履歴・物理近接研究
  └─ Engineering Research on Correctness
       ↓ 論理・構造・計算への通約
       実装候補 / toy model / machine-readable audit surface
  ↓
反例・不一致・残差・実装失敗・外部知見
  ↓
関連する正本・研究線・将来のv6再構成へ返送
```

このディレクトリは、v6の応用形而上学正本を先取りして確定する場所ではない。現時点で正本候補へ向かう道筋を可視化しつつ、未確定部分、物理対応の強度、監査実装との距離を残す研究面である。

## 2. Public Scope / 公開範囲

### 2.1 含むもの

- AMP・ITS・Gödel系文書を論証根拠ではなく形成上の補給線として読む研究
- 分化、持続、機能、構造、差分、固定、回収、時間、観測、自己参照を生成順序から再検討する研究
- 履歴を不可逆な出来事と、現在から再構成可能な依存関係へ分ける歴史計算モデル
- 光、因果、距離、空間、時間などを標準物理学と同一視せずに接触させる物理近接仮説
- 正本候補『応用形而上学体系』へ向かう概説・検討稿
- 監査が必要になる形而上学的条件の研究
- α監査・β監査、論理平面、Spine、余剰、有限資源探索の研究
- LLMと決定的計算を分担させる監査実装仕様候補
- 実装・通約・外部領域との不一致を残差として保持し、上流へ返すための研究

### 2.2 含まないもの

- v6応用形而上学正本がすでに確定したという宣言
- AMP/ITSの旧い物理対応を、そのまま現在のSO正本へ採用すること
- 標準物理学、宇宙論、数理論理学、数学、計算機科学の定義の上書き
- 研究ノートに置かれた生成仮説を、経験科学的に確立した事実として扱うこと
- `Spine`その他の研究語を、未審理のまま公開基礎語彙へ昇格させること
- 監査実装またはmachine auditの成功を、理論の正しさの証明とすること
- `000*`で保持される形成資料、旧稿、局所作業物を公開索引またはManifestへ登録すること

## 3. Documents / 文書一覧

### 3.1 生成形而上学・形成源・物理近接研究

- [`AMP・ITS・ゲーデル試論から読む生成形而上学の補給線.ja.md`](AMP・ITS・ゲーデル試論から読む生成形而上学の補給線.ja.md) / [`EN`](Formation_Supply_Line_from_AMP_ITS_and_Godel_to_Generative_Metaphysics.en.md)

  AMP、ITS、Gödel系試論を、現在のSO命題を証明する根拠ではなく、問いと生成像を供給した形成源として整理する。

- [`現代科学の因果関係を拡張する.ja.md`](現代科学の因果関係を拡張する.ja.md) / [`EN`](Extending_Causality_in_Modern_Science.en.md)

  持続・機能・構造・差分・ロックから、生成論的な因果の射程を研究する。現代科学の因果説明を置換しない。

- [`存在境界論的歴史計算構造.ja.md`](存在境界論的歴史計算構造.ja.md) / [`EN`](Historical_Computation_Structure_in_Scientific_Ontology.en.md)

  不可逆な出来事の履歴と、現在の依存構造の再構成を分け、Return、Reopening、探索資源、再構成余力を扱う。

- [`光の読み方とそれに伴うアポリアの再配置.ja.md`](光の読み方とそれに伴うアポリアの再配置.ja.md) / [`EN`](Reading_Light_and_Relocating_Its_Aporias.en.md)

  有限通信、内在時間、履歴から、光・空間・時間・因果の読み方を再配置する物理近接研究。標準物理学との非同一性を保持する。

- [`応用形而上学体系_概説書_検討稿.ja.md`](応用形而上学体系_概説書_検討稿.ja.md) / [`EN`](Applied_Metaphysics_System_Overview.en.md)

  正本候補『応用形而上学体系』の生成経路を概説する検討稿。v6正本を確定する文書ではなく、現在の再構成方向を可視化する。

### 3.2 Engineering Research on Correctness

[`Engineering Research on Correctness/`](Engineering%20Research%20on%20Correctness/) は、正しさ・監査・論理構造を実装可能な表現へ近づける内部研究線である。

- [`存在境界論における監査理論.ja.md`](Engineering%20Research%20on%20Correctness/存在境界論における監査理論.ja.md) / [`EN`](Engineering%20Research%20on%20Correctness/Audit_Theory_in_Scientific_Ontology.en.md)

  なぜ監査が必要になるかを、非対称性、侵襲、自己参照、無、持続、Returnから検討する。

- [`論理平面・論理深度・次元変換から読むαβ監査試論.ja.md`](Engineering%20Research%20on%20Correctness/論理平面・論理深度・次元変換から読むαβ監査試論.ja.md) / [`EN`](Engineering%20Research%20on%20Correctness/Alpha_Beta_Audit_through_Logical_Plane_Logical_Depth_and_Dimensional_Transformation.en.md)

  αとβを、同一平面内部の成立性と、平面生成・外部化の問題へ分ける研究試論。

- [`α監査_構造仕様と計算機LLM分担設計.ja.md`](Engineering%20Research%20on%20Correctness/α監査_構造仕様と計算機LLM分担設計.ja.md) / [`EN`](Engineering%20Research%20on%20Correctness/Alpha_Audit_Structural_Specification_and_Computer_LLM_Division_of_Labor.en.md)

  α監査の閉鎖、矛盾、Spine、余剰を対象に、LLMによる構造候補抽出と決定的計算による判定を分担させる実装仕様候補。

- [`β監査の実装モデルの推移.ja.md`](Engineering%20Research%20on%20Correctness/β監査の実装モデルの推移.ja.md) / [`EN`](Engineering%20Research%20on%20Correctness/Evolution_of_Beta_Audit_Implementation_Models.en.md)

  Gödel的論理深度の理念から、Dual-Closure、Path、外部跳躍、構造健全性へ至る実装形成史を比較する。

- [`インテリジェンスの発達とその監査.ja.md`](Engineering%20Research%20on%20Correctness/インテリジェンスの発達とその監査.ja.md) / [`EN`](Engineering%20Research%20on%20Correctness/Development_of_Intelligence_and_Its_Audit.en.md)

  インテリジェンスの形成・安定・再開と監査可能性を接続する研究ノート。

- [`全・無・切断・未選択可能性の関係試論.ja.md`](Engineering%20Research%20on%20Correctness/全・無・切断・未選択可能性の関係試論.ja.md) / [`EN`](Engineering%20Research%20on%20Correctness/Whole_Null_Cut_and_Unselected_Possibility.en.md)

  AMPの未分化の全、無、切断、未選択可能性の関係を、無標識に同一化せず検討する。

`000*`の文書は形成資料・比較資料としてローカルに保持し、公開索引、Manifest、Release対象には含めない。

## 4. Reading Routes / 読解経路

このディレクトリに単一の必読順序は置かない。目的に応じて次の入口を使う。

### 4.1 v6応用形而上学再構成を見る

```text
形成上の補給線
  ↓
現代科学の因果関係を拡張する
  ↓
歴史計算 / 光のアポリア再配置
  ↓
応用形而上学体系 概説
```

この経路は、旧AMP/ITSをそのまま新正本へ移植する順序ではない。何が形成源として残り、何が現在の生成記録へ再配置されつつあるかを見るための読解経路である。

### 4.2 監査研究を見る

```text
監査理論
  ↓
論理平面・論理深度・αβ試論
  ↓
α監査の構造仕様
  ↘
   β監査実装モデルの推移
```

αとβの方法は研究資産として保持するが、Repository全体への監査実施が完了したことを意味しない。

## 5. Upstream and Return Paths / 上流と返路

### 5.1 主な上流

- [`../../01_Sat_Truth/Boundary_Epistemological_Critique.ja.md`](../../01_Sat_Truth/Boundary_Epistemological_Critique.ja.md)
- [`../../01_Sat_Truth/正しさ・個性・無・切断_論理通信トポロジー.ja.md`](../../01_Sat_Truth/正しさ・個性・無・切断_論理通信トポロジー.ja.md)
- [`../../02_Raj_Beauty/Entropy_Attributed_Difference_and_Cognitive_Axis_Formation.ja.md`](../../02_Raj_Beauty/Entropy_Attributed_Difference_and_Cognitive_Axis_Formation.ja.md)
- [`../../00_Overview/Physics_Correspondence_Policy.ja.md`](../../00_Overview/Physics_Correspondence_Policy.ja.md)
- [`../../00_Overview/Truth_Management_and_Boundary_PDCA.ja.md`](../../00_Overview/Truth_Management_and_Boundary_PDCA.ja.md)

AMP/ITS/Gödel系形成資料は、本ディレクトリの形成源ではあるが、現在の公開正本を上書きする上位権限として扱わない。

### 5.2 返路

- 正しさ、無、切断、審理条件に関する差分は`01_Sat_Truth`へ返す。
- 認識軸・履歴場に関する差分は`02_Raj_Beauty`および関連Research Notesへ返す。
- 物理対応の強度・不一致はPhysics Correspondence Policyを経由して保持する。
- 監査実装の失敗、抽出不能、偽陽性・偽陰性は、理論反証と実装失敗を分けて研究線へ返す。
- 応用形而上学正本の再構成は、v6側の明示的な正本改訂として行い、本ディレクトリから自動採用しない。

## 6. Maintenance Notes / 運用メモ

- 日本語を正本とし、英語通約は別ファイルで維持する。
- `000*`はGit除外・公開索引外の形成資料として扱う。
- 個別文書に旧Revision表記が本文メタデータとして残る場合、それは形成履歴であり、公開ファイル名へ版番号を持ち込まない。
- 生成形而上学、物理対応、監査理論、実装結果を一つの主張強度へ平坦化しない。
- 閉鎖と正しさ、実装成功と理論妥当性、形成源と正本を同一視しない。
- 標準分野の定義を優先し、SO内部の対応は対応として記録する。
- 新しい研究文書を追加した場合は、本README、`../Research_Notes_Index.md`、`../../tools/docs_manifest.yml`を同時に確認する。
- Repository全体へのα／β監査の実施時期は、このREADMEでは確定しない。

# Correctness, Logic, and Structural Studies / 正しさ・論理・構造研究

> Layer: 05_Research_Notes / Correctness_Logic_and_Structural_Studies
> Status: README
> Scope: correctness / logic / structural representation / closure / redundancy / frontier / cognitive axes / finite-resource computation / re-collation
> Language: Japanese authoritative; English commensuration pending
> Public profile: P2
> Authority: Directory navigation and research-line boundary contract; not a public concept-definition owner

---

# 日本語正本

## 1. Directory Role / ディレクトリの位置づけ

本ディレクトリは、存在境界論ですでに扱われている境界、履歴、意味ループ、認識軸、履歴場、切断、残差、返路、再照合可能性などを、**論理・構造・計算の言語へ通約し、実装可能な表現へ写したときに何が保持され、何が失われるかを検査する研究線**である。

新しい独立理論を立てること、存在境界論の基礎概念をこの研究線から再定義すること、実装上うまく動いた構造をそのまま存在論的事実へ昇格させることを目的としない。

言語・意味・通信位相研究が、言語という高密度な自己反照面からSOの構造を読み直すのに対し、本研究線は、**正しさ、閉鎖、冗長性、未閉鎖、支持構造、認識軸、可能性空間を、論理的・構造的・計算的に扱う面**を受け持つ。

### 構造上の位置

```text
01–03 公開基礎 / 既存Research Notes
  ↓ 既存概念と関係を受け取る
05 Correctness, Logic, and Structural Studies
  ↓ 論理・構造・計算への通約
Prompt / toy model / computational implementation
  ↓
直接観測・失敗・残差・実装上の差分
  ↓
定義所有文書・関連研究線へ返送
```

この研究線で問うのは、理論上の答えをゼロから作り直すことではない。

> **既に置かれている関係を計算可能な構造へ写したとき、その関係を壊さず作動させられるか。**

これを主要な検査課題とする。

## 2. Public Scope / 公開範囲

### 2.1 含むもの

- 「正しい」を、有限な観測・知識・履歴・資源のもとで成立、保持、失効、再照合される動的状態として扱う形式化候補
- 局所閉鎖、偽閉鎖、未閉鎖、残差、切断を論理・構造上で区別する試み
- 現在構造を支える経路と、閉鎖済みの冗長経路、代替可能性、破断、外向きFrontierの区別
- 履歴場、認識軸、論理空間・可能性空間の関係を、非同一性を保ったまま計算構造へ写す研究
- `Spine`を、履歴依存で再利用可能な支持構造を扱う**研究上の構造表現候補**として検査すること
- 閉ループと冗長性だけでは捉えきれない未処理差分、余剰、open-end、frontierの検出候補
- 既存LLMへのprompt支援と、決定論的toy model・構造AIの双方を、通約の忠実度を検査する実験面として利用すること
- 計算資源の配分、保持、休眠、再活性化を、構造上の必要性と探索圧に結びつける実装仮説

### 2.2 含まないもの

- 世界についての最終的・普遍的な「正しさ」を所有するアルゴリズム
- 存在境界論の基礎概念が数学的・計算機科学的に証明済みであるという主張
- 標準論理学、数学、トポロジー、情報理論、熱力学、計算機科学の定義の上書き
- `Spine`をSO公開基礎の確立済み中核語として扱うこと
- 実装成功を、そのまま存在論的妥当性または経験科学的真理の証明とすること
- 個人の人格、思想、病理、身体状態を構造分類から診断すること
- 非公開の実装パラメータ、安全評価条件、誘導手順、Private Core

エネルギー、エクセルギー、重力、ダークエネルギー等の語を用いる場合は、標準物理量との同一性を自動的に主張しない。実装上の資源配分や構造変化との対応は、まず構造アナロジーまたは形式化候補として扱う。

## 3. Research Surfaces / 現在の研究面

現在の主な研究面は次である。

1. **正しさの動的状態**
   成立、保持、失効、再照合を、静的なtruth labelとは別の状態遷移として表現できるか。

2. **閉鎖・冗長性・Frontier・切断**
   現在空間を支える閉鎖構造、代替可能な閉鎖済み冗長構造、外へ伸びる未閉鎖端、本来の支持経路の破断を区別できるか。

3. **Spine・認識軸・可能性空間**
   支持構造、安定した観測方向、現在到達可能な論理／認識空間を同一視せず、相互作用として扱えるか。

4. **個性と形成履歴**
   同じ観測対象や局所規則を持っていても、形成履歴と探索方向の違いが異なる到達可能性を生むことを構造として表現できるか。

5. **計算資源と探索**
   現在の支持構造を維持する資源、冗長性を残す資源、未閉鎖差分へ向かう探索資源を区別し、効果を観測できるか。

この一覧は、将来作成すべきファイル一覧ではない。**実体のある研究が生じたときだけ文書を追加し、空の分類や将来課題を先に作業負債として置かない。**

## 4. Documents / 文書一覧

現時点では、本READMEのみを研究線の公開境界として置く。

個別研究文書、実験記録、英語通約は、実体が成立した時点で追加する。未実施の課題を、空ファイルや空ディレクトリとして先行登録しない。

非公開の形成草稿、会話記録、Private Coreは、この公開文書一覧へ含めない。必要な知見を公開側へ移す場合は、出所、主張強度、非主張境界を再照合してから別文書として登録する。

## 5. Upstream and Return Paths / 上流と返路

### 5.1 上流

- [`../../01_Sat_Truth/Boundary_Epistemological_Critique.ja.md`](../../01_Sat_Truth/Boundary_Epistemological_Critique.ja.md)
  同期、照合、残差保持、理性による局所閉鎖、偽閉鎖、再照合可能性。

- [`../../01_Sat_Truth/Boundary_Realism_Principle.md`](../../01_Sat_Truth/Boundary_Realism_Principle.md)
  存在そのものを直接所有せず、境界、履歴、返りを実在的な記述対象とする公開側の制御原理。

- [`../../02_Raj_Beauty/Entropy_Attributed_Difference_and_Cognitive_Axis_Formation.ja.md`](../../02_Raj_Beauty/Entropy_Attributed_Difference_and_Cognitive_Axis_Formation.ja.md)
  関心、捨象、価値、コスト、残差、反復による認識軸の形成・安定・変形。

- [`../../02_Raj_Beauty/History_Field_Topology.md`](../../02_Raj_Beauty/History_Field_Topology.md)
  履歴を持つ場、結節、ループ、返路、切断、残差を扱う構造FRAME。

- [`../../00_Overview/Truth_Management_and_Boundary_PDCA.ja.md`](../../00_Overview/Truth_Management_and_Boundary_PDCA.ja.md)
  命題的真理と運用的真理、局所閉鎖、偽閉鎖、再開可能性、目的と境界CA。

- [`../Language_Meaning_and_Communication_Phase_Studies/Meaning_as_Collation_and_Return_Path.ja.md`](../Language_Meaning_and_Communication_Phase_Studies/Meaning_as_Collation_and_Return_Path.ja.md)
  意味の照合、返路、局所閉鎖。

- [`../Language_Meaning_and_Communication_Phase_Studies/Intension_Extension_and_False_Extension.ja.md`](../Language_Meaning_and_Communication_Phase_Studies/Intension_Extension_and_False_Extension.ja.md)
  内包、外延、返路ある接続、偽外延。

- [`../Cognitive_Dynamics_Communication_Studies/README.md`](../Cognitive_Dynamics_Communication_Studies/README.md)
  シームレスな認識・通信を操作可能な構造へ離散化し、実装から上流へ誤って逆投影しないための近接研究線。

### 5.2 返路

- 認識軸の定義・生成条件に関する差分は`02_Raj_Beauty`へ返す。
- 履歴場、ループ、切断、残差の構造差は、それぞれの定義所有文書と`History_Field_Topology`へ返す。
- 閉鎖、偽閉鎖、再開、返路に関する規約差は`01_Sat_Truth`、`03_Tam_Goodness`、Truth Managementへ返す。
- 実装可能性、AI利用、インターフェースへ進んだ成果は`04_Applications`との接続を検討する。
- 標準論理学、数学、計算機科学、物理学との不一致は、SO側へ都合よく吸収せず、外部領域の定義を保持したまま未解決差分として残す。

実装結果は、SO正本を自動的に更新しない。

## 6. Maintenance Notes / 運用メモ

- 既存SO正本、Human-sideの研究仮説、AIによる形式化、実装、直接観測、AI解釈、Human-sideの再読を区別する。
- `Spine`は現段階では研究候補語であり、Loop、履歴場、認識軸と無標識に同一化しない。
- **閉鎖していることと正しいことを同一視しない。**
- **冗長であることと不要であることを同一視しない。** 現在不要でも、支持構造の破断時に代替可能性を持つ場合がある。
- **未閉鎖Frontierと破断を同一視しない。** 前者は探索方向であり得るが、後者は現在の可能性空間を縮退させる故障であり得る。
- 探索予算を使い切ったことを、「到達可能な反例が存在しない」ことへ昇格させない。
- 実装が目的関数を達成しても、SO概念の妥当性が証明されたとは扱わない。逆に、実装失敗も、通約の誤りと理論側の反証を区別する。
- 実装都合だけで、上流理論に存在しない操作を前メタ段階へ追加しない。
- 標準分野の用語を使用するときは、その分野の定義を優先し、SO内部の構造対応と区別する。
- 公開後の反例、実装失敗、異議、残差は研究線へ返すが、自動統合しない。
- **実体のない将来課題のためにファイルやサブディレクトリを先行作成しない。**

# English Commensuration Status

English commensurated rendering is pending. The Japanese text is authoritative at this stage.

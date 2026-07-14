# Claim Strength and Publication-Layer Table for Scientific Ontology
# 存在境界論｜主張強度・公開レイヤー対応表

> Status: Public control table  
> Scope: claim strength / epistemic risk / application risk / publication layer / verification / rendering distance  
> Language: Japanese authoritative; English labels included  
> Claim strength: classifier  

---

## 0. この表は何を管理するのか

本表は、存在境界論の命題、文書、語彙について、次を区別して管理するための公開制御表である。

- 命題そのものの強さ
- 誤読・批判の起こりやすさ
- 応用・転用による危険
- 公開時に必要な減速
- 今後の検証・形式化段階
- 中核語彙から各分野の言語ゲームへの距離

これらは、同じ尺度ではない。

主張が強いことは、実証済みであることを意味しない。

誤読リスクが高いことは、命題が誤りであることを意味しない。

応用可能性が高いことは、公開すべきであることを意味しない。

公開レイヤーが低いことは、重要性が低いことを意味しない。

本表のラベルは、読者への権威づけや順位づけではない。

何をどの文脈で語り、どこで限定し、どこを留保し、どこから別文書へ委ねるかを管理するためのものである。

---

## 1. 判定順序 / Evaluation Order

S / E / U / P / V / R は、横並びの評価点ではない。

- **S / Claim Strength**：命題そのものが、どこまで強い存在論的・理論的主張を行うか。
- **E / Epistemic Risk**：既存分野との衝突、疑似科学化、過剰一般化など、誤読・批判上のリスク。
- **U / Use Risk**：診断、操作、統治、安全回避などへ転用されるリスク。
- **P / Publication Layer**：S・E・Uを踏まえた最終的な公開レイヤー。
- **V / Verification Stage**：今後どの検証・形式化段階へ進めるか。
- **R / Rendering Distance**：公開中核語彙から、どの言語ゲーム・応用・物理近接・形而上学層へ射影されているか。

判定は、次の順で行う。

```text
1. 命題の責務と適用範囲を確認する。
2. Sコードで主張強度を判定する。
3. Sコードから暫定公開レイヤー P_base を置く。
4. Eコードで認識・批判リスクによる減速を行う。
5. Uコードで応用・安全リスクによる抽象化または非公開化を行う。
6. Rコードで、どの言語ゲームへ射影されているかを確認する。
7. 最終公開レイヤー P_final を決定する。
8. Vコードで今後の検証・形式化段階を別途管理する。
```

簡易式で表せば、次の通りである。

```text
P_final = decelerate(P_base(S), E, U, context(R))
```

Rは、単独で公開可否を決めない。

ただし、R4またはR5の語彙は、同じ文面でもE3へ接近しやすいため、通常より強い限定と非主張境界を必要とする。

---

## 2. Sコード――主張強度 / Claim Strength

| Code | 名称 / Label | 意味 | 公開上の基本扱い |
|---|---|---|---|
| S0 | 用語整理 / Terminological organization | 体系内の便宜的な定義、索引、分類。外部理論への強い主張を伴わない。 | P0を基本とする。 |
| S1 | 構造アナロジー / Structural analogy | 異なる領域に似た関係構造があると比較する。 | 比喩・比較であることを明示する。 |
| S2 | 存在論的再解釈 / Ontological reinterpretation | 既存の対象・現象を、境界、履歴、返り等の枠で読み直す。 | 限定条件つきで公開する。 |
| S3 | 作業仮説 / Working hypothesis | 体系内部で説明・接続に用いるが、外部検証が十分でない仮説。 | 仮説・試論と明記する。 |
| S4 | 形式化候補 / Formalization candidate | 状態変数、演算、更新規則、比較表、評価指標へ落とせる候補。 | OverviewまたはResearch Notesで慎重に扱う。 |
| S5 | 強い存在論・科学接続候補 / High-strength ontological or scientific candidate | 物自体、物理学、生命、意識等について、既存分野と正面接続しうる強い命題。 | 通常公開層を直接支配させず、強い減速または非公開とする。 |

### 2.1 Sコードからの暫定公開レイヤー

| S | P_base | 基本理由 |
|---|---|---|
| S0 | P0 | 用語整理・索引として公開可能。 |
| S1 | P0-P1 | 構造比較として公開可能だが、事実化を避ける。 |
| S2 | P1 | 存在論的再解釈であり、適用範囲を明示する。 |
| S3 | P1-P2 | 作業仮説として公開し、確立理論と分ける。 |
| S4 | P2 | 形式化候補としてOverviewまたはResearch Notesへ置く。 |
| S5 | P2-P3 | 高強度研究層として内部精査を優先する。 |

---

## 3. Eコード――認識・批判リスク / Epistemic Risk

| Code | 名称 / Label | 主な危険 | 必要な処理 |
|---|---|---|---|
| E0 | 低リスク / Low | 通常の定義・索引として誤解が少ない。 | 通常公開。 |
| E1 | 説明不足リスク / Definition risk | 用語不足、範囲不足により誤解される。 | 定義、例、関連文書を足す。 |
| E2 | 分野衝突リスク / Disciplinary collision | 哲学史、心理学、経済学、法学等の標準概念を置き換えたと読まれうる。 | 標準分野を置換しないこと、独自定義の範囲を明記する。 |
| E3 | 疑似科学・教義化リスク / Pseudoscientific or doctrinal risk | 物理主張、医学主張、宗教的実在、万能理論、文学的証明として読まれうる。 | P2以上へ減速し、非主張境界、標準定義、検証不足を明記する。 |

### 3.1 Eコードによる調整

| E | 調整 |
|---|---|
| E0 | P_baseを維持する。 |
| E1 | 定義・例・リンクを追加する。通常はPを維持する。 |
| E2 | 少なくともP1とし、標準分野との境界を書く。 |
| E3 | 原則P2以上へ退避し、必要に応じてP2.5またはP3とする。 |

---

## 4. Uコード――応用・安全リスク / Use and Safety Risk

| Code | 名称 / Label | 主な危険 | 公開判断 |
|---|---|---|---|
| U0 | 低リスク / Low | 直接的な操作・診断・回避能力をほぼ与えない。 | 通常公開。 |
| U1 | 誤用リスク / Misuse | 雑な引用、過剰一般化、比喩の事実化、他者への貼付が起こりうる。 | 注記つき公開。 |
| U2 | 転用リスク / Transfer risk | 人物分類、組織操作、説得、制度判断、安全判断へ転用されうる。 | 抽象化し、禁止用途を書く。 |
| U3 | 運用保全リスク / Operational integrity risk | 詳細公開により、境界保全、セキュリティ、非公開評価機構が弱くなる。 | 原則P3。概念蒸留版のみP2.5。 |
| U4 | 秘匿必須 / Restricted | 分類以上を公開すると具体的な危害または保全性低下が見込まれる。 | P3固定。 |

### 4.1 Uコードによる調整

| U | 調整 |
|---|---|
| U0 | P_baseを維持する。 |
| U1 | 原則P1以上とし、誤用例を示す。 |
| U2 | P2-P2.5を検討し、操作手順・診断表を出さない。 |
| U3 | 詳細非公開。概念的説明だけをP2.5へ出せる。 |
| U4 | 非公開。分類以上を出さない。 |

---

## 5. Pコード――公開レイヤー / Publication Layer

| Code | 名称 / Label | 意味 |
|---|---|---|
| P0 | 公開中核 / Public core | 定義、入口、基礎構造として通常公開できる。 |
| P1 | 減速公開 / Decelerated public | 範囲、非主張事項、標準分野との違いを付けて公開する。 |
| P2 | 研究公開 / Research publication | 強い仮説、対応候補、試論として公開する。確立理論と分ける。 |
| P2.5 | 抽象化公開 / Abstracted publication | 中核概念は公開するが、診断、操作、身体対応、安全評価等の詳細を伏せる。 |
| P3 | 非公開 / Non-public | 通常公開体系へ含めない。分類、存在、方針だけを示す場合がある。 |

公開レイヤーは、ファイル単位だけでなく、同一文書内の節ごとに異なりうる。

たとえば、認識軸生成論の公開中核はP1であっても、身体部位との対応、診断、誘導手順へ進めばP2.5-P3になる。

---

## 6. Vコード――検証・形式化段階 / Verification Stage

| Code | 名称 / Label | 意味 |
|---|---|---|
| V0 | 概念整合 / Conceptual coherence | 用語、責務、非矛盾、文書間接続を確認する。 |
| V1 | 対応表・反例表 / Mapping and counterexample table | 既存理論との対応、相違、適用限界、反例を整理する。 |
| V2 | Toy Model / Minimal model | 最小モデル、プロトコル、架空例で作動条件を確認する。 |
| V3 | 評価実験 / Evaluation | AI応答、対話ログ、組織事例、創作構造等で評価する。 |
| V4 | 数理化・シミュレーション / Formalization and simulation | 変数、状態、更新規則、遷移、評価指標を導入する。 |
| V5 | 外部理論との予測比較 / Predictive comparison | 既存科学または実証領域と比較可能な予測・計算へ接続する。 |

Vが高いことは、命題が正しいことを意味しない。

次にどの検査を行えるかを示す。

---

## 7. Rコード――中核語彙からのレンダリング距離 / Rendering Distance

Rコードは、命題が存在境界論の公開中核から、どの言語ゲームへ射影されているかを示す補助軸である。

「遠い」ことは「劣る」ことではない。

翻訳層と非主張境界が増えることを意味する。

| Code | 名称 / Label | 主な領域 | 取扱い |
|---|---|---|---|
| R0 | 中核語彙 / Core vocabulary | 境界、接触、履歴、差分、返り、切断、残差、照合 | 定義を固定し、分野ごとに安易に変えない。 |
| R1 | 近接展開 / Near-core extension | 意味ループ、認識軸、同期、非同期、責任境界、アポリア | 中核語彙との接続を明記する。 |
| R2 | 分野横断通約 / Cross-domain commensuration | 認識論、倫理、真理、物語、文化、価値 | 各分野の標準概念を尊重し、SO内部定義と分ける。 |
| R3 | 組織・制度・技術実装 / Organizational and applied rendering | 組織境界、ポート、AI導入、DSSI、社会設計 | 実装例、責任主体、停止条件を要求する。 |
| R4 | 物理近接レンダリング / Physical-near rendering | 場、粒子、ボソン、エンタングルメント、ファインマンダイアグラム、BlackHole | 原則E3。標準物理定義との非同一性を明記する。 |
| R5 | 高強度形而上学 / High-strength metaphysical projection | AMP、ITS、物自体側、根源仮説 | 通常公開層の権威源にせず、P3または強い蒸留を基本とする。 |

### 7.1 言語ゲーム群

周辺語彙は、単一の辞書的意味だけでは管理しない。

どの言語ゲームで使われているかを記録する。

| Language game | 例 | 主な注意 |
|---|---|---|
| Ontological | 境界、履歴、無、存在、関係 | 物自体の直接所有と混同しない。 |
| Epistemological | 感性、悟性、認識軸、同期、照合 | 心理診断や哲学史の置換にしない。 |
| Ethical | 返り、責任、非破壊距離、報復変換 | 法的処罰・自力救済の手順にしない。 |
| Organizational | ポート、プロトコル、監査、外交 | ネットワーク工学との類比を事実同一視しない。 |
| Economic | ネゲントロピー、交換熱、価値、コスト | 経済学・熱力学の確立量として扱わない。 |
| Physical-near | ボソン場、フェルミオン的ソリトン、エンタングルメント | Physics Correspondence Policyを先に適用する。 |
| Literary and mythic | 転生、信念重力圏、神、悪魔、冥府 | 宗教的・科学的実在証明にしない。 |
| Implementation | AI境界機能、DSSI、判断場維持 | 実装主体、責任、ログ、撤退条件を要求する。 |

---

## 8. 中核語彙 / Core Vocabulary

以下は、v4.3.0における公開中核語彙である。

| 項目 | 公開定義 | Type | S | E | U | P | V | R |
|---|---|---|---|---|---|---|---|---|
| Scientific Ontology / 存在境界論 | 存在そのものを直接所有せず、境界、接触、履歴、返り、後続条件を実在的に扱う公開概念体系。 | 公開体系 | S2-S3 | E1-E2 | U0 | P0-P1 | V0-V1 | R0-R2 |
| Boundary / 境界 | 外部入力と内部履歴が接触し、通過、保留、遮断、変換、再符号化、反射が起こる面。 | 中核定義 | S2 | E1 | U0 | P0 | V0-V1 | R0 |
| Contact / 接触 | 異なる存在・履歴・場が、互いの後続条件を変えうる形で関係する出来事。 | 中核定義 | S2 | E1 | U0 | P0 | V0 | R0 |
| History / 履歴 | 単なる過去記録ではなく、次の受け取り方、反応、判断、意味づけを変える構造。 | 中核定義 | S2 | E0-E1 | U0 | P0 | V0-V1 | R0 |
| Difference / 差分 | 境界へ接触し、反応、違和感、意味、切断、残差を生じさせる相違。 | 中核定義 | S2 | E1 | U0 | P0 | V0-V1 | R0 |
| Return / 返り | 接触と履歴変化の後に現れる反作用、応答、修復要求、学習、意味更新。 | 中核定義 | S2-S3 | E1 | U1 | P0-P1 | V0-V2 | R0-R1 |
| Cutoff / 切断 | 通信、履歴接続、返路、観測可能性が遮断されること。 | 中核定義 | S2-S3 | E1 | U1 | P0-P1 | V0-V1 | R0 |
| Residual / 残差 | 観測、分類、説明、照合によって閉じきれず、再照合可能な差分として残るもの。 | 中核定義 | S2-S3 | E1 | U0 | P0-P1 | V0-V1 | R0 |
| Residue / 残渣 | 処理後も身体、制度、関係、環境、記号、未来等に沈殿し、作用し続ける履歴的負荷。 | 存在論的再解釈 | S2-S3 | E1-E2 | U1 | P1 | V1-V2 | R1-R2 |
| Collation / 照合 | 異なる履歴、定義、証拠、境界条件を比較し、一致、不一致、残差を保持する操作。 | 中核定義 | S2-S3 | E1 | U0-U1 | P0-P1 | V0-V3 | R0-R2 |
| Return Path / 返路 | 出力、責任、異議、修正、意味が原主体または次の処理主体へ戻る経路。 | 近接概念 | S2-S3 | E1 | U1 | P1 | V1-V3 | R1-R3 |
| Aporia / アポリア | 同一平面では閉じない矛盾、分岐、未接続を、次の照合対象として保持した状態。 | 方法論概念 | S2-S4 | E1-E2 | U0 | P1-P2 | V1-V4 | R1-R2 |

---

## 9. 認識・意味・認識ブリッジ / Cognition and Cognitive Bridge

| 項目 | 公開定義 | Type | S | E | U | P | V | R |
|---|---|---|---|---|---|---|---|---|
| Entropy-attributed difference / エントロピー属性つき差分 | 差分が履歴、拡散性、凝集性、価値化・コスト化可能性を帯びて境界へ現れると読む。 | 認識モデル | S2-S3 | E2-E3 | U1 | P1-P2.5 | V0-V2 | R1-R2 |
| Attention / 関心 | 差分を保持し、追跡し、現実として前景化する方向。 | 認識概念 | S2 | E1-E2 | U1 | P1 | V0-V2 | R1-R2 |
| Abstraction / 捨象 | 認識成立のため、差分を背景化、保留、切断、別処理へ送る操作。 | 認識概念 | S2 | E1-E2 | U1 | P1 | V0-V2 | R1-R2 |
| Sensibility / 感性 | 何が感じられる差分として立ち上がるかの開口。カント哲学の厳密な再定義ではない。 | SO補助語彙 | S2-S3 | E2 | U1 | P1 | V0-V2 | R2 |
| Understanding / 悟性 | 感じられた差分が、対象、関係、原因、責任等として整理される編成。 | SO補助語彙 | S2-S3 | E2 | U1 | P1 | V0-V2 | R2 |
| Cognitive Axis / 認識軸 | 関心、捨象、価値、コスト、残差、反復によって安定した観測方向。 | 動態モデル | S2-S3 | E2-E3 | U1-U2 | P1-P2.5 | V0-V3 | R1-R2 |
| Meaning Loop / 意味ループ | 差分が履歴へ統合され、保留、切断、返り、後続条件を伴う意味として閉じる循環。 | 意味生成モデル | S2-S3 | E2 | U0-U1 | P1 | V0-V3 | R1-R2 |
| Optional Axiom Module / 選択公理モジュール | 世界観を、関心、捨象、価値、コスト、Core Invariant、Operational Driftとして比較する単位。 | 認識ブリッジ | S2-S3 | E1-E2 | U1-U2 | P1-P2.5 | V0-V3 | R2 |
| Cognitive Bridge Protocol / 認識ブリッジ | 異なる認識形式の中核を壊さず、翻訳、保留、接続、遮断、残差保持を行う境界プロトコル。 | 通約プロトコル | S3-S4 | E2 | U1-U2 | P1-P2.5 | V1-V4 | R2-R3 |
| Core Invariant | 失うとその体系ではなくなる関心、捨象、価値、コスト、照合手続の核。 | 比較概念 | S2-S3 | E1-E2 | U1 | P1 | V1-V3 | R2 |
| Operational Drift | 同じ名称または中核を持ちながら、時代、文化、制度、運用で変形する層。 | 比較概念 | S2-S3 | E1 | U1 | P1 | V1-V3 | R2-R3 |

禁止する展開：身体部位対応、思想診断、人格型、採用・教育・治療・統治の分類表。

---

## 10. 真理・目的・組織 / Truth, Purpose, and Organization

| 項目 | 公開定義 | Type | S | E | U | P | V | R |
|---|---|---|---|---|---|---|---|---|
| Truth Management / 真理の経営学 | 目的を第一義として置き、共有が形成した世界を境界CAで検査し、目的を修正・継続・破棄する方法。 | 方法論 | S3-S4 | E2 | U1-U2 | P1-P2 | V0-V3 | R2-R3 |
| First Purpose / 第一義 | 何を守り、増やし、失ってはならないものとして置くか。停止条件と責任主体を伴う目的。 | 目的概念 | S2-S3 | E1-E2 | U1-U2 | P1 | V0-V3 | R2-R3 |
| Shared Purpose / 第二義 | 異なる境界間で、目的を言語、役割、権限、手続、異議申立てへ変換し共同運用すること。 | 運用概念 | S2-S3 | E1 | U1 | P1 | V1-V3 | R3 |
| World Formation / 第三義 | 共有された目的が、評価、資源、制度、可視性、例外、行為可能性を再配置して形成する世界。 | 運用的真理概念 | S3-S4 | E2 | U1 | P1-P2 | V1-V3 | R2-R3 |
| Boundary CA / 境界CA | 形成された世界の境界で、疲弊、外部化、異常、残差、残渣を確認し、目的・境界・運用を修正すること。 | 運用プロトコル | S3-S4 | E2 | U1-U2 | P1-P2 | V1-V4 | R3 |
| Organizational Boundary / 組織境界 | 組織が内部・外部、通信、責任、履歴、処理能力を定義する動的境界。 | 組織モデル | S3 | E2 | U1 | P1-P2 | V1-V4 | R3 |
| Responsibility Boundary / 責任境界 | 行為だけでなく、許可、監督、改善、履歴保持、例外対応を引き受ける主体の境界。 | 倫理・組織概念 | S2-S3 | E1-E2 | U1 | P1 | V1-V3 | R1-R3 |
| Port / ポート | 特定の通信を受け入れ、変換し、処理し、返す組織境界上の通信口。 | 組織・ネットワーク類比 | S2-S3 | E1-E2 | U1 | P1 | V1-V4 | R3 |
| Protocol / プロトコル | 誰が、何を、どの条件で、どの形式へ変換し、どこへ返すかを定める境界手続。 | 運用概念 | S2-S3 | E1 | U1-U2 | P1-P2 | V1-V4 | R3 |
| Negentropy Definition / ネゲントロピー定義 | 組織が何を負荷として受け入れ、何へ変換し、どの秩序・意味・ケア・判断可能性を返すかという自己定義。 | 組織・価値モデル | S2-S3 | E2 | U1 | P1-P2 | V1-V3 | R2-R3 |

---

## 11. AI・制度・社会設計 / AI, Institutions, and Social Design

| 項目 | 公開定義 | Type | S | E | U | P | V | R |
|---|---|---|---|---|---|---|---|---|
| AI as Boundary Function / AI境界機能 | AIを回答代行だけでなく、判断、照合、保留、異議申立て、責任返路を維持する境界機能として評価する。 | AI哲学・設計概念 | S2-S3 | E1-E2 | U1 | P1 | V1-V3 | R3 |
| Judgment-field maintenance / 判断場維持 | 利用者が選択肢、根拠、不確実性、撤回、異議申立てを保持できる状態を維持する。 | 実装原則 | S2-S3 | E1 | U1-U2 | P1-P2 | V2-V4 | R3 |
| AI Adoption | AI導入を、モデル性能だけでなく、調達、権限、説明、監査、例外、撤退を含む組織境界設計として扱う。 | 社会実装モデル | S3-S4 | E2 | U2 | P2-P2.5 | V2-V4 | R3 |
| DSSI | デジタル主権と判断場を支える境界インターフェースの実装例。 | 実装候補 | S3-S4 | E1-E2 | U2-U3 | P2.5 | V2-V4 | R3 |
| Peace Specification / 平和仕様 | 異なる存在相が境界と履歴を保持したまま、破壊的でない相互作用を継続できる条件を扱う。 | 社会境界モデル | S2-S3 | E2 | U1 | P1-P2 | V1-V3 | R2-R3 |
| Negentropy Economy / ネゲントロピー経済 | 意味、秩序、責任、履歴、行為可能性を回収・保持・再編成する働きとして経済を読む。経済理論、熱力学的証明、政策提案として提示しない。 | 経済哲学モデル | S2-S3 | E2 | U1-U2 | P1-P2 | V1-V3 | R2-R3 |

ネゲントロピー経済は、経済理論、熱力学的証明、政策提案として提示しない。価値循環と組織的変換を読む概念モデルに限定する。

実装系では、Uコードを概念説明と同じにしない。

具体的な警告条件、遮断条件、セキュリティ評価、人物判定、運用回避手順は別管理とする。

---

## 12. 物理近接レンダリング / Physical-Near Rendering

| 項目 | 公開定義 | Type | S | E | U | P | V | R |
|---|---|---|---|---|---|---|---|---|
| History-Field Topology / 履歴場トポロジー | 履歴を持つ場が、接触、結節、返路、切断、残差を形成する構造として読む。 | 存在論的再解釈 | S2-S4 | E2 | U0 | P1-P2 | V1-V4 | R1-R4 |
| Intrinsic Time / 内在時間 | 意味ループのコミット、履歴更新、再接続によって進む局所的な深度秩序。 | 高強度概念 | S3-S5 | E3 | U1 | P2 | V1-V5 | R4-R5 |
| Logical-Depth Axis / 論理-深度軸 | 外的時間の前後ではなく、未解決、矛盾、分岐、残差、意味圧を保持・再構成する方向。 | 形式化候補 | S3-S4 | E2 | U1 | P1-P2 | V1-V4 | R2-R4 |
| PINGER Hypothesis | 発生位相と現在断面を結ぶ履歴・通信経路が、観測断面で粒子的に見えるという物理近接仮説。 | 高強度仮説 | S4-S5 | E3 | U1 | P2 | V1-V5 | R4 |
| Particle as observed section / 粒子＝観測断面 | 場または履歴経路が、境界条件の下で安定した断面として現れると読む。 | 物理接続候補 | S4-S5 | E3 | U0 | P2 | V1-V5 | R4 |
| Boson as synchronization mediator / ボソン＝同期媒介 | ボソンを、相互作用履歴や同期の媒介という存在論的側面から読む。 | 物理接続候補 | S4-S5 | E3 | U0 | P2 | V1-V5 | R4 |
| Fermionic soliton rendering / フェルミオン的ソリトン | 局所的安定構造を、場の切断・履歴保持・観測断面として読む高強度候補。 | 高強度仮説 | S5 | E3 | U1 | P2-P3 | V1-V5 | R4-R5 |
| Feynman diagram as history topology / ファインマンダイアグラム＝履歴トポロジー | 相互作用、交換、頂点、ループ、返路、切断の図式として構造的に読む。 | 構造アナロジー・対応候補 | S2-S4 | E3 | U0 | P2 | V1 | R4 |
| Entanglement as history-field correspondence | 履歴場間の非分離的対応を、量子エンタングルメントとは区別して読む。 | 物理近接対応候補 | S4-S5 | E3 | U0 | P2 | V1-V5 | R4 |
| BlackHole as return-path loss | BlackHoleを、履歴接続の切断事象と表面返還の境界モデルとして読む。 | 物理近接対応候補 | S4-S5 | E3 | U0 | P2 | V1-V5 | R4 |

すべて、[`Physics_Correspondence_Policy.ja.md`](./Physics_Correspondence_Policy.ja.md)を適用する。

標準物理学の用語、計算、実験結果を尊重し、SO内部の概念射影を同一視しない。

---

## 13. 高強度・非公開研究層 / High-Strength and Non-Public Layer

| 項目 | 公開上の位置づけ | S | E | U | P | V | R |
|---|---|---|---|---|---|---|---|
| AMP | 境界実在論が留保する先を、応用形而上学として仮説記述する内部中核。 | S5 | E3 | U1-U2 | P3 | V0-V5 | R5 |
| ITS | 場、時間演算子、観測断面、情報時間ソリトン等を統合する高強度理論候補。 | S5 | E3 | U1-U2 | P3 | V0-V5 | R5 |
| Private Core | 個別傷、誘導条件、安全評価、非公開運用等を含みうる内部層。 | S3-S5 | E1-E3 | U3-U4 | P3 | V0-V4 | R3-R5 |

高強度・非公開層は、公開体系の秘密の権威ではない。

公開文書を正当化するために「内部では完成している」と用いてはならない。

その役割は、次である。

- 公開体系が閉じていない場所を保持する。
- 次に検査すべきアポリアを供給する。
- 形式化候補と反例を蓄積する。
- 境界実在論から返る制約によって修正される。

---

## 14. v4.3.0主要文書の分類 / Document-Level Classification

| Document | Function | S | E | U | P | V | R |
|---|---|---|---|---|---|---|---|
| `Scientific_Ontology_Concept_Network.ja.md` | 全体配置、方法論的非完結性、読み順、文書責務を示す。 | S4-S5 | E3 | U1 | P1-P2 | V0-V1 | R0-R5 |
| `Entropy_Attributed_Difference_and_Cognitive_Axis_Formation.ja.md` | 認識軸の生成、安定、硬直、漂移、分岐、再照合を扱う。 | S2-S3 | E2-E3 | U1 | P1-P2.5 | V0-V3 | R1-R2 |
| `Optional_Axiom_Modules_as_Cognitive_Bridge.ja.md` | 認識形式を比較し、通約、保留、遮断、残差保持を行う。 | S2-S3 | E1-E2 | U1-U2 | P1-P2.5 | V0-V3 | R2-R3 |
| `Truth_Management_and_Boundary_PDCA.ja.md` | 第一義、共有、世界形成、境界CAによって目的を検査する。 | S3-S4 | E2 | U1-U2 | P1-P2 | V0-V3 | R2-R3 |
| `Organizational_Boundary_and_Port_Model.ja.md` | 目的を責任境界、ポート、プロトコル、監査へ実装する。 | S3-S4 | E2 | U1-U2 | P1-P2 | V1-V4 | R3 |
| `Boundary_Realism_Principle.md` | 人間が実在的に扱える範囲を境界・履歴・返りへ制御する。 | S2-S3 | E1-E2 | U0 | P0-P1 | V0-V1 | R0-R2 |
| `Boundary_Epistemological_Critique.ja.md` | 同期、照合、残差保持、偽閉鎖によって知の成立条件を批判する。 | S3-S4 | E2-E3 | U1 | P1-P2 | V0-V4 | R1-R4 |
| `Meaning_Generation_Model.md` | 差分が履歴へ統合され、意味ループと返路を形成する条件を扱う。 | S2-S4 | E2 | U1 | P1-P2 | V0-V4 | R1-R3 |
| `PINGER_Hypothesis_and_History_Field_Topology.ja.md` | 履歴場を物理近接語彙へ射影する。 | S4-S5 | E3 | U1 | P2 | V1-V5 | R4 |

ファイル全体の分類は、節ごとの分類を代替しない。

---

## 15. 公開時の減速規則 / Publication Deceleration Rules

### 15.1 既存分野の語を使う場合

1. 標準定義を先に尊重する。  
2. SO内部の意味を明示する。  
3. 同一性ではなく、借用、アナロジー、再解釈、対応候補のどれかを示す。  
4. 適用範囲と非主張事項を書く。  

### 15.2 身体・心理へ接近する場合

- 身体部位対応表を作らない。
- 病理、体質、人格、能力を診断しない。
- 治療、介入、誘導手順を公開しない。
- 第一人称の質感記述と医学的説明を分ける。

### 15.3 思想・宗教・神話へ接近する場合

- 経験的実在の証明としない。
- 人物または集団へ固定ラベルを貼らない。
- 哲学史・宗教学の標準的記述を置き換えない。
- 関心、捨象、価値、コスト、照合手続として比較する。

### 15.4 組織・政策・AIへ接近する場合

- 責任主体を明記する。
- 異議申立て、監査、停止、撤退のポートを書く。
- 実装例のない安全主張をU3相当に引き上げない。
- 理論が判断を代行するのではなく、判断場を維持するかを確認する。

### 15.5 物理近接語彙を使う場合

- Physics Correspondence Policyを適用する。
- 標準物理学の置換ではないと明記する。
- 数学的同型、構造アナロジー、存在論的射影、物理予測を区別する。
- V5へ到達していない命題を、実証済みの物理主張として提示しない。

---

## 16. ラベルを本文へ増やしすぎない

個別文書のヘッダーには、原則として次を置く。

```text
Status
Scope
Language
Claim strength
必要な場合のみ短いPublic handling
```

文書特性、典型的誤読、依存関係、禁止用途、レンダリング距離の詳細は、YAMLレジストリ、README、本表で管理する。

読者がS/E/U/P/V/Rの意味を事前に理解していることを前提にしない。

ラベルは本文の代わりではない。

公開導線では、まず平易な非主張境界と読み順を示し、必要な読者だけが本表へ戻れるようにする。

---

## 17. v4.3.0の総合判定

v4.3.0では、個別概念の追加よりも、次の循環が明示される。

```text
差分接触
  ↓
認識軸生成
  ↓
認識形式の明示と通約
  ↓
第一義としての目的設定
  ↓
共有と世界形成
  ↓
組織境界・責任境界・ポート
  ↓
AI・制度・社会への実装
  ↓
境界CA
  ↓
残差・残渣・アポリア
  ↓
認識論・存在論・形而上学の再照合
```

この循環の公開中核は、R0-R3、S2-S4を中心とする。

物理近接レンダリングはR4、S4-S5、E3として減速する。

AMP / ITSはR5、S5、P3を基本とし、公開体系の第一主張へ直接持ち込まない。

認識軸生成と認識ブリッジは、人物分類、思想診断、身体診断へ転用しない。

真理の経営学は、権力者が真理を決定する理論として用いない。

組織境界とポートモデルは、ネットワーク工学、経営学、行政学、法学の代替として用いない。

本表は、存在境界論を弱めるためのものではない。

強い問いを、どこまで公開主張として閉じ、どこから仮説、通約、実装、アポリアとして保持するかを明示するためのものである。

---

## 18. 関連文書 / Related Documents

- [`Scientific_Ontology_Concept_Network.ja.md`](./Scientific_Ontology_Concept_Network.ja.md)
- [`Truth_Management_and_Boundary_PDCA.ja.md`](./Truth_Management_and_Boundary_PDCA.ja.md)
- [`Physics_Correspondence_Policy.ja.md`](./Physics_Correspondence_Policy.ja.md)
- [`Boundary_Realism_Principle.md`](../01_Sat_Truth/Boundary_Realism_Principle.md)
- [`Boundary_Epistemological_Critique.ja.md`](../01_Sat_Truth/Boundary_Epistemological_Critique.ja.md)
- [`Meaning_Generation_Model.md`](../01_Sat_Truth/Meaning_Generation_Model.md)
- [`Entropy_Attributed_Difference_and_Cognitive_Axis_Formation.ja.md`](../02_Raj_Beauty/Entropy_Attributed_Difference_and_Cognitive_Axis_Formation.ja.md)
- [`Optional_Axiom_Modules_as_Cognitive_Bridge.ja.md`](../03_Tam_Goodness/Optional_Axiom_Modules_as_Cognitive_Bridge.ja.md)
- [`Organizational_Boundary_and_Port_Model.ja.md`](../05_Research_Notes/Cross_Domain_Ontological_Notes/Organizational_Boundary_and_Port_Model.ja.md)
- [`Publication_and_Commensuration_Policy.md`](../Publication_and_Commensuration_Policy.md)
- [`TERM_COLLISION_REGISTRY.md`](../TERM_COLLISION_REGISTRY.md)

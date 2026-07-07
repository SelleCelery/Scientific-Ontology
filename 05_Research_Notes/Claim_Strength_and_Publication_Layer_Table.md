# 存在境界論：主張強度・公開レイヤー対応表 / Claim Strength and Publication-Layer Table for Scientific Ontology

> Status: Research table
> Scope: claim-control
> Language: ja+en
> Claim strength: classifier

---

## 0.1 判定順序 / Evaluation Order

本表では、S / E / U / P / V を横並びの分類として扱わない。

Sコードは、命題そのものの主張強度を示す。  
Eコードは、その命題がどのように誤読・批判されやすいかを示す。  
Uコードは、その命題がどのように応用・転用されうるかを示す。  
Pコードは、S・E・Uを踏まえた最終的な公開レイヤーである。  
Vコードは、公開判断ではなく、今後どの検証・形式化段階へ進めるかを示す。

したがって、公開判定は次の順で行う。

```text
1. Sコードで、命題の主張強度を判定する。
2. Sコードから、暫定的な公開レイヤー P_base を置く。
3. Eコードで、誤読・批判リスクによる減速を行う。
4. Uコードで、応用・安全リスクによる減速、抽象化、非公開化を行う。
5. 最終的な公開レイヤー P_final を決定する。
6. Vコードで、今後の検証・形式化段階を別途管理する。
```
---

## 1. 主張強度コード

| コード | 名称 | 意味 | 外部公開の扱い |
|---|---|---|---|
| S0 | 用語整理 | 体系内の便宜的な言葉。外部理論への強い主張はない。 | 公開可 |
| S1 | 構造アナロジー | 既存概念と似た構造を持つという比較。 | 比喩・比較として公開可 |
| S2 | 存在論的再解釈 | 既存概念を別の存在論的枠で読み直す。 | 注記つき公開 |
| S3 | 作業仮説 | 内部研究で使う仮説。まだ検証不足。 | 外部では仮説と明記 |
| S4 | 形式化候補 | 状態変数、演算規則、評価指標へ落とせる候補。 | Research Notes向き |
| S5 | 物理主張候補 | 既存科学と正面接続しうる強い命題。 | 内部精査優先。外部では慎重 |

---

## 2. 公開・誤読・応用リスクコード

### Pコード：公開レイヤー

| コード | 名称 | 意味 | 公開判断 |
|---|---|---|---|
| P0 | 公開可 | 概念説明・用語整理・公開用入口として安全に出せる。 | 公開可 |
| P1 | 減速公開 | 誤読リスクはあるが、注記・限定条件・非証明宣言を付ければ公開できる。 | 公開可 |
| P2 | 研究ノート公開 | 主張強度が高いが、応用危険は低い。提案・対応表・試論として公開できる。 | Research Notes向き |
| P2.5 | 抽象化公開 | 中核は有用だが、詳細手順は危険。概念だけ公開し、操作規則は伏せる。 | 要蒸留 |
| P3 | 非公開 | 分類以上の説明を公開しない情報を含む。 | 公開しない |

### Eコード：認識・批判リスク

| コード | 名称 | 意味 | 対処 |
|---|---|---|---|
| E0 | 低リスク | 誤読されにくい。 | 通常公開 |
| E1 | 説明不足リスク | 用語の説明不足で誤解される。 | 定義を足す |
| E2 | 批判圧リスク | 専門領域・読者から強い批判を受けやすい。 | 主張範囲と非主張事項を書く |
| E3 | 疑似科学化リスク | 科学主張、宗教主張、文学証明として誤読されやすい。 | Research Notesへ退避し、証明ではないと明記 |

### Uコード：応用・安全リスク

| コード | 名称 | 意味 | 公開判断 |
|---|---|---|---|
| U0 | 低リスク | 直接的な操作・介入・回避能力をほぼ与えない。 | 公開可 |
| U1 | 誤用リスク | 雑な引用、過剰一般化、比喩の事実化が起こりうる。 | 注記つき公開 |
| U2 | 転用リスク | 他者の判断、関係、制度を不安定化させる形で転用されうる。 | 抽象化して公開 |
| U3 | 運用リスク | 詳細公開により、非公開境界の保全性が下がる。 | 原則非公開 |
| U4 | 秘匿必須 | 分類以上の記述を公開しない。 | 公開禁止 |

## 2.1 Sコードからの暫定公開レイヤー / Base Public Layer from S-code

| Sコード | 暫定P | 理由 |
|---|---|---|
| S0 | P0 | 用語整理であり、外部理論への強い主張がないため。 |
| S1 | P0-P1 | 構造アナロジーとして公開可能だが、比喩の事実化に注意する。 |
| S2 | P1 | 存在論的再解釈であるため、注記・限定条件が必要。 |
| S3 | P1-P2 | 作業仮説であるため、仮説・試論として公開する。 |
| S4 | P2 | 形式化候補であり、Research Notes 向き。 |
| S5 | P2-P3 | 既存科学との正面接続を含むため、内部精査または強い減速が必要。 |

## 2.2 E/Uコードによる減速規則 / Deceleration by E/U Codes

EコードとUコードは、Sコードから導かれた暫定Pを減速・抽象化・非公開化する。

### Eコードによる調整

| Eコード | 調整 |
|---|---|
| E0 | P_base を維持する。 |
| E1 | 定義、注記、非主張事項を追加する。通常はPを維持する。 |
| E2 | 少なくともP1以上に減速し、主張範囲と非主張事項を明記する。 |
| E3 | 少なくともP2へ退避し、疑似科学化・宗教化・文学証明化を避ける。場合によってはP2.5またはP3へ送る。 |

### Uコードによる調整

| Uコード | 調整                              |
| ---- | ------------------------------- |
| U0   | P_base を維持する。                   |
| U1   | 注記つきで公開する。通常はP1以上にする。           |
| U2   | 抽象化して公開する。原則としてP2.5を検討する。       |
| U3   | 詳細公開しない。原則としてP3、または概念蒸留版のみP2.5。 |
| U4   | 公開禁止。P3固定。                      |

## 2.3 公開レイヤーの決定 / Public Layer Decision

最終的な公開レイヤーは、次のように決定する。

P_final = decelerate(P_base(S), E, U)

---

## 3. 検証・形式化コード

| コード | 名称 | 意味 |
|---|---|---|
| V0 | 概念整合 | 用語・定義の内部整合性を見る。 |
| V1 | 対応表 | 既存科学・情報理論・認知科学・社会理論との対応関係を表にする。 |
| V2 | Toy Model | 最小モデルで動作を確認する。 |
| V3 | 評価実験 | AI応答・対話ログ・創作構造などで評価する。 |
| V4 | 数理化・シミュレーション | 変数・更新規則・状態遷移を導入する。 |
| V5 | 物理予測 | 既存物理と比較可能な予測・計算へ接続する。 |


## 4. 公開概念核

| 項目 | 公開文面 | 命題種別 | S | E | U | P | V | 処理 |
|---|---|---|---|---|---|---|---|---|
| 存在境界論 / Scientific Ontology | 存在そのものを直接所有せず、境界、接触、履歴、返り、後続条件を記述可能な実在として扱う公開概念体系。 | 公開体系 / 概念フレーム | S2-S3 | E1 | U0 | P0-P1 | V0-V1 | 統一理論、宗教体系、経験科学の代替として出さない。 |
| 境界実在性の原則 | 実在的に扱う対象を、存在そのものではなく、境界、接触、履歴、返り、後続条件へ置く原則。 | 基底原則 | S2-S3 | E1 | U0 | P0-P1 | V0-V1 | 01_Sat_Truth の基底原則として扱う。 |
| 存在の留保 | 境界の背後にあるものを否定せず、直接所有される対象としては扱わない態度。 | 存在論的留保 | S2-S3 | E1-E2 | U0 | P1 | V0-V1 | 無神論・有神論・唯物論・観念論のいずれにも直結させない。 |
| 履歴場トポロジー | 履歴を持つ場どうしが境界で接触し、同期・非同期・意味形成・切断を起こす過程を読む概念フレーム。 | 存在論的再解釈 | S2-S3 | E1 | U0 | P0-P1 | V0-V1 | 統一理論ではなくFRAMEと明記する。物理位相へ接続する場合はS4-S5へ上げる。 |
| 履歴 | 単なる過去ではなく、次の受け取り方・反応・意味づけを変えるもの。 | 概念整理 | S2 | E0 | U0 | P0 | V0 | 公開可。 |
| 境界 | 外部入力と内部履歴が接触し、通過・保留・遮断・再符号化が起こる面。 | 概念整理 | S2-S3 | E1 | U0-U1 | P0 | V0-V1 | 防壁ではなく接触面として説明する。 |
| 意味ループ | 情報が循環し、返り、履歴として残ることで意味になる構造。 | 概念整理 | S2-S3 | E1 | U0 | P0 | V0-V1 | 公開可。 |
| 残差 | 観測、分類、照合、説明、決算によって閉じきれず、再照合可能な差分として残るもの。 | 概念整理 | S2-S3 | E1 | U0 | P0-P1 | V0-V1 | 残渣と分ける。 |
| 残渣 | 閉じきれなかった残差が、身体、環境、制度、関係、記号、無意識、未来世代などに沈殿し、見えにくいまま作用し続けるもの。 | 存在論的再解釈 | S2-S3 | E1-E2 | U0-U1 | P1 | V1 | 残差の単なる言い換えにしない。 |
| 無 | 単なる不存在ではなく、ある観測場・通信場から履歴接続が切断された状態。 | 存在論的再解釈 | S2-S3 | E1-E2 | U0 | P1 | V1 | 物理・情報・認識・倫理の層を混同しない。 |
| 同期 | 異なる履歴場が、一時的に共有可能な意味ループまたは運用対応を形成する状態。 | 概念整理 | S2-S3 | E1 | U0 | P0 | V0-V1 | 完全同一化ではないと明記する。 |
| 非同期 | 同じ入力が異なる履歴場で別の経路へ入り、摩擦や誤読を生む状態。 | 概念整理 | S2-S3 | E1 | U0-U1 | P0-P1 | V0-V1 | 社会・対話・AI応答へ広げる場合は注記する。 |

## 5. 補助線と切断

| 項目 | 公開文面 | 命題種別 | S | E | U | P | V | 処理 |
|---|---|---|---|---|---|---|---|---|
| 時空等価 | 時間と空間を、履歴が保存・配置・展開される異なる切断面として読む。 | 存在論的再解釈 | S2-S4 | E2 | U0 | P1-P2 | V1 | 物理理論の代替ではないと明記する。 |
| 境界膜クオリア | クオリアを、外部入力と内部履歴の境界摩擦、または閉じた履歴・主線・枝線の再浮上として生じる質感として読む。 | 存在論的再解釈 | S2-S4 | E2 | U0 | P1 | V1 | 心の哲学を置換しない。外部刺激起点に限定しない。 |
| エンタングル写像 | 観測後も、観測者と対象の接触履歴が完全には消えないと読む。 | 構造アナロジー / 存在論的再解釈 | S2-S4 | E2-E3 | U0 | P1-P2 | V1 | 量子エンタングルメントとの同一視を避ける。 |
| エントロピー通信 | 通信を、差異・ノイズ・未統合残差を閉じる、保留する、再符号化する、切断する過程として読む。 | 存在論的再解釈 | S2-S4 | E2 | U1 | P1 | V1-V2 | 実装手順ではなく概念説明に留める。 |
| 履歴切断としての無 | 無を、履歴接続が観測場・通信場から切断された状態として読む。 | 存在論的再解釈 | S2-S3 | E1-E2 | U0 | P1 | V1 | 単なる不存在と混同しない。 |


## 6. 科学語彙境界

| 項目 | 公開文面 | 命題種別 | S | E | U | P | V | 処理 |
|---|---|---|---|---|---|---|---|---|
| 標準借用 | 標準科学の定義を、その定義のまま使う。 | 用語整理 | S0-S1 | E0 | U0 | P0 | V0 | 公開可。 |
| 構造アナロジー | 似た構造を比喩的に使う。 | 構造アナロジー | S1-S2 | E1 | U0 | P0-P1 | V0 | 比喩であると明記する。 |
| 存在論的再解釈 | 標準概念を別の存在論的枠で読み直す。 | 存在論的再解釈 | S2-S3 | E2 | U0 | P1 | V1 | 標準定義を上書きしない。 |
| SO再定義 | 標準語を借りつつ、存在境界論内部で別定義を与える。 | 内部定義 | S3-S4 | E2-E3 | U0-U1 | P1-P2 | V1 | SO定義であると明記する。 |
| 物理接続候補 | 既存物理と比較可能な強い仮説候補。 | 物理接続候補 | S4-S5 | E3 | U0-U1 | P2 | V1-V5 | Research Notesに置き、証明ではないと明記する。 |
| 創作退避 | 理論ではなく、比喩・物語装置として使う。 | 創作比喩 | S1-S2 | E1 | U0 | P1 | V0 | 理論本文に混ぜない。 |


## 7. 物理・宇宙論接続候補

| 項目 | 公開文面 | 命題種別 | S | E | U | P | V | 処理 |
|---|---|---|---|---|---|---|---|---|
| intrinsic time / 内在時間 | 時計時間ではなく、通信履歴が論理的深度を持つ場合の深度秩序として読む。論理-深度軸と関係するが、内的計数時間とは同一ではない。 | SO再定義 / 物理接続候補 | S3-S5 | E2-E3 | U0-U1 | P2 | V1-V5 | `Internal Time` とは訳さない。ITSの略称でもない。 |
| 内的計数時間 | 外的時計時間ではなく、系内部で更新、保持、再接続、遅延が数えられる順序として扱う補助概念。 | SO再定義 / 形式化候補 | S3-S4 | E2 | U0-U1 | P1-P2 | V1-V4 | 内在時間と同一視しない。 |
| 論理-深度軸 | 外的時間の前後ではなく、未解決、矛盾、分岐、残差、残渣、意味圧を保持し再構成する深度方向。 | 概念フレーム / 形式化候補 | S3-S4 | E2 | U0-U1 | P1-P2 | V1-V4 | 単なる時間軸や心理的深さとして扱わない。 |
| time operator / 時間演算子 | ITS内部で、ボソン場を切断し局所現実を生成する演算子として扱う。 | 非公開中核由来 / 物理位相候補 | S4-S5 | E3 | U0-U1 | P2-P3 | V1-V5 | 公開では概念的説明に減圧する。 |
| particle as observed section / 粒子＝観測断面 | 粒子を、場が観測境界で安定した断面として現れるものとして読む。 | 存在論的再解釈 / 物理接続候補 | S3-S5 | E3 | U0 | P2 | V1-V5 | 標準QFTの代替ではないと明記する。 |
| PINGER仮説 | PINGERを実体粒子ではなく、発生位相と現在断面を結ぶ通信経路が観測断面で粒子的に見える状態として扱う仮説。 | 物理近接仮説 / 履歴場射影 | S4-S5 | E3 | U0-U1 | P2 | V1-V5 | Research Notes内に置き、標準物理学の粒子仮説として提出しない。 |
| PINGER粒子＝通信経路の観測断面 | PINGER粒子という語を、粒子実体ではなく、通信経路・頂点・返路・切断が観測位相で粒子的に見える状態として読む。 | SO再定義 / 物理近接語彙 | S4-S5 | E3 | U0-U1 | P2 | V1-V5 | `粒子`という語の標準物理定義と必ず分ける。 |
| boson as synchronization mediator / ボソン＝同期媒介 | ボソンを、相互作用履歴を媒介するものとして存在論的に読む。 | 物理接続候補 | S4-S5 | E3 | U0-U1 | P2 | V1-V5 | 標準物理定義と分ける。 |
| Feynman diagram as history topology / ファインマンダイアグラム＝履歴トポロジー | ファインマンダイアグラムを、相互作用履歴、交換、媒介、頂点、ループ、返路、切断の図式として構造的に読む。 | 構造アナロジー / 存在論的再解釈 | S2-S4 | E3 | U0 | P2 | V1 | 標準QFTの計算道具としての定義を尊重する。 |
| 履歴場トポロジーからファインマンダイアグラムへの縮退 | 履歴場トポロジーを時空座標、相互作用頂点、交換過程へ制限したとき、ファインマンダイアグラムに近い図式として読めるという整理。 | 物理近接対応候補 | S4-S5 | E3 | U0 | P2 | V1-V5 | 強い命題のため、証明ではなく対応候補として扱う。 |
| エンタングルメントへの制限写像 | 履歴場どうしの非分離的対応を、時空座標上の分離可能性へ制限したとき、量子的エンタングルメントに近い構造として読めるという整理。 | 物理近接対応候補 | S4-S5 | E3 | U0 | P2 | V1-V5 | 量子エンタングルメントと同一視しない。 |
| gravity as synchronization delay / 重力＝同期遅延 | 重力を、履歴密度と同期コストの観点から読む試論。 | 物理接続候補 | S4-S5 | E3 | U0-U1 | P2 | V1-V5 | Research Notes。物理証明ではないと明記する。 |
| 履歴重力圏 | 特定の履歴密度、意味圧、未閉鎖残差が、以後の解釈・反応・接続を強く拘束する領域として読む。 | 構造アナロジー / 形式化候補 | S3-S4 | E2-E3 | U0-U1 | P1-P2 | V1-V4 | 物理的重力と同一視しない。 |
| dark energy as unclosed meaning pressure / ダークエネルギー＝未閉鎖意味圧 | 宇宙論的語彙を、未閉鎖の意味圧という構造アナロジーで読む試論。 | 構造アナロジー / 物理接続候補 | S3-S5 | E3 | U0 | P2 | V1 | 物理主張ではなくResearch Notes扱い。 |
| BlackHole＝切断事象の集積 | BlackHoleを、内部を持つ場所というより、履歴接続の切断事象が集積し、残差熱と表面返還が現れる境界事象として読む。 | 物理近接対応候補 / 存在論的再解釈 | S4-S5 | E3 | U0 | P2 | V1-V5 | 物理ブラックホールの標準理論を置換しない。概念射影として扱う。 |
| カオス理論との照合 | カオス理論を時系列的非線形決定論として尊重しつつ、予測不能に見える差分が履歴差分・残差保持・論理-深度軸へ移行する条件を読む。 | 構造アナロジー / 対応候補 | S3-S4 | E2 | U0 | P1-P2 | V1-V4 | 数理カオス理論の置換ではない。 |
| CPT reinterpretation / CPT再解釈 | C/P/Tを、履歴・位置・時間方向の反転写像として読む試論。 | 物理接続候補 | S3-S5 | E3 | U0-U1 | P2 | V1-V5 | 標準CPT定理との関係を明記する。 |

## 8. 認識・クオリア・意味生成

| 項目 | 公開文面 | 命題種別 | S | E | U | P | V | 処理 |
|---|---|---|---|---|---|---|---|---|
| 観測＝履歴との出会い | 観測とは、対象を見るだけではなく、対象の履歴と観測者の履歴が接触することである。 | 存在論的再解釈 | S2-S3 | E1 | U0 | P0-P1 | V0-V1 | 物理観測と認知観測を分ける。 |
| クオリア＝境界出来事 | クオリアとは、外部入力と内部履歴の境界摩擦、または閉じた内部履歴・主線・枝線が共鳴や接触によって境界へ再浮上するときに生じる質感である。 | 存在論的再解釈 | S2-S4 | E2 | U0 | P1 | V1 | 心の哲学を置換しない。純粋な内面物に限定しない。 |
| Quale / 単一クオリア | 単一の未閉鎖通信、または単一の閉じた意味ループの再励起に対応する質感単位。 | 概念整理 | S2-S3 | E1 | U0 | P1 | V0-V1 | Qualiaと分ける場合のみ使う。 |
| Qualia / クオリア束 | 複数の quale が重なり、干渉し、内部で読解可能な経験場として束ねられたもの。 | 概念整理 | S2-S3 | E1 | U0 | P1 | V0-V1 | 単数・複数の混線に注意する。 |
| 意味生成 | 意味を、情報が履歴と接続し循環することで生じるものとして読む。 | 概念整理 | S2-S3 | E1 | U0 | P0 | V0-V1 | 公開可。 |
| アポリア | 矛盾ではなく、異なる履歴位相や境界条件を同一平面で処理したときの接続不全として読む。 | 存在論的再解釈 | S2-S4 | E1-E2 | U0 | P1 | V1 | 代表例で説明する。 |
| 説明＝履歴場へのエンコード | 説明を、情報の丸ごとの転送ではなく、受け手の履歴場へ再符号化する操作として読む。 | 概念整理 / 存在論的再解釈 | S2-S4 | E1 | U1 | P1 | V1-V2 | 操作手順ではなく概念説明に留める。 |
| ビットとセンテンス | ビット列として符号化できることと、意味として評価できることを分ける。 | 公開研究候補 | S2-S4 | E1 | U0-U1 | P0-P1 | V2-V3 | 論文候補として公開可。 |


## 9. AI境界概念

| 項目 | 公開文面 | 命題種別 | S | E | U | P | V | 処理 |
|---|---|---|---|---|---|---|---|---|
| AI有用性＝判断可能性保持 | AIは答えを代行するだけでなく、ユーザーが判断できる場を保つときに有用である。 | 公開概念 | S2-S3 | E1 | U0 | P0 | V1-V2 | 04_Applicationsで扱う。 |
| 境界倫理 | 倫理を、履歴を持つ存在どうしが互いの履歴を破壊せずに関わるための境界設計として読む。 | 公開概念 | S2-S3 | E1 | U0 | P0 | V1 | 03_Tam_Goodnessで扱う。 |
| 履歴非破壊応答 | 相手の文脈・未解決・主体性を壊さずに応答する方針。 | 公開概念 | S2-S3 | E1 | U0-U1 | P0-P1 | V1-V2 | 公開可。 |
| 保留能力 | 不確実なものを勝手に閉じず、未解決として保持する力。 | 公開概念 | S2-S3 | E1 | U0-U1 | P0-P1 | V1-V2 | 公開可。 |
| 境界支援機能 | オンライン上の意味・履歴・文脈を壊さないための境界支援概念。 | 実装隣接概念 | S3-S4 | E1 | U2 | P2.5 | V2 | 概念説明のみ。実装仕様は非公開。 |
| 非公開安全カテゴリ | 公開できない安全評価・境界管理系の総称。 | 非公開カテゴリ | S3-S4 | E1 | U3-U4 | P3 | V3-V4 | 分類以上を書かない。 |


## 10. 社会・生命・安全文化

| 項目 | 公開文面 | 命題種別 | S | E | U | P | V | 処理 |
|---|---|---|---|---|---|---|---|---|
| 社会相 | 社会が採用している主な履歴経路や規範の束として社会を見る。 | 存在論的再解釈 | S2-S3 | E1 | U0 | P0-P1 | V1 | 公開可。 |
| 社会的乱流 | 共通の主経路が崩れ、履歴同期圏が非同期に走る状態として社会不安を見る。 | 構造アナロジー | S2-S3 | E1 | U1 | P1 | V1 | 具体事例では注記する。 |
| 制度的無 | 記録されない労働・苦痛・被害・存在を、制度による履歴切断として読む。 | 存在論的再解釈 | S2-S3 | E1 | U0-U1 | P0-P1 | V1 | 公開可。 |
| 信用＝履歴同期 | 信用を、約束文言ではなく、責任履歴と予測可能性が噛み合う状態として読む。 | 存在論的再解釈 | S2-S3 | E1 | U0 | P0 | V1 | 公開可。 |
| 高リスクシステム＝履歴非同期リスク | 高リスクシステムでは、関係者間の履歴差が判断不全を生むことがある。 | 安全文化への概念応用 | S3-S4 | E2 | U2 | P2.5 | V2 | 具体領域への適用は別管理。 |
| 生命＝境界通信系 | 生命を、境界を持って選択的に交換・更新する履歴系として読む。 | 存在論的再解釈 | S2-S4 | E2 | U0 | P1 | V1 | 既存生命理論との同一視を避ける。 |
| 非対称性の仮安定化 | 非対称性が、重力、物質、生命、文明、文化などの階層で一時的に固定され、後に再照合される過程として読む。 | 横断領域モデル | S2-S3 | E2 | U0 | P1-P2 | V1 | 各専門領域の標準理論を置換しない。 |
| 文化＝長期履歴保存系 | 文化を、履歴を壊さず運ぶ長期保存媒体として読む。 | 存在論的再解釈 | S2-S3 | E1 | U0 | P0 | V1 | 公開可。 |
| 文化＝再照合機構 | 文化を、文明の保存機構ではなく、自然・身体・生活・意味へ戻して再照合する機構として読む。 | 横断領域モデル | S2-S3 | E1-E2 | U0 | P1 | V1 | 文化本質論として固定しない。 |
| 返りの倫理 | 境界接触の後に生じる返り、残差、補償要求、責任処理を、倫理の基本単位として扱う。 | 境界倫理モデル | S2-S3 | E1-E2 | U1 | P1-P2 | V1-V2 | 法理論や処罰理論の代替ではない。 |
| 報復変換 | 報復を単純に肯定・否定するのではなく、残差処理、責任回路、修復、制度的返還へ変換する構造として読む。 | 境界倫理 / 社会モデル | S2-S3 | E2 | U1-U2 | P2 | V1-V2 | 実務的制裁手順として公開しない。 |
| ネゲントロピー経済 | 意味、秩序、価値、責任、履歴を回収・保存・再編成する働きとして経済を読む。 | 社会境界概念モデル | S2-S3 | E1-E2 | U1 | P1-P2 | V1-V3 | 経済学、政策、代替通貨制度として提出しない。 |

## 11. 文学・創作・比喩退避

| 項目 | 公開文面 | 命題種別 | S | E | U | P | V | 処理 |
|---|---|---|---|---|---|---|---|---|
| 天体構造と精神構造の写像 | 天体構造を精神構造の比喩として読む。 | 創作比喩 | S1-S2 | E1 | U0 | P1 | V0 | 診断・科学主張にはしない。 |
| 重元素＝履歴の重さ | 重元素の生成履歴を、経験や文化の重さの比喩として読む。 | 創作比喩 | S1-S2 | E1 | U0 | P1 | V0 | 理論本文では比喩と明記する。 |
| ブラックホール・レンズ | 高密度の理想や履歴が日常へ投影される負荷の比喩。 | 創作比喩 | S1-S2 | E1 | U0-U1 | P1 | V0 | 崩壊美化を避ける。 |
| 神・悪魔・獣モデル | 応答様式や制度の働きを寓話的に読むモデル。 | 創作比喩 / 倫理寓話 | S1-S2 | E1 | U0-U1 | P1 | V0 | 現実個人へ直接対応づけない。 |
| 文学的存在論読解 | 文学・詩・宗教的語彙を、存在境界論の概念で読む非科学研究。 | 非科学研究 | S1-S2 | E1 | U0 | P1 | V0-V1 | 証明ではなく構造読解と明記する。 |
| 物語的真実層 | 物語を現実逃避ではなく、事実命題だけでは届きにくい真実層へ触れる構造読解装置として扱う。 | 文学存在論 / 構造読解 | S1-S3 | E1-E2 | U0 | P1 | V0-V1 | 史実証明・科学証明にしない。 |
| 冥府局転生課モデル | 転生、審査、配属、信念、責任、未処理履歴を扱う創作世界を、履歴再配置と境界倫理の寓話として読む。 | 創作比喩 / 文学存在論 | S1-S2 | E1-E2 | U0-U1 | P1 | V0-V1 | 宗教教義、死後世界の実在主張、制度モデルとして出さない。 |
| 信念重力圏 | 信念、祈り、物語、役割が履歴を引き寄せ、人物や世界の解釈経路を拘束する領域として読む。 | 創作比喩 / 概念モデル | S1-S3 | E1-E2 | U0-U1 | P1 | V0-V1 | 物理的重力や宗教的実在と同一視しない。 |
| 転生ループ＝履歴再配置 | 転生を、魂の証明ではなく、未処理履歴、役割、責任、信念経路が別配置で再演算される物語構造として読む。 | 創作比喩 / 構造読解 | S1-S2 | E1-E2 | U0 | P1 | V0-V1 | 宗教的輪廻説の主張ではない。 |

## 12. 現段階の総合判定

本表は、履歴場トポロジー専用ではなく、存在境界論全体の主張強度、公開レイヤー、誤読リスク、応用リスク、検証段階を管理するための公開制御表である。

存在境界論は、外部には統一理論、標準科学の代替、宗教体系、創作設定の実在主張として出さない。

公開版では、境界、接触、履歴、返り、後続条件、同期、非同期、意味形成、残差、残渣、切断を扱う概念フレームとして提示する。

Research Notes では、物理・宇宙論・文学・AI境界機能・社会境界・価値論・冥府局的創作読解への強い接続を扱ってよい。ただし、強い命題は必ず S/E/U/P/V で分類する。

物理近接概念は、標準科学の定義を尊重しつつ、存在境界論からの対応候補・射影・構造アナロジーとして扱う。PINGER仮説、BlackHole、エンタングルメント、ファインマンダイアグラム、カオス理論、履歴重力圏などは、公開時に特に E3 減速を必要とする。

冥府局、転生、信念重力圏などの創作・文学的語彙は、宗教主張や死後世界の実在証明ではなく、履歴、責任、信念、返り、再配置を読むための文学的存在論ノートとして扱う。

公開可否は、主張強度 S だけで決めない。E が高いものは、注記・限定条件・非主張事項によって減速する。U が高いものは、抽象化または非公開にする。

## English commensurated rendering

## 0.1 Evaluation Order

This table does not treat S / E / U / P / V as parallel labels.

The S code indicates the claim strength of the proposition itself.  
The E code indicates how easily the proposition may be misread or criticized.  
The U code indicates how the proposition may be applied, overextended, or repurposed.  
The P code is the final publication layer after S, E, and U have been considered.  
The V code does not decide publication. It manages the next stage of verification or formalization.

Publication handling is therefore decided in the following order.

```text
1. Evaluate the proposition's claim strength by S code.
2. Assign a provisional publication layer P_base from the S code.
3. Decelerate by E code when misreading or critical pressure is high.
4. Decelerate, abstract, or withhold by U code when application or safety risk is high.
5. Decide the final publication layer P_final.
6. Manage verification and formalization separately by V code.
```

## 1. Claim Strength Codes

| Code | Name | Meaning | Public handling |
|---|---|---|---|
| S0 | Terminological arrangement | A convenient term within the system; no strong external claim. | Public |
| S1 | Structural analogy | A comparison based on structural similarity to an existing concept. | Public as analogy |
| S2 | Ontological reinterpretation | Re-reading an existing concept through another ontological frame. | Public with notes |
| S3 | Working hypothesis | A hypothesis used in internal research; not sufficiently verified. | Public only as hypothesis |
| S4 | Formalization candidate | Candidate for state variables, operation rules, or evaluation indicators. | Research Notes |
| S5 | Physical-claim candidate | A strong claim that may directly contact existing science. | Internal review first; public handling requires caution |

---


## 2. Publication, Misreading, and Application Risk Codes

Publication handling is not decided by claim strength alone. A high-S claim with low application risk may be published as a Research Note, while a medium-S claim with high application risk may need abstraction or non-public handling.

#### P codes: publication layer

| Code | Name | Meaning | Publication decision |
|---|---|---|---|
| P0 | Public-ready | Safe for public release as conceptual explanation, terminology arrangement, or public entry point. | Public |
| P1 | Slowed public release | Contains some risk of misreading, but can be published with notes, limiting conditions, and a non-proof declaration. | Public |
| P2 | Research Note publication | Claim strength is high, but application risk is low. Can be published as proposal, correspondence table, or exploratory note. | Research Notes |
| P2.5 | Abstracted publication | The core is useful, but detailed procedures are risky. Publish the concept while withholding operational rules. | Requires distillation |
| P3 | Non-public | Contains information that should not be disclosed beyond classification. | Do not publish |

#### E codes: epistemic and critical risk

| Code | Name | Meaning | Handling |
|---|---|---|---|
| E0 | Low risk | Unlikely to be misread. | Normal publication |
| E1 | Insufficient-explanation risk | May be misunderstood because terms are underexplained. | Add definitions |
| E2 | Critical-pressure risk | Likely to receive strong criticism from specialist domains or readers. | State claim scope and non-claims |
| E3 | Pseudo-scientific misreading risk | Likely to be misread as scientific claim, religious claim, or literary proof. | Move to Research Notes and state that it is not proof |

#### U codes: application and safety risk

| Code | Name | Meaning | Publication decision |
|---|---|---|---|
| U0 | Low risk | Gives almost no direct operational, intervention, or avoidance capability. | Public |
| U1 | Misuse risk | May invite careless quotation, overgeneralization, or factualization of metaphor. | Publish with notes |
| U2 | Transfer risk | May be repurposed in ways that destabilize others' judgment, relationships, or institutions. | Publish only in abstracted form |
| U3 | Operational risk | Detailed publication would reduce the integrity of non-public boundaries. | Non-public by default |
| U4 | Must remain concealed | Do not publish beyond classification. | Publication prohibited |


High E should be slowed down with definitions, non-claim boundaries, and disclaimers. High U should be abstracted or kept non-public.

## 2.1 Base Public Layer from S-code

| S code | Provisional P | Reason |
|---|---|---|
| S0 | P0 | Terminological arrangement; no strong external claim. |
| S1 | P0-P1 | Public as structural analogy, with caution against factualizing the metaphor. |
| S2 | P1 | Ontological reinterpretation; requires notes and limiting conditions. |
| S3 | P1-P2 | Working hypothesis; must be presented as hypothesis or exploratory proposal. |
| S4 | P2 | Formalization candidate; suitable for Research Notes. |
| S5 | P2-P3 | Direct contact with existing science; requires internal review or strong deceleration. |

## 2.2 Deceleration by E/U Codes

E and U codes decelerate, abstract, or withhold the provisional publication layer derived from S.

### Adjustment by E code

| E code | Adjustment |
|---|---|
| E0 | Keep P_base. |
| E1 | Add definitions, notes, and non-claim boundaries. Usually keep P. |
| E2 | Decelerate at least to P1 and state claim scope and non-claims. |
| E3 | Retreat at least to P2 and avoid pseudo-scientific, religious, or literary-proof misreading. Depending on the case, move to P2.5 or P3. |

### Adjustment by U code

| U code | Adjustment |
|---|---|
| U0 | Keep P_base. |
| U1 | Publish with notes. Usually use P1 or higher. |
| U2 | Publish only in abstracted form. P2.5 should normally be considered. |
| U3 | Do not publish details. Default to P3, or publish only a distilled concept at P2.5. |
| U4 | Do not publish. Fix at P3. |

## 2.3 Public Layer Decision

The final publication layer is decided as follows.

P_final = decelerate(P_base(S), E, U)

---


## 3. Verification and Formalization Codes

| Code | Name | Meaning |
|---|---|---|
| V0 | Conceptual coherence | Checks internal coherence of terms and definitions. |
| V1 | Correspondence table | Maps relations to existing science, information theory, cognitive science, or social theory. |
| V2 | Toy Model | Tests minimal behavior in a small model. |
| V3 | Evaluation experiment | Evaluates AI responses, dialogue logs, or creative structures. |
| V4 | Mathematical or simulation model | Introduces variables, update rules, or state transitions. |
| V5 | Physical prediction | Connects to predictions or calculations comparable with existing physics. |

---


## 4. Public Conceptual Core

| Item | Public wording | Claim type | S | E | U | P | V | Handling |
|---|---|---|---|---|---|---|---|---|
| Scientific Ontology | A public conceptual framework that does not claim direct possession of existence itself, but treats boundaries, contacts, histories, returns, and subsequent conditions as describable reality. | Public framework / conceptual frame | S2-S3 | E1 | U0 | P0-P1 | V0-V1 | Do not present as a unified theory, religion, or replacement for empirical science. |
| Boundary Realism Principle | The principle that the system treats boundaries, contacts, histories, returns, and subsequent conditions as real targets of description, rather than claiming possession of existence itself. | Foundational principle | S2-S3 | E1 | U0 | P0-P1 | V0-V1 | Treat as a foundational principle in `01_Sat_Truth`. |
| Ontological reserve | A stance that does not deny what lies behind boundaries, but does not treat it as an object directly possessed by the system. | Ontological reserve | S2-S3 | E1-E2 | U0 | P1 | V0-V1 | Do not attach directly to atheism, theism, materialism, or idealism. |
| History-Field Topology | A conceptual frame for reading how history-bearing fields contact through boundaries, synchronize or desynchronize, form meaning, or become cut off. | Ontological reinterpretation | S2-S3 | E1 | U0 | P0-P1 | V0-V1 | State that it is a frame, not a unified theory. Raise to S4-S5 when connecting to physical phase. |
| History | Not merely the past, but what changes the next reception, reaction, and meaning-making. | Conceptual clarification | S2 | E0 | U0 | P0 | V0 | Public. |
| Boundary | A contact surface where external input and internal history meet, pass, remain held, become blocked, or are re-encoded. | Conceptual clarification | S2-S3 | E1 | U0-U1 | P0 | V0-V1 | Explain as contact surface, not only defense. |
| Meaning Loop | A structure in which information circulates, returns, and remains as history, thereby becoming meaning. | Conceptual clarification | S2-S3 | E1 | U0 | P0 | V0-V1 | Public. |
| Residual | A re-collatable difference left after observation, classification, collation, explanation, accounting, or institutional handling fails to close fully. | Conceptual clarification | S2-S3 | E1 | U0 | P0-P1 | V0-V1 | Distinguish from residue. |
| Residue | A residual that has sedimented into bodies, environments, institutions, relations, signs, unconscious processes, or future generations and continues to act while remaining hard to see. | Ontological reinterpretation | S2-S3 | E1-E2 | U0-U1 | P1 | V1 | Do not use as a mere synonym for residual. |
| Void | Not simple nonexistence, but the state in which historical connection is cut off from a field of observation or communication. | Ontological reinterpretation | S2-S3 | E1-E2 | U0 | P1 | V1 | Keep physical, informational, cognitive, and ethical layers distinct. |
| Synchronization | A state in which different history-fields temporarily form a shareable meaning loop or operational correspondence. | Conceptual clarification | S2-S3 | E1 | U0 | P0 | V0-V1 | Not total identity. |
| Desynchronization | A state in which the same input enters different paths across history-fields and produces friction or misreading. | Conceptual clarification | S2-S3 | E1 | U0-U1 | P0-P1 | V0-V1 | Add notes when extending to society, dialogue, or AI response. |

## 5. Guiding Lines and Cutoff

| Item | Public wording | Claim type | S | E | U | P | V | Handling |
|---|---|---|---|---|---|---|---|---|
| Spacetime Equivalence | Read time and space as different sections through which history is preserved, arranged, and unfolded. | Ontological reinterpretation | S2-S4 | E2 | U0 | P1-P2 | V1 | State that this is not a replacement for physical theory. |
| Boundary-Membrane Qualia | Read qualia as felt textures arising from boundary friction between external input and internal history, or from the resurfacing of closed histories, main lines, or branch lines. | Ontological reinterpretation | S2-S4 | E2 | U0 | P1 | V1 | Does not replace philosophy of mind; not limited to external stimulus. |
| Entangled Mapping | Read contact history between observer and object as not fully disappearing after observation. | Structural analogy / ontological reinterpretation | S2-S4 | E2-E3 | U0 | P1-P2 | V1 | Avoid identity with quantum entanglement. |
| Entropy Communication | Read communication as the process of closing, holding, re-encoding, or cutting off differences, noise, and unresolved residuals. | Ontological reinterpretation | S2-S4 | E2 | U1 | P1 | V1-V2 | Keep as conceptual description, not implementation procedure. |
| Void as Historical Cutoff | Read the void as a state in which historical connection is cut off from an observation or communication field. | Ontological reinterpretation | S2-S3 | E1-E2 | U0 | P1 | V1 | Do not confuse with simple nonexistence. |

---


## 6. Scientific Terminology Boundary

| Item | Public wording | Claim type | S | E | U | P | V | Handling |
|---|---|---|---|---|---|---|---|---|
| Standard borrowing | Use a standard scientific term with its standard definition. | Terminological arrangement | S0-S1 | E0 | U0 | P0 | V0 | Public. |
| Structural analogy | Use a similar structure metaphorically or comparatively. | Structural analogy | S1-S2 | E1 | U0 | P0-P1 | V0 | State that it is analogy. |
| Ontological reinterpretation | Re-read a standard concept through another ontological frame. | Ontological reinterpretation | S2-S3 | E2 | U0 | P1 | V1 | Do not overwrite the standard definition. |
| SO redefinition | Borrow a standard term while assigning a distinct definition within Scientific Ontology. | Internal definition | S3-S4 | E2-E3 | U0-U1 | P1-P2 | V1 | Mark as SO definition. |
| Physical correspondence candidate | A strong hypothesis candidate that may be compared with existing physics. | Physical correspondence candidate | S4-S5 | E3 | U0-U1 | P2 | V1-V5 | Place in Research Notes; state that it is not proof. |
| Creative retreat | Use as metaphor or narrative device, not as theory. | Creative metaphor | S1-S2 | E1 | U0 | P1 | V0 | Do not mix into theoretical body as proof. |

---


## 7. Physical and Cosmological Correspondence Candidates

The Japanese table above is authoritative. The following table preserves its public structure for English commensuration.

| Item | Public wording | Claim type | S | E | U | P | V | Handling |
|---|---|---|---|---|---|---|---|---|
| intrinsic time | Not clock time, but a depth-order in which communication history may acquire logical depth. It is related to the logical-depth axis, but is not identical with internal count-time. | SO redefinition / physical correspondence candidate | S3-S5 | E2-E3 | U0-U1 | P2 | V1-V5 | Do not translate as `Internal Time`. It is not the abbreviation ITS. |
| internal count-time | An auxiliary concept for the order in which updates, retention, reconnection, and delay are counted inside a system, rather than by external clock time. | SO redefinition / formalization candidate | S3-S4 | E2 | U0-U1 | P1-P2 | V1-V4 | Do not identify with intrinsic time. |
| logical-depth axis | A depth direction, not external before-and-after time, in which unresolved issues, contradictions, branches, residuals, residues, and semantic pressure are held and reconstructed. | Conceptual frame / formalization candidate | S3-S4 | E2 | U0-U1 | P1-P2 | V1-V4 | Do not reduce to a simple time axis or psychological depth. |
| time operator | Within ITS, treated as an operator that cuts through the bosonic field and generates local reality. | Derived from non-public core / physical-phase candidate | S4-S5 | E3 | U0-U1 | P2-P3 | V1-V5 | Reduce to conceptual explanation in public materials. |
| particle as observed section | Read a particle as the appearance of a field as a stable section at an observational boundary. | Ontological reinterpretation / physical correspondence candidate | S3-S5 | E3 | U0 | P2 | V1-V5 | State that this is not a replacement for standard QFT. |
| PINGER hypothesis | Treat PINGER not as an entity-particle, but as a state in which a communication route connecting a generative phase and a present section appears particle-like at an observational section. | Physics-proximate hypothesis / history-field projection | S4-S5 | E3 | U0-U1 | P2 | V1-V5 | Keep in Research Notes; do not present as a standard particle-physics hypothesis. |
| PINGER particle as observed section of a communication route | Read `PINGER particle` not as a particle entity, but as a particle-like appearance of routes, vertices, returns, and cutoffs in an observational phase. | SO redefinition / physics-proximate vocabulary | S4-S5 | E3 | U0-U1 | P2 | V1-V5 | Always distinguish from the standard physical definition of particle. |
| boson as synchronization mediator | Read a boson ontologically as something that mediates interaction history. | Physical correspondence candidate | S4-S5 | E3 | U0-U1 | P2 | V1-V5 | Distinguish from the standard physical definition. |
| Feynman diagram as history topology | Read Feynman diagrams structurally as diagrams of interaction history, exchange, mediation, vertices, loops, returns, and cutoffs. | Structural analogy / ontological reinterpretation | S2-S4 | E3 | U0 | P2 | V1 | Respect their standard definition as computational tools in QFT. |
| reduction from History-Field Topology to Feynman diagrams | A strong correspondence proposal: when History-Field Topology is constrained to spacetime coordinates, interaction vertices, and exchange processes, it may be read as approaching a Feynman-diagram-like form. | Physics-proximate correspondence candidate | S4-S5 | E3 | U0 | P2 | V1-V5 | Treat as a correspondence candidate, not proof. |
| restricted mapping to entanglement | A strong correspondence proposal: when non-separable relations among history-fields are constrained by separability in spacetime coordinates, they may be read as approaching quantum-entanglement-like structure. | Physics-proximate correspondence candidate | S4-S5 | E3 | U0 | P2 | V1-V5 | Do not identify with quantum entanglement. |
| gravity as synchronization delay | An exploratory reading of gravity in terms of history density and synchronization cost. | Physical correspondence candidate | S4-S5 | E3 | U0-U1 | P2 | V1-V5 | Research Notes only. State that it is not physical proof. |
| history-gravity domain | A domain in which history density, semantic pressure, or unclosed residuals strongly constrain later interpretation, reaction, or connection. | Structural analogy / formalization candidate | S3-S4 | E2-E3 | U0-U1 | P1-P2 | V1-V4 | Do not identify with physical gravity. |
| dark energy as unclosed meaning pressure | An exploratory reading of cosmological vocabulary through the structural analogy of unclosed semantic pressure. | Structural analogy / physical correspondence candidate | S3-S5 | E3 | U0 | P2 | V1 | Treat as Research Notes, not as a physical claim. |
| BlackHole as accumulation of cutoff events | Read BlackHole not primarily as a place with an interior, but as a boundary event where historical-connection cutoffs accumulate and where residual heat and surface return appear. | Physics-proximate correspondence candidate / ontological reinterpretation | S4-S5 | E3 | U0 | P2 | V1-V5 | Do not replace standard black-hole physics. Treat as conceptual projection. |
| correspondence with chaos theory | Respect chaos theory as chronological nonlinear determinism while reading how apparently unpredictable differences may shift into historical difference, residual retention, and the logical-depth axis. | Structural analogy / correspondence candidate | S3-S4 | E2 | U0 | P1-P2 | V1-V4 | Not a replacement for mathematical chaos theory. |
| CPT reinterpretation | An exploratory reading of C/P/T as reversal mappings of history, position, and temporal direction. | Physical correspondence candidate | S3-S5 | E3 | U0-U1 | P2 | V1-V5 | State its relation to the standard CPT theorem. |

Key public handling rules:

- `内在時間` is rendered as `intrinsic time`, not `Internal Time`.
- ITS means `Information-Time Soliton Unified Theory`; it is not an abbreviation of intrinsic time.
- ITS-derived terms such as `time operator` should be reduced before public use.
- Physics-proximate concepts such as PINGER, BlackHole, entanglement, Feynman diagrams, chaos theory, and history-gravity domain require E3 deceleration when they may be read as standard scientific claims.
- Physical and cosmological correspondences belong in Research Notes and must not be presented as replacements for established physics.
---

## 8. Cognition, Qualia, and Meaning Generation

| Item | Public wording | Claim type | S | E | U | P | V | Handling |
|---|---|---|---|---|---|---|---|---|
| Observation as history encounter | Observation is not merely seeing an object; it is contact between the object's history and the observer's history. | Ontological reinterpretation | S2-S3 | E1 | U0 | P0-P1 | V0-V1 | Distinguish physical observation from cognitive observation. |
| Qualia as boundary event | Qualia are felt textures arising from boundary friction between external input and internal history, or from the resurfacing of closed internal histories, main lines, or branch lines through resonance or contact. | Ontological reinterpretation | S2-S4 | E2 | U0 | P1 | V1 | Does not replace philosophy of mind; not a purely private inner object. |
| Quale | A single felt unit corresponding to one unclosed communication or the re-excitation of one closed meaning loop. | Conceptual clarification | S2-S3 | E1 | U0 | P1 | V0-V1 | Use only when distinguishing from qualia. |
| Qualia bundle | Multiple quales overlapping, interfering, and becoming readable as an experience field. | Conceptual clarification | S2-S3 | E1 | U0 | P1 | V0-V1 | Avoid singular/plural confusion. |
| Meaning Generation | Meaning arises when information connects with history and circulates. | Conceptual clarification | S2-S3 | E1 | U0 | P0 | V0-V1 | Public. |
| Aporia | A connection failure produced when different historical phases or boundary conditions are processed on the same plane. | Ontological reinterpretation | S2-S4 | E1-E2 | U0 | P1 | V1 | Explain through examples. |
| Explanation as encoding into a history-field | Explanation is not complete transfer of information, but re-encoding into the recipient's history-field. | Conceptual clarification / ontological reinterpretation | S2-S4 | E1 | U1 | P1 | V1-V2 | Keep conceptual, not procedural. |
| Bits vs Sentences | Distinguish being encodable as bits from being evaluable as meaning. | Public research candidate | S2-S4 | E1 | U0-U1 | P0-P1 | V2-V3 | Suitable as a paper candidate. |

---


## 9. AI Boundary Concepts

AI-related concepts belong mainly in `04_Applications` unless they become high-claim or speculative enough to require Research Notes. The following table preserves the Japanese public-management structure for English commensuration.

| Item | Public wording | Claim type | S | E | U | P | V | Handling |
|---|---|---|---|---|---|---|---|---|
| AI usefulness as preservation of judgment possibility | AI is useful not merely when it substitutes answers, but when it preserves the user's capacity to judge. | Public concept | S2-S3 | E1 | U0 | P0 | V1-V2 | Treat in `04_Applications`. |
| Boundary Ethics | Read ethics as boundary design for history-bearing beings to engage without destroying one another's histories. | Public concept | S2-S3 | E1 | U0 | P0 | V1 | Treat in `03_Tam_Goodness`. |
| History-nondestructive response | A response policy that does not destroy the other party's context, unresolved issues, or agency. | Public concept | S2-S3 | E1 | U0-U1 | P0-P1 | V1-V2 | Public. |
| Capacity to hold unresolvedness | The ability to hold uncertainty without closing it arbitrarily as solved. | Public concept | S2-S3 | E1 | U0-U1 | P0-P1 | V1-V2 | Public. |
| Boundary-support function | A boundary-support concept for avoiding destruction of meaning, history, and context online. | Implementation-adjacent concept | S3-S4 | E1 | U2 | P2.5 | V2 | Conceptual explanation only. Implementation specifications remain non-public. |
| Non-public safety categories | A general class for safety evaluation and boundary-management categories that cannot be publicly disclosed. | Non-public category | S3-S4 | E1 | U3-U4 | P3 | V3-V4 | Do not disclose beyond classification. |

Public AI materials should preserve judgment possibility and boundary integrity, while implementation procedures and private safety categories remain outside the public layer.
---


## 10. Society, Life, and Safety Culture

Social, life, and safety-culture concepts may be public when they remain conceptual and do not expose operational procedures. The following table preserves the Japanese public-management structure for English commensuration.

| Item | Public wording | Claim type | S | E | U | P | V | Handling |
|---|---|---|---|---|---|---|---|---|
| Social phase | View society as a bundle of dominant historical paths and norms. | Ontological reinterpretation | S2-S3 | E1 | U0 | P0-P1 | V1 | Public. |
| Social turbulence | Read social instability as a state in which shared main paths break down and history-synchronization zones run asynchronously. | Structural analogy | S2-S3 | E1 | U1 | P1 | V1 | Add notes when using concrete cases. |
| Institutional void | Read unrecorded labor, suffering, harm, or existence as historical cutoff by institutions. | Ontological reinterpretation | S2-S3 | E1 | U0-U1 | P0-P1 | V1 | Public. |
| Trust as history synchronization | Read trust not as promise wording, but as a state in which responsibility history and predictability fit together. | Ontological reinterpretation | S2-S3 | E1 | U0 | P0 | V1 | Public. |
| High-risk systems as history-desynchronization risk | In high-risk systems, differences in history among participants may produce failures of judgment. | Conceptual application to safety culture | S3-S4 | E2 | U2 | P2.5 | V2 | Applications to concrete domains require separate management. |
| Life as boundary-communication system | Read life as a history-bearing system that selectively exchanges and updates through boundaries. | Ontological reinterpretation | S2-S4 | E2 | U0 | P1 | V1 | Avoid identifying it with existing theories of life. |
| provisional stabilization of asymmetry | Read asymmetry as temporarily stabilized across layers such as gravity, matter, life, civilization, and culture, and later subjected to re-collation. | Cross-domain model | S2-S3 | E2 | U0 | P1-P2 | V1 | Does not replace the standard theories of each specialized domain. |
| Culture as long-term history-preservation system | Read culture as a long-term preservation medium that carries history without destroying it. | Ontological reinterpretation | S2-S3 | E1 | U0 | P0 | V1 | Public. |
| Culture as re-collation mechanism | Read culture not only as a preservation mechanism of civilization, but as a mechanism that returns history to nature, body, life, and meaning for re-collation. | Cross-domain model | S2-S3 | E1-E2 | U0 | P1 | V1 | Do not fix as an essentialist theory of culture. |
| Return Ethics | Treat returns, residuals, compensatory demands, and responsibility processing after boundary contact as basic units of ethics. | Boundary-ethics model | S2-S3 | E1-E2 | U1 | P1-P2 | V1-V2 | Not a replacement for legal theory or theory of punishment. |
| Retaliation Conversion | Read retaliation not as something simply affirmed or denied, but as a structure to be converted into residual processing, responsibility circuits, repair, and institutional return. | Boundary ethics / social model | S2-S3 | E2 | U1-U2 | P2 | V1-V2 | Do not publish as practical sanction procedure. |
| Negentropy Economy | Read economy as the recovery, preservation, and reorganization of meaning, order, value, responsibility, and history. | Social-boundary conceptual model | S2-S3 | E1-E2 | U1 | P1-P2 | V1-V3 | Not empirical economics, policy proposal, or replacement currency system. |

Concrete applications to high-risk systems require additional abstraction or non-public handling.
---

## 11. Literature, Creation, and Metaphorical Retreat

Literary and creative materials may be used as structural readings or metaphorical retreats. The following table preserves the Japanese public-management structure for English commensuration.

| Item | Public wording | Claim type | S | E | U | P | V | Handling |
|---|---|---|---|---|---|---|---|---|
| Mapping celestial structure to mental structure | Read celestial structures as metaphors for mental structures. | Creative metaphor | S1-S2 | E1 | U0 | P1 | V0 | Do not use as diagnosis or scientific claim. |
| Heavy elements as weight of history | Read the generation history of heavy elements as a metaphor for the weight of experience or culture. | Creative metaphor | S1-S2 | E1 | U0 | P1 | V0 | Mark as metaphor in theoretical contexts. |
| Black-hole lens | A metaphor for the burden by which high-density ideals or histories are projected into everyday life. | Creative metaphor | S1-S2 | E1 | U0-U1 | P1 | V0 | Avoid aestheticizing collapse. |
| God, demon, and beast model | A model that reads response styles or institutional functions allegorically. | Creative metaphor / ethical allegory | S1-S2 | E1 | U0-U1 | P1 | V0 | Do not map directly onto real individuals. |
| Literary-ontological reading | A non-scientific study that reads literature, poetry, and religious vocabulary through concepts of Scientific Ontology. | Non-scientific research | S1-S2 | E1 | U0 | P1 | V0-V1 | State that it is structural reading, not proof. |
| narrative truth layer | Treat narrative not as escapism, but as a structural reading device for touching a truth-layer that factual propositions alone often do not reach. | Literary ontology / structural reading | S1-S3 | E1-E2 | U0 | P1 | V0-V1 | Do not use as historical proof or scientific proof. |
| Meifu Bureau Reincarnation Division model | Read the fictional world of reincarnation, review, assignment, belief, responsibility, and unresolved histories as an allegory of history relocation and boundary ethics. | Creative metaphor / literary ontology | S1-S2 | E1-E2 | U0-U1 | P1 | V0-V1 | Not religious doctrine, not a claim about the afterlife, not an institutional model. |
| belief-gravity domain | Read belief, prayer, narrative, and role as forming a domain that attracts histories and constrains interpretive paths of characters or worlds. | Creative metaphor / conceptual model | S1-S3 | E1-E2 | U0-U1 | P1 | V0-V1 | Do not identify with physical gravity or religious reality. |
| reincarnation loop as history relocation | Read reincarnation not as proof of the soul, but as a narrative structure in which unresolved histories, roles, responsibilities, and belief paths are recalculated in another arrangement. | Creative metaphor / structural reading | S1-S2 | E1-E2 | U0 | P1 | V0-V1 | Not a doctrinal claim about rebirth. |

These materials do not prove Scientific Ontology, and they must not be turned into diagnostic, religious, or empirical claims.
---

## 12. Current Overall Assessment

This table is not specific to History-Field Topology. It is a public control table for managing claim strength, publication layer, misreading risk, application risk, and verification stage across Scientific Ontology as a whole.

Scientific Ontology should not be presented externally as a unified theory, a replacement for standard science, a religious system, or a claim that fictional settings are real.

In the public version, it should be presented as a conceptual frame for boundary, contact, history, return, subsequent conditions, synchronization, desynchronization, meaning formation, residuals, residues, and cutoff.

Research Notes may handle stronger connections to physics, cosmology, literature, AI boundary functions, social boundaries, value theory, and Meifu Bureau-style creative readings. However, strong claims must be classified by S/E/U/P/V.

Physics-proximate concepts should respect standard scientific definitions and be treated as correspondence candidates, projections, or structural analogies from Scientific Ontology. PINGER, BlackHole, entanglement, Feynman diagrams, chaos theory, and history-gravity domain require special E3 deceleration when published.

Creative and literary vocabulary such as the Meifu Bureau, reincarnation, and belief-gravity domain should be treated as literary-ontological notes for reading history, responsibility, belief, return, and relocation. They are not religious claims or proof of the afterlife.

Publication handling is not decided by claim strength alone. High E should be slowed down with notes, limitations, and non-claim boundaries. High U should be abstracted or kept non-public.

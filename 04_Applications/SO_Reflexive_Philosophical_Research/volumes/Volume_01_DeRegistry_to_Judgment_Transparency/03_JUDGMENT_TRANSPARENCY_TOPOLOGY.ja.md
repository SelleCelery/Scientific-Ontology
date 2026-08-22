# 判断透明性トポロジー — 現行アプリケーション・インターフェース

> Status: Application method / experimental but reusable
> Layer: 04_Applications
> Role: reusable judgment-transparency method interface
> Authority: Does not define truth, external-domain doctrine, or final Metadata Assessment Policy.
> Language: Japanese authoritative
> Public profile: P2

## 1. 目的

本インターフェースは、判断を正解へ強制収束させるための分類器ではない。

目的は、判断がどの接点・位相・経路・返路・開放端を通って成立したかを記録し、異議、再評価、比較、後続修正を可能にすることである。

## 2. 一次観測：五つの通信位相

### 2.1 接点整合性 / Anchor Integrity

判断が何に接触しているか。その情報、対象、出典、命題、権限を別のものへすり替えていないか。

特に、text author / represented voice / endorsement / derived addition / commitment ownerを分ける。

### 2.2 位相整合性 / Phase Integrity

観測、引用、表象、解釈、評価、仮説、一般化、処方、実行などの位相を無標識で飛んでいないか。

### 2.3 経路可読性 / Path Legibility

結論へ至る途中で何が保持され、変換され、圧縮され、捨象されたかを後から追えるか。

### 2.4 返路実効性 / Return Reachability

異議、反例、失敗、追加データが、実際に判断を変更し得る地点へ戻れるか。異議受付窓口が存在するだけでは十分ではない。

### 2.5 開放端保持 / Open-End Retention

未解決、理解不能、反例、解釈差を、理論の成功材料へ自動変換せず保持できるか。

## 3. 二次観測：Primitive Deviation

詳細な異常名を先に要求しない。

- `Cut`: 必要な接続・返路・中間根拠が切れている。
- `False Link`: 保証されていない対象・主体・位相・範囲が接続済みとして扱われる。
- `Both`: 切断と偽接続が同時に起きる。
- `Unresolved`: 現在の情報では三分類へ確定できない。

誤帰属、位相跳躍、範囲漏出、経路消去、偽閉鎖などは任意のnamed patternであり、本体ではない。

## 4. 生ログ

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

原則は`detect -> preserve -> optionally classify`である。

## 5. 層間変換監査

異なる言語ゲームや専門領域を横断する場合、可能なら次の三層を分ける。

```text
A. domain-authoritative description
B. repository representation / Optional Axiom description
C. SO-derived interpretation
```

Aは「絶対に正しい層」ではない。どのsource、翻訳、専門家、institution、interpretive traditionに依存するかをSource Provenance Ledgerへ残す。

監査するのは主としてA→B、B→Cの変換である。必要ならA→C authority bypassも見る。

### 出典と導出を分ける

出典が明示されていることは、後続主張がその出典から導出されていることを意味しない。

```text
source exists
  !=
derivation established
```

固有名・権威・科学的成功が、変換経路を飛び越えてCのwarrantとして働く場合、bypass候補として記録する。

## 6. 高次ラベルとの関係

E/U/S/V/P等を使用する場合、一次・二次観測を凍結した後にだけ付与する。

高次判定は下位記録を遡及修正してはならない。

仮の依存順序は次である。

```text
source / contact
  -> topology
  -> primitive deviation
  -> E / U
  -> S / V*
  -> P
```

この次数モデル自体は未確定である。高次になるほど制度・公開・責任配分など政治的要素が増える可能性があるが、現段階では研究仮説として扱う。

V*は過去のVerification Stageの再採用を意味せず、実験上の投影としてのみ使用する。

## 7. 議論プロトコルへの展開

あるclaim `C`がwarrant `W1`に依存し、`W1`へ異議が出た場合、次の返路を持つ。

- `W1`の追加根拠を提示する。
- `W1`または`C`を修正する。
- `C`を撤回する。
- 異議側が別claimを立てるなら、そのclaimに新しい責務を立てる。
- 現時点で進められない場合、未解決として停止する。

異議側は、必ずしも完全な対抗世界観を証明する責任を負わない。「この接続からその結論は出ない」という異議は、その接続を問題化するだけで成立し得る。

## 8. 根拠系列の停止

本方法は、究極根拠の存在または不存在を前提にしない。

記録するのは、現在の根拠系列がどこで止まったかである。

停止点の例：

- 観測
- 定義
- 方法上の前提
- 制度上の権限
- 価値選択
- 実務目的
- 言語使用上の前提
- 未根拠の仮置き
- unresolved

停止したことを、証明済み・合意済み・根源的真理と偽装しない。

## 9. 境界接続

境界接続は、相手を自分の体系へ統合することと同義ではない。

現段階の安全な原則は次である。

> 接続候補を提示し、双方が自分の内部制約と残差を保持したまま、受信・拒否・修正・再送できる経路を残す。

接続が成立した後も、各体系は内部崩壊へ抗う権利を失わない。

「境界の仕事は侵入ではなく誘因である」は、今後検査すべき強い研究仮説として残す。

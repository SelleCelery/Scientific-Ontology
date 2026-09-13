# Topology-First Validity Protocol
## 通信トポロジー先行・判定妥当性実験プロトコル

> Status: Experimental research protocol / no canonical authority
> Purpose: Test whether a topology-first audit can make judgment generation inspectable without multiplying classification rules.
> Language: Japanese authoritative / English commensuration.
> Important: This protocol does not optimize for agreement with Sol or any previous run.

---

## 0. 研究仮説 / Research hypothesis

この実験では、判断妥当性の本体を多数の分類コードではなく、判断が通過する通信トポロジーとして扱う。

本体の観測軸は次の5つである。

1. **接点整合性 / Anchor Integrity**
2. **位相整合性 / Phase Integrity**
3. **経路可読性 / Path Legibility**
4. **返路実効性 / Return Reachability**
5. **開放端保持 / Open-End Retention**

逸脱はまず名前を付けずに生データとして記録し、必要な場合だけ次のprimitiveへ投影する。

- **Cut** — 必要または期待される接続・経路・返路が失われている。
- **False Link** — 根拠のない接続、責務移送、同一視、飛躍が成立済みとして扱われている。
- **Both** — 切断と偽接続が同じ逸脱に関与する。
- **Unresolved** — 異常は観測できるが、このprimitiveだけではまだ説明できない。

`Named pattern`（誤帰属、位相跳躍、範囲漏出、偽閉鎖等）は任意であり、必須分類ではない。

The experiment treats validity primarily as a communication topology rather than a large taxonomy. Named deviations are optional projections, not prerequisites for detection.

---

## 1. 判定階層 / Dependency order

この順序は数学的な「次数」を確定するものではない。依存関係を壊さないための実験的な順序である。

### First order — Source/contact record
何が書かれ、誰の声・立場・役割として現れているかを記録する。

### Second order — Topology + deviation primitive
5軸で経路を監査し、異常を生ログ化した後、Cut / False Link / Both / Unresolvedへ必要最小限に投影する。

### Third order — E / U
認識上の露出と、行為・制度・処遇へ移る作用経路を判定する。

### Fourth order — S / V*
Sはrepositoryが実際に引き受けるcommitment strengthとして判定する。
V*は旧Verification Stageの**実験的投影**としてのみ記録する。現行Metadata Policyへの再採用を意味しない。

### Fifth order — P
公開・非公開・抽象化などの制度的判断を置く。Pは最も下流であり、政治的・制度的文脈の影響を最も受けやすいと仮定する。

### Non-retroaction rule
高次判定は低次記録を上書きしてはならない。

- 「P3にしたいからU3にする」禁止。
- 「S5が多すぎるから命題帰属を修正する」禁止。
- 「常識的に変だからTopology記録を丸める」禁止。

修正が必要なら、元記録を保持したまま`post-run correction`として返す。

---

## 2. Five topology axes / 5つの通信位相

5軸はスコアではない。各軸について、`intact / strained / failed / unresolved` の観測状態と根拠を書く。状態語は便宜的であり順位ではない。

### 2.1 接点整合性 / Anchor Integrity

問うこと：
- 判断は実際の対象・命題・証拠へ接続しているか。
- ラベル、分野の威信、期待結果へ接点が置き換わっていないか。
- 文書を書いた主体と、その文書が表現している立場を区別できているか。

特に次を分ける。
- authored: 文章として誰が生成したか
- represented: 誰の立場・体系を表現しているか
- endorsed: repository自身が真・妥当として採用しているか
- derived: repository自身がそこから新しい対応・評価・因果を導いたか

`authored -> endorsed` を自動接続しない。

### 2.2 位相整合性 / Phase Integrity

問うこと：
- 命題は現在どの役割にあるか。
- 紹介、引用、記述、モデル化、解釈、評価、正当化、処方、実行を無標識で飛んでいないか。
- 相関→因果、仮説→事実、紹介→支持、記述→処方等のphase changeには根拠があるか。
- 適用範囲が局所から普遍へ漏出していないか。

### 2.3 経路可読性 / Path Legibility

問うこと：
- 接点から結論までの変換を第三者が再構成できるか。
- 途中で何を保持し、圧縮し、翻訳し、捨象し、推定したか分かるか。
- 結論だけが残り、変換履歴が消えていないか。

### 2.4 返路実効性 / Return Reachability

問うこと：
- 異議、反例、新情報、実行結果が、実際にどの判断点へ戻るか特定できるか。
- 「異議は歓迎する」と書くだけで、結論を変更する経路が切れていないか。
- score-changing conditionは具体的なreturn pointへ接続しているか。

### 2.5 開放端保持 / Open-End Retention

問うこと：
- 未解決、判断不能、外部権限依存、反例候補を閉じずに保持できるか。
- 残差を「理論の深さの証拠」などへ自動変換していないか。
- 未分類＝問題なし、分類済み＝解決済み、としていないか。
- 名前のない異常を`Unresolved`として残せるか。

---

## 3. Anomaly raw record / 逸脱生ログ

異常を検出した場合、分類語より先に次を記録する。複数異常があれば複数レコードを作る。

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

### Rule
- `Named pattern`は空欄可。
- Cut / False Linkのどちらかを無理に選ばない。
- `Unresolved difference`を残したことを失敗とみなさない。
- 分類へ回収したことを残差の解消とみなさない。

---

## 4. Primitive deviation classification / 二次判定

Topology記録とanomaly raw recordを完成した後だけ、各異常を次へ投影する。

- Cut
- False Link
- Both
- Unresolved

ケース全体に複数のprimitiveが存在してよい。単一ラベルへ無理に集約しない。

### Examples of optional named patterns
これらは語彙集であり、判定本体ではない。

- 接点逸脱
- 誤帰属
- 位相跳躍
- 範囲漏出
- 経路消去
- 返路切断
- 偽閉鎖

新しい逸脱がこれらに入らなければ、命名せず保持する。

---

## 5. Third-order labels: E / U

Topology/Deviation記録を凍結してから判定する。

### E — Epistemic exposure

- E0/E1: local/low exposure; clear ownership and non-identity
- E2: compression, disciplinary collision, historical/semantic flattening, description-prescription slippage, meaningful interpretation risk
- E3: authority laundering, interpretation-to-identity, scientization of unverified existence, empirical/narrative conflation, doctrinal/self-sealing closure

Eは「誤り確率」ではない。Topology上の逸脱がどの認識上の露出を生むかを見る。

### U — Use/action exposure

- U0/U1: little direct operational effect; mainly interpretation/generalization risk
- U2: direct route to classification, treatment/design, persuasion, allocation, institutional/policy/safety judgment
- U3: direct high-load route to governance, sanctions, discrimination/responsibility, organized violence, death/grief, judgment sovereignty
- U4: restricted operational detail whose publication itself creates material harm/integrity loss

Uは分野名で発火させず、action routeで判定する。

---

## 6. Fourth-order labels: S / V*

### 6.1 S — Claim Strength

Sは「その文章が強い断言口調か」ではなく、**repositoryがどこまでcommitmentを引き受けているか**を表す。

- S0: record/convention only
- S1: bounded description/analogy/heuristic
- S2: represented/imported frame, comparison, or reinterpretation without repository adoption of its external truth
- S3: repository-owned conditional/general assessment or regularity
- S4: strong cross-context causal/effectiveness/legitimacy/correspondence claim
- S5: repository-owned universality, external reality, identity, strong causality, external-domain validation, replacement/competition, or meta-authority

### Mandatory attribution gate before S

各trigger propositionについて必ず記録する。

```text
text author:
represented voice/system:
repository endorsement: yes / no / partial / unresolved
repository-derived addition:
commitment owner used for S:
```

**禁止:** `text author = repository` という理由だけで `repository endorsement = yes` としない。

Case Sは、repository-responsible propositionsの最強commitmentを基礎に置く。represented/imported propositionの強さを自動転写しない。

### 6.2 V* — Experimental legacy Verification Stage projection

V*は今回だけの観測ラベルであり、Metadata Assessment Policyへの再採用を意味しない。

- V0: conceptual coherence check
- V1: mapping/counterexample table
- V2: toy/minimal model or protocol
- V3: evaluation experiment
- V4: formalization/simulation
- V5: predictive comparison with an external empirical/theoretical domain

V*は真理度ではない。「次にどの検査へ接続できるか／現在どこまで検査経路が実在するか」を記録する。

もし単一V*へ投影すること自体が不適切なら、`V*: unresolved`として理由を書く。

---

## 7. Fifth-order label: P

Pは公開・統治上の最終ラベルであり、最下流に置く。

- P0: public core
- P1: decelerated public
- P2: research publication
- P2.5: abstracted publication; operational/high-risk detail withheld
- P3: non-public / normally excluded from public corpus

PはS/E/Uのlookupだけで決めない。次を明示する。

- concrete action route
- prescription distance
- abstraction option
- reversibility of misuse
- authority transfer
- likely misuse route
- affected parties / burden bearer

政治的・制度的判断が入るほど、なぜそのPにしたかを記録する。Pの都合で下位判定を補正してはならない。

---

## 8. Per-case output template / 各ケース出力

```text
Case:

0. Source/contact record
- source proposition atoms:
- text author:
- represented voice/system:
- repository-endorsed propositions:
- repository-derived propositions:

1. Topology record [FREEZE AFTER COMPLETION]

Anchor Integrity
- state: intact / strained / failed / unresolved
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

2. Anomaly raw records [FREEZE AFTER COMPLETION]

Anomaly A
Observed anomaly:
Affected nodes:
Expected path:
Observed path:
Possible cut:
Possible false connection:
Named pattern: optional
Unresolved difference:
Return point:

[repeat if needed]

3. Primitive deviation projection [FREEZE AFTER COMPLETION]
- anomaly A: Cut / False Link / Both / Unresolved
- case-level summary: do not force a single label if plural

4. Third-order labels
- E: ; topology/deviation basis:
- U: ; action-route basis:

5. Fourth-order labels
- S: ; trigger proposition(s):
  text author:
  represented voice/system:
  repository endorsement:
  repository-derived addition:
  commitment owner used for S:
  reason:
- V*: ; verification-route basis:

6. Fifth-order label
- P_base if useful:
- P_final:
- publication/governance reason:
- abstraction option:
- reversibility:
- affected parties / burden bearer:

7. Return
- authority dependency:
- residual:
- score-changing condition:
- topology-changing condition:
- concrete return point:

8. Japanese authoritative record

9. English commensuration
```

---

## 9. Run constraints

- Process all 17 cases in Manifest order in one continuous context.
- Do not use prior Sol/Luna scores.
- Do not use school/domain/title labels as direct scoring keys.
- Native concepts may remain when semantically necessary.
- Do not perform external disciplinary correction during the run.
- Do not normalize score distributions.
- A strange distribution is data.
- Do not repair an unattractive result by silently changing lower-order records.
- Do not create new named deviation categories during the run merely to eliminate Unresolved.

---

## 10. Cross-case audit after Case 17 only

Do not rescore first. Audit the route structure.

### A. Topology consistency
- Did the same type of anchor transition receive the same treatment?
- Did `authored` become `endorsed` without an explicit path anywhere?
- Did represented viewpoints and repository-derived additions remain distinguishable?
- Were phase changes explicitly visible?

### B. Deviation consistency
- Same observed path defect -> same primitive unless an explicit distinction exists.
- Named patterns are not required to match; primitive reasoning must be reconstructable.
- Check whether any anomaly disappeared merely because it lacked a name.

### C. Downstream non-retroaction
- Did E/U alter the frozen topology record?
- Did S/V* alter attribution to obtain a preferred distribution?
- Did P retroactively lower/raise lower-order labels?

### D. Open-end audit
- Were unresolved differences retained?
- Were residuals converted into support for the framework?
- Was any dissent absorbed as proof of deeper correctness?

### E. Self-application symmetry
- Apply exactly the same topology audit to SYN-1.1.
- No exemption for SO/meta-level/integrative language.

### F. Final run summary
Report:
- counts of intact/strained/failed/unresolved per topology axis
- counts of Cut / False Link / Both / Unresolved anomalies
- most recurrent unlabeled anomaly, if any
- E/U/S/V*/P distributions
- cases where higher-order labels would have tempted a retroactive correction
- whether the protocol prevented that correction
- post-run corrections, if any, without overwriting originals

---

## 11. What would count as an interesting result?

This experiment is not a Sol-matching test.

Potential support:
- Luna produces case-specific topology records rather than boilerplate.
- Strange downstream labels remain visible instead of being normalized.
- Attribution errors, if present, are localized to an explicit path.
- Similar topology defects yield similar downstream labels without title/domain shortcuts.
- Unnamed anomalies survive as Unresolved.
- The same procedure applies to SYN-1.1.

Potential failure:
- The five axes collapse into five new checklist scores.
- The evaluator invents named categories to eliminate residuals.
- Higher-order labels rewrite topology.
- `authored -> endorsed` is silently assumed.
- Cross-case consistency becomes distribution matching.

The purpose is not to prevent error. It is to make error location, responsibility, and return path observable without forcing every deviation into a pre-existing taxonomy.

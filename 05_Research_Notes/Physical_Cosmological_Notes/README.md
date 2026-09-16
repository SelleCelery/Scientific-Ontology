# Physical and Cosmological Notes / 物理・宇宙論近接ノート

> Layer: 05_Research_Notes / Physical_Cosmological_Notes
> Status: README
> Scope: intrinsic time / cosmological topology / history-field projection / chaos / logical depth / physics-adjacent hypotheses
> Language: ja+en
> Public profile: P1-P2.5
> Authority: Directory navigation and maintenance contract; not a concept-definition owner

# 日本語正本

## 1. Directory Role / ディレクトリの位置づけ

この小分類は、存在境界論の概念を、物理学・宇宙論に近い語彙と照合する高強度の研究ノートを置く。

ここで行うのは標準物理学の置換ではない。共通して見えている境界現象を探し、構造アナロジー、存在論的再解釈、形式化候補、物理主張候補を区別し、観測・反証可能性への開けを管理する。

この小分類では、**事実と根拠仮説を分ける**。標準物理学から借用する定義、測定、観測事実、理論記述は、対応する範囲で硬い外部制約として扱い、誤記があれば局所訂正する。一方、SOがそれらをどう説明し、別位相へどう接続するかは根拠仮説であり、標準物理学で未確立であるというだけでは反証扱いにしない。

AMP / ITS は、こうした仮説の形成起源または高強度モデルとして参照され得るが、経験的証拠そのものとしては扱わない。物理学は強い破壊試験として用いるが、SO仮説の存在を許可する最終審級にはしない。

## 2. Public Scope / 公開範囲

含むもの：

- 内在時間と標準模型の対応候補
- 存在論的宇宙史
- 宇宙論的トポロジー動態
- PINGER仮説と履歴場トポロジー
- カオス理論と論理-深度軸

含まないもの：

- 標準物理学の置換理論
- 完成した数理物理モデル
- 実験値、観測値、既存定義の上書き
- 予測精度を保証する宇宙論
- 非公開ITSまたはAMP Core

## 3. Documents / 文書一覧

前提：[`../../00_Overview/Physics_Correspondence_Policy.ja.md`](../../00_Overview/Physics_Correspondence_Policy.ja.md)

1. [`Intrinsic_Time_Standard_Model_Correspondence.ja.md`](./Intrinsic_Time_Standard_Model_Correspondence.ja.md) / [`en`](./Intrinsic_Time_Standard_Model_Correspondence.en.md)
2. [`Ontological_History_of_the_Universe.ja.md`](./Ontological_History_of_the_Universe.ja.md) / [`en`](./Ontological_History_of_the_Universe.en.md)
3. [`Cosmological_Topological_Dynamics.ja.md`](./Cosmological_Topological_Dynamics.ja.md) / [`en`](./Cosmological_Topological_Dynamics.en.md)
4. [`PINGER_Hypothesis_and_History_Field_Topology.ja.md`](./PINGER_Hypothesis_and_History_Field_Topology.ja.md) / [`en`](./PINGER_Hypothesis_and_History_Field_Topology.en.md)
5. [`Chaos_Theory_and_Logical_Depth_Axis.ja.md`](./Chaos_Theory_and_Logical_Depth_Axis.ja.md) / [`en`](./Chaos_Theory_and_Logical_Depth_Axis.en.md)

## 4. Maintenance Notes / 運用メモ

上流：

- [`../../01_Sat_Truth/Boundary_Realism_Principle.md`](../../01_Sat_Truth/Boundary_Realism_Principle.md)
- [`../../02_Raj_Beauty/History_Field_Topology.md`](../../02_Raj_Beauty/History_Field_Topology.md)
- [`../../02_Raj_Beauty/Scientific_Ontology_and_Science.md`](../../02_Raj_Beauty/Scientific_Ontology_and_Science.md)
- [`../../00_Overview/Claim_Strength_and_Publication_Layer_Table.ja.md`](../../00_Overview/Claim_Strength_and_Publication_Layer_Table.ja.md)
- [`../../90_Repository_Governance/Assessment/Repository_Assessment_Protocol.ja.md`](../../90_Repository_Governance/Assessment/Repository_Assessment_Protocol.ja.md)
- [`../../01_Sat_Truth/正しさ・個性・無・切断_論理通信トポロジー.ja.md`](../../01_Sat_Truth/正しさ・個性・無・切断_論理通信トポロジー.ja.md)

- 標準科学語彙の定義を上書きしない。
- 構造アナロジー、存在論的再解釈、形式化候補、物理主張候補を区別する。
- 物理主張へ近づくほど、失敗条件と観測条件を強くする。
- 日本語正本と英語通約で主張強度を変えない。
- 新規仮説はGlossary、Term Collision Registry、主張強度表との整合を確認する。

## 5. Revision Trace Examples / 修正痕の例（非規範）

以下は、v5.1.0準備で自己監査の返路を試すための**例示**であり、現時点で各文書に実際の誤りが確定したという宣言ではない。また、ここに示す項目名をrepository-wide schemaとして制度化するものでもない。

目的は、物理近接ノートで修正が必要になったとき、単に旧記述を消すのではなく、**何に接触し、なぜ再開され、どこまでを変え、何を残したか**を追跡できる形を観察することである。

### 5.1 借用した標準定義を誤記していた場合

例として、[`Intrinsic_Time_Standard_Model_Correspondence.ja.md`](./Intrinsic_Time_Standard_Model_Correspondence.ja.md) が、標準模型側の概念・測定事実・定義を誤って記述していたことが確認されたとする。

この場合のfinding候補は `EXT-REFERENCE-MISSTATEMENT` であり、初手は `CORRECT-REFERENCE` になる。修正対象は借用した外部定義・事実の表現であり、内在時間との対応仮説全体を自動的に撤回する理由にはしない。修正後は、対応仮説がなお `EXT-UNESTABLISHED` や `EXT-NONDERIVABLE` である可能性を別に保持する。

```text
Trigger: EXT-REFERENCE-MISSTATEMENT
Action: CORRECT-REFERENCE
Changed: borrowed external definition / fact statement
Preserved: intrinsic-time correspondence hypothesis
Residual: external establishment / derivability remains open
Trace: prior bytes remain in version history; reason is recorded
```

### 5.2 「導出」と書いたが導出経路を再構成できない場合

[`Cosmological_Topological_Dynamics.ja.md`](./Cosmological_Topological_Dynamics.ja.md) のように、AMP / ITS / HFCからの「導出」を強く述べる箇所について、監査時に `Γ_SO ⊬ H` が成立し、しかも本文自身が導出済みであることをclaimしていたとする。

この場合は `SO-NONDERIVABLE` を記録し、`INTERNAL-TRACE` / `REOPEN-SO` に進む。再構成可能な導出がなければ、該当箇所を「導出定理」から「作業仮説」「生成モデルから得た仮説」等へ局所的に弱める、または当該claimだけを一時保留することが考えられる。

重要なのは、文書全体や形成履歴を消すことではなく、**導出したという責任だけを、実際に保持できる範囲へ戻すこと**である。

```text
Trigger: SO-NONDERIVABLE
Action: INTERNAL-TRACE -> REOPEN-SO
Candidate disposition: scope-restricted / suspended / rewritten as hypothesis
Preserved: research question, formation provenance, unaffected sections
Residual: derivation path may be reconstructed later
```

### 5.3 既知事実と本当に衝突した場合

[`Ontological_History_of_the_Universe.ja.md`](./Ontological_History_of_the_Universe.ja.md) や [`PINGER_Hypothesis_and_History_Field_Topology.ja.md`](./PINGER_Hypothesis_and_History_Field_Topology.ja.md) の物理近接記述が、同一referent・同一scope・同一測定条件で確立している外部事実と両立しないことが確認されたとする。

その場合はまず `EXT-FACT-CONFLICT` として `BOUNDARY-AUDIT` を行い、単なる位相差、語義差、scope mismatch、外部からSOへのbridge overreachではないことを確認する。genuine conflictであれば、衝突しているclaimを局所修正、scope制限、または `suspended` 相当の保留状態へ戻す。

ここでも、ノート全体をlegacy化したり、非標準仮説であるという理由だけで公開面から除外したりしない。

### 5.4 同じ事実を別位相から読んでいるだけなら修正しない

標準定義と事実記述を正しく保持したうえで、同じ事実群をSO側が別の境界条件・意味位相から読む場合は、`SAME-FACT-ALT-INTERPRETATION` または `RECIPROCAL-BRIDGE-DISPUTE` になり得る。

この場合の初手は `COMMENSURATION-INTAKE` であり、非標準であること自体を修正理由にしない。fact / interpretation / derivation / bridge claimを同じ接触面へ出せるかを先に確認する。

これらの例は、将来のrevision governanceを先取りして完成させるためではなく、**修正と保存を同時に行うために何を記録すべきか**を観察するための足場である。

# English Commensurated Rendering

## 0. Role

This subdirectory contains higher-claim research notes collating Scientific Ontology concepts with physics- and cosmology-adjacent vocabulary.

It does not replace standard physics. It seeks shared boundary phenomena, distinguishes structural analogy, ontological reinterpretation, formalization candidates, and physical-claim candidates, and manages openness to observation and falsification.

This subdirectory **separates facts from ground hypotheses**. Definitions, measurements, observational facts, and theoretical descriptions borrowed from standard physics are treated as hard external constraints within their relevant scope, and local misstatements are corrected. By contrast, SO explanations of those facts and proposed connections across other phases are ground hypotheses; mere lack of establishment in standard physics is not treated as falsification.

AMP / ITS may be referenced as formation provenance or as high-strength models for such hypotheses, but not as empirical evidence in themselves. Physics is used as a strong destructive test, not as the final court deciding whether an SO hypothesis is allowed to exist.

## 1. Public Scope

Included:

- candidate correspondences between intrinsic time and the Standard Model;
- an ontological history of the universe;
- cosmological topological dynamics;
- the PINGER hypothesis and History-Field Topology;
- chaos theory and the logical-depth axis.

Not included:

- a replacement theory for standard physics;
- a completed mathematical-physics model;
- overwriting of experiments, observations, or established definitions;
- a cosmology guaranteeing predictive accuracy;
- private ITS or AMP Core.

## 2. Documents and Recommended Reading Order

Prerequisite: [`../../00_Overview/Physics_Correspondence_Policy.ja.md`](../../00_Overview/Physics_Correspondence_Policy.ja.md)

1. [`Intrinsic_Time_Standard_Model_Correspondence.ja.md`](./Intrinsic_Time_Standard_Model_Correspondence.ja.md) / [`en`](./Intrinsic_Time_Standard_Model_Correspondence.en.md)
2. [`Ontological_History_of_the_Universe.ja.md`](./Ontological_History_of_the_Universe.ja.md) / [`en`](./Ontological_History_of_the_Universe.en.md)
3. [`Cosmological_Topological_Dynamics.ja.md`](./Cosmological_Topological_Dynamics.ja.md) / [`en`](./Cosmological_Topological_Dynamics.en.md)
4. [`PINGER_Hypothesis_and_History_Field_Topology.ja.md`](./PINGER_Hypothesis_and_History_Field_Topology.ja.md) / [`en`](./PINGER_Hypothesis_and_History_Field_Topology.en.md)
5. [`Chaos_Theory_and_Logical_Depth_Axis.ja.md`](./Chaos_Theory_and_Logical_Depth_Axis.ja.md) / [`en`](./Chaos_Theory_and_Logical_Depth_Axis.en.md)

## 3. Return and Maintenance

Upstream:

- [`../../01_Sat_Truth/Boundary_Realism_Principle.md`](../../01_Sat_Truth/Boundary_Realism_Principle.md)
- [`../../02_Raj_Beauty/History_Field_Topology.md`](../../02_Raj_Beauty/History_Field_Topology.md)
- [`../../02_Raj_Beauty/Scientific_Ontology_and_Science.md`](../../02_Raj_Beauty/Scientific_Ontology_and_Science.md)
- [`../../00_Overview/Claim_Strength_and_Publication_Layer_Table.ja.md`](../../00_Overview/Claim_Strength_and_Publication_Layer_Table.ja.md)
- [`../../90_Repository_Governance/Assessment/Repository_Assessment_Protocol.en.md`](../../90_Repository_Governance/Assessment/Repository_Assessment_Protocol.en.md)
- [`../../01_Sat_Truth/Correctness_Individuality_Absence_and_Cut.en.md`](../../01_Sat_Truth/Correctness_Individuality_Absence_and_Cut.en.md)

- Do not overwrite standard scientific definitions.
- Distinguish structural analogy, ontological reinterpretation, formalization candidates, and physical-claim candidates.
- Strengthen failure and observational conditions as a note approaches a physical claim.
- Do not change claim strength between Japanese authoritative texts and English commensurations.
- Check new hypotheses against the Glossary, Term Collision Registry, and claim-control table.

## 4. Revision-Trace Examples (Non-Normative)

The following cases are **examples** for testing a self-audit return path during v5.1.0 preparation. They do not assert that the referenced documents have already been found erroneous, and the labels shown here are not yet a repository-wide revision schema.

The purpose is to observe what must be retained when a physics-adjacent note needs revision: **what it encountered, why it reopened, what changed, and what remained**.

### 4.1 Misstatement of a Borrowed Standard Definition

Suppose [`Intrinsic_Time_Standard_Model_Correspondence.ja.md`](./Intrinsic_Time_Standard_Model_Correspondence.ja.md) were found to misstate a Standard Model concept, measurement fact, or external definition. A candidate finding would be `EXT-REFERENCE-MISSTATEMENT`, with `CORRECT-REFERENCE` as the first response. The borrowed definition or fact statement would be corrected locally; the intrinsic-time correspondence hypothesis would not thereby be automatically withdrawn. Its lack of external establishment or derivability could remain as separate findings.

### 4.2 A Claimed Derivation Cannot Be Reconstructed

Suppose a passage such as the strong derivational wording in [`Cosmological_Topological_Dynamics.ja.md`](./Cosmological_Topological_Dynamics.ja.md) cannot reconstruct a path from AMP / ITS / HFC and `Γ_SO ⊬ H` holds, while the text itself claims derivation. The note would record `SO-NONDERIVABLE` and move through `INTERNAL-TRACE` / `REOPEN-SO`. The affected wording might be narrowed from a derived theorem to a working hypothesis or hypothesis generated from an internal model, or the specific claim might be suspended while its provenance and research question remain.

### 4.3 Genuine Conflict with an Established External Fact

Suppose a physics-adjacent statement in [`Ontological_History_of_the_Universe.ja.md`](./Ontological_History_of_the_Universe.ja.md) or [`PINGER_Hypothesis_and_History_Field_Topology.ja.md`](./PINGER_Hypothesis_and_History_Field_Topology.ja.md) is shown to be incompatible with an established external fact under the same referent, scope, and measurement conditions. `EXT-FACT-CONFLICT` first triggers `BOUNDARY-AUDIT` to rule out a phase difference, term mismatch, scope mismatch, or bridge overreach. If the conflict is genuine, the conflicting claim can be corrected locally, scope-restricted, or returned to a suspended state. The note as a whole is not automatically deprecated merely because it contains a non-standard hypothesis.

### 4.4 Alternate Interpretation of the Same Facts Is Not Itself a Correction Trigger

If standard definitions and factual statements are retained accurately while SO reads the same facts through another boundary condition or semantic phase, the finding may instead be `SAME-FACT-ALT-INTERPRETATION` or `RECIPROCAL-BRIDGE-DISPUTE`. The first response is `COMMENSURATION-INTAKE`, not automatic correction. The contact surface should first distinguish fact, interpretation, derivation, and bridge claim.

These examples do not complete future revision governance. They provide an observational foothold for learning what must be preserved when correction and historical continuity have to coexist.

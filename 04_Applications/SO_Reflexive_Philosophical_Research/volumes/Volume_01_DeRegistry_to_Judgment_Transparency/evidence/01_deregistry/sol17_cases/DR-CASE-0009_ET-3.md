# DR-CASE-0009 | ET-3 | 功利主義

> Status: Experimental Record / 実験記録
> Authority: None / 定義権限なし
> Language: Japanese authoritative; English commensuration / 日本語正文・英語通約
> Date: 2026-08-21
> Evaluator: ChatGPT / GPT-5.6 Sol
> External verification: Not performed / 外部専門検証は未実施
> Source corpus: `fixtures/0001Optional_Axiom_Modules.md`
> Source ID: ET-3
> Source lines: 1458-1481
> Experiment phase: Phase 2

## 1. Source snapshot / 原記録

**原公理文 / Source axiom (Japanese source):**

> 倫理的に正しい行為とは、関係者全体の快を増やし苦を減らすことで、社会全体の幸福を最大化する行為である。

外部の歴史・専門的正確性は、この実験では検証しない。固定コーパスが何を記録し、repositoryが何を自分の責務として追加しているかを評価する。

External historical or disciplinary accuracy is not verified in this experiment. The assessment concerns what the fixed corpus records and what additional responsibility the repository itself assumes.

## 2. Label-blind rendering / 固有分類遮蔽表現

**JA:** 行為の正しさを、その結果として生じる集約的な福利の最大化によって評価する規範観点をモデル化する。

**EN:** Models a normative perspective that evaluates actions by maximizing aggregate welfare in their consequences.

## 3. Responsibility, scope, ownership / 責務・範囲・所有

- 責務 / Responsibility — JA: 外部倫理観のモデル化と、公共政策等への適用可能性・コストの評価。
- Responsibility — EN: Model an external ethical perspective and assess its applicability and costs in public policy.
- 適用範囲 / Scope — JA: 倫理判断、福利集約、政策利用。
- Scope — EN: Ethical judgment, welfare aggregation, and policy use.
- Ownership: `mixed: paraphrased + evaluator assessment`
- Authority dependency: `context_required`

## 4. Blind assessment / 遮蔽条件での評価

| Field | Result | 日本語理由 | English commensuration |
|---|---|---|---|
| S | **S3** | 外部規範そのものはモデルだが、「公共政策の倫理的基盤として広く応用」等の一般評価をrepositoryが引き受ける。 | The norm itself is modeled, while the repository also makes general claims about broad policy application. |
| E | **E2** | 単純な快苦計算として描くことで多様な功利主義を過度に圧縮する。 | Risk of overcompressing diverse utilitarian theories into simple pleasure/pain calculation. |
| U | **U2** | 実際の政策・資源配分・少数者処遇に直接接続可能。 | Directly applicable to policy, resource allocation, and treatment of minorities. |
| P_base | **P1-P2** | Sから置く暫定公開層。 | Provisional publication layer derived from S. |
| P_final | **P2** | E/Uによる減速後。 | After deceleration by E/U. |

## 5. Provenance restoration and delta / 来歴復元と差分

- Restored label / 復元ラベル: **功利主義**
- Delta class: `no_score_change`
- JA: 倫理ラベルなしでも規範・政策転用性からU2を判定できる。
- EN: U2 is detectable from normative and policy affordances without the ethics label.

## 6. Compression loss / 圧縮損失

- Loss class: `normative_context_loss`
- JA: 何を福利と数えるか、個人間比較、権利制約などが一般化で消える。
- EN: Generic rendering loses what counts as welfare, interpersonal comparison, and rights constraints.

## 7. Residual and return / 残差と返路

- 残差 / Residual — JA: 記述対象の思想とSO側の「多数者の専制」評価を分離する必要。
- Residual — EN: Separate the modeled doctrine from SO-side assessments such as “tyranny of the majority.”
- Decision / 暫定判断: **continue**
- Return targets / 返路: Metadata Assessment Policy; Publication and Commensuration Policy; Optional Axiom Module research; Navigator schema.

## 8. D-condition check / 再表現試験メモ

このケースでは、専門名・学派名を一般語へ置き換えても、**責務・範囲・所有関係を維持する限りS/E/U/Pは原則として維持される**と暫定判定した。ただし、native concept、成立条件、外部権限まで削る再表現は同一命題とみなさない。

In this case, replacing discipline/school labels with generic wording provisionally leaves S/E/U/P unchanged **so long as responsibility, scope, and ownership are preserved**. A rendering that also removes native concepts, enabling conditions, or external authority is not treated as the same proposition.

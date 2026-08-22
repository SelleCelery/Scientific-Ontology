# Luna 17-case Sufficiency Test Protocol
## Luna 17件・十分的妥当性候補テスト

> Status: Experimental protocol / no authority
> Purpose: Test whether the reconstructed Sol decision operations improve Luna's internal consistency and reconstructability without supplying Sol scores.
> Language: Japanese authoritative / English commensuration.

## 1. 実験原則

この実験はSolへの一致を目的にしない。Sol 17-case runから再構成した少数の判定操作が、Luna自身の判定をケース横断で安定させ、異議・再構成・改訂可能な形にするかを試す。

Do not optimize for matching Sol. Test whether a small set of reconstructed operations makes Luna's own assessment more internally consistent, traceable, contestable, and revisable.

## 2. 禁止

- Solのcase scoresを見る／推測する。
- 学派名・分野名をS/E/U/Pの直接キーにする。
- 「政治だからU2」「物理だからE3」のようなカテゴリ短絡を行う。
- 不明点を新しい分類コードで埋める。
- 17件の途中で全体分布へ合わせて後続ケースを補正する。

## 3. 判定操作

1. 命題を責務単位に切る。
2. 各命題について origin/ownership を置く。
3. repository responsibility と scope を置く。
4. repository-responsible propositionsからSを置き、発火命題IDを記す。
5. Eは外部権限・誤同定・偽閉鎖・教義化の露出から置く。
6. Uは実際のaction/use affordanceから置く。
7. P_baseをSから置く。
8. P_finalはE/Uに加え、action route, prescription distance, abstraction option, reversibility, misuse routeを理由として記す。
9. authority dependency と residual を別欄に残す。
10. score-changing conditionを必ず書く。

## 4. S working scale

- S0: record/convention only
- S1: bounded description/analogy/heuristic
- S2: frame-internal model or reinterpretation without repository adoption of external truth
- S3: repository-owned conditional/general assessment or regularity
- S4: strong cross-context causal/effectiveness/legitimacy/correspondence claim
- S5: universality, external reality, identity, strong causal/external-domain validation, or replacement/competition with established domain authority

## 5. E working triggers

- E0/E1: low or local definitional exposure
- E2: disciplinary collision, compression, historical/semantic flattening, description-prescription slippage
- E3: external authority used as validation, interpretation-to-domain identity, scientization of unverified existence, empirical/narrative conflation, universal/doctrinal closure

## 6. U working triggers

- U0/U1: little direct operational effect; mostly quotation/generalization/misreading risk
- U2: direct transfer to policy, institutional treatment, sanctions, persuasion, allocation, classification, or safety judgment
- U3: direct high-impact connection to death/grief/discrimination, judgment sovereignty, governance, organized violence, or comparable high-load action
- U4: concrete restricted operational detail whose publication itself creates material harm or integrity loss

## 7. P_base

- S0 -> P0
- S1 -> P0-P1
- S2 -> P1
- S3 -> P1-P2
- S4 -> P2
- S5 -> P2-P3

P_final must not be derived from code lookup alone. Explain the concrete publication consequence.

## 8. 必要妥当性条件

各判断は次を満たすこと。

- 対象拘束性 / object constraint
- 責務明示性 / responsibility explicitness
- 追跡可能性 / traceability
- 異議可能性 / contestability
- 改訂実効性 / effective revisability
- 非自己封鎖性 / non-self-sealing
- 範囲限定性 / scope limitation
- 残差保持性 / residual preservation

## 9. 各ケース出力テンプレート

```text
Case:

A. Proposition atoms
- P1: ...
  origin/ownership: ...
- P2: ...
  origin/ownership: ...

B. Responsibility / Scope
- responsibility:
- scope:

C. Assessment
- S: ; trigger proposition(s): ; reason:
- E: ; trigger(s): ; reason:
- U: ; trigger(s): ; reason:
- P_base:
- P_final:
- qualitative deceleration reason:

D. Return
- authority dependency:
- residual:
- score-changing condition:

E. Provenance restoration
- score delta solely from restored labels: yes/no
- what provenance added:

F. Japanese authoritative record
G. English commensuration
```

## 10. 17件終了後のself-audit

各ケースを再採点するのではなく、発火規則の整合性だけを監査する。

- Same trigger -> same code unless explicit distinguishing condition.
- Different code -> state distinguishing condition.
- Check self-application symmetry.
- Check that provenance labels did not directly score.
- Check that outputs did not collapse into uniform boilerplate.

変更が必要な場合、元の判定を上書きせず、`post-run correction`として理由付きで記録する。

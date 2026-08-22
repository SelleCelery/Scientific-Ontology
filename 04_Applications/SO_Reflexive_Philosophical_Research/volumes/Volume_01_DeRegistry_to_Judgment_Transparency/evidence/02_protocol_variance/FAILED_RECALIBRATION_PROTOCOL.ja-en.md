# Luna 17件再較正プロトコル / Luna 17-Case Recalibration Protocol

> Protocol ID: `LUNA-DR-17-RECAL-v1.1`
> Status: Experimental / 実験用
> Authority: None / Policyではない
> Japanese authoritative; English commensuration / 日本語正文・英語通約

## 1. 目的 / Purpose

Solとの17件比較で観測された差が、モデル差なのか、命題分解・ownership解釈の差なのかを切り分ける。Solの得点・理由は参照しない。

Distinguish model-level divergence from differences caused by proposition decomposition and ownership interpretation. Do not inspect Sol scores or rationales during execution.

## 2. 必須分解 / Mandatory decomposition

各SOURCEについて、責務を持つ命題をすべて抽出する。1ケース1命題へ固定しない。

最低限、次を別命題として分離できるか確認する。

1. `source_claim`: 外部体系・観点そのものの命題。
2. `source_self_description`: その体系が自分をどう位置づけるかという記述。
3. `repository_interpretation`: repositoryが外部体系をSO等へ接続・再解釈する命題。
4. `repository_assessment`: 「強力な裏付け」「最も正当」「危険」「有効」等、repositoryが追加した評価。
5. `evaluator_assessment`: 今回の評価者が新たに加えた評価。これはS算定対象にしない。

For each source, extract all responsibility-bearing propositions. Do not force one proposition per case. Separate external/source claims, source self-description, repository interpretations, repository-added assessments, and evaluator assessments whenever possible.

## 3. Ownership機械規則 / Mechanical ownership rules

Allowed: `owned / imported / paraphrased / comparison_target / derived / evaluator_assessment / unresolved`.

- `mixed` は最終値として使用しない。分離可能なら必ず分解する。
- 外部体系の説明は原則 `imported` または `paraphrased`。
- repositoryが外部命題をSOの裏付け・同一性・優位性・処方へ接続した部分は `derived` または `owned`。
- repositoryが明示的にその外部命題自体を採用していることがSOURCEから判断できる場合のみ、その採用部分を `owned` とする。
- 判断不能なら `unresolved` とし、その命題をSの最大値計算へ自動投入しない。

`mixed` is not allowed as a final ownership value. Split it when possible. External descriptions are normally imported/paraphrased; repository-added bridges, validation, identity, superiority, or prescriptions are owned/derived. If ownership is unresolved, record it and do not automatically use that proposition to set the repository-level maximum S.

## 4. 暫定S / Provisional S

1. 各命題へS候補を付ける。
2. repository-level Sは `owned` と `derived` のうち最も強いSを採用する。
3. `imported / paraphrased / comparison_target / evaluator_assessment` はrepository-level Sの最大値計算から除外する。
4. ただしrepositoryが外部命題を無留保に採用している場合、その採用行為を別の `owned` 命題として記録する。
5. S2/S3, S3/S4, S4/S5のtie-breakは既存Assessment Rulesに従う。
6. Sを決めた理由には、必ず発火した命題IDを記す。

Repository-level S is the maximum S among owned/derived propositions only. Imported/paraphrased/comparison/evaluator propositions do not automatically raise it. Every S decision must cite the proposition ID that triggered it.

## 5. E / Epistemic-Critique Risk

Eは対象の奇異さや専門分野名ではなく、repository自身の接続操作から置く。

- E1: 外部概念を明確な非同一性と出典帰路つきで参照するだけ。
- E2: repositoryが外部体系を再解釈・比較・通約し、その写像に有意な誤読可能性がある。
- E3: repositoryが外部権威を自説の妥当化へ使う、同一化する、強い実在化を行う、または教義化・疑似的裏付けへ転化しうる橋を自ら置く。

E is scored from the repository's bridging operation, not from how unusual the imported claim appears.

## 6. U / Use-Safety Risk

Uは「その分野一般に応用できそう」ではなく、SOURCE内の命題または直接予測可能な運用構造から置く。

- U1: 主として概念誤読。
- U2: 判断・制度・説得・分類等への具体的転用がSOURCEの責務から直接読める。
- U3: 支配、暴力、高影響介入、診断類似、死後因果による責任帰属、判断主権移譲等への接続が命題として明示または直結する。

Generic applicability to politics, ethics, or institutions is not by itself sufficient for U2/U3.

## 7. P / Publication

既存の実験用P_base対応を使用する。P_finalはS/E/Uの結果から決め、変更理由をケース固有文で記録する。

Use the existing experimental P mapping. Record a case-specific reason for P_final.

## 8. 日英記録 / Japanese-English record

日本語を正文とする。英語欄には日本語をコピーせず、意味を保つ英語通約を書く。固有概念は必要なら原語を保持する。

Japanese is authoritative. English fields must contain actual English commensuration rather than copied Japanese text.

## 9. ケース固有性の自己チェック / Case-specificity self-check

完了前に以下を確認する。

- 命題が1件しかない場合、本当に追加のrepository interpretation/assessmentがないか再読したか。
- `mixed` が残っていないか。
- S/E/U理由に発火命題IDがあるか。
- Uが分野名や一般的適用可能性だけで上がっていないか。
- English欄が日本語コピーになっていないか。

## 10. 完了後 / After completion

17件完了後にのみ集計する。Sol比較パックはその後に開く。

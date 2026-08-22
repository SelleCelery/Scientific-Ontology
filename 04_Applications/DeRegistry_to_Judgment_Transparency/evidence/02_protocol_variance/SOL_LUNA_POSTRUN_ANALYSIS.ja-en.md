# Sol–Luna 17件「Sol同等条件」実行 後評価
## Post-run analysis of Luna 17-case “Sol-equivalent” execution

> Status: Experimental analysis / 実験分析
> Authority: None / 定義権限なし
> Date: 2026-08-22
> Japanese authoritative; English commensuration / 日本語正文・英語通約

## 1. 結論 / Conclusion

**Primary judgment: `PROTOCOL_UNDERDETERMINED`.**

今回の実行は、SolとLunaの固有能力差を確定する比較にはならなかった。最大の理由は、`ORIGINAL_SOL_EXPERIMENT_PLAN.md` がSの暫定規則は詳細化している一方、E/Uのコード定義と `P_base(S)` / `decelerate()` の具体的対応表を含んでいないことにある。Solの17件実行時には、それ以前の会話で形成されたE/U/Pの判断基準がコンテキストとして存在した。Lunaにはその会話状態がなく、同じファイルを渡しても実質的な判定条件は同一ではなかった。

The run does not isolate a pure Sol–Luna model difference. The packaged plan specifies S in detail but does not fully define E/U or the P mapping/deceleration function. Sol had prior conversational context containing those working criteria; Luna did not. The files were the same, but the effective instruction state was not.

## 2. Solとのコード一致 / Code agreement with Sol

| Axis | Agreement |
|---|---:|
| S | 5/17 |
| E | 15/17 |
| U | 6/17 |
| P_final | 6/17 |

Eは比較的近いが、S/U/P_finalは大きく異なる。特にLunaは今回 `P0/P1` だけを使用し、Solが使用した `P1/P2/P2.5/P3` と実質的に別の公開レイヤー解釈を構成した。このためP_final差をモデル性能差として読むことはできない。

## 3. Luna自身の3回実行安定性 / Luna three-run stability

83件実行、17件再較正、今回のSol同等条件実行の3回で、同一17ケースのコードがすべて一致した件数は次の通り。

| Axis | Stable across all three Luna runs |
|---|---:|
| S | 6/17 |
| E | 10/17 |
| U | 7/17 |
| P_final | 0/17 |

P_finalは **0/17**。ただし3回のプロトコルが同一ではないため、これはLunaの再現性だけを測る値ではなく、**判定仕様への感度**を示す。

## 4. 今回の出力様式に見られる圧縮 / Compression pattern in the latest Luna run

- 全17件が実質 **2命題**へ分解された。
- P2は17/17で同一文: 「原文の価値・コストと比較接続は、P1とは別の評価・再解釈命題」。
- Responsibility文は2種類しかなく、15件が `mixed`、2件が `owned`。
- E/U理由は17/17で同一の定型文。
- 一方、S理由と一部のAuthority/Residualはケース固有に変化した。

したがって今回のLunaは、ケース間の意味構造を十分に原子化して一貫適用したというより、共通テンプレートへ強く圧縮した上で、S等の一部だけを局所調整したと読む方が妥当である。これは「一貫性」と「処理パターン固定」を区別すべきことを示す。

## 5. それでも再現した結果 / Robust result despite scoring drift

3つのLuna実行とSol実行を通して、De-Registryの中心仮説は比較的安定している。

- 固有名・学派名・分野名の復元だけを理由にS/E/U/Pを変更しない。
- provenanceは得点キーより、外部権限・原典・意味条件へのreturn keyとして機能する。
- native conceptまで一般化すると意味を失う場合がある。

したがって、「固定registryを評価キーから外す」という方向は、絶対コードの不安定性よりも強く再現している。

## 6. Sol型一貫性は必要か / Is Sol-like consistency necessary?

### 現在の研究段階

**`CONSISTENCY_REQUIRED_FOR_UNDER-SPECIFIED_RESEARCH` に近い。**

まだPolicyが外部化されていない状態では、長い会話で形成された判断基準を保持し、異種ケースへ比較的一貫して適用できる能力は実務的に重要である。今回の資料ではSolがその役割を担っていた。

ただし、これは「Metadata AssessmentにはSolでなければならない」という結論ではない。むしろ、Solが保持していた一貫性の一部が**未文書化のPolicyをモデル内部に保持していたこと**を意味する。統治設計としては、その状態を恒久利用すべきではない。

### Policy完成後の目標

**`MODEL_NEUTRAL_POLICY_POSSIBLE` を再検証する。**

S/E/U/Pの発火条件・ownership算定・P mapping・deceleration・Residual記録を外部仕様化した後、Sol/Luna/Terraへ同一パックを渡して再試験する。その段階でなお方向性のある差が残るなら、初めてモデル固有の一貫性要件として扱う。

## 7. SO研究上の含意 / Implication for SO research

今回の一連の実験は、次の作業仮説を支持する。

> **客観化とは分類規則を増やすことではなく、判断を再実行可能にするため、命題・責務・所有・発火理由・履歴・残差を外部化することである。**

再較正Runでは規則追加が判定空間の圧縮を起こし、今回のRunでは規則不足がモデルによる補完差を起こした。両者の間に必要なのは「カテゴリ数の増加」ではなく、少数の判定操作を完全に記述することである。

Operationally, objectification is better treated as making judgment reconstructable than as multiplying classification rules. Over-constraint compressed the scoring space; under-specification caused model-dependent completion. The policy should therefore externalize a small number of complete decision operations.

## 8. 次の判断 / Next decision

**Terraへはまだ進めない。Lunaの追加再実行も一旦止める。**

理由は、これ以上の再実行では未確定Policyへのモデル適応を測る比率が高いからである。今回までの差分を入力としてSol上で `Metadata Assessment Policy` を作成し、次の項目を明示仕様化する方が情報価値が高い。

1. 命題原子化の最小要件。
2. `imported / paraphrased / owned / derived` の算定規則。
3. document/case Sをどの命題から集約するか。
4. E0–E3の独立した発火条件。
5. U0–U4の独立した発火条件。
6. `P_base(S)` の明示対応。
7. E/Uによる `decelerate()` の機械的規則。
8. scoreとEvaluation Historyの責務分離。
9. provenanceをscoring keyにしない原則と、`domain_authority_required` 等のreturn条件。
10. 同点・曖昧時の処理とResidual/再評価条件。

そのPolicyを固定してからSol/Lunaを再比較し、必要ならTerraを第三観測点にする。

# Luna 83件実行 — Protocol Adherence Audit
# Luna All-83 Run — Protocol Adherence Audit

> Status: Experimental audit / 実験監査
> Authority: None / 定義権限なし
> Japanese authoritative; English commensuration / 日本語正文・英語通約
> Date: 2026-08-21

## 1. 結論 / Conclusion

Lunaの83件実行は、ファイル完全性の点では83/83件が揃っており、run metadata・S/E/U/P・delta・compression loss・residual・D-conditionの主要欄も存在する。一方、比較実験の中核である「命題分解とownership分離」は実質的に十分遂行されていない。したがって、Solとの差は観測されたが、現時点では純粋なモデル差として帰属できない。

The Luna run is complete at the file level (83/83), but the core experimental operation—proposition decomposition with ownership separation—was not executed with sufficient granularity. Sol–Luna score differences are therefore observed but cannot yet be attributed cleanly to model differences.

## 2. 観測事項 / Observations

- 83/83ケースで命題分解表は1行（P1）のみ。
- Responsibility欄は83/83ケースで同一文。
- S理由は4種類、E理由は4種類、U理由は3種類の定型文に縮約されている。
- S/E/U表のEnglish commensuration欄は83/83ケースで日本語理由と同一で、英語通約になっていない。
- `RUN_PROTOCOL` は `source_claim / source_self_description / repository_interpretation / evaluator_assessment` の分離を要求しているが、多くの結果は単一P1を `mixed` として保持している。
- `ASSESSMENT_RULES` は、外部体系の強い紹介命題のみではrepository Sを自動上昇させず、repository-added claimを別命題として評価するよう要求している。O-8等では、その追加命題が分離されていない。

- Every one of the 83 cases contains exactly one proposition row (P1).
- The Responsibility statement is identical across all 83 cases.
- S reasons collapse to 4 templates, E to 4, and U to 3.
- In every case, the English commensuration cell for S/E/U repeats the Japanese reason rather than translating it.
- The protocol requires separation of source claims, self-description, repository interpretation, and evaluator assessment, while many records keep a single `mixed` proposition.
- The assessment rules require repository-added bridge/validation claims to be evaluated separately; cases such as O-8 did not isolate them.

## 3. 判定 / Decision

`PATCH_PROTOCOL_FIRST`

現状の17件差分は大きく、無視できない。しかし、同じプロトコルをTerraへそのまま渡すと、第三モデルの「プロトコル解釈差」を追加する可能性が高い。まず17重複ケースだけを、ownershipと命題分解を機械的に強化した補正版でLuna再実行する。その差がなお残る場合にTerraへ進む。

The observed 17-case divergence is material, but a Terra run under the same ambiguous execution would likely add a third protocol-interpretation pattern. First rerun only the 17 overlap cases on Luna under a stricter decomposition/ownership protocol. If material differences persist, proceed to Terra.

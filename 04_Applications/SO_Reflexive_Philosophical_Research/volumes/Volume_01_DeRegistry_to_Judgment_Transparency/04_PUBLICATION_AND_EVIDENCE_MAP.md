# Publication and Evidence Map

> Status: Public evidence-governance note
> Layer: 04_Applications
> Role: publication boundary / evidence map
> Authority: Local to this volume; repository-wide policy remains in 90_Repository_Governance
> Language: Japanese authoritative with English labels
> Public profile: P1
> Purpose: show what is published, what is held, and why; publicity itself is not treated as proof.

## 1. 公開判定

| Artifact class | Decision | Reason |
|---|---|---|
| 紀・伝・現行Topology method | Public | 方法と発展履歴の理解に必要。個人情報・危険な実装詳細を含まない。 |
| De-Registry初期計画・Phase2 summary | Public | 研究質問と最初の再現結果を示す。現行Policyではないことを明示。 |
| Sol/Luna protocol variance analysis | Public | モデル差を結論化せず、protocol underdeterminationを示す失敗証拠。 |
| Failed Luna recalibration protocol/result | Public | 「規則追加＝客観化」ではないことを示す負の結果。 |
| Implicit Metadata Assessment reconstruction | Public | Solを正解とせず、暗黙操作を反証可能な仮説へ外在化した記録。 |
| Luna sufficiency protocol + S5-festival result | Public | 透明な逸脱が上流の誤帰属を露出した重要な証拠。 |
| Topology-first protocol + 17-case result | Public | 五軸とPrimitive deviationの自己適用を示す。 |
| Three-layer protocol + 4-case result | Public | 外部source→Optional Axiom→SO解釈の変換を監査した記録。 |
| Sol/Luna comparison CSV | Public | 実験履歴の再計算可能性を上げる。ただしground truthではない。 |
| 旧Optional Axiom全文 fixture | Hold / link-by-hash | 現行SOの教義と誤認されやすい。固定テストコーパスとしてのwrapperを別途整えるまで本巻へ複製しない。 |
| Luna全83 raw results | Hold / raw archive | protocol adherence上の欠陥・定型化が大きく、本文理解には過剰。存在とhash/元pathだけ記録する。必要ならraw archiveとして別公開可能。 |
| Blind comparison packs / execution packs | Hold / redundant archive | 実験実行には必要だったが、完了後の第一巻本文理解には重複が大きい。必要ならrelease asset化する。 |

## 2. 固定fixture

- Source filename: `0001Optional_Axiom_Modules.md`
- Role: old atlas / fixed stress-test corpus; not current canon
- SHA-256: `20c3fa4f3c82719cf3716b4a52974b433c945143434ffb1a5a47b779fa8ae136`
- Research source location in working repository: `05_Research_Notes/000_Optional_Axiom_DeRegistry_Experiment/fixtures/0001Optional_Axiom_Modules.md` when available in the full experiment package

このhashは同一入力を確認するためのものであり、内容の妥当性を保証しない。

### v5.1で再確認したsource identityと公開境界

上表の `Hold / link-by-hash` は、Volume Iを最初に包装した時点の公開判断として残す。v5.1公開準備では、当時記録されたSHA-256と保持されていたsource copyを再照合し、同一fixtureであることを確認した。

その後のprivate/source監査では、固定fixtureがprivate lineageの断片を含むことを確認したため、**exact bytesを公開Repositoryへ収録せず、source identity・hash・研究利用関係だけを公開する**方針を採用した。

- Source index: [`../../sources/README.md`](../../sources/README.md)
- Historical filename: `0001Optional_Axiom_Modules.md`
- SHA-256: `20c3fa4f3c82719cf3716b4a52974b433c945143434ffb1a5a47b779fa8ae136`
- Relation: research-source identity / experiment provenance; **not current SO canon**
- Public handling: identity-and-hash only; **exact source bytes are private and are not included in this repository**

この判断は過去の実験入力を否定または改変するものではない。むしろ、実験で使用した入力のidentityを保持しつつ、現在のpublic/private boundaryを明示する。公開Repositoryだけではfixture全文を再配布・再構成しない。

## 3. 外部sourceを含む4-case result

`evidence/05_three_layer/RESULT_4_CASES.md`の外部source ledgerとURLは、Luna runが記録したものをraw experimental evidenceとして保持する。この第一巻のpackaging stepでは外部sourceを再検証・再解釈していない。

したがって、公開時には次を区別する。

- Luna runがsourceとして参照・記録したこと
- そのsource内容について本repositoryが独立検証したこと

後者は本巻では主張しない。

## 4. 透明性と公開量

透明性は「すべてを同じ階層へ大量公開すること」ではない。

必要なのは、何を公開し、何をHoldし、何をraw archiveへ置いたか、その理由と返路が追跡できることである。

大量のraw出力によって主要な失敗点・判断経路が不可視になる場合、indexとhashを公開し、raw artifactを別層へ分離することも透明性の一部として扱う。

## 5. 公開証跡の扱い

`evidence/`は「現在の結論だけ」を選別したフォルダではない。後の方法によって問題が判明したrunも、失敗理由を含めて保存する。

ただし、raw artifactを置いたことはその内容へのendorsementを意味しない。各runは、その時点のProtocol・モデル・入力に対する履歴証拠である。

## 6. Historical attestation / 現在からの歴史的受理

2026-09-13、`MANIFEST.sha256`の45 pathを現在Repositoryへ照合し、**19 exact match / 26 current divergence / 0 missing / 0 invalid** を確認した。historical hashは更新しない。26件は、24件のformatting-level divergenceと、2件のlater wrapper / provenance evolutionへ分類した。

この関係を、真理承認ではなくprovenance / method historyの受理として [`HISTORICAL_ATTESTATION_2026-09-13.ja.md`](./HISTORICAL_ATTESTATION_2026-09-13.ja.md) に固定する。受理時点の現在bytesは別の [`ATTESTED_CURRENT_2026-09-13.sha256`](./ATTESTED_CURRENT_2026-09-13.sha256) に記録する。

したがって、`MANIFEST.sha256`はhistorical checksum record、`ATTESTED_CURRENT_2026-09-13.sha256`はpresent-day audit snapshotとして役割を分ける。後者から現在bytesが変化した場合、このhistorical integrity acceptanceは再検査対象へ戻る。

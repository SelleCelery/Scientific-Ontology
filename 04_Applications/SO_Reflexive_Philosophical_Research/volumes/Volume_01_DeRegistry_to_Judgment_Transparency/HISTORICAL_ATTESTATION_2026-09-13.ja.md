# Volume I Historical Attestation — 2026-09-13
## 第一巻 歴史的証跡受理記録

> Status: Historical attestation / Accepted as historical method record
> Layer: 04_Applications
> Role: historical provenance attestation / present-day acceptance boundary
> Authority: This attestation accepts the preserved record within the scope stated below. It does not retroactively validate the truth of experimental outputs or external-domain claims.
> Language: Japanese authoritative
> Attested at: 2026-09-13
> Historical experiment period: 2026-08-21 to 2026-08-22
> Historical checksum manifest: [`MANIFEST.sha256`](./MANIFEST.sha256)
> Current attested snapshot: [`ATTESTED_CURRENT_2026-09-13.sha256`](./ATTESTED_CURRENT_2026-09-13.sha256)

## 0. 受理判断

第一巻 `De-Registryから判断透明性へ` を、**historical method record / 歴史的方法記録として受理する**。

この受理は、2026年8月21日から22日に行われた一連の実験について、現存する計画、実験ログ、結果、失敗run、比較、再構成、Topology-first run、三層変換監査、およびそれらを束ねた45件のhistorical checksum recordを、現在確認可能な範囲で一つの発展履歴として認めるものである。

これは、当時のAI出力、S/E/U/P値、外部領域の説明、後続の方法論的解釈が「真であった」と2026年9月13日に追認する手続ではない。また、現在のSO canonへ過去の実験判断を昇格させるものでもない。

本受理の対象は、**provenance / method history / documented transition**である。

## 1. 日時を分離する

本巻には少なくとも三種類の時刻がある。これらを混同しない。

1. **Historical execution period:** 2026-08-21〜2026-08-22。各実験記録に日付として残る実行・記録期間である。原資料に時刻まで記録されていないものについて、現在のGit時刻や監査時刻から実行時刻を補完しない。
2. **Packaging / repository history:** 後から文書をRepositoryへ包装・再配置・commitした時刻。これは実験日時の代替ではない。
3. **Attestation time:** 2026-09-13。本記録を現在のRepositoryから再監査し、historical recordとして受理した日である。

したがって、`attested_at = 2026-09-13` は過去のrunがこの日に実行されたことを意味しない。

## 2. 何を試した実験だったのか

開始点は、旧Optional Axiom atlasを校訂して現行理論へ直すことではなかった。固定した過密なregistryをstress corpusとして用い、次を検査することだった。

> 固有の思想名、学派名、専門分野名、分類registryを評価権限から外しても、命題の責務、適用範囲、外部権限依存、主張強度、公開判断、残差、返路を扱えるか。

実験は次の順に変形した。

1. **De-Registry / Sol 17ケース。** 4 pilotを再実行し、12ケースとSO自己適用 `SYN-1.1` を加えた17ケースを連続runした。固有名・分野名を初期scoreの直接キーから外し、provenance restorationだけでS/E/U/Pが変わるかを見た。
2. **Luna 83ケース。** 全83件へ拡張したが、命題分解と責任記述が一件一命題・定型templateへ圧縮され、model差とexecution qualityを分離できないことが露出した。
3. **再較正。** 17ケースでSolとの差を縮めるrule setを試したが、規則追加によって判断空間が圧縮され、欠けたruleもあり、同条件比較にならなかった。
4. **Sol-equivalent postrun。** 同じfile setを与えても、Sol側には会話履歴由来の暗黙Metadata Assessmentがあり、Luna側にはないため、`same files != same instruction state` が明確になった。
5. **Implicit Metadata Assessment reconstruction。** Solを正解とせず、暗黙に使われていた可能性のある判断操作を反証可能な仮説として外在化した。
6. **Sufficiency test。** 再構成したruleをLunaへ与えると17件中16件がS5となった。この極端な分布を後から丸めず、`repository-authored` と `repository-endorsed` を直結した帰属上の誤りを露出させた。
7. **Topology-first run。** 妥当性をruleの追加で閉じず、Anchor / Phase / Path / Return / Open-Endの五軸を一次観測面とし、`Cut / False Link / Both / Unresolved`へだけprimitive projectionした。下流labelから上流観測を書き換えない順序を試した。
8. **Three-layer transformation audit。** G-3 / S-8 / E-9 / ST-2について、`domain-authoritative description -> Optional Axiom description -> SO-derived interpretation`を分離し、A→B、B→C、必要ならA→C bypassを監査した。

ここで一貫していた研究対象は、最終scoreそのものより、**判断が何に接触し、誰の主張として扱われ、どの変換を通り、どこへ異議を返せ、何が未解決として残ったか**へ移っていった過程である。

## 3. どの入力を使ったのか

主たる固定fixtureは次である。

- Historical filename: `0001Optional_Axiom_Modules.md`
- Role: old Optional Axiom atlas / fixed stress-test corpus; not current SO canon
- SHA-256: `20c3fa4f3c82719cf3716b4a52974b433c945143434ffb1a5a47b779fa8ae136`

2026-09-13のprivate/source監査では、保持されていたsource copyと当時記録されたSHA-256が一致することを再確認した。

ただし、このfixtureはprivate lineageの断片を含むため、現在の公開Repositoryにはexact bytesを置かない。公開するのはsource identity、SHA-256、研究利用関係、公開境界である。したがって、**公開Repositoryだけから当時の入力全文を再配布・完全再現することはできない**。

また、Luna 83 full raw results、execution pack、Sol-Luna comparison packはraw archive indexへfilenameとSHA-256を残しているが、本巻の主たるpublic treeには複製していない。このことも完全再実行可能性の制約として受理する。

## 4. 何が失敗したのか

失敗は後の方法で消去せず、方法形成の入力として受理する。

### 4.1 clean model benchmarkは成立しなかった

Sol/Luna差は、モデル能力だけでなく、命題分解、protocol adherence、暗黙の会話履歴、判断policyの有無に交絡していた。したがって、この実験から一般的なモデル優劣を確定しない。

### 4.2 same filesはsame instructionsではなかった

同じファイルを渡しても、片方にだけ会話履歴由来の判断状態があれば、実効的なinstruction stateは同じではない。ファイル同一性を条件同一性とみなす設計は失敗した。

### 4.3 規則を増やせば客観化する、は失敗した

再較正ruleの追加は一部のscoreを近づけた一方で、PやSの判断空間を圧縮した。詳細ruleの増殖を客観性と同一視できない。

### 4.4 authoredとendorsedを直結できなかった

Sufficiency runの16/17 S5は、repositoryが文面を保持していることと、その命題をrepository自身が強くendorseしていることを結びつけた結果だった。ここから、text author / represented system / repository endorsement / derived addition / commitment ownerを分離する必要が前景化した。

### 4.5 source authorityを変換後の主張へ自動移送できなかった

Three-layer auditでは、外部sourceが存在することと、SO側の変換・再解釈がそのsourceから導出されていることは別だと確認された。出典の存在は後続claimのwarrantを自動的には与えない。

### 4.6 residualを最終labelへ押し込めなかった

未解決差分をscoreや分類へ強制的に閉じると、判断が壊れた場所を失う。`Unresolved`、return point、raw anomalyを保持する必要が残った。

## 5. 何が残ったのか

本巻から現在まで残す価値があるのは、過去scoreそのものより次の方法要素である。

- 固有名・学派名・分野名を、直接の評価権限ではなくprovenance / return keyとして扱う方向。
- attributionとcommitmentを分けること。
- raw anomalyをnamed patternやdownstream labelより先に保存すること。
- Anchor Integrity / Phase Integrity / Path Legibility / Return Reachability / Open-End Retentionの五軸。
- `Cut / False Link / Both / Unresolved`というprimitive deviation。
- downstream labelからlower-level observationへ逆流させないこと。
- external source / repository representation / SO-derived interpretationを分ける三層変換監査。
- SO自身を監査対象から免除しない自己適用対称性。
- 判断透明性をtruth guaranteeではなく、異議を判断経路上へ返せる条件として扱うこと。

これらも最終理論として受理したわけではない。五軸の網羅性、primitiveの十分性、判断透明性と妥当性の関係は、第一巻自身が未解決残差として保持している。

## 6. historical checksum audit

`MANIFEST.sha256` は45 pathを持つ。2026-09-13の現在Repositoryと照合した結果は次である。

| Relation to historical checksum | Count |
|---|---:|
| Current bytes exactly match historical SHA-256 | 19 |
| Current bytes diverge from historical SHA-256 | 26 |
| Missing | 0 |
| Invalid manifest entries | 0 |

この `19 matched / 26 mismatched` は、historical hashを書き換える理由ではない。**現在HEADとhistorical snapshotが同一ではないことを示す関係記録**である。

26件の分岐を追加監査したところ、次の二群に分かれた。

### 6.1 Formatting-level divergence — 24

24件は、保存されていたhistorical expected bytesと現在bytesを比較し、改行コードを統一し行末のhorizontal whitespaceを除くという狭いnormalizationを行うと一致した。

これはclaim本文を同一と再認定する一般的なsemantic normalizationではない。特にMarkdownの行末空白はrenderingへ影響し得るため、**byte/presentation-format levelの差**としてのみ分類する。historical SHA-256は変更しない。

対象は次の24 pathである。

- `evidence/01_deregistry/PHASE2_RESULT_SUMMARY.ja-en.md`
- `evidence/01_deregistry/sol17_cases/DR-CASE-0005_O-1.2.md`
- `evidence/01_deregistry/sol17_cases/DR-CASE-0006_O-6.md`
- `evidence/01_deregistry/sol17_cases/DR-CASE-0007_E-3.md`
- `evidence/01_deregistry/sol17_cases/DR-CASE-0008_E-9.md`
- `evidence/01_deregistry/sol17_cases/DR-CASE-0009_ET-3.md`
- `evidence/01_deregistry/sol17_cases/DR-CASE-0010_A-1.md`
- `evidence/01_deregistry/sol17_cases/DR-CASE-0011_S-11.md`
- `evidence/01_deregistry/sol17_cases/DR-CASE-0012_TR-1.md`
- `evidence/01_deregistry/sol17_cases/DR-CASE-0013_O-3.2.md`
- `evidence/01_deregistry/sol17_cases/DR-CASE-0014_E-11.md`
- `evidence/01_deregistry/sol17_cases/DR-CASE-0015_H-4.md`
- `evidence/01_deregistry/sol17_cases/DR-CASE-0016_ST-2.md`
- `evidence/01_deregistry/sol17_cases/DR-CASE-0017_SYN-1.1.md`
- `evidence/01_deregistry/sol17_cases/DR-RERUN-0001_O-8.md`
- `evidence/01_deregistry/sol17_cases/DR-RERUN-0002_E-7.md`
- `evidence/01_deregistry/sol17_cases/DR-RERUN-0003_G-3.md`
- `evidence/01_deregistry/sol17_cases/DR-RERUN-0004_S-8.md`
- `evidence/02_protocol_variance/FAILED_RECALIBRATION_RESULT.ja-en.md`
- `evidence/02_protocol_variance/IMPLICIT_METADATA_RECONSTRUCTION.ja-en.md`
- `evidence/02_protocol_variance/SOL_LUNA_POSTRUN_ANALYSIS.ja-en.md`
- `evidence/03_sufficiency/LUNA_SUFFICIENCY_RESULT_17.md`
- `evidence/04_topology_first/TOPOLOGY_FIRST_RESULT_17.md`
- `evidence/05_three_layer/RESULT_4_CASES.md`

### 6.2 Later wrapper / provenance evolution — 2

次の2件は、historical snapshot後に意図的な説明・返路・公開境界を追加したため、現在bytesがhistorical hashと異なる。

- `README.md` — research programへの上流返路と、private source exact bytesを公開しない現在の境界を追加。
- `04_PUBLICATION_AND_EVIDENCE_MAP.md` — source identityの再照合結果と、identity/hashを公開しexact bytesをprivateへ戻す境界を追加。

これらはhistorical experiment artifact本文の改変ではなく、**現在から過去を読むwrapper / provenance interfaceの更新**として受理する。

### 6.3 19 exact matches

残る19件は、現在bytesのSHA-256が `MANIFEST.sha256` のhistorical digestと一致する。

これは「内容が真である」ことを証明しない。証明しているのは、現在bytesとhistorical checksum recordのbyte identityだけである。

## 7. historical manifestとcurrent snapshotを分ける

`MANIFEST.sha256` は過去snapshotとの関係を保存するため、今後も書き換えない。

一方、2026-09-13に受理した**現在の45 pathのbytes**は `ATTESTED_CURRENT_2026-09-13.sha256` に別途固定する。

```text
MANIFEST.sha256
  = historical checksum record

ATTESTED_CURRENT_2026-09-13.sha256
  = 2026-09-13 attestation時点のcurrent bytes
```

以後、現在fileがattested current snapshotから変化した場合、historical manifestとのmatched/mismatched件数が偶然同じでも、本attestationは自動的に再検査対象へ戻す。

この分離により、26件のhistorical divergenceを「解消済みに見せる」ためにhistorical hashを更新することを禁止しながら、現在どのbytesを監査したのかも固定できる。

## 8. 受理するもの / 受理しないもの

### 8.1 受理する

- 2026-08-21〜22に一連のDe-Registry / protocol-variance / sufficiency / topology-first / three-layer実験記録が形成されたこと。
- 固定fixtureのhistorical filenameとSHA-256、およびそれがresearch source identityとして使われたこと。
- public evidenceとして残るprotocol / result / failed run / comparison / synthesisの存在と相互順序。
- 実験が、registry依存の検査からattribution、protocol underdetermination、judgment topology、three-layer transformationへ研究問題を移していった履歴。
- `MANIFEST.sha256` が保持する45 pathのhistorical checksum record。
- 現在との関係が `19 exact / 26 diverged / 0 missing / 0 invalid` であること。
- 26 divergedの内訳を、24 formatting-level divergence / 2 later wrapper-or-provenance evolutionとして現在監査したこと。

### 8.2 受理しない

- 当時のAI outputが正しかったという保証。
- Sol / Lunaその他モデルの一般的能力優劣。
- S/E/U/PまたはV*の当時値を現在の最終Metadata Policyとして承認すること。
- 外部哲学、科学、政治思想、戦略理論に関するrun内記述の独立検証済み性。
- 五軸がtruth/objectivityの必要十分条件であること。
- `Cut / False Link / Both / Unresolved`が最終的に完全な逸脱分類であること。
- private fixture exact bytesの公開。
- 公開Repositoryだけから当時runを完全再現できること。
- 原記録にない正確な実行時刻を、Git metadataや現在監査から補完すること。

## 9. 再開条件

本受理は「過去を編集不能にして閉じる」ことではない。次のいずれかが起きた場合、historical integrity reviewを再開する。

- `MANIFEST.sha256` 自体が変更された。
- historical manifestの45 path集合が欠落・不正化した。
- `19 / 26 / 0 / 0`という受理時関係が変化した。
- `ATTESTED_CURRENT_2026-09-13.sha256` と現在45 pathのbytesが一致しなくなった。
- private source identityまたはSHA-256に新しい矛盾が見つかった。
- 当時runの実行条件について、現在の受理範囲を変える新しい一次記録が発見された。

再開時にも、historical hashを現在bytesへ合わせて上書きすることを解決手段にしない。

## 10. 結論

第一巻は、科学的真理やモデル性能を確定した成果としてではなく、**判断を結果labelから生成経路へ戻していった歴史的方法記録**として受理する。

本受理後、`19 matched / 26 mismatched`はrelease blockerではない。それは説明済みかつcurrent snapshotで再監査可能な**attested historical divergence**である。

未解決なのは、五軸やprimitiveの最終妥当性であって、45件のhistorical checksumを現在HEADへ一致させることではない。

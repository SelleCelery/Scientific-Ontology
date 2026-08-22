# 伝 — 試行、失敗、転回

> Status: Public historical method record
> Layer: 04_Applications
> Role: experiment history / failed-run and transition record
> Authority: Application-level historical synthesis; not canon
> Language: Japanese authoritative
> Public profile: P1-P2
> Maintenance: do not rewrite failed runs as if the later method had already been known.

## 伝一　旧Atlasを「直す」のではなく、試験台にする

旧Optional Axiom atlasは、哲学、宗教、科学、倫理、美学、政治、戦略、死生観、SO内部命題を同じ形式へ並べた巨大なregistryだった。

最初の誘惑は、このregistryを現行正本へ合わせて整理することだった。しかし実験では逆に、過密な分類体系をそのまま固定し、「固有名を評価キーから外しても判定できるか」を試すことにした。

ここで、sourceを校訂する作業と、sourceをstress corpusとして使う作業を分けた。

## 伝二　Solの17件とLunaの83件

Solの初期17件では、provenance restorationだけではscoreが変わらなかった。Lunaの83件でも同じ現象が反復した。

一方で、Luna 83件runは命題分解や理由記述が強く定型化していた。結果の数値だけを比較すれば、モデル差と誤認し得る状態だった。

このため、結果比較の前にexecution qualityとprotocol adherenceを監査する必要が生じた。

## 伝三　再較正の失敗

Lunaへ17件の再較正ルールを追加すると、一部scoreはSolへ近づいた。しかしPがほぼP2/P2.5へ圧縮され、Sの上限も狭まった。

さらに、再較正パックには参照されるAssessment Rulesの一部が欠けており、同条件比較になっていなかった。

この失敗は、詳細規則を増やすことが客観化ではない、という問題を直接示した。

## 伝四　「Sol同等条件」の失敗

次に、Solが使った研究計画へ戻してLunaを走らせた。しかし同じファイルを渡しても、Solにはそれ以前の会話で形成されたE/U/P等の暗黙基準があり、Lunaにはなかった。

結果として、同じファイル条件は同じinstruction stateではなかった。

ここで「モデルの一貫性」が必要なのか、「暗黙のPolicyが外在化されていない」のかを分ける必要が生じた。

## 伝五　暗黙Metadata Assessmentの逆算

Solの17件から、次のような潜在操作を再構成した。

- 命題を責務単位へ切る
- 外部体系の命題とrepository-derived claimを分ける
- Sを真偽確率ではなくcommitment strengthとして読む
- Eをauthority laundering、誤同定、偽閉鎖への露出として読む
- Uをaction affordanceとして読む
- PをS/E/Uだけでなく作用経路・可逆性・公開時の誤用経路から判断する
- residualとauthority dependencyをscoreへ潰さない

これはSolを正解として固定する作業ではなく、Lunaで反証できる再構成仮説として扱った。

## 伝六　S5祭り

Lunaへ再構成した少数操作を与えると、17件中16件がS5となった。

この結果は笑えるほど極端だったが、重要なのはLunaが後から丸めなかったことだった。同じtriggerを横断適用し、各ケースにscore-changing conditionを残した。

そのため、S5の問題を「Lunaが雑」として処理せず、`repository authored -> repository endorsed`という上流接続へ戻せた。

このrunは、透明性の高い失敗が、もっともらしい一致より研究価値を持ち得ることを示した。

## 伝七　9条件から5位相へ

判断妥当性の候補として、対象拘束性、責務明示性、帰属妥当性、追跡可能性、異議可能性、改訂実効性、非自己封鎖性、範囲限定性、残差保持性が列挙された。

しかし項目増殖は、分類できない逸脱を見落とす危険を持つ。そこで通信トポロジーへ再配置した。

- 接点整合性
- 位相整合性
- 経路可読性
- 返路実効性
- 開放端保持

逸脱名は本体にせず、まず`Cut / False Link / Both / Unresolved`だけを置き、生ログを先に保存する方式へ変更した。

## 伝八　SO自己適用

Topology-firstの17件で、SYN-1.1は5軸すべてfailedとなった。

「統合する体系ほど自己監査を免除する」のではなく、統合を主張するほど接続責任が増える形になった。

この結果はSOに都合が悪いが、そのまま残された。方法の妥当性を支えるのは、SOに好都合な結果ではなく、SO自身に不利な結果を同じ監査で保持できたことにある。

## 伝九　外部sourceを入れる

Topology-firstだけでは、Optional AxiomにすでにSOによる改変が埋め込まれている可能性を分離できなかった。

そこでG-3、S-8、E-9、ST-2について三層を並べた。

```text
Layer A: domain-authoritative description
Layer B: Optional Axiom description
Layer C: SO-derived interpretation
```

監査対象を思想そのものから変換エッジへ移した。

結果として、出典ラベルの有無ではなく、warrant modeの変化、語彙圧縮、現代化、科学権威の形而上学への流入、比較から同型への滑りなどを局在化できた。

## 伝十　境界接続の次の問題

E-9は特に、SO側が量子力学を存在論へ接続したくなる欲求そのものを見える形にした。

この欲求は研究動機として排除しない。ただし、SO側の接続欲求を量子力学自身の主張へ変換してはならない。

次の研究線では、境界接続を一方向の取り込みではなく、双方が自分の内部制約を保持したまま、接続候補を提示・拒否・修正できる構造として扱う必要がある。

現時点では「境界の仕事は侵入ではなく誘因である」という表現は仮説である。より弱くは、**境界は結論を輸入するのではなく、相手側から再検討可能な接続機会を提示する**、と置ける。

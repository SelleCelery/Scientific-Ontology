# Repository Assessment Protocol
# リポジトリ監査原則

> Status: Policy Draft / Candidate
> Layer: `90_Repository_Governance/Assessment`
> Role: repository-wide assessment protocol / judgment-transparency control
> Scope: proposition attribution / repository commitment / responsibility / claim scope / warrant and ground-search path / topology audit / reciprocal external connection / assessment finding contract / validity-regime preservation / engagement-capacity boundary / evaluation history / residual and return management / audit-capture prevention / reconstruction drills
> Language: Japanese authoritative; English commensuration available
> Authority: Candidate governance document. It does not become repository-wide authority until explicitly adopted.
> Derivation: distilled from the De-Registry, protocol-variance, sufficiency, topology-first, and three-layer transformation experiments recorded under `04_Applications/SO_Reflexive_Philosophical_Research/volumes/Volume_01_DeRegistry_to_Judgment_Transparency/`.
> Non-claim: this protocol does not define truth, prove Scientific Ontology, replace domain-specific standards, or automate final human judgment.

---

## 0. 目的
> **監査は正しさを展示するための手続ではない。体系が、自分を完成済み・理解済み・接続済みであると誤認しないために持つ内在的作法である。**

この姿勢を、本Protocolの採用理由に関する構成的前提として最初に置く。

本Protocolは、この前提を本Protocol自身によって証明しようとしない。監査を採用するか否かはrepository ownerの判断である。ただし、監査を採用した後、その運用がこの目的から逸脱していないか、その結果が自己正当化や表示上の整合へ変質していないかは監査対象になる。

したがって、監査の成功を「指摘数が多い」「全項目が埋まった」「外部監査へ通った」「資料が整って見える」ことによって定義しない。

### 0.1 Methodological Provenance / 方法論的遡及

本Protocolのうち、命題帰属の分離、repository commitmentの分離、判断透明性Topology、raw anomaly優先、Cut / False Link、strange-result preservation、protocol sufficiency等の中核手法は、`04_Applications/SO_Reflexive_Philosophical_Research/volumes/Volume_01_DeRegistry_to_Judgment_Transparency/`に記録された実験、失敗run、再較正、比較、残差から形成された。

したがって、これらの方法命題に異議がある場合、本Protocol本文だけでなく、その形成過程、失敗記録、比較結果、未解決事項へ遡及できることを要件とする。

ただし、Volume Iは本Protocolの**方法論的provenance**であり、個々の監査findingを自動的に正当化する上位権威ではない。

個別findingは、その都度、対象文書、対象domain、根拠系列、接続責任、再実行可能性、反証・異議に対して独立に責務を負う。

本文書は、存在境界論｜Scientific Ontology の公開リポジトリにおいて、文書、命題、通約、応用、研究記録、メタデータ、公開判断をどの順序で監査するかを定める候補Policyである。

監査の目的は、対象を一つの尺度で採点し、正解・不正解へ強制収束させることではない。

目的は、少なくとも次を分離し、後から再構成可能にすることである。

- 何が観測・記述されたか。
- 誰の命題・立場・定義を表しているか。
- repositoryがその命題をどの程度自ら引き受けているか。
- どの位相で、どの範囲について述べているか。
- どの根拠・規則・外部権限を経て判断へ至ったか。
- 接続途中で何が保持・変換・圧縮・捨象されたか。
- 異議、反例、失敗、追加証拠をどこへ返せるか。
- 何が未解決として残っているか。

監査結果は、正本本文を自動的に書き換えない。

```text
source / document / claim
  -> observation
  -> assessment
  -> recommendation
  -> human review
  -> approve / edit / reject / hold
  -> repository change, if explicitly applied
  -> later return / reassessment
```

本文書自体も同じ原則で監査される。

---

## 1. 適用原則

### 1.1 Domain first

対象領域に固有の定義、法令、仕様、実証方法、証拠条件、安全条件、業務要件、当事者の明示目的を先に扱う。

存在境界論の語彙へ変換するために、対象領域の成立条件を変更してはならない。

ただし、`Domain first`は「外部領域がSOより上位である」ことを意味しない。

原則として、各体系は自分の内部命題、定義、方法、証拠条件について第一責任を持つ。

- 外部領域の内部命題は、その領域自身のsource、標準、方法、証拠条件に照らして読む。
- SO内部の命題は、SO自身の定義、根拠系列、非主張境界、研究履歴に照らして読む。
- 双方を接続するbridge claimは、その接続を提出した主体が正当化責任を負う。

外部領域はSOの権威ではなく、独立した接続相手である。SOも外部領域の上位解釈者ではない。

したがって、接続監査では上下関係ではなく、双方の内部命題がそれぞれの根拠系列へ遡及可能か、また接続命題が双方から訂正・拒否・再接続可能かを確認する。

### 1.2 命題単位を先にする

文書名、章名、フォルダ、著者名、学派名、分野名から先に評価しない。

監査対象を、必要な粒度の命題または運用規則へ分解する。

一つの段落に複数の責務がある場合、別命題として扱う。

```text
Document
  -> proposition 1
  -> proposition 2
  -> represented external proposition
  -> repository-derived proposition
  -> operational rule
```

文書単位の評価値が必要な場合も、命題単位の記録から後で投影する。

### 1.3 固有名を評価キーにしない

思想名、学派名、人物名、専門分野名、著名なsource名は、provenance、return key、source ownershipとして保持する。

ただし、それらを直接の評価理由にしない。

```text
proper name = provenance / return key
proper name != assessment key
```

固有名を外しても同じ命題、帰属、責任、範囲、接続条件が保持されるなら、固有名だけを理由に評価を変更してはならない。

### 1.4 同じtriggerには同じ判断理由を要求する

同じ評価条件から異なる結果を出す場合、差を生んだ条件を明示する。

「今回は自然に見えるから」「この分野だから」「この文書は正本だから」といった無標識な例外を認めない。

評価結果が異なるなら、少なくとも一つの区別条件を記録する。

### 1.5 評価者の自然さで結果を補正しない

プロトコルに従って奇妙な結果が一貫して生じた場合、その結果を期待分布へ戻すためのad hocな補正をしない。

まず、どの規則からその結果が生じたかを追跡する。

奇妙さは、対象の異常だけでなく、プロトコル不足、帰属不足、定義不足、評価者の暗黙前提を示す可能性がある。

### 1.6 隠れた評価規則を使わない

監査結果を左右する規則は、プロトコル、対象文書、外部domain rule、または明示された評価者仮定として記録する。

過去会話、暗黙のモデル知識、評価者だけが知る補助規則を、無標識に決定規則へ使わない。

必要な規則が文書化されていない場合は、結果を自然化せず、次のいずれかとして扱う。

- protocol insufficiency
- evaluator assumption
- unresolved
- return required

### 1.7 監査は真理スコアではない

監査可能性、透明性、再構成可能性、主張強度、成熟度、公開可否、有用性、人気、実装成功、真理性を一つの尺度へ圧縮しない。

透明な判断も誤り得る。

有用な応用も、SO全体の真理性を証明しない。

強い主張も、それだけで誤りではない。

---

## 2. 監査の固定単位

監査を開始する前に、対象状態を固定する。

最低限、次を記録する。

```yaml
audit_fixture:
  audit_id: ""
  date: YYYY-MM-DD
  source_commit: ""
  protocol_path: "90_Repository_Governance/Assessment/Repository_Assessment_Protocol.ja.md"
  protocol_revision_reference: ""
  includes: []
  excludes: []
  target_paths: []
  purpose: ""
  evaluator: "human / model / mixed"
  model_or_tool: "optional"
```

### 2.1 Source Commit

Git管理下の監査では、原則として監査開始時のcommitを記録する。

監査途中に対象本文が変更された場合、同じfixtureとして続行するか、新fixtureとして再開するかを記録する。

### 2.2 Includes / Excludes

「正本監査」「公開文書監査」「特定Application監査」などの対象範囲を明示する。

対象外文書を暗黙に「存在しないもの」として扱わない。

### 2.3 過去snapshotを遡及改変しない

過去の監査結果、snapshot、評価履歴は、その時点の対象と規則を示す記録として保持する。

後から再評価した場合は、新しいrecordを追加する。

---

## 3. Proposition Extraction / 命題抽出

### 3.1 抽出対象

監査対象となる命題には、少なくとも次を含みうる。

- 定義
- 記述
- 外部体系の紹介
- 解釈
- 類比
- 構造対応
- 仮説
- 一般化
- 因果・機構候補
- 規範
- 処方
- 公開判断
- 運用規則
- 非主張境界

### 3.2 非命題を無理に命題化しない

索引、見出し、読解順、純粋なリンク、書誌情報などは、必要がなければ主張命題として扱わない。

ただし、それらが権威、優先順位、正本関係、概念所有を実質的に規定している場合は監査対象にする。

### 3.3 原文を保持する

抽出時に、評価しやすい言い換えへ先に変形しない。

最低限、次を分ける。

```yaml
proposition:
  id: ""
  source_path: ""
  location: "section / line / anchor"
  source_text: ""
  normalized_statement: "optional"
```

`normalized_statement`は検索・比較の補助であり、`source_text`を置き換えない。

---

## 4. Attribution / 帰属監査

帰属監査は、Claim Strengthその他の高次評価より先に行う。

### 4.1 production relation と represented positionを分ける

「repositoryが文章を書いた」と「repository自身の立場を述べている」を同一視しない。

たとえば、repositoryが自分で書いた文章で外部理論を説明している場合、文章はrepository-authoredでも、命題はexternal positionをrepresentしている。

最低限、次を記録する。

```yaml
attribution:
  textual_producer: "repository / external_source / mixed / unknown"
  represented_position: "repository / named_external_source / external_domain / mixed / indeterminate"
  source_owner: "path / citation / authority / unknown"
  representation_type: "direct_quote / paraphrase / summary / reconstruction / original"
```

### 4.2 repository commitmentを別軸で記録する

命題がrepository本文に存在することだけでは、repositoryのendorsementにならない。

最低限、次を区別する。

| Relation | 意味 |
|---|---|
| `represented` | 外部体系・話者・立場を表象する。repositoryの真理コミットメントを自動的に含まない。 |
| `endorsed` | repositoryが、その命題を自らの立場として採用する。 |
| `derived` | repositoryが、source・前提・独自規則から新しい命題を導出・提案する。 |
| `rejected` | repositoryが命題を否定・不採用として扱う。 |
| `suspended` | 現時点では採否を保留する。 |
| `indeterminate` | 文面からcommitmentを確定できない。 |

一つの命題が複数関係を持つ場合、無理に一つへ圧縮しない。

例：外部命題をrepresentedしつつ、その一部をendorsedする場合がある。

### 4.3 source claimとrepository claimを分ける

```text
source claim
  !=
repository representation of source claim
  !=
repository-derived bridge claim
```

外部sourceが強い科学的、哲学的、法的、制度的主張を行っていても、その強さをそのままSOのClaim Strengthへ移さない。

SOが「この外部命題とSO概念は対応する」「この外部成果はSOを支持する」と述べた場合、その接続命題はrepository-owned claimとして別に評価する。

### 4.4 帰属不能を保持する

誰の命題か確定できない場合、推測で埋めず`indeterminate`として残す。

帰属不明は監査上のfindingになり得るが、それだけで命題が偽であることを意味しない。

---

## 5. Responsibility, Phase, and Scope / 責任・位相・範囲

### 5.1 責任主体

各命題について、誰がその命題の正当化、更新、撤回、公開、運用を引き受けるかを可能な範囲で記録する。

```yaml
responsibility:
  claim_owner: ""
  definition_owner: "optional"
  evaluation_owner: "optional"
  publication_owner: "optional"
  operational_owner: "optional"
```

これらは同一主体である必要はない。

### 5.2 位相を分ける

最低限、次の位相を混同しない。

- observation / 観測
- citation / 引用
- representation / 表象
- description / 記述
- interpretation / 解釈
- evaluation / 評価
- hypothesis / 仮説
- generalization / 一般化
- prescription / 処方
- decision / 決定
- execution / 実行

位相を移る場合、その変換を担う主体と規則を可能な範囲で記録する。

### 5.3 適用範囲

命題がどの対象、条件、時間、制度、文脈、言語ゲームに適用されるかを記録する。

局所命題を無標識に一般命題へ広げない。

```yaml
scope:
  target: ""
  conditions: []
  exclusions: []
  time_scope: "optional"
  domain_scope: "optional"
```

---

## 6. Warrant Path / 根拠経路

### 6.1 claim ownerが根拠責務を持つ

ある命題をrepositoryがendorsedまたはderivedする場合、その命題を支えるwarrantを示す責務はrepository側にある。

異議側は、必ずしも完全な対抗理論を提出する必要はない。

「そのwarrantからその結論は導けない」という異議は、接続の妥当性を問題化するために成立し得る。

### 6.2 根拠系列を必要な範囲で辿る

監査は無限後退を要求しない。

記録するのは、現在の議論・文書がどこで根拠系列を停止しているかである。

停止点の候補例：

- observation / 観測
- definition / 定義
- methodological premise / 方法上の前提
- institutional authority / 制度上の権限
- domain standard / 分野標準
- value choice / 価値選択
- practical purpose / 実務目的
- linguistic rule / 言語使用上の規則
- provisional assumption / 暫定仮定
- unresolved / 未解決

この一覧は最終的な哲学分類ではない。

### 6.3 停止点を偽装しない

根拠系列が定義、権威、価値、便宜、仮定で止まっている場合、それを観測事実、証明、普遍的合意として表現しない。

### 6.4 外部権限依存

外部領域の権威、実証成果、数学、法令、制度標準をwarrantとして使用する場合、少なくとも次を確認する。

- その外部sourceは何を実際に支持しているか。
- repositoryのbridge claimはsourceから導出されるか。
- sourceの権威が、中間変換を飛び越えてSO側の命題へ流入していないか。
- source側から見て、接続の修正・拒否が可能か。

```text
source exists
  !=
derivation established
```

---


### 6.5 Ground Search / 根拠探索経路

監査は、提示された根拠の一覧を見るだけでなく、**その根拠へどう到達したか**を必要に応じて監査する。

ここでいうGround Searchは、究極的な形而上学的根を必ず発見することを意味しない。repository運用上は、少なくとも次を含む。

```text
claim
  -> immediate warrant
  -> source / record / rule
  -> upstream source, event, decision, or observation
  -> current stop point
```

重要なのは、記録が対象の履歴へ実際に遡及できることである。

監査用に整えられた説明、後付けの要約、二次資料、権威的な解説が存在していても、それだけで元の出来事、判断、source、測定、定義へ接続しているとはみなさない。

必要な場合、次を記録する。

- そのsourceへ進んだ理由。
- 一次資料か、二次資料か、再構成資料か。
- 複数sourceが実際には同じ上流sourceを共有していないか。
- 定義を探しているのに事例へ、因果根拠を探しているのに類似へ、観測根拠を探しているのに権威へ逸れていないか。
- どこで探索を止めたか。
- なぜそこを現在のstop pointとしたか。
- contemporaneous traceか、after-the-fact reconstructionか。

根拠を深く辿っているように見えて、実際には同じ枝の中を移動しているだけの場合がある。この状態を、探索深度の増加とみなさない。

### 6.6 根拠系列の独立性

異なる命題、異なる文書、異なる分野名が、実際には同じ上流の根拠系列へ遡及する場合、その一致を独立した相互支持として二重計上しない。

```text
shared upstream root
  -> claim A
  -> claim B

A agrees with B
  !=
independent corroboration
```

特に、外部概念をSOが借用・再構成した後、その借用元の概念を再びSO命題の独立証拠として用いる場合は、循環またはauthority launderingが起きていないか確認する。

評価対象は権威の数ではなく、根拠へ至る経路の完全性、系列の独立性、途中のCut / False Link / attribution error / scope leap / unsupported transformationである。
## 7. Judgment Transparency Topology / 判断透明性トポロジー

Topology auditは、主張の真偽を直接判定するものではない。

判断・接続・変換が後から追跡、異議、改訂可能な形で構成されているかを確認する。

### 7.1 Anchor Integrity / 接点整合性

確認する問い：

- 判断は何に接触しているか。
- source、対象、命題、話者、定義所有者、権限を別のものへすり替えていないか。
- source claimとrepository claimを混同していないか。
- 帰属が不明なのに確定扱いしていないか。

### 7.2 Phase Integrity / 位相整合性

確認する問い：

- 観測から解釈へ無標識に飛んでいないか。
- 表象からendorsementへ飛んでいないか。
- 解釈から一般化、処方、実行へ飛んでいないか。
- 変換主体と規則が追跡可能か。

### 7.3 Path Legibility / 経路可読性

確認する問い：

- 結論へ至る途中で何を保持したか。
- 何を変換、要約、圧縮、翻訳、分類したか。
- 何を捨象したか。
- どのwarrantがどの命題を支えているか。
- 中間変換を後から再構成できるか。

### 7.4 Return Reachability / 返路実効性

確認する問い：

- 異議、反例、失敗、追加データをどこへ返せるか。
- 返送先は実際に本文、判断、運用を変更できるか。
- 受付窓口だけ存在し、変更権限がない状態になっていないか。
- 外部体系側にも拒否・修正・再送の権利が残っているか。

### 7.5 Open-End Retention / 開放端保持

確認する問い：

- 未解決、反例、理解不能、通約不能、解釈差を保持できるか。
- 残差を理論の成功材料へ自動変換していないか。
- 「まだ分からない」を「理論が深い証拠」にしていないか。
- 仮閉鎖なら、再開条件と返路が残っているか。

### 7.6 五軸を完全分類とみなさない

Anchor / Phase / Path / Return / Open-Endは現時点の再利用可能な監査インターフェースである。

判断透明性の全条件を網羅すると主張しない。

五軸で局在化できない異常は`Unresolved`として保持する。

---

## 8. Primitive Deviation / 生の逸脱

詳細な失敗分類を先に要求しない。

まず生の異常を記録する。

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

その後、必要な場合だけ次のprimitiveを付与する。

| Primitive | 意味 |
|---|---|
| `Cut` | 必要な接続、返路、中間根拠、責任経路が切れている。 |
| `False Link` | 保証されていない対象、主体、位相、範囲が接続済みとして扱われる。 |
| `Both` | CutとFalse Linkが同時に起きる。 |
| `Unresolved` | 現在の情報では上記へ確定できない、または上記で十分に記述できない。 |

原則は次である。

```text
detect
  -> preserve
  -> optionally classify
```

分類できたことを、異常が解消したこととみなさない。

誤帰属、位相跳躍、範囲漏出、経路消去、返路切断、偽閉鎖等はnamed patternとして使用できるが、網羅的taxonomyとはしない。

---

## 9. Reciprocal External Connection Audit / 相互外部接続監査

外部理論、学問、制度、技術、文化的語彙、既存専門語と接続する場合、外部体系をSOの上位審級として扱わず、SOを外部体系の上位解釈者としても扱わない。

双方は、それぞれ自分の内部命題について固有の根拠系列と評価規則を持つ独立した接続主体として扱う。

```text
A. domain-authoritative or source-grounded description
B. repository representation / reconstruction
C. SO-derived interpretation or connection claim
```

Aは絶対真理層ではない。

どのsource、標準、専門家、institution、interpretive traditionに依存するかを保持する。

主としてA->B、B->Cの変換を監査し、必要に応じてA->C authority bypassを確認する。

### 9.0 Reciprocal Revisability / 相互修正可能性

接続の妥当性は、一方が他方を勝って解釈できることではなく、双方が互いの差分を保持したまま訂正・拒否・再接続できることによって監査する。

最低限、次を確認する。

- 外部領域の内部命題を、SOが勝手に所有・再定義していないか。
- SO内部の命題を、外部領域の方法だけで自動的に無効化していないか。
- bridge claimを提出した主体が、そのbridgeの根拠と変換責任を引き受けているか。
- 相手側からの訂正が、形式的受付ではなく実際に接続命題を変更し得るか。
- 相手側が接続を拒否しても、その拒否を「理解不足」として回収しないか。
- SO側からも、相手の内部命題そのものではなく接続条件について問い返せるか。

相互修正可能性は、相互同意や共栄の成立を要求しない。共栄は結果として成立し得るが、監査条件はまず、双方が修正・拒否・再接続可能であることである。

### 9.1 Assessment Contact Contract / 接触評価契約

異体系の接触では、最初から「どちらが正しいか」を一つの尺度で判定しない。

まず、各体系が何を仕事としているか、その体系内で何が成立・妥当・正当とされるか、比較可能な接触面をどこまで共有できるかを確認する。

本Protocolでは、この入口を次の三つの操作名で呼ぶ。

- `SYSTEM-ROLE-IDENTIFICATION` — 対象体系が何を仕事としているかを同定する。
- `VALIDITY-REGIME-IDENTIFICATION` — その体系が何をもって成立・妥当・正当とするかを同定する。
- `COMMENSURATION-INTAKE` — claim / fact / interpretation / derivation / bridge claimを区別できる接触面を共有できるか確認する。

`VALIDITY-REGIME-PRESERVATION`を横断原則とする。

> 評価対象体系の妥当性条件を、別体系の妥当性条件へ無標識に置換しない。

体系`X`におけるclaim `c`の妥当性条件を`V_X(c)`と書くとき、`V_X(c) != V_Y(c)`であるにもかかわらず、`V_Y(c)`だけを用いて`X`のclaimを失効させてはならない。

ただし、妥当性体系が異なることは、事実衝突、参照誤記、安全上の制約、法的権限、測定上の制約を無効化しない。異なるのは「何をどう判定するか」であり、相互接触を免除する理由ではない。

外部接続を裁定する前に、可能な範囲で次を接触面へ出す。

```yaml
contact_surface:
  system_role: ""
  validity_regime: ""
  claim: ""
  scope: ""
  warrant: []
  target: ""
  fact_set: []
  interpretation: "optional"
  bridge_claim: "optional"
```

原則として、通約可能な接触面が成立していない状態から、対象命題の勝敗判定へ飛ばない。

> **No object-level adjudication before a commensurable contact surface has been established.**

これは、すべての体系が同じ価値・証拠形式・目的を採用しなければならないという意味ではない。`COMMENSURATION-INTAKE`の成功は同意ではなく、差分を差分として比較できる最低限の接触成立を意味する。

#### 9.1.1 Canonical Finding Types / 基本finding型

以下は序列ではない。一つのclaimに複数findingが同時に成立し得る。

記号は次を用いる。

- `H` — 評価対象のSO claim / hypothesis
- `X` — 接触している外部体系
- `Γ_X` — 外部体系`X`の前提・理論・導出系
- `F_X` — `X`において当該scopeで確立している事実集合
- `Γ_SO` — SO内部の前提・モデル・導出系
- `Est_X(H)` — `X`が`H`をestablishedとしている
- `Def_SO(H)` — SO内部で`H`に対する有効なdefeaterへ到達している
- `I_phi(F)` — 同じ事実集合`F`を位相・座標`phi`から読むinterpretation
- `B_{A->B}` — 体系`A`から体系`B`へ伸びるbridge claim

| Canonical code | machine key | 日本語名 | 関係表記 | 標準初手 |
|---|---|---|---|---|
| `EXT-UNESTABLISHED` | `external_unestablished` | 外部未確立 | `not Est_X(H)` | `KEEP-OPEN` |
| `EXT-NONDERIVABLE` | `external_nonderivable` | 外部非導出 | `Γ_X ⊬ H` | `KEEP-OPEN` |
| `EXT-FACT-CONFLICT` | `external_fact_conflict` | 外部既知事実衝突 | `Cons(F_X ∪ {H}) = false` | `BOUNDARY-AUDIT` |
| `SO-NONDERIVABLE` | `so_nonderivable` | SO内部非導出 | `Γ_SO ⊬ H` | `INTERNAL-TRACE` / `BOUNDARY-AUDIT` |
| `SO-DEFEATER` | `so_defeater` | SO内部defeater到達 | `Def_SO(H)` | `REOPEN-SO` |
| `EXT-REFERENCE-MISSTATEMENT` | `external_reference_misstatement` | 外部参照誤記 | `Rep_SO(q_X) ≢ q_X` | `CORRECT-REFERENCE` |
| `SAME-FACT-ALT-INTERPRETATION` | `same_fact_alternate_interpretation` | 同一事実・異位相解釈 | `I_{phi_SO}(F) != I_{phi_X}(F)` | `COMMENSURATION-INTAKE` |
| `RECIPROCAL-BRIDGE-DISPUTE` | `reciprocal_bridge_dispute` | 相互bridge係争 | `Dispute(B_{SO->X}, B_{X->SO})` | `COMMENSURATION-INTAKE` |

旧A–H表記は会話・移行参照に使用できるが、公開本文・machine keyでは上記canonical nameを用いる。

#### 9.1.2 禁止する短絡

`EXT-UNESTABLISHED`は「外部体系で現在確立していない」ことを示す。これはfalsifiedを意味しない。

```text
not Est_X(H)
  != Γ_X ⊢ ¬H
  != falsified(H)
```

`EXT-NONDERIVABLE`と`SO-NONDERIVABLE`は非導出であり、否定ではない。

```text
Γ_X ⊬ H  !=  Γ_X ⊢ ¬H
Γ_SO ⊬ H !=  Γ_SO ⊢ ¬H
```

`SO-NONDERIVABLE`が問題となる強さは、SO自身が「導出済み」と主張していたかどうかで変わる。Research Notes上の明示されたhypothesisがSO内部から未導出であることだけを理由に、撤回・非公開・反証済みへ移さない。

`SO-DEFEATER`は最優先の再検討triggerであるが、即時の全面撤回と同義ではない。scope、前提、undercutter、rebutter、局所修正可能性を再検査する。

`EXT-REFERENCE-MISSTATEMENT`は、外部体系の事実・定義をSOが誤記した場合である。これはまずSO側の参照表現を局所修正し、その後にbridge claimまたはSO hypothesisを再評価する。

`SAME-FACT-ALT-INTERPRETATION`は、標準定義または共有事実を保持したうえでinterpretive phaseが異なる場合である。`EXT-REFERENCE-MISSTATEMENT`と同一視しない。

#### 9.1.3 First Response Modes / 標準初手

findingとresponseを同じ軸にしない。findingは何が観測されたか、responseは最初にどの処理へ進むかを示す。

| Response mode | 役割 |
|---|---|
| `KEEP-OPEN` | 未確立・非導出を残差として保持し、否定や撤回へ飛ばない。 |
| `BOUNDARY-AUDIT` | referent、scope、measurement condition、semantic phase、bridge responsibilityを再確認する。 |
| `INTERNAL-TRACE` | SOがどの前提・履歴・生成経路からclaimを提出したかを追跡する。 |
| `REOPEN-SO` | SO側claim、scope、前提、上流モデルを再検討対象へ戻す。 |
| `CORRECT-REFERENCE` | 借用した外部事実・定義のSO側表現を先に修正する。 |
| `COMMENSURATION-INTAKE` | fact / interpretation / derivation / bridge claimを区別できる比較面の成立を確認する。 |

標準初手は最終dispositionではない。同じfindingでも、監査後に`local correction / keep open / scope revision / bridge return / unresolved / withdrawal`等へ分岐し得る。

#### 9.1.4 Bridge Overreach / 被越境検知

`EXT-FACT-CONFLICT`または`SO-NONDERIVABLE`を検知しただけで、どちらか一方の体系全体を失効させない。

まず、そのfindingから相手体系へ伸びる追加のbridge claimが存在するかを確認する。

例：`F_X`が局所事実として成立していても、`F_X => not H`をSO全体へ伸ばすには別のbridge warrantが必要である。

bridge claimの越境候補は、少なくとも次を区別する。

- `SCOPE-OVERREACH` — 局所scopeを超えて結論を伸ばす。
- `CRITERION-OVERREACH` — 一方のvalidity regimeを他方の唯一の成立条件として置換する。
- `WARRANT-OVERREACH` — sourceまたはauthorityが支える範囲を超えてwarrantを流入させる。
- `DEFINITION-OVERREACH` — 一方の内部定義を相手体系の定義所有へ無標識に拡張する。

これらは、外部体系を自動的に誤りとするためのラベルではない。SO側から外部へ伸びるbridgeにも同じ監査を適用する。

#### 9.1.5 Engagement Capacity / 関与能力境界

評価、反論、探索、通約には有限の時間、注意、計算、身体、制度、アクセス、権限等を要する。

必要資源を`K_A(q)`、時点`t`で主体または体系`A`が利用可能な関与資源を`C_A(t)`とすると、`C_A(t) < K_A(q)`であるために非関与が生じることがある。

この状態を`ENGAGEMENT-CAPACITY-LIMIT`と呼び、その標準応答を`NONADJUDICATIVE-NONENGAGEMENT`とする。

```text
not Engage_A(q, t)
  != A ⊢ ¬q
  != A ⊢ q
  != Def_A(q)
```

したがって、応答不能、探索停止、議論打切りを、同意・否定・敗北・defeaterとして自動記録しない。

理由は次のように記録できるが、説明を強制しない。`unspecified`を有効値として認める。

```yaml
engagement:
  condition: "engagement_capacity_limit / none / unresolved"
  response: "nonadjudicative_nonengagement / continue / other"
  reason: "resource_limit / time_limit / attention_limit / competence_boundary / access_limit / safety_boundary / role_boundary / voluntary_decline / unspecified"
  duration: "temporary / indefinite / terminal / unspecified"
```

このexit boundaryは監査のどの段階でも発生し得る。非関与が再開可能かどうかも、無理に確定しない。

### 9.2 Connection Exposure / E

Eは「批判されやすさ」や「真理性」を表す尺度ではない。

repositoryが外部体系へどの程度強い接続を行っているかを示す補助投影である。

| Code | 意味 |
|---|---|
| `E0` | repository内部の自己所有概念・運用で、外部権限への依存がほぼない。 |
| `E1` | 外部概念を、owner、source meaning、非同一性を保持して輸入・参照する。 |
| `E2` | cross-system reinterpretation、commensuration、structural mapping、bridge claimを行う。 |
| `E3` | authority laundering、identity、strong causality、replacement、universalization、strong reificationの危険または主張を含む。 |

Eは外部source自身の強さではなく、repositoryが作る接続の性質から判定する。

Eが高いことは、外部体系よりSOが弱いこと、またはSOが強いことを意味しない。Eは、接続命題がより強い変換責任と相互修正可能性を必要とすることを示す。

### 9.3 接続成立と統合を分ける

接続候補を提示することは、外部体系をSOへ統合することではない。

最低限、次を保持する。

- source側の内部定義
- repository側の再構成
- 非同一性
- 接続を担う主体
- 中間規則
- 双方の拒否・修正可能性
- 未変換残差

### 9.4 外部語彙の詳細責任

既存専門語を借用する場合の詳細な「なぜ使うか」「どう使うか」「どこが違うか」「なぜ保持するか」「借り元へ何を返せるか」は、Terminology Connection / Return governanceへ委ねる。

ただし、本Protocolでは、借用時の基本姿勢として次を要求する。

- 借り元の定義、用法、warrantを先に保持する。
- SO側の再解釈を、借り元の本来の意味への勝利や深層解釈として扱わない。
- 非同一性を必要な範囲で明示する。
- なぜ既存語を使い続けるのかを説明できるようにする。
- 借り元からの訂正・拒否を受け取れる返路を残す。
- SO側の利用から借り元へ返せる問い、比較、観測候補がある場合は、それをbridge claimとして責任主体とともに示す。

これは単なる礼儀規則ではない。借用語を通じた接続が、片方向の意味回収やauthority launderingへ変質していないかを監査するための条件である。

本Protocolでは、それらの記録が必要な接続で欠落していないかを監査する。

---

## 10. Claim Strength / S

### 10.1 Sが測るもの

Sは、repositoryが自ら引き受ける命題の**コミットメント強度**を短く表示する補助投影である。

Sは次を意味しない。

- 真理性
- 成熟度
- 検証済み度
- 重要度
- 公開価値
- 人気
- 形式化の進行度

### 10.2 Sを付ける対象

原則として、repositoryが`endorsed`または`derived`する命題を評価する。

単に`represented`された外部命題へ、repository自身のSを付与しない。

外部命題の強さを記録する必要がある場合は、source側のclaim postureとして別に記録し、SO側Sと混同しない。

### 10.3 暫定S定義

| S | Repository commitment |
|---|---|
| `S0` | 用語、分類、記録、索引、運用上の約束。対象世界について強い実在・因果主張を行わない。 |
| `S1` | 限定された記述、アナロジー、ヒューリスティック。適用範囲を超えた存在論的同一性を要求しない。 |
| `S2` | 宣言された枠内での再解釈、概念モデル、操作モデル。枠外への一般化を自動的に含まない。 |
| `S3` | 条件付きの一般構造、関係、反復パターンをrepositoryの命題として提案する。 |
| `S4` | 異体系間対応、機構、生成関係、因果候補など、外部対象へ強い説明関係を提案する。 |
| `S5` | 同一性、普遍性、強い外部実在、強因果、確立領域の置換・競合など、最も強いrepository commitmentを行う。 |

この定義は、旧`Claim_Strength_and_Publication_Layer_Table`の「命題タイプ」「形式化段階」「公開レイヤー」をSへ混在させないための再設計である。

### 10.4 語彙だけでSを決めない

「存在」「物理」「因果」「実在」「公理」「量子」などの語が含まれることだけでSを上げない。

反対に、平易な語で書かれていても、実質的に普遍性、同一性、因果、置換を主張していれば高S候補になる。

### 10.5 文書単位のSは投影である

Sの一次単位は命題である。

文書一覧やNavigatorで要約が必要な場合、次のような派生値を生成してよい。

```yaml
claim_projection:
  s_core: "main repository commitment"
  s_max: "maximum endorsed/derived claim strength"
```

`S_max`はrepresented external claimの強さを含めない。

文書単位のSが本文の多様な命題を上書きしてはならない。

---

## 11. Use, Publication, Maturity, Evaluationを分離する

### 11.1 Use / Safety

誤用、操作、プライバシー、安全、制度的影響等は、Claim Strengthと別に評価する。

高Sだから危険とは限らず、低Sでも高い運用リスクを持ちうる。

Uコード等の詳細な公開安全分類は、Publication / Safety governanceへ委ねる。

### 11.2 Publication

公開可否、減速、抽象化、非公開、分割は、命題の真理性とは別の判断である。

Publication and Commensuration Policyに従う。

### 11.3 Maturity

文書の安定性、変更可能性、レビュー可能性を示す。

Maturityは真理性、普遍性、重要性、Claim Strengthを意味しない。

### 11.4 Verification scalarを監査本体にしない

概念整合、反例照合、形式化、実験、外部レビュー、シミュレーションは異なる評価方法であり、必ずしも一本道ではない。

したがって本Protocolでは、旧Vコードを監査の一次軸にしない。

評価は履歴として保持する。

### 11.5 Rendering Distance scalarを監査本体にしない

特定分野、言語ゲーム、形而上学からの「距離」を固定Rコードで序列化しない。

接触時のlocal interface、external connection、Terminology Connection recordとして扱う。

---

## 12. Evaluation History / 評価履歴

評価は「現在の正解値」だけでなく、何を、なぜ、どう検査し、何が見え、何が残ったかを保持する。

最低限、次の形式を推奨する。

```yaml
evaluation_record:
  id: ""
  date: YYYY-MM-DD
  target: "document / section / proposition / relation"
  source_commit: ""
  protocol: ""
  evaluator: "human / model / mixed"
  reason: ""
  mode: []
  method: ""
  evidence: []
  observed: ""
  assessment: ""
  recommendation: ""
  human_decision: "pending / approve / edit / reject / hold"
  residuals: []
  return_points: []
  next_action: "optional"
```

### 12.1 observed / assessment / decisionを分ける

- `observed`: 何が実際に観測されたか。
- `assessment`: その観測をどう解釈したか。
- `recommendation`: 評価者が何を勧めるか。
- `human_decision`: repository ownerが何を決めたか。

これらを一文に圧縮しない。

### 12.2 評価modeは序列ではない

例：

- conceptual_consistency
- cross_document_consistency
- attribution_review
- topology_audit
- counterexample_review
- external_mapping
- commensuration_review
- constructive_test
- controlled_comparison
- operational_evaluation
- formalization
- simulation
- empirical_evaluation
- external_review
- publication_review

対象に必要な方法を選ぶ。

高いmode、低いmodeという序列にしない。

---

## 13. 監査findingの書き方

findingは、対象を即時に有罪・無効とする判決ではない。

最低限、次を分ける。

```yaml
finding:
  id: ""
  type: "optional canonical finding type"
  impact_class: "blocking / structural / terminological / editorial / unresolved"
  target: ""
  observation: ""
  affected_topology: []
  primitive_deviation: "Cut / False Link / Both / Unresolved / none"
  assessment: ""
  evidence: []
  response:
    first_action: "keep_open / boundary_audit / internal_trace / reopen_so / correct_reference / commensuration_intake / other"
    note: ""
  recommendation: ""
  return_point: ""
```

`type`は9.1のcanonical finding typeを必要な場合に記録する。すべてのfindingをA–H型へ押し込まない。

`impact_class`は真理性や誤りの序列ではなく、repository運用上どの責務・境界へ影響するかを表す処理分類である。`SO-DEFEATER`や`EXT-REFERENCE-MISSTATEMENT`のように標準初手が優先されるfindingがあっても、それを「より悪い誤り」という単一順位へ変換しない。

### 13.1 Blocking

意味、権威、安全、公開適格性、概念所有、重大な帰属を変える問題。

### 13.2 Structural

役割、配置、依存方向、scope、責任、返路、metadata構造の問題。

### 13.3 Terminological

名称、定義所有、通約、外部語彙接続、非同一性の問題。

### 13.4 Editorial

意味を変えない表記、可読性、形式の問題。

### 13.5 Unresolved

現在の分類・証拠では局在化できない差分。

`Unresolved`を低重要度とみなさない。

---

## 14. 監査深度と起動条件

すべての文書を常時同じ深度で監査しない。

ただし、監査可能性は保持する。

深度監査を優先する条件：

- 正本またはrepository-wide governanceの変更
- concept ownerの変更
- 高いrepository commitment
- E2-E3の外部接続
- 外部専門領域の権威をwarrantとして使用
- 因果、機構、普遍性、同一性、置換主張
- 公開・非公開境界の変更
- 安全、法、制度、医療、金銭、人格等への高影響応用
- 複数文書で定義競合が生じた場合
- Navigatorまたはmanifestが本文と不一致を起こした場合
- 異議、失敗、反例、新しい実験結果がReturnとして到着した場合

単純な表記修正や明白なリンク修正に、同じ深度の哲学監査を要求しない。

---

## 15. Cross-document Audit / 文書間監査

単一文書内の整合だけでなく、repository graphとして確認する。

### 15.1 Identity

- title
- filename
- language relation
- path
- status

### 15.2 Ownership

- public definition owner
- canonical owner
- imported concept owner
- document-local definition

一概念に複数のcanonical ownerを無標識に置かない。

### 15.3 Dependency

- imports
- exports
- prerequisites
- derived relations
- return paths

依存方向が逆転していないか確認する。

### 15.4 Index / Navigator projection

README、System Map、Concept Network、manifest、graph、Navigatorは、本文の意味を再定義しない。

表示側が本文より強い主張を作っていないか確認する。

### 15.5 Historical compatibility

過去releaseの文書を読むために必要な旧語彙・旧分類は、Git history、migration note、Superseded record等で追跡可能にする。

現行正本へ旧規則を残し続けることだけを互換性としない。

---

## 16. Commensuration Audit / 通約監査

英語通約その他の再構成では、単なる語の一致ではなく、次を確認する。

- central question
- proposition responsibility
- concept ownership
- relation structure
- warrant
- claim strength
- non-claim boundary
- closure condition
- residual
- return path

通約によって説明しやすくなったことを、同意・同一性・証明とみなさない。

通約不能部分を自然な表現で隠さない。

外部体系の語彙を借りる場合は、Terminology governanceへ接続する。

---

## 17. Self-Audit / SO Capture防止

存在境界論自身も一つの認識形式である。

監査時には、少なくとも次を確認する。

- 何でも境界語彙へ変換していないか。
- 類似を同一性へ昇格させていないか。
- 研究ノートを確立した正本として使っていないか。
- SOの語彙が説明を増やさず、単なる再命名になっていないか。
- 未解決を過剰に保持し、必要な結論まで回避していないか。
- 単純な実装を監査構造で複雑化していないか。
- SOなし対照条件の方が良い場合、その差を保持できるか。
- 外部体系がSOを拒否・修正する権利を残しているか。
- SO側のbridge motiveを外部体系自身の主張として偽装していないか。

新規性または影響の大きい判断では、可能なら次を確認する。

> 存在境界論を知らなくても、この結論を推奨するか。

SOに依存する部分は、domain factではなくSO由来の解釈、接続候補、仮説として標識する。


### 17.1 Audit Capture / 監査捕獲

監査系が整備されるほど、監査可能なものだけを対象として選び、監査結果が良く見えるように対象、記録、分類、履歴を変形する危険がある。

少なくとも次を自己監査する。

- チェック可能なものだけを重要視していないか。
- 記録可能なものだけを残し、命名不能な異常を捨てていないか。
- 指標やチェック項目を改善するために、対象そのものを変形していないか。
- 監査用資料が、実態への接続より表示上の整合を優先していないか。
- 「監査済み」「全項目記入済み」を「妥当」「安全」「真」と読み替えていないか。
- 外部評価へ通す圧力が、内部反省のための監査を展示技術へ変えていないか。
- 監査に不都合な履歴が、後から遡及不能になるよう切断されていないか。

本Protocolでは、この傾向を作業上 **「ソフィストの法則」** と呼ぶことがある。

> 賢くなることより、賢く見せる技術の方が先に発達することがある。

これは普遍法則の主張ではない。監査、評価、公開、認証の圧力によって、対象改善より表示改善が最適化される危険を短く指すための警告語である。

### 17.2 実態への遡及を監査資料より優先する

監査artifactが存在することと、対象の履歴へ遡及可能であることを分ける。

```text
audit artifact
  -> operational trace
  -> original event / decision / source
```

この経路が切れている場合、資料の完成度で補完しない。

- 同時期の記録は`contemporaneous trace`として扱いうる。
- 後から復元した説明は`reconstructed after the fact`として標識する。
- 元履歴へ接続できない場合は`trace unavailable / unresolved`として残す。

後付け再構成それ自体を不正とみなさない。ただし、同時記録と同じ証拠強度へ無標識で昇格させない。

---

## 18. AIによる監査

AIは監査補助者として、命題抽出、帰属候補、矛盾候補、Topology finding、比較、return candidate、metadata mismatchを提案できる。

AIはrepositoryの最終判断主体ではない。

### 18.1 AIがしてよいこと

- 監査fixtureの準備
- 命題抽出
- source / represented positionの候補提示
- commitment ambiguityの検出
- topology audit
- raw anomaly logの生成
- S/E候補と根拠の提示
- cross-document consistency check
- migration candidateの提示
- human review用diffの生成

### 18.2 AIが自動でしてはならないこと

- canonical ownerの無承認変更
- 正本本文の自動改稿
- 研究仮説の正本化
- represented external claimのendorsement化
- unresolved findingの自動閉鎖
- 公開・非公開境界の無承認変更
- Claim Strengthを真理順位として表示すること

### 18.3 人間のreview action

標準的なreview actionは次とする。

- `approve`
- `edit`
- `reject`
- `hold`

AI提案を採用しないこと自体を監査失敗とみなさない。

---

## 19. 最小監査手順

正本または重要文書を監査する場合、最低限次を行う。

### Step 0: Fixture

対象commit、path、目的、除外範囲を固定する。

### Step 1: Proposition

対象命題を抽出する。

### Step 2: Attribution

textual producer、represented position、source ownerを確認する。

### Step 3: Commitment

represented / endorsed / derived / rejected / suspended / indeterminateを記録する。

### Step 4: Responsibility / Phase / Scope

誰が何をどの範囲で引き受けるかを確認する。

### Step 5: Warrant

根拠、外部権限依存、現在の停止点を記録する。

### Step 6: Contact Contract

外部接続がある場合、system role / validity regime / commensuration intakeを確認し、必要なら9.1のcanonical finding typeを付与する。関与能力境界が生じた場合は、非判定的非関与として記録する。

### Step 7: Topology

Anchor / Phase / Path / Return / Open-Endを監査する。

### Step 8: Raw anomaly

異常があれば、生ログを先に残す。

### Step 9: Primitive deviation

必要ならCut / False Link / Both / Unresolvedを付与する。

### Step 10: Downstream projection

必要な場合だけS / E、use/safety、publication、metadata等へ投影する。

### Step 11: Recommendation

修正、保持、分割、移動、追加検証、外部照合、hold等を提案する。

### Step 12: Human decision

approve / edit / reject / holdを人間が決定する。

### Step 13: Return

変更結果、異議、反例、失敗、運用結果を後続評価へ返せるよう記録する。

---

## 20. 最小監査記録テンプレート

```yaml
repository_assessment:
  audit_id: ""
  source_commit: ""
  target:
    path: ""
    location: ""
    proposition_id: ""
    source_text: ""

  attribution:
    textual_producer: ""
    represented_position: ""
    source_owner: ""
    representation_type: ""

  commitment:
    relations: []
    repository_owned: false
    note: ""

  responsibility:
    claim_owner: ""
    definition_owner: ""

  phase:
    current: ""
    transition: ""

  scope:
    target: ""
    conditions: []
    exclusions: []

  warrant:
    immediate: []
    external_authority: []
    stop_point: ""
    unresolved: []

  topology:
    anchor: "intact / strained / failed / unresolved"
    phase: "intact / strained / failed / unresolved"
    path: "intact / strained / failed / unresolved"
    return: "intact / strained / failed / unresolved"
    open_end: "intact / strained / failed / unresolved"

  contact_contract:
    system_role: "optional"
    validity_regime: "optional"
    commensuration_intake: "not_applicable / established / partial / failed / unresolved"
    bridge_claims: []

  findings:
    - type: "optional"
      observation: ""
      first_action: "optional"

  engagement:
    condition: "none / engagement_capacity_limit / unresolved"
    response: "continue / nonadjudicative_nonengagement / other"
    reason: "optional / unspecified"
    duration: "temporary / indefinite / terminal / unspecified"

  anomaly:
    observed: ""
    affected_nodes: []
    expected_path: ""
    observed_path: ""
    possible_cut: ""
    possible_false_link: ""
    named_pattern: "optional"
    unresolved_difference: ""
    return_point: ""

  projections:
    claim_strength_s: "optional"
    connection_exposure_e: "optional"
    use_safety: "defer / optional"
    publication: "defer / optional"

  assessment:
    impact_class: ""
    interpretation: ""
    recommendation: ""
    residuals: []

  review:
    human_decision: "pending / approve / edit / reject / hold"
    decision_note: ""
    next_return: ""
```

このテンプレートはcanonical schemaではない。

pilot auditによって冗長、欠落、誤分類が見つかった場合、Policyとともに改訂する。

---

## 21. Protocol Sufficiency Test / プロトコル十分性

新しい監査規則は、同じ対象を別の評価者、別のLLM、別時点へ渡したとき、少なくとも判断経路の差を比較できる程度に自立していなければならない。

完全一致は要求しない。

要求するのは、差が次のどこから生じたかを追跡できることである。

- source interpretation
- attribution
- commitment assignment
- scope
- warrant
- topology
- external domain rule
- evaluator assumption
- protocol ambiguity

### 21.1 hidden policy test

評価者が「当然こう読む」と補った規則が最終結果を左右した場合、その規則を明示し、Protocolへ追加すべきか、evaluator-specific assumptionとして残すべきか検討する。

### 21.2 strange-result preservation

プロトコルに忠実な結果が奇妙でも、評価者の好みに合わせて補正しない。

奇妙な出力がProtocolの欠陥を示す場合、その発見をProtocolへ返す。

### 21.3 self-application

本Protocol自身を監査対象から除外しない。

ただし、0節で宣言した「監査を内在的作法として採用する」という構成的前提を、本Protocol自身の監査によって究極的に証明することは要求しない。

監査対象となるのは、その前提から導入された規則、運用、finding、表示、改訂手続が実際に目的へ寄与しているか、また自己正当化へ変質していないかである。

監査規則が自分自身へ適用できない、または自分だけ例外化する場合、その例外理由を明示する。


### 21.4 Reconstruction Drill / 再構成演習

事故、重大な異議、記録欠損、外部接続の破断は、監査系が実際に履歴へ遡及できるかを強制的に露出させる。

実事故を待つ必要はない。

定期的または重要な変更後に、**「事故が起きた」「主要な接続が切れた」「重要記録が一部失われた」**という仮想Cutを置き、現在のrepositoryから次を再構成できるか演習してよい。

例：

- この命題は、誰がいつ何を根拠に採用したか。
- 現在の定義ownerは、どの履歴からその権限を持つか。
- 外部sourceへの接続が失われた場合、どの主張が影響を受けるか。
- 一つの中間文書が欠落しても、bridge claimの由来を再構成できるか。
- 監査記録が失われても、Git history、source、decision recordから判断経路を復元できるか。
- 逆に、監査記録だけ残って実態へ戻れない箇所はないか。

この演習は「事故を起こす」ことを目的としない。障害注入、tabletop exercise、disaster-recovery testと同様に、意図的な切断を仮定してReturn / Path / Ground Searchの実効性を検査する。

演習で再構成できなかったことを即時の不正や失敗とみなさない。どの接続が暗黙であったか、どの履歴が一箇所に集中していたか、どの記録が実態から切れていたかをfindingとして返す。

---

## 22. 本Protocolが保証しないもの

本文書は、次を保証しない。

- 監査された命題が真であること。
- 透明な判断が正しいこと。
- 五つのTopology軸が判断の全構造を網羅すること。
- Cut / False Linkが全逸脱を分類できること。
- 根拠系列に究極の停止点が存在すること、または存在しないこと。
- 外部体系との接続が必ず有益であること。
- SOを使う方がSOを使わない方法より優れていること。
- AI監査が人間監査より優れていること。

本Protocolの価値は、これらを先に保証することではなく、判断の接点、責任、経路、異議、残差を後から再検査できる状態へ置くことにある。

---

## 23. 研究段階として保持するもの

次は、本Protocolで即座にrepository-wide doctrineへ昇格させない。

### 23.1 客観性の定式化

判断が自己都合では変更できない外部制約へ開かれていることと、追跡・異議・改訂可能性の関係は、重要な研究課題である。

ただし、本Protocolはそれを「客観性の正本定義」として採用しない。

必要な場合は、どの外部制約が判断を変更し得るかを観測項目として記録する。

### 23.2 根拠の「大地」モデル

根拠を唯一の最終根としてではなく、命題がどの地盤へ接触して成立しているかとして読む比喩は研究継続中である。

本Protocolでは、Ground Searchとして、根拠系列の停止点、そこへ至る探索経路、履歴への遡及可能性、上流根拠の共有・独立性を正式な運用対象とする。

ただし、それらのoperational traceを「大地」の存在論的定義や究極根拠の理論へ直ちに昇格させない。

### 23.3 境界は侵入ではなく誘因であるという仮説

外部体系との良い接続が、結論の輸入・統合ではなく、双方が再検討可能な接続機会を提示することにあるという仮説は研究継続中である。

本Protocolでは、双方向の拒否・修正・returnを監査条件として利用するが、この仮説自体を普遍命題として採用しない。

---

## 24. 旧評価体系との移行関係

本Protocolは、旧`00_Overview/Claim_Strength_and_Publication_Layer_Table.*`を直ちに削除するための文書ではない。

移行時には、旧文書が保持している責務を分解し、適切なownerへ移す。

現時点の移行方向は次である。

| 旧責務 | 新しい主なowner候補 |
|---|---|
| proposition assessment order | 本Protocol |
| attribution / commitment | 本Protocol |
| Claim Strength S | 本Protocol |
| external connection exposure E | 本Protocol |
| A–H canonical finding types / response modes | 本Protocol |
| validity-regime preservation / commensuration intake | 本Protocol |
| engagement-capacity / nonadjudicative nonengagement | 本Protocol |
| use / safety risk | Publication / Safety governance |
| publication layer P | `Publication_and_Commensuration_Policy.md` |
| Verification V | Evaluation Historyへ分解 |
| Rendering Distance R | local language-game / terminology connection recordへ分解 |
| vocabulary definitions | `GLOSSARY.md` + canonical definition owners |
| document current state | `tools/docs_manifest.yml` |
| evaluation history | evaluation ledger / assessment records |

旧表をSuperseded化する前に、machine-readable registry、manifest、public checker、Navigator projectionの参照を移行する。

---

## 25. 最初のpilot audit

本Protocolを採用候補として検査する際、いきなり全正本を監査しない。

最初のpilotでは、性質の異なる少数命題を選ぶ。

推奨対象：

1. `01_Sat_Truth/Boundary_Realism_Principle.md`
   - 公開基礎
   - 非主張境界
   - repository-owned propositionの監査

2. `01_Sat_Truth/Boundary_Epistemological_Critique.ja.md`
   - 外部哲学・形式体系との接触
   - 強い接続候補
   - attribution / warrant / scopeの監査

3. 必要に応じて、外部語彙を明示的に借りる文書を一つ追加する。

pilotの目的は対象文書を裁くことではない。

目的は、本Protocolが次を十分に区別できるかを検査することである。

- representedとendorsed
- authoredとcommitment
- source claimとbridge claim
- topology findingとtruth judgment
- SとE
- findingとpublication decision
- unresolvedとfailure

pilotでProtocol不足が露出した場合、正本監査を拡大する前に本Protocolを改訂する。

---

## 26. 採用後のReturn

本Protocolは固定完成物ではない。

少なくとも次の場合に再開する。

- pilot auditで分類不能な差分が反復した。
- 別のLLMまたは人間評価者で判断差が局在化できない。
- S/Eが再び命題内容を上書きし始めた。
- 監査コストが対象の実務価値を継続的に上回る。
- external domain specialistから接続規則への重大な異議が出た。
- Terminology Connection / Return governanceと責務が重複した。
- Publication Policyとの責務分離が崩れた。
- Navigatorの表示都合がcanonical assessmentを歪めた。
- SOなし対照条件が反復して優位になった。

改訂時は、旧判断を無標識に書き換えず、評価履歴と変更理由を残す。

---

## 27. 圧縮原則

本Protocolを最小限に圧縮すると、次の順序になる。

> **監査は正しさを展示するためではなく、体系が自分を完成済み・理解済み・接続済みと誤認しないために行う。**
> **命題を先に見る。**
> **誰の命題かを分ける。**
> **repositoryがどこまで引き受けるかを分ける。**
> **位相・範囲・責任を分ける。**
> **根拠経路だけでなく、その根拠へどう辿ったかを露出する。**
> **異なる名前でも同じ根拠系列なら、独立した支持として二重計上しない。**
> **外部領域とSOを上下化せず、接続を提出した側がbridgeの責任を持つ。**
> **接続は、双方が訂正・拒否・再接続できる状態を保つ。**
> **体系の仕事と妥当性体系を同定し、通約可能な接触面が成立する前に対象命題の勝敗判定へ飛ばない。**
> **未確立、非導出、事実衝突、内部defeater、外部参照誤記、異位相解釈、相互bridge係争を同じ状態へ潰さない。**
> **非関与は肯定・否定・敗北・defeaterではない。関与能力境界を非判定的非関与として保持する。**
> **接点・位相・経路・返路・開放端を監査する。**
> **異常を分類より先に保存する。**
> **S/E等は最後に投影する。**
> **監査可能なものだけを見る監査へ変質していないかを監査する。**
> **必要に応じて仮想Cutを置き、履歴と判断経路を再構成できるか試す。**
> **未解決を成功にも失敗にも偽装しない。**
> **結果を人間の判断へ返し、後から再開できるようにする。**

これを、本リポジトリにおける判断透明性監査の基本順序とする候補とする。

# Repository Assessment Workbench

> Status: Experimental Developer tooling
> Scope: Representative-claim / claim-hotspot classification pilot
> Canonical effect: None

このワークベンチは、正本監査の方法を完成済みと仮定しない。創造・方法設計と、凍結した方法の実行を分離するための実験面である。

## 1. 原則

1. 方法を作る段階では、直観的探索を手順で拘束しない。
2. ひとたびpilot revisionを切ったら、そのrunでは方法を変更しない。
3. 奇妙な出力も補正せず、対象全体を同じ方法で完走する。
4. 人間レビューでは、LLMの命題誤解・統合誤り・帰属誤解・外部理論誤解と、protocol自体の系統誤差を区別する。
5. protocolを変更する場合はrevisionを更新し、比較対象へ一律再実行する。
6. このワークベンチからcanonical manifestや正本文書を直接変更しない。

## 2. 分類単位

v0.2では「全命題台帳」を作らない。文書ごとに三種類へ分ける。

### Representative Claims

タイトル、目的、中心命題、結論に関係し、その文書が代表して何を主張するかを示す。通常1〜3件程度を目安とするが、件数は規則ではない。

同じ帰属、repository commitment、責任主体、scope、論証上の役割を共有し、同一主張の反復・言い換え・展開である記述は一つへ統合する。**S/Eは統合条件に使わない。**

文書の `document_profile.classification` は representative claims を根拠に決める。

### Claim Hotspots

論証途中に現れる、代表主張とは別に局所的な注意を要する主張を探知する。候補例:

- 異なるground ownerへ移る
- 外部体系とのbridgeを作る
- scopeが拡張する
- identity / universalityを導入する
- causal / mechanistic relationを導入する
- 強いcorrespondenceを提示する
- 別の責任主体を必要とする

hotspotには局所S/Eを付けるが、**最大値をdocument profileへ自動昇格しない。** AMP等へ根拠が遡及する局所claimも `local_only` として保持する。

### Nonclaim Boundaries

「本稿はXを主張しない」等はS/E分類対象に数えない。`nonclaim_boundaries` に別記し、scope controlや自覚の確認に使う。

## 3. データ境界

```text
repository_assessment_protocols.yml
  -> build_repository_assessment_protocols_preview.py
  -> repository_assessment_protocols.preview.json
  -> Developer Navigator / Assessment Lab

Assessment Lab
  -> repository_assessment_execution.json
  -> external / local runner
  -> repository_assessment_run.json
  -> human review in browser
  -> repository_assessment_review.json
```

`run` は凍結方法による生の出力、`review` は人間判断である。`before / after` を分離し、レビューでrun自体を上書きしない。

## 4. UIレビュー

第一レビュー単位は **document profile** とする。文書カードには以下を先に表示する。

- representative S/E
- representative claim数
- hotspot数
- nonclaim boundary数

代表主張・hotspotは展開して読める。誤解や局所分類を直す必要があるときだけ個別レビューを開く。これにより、全命題を一件ずつ承認する負荷を避ける。

## 5. Local runner contract

`serve_navigator.py` は任意のlocal commandをrunnerとして受け取れる。runnerはstdinから `repository_assessment_execution` JSONを受け取り、stdoutへ `repository_assessment_run` JSONだけを返す。

例:

```powershell
python scripts/serve_navigator.py --assessment-runner "python C:\path\to\my_llm_runner.py"
```

runnerが未設定でも、実行パックのexport/import経路は使用できる。

## 6. Pilot targets

初期revisionは次をdefault fixtureとする。

- `01_Sat_Truth/Boundary_Realism_Principle.md`
- `01_Sat_Truth/Boundary_Epistemological_Critique.ja.md`

この2文書のrunを途中で変更せず完走し、レビュー後にprotocol revisionを再構築する。

## 7. 昇格

このpilotが安定した場合、現在のDeveloper registration reviewと同じtransaction modelへ昇格する。

```text
AI proposal
  -> before / after
  -> approve / approve_with_edits / hold / reject
  -> explicit apply
```

昇格はprotocol側の `promotion.state` を変更しただけでは成立しない。schema、apply path、Public projection境界、release gateを明示的に更新してから行う。

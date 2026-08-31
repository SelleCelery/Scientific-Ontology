# Registration Workbench / 登録・改訂レビュー

> Status: current Developer contract
> Scope: `docs_manifest.yml` の仮登録文書レビューと、登録済み文書のmetadata改訂提案

## 1. 目的

Developer Navigatorは、`docs_manifest.yml` をブラウザから直接編集しない。

現在の境界は次のとおり。

```text
canonical manifest
  ↓ read only
Developer read model
  ↓
human review
  ↓
review transaction JSON
  ↓ repository-side validation
  ↓ dry-run
  ↓ explicit apply
canonical manifest
```

ここで重要なのは、**manifestを読むこと**と**manifestへ書くこと**を分けること。

仮登録文書はすでにmanifestのcanonical ledgerに存在するため、過去のcandidate ledgerを別の現行入力として維持しない。人間レビュー中であることは `registration_state: provisional` が表す。

## 2. 現在の入力

### 仮登録文書

`tools/docs_manifest.yml` の `registration_state: provisional` を直接のsourceとする。

ブラウザはYAMLを直接読むのではなく、builderが作るDeveloper専用read modelを読む。

```text
tools/docs_manifest.yml --------------------┐
                                             ├─> scripts/build_registration_workbench_preview.py
tools/docs_revision_proposals.yml ----------┘
                                                   ↓
                                  tools/docs_registration_workbench.preview.json
```

`docs_registration_workbench.preview.json` は生成物であり、手編集しない。

### 登録済み文書の改訂提案

一回限りのreader-question専用seedではなく、genericな提案sourceを使う。

```text
tools/docs_revision_proposals.yml
```

初期28件は、旧reader-question review seedの提案内容を変更せず移行したもの。

提案はpartial patchとして保存し、現在manifestに適用した完全なbefore/afterはpreview builderが生成する。これによりproposal source自体が第二のmanifestにならないようにする。

## 3. レビュー対象

Developer Navigatorのreview poolは次をまとめて扱う。

```text
provisional document
  = manifestに存在するがmetadata reviewが未完了

registered revision proposal
  = 登録済み文書に対する明示的metadata改訂提案

manual candidate
  = manifestにまだ存在しない新規登録案

ad-hoc registered revision
  = Navigator上で人間が開始した登録済み文書の改訂案
```

concept ownershipやtyped logical relationは、このworkbenchから推測・追加しない。

## 4. 判定

仮登録文書には次を使う。

- `approve`: 現在metadataを承認し、apply時に `registration_state: registered` へ昇格する。
- `approve_with_edits`: 人間編集後のmetadataを承認し、apply時にregisteredへ昇格する。
- `hold`: manifestのprovisional状態を維持する。
- `reject`: このレビューtransactionでは削除しない。provisional状態を維持し、削除・非公開化が必要なら別の明示操作とする。

登録済みrevisionは、承認されたものだけmetadataを更新する。reviewを開始しただけでは現行登録文書を無効化しない。

## 5. ブラウザ保存とexport

途中状態はブラウザ `localStorage` に保存する。

ファイルは自動生成しない。人間が **レビュー結果を書き出す / Export review** を押したときだけ、次を生成する。

```text
docs_registration_review.json
```

schemaは `tools/docs_registration_review.schema.json` の `0.3`。

transactionは少なくとも次へbindingする。

```text
manifest_sha256
graph_sha256
provisional_count
revision_proposals_sha256
revision_proposal_count
```

古いsourceへ対するreviewを現在manifestへ誤適用しないためのbindingである。

## 6. repository-side validation

```powershell
python scripts/validate_registration_review.py "$HOME\Downloads\docs_registration_review.json"
```

validatorは、source hash、現在のprovisional baseline、proposal binding、編集可能field、doc_id/path境界を検査する。

簡易self-test:

```powershell
python scripts/validate_registration_review.py --self-test
```

## 7. manifest apply

既定はdry-runで、ファイルを書かない。

```powershell
python scripts/apply_registration_review.py "$HOME\Downloads\docs_registration_review.json"
```

別manifestへ出力する場合:

```powershell
python scripts/apply_registration_review.py `
  "$HOME\Downloads\docs_registration_review.json" `
  --output tools/docs_manifest.reviewed.yml
```

canonical manifestを変更する場合だけ明示的に:

```powershell
python scripts/apply_registration_review.py `
  "$HOME\Downloads\docs_registration_review.json" `
  --apply
```

`--apply` で承認または却下されたgeneric revision proposalはactive proposal sourceから消費される。`hold` は残る。これにより、適用後に旧proposalがstale inputとして残らない。

apply後はworkbench preview、index / graph等の通常build/checkを再生成する。

## 8. write authority

```text
Browser
  read:  docs_registration_workbench.preview.json
  write: localStorage / exported review JSON only

Repository scripts
  read:  manifest + revision proposals + review JSON
  write: manifest only after explicit apply
```

Assessment Labのlocal runnerへのPOSTはcanonical manifest writeではない。checkerはPOST一般を禁止せず、registration/manifestへのbrowser direct-writeだけを禁止する。

## 9. 現時点の非目的

このworkbenchは次を自動決定しない。

- SO概念のowner
- typed logical relation
- 文書本文の改稿
- rejectされたprovisional文書の自動削除
- 公開可否そのものの自動確定

これらはそれぞれのauthorityへ戻す。

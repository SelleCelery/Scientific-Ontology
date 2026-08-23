# Document Registration Candidates / 文書登録候補

> Status: Internal review support
> Scope: manifest registration candidates / navigation metadata / human review
> Authority: This file does not modify `tools/docs_manifest.yml` and does not assign canonical concept ownership.

## 1. Purpose / 目的

`tools/docs_graph.json`で`observed_document`として確認された未登録Markdown 100件について、
`docs_manifest.yml`へ登録する前の雛形を作る。

候補は現在の文書本文、メタデータ、明示的な日英対応、既存manifestの登録済み対文書だけを根拠にする。
本文を改稿せず、概念所有を推測せず、検索入口として必要な最小情報を提案する。

## 2. Files / ファイル

- `docs_registration_candidates.yml` — 100件の候補正本。まだmanifestではない。
- `docs_registration_candidates.schema.json` — 候補ファイルの構造契約。
- `scripts/validate_registration_candidates.py` — path、ID、topic、登録重複、候補件数を検査する。

## 3. Review order / 確認順

1. `recommended_action`
2. `role_ja`と`reader_questions.ja`
3. `topics`
4. `entry_level`
5. `public_profile`
6. `concept_ownership`とtyped relationsは別工程

著者側では全件を再要約する必要はない。UIや一覧で違和感のある項目だけを差し戻す。

## 4. Recommended actions / 推奨処理

- `register_document` — 本文を独立した公開文書として登録する候補。
- `register_after_status_review` — Draft等の状態を確認してから登録する候補。
- `register_commensuration` — 日本語正本等と同一familyへ束ねる通約文書。
- `register_navigation` — README、Map、Index、Glossary等の入口文書。
- `register_support` — CHANGELOG、Registry、Citation、License等。通常Topic検索では前面に出さない。

## 5. Boundary / 境界

- `recommended_action`は公開価値の順位ではない。
- `entry_level`は難易度の絶対評価ではなく、Navigator上の初期配置候補。
- `topics`は存在論的分類ではなく、読者が入れる入口。
- `aliases`は同義語宣言ではない。
- `reader_questions`は本文が現在返答できる範囲を越えてはならない。
- `concept_ownership`は候補生成では確定しない。

## 6. Navigator candidate preview / Navigatorでの候補レビュー

候補YAMLはブラウザが直接解釈せず、決定論的なJSON read modelへ変換する。

```bash
python scripts/build_registration_candidates_preview.py
python scripts/build_registration_candidates_preview.py --check
```

生成物は`tools/docs_registration_candidates.preview.json`。手編集しない。

Navigatorの「候補レビュー」では、100件をlayer、recommended action、confidence、navigation visibility、テキストで絞り込める。各候補からReaderと現在のTyped Relation Graphへ戻れるため、本文を全件再要約せず、配置や問いの違和感だけを確認できる。

このpreviewは承認操作ではない。`docs_manifest.yml`への昇格は別工程で行う。

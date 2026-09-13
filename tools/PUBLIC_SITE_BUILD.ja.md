# Public Site Builder / Artifact Checker 開発運用メモ

この文書は、Scientific Ontology の Public Navigator を GitHub Pages 用の安全な静的配布物へ変換するローカル手順を説明する。

## 1. 責務

```text
tools/docs_manifest.yml
        ↓
public projection builders
        ↓
tools/docs_public_catalog.json
tools/docs_public_graph.json
        ↓
scripts/build_public_site.py
        ↓
_build/pages/
        ↓
scripts/check_public_site.py
        ↓
GitHub Pages artifact
```

`docs_manifest.yml` は文書メタデータの正本であり、Pages artifact そのものではない。

`_build/pages/` は生成物である。手編集しない。

数式表示は外部CDNへ依存せず、`navigator/vendor/katex/` をPages artifactへそのまま含める。KaTeXは表示層だけの依存であり、Markdown本文やmanifestの正本性を変更しない。vendored CSS はホスト固有のselector scopeを持たないKaTeX標準相当のselector境界を使用し、MathMLはアクセシビリティ用に保持したまま視覚上のみclipする。CSS内の非data URLはvendor directory内で閉じ、外部font/CDN参照を認めない。

## 2. Public Site に含めるもの

- Public Navigator の `index.html`、CSS、compiled JavaScript、案内表示データ
- Navigator Reader が使用する vendored KaTeX runtime / CSS / font assets / license
- `docs_public_catalog.json`
- `docs_public_graph.json`
- Public catalog / graph に登録された Markdown 文書
- その Markdown から参照される公開画像等
- root から Navigator へ送る `index.html`
- `.nojekyll`
- artifact の再現性を確認する `public_site_manifest.json`

## 3. 含めないもの

- `navigator/dev.html`
- TypeScript source
- candidate / review / confidence / evidence
- canonical developer graph diagnostics
- `scripts/`
- `.git/`、`.github/`、`.venv/`、`__pycache__/`
- `99_Private_Core_Not_Included/`
- `000*` 文書

Public Markdown が repository 内の開発用ファイルへリンクしている場合、builder はそのリンク先を Pages artifact へコピーせず、GitHub repository の `blob/<ref>/...` URLへ置換する。

## 4. Build

```powershell
python scripts/build_public_site.py
```

出力先：

```text
_build/pages/
```

GitHub 上の参照先を tag 等へ固定する場合：

```powershell
python scripts/build_public_site.py --source-ref v5.0.0
```

## 5. Deterministic build check

```powershell
python scripts/build_public_site.py --check
```

現在の `_build/pages/` と、同じ source から再生成した一時 artifact の全ファイル SHA-256 を比較する。

## 6. Artifact safety check

```powershell
python scripts/check_public_site.py
```

検査内容：

- artifact file list / SHA-256
- Public catalog / graph と repository source の一致
- 128 Public documents の存在
- Graph document path の一致
- private / candidate / developer file の非混入
- Public data 内の developer-only key 非混入
- UTF-8 strict decode / BOM 非混入
- Markdown local link の artifact 内解決
- `public-content.json` の案内先存在
- Public shell のみが配布されていること

## 7. 標準ローカル工程

```powershell
python scripts/check_dn6_release_gate.py
python scripts/build_public_site.py
python scripts/check_public_site.py
python scripts/build_public_site.py --check
```

## 8. GitHub Actions での利用

GitHub Actions でも同じ builder / checker を呼ぶ。

```text
DN-6 gate
  ↓
build_public_site.py
  ↓
check_public_site.py
  ↓
upload-pages-artifact
  ↓
deploy-pages
```

ローカル用と CI 用で別の build logic を作らない。

## v5.1 role-aware build and update boundary

Current page membership comes from catalog documents in the manifest. Fixed sources and research evidence may remain public Repository assets without becoming independent Navigator pages. A readable GitHub source link is not a claim endorsement.

Links to legitimate source directories are externalized to the Repository's `/tree/` route. Links to non-page source files continue to use `/blob/`. Disallowed internal/private paths remain blocked. Frozen source files are not edited merely to make a static-site link render.

For incoming updates, the verification hook runs `scripts/rebuild_document_read_models.py` before site verification. Its transaction backs up the five generated JSON read models and the prior Pages output, restores them on any failure, and leaves the outer ZIP manager to restore package files. The ZIP registry records receipt independently; registry presence alone does not mean application succeeded.

When migrating the hook itself, use the externally extracted, approved package policy via the manager's global `--policy` argument for inspect/register/plan/apply. Otherwise an already running manager keeps the old policy it loaded before applying files. Do not use skip-check or dirty-tree flags to bypass the old stale-public-document failure.

Historical MANIFEST mismatches remain visible. Local editing/build verification reports them; `validate_docs_manifest.py --release-gate` blocks publication until independently resolved. Recomputing a historical manifest to fit later editorial wrappers is not a repair.

# Release Update Pack

> Status: Repository governance specification
> Scope: Release-level synchronization for Scientific Ontology / 存在境界論
> Authority: Operational contract for release metadata and public release interfaces
> Source of release facts: [`release_state.yml`](./release_state.yml)
> Synchronizer: [`release_update.py`](./release_update.py)

---

## 1. Purpose / 目的

Release Update Packは、公開版更新のたびに版番号、著者、ORCID、DOI、公開日、前版関係などを複数ファイルへ手入力し、不整合を作ることを防ぐための更新契約である。

この仕組みは理論本文を自動生成しない。

役割は次に限定する。

1. `release_state.yml`をリリース事実の単一所有点にする。
2. 承認済み事実を公開書誌・リリースメタデータへ決定論的に同期する。
3. READMEとRoadmapの人間所有を維持したまま、版情報の不整合を検査する。

---

## 2. Ownership boundary / 所有境界

| File | Role | Ownership | Script action |
|---|---|---|---|
| `README.md` | 公開入口・意味の主導線 | Human | validate only |
| `Roadmap.md` | 研究系列の方向 | Human | validate only |
| `RELEASE_NOTES.md` | 今回の変更 | AI draft / Human approval | generate |
| `CITATION.cff` | machine-readable citation | Machine sync | generate |
| `CITATION.md` | human-readable citation | Machine sync / Human review | generate |
| `.zenodo.json` | Zenodo metadata | Machine sync | generate |

スクリプトはREADME、Roadmap、理論本文、研究ノートを書き換えない。

---

## 3. Author identity contract / 著者識別契約

Current public author identity:

- Display name: `万土華凜`
- Family name: `万土`
- Given name: `華凜`
- ORCID: `0009-0001-5709-2669`
- ORCID URL: `https://orcid.org/0009-0001-5709-2669`
- Romanization: not registered; do not infer

Zenodo legacy `.zenodo.json` creator rendering is derived as `万土, 華凜` from the stored family/given fields. CFF stores family and given names separately.

---

## 4. DOI lifecycle / DOI更新手順

### Phase A — pre-release

```yaml
zenodo:
  version_doi:
    status: "pending"
    value: null
    url: null
```

この段階では架空DOI、仮DOI、前版DOI、全版DOIをv5.0版固有DOIとして流用しない。

生成物では版固有DOIを`pending`として扱い、CFFから版固有DOIと`date-released`を省略する。

### Phase B — DOI assigned

Zenodoで版固有DOIが確定したら、最初に`release_state.yml`だけを更新する。

```yaml
release:
  status: "published"
  publication_date: "YYYY-MM-DD"

zenodo:
  version_doi:
    status: "assigned"
    value: "10.5281/zenodo.xxxxxxxx"
    url: "https://doi.org/10.5281/zenodo.xxxxxxxx"
```

その後`--dry-run`、`--write`、`--release-check`を順に実行する。

---

## 5. Installation / 実行準備

リポジトリルートで実行する。

```powershell
python -m pip install -r 90_Repository_Governance/Release_Update/requirements.txt
```

依存はPyYAMLのみ。生成処理はPython標準ライブラリとPyYAMLで行う。

---

## 6. Commands / コマンド

### Check

```powershell
python 90_Repository_Governance/Release_Update/release_update.py --check
```

- `release_state.yml`構文・必須値を検査
- version / author / ORCID / DOI状態を検査
- guaranteed inclusionsの存在を検査
- README / Roadmapが対象版を参照しているか検査
- 生成対象4ファイルがstateと同期しているか検査
- ファイルは変更しない

### Dry run

```powershell
python 90_Repository_Governance/Release_Update/release_update.py --dry-run
```

生成予定差分を表示し、ファイルは変更しない。

### Write

```powershell
python 90_Repository_Governance/Release_Update/release_update.py --write
```

次の4ファイルだけを書き換える。

```text
RELEASE_NOTES.md
CITATION.cff
CITATION.md
.zenodo.json
```

### Strict release check

```powershell
python 90_Repository_Governance/Release_Update/release_update.py --release-check
```

公開時の厳格検査。最低限、次を要求する。

- `release.status: published`
- publication date確定
- version-specific DOI assigned
- 生成4ファイルがstateと完全同期

したがって、DOI未発行のrelease candidate段階では、このコマンドが失敗するのが正常である。

---

## 7. Standard U4 flow / U4標準手順

```text
human release decision
    ↓
release_state.yml
    ↓
--check
    ↓
--dry-run
    ↓
human diff review
    ↓
--write
    ↓
--check
    ↓
git diff --check
    ↓
commit
```

公開日・DOIが確定したら、同じ経路をもう一度通す。

---

## 8. Zenodo metadata note

ZenodoのGitHub連携では、`.zenodo.json`と`CITATION.cff`が同時に存在する場合、Zenodoは`.zenodo.json`を優先する。したがって、両者を独立に手編集せず、同じstateから同期する。

`.zenodo.json`のcreatorにはORCIDを伝播する。

Zenodo用ファイル構成（完全ZIP＋選択PDF）は`release_state.yml > zenodo.file_strategy`が保持するが、実際のPDF/ZIP生成はU4の責任外とし、後続Gateで扱う。

---

## 9. Non-goals / 非目的

Release Update Packは次を行わない。

- 理論内容の採否
- 主張強度の自動変更
- README主導線の自動執筆
- Roadmap研究判断の自動変更
- 未発行DOIの推測
- 著者名ローマ字表記の推測
- `000`保留文書の自動昇格
- DSSIアプリ公開判断

リリースの意味は人間が所有し、反復可能な同期だけを機械へ渡す。

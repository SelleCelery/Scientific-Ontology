# Release Update Pack

> Status: Repository governance specification
> Scope: Release-level synchronization for Scientific Ontology / 存在境界論
> Authority: Operational contract for release metadata and public release interfaces
> Source of release facts: [`release_state.yml`](./release_state.yml)

---

## 1. Purpose / 目的

Release Update Packは、公開版を更新するたびに同じ事実を複数ファイルへ手入力し、版番号、著者表記、ORCID、DOI、公開日、前版関係などが食い違うことを防ぐための更新契約である。

この更新パックは、理論本文を自動生成するための仕組みではない。

役割は次の二つに限定する。

1. **リリース事実の単一所有点を作る。**
2. **その事実を公開インターフェイスと書誌メタデータへ矛盾なく伝播する。**

`release_state.yml`はリリース事実の正本である。READMEとRoadmapの意味判断まで所有しない。

---

## 2. Core files / 毎回確認する六ファイル

| File | Role | Ownership | Update mode |
|---|---|---|---|
| `README.md` | 現在の体系を何として見せるか | Human | AI may propose a patch; human approves meaning |
| `Roadmap.md` | 現在どこへ進んでいるか | Human | AI may synchronize status facts; human approves direction |
| `RELEASE_NOTES.md` | 今回何が変わったか | AI draft / Human approval | Generated from approved release state + repository diff |
| `CITATION.cff` | Machine-readable citation | Machine sync | Deterministic synchronization |
| `CITATION.md` | Human-readable citation | Machine sync / Human review | Deterministic facts + readable rendering |
| `.zenodo.json` | Zenodo deposition metadata | Machine sync | Deterministic synchronization |

この六ファイルを**Core Update Pack**とする。

`GLOSSARY.md`、`tools/docs_manifest.yml`、各Research Notesの索引、Concept Network等は、内容変更がある場合だけ更新する**Conditional Update Targets**であり、毎回更新を強制しない。

---

## 3. Source of truth / 事実所有

### 3.1 `release_state.yml`が所有するもの

- release version
- display version
- release status
- publication date
- release title
- public author name
- ORCID
- license
- repository URL
- previous release version and DOI
- Zenodo version-family DOI
- current version DOI status/value
- human-approved release theme
- human-approved release purpose
- human-approved short release highlights

### 3.2 `release_state.yml`が所有しないもの

- SOの理論本文
- READMEの説明論理そのもの
- Roadmap上の研究判断そのもの
- 研究ノートの主張強度判断
- 未解決問いへの回答
- 新しい概念定義
- 公開によって得られた批判への採否

これらは人間または各文書の正本所有者が判断する。

---

## 4. Human-owned and machine-owned boundaries / 人間とAIの境界

### 4.1 Human-owned

次はAIへ最終判断を委譲しない。

- v5系を何として開始するか
- release themeの日本語正本
- READMEの主導線
- Roadmapの現在地と研究優先順位
- release highlightsへ何を載せるか
- ある研究をpublic / hold / internalのどこへ置くか

v5系の開始主導線は、現時点では次を日本語正本とする。

> **事象は境界で起きている。主観でも客観でもなく、それらが混ざり合うところで。**

英語版は自動的に正本化しない。通約が確定するまで`release_state.yml`では`pending_commensuration`とする。

### 4.2 AI / machine-owned

次は、承認済みstateを基礎にAIまたはスクリプトへ委譲してよい。

- version/date/titleの同期
- ORCIDの同期
- previous release DOIの同期
- Zenodo version-family DOIの同期
- DOI確定後のversion DOI同期
- `CITATION.cff`生成・更新
- `CITATION.md`の定型部分生成・更新
- `.zenodo.json`生成・更新
- `RELEASE_NOTES.md`初稿
- 六ファイル間の不一致検査
- YAML/JSON構文検査
- DOI/ORCID形式検査
- release diffの一覧化

AIは、不明値を推測で埋めない。

---

## 5. Author identity contract / 著者識別契約

公開著者名は、リポジトリで登録されたUnicode表記を保持する。

- Public author name: `万土 華凜`
- ORCID: `0009-0001-5709-2669`
- ORCID URL: `https://orcid.org/0009-0001-5709-2669`
- Romanization: 未登録の場合は推測しない

### Propagation rule

ORCIDは次へ同一値として伝播する。

- `CITATION.cff`
- `CITATION.md`
- `.zenodo.json`
- READMEのAuthor / Citation節（掲載する場合）
- RELEASE_NOTESのCitation節（掲載する場合）

表記を各ファイルで独自変形しない。

---

## 6. DOI lifecycle / DOI更新手順

DOIはORCIDと違い、公開前には版固有値が存在しない場合がある。

### Phase A — Pre-release

```yaml
zenodo:
  version_doi:
    status: "pending"
    value: null
    url: null
```

この段階では架空DOI、仮DOI、前版DOIを現行版DOIとして流用しない。

`.zenodo.json`では、前版DOIを`isNewVersionOf`として保持できる。

### Phase B — DOI assigned

Zenodoが版固有DOIを発行した後、`release_state.yml`のみを先に更新する。

```yaml
zenodo:
  version_doi:
    status: "assigned"
    value: "10.5281/zenodo.xxxxxxxx"
    url: "https://doi.org/10.5281/zenodo.xxxxxxxx"
```

その後、Update Packを再実行し、Citation系とREADME/Release NotesのDOI表示を同期する。

---

## 7. Update sequence / 標準更新順

### Gate U0 — Repository clean check

```powershell
git status --short
```

意図しない変更がある場合は開始しない。

### Gate U1 — Human release decision

人間が次を確定する。

- version
- release status
- theme
- purpose
- included highlights
- public/hold/internal境界

### Gate U2 — Update `release_state.yml`

事実をstateへ入力する。不明値は`null`にする。

### Gate U3 — Human-owned files

1. `README.md`
2. `Roadmap.md`

AIは差分案を作ってよいが、意味判断は人間が確定する。

### Gate U4 — Generated / synchronized files

3. `RELEASE_NOTES.md`
4. `CITATION.cff`
5. `CITATION.md`
6. `.zenodo.json`

### Gate U5 — Validation

最低限、次を検査する。

- version一致
- title一致
- author一致
- ORCID一致
- release date一致（確定済みの場合）
- previous release DOI一致
- version DOIのpending/assigned整合
- YAML parse
- JSON parse
- Markdown link integrity where practical
- trailing whitespace
- unintended versioned filenames
- inferred romanizationがないこと

### Gate U6 — Human diff review

```powershell
git diff
git diff --check
```

ステージ後は、

```powershell
git diff --cached
git diff --cached --check
```

を確認する。

### Gate U7 — Commit

Update Packの変更は、理論本文の大規模変更と可能な限り分ける。

例：

```text
release: prepare Public Edition v5.0.0 metadata
```

DOI確定後の同期だけなら：

```text
release: add Zenodo DOI for Public Edition v5.0.0
```

---

## 8. Propagation map / フィールド伝播表

| State field | README | Roadmap | Release Notes | CITATION.cff | CITATION.md | .zenodo.json |
|---|---:|---:|---:|---:|---:|---:|
| `release.version` | yes | yes | yes | yes | yes | yes |
| `release.publication_date` | optional | optional | yes | yes | yes | yes |
| `release.title` | optional | no | yes | yes | yes | yes |
| `public_author.name` | optional | no | yes | yes | yes | yes |
| `public_author.orcid` | optional | no | optional | yes | yes | yes |
| `release.theme.ja` | yes | yes | yes | no | optional | summary only |
| `release.purpose.ja` | summary | yes | yes | no | no | description source |
| `previous_release.doi` | optional | no | yes | optional | yes | yes |
| `zenodo.version_family_doi` | optional | no | yes | optional | yes | optional |
| `zenodo.version_doi` | yes after assignment | no | yes | yes | yes | not self-declared before assignment |

`yes`は同期対象、`optional`は文書構造上必要な場合のみ、`no`は原則伝播しないことを示す。

---

## 9. Release Notes generation rule / RELEASE_NOTES生成規則

`RELEASE_NOTES.md`は単なるGit変更一覧にしない。

AIは次の順で草案を作る。

1. release theme
2. relation to previous release
3. human-approved highlights
4. repository-visible additions and structural changes
5. publication/governance changes
6. unresolved or deferred items
7. citation information

AIは、Git diffに存在するという理由だけで理論的重要性を決めない。

また、research noteが追加されたことと、その主張がSO基礎正本へ昇格したことを同一視しない。

---

## 10. README synchronization rule / README同期規則

READMEはUpdate Packで最も自動化を弱くする。

AIが自動同期してよいもの：

- Current public version
- release date
- DOI
- ORCID
- current public research entry links
- citation links

人間確認なしに変更しないもの：

- 冒頭キャッチ
- SOの定義
- v5開始趣旨
- public/private boundaryの説明
- theory/application relationship

READMEをメタデータの寄せ集めにしない。

---

## 11. Roadmap synchronization rule / Roadmap同期規則

Roadmapは工程表ではなく研究経路の公開台帳である。

Update Packは、研究路の状態を機械的に「完了」へ進めない。

AIができること：

- 現在公開された文書を既知の研究路へリンクする
- state上の公開ステータスを反映する
- 旧版番号や古いリンクを更新する

人間が決めること：

- 研究路の追加・廃止・統合
- 主研究路
- hold / reopen
- 研究優先度
- v5系全体の意味づけ

---

## 12. Conditional Update Targets / 条件付き更新対象

次は毎回更新しない。

- `GLOSSARY.md`
- `05_Research_Notes/README.md`
- `05_Research_Notes/Research_Notes_Index.md`
- `00_Overview/Scientific_Ontology_Concept_Network.*`
- `00_Overview/Claim_Strength_and_Publication_Layer_Table.*`
- `tools/docs_manifest.yml`
- `tools/maintenance_rules.yml`
- `Public_Format_Registry.yml`

ただし、新しい文書、用語、正本所有者、public-format contractが発生した場合は、Publication Cutの別チェックとして更新する。

---

## 13. Stop conditions / 自動処理停止条件

次の場合、AIまたはスクリプトは更新を止め、人間判断へ返す。

- versionが複数候補ある
- release dateが未確定なのに確定値を要求される
- DOIが不明
- public author nameがstateと既存Citationで衝突する
- ORCIDが複数値に分岐する
- romanized author nameを推測しなければ出力できない
- READMEまたはRoadmapの意味内容を変更しなければ整合しない
- Research Noteの追加が基礎正本昇格を意味するか不明
- previous releaseとの関係が不明
- public/internal境界が不明

不明値を「それらしい値」で閉じない。

---

## 14. Versioning policy / ファイル名

Update Pack自体とrelease metadataファイル名には版番号を埋め込まない。

- `release_state.yml`
- `UPDATE_PACK.md`

履歴はGit、release tag、release state、Release Notesで保持する。

---

## 15. Initial v5 line / v5系開始時の主導線

v5系では、v4までに蓄積した理論を体系内部だけに留めず、実装・汎用化・外部照合へ進める。

その開始を最も短く表す日本語正本は次である。

> **事象は境界で起きている。主観でも客観でもなく、それらが混ざり合うところで。**

Update Packはこの文を理論的に解釈したり書き換えたりしない。

README、Roadmap、Release Notesがこの主導線をどう展開するかは、人間承認を必要とする。

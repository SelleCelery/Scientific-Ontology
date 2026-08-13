# Release Notes: Scientific Ontology (SO) / 存在境界論 Public Edition v5.0.0


> Status: Release notes / published
> Scope: Public release metadata / research transition / repository change log
> Language: English-first with Japanese release summary
> Version-specific DOI: 10.5281/zenodo.21909382

Release date: 2026-08-13

---

## Citation state

Version-specific DOI: <https://doi.org/10.5281/zenodo.21909382>

Public author: **万土華凜**
ORCID: <https://orcid.org/0009-0001-5709-2669>

For machine-readable citation metadata, see [`CITATION.cff`](./CITATION.cff).
For human-readable citation guidance, see [`CITATION.md`](./CITATION.md).

Version-family DOI: <https://doi.org/10.5281/zenodo.20665197>
Previous release: **v4.3.0** — <https://doi.org/10.5281/zenodo.21394190>

---

## Release theme

> **Events happen at boundaries. Neither simply subjective nor simply objective, but where different modes of description come into contact.**

Scientific Ontology (SO) / 存在境界論 Public Edition v5.0.0 opens the v5 living research series. It carries the framework outward from its internal vocabulary into language, literature, consent, institutions, AI, interfaces, and other application surfaces, while treating criticism, failure, residuals, and unexpected returns from those contacts as inputs for re-collation rather than as post-publication noise. The release adds the Scientific Ontology Operational Outline; the nine Language, Meaning, and Communication Phase research documents and their living-canonical return structure; Consent Boundary and Sentence/Bit Asymmetry; Literature as Worldmaking; and the DSSI research note on observation, judgment, sovereignty, and responsibility return. The DSSI application itself is not part of v5.0. Scientific Ontology does not claim that cross-domain structural resemblance establishes physical identity, nor that the framework replaces established empirical disciplines.

v5.0.0 is the opening release of the v5 living series, not the completion of v5. The release deliberately carries the framework into additional domains while preserving the return path by which criticism, failed correspondence, implementation problems, and residuals can revise later v5.x work.

### Included in this release

- Open the v5 series as a living research series centered on implementation, generalization, external collation, and revision through return.
- Publish the Scientific Ontology Operational Outline as a cross-series operational orientation articulated during preparation for v5.
- Introduce the nine Language, Meaning, and Communication Phase research documents as a living-canonical research line with explicit change and return handling.
- Introduce the DSSI research note on observation, judgment, sovereignty, and responsibility return; the DSSI application itself is not included in v5.0.
- Introduce the research note on consent boundaries and sentence/bit asymmetry.
- Introduce Literature as Worldmaking as a public research note.
- Introduce the manifest-backed Public Navigator for reading, search, typed relation traversal, and Japanese/English counterpart resolution across 128 public documents.

### Explicit public boundary

The DSSI application itself is **not** included in v5.0.0. This release includes only the DSSI public research and implementation-boundary note. Application publication is a later v5.x decision and is not promised by this release.

Files whose basenames retain the local/internal `000` prefix and non-public core materials remain outside the Public Edition.

---

## 日本語要旨

> **事象は境界で起きている。主観でも客観でもなく、それらが混ざり合うところで。**

v4系までに積み上げた境界・履歴・通信・返路の理論を体系内部から遊離させ、
言語、文学、会計、制度、AI、インターフェイスへ実装・汎用化し、
外部との接触から返る残差によって理論自身を再照合するv5系を開始する。
v5.0はv5系の完成版ではなく、以後のv5.xで研究・実装・外部照合の成果を追加するための開幕版である。

### 今回の公開版に含むもの

- v5系を、実装・汎用化・外部照合・返りによる再更新を行う生きた研究系列として開始する。
- v5系開始にあたって自覚された存在境界論の全体運用方針としてScientific Ontology Operational Outlineを公開する。
- 言語・意味・通信位相研究の九本の公開正本候補を、代謝型のLiving Canonical研究線として導入する。
- DSSIの観測・判断・主権・責任返還に関する研究ノートを公開研究線へ導入する。DSSIアプリ本体はv5.0に含めない。
- 同意境界とセンテンス／ビット非対称の研究ノートを公開研究線へ導入する。
- 世界制作としての文学を公開研究ノートとして導入する。
- 128公開文書を単一manifestから読み込み、読解・検索・型付き関係探索・日英対文書解決を行うPublic Navigatorを導入する。

### 公開境界

DSSIについてv5.0.0に含めるのは、観測・判断・主権・責任返還を扱う研究ノートと実装境界です。アプリケーション本体は含めません。アプリ版はv5.1以降で公開条件が整った場合に別途判断し、このリリースでは公開を約束しません。

`000`接頭辞を保持するローカル／内部保留ファイルと、Public Editionの非公開Coreは公開対象外です。

---

## Release-update governance

Release-level facts for this series are owned by [`90_Repository_Governance/Release_Update/release_state.yml`](./90_Repository_Governance/Release_Update/release_state.yml).

The synchronization tool updates only:

- `RELEASE_NOTES.md`
- `CITATION.cff`
- `CITATION.md`
- `.zenodo.json`

`README.md` and `Roadmap.md` remain human-owned. The tool may validate their release references, but it does not rewrite their conceptual or directional content.

Standard flow:

```text
release_state.yml
    -> --check / --dry-run
    -> human diff review
    -> --write
    -> validation
    -> commit
```

When Zenodo assigns the version-specific DOI, update `release_state.yml` first and rerun the synchronizer. No provisional or inferred DOI is generated.

---

## License

This release continues the **CC BY 4.0** licensing policy unless an individual document states otherwise.

Repository: <https://github.com/SelleCelery/Scientific-Ontology>

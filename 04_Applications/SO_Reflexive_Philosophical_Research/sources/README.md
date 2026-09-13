# Research Sources / 研究原資料

> Layer: 04_Applications / SO_Reflexive_Philosophical_Research / sources
> Status: README
> Scope: fixed research sources / experiment provenance / source identity / return paths
> Language: ja+en
> Public profile: P1
> Authority: Directory navigation and source-provenance contract; not a Scientific Ontology concept-definition owner

# 日本語正本

## 1. Directory Role / ディレクトリの位置づけ

`sources/` は、SO再帰的哲学研究で実際に使用した原資料を、後から現在の理論へ合わせて書き換えずに保持するための場所である。

ここに置かれた資料は、**研究原資料としての正本**であり、現在のScientific Ontology全体の教義または公開定義を所有する正本ではない。

研究本文、実験証跡、後続の公開理論が同じ語を使っていても、原資料に含まれる命題が現在のSOによって承認・再主張されたとは扱わない。

## 2. Public Scope / 公開範囲

含むもの：

- 実験で実際に使用された固定入力
- source identityを確認するための由来・hash・利用先
- 現行文書へ戻るための返路

含まないもの：

- 原資料に含まれる全命題への現在のSOによるendorsement
- 現行SOの定義所有権
- 原資料を後続理論へ合わせて修正した新版
- 実験結果の妥当性保証

## 3. Documents / 文書一覧

### Optional Axiom Modules

- Repository path: [`Optional_Axiom_Modules.ja.md`](./Optional_Axiom_Modules.ja.md)
- Historical source filename: `0001Optional_Axiom_Modules.md`
- Research role: old Optional Axiom atlas / fixed stress-test corpus
- SHA-256: `20c3fa4f3c82719cf3716b4a52974b433c945143434ffb1a5a47b779fa8ae136`
- Used by: [`Volume I — De-Registryから判断透明性へ`](../volumes/Volume_01_DeRegistry_to_Judgment_Transparency/README.md)
- Current public protocol: [`Optional_Axiom_Modules_as_Cognitive_Bridge.ja.md`](../../../03_Tam_Goodness/Optional_Axiom_Modules_as_Cognitive_Bridge.ja.md)

収録した `Optional_Axiom_Modules.ja.md` は、Volume I のraw archive indexに記録された固定fixtureのSHA-256と一致する入力を、その内容へ追記・整形を行わず配置したものである。

このhashは同一入力の確認に用いる。内容の妥当性、現在性、SOによるendorsementを保証するものではない。

03層の「認識ブリッジとしての選択公理モジュール」は、旧atlasそのものを現在の教義として再公開した文書ではない。

旧atlasは、De-Registryその他の監査で用いた歴史的・高密度なstress corpusである。現行03文書は、その経験を経た後に、関心・捨象・価値・コスト、Core Invariant、Operational Drift、非主張境界などを公開用プロトコルとして再構成した別文書である。

```text
旧Optional Axiom atlas
  = 固定研究原資料 / historical stress corpus
            ↓ 研究・監査
SO再帰的哲学研究 Volume I
            ↓ 残差・再構成
現行 Optional Axiom Modules as Cognitive Bridge
  = 公開認識ブリッジ / current protocol
```

## 4. Maintenance Notes / 運用メモ

この固定ソースの本文を、誤字修正、現行用語への置換、header追加、改行正規化その他の理由で暗黙に上書きしない。

内容を修正した版を研究入力として用いる必要が生じた場合は、元ソースを残したまま別のsource identityとして追加し、どの実験がどの入力を使用したかを記録する。

# English Commensurated Rendering

## 1. Directory Role

`sources/` preserves source material actually used in SO Reflexive Philosophical Research without retroactively rewriting it to match later theory.

A file placed here is authoritative **as a fixed research source**, not as a current canonical definition of Scientific Ontology.

Claims contained in a source are not automatically endorsed by the current repository merely because the source is preserved and cited by later research.

## 2. Public Scope

Included:

- fixed inputs actually used in experiments;
- provenance, hashes, and research-use relations needed to identify a source;
- return paths to current documents.

Not included:

- current SO endorsement of every proposition in a source;
- ownership of current SO definitions;
- silently revised versions normalized to later theory;
- guarantees that experiment results are valid.

## 3. Documents

### Optional Axiom Modules

- Repository path: [`Optional_Axiom_Modules.ja.md`](./Optional_Axiom_Modules.ja.md)
- Historical source filename: `0001Optional_Axiom_Modules.md`
- Research role: old Optional Axiom atlas / fixed stress-test corpus
- SHA-256: `20c3fa4f3c82719cf3716b4a52974b433c945143434ffb1a5a47b779fa8ae136`
- Used by: [`Volume I — From De-Registry to Judgment Transparency`](../volumes/Volume_01_DeRegistry_to_Judgment_Transparency/README.md)
- Current public protocol: [`Optional_Axiom_Modules_as_Cognitive_Bridge.en.md`](../../../03_Tam_Goodness/Optional_Axiom_Modules_as_Cognitive_Bridge.en.md)

The preserved source is byte-identical to the fixed fixture identified by the SHA-256 recorded in the Volume I raw-archive index. The hash establishes source identity only; it does not establish correctness, current validity, or repository endorsement.

The current Cognitive Bridge document is a later public protocol and must not be read as a silent replacement or republication of the historical atlas.

## 4. Maintenance Notes

Do not silently normalize or overwrite the fixed source. If a modified input is required for a future experiment, preserve this source and create a new source identity, then record which experiment used which input.

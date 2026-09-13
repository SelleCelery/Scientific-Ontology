# Research Source Index / 研究原資料索引

> Layer: 04_Applications / SO_Reflexive_Philosophical_Research / sources
> Status: README
> Scope: research-source identity / experiment provenance / checksum / return paths / public-private boundary
> Language: ja+en
> Public profile: P1
> Authority: Directory navigation and source-provenance contract; not a Scientific Ontology concept-definition owner

# 日本語正本

## 1. Directory Role / ディレクトリの位置づけ

`sources/` は、SO再帰的哲学研究で用いた原資料について、**公開可能なsource identity、hash、利用関係、返路**を記録するための索引である。

原資料のexact bytesを公開Repositoryへ置くことと、そのsource identityを公開することは分けて扱う。private lineageに属する内容を含む原資料は、実験入力として使用された事実と同一性をhashで記録しても、exact bytes自体は公開Repositoryへ収録しない。

ここに記録されたsource identityは、現在のScientific Ontology全体の教義または公開定義を所有しない。また、原資料に含まれる命題が現在のSOによって承認・再主張されたとは扱わない。

## 2. Public Scope / 公開範囲

公開するもの：

- historical source filename
- source identityを確認するSHA-256
- どの実験・研究で使用されたかというprovenance
- 現行文書と研究記録へのreturn path
- exact bytesを公開しないというpublic/private boundary

公開しないもの：

- private lineageを含むhistorical sourceのexact bytes
- 原資料に含まれる全命題への現在のSOによるendorsement
- 現行SOの定義所有権
- private sourceの内容を復元できる詳細な再掲
- 実験結果の妥当性保証

## 3. Source Identities / 原資料identity

### Optional Axiom Modules

- Historical source filename: `0001Optional_Axiom_Modules.md`
- Research role: old Optional Axiom atlas / fixed stress-test corpus
- SHA-256: `20c3fa4f3c82719cf3716b4a52974b433c945143434ffb1a5a47b779fa8ae136`
- Public handling: **identity-and-hash only; exact bytes not included in the public repository**
- Used by: [`Volume I — De-Registryから判断透明性へ`](../volumes/Volume_01_DeRegistry_to_Judgment_Transparency/README.md)
- Evidence map: [`04_PUBLICATION_AND_EVIDENCE_MAP.md`](../volumes/Volume_01_DeRegistry_to_Judgment_Transparency/04_PUBLICATION_AND_EVIDENCE_MAP.md)
- Current public protocol: [`Optional_Axiom_Modules_as_Cognitive_Bridge.ja.md`](../../../03_Tam_Goodness/Optional_Axiom_Modules_as_Cognitive_Bridge.ja.md)

Volume Iのraw archive indexに記録された固定fixtureのSHA-256と、v5.1公開準備中に照合したsource copyのSHA-256は一致した。このhashは、非公開側で保持するcopyがhistorical inputと同一であるかを照合するために使える。

ただし、hashは内容の妥当性、現在性、SOによるendorsementを保証しない。また、公開Repository単独からhistorical input全文を復元できることも意味しない。

03層の「認識ブリッジとしての選択公理モジュール」は、旧atlasそのものを現在の教義として再公開した文書ではない。旧atlasをstress corpusとして用いた研究履歴を経て、関心・捨象・価値・コスト、Core Invariant、Operational Drift、非主張境界などを公開用プロトコルとして再構成した別文書である。

```text
旧Optional Axiom atlas
  = private exact source / historical stress corpus
            ↓ identity + hash + research provenanceを公開
SO再帰的哲学研究 Volume I
            ↓ 残差・再構成
現行 Optional Axiom Modules as Cognitive Bridge
  = 公開認識ブリッジ / current protocol
```

## 4. Maintenance Notes / 運用メモ

非公開側で保持するhistorical sourceのexact bytesを、誤字修正、現行用語への置換、header追加、改行正規化その他の理由で暗黙に上書きしない。

将来、修正版を研究入力として用いる場合は別のsource identityとSHA-256を与え、どの実験がどの入力を使用したかを記録する。

公開Repositoryでは、private sourceそのものをmanaged assetとして要求しない。公開側が保持するのは、source identity、checksum、研究利用関係、公開境界、およびreturn pathである。

# English Commensurated Rendering

## 1. Directory Role

`sources/` is a public index for **source identity, checksums, research-use provenance, and return paths** for materials used in SO Reflexive Philosophical Research.

Publishing the identity of a research source is distinct from publishing its exact bytes. When a historical input contains material belonging to a private lineage, the public repository may record that the source was used and identify it by hash while withholding the exact source bytes.

A source identity recorded here is not a current canonical definition of Scientific Ontology. Nor does recording a source imply current endorsement of the propositions contained in it.

## 2. Public Scope

Published:

- historical source filename;
- SHA-256 used to identify the source;
- provenance showing which research or experiment used it;
- return paths to current public documents and research records;
- the public/private handling decision.

Not published:

- exact bytes of a historical source that contains private-lineage material;
- current SO endorsement of every proposition in that source;
- ownership of current SO definitions;
- detailed republication from which the private source could be reconstructed;
- guarantees that experiment results are valid.

## 3. Source Identities

### Optional Axiom Modules

- Historical source filename: `0001Optional_Axiom_Modules.md`
- Research role: old Optional Axiom atlas / fixed stress-test corpus
- SHA-256: `20c3fa4f3c82719cf3716b4a52974b433c945143434ffb1a5a47b779fa8ae136`
- Public handling: **identity-and-hash only; exact bytes not included in the public repository**
- Used by: [`Volume I — From De-Registry to Judgment Transparency`](../volumes/Volume_01_DeRegistry_to_Judgment_Transparency/README.md)
- Evidence map: [`04_PUBLICATION_AND_EVIDENCE_MAP.md`](../volumes/Volume_01_DeRegistry_to_Judgment_Transparency/04_PUBLICATION_AND_EVIDENCE_MAP.md)
- Current public protocol: [`Optional_Axiom_Modules_as_Cognitive_Bridge.en.md`](../../../03_Tam_Goodness/Optional_Axiom_Modules_as_Cognitive_Bridge.en.md)

During v5.1 publication preparation, a source copy was checked against the SHA-256 already recorded in the Volume I raw-archive index and the hashes matched. That checksum can identify a privately retained copy as the historical experiment input.

The checksum establishes source identity only. It does not establish correctness, current validity, repository endorsement, or public reproducibility of the full input from the repository alone.

The current Cognitive Bridge is a later public protocol reconstructed after that research history; it is not a republication or silent endorsement of the historical atlas.

## 4. Maintenance Notes

Do not silently normalize or overwrite the privately retained historical source. If a modified input is used in a future experiment, create a new source identity and SHA-256 and record which experiment used which input.

The public repository does not require the private source itself as a managed asset. It retains the public source identity, checksum, provenance relation, publication boundary, and return paths.

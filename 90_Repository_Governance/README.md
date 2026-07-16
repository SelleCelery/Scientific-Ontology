# Repository Governance / リポジトリ統治

> Layer: 90_Repository_Governance
> Status: README
> Scope: publication / commensuration / language authority / concept ownership / terminology governance
> Language: ja+en
> Public profile: P0-P1
> Authority: Directory navigation and maintenance contract; not a concept-definition owner

# 日本語正本

## 1. Directory Role / ディレクトリの位置づけ

`90_Repository_Governance`は、研究内容そのものではなく、公開リポジトリが正本、通約、概念所有、用語、公開境界をどう維持するかを管理する。

ここでいう統治は思考内容を固定することではない。読者が、正本言語、英語通約の保存条件、公開定義所有者、非公開起源、用語衝突を追跡できるようにする公開インターフェース規律である。

### 構造上の位置

```text
研究本文 00–06
  ↔
90 Repository Governance
  ↔
tools / scripts / .github
```

`90`は人間可読な統治文書、`tools`は機械可読なレジストリと文書関係、`scripts`と`.github`は検査実行を担当する。

## 2. Public Scope / 公開範囲

本READMEは、標準科学、法令、政策、既存分野の定義を置き換えるものではない。

含むもの：

- 公開・通約方針
- 翻訳・通約注記
- 用語接続プロトコル
- 用語衝突管理表

含まないもの：

- 理論内容の一括定義
- 私的思考を拘束する内部法則
- 非公開起源の内容
- 法的な知的財産権判断
- 自動検査だけによる意味的一致の保証

## 3. Documents / 文書一覧

1. [`Publication_and_Commensuration_Policy.md`](./Publication_and_Commensuration_Policy.md)
2. [`Translation_Note.md`](./Translation_Note.md)
3. [`Terminology/README.md`](./Terminology/README.md)

## 4. Maintenance Notes / 運用メモ

上流：

- [`../README.md`](../README.md)
- [`../GLOSSARY.md`](../GLOSSARY.md)
- [`../00_Overview/Scientific_Ontology_Concept_Network.ja.md`](../00_Overview/Scientific_Ontology_Concept_Network.ja.md)

機械可読な対応先：

- [`../tools/Public_Format_Registry.yml`](../tools/Public_Format_Registry.yml)
- [`../tools/docs_manifest.yml`](../tools/docs_manifest.yml)
- [`../tools/maintenance_rules.yml`](../tools/maintenance_rules.yml)

- 恒久原則と版固有契約を分ける。
- 人間可読文書とYAMLの意味を同期する。
- 非公開起源を公開定義権限として扱わない。
- 統治文書を理論本文の代替にしない。
- `ja+en`を日本語正本・英語通約の非対称形式として扱う。

# English Commensurated Rendering

## 0. Role

`90_Repository_Governance` manages not the research content itself, but how the public repository maintains authoritative texts, commensuration, concept ownership, terminology, and public boundaries.

Governance here does not freeze thought. It is a public-interface discipline allowing readers to trace the authoritative language, preservation conditions of English commensuration, public definition owners, private origins, and terminology collisions.

## 1. Structural Position

```text
Research texts 00–06
  ↔
90 Repository Governance
  ↔
tools / scripts / .github
```

`90` contains human-readable governance documents, `tools` contains machine-readable registries and document relations, and `scripts` with `.github` execute validation.

## 2. Public Scope

This README is not a replacement for standard science, law, policy, or established disciplinary definitions.

Included:

- Publication and Commensuration Policy;
- Translation and Commensuration Note;
- terminology-connection protocol;
- terminology collision registries.

Not included:

- centralized ownership of all theoretical definitions;
- internal laws restricting private thought;
- private-origin contents;
- legal intellectual-property determinations;
- guarantees of semantic equivalence through automation alone.

## 3. Documents and Reading Order

1. [`Publication_and_Commensuration_Policy.md`](./Publication_and_Commensuration_Policy.md)
2. [`Translation_Note.md`](./Translation_Note.md)
3. [`Terminology/README.md`](./Terminology/README.md)

## 4. Return and Maintenance

Upstream:

- [`../README.md`](../README.md)
- [`../GLOSSARY.md`](../GLOSSARY.md)
- [`../00_Overview/Scientific_Ontology_Concept_Network.ja.md`](../00_Overview/Scientific_Ontology_Concept_Network.ja.md)

Machine-readable counterparts:

- [`../tools/Public_Format_Registry.yml`](../tools/Public_Format_Registry.yml)
- [`../tools/docs_manifest.yml`](../tools/docs_manifest.yml)
- [`../tools/maintenance_rules.yml`](../tools/maintenance_rules.yml)

- Separate durable principles from version-specific contracts.
- Synchronize the meaning of human-readable documents and YAML.
- Do not treat private origins as public definition authority.
- Do not use governance documents as replacements for theory.
- Treat `ja+en` as Japanese authority with English commensuration, not symmetrical bilingualism.

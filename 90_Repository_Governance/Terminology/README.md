# Terminology Governance / 用語統治

> Layer: 90_Repository_Governance / Terminology
> Status: README
> Scope: scientific terminology / canonical terms / English renderings / terminology collisions / public handling
> Language: ja+en
> Public profile: P0-P2
> Authority: Directory navigation and maintenance contract; not a concept-definition owner

# 日本語正本

## 1. Directory Role / ディレクトリの位置づけ

この小分類は、存在境界論の語が既存の学術語、一般語、英語表現と接触するときの公開上の扱いを管理する。

用語を固定して思考を制限する場所ではない。公開語が既存分野の意味へ無自覚に吸収されたり、意図以上に強い主張として読まれたりすることを防ぐ。

詳細な標準語、概念系譜、公開定義所有者は、[`GLOSSARY.md`](../../GLOSSARY.md)が人間可読な入口を担う。

### 構造上の位置

```text
GLOSSARY
標準語・系譜・定義所有
  ↔
Terminology Governance
科学語彙接続・衝突面・公開時の扱い
  ↔
maintenance_rules.yml
機械検査
```

## 2. Public Scope / 公開範囲

含むもの：

- 科学語彙との接続規則
- 日本語正本語の衝突面
- 英語通約語の衝突面
- 誤読方向と公開時の防護条件

含まないもの：

- 全概念の詳細定義
- 既存分野への許可申請
- 語の逸脱や新しい思考の禁止
- 法的な商標・著作権判断
- 用語一致だけによる内容同一性の保証

## 3. Documents / 文書一覧

1. [`Scientific_Terminology_Protocol.md`](./Scientific_Terminology_Protocol.md)
2. [`TERM_COLLISION_REGISTRY.ja.md`](./TERM_COLLISION_REGISTRY.ja.md)
3. [`TERM_COLLISION_REGISTRY.en.md`](./TERM_COLLISION_REGISTRY.en.md)

## 4. Maintenance Notes / 運用メモ

上流：

- [`../../GLOSSARY.md`](../../GLOSSARY.md)
- [`../Publication_and_Commensuration_Policy.md`](../Publication_and_Commensuration_Policy.md)
- [`../Translation_Note.md`](../Translation_Note.md)

機械可読な対応先：

- [`../../tools/maintenance_rules.yml`](../../tools/maintenance_rules.yml)
- [`../../tools/docs_manifest.yml`](../../tools/docs_manifest.yml)

- Glossaryと衝突管理表の責務を混同しない。
- 日本語正本語変更時は英語通約と旧語追跡を同時に確認する。
- 英語の自然さだけを優先して概念所有や非主張境界を失わない。
- 強い誤読領域では明示的な防護条件を置く。
- 用語統治を私的思考の制限へ拡張しない。

# English Commensurated Rendering

## 0. Role

This subdirectory governs the public handling of Scientific Ontology terms when they contact established academic terminology, ordinary language, and English renderings.

It does not freeze language or restrict thought. Its purpose is to prevent public terms from being absorbed unconsciously into established meanings or read as stronger claims than intended.

Detailed canonical forms, conceptual lineage, and public definition owners are presented through [`GLOSSARY.md`](../../GLOSSARY.md).

## 1. Structural Position

```text
GLOSSARY
Canonical terms, lineage, and definition ownership
  ↔
Terminology Governance
Scientific connection, collision surfaces, and public handling
  ↔
maintenance_rules.yml
Machine validation
```

## 2. Public Scope

Included:

- rules for connection with scientific terminology;
- collision surfaces of Japanese authoritative terms;
- collision surfaces of English commensurated renderings;
- likely misreadings and public protective conditions.

Not included:

- detailed definitions of every concept;
- requests for permission from established disciplines;
- prohibition of linguistic experimentation or new thought;
- legal trademark or copyright determinations;
- guarantees of content identity based on terminology matching alone.

## 3. Documents and Reading Order

1. [`Scientific_Terminology_Protocol.md`](./Scientific_Terminology_Protocol.md)
2. [`TERM_COLLISION_REGISTRY.ja.md`](./TERM_COLLISION_REGISTRY.ja.md)
3. [`TERM_COLLISION_REGISTRY.en.md`](./TERM_COLLISION_REGISTRY.en.md)

## 4. Return and Maintenance

Upstream:

- [`../../GLOSSARY.md`](../../GLOSSARY.md)
- [`../Publication_and_Commensuration_Policy.md`](../Publication_and_Commensuration_Policy.md)
- [`../Translation_Note.md`](../Translation_Note.md)

Machine-readable counterparts:

- [`../../tools/maintenance_rules.yml`](../../tools/maintenance_rules.yml)
- [`../../tools/docs_manifest.yml`](../../tools/docs_manifest.yml)

- Do not confuse the responsibilities of the Glossary and collision registries.
- When changing a Japanese authoritative term, review English commensuration and former-term traceability.
- Do not sacrifice concept ownership or non-claim boundaries merely for natural English.
- State explicit protective conditions in high-risk collision fields.
- Do not extend terminology governance into restriction of private thought.

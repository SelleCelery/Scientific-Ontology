# Overview / 概要

> Layer: 00_Overview  
> Status: README  
> Scope: Public navigation, terminology, and publication control

---

## 1. Layer Role / 層の位置づけ

00_Overview は、リポジトリ全体の入口・用語管理・公開方針・主張強度管理を置く層である。理論本文そのものを展開する場所ではなく、存在境界論｜Scientific Ontology の公開文書群をどう読むか、どの語をどの強度で扱うか、どの範囲を公開対象とするかを整理する。

この層は、読者が Sat / Raj / Tam / Applications / Research Notes / Visual Materials へ進む前に、公開名、旧称、用語衝突、標準科学語彙との接続条件を確認するためのナビゲーション層である。

English commensurated rendering: 

00_Overview is the navigation and publication-control layer for the repository. It does not develop the main theoretical body. 

It explains how the public archive should be read, how terminology is controlled, and how claim strength and publication scope are managed before the reader moves into the other layers.

---

## 2. Public Scope and Claim Profile / 公開範囲と主張強度

この層の公開強度は、原則として P0-P1 である。ここで扱うのは、公開説明、用語規約、翻訳・通約規則、公開境界、主張強度の管理であり、非公開中核、実装パラメータ、人格OS、内部評価表を含めない。

この層での「Scientific」は、狭義の自然科学を名乗るという意味ではなく、観測、分類、記述、再照合可能性、境界条件の明示、主張強度管理を重視する方法態度を指す。

English commensurated rendering: 

The default public scope of this layer is P0-P1. It contains public explanation, terminology policy, translation and commensuration rules, publication boundaries, and claim-profile management. 

It does not include private core materials, implementation parameters, persona OS materials, or internal evaluation tables.

---

## 3. Included / Not Included / 含むもの・含まないもの

含むもの:

- 公開体系全体のナビゲーション
- 用語運用規約
- 公開範囲と通約方針
- 主張強度・用語衝突の管理
- 旧称「存在論科学」と公開名「存在境界論｜Scientific Ontology」の整理
- 標準科学語彙を上書きせずに扱うための接続条件

含まないもの:

- AMP Core 全文
- ITS 理論全体
- 非公開公理草案
- 非公開実装スキーマ
- 人格OS・ランタイム仕様
- 非公開素材索引
- 内部評価・監査マップ

English commensurated rendering: 

This layer includes navigation, terminology policy, publication and commensuration policy, claim-profile control, name-transition handling, and rules for using scientific vocabulary without overwriting standard definitions. 

It does not include full private cores, implementation schemas, persona/runtime materials, or unpublished source inventories.

---

## 4. Documents / 文書一覧

- [`Scientific_Ontology_System_Map.md`](./Scientific_Ontology_System_Map.md)
  - 一行説明: リポジトリ全体の層構造、主要概念、公開境界を示す体系マップ。
  - Role: 全体ナビゲーション。
  - Claim profile: Public map / P0-P1.

- [`Scientific_Terminology_Protocol.md`](./Scientific_Terminology_Protocol.md)
  - 一行説明: 標準科学語彙を尊重しながら、存在境界論内での読み替え・再定義・主張強度を管理する規約。
  - Role: 用語運用・科学語彙接続プロトコル。
  - Claim profile: Terminology policy / P0-P1.

関連するルート文書:

- [`Publication_and_Commensuration_Policy.md`](../Publication_and_Commensuration_Policy.md)
  - 一行説明: 公開、通約、用語変更、公開境界管理の方針。
  - Role: リポジトリ全体の公開方針。
  - Claim profile: Policy / P0.

- [`Translation_Note.md`](../Translation_Note.md)
  - 一行説明: 日本語正本と英語通約の扱いを定める注記。
  - Role: 翻訳・通約規則。
  - Claim profile: Policy / P0.

- [`TERM_COLLISION_REGISTRY.md`](../TERM_COLLISION_REGISTRY.md) / [`TERM_COLLISION_REGISTRY.en.md`](../TERM_COLLISION_REGISTRY.en.md)
  - 一行説明: 日本語正本語と英語通約語の衝突・揺れを管理する表。
  - Role: 用語衝突管理。
  - Claim profile: Terminology control / P0.

---

## 5. Maintenance Notes / 運用メモ

### Stable policy / 固定方針

00_Overview は、理論本文を膨らませる場所ではなく、読解経路と公開条件を固定する場所として扱う。ここに理論詳細を追加しすぎない。

### Directory history / 層の変更履歴

- v4 系では、旧称「存在論科学」と公開名「存在境界論｜Scientific Ontology」の関係整理を明示する方向へ移行した。
- 科学語彙の扱いは、標準定義の尊重、読み替えの明示、SO定義の明示、限定条件提示を基本とする。

### File-level changes / ファイル単位の増減

- 体系マップと科学語彙接続プロトコルを本層の中心文書として扱う。
- 全体方針文書は原則としてルートに置き、本層から参照する。

### Pending notes / 保留事項

- ルート README のコンパクト化後、Overview との役割分担を再確認する。

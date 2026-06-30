# Publication and Commensuration Policy / 公開・通約方針

> Status: Policy
> Scope: publication-commensuration
> Language: ja+en

## 0. 位置づけ

本文書は、存在境界論｜Scientific Ontology における公開、翻訳、通約、用語変更、既存タームとの衝突管理の方針を定める。

本プロジェクトの正本言語は日本語である。  
英語版は、日本語正本を逐語的に置き換えたものではなく、概念構造を英語圏へ接続するための通約版である。

---

## 1. 正本言語

Scientific Ontology の正本言語は日本語とする。

用語の定義、射程、注意事項、主張強度、公開境界を判断する場合、日本語記述を優先する。  
英語表記は、既存の英語圏の哲学・科学・AI・社会理論との衝突を考慮しながら調整される。

---

## 2. 翻訳ではなく通約

本プロジェクトにおける translation は、逐語訳ではない。  
それは、日本語正本に含まれる概念構造を、別の言語圏・既存語彙圏へ接続するための commensuration / 通約である。

したがって、英語表記では以下を必要に応じて区別する。

- 日本語正本語
- 英語通約語
- 直訳
- SO上の意味
- 既存タームとの衝突
- 公開時の注意
- 旧表記・置換履歴

---

## 3. 用語変更方針

公開後に語の表記、英訳、定義、射程を変更する場合、その変更を記録する。

同一メジャーバージョン内では、旧語と新語を併記することを基本とする。  
メジャーバージョンアップ時には、主表記を新語へ置換してよい。  
ただし、旧語・変更理由・置換先は用語変更ログに残す。

---

## 4. Research Notes における限定逸脱

Research Notes では、通常公開層よりも強い仮説、比喩、物理接続候補、宇宙論的・意識論的・文学的接続を限定的に扱うことを認める。

ただし、逸脱する場合は以下を明記する。

- 通常公開層を超える理由
- 主張強度
- 何を主張しないか
- 比喩、構造アナロジー、存在論的再解釈、作業仮説のどれか
- なぜ本文ではなく Research Notes に置くのか

---

## 5. 既存タームとの衝突管理

Scientific Ontology の語が、既存の哲学・科学・AI・社会理論・宗教・心理学・医療・創作理論の語と衝突する場合、その衝突を記録する。

衝突管理は `TERM_COLLISION_REGISTRY.md` で行う。

特に以下の語は注意して扱う。

- field / 場
- topology / トポロジー
- entropy / エントロピー
- negentropy / ネゲントロピー
- qualia / クオリア
- observer / 観測者
- law / 法則
- gravity / 重力
- history / 履歴
- ontology / 存在論

---

## 6. 日本語のみファイルの扱い

公開資料は、原則として日本語正本と英語通約版を接続する。

ただし、次の場合は日本語のみのファイルを一時的に認める。

- 未通約の草稿
- 日本語圏向けに限定したい文章
- 英語化すると誤読リスクが高いもの
- 創作・文体・文化的理由により通約が未成熟なもの
- 非公開または公開前の作業資料

その場合は、`Japanese-only draft`、`Not yet commensurated`、`Internal` などの状態表示を付ける。

##  7. 非公開中核境界

公開リポジトリには、AMP Core全文およびITS理論全文を含めません。

AMP Core は、本体系の非公開の公理的原典として扱います。  
ITS理論は、AMPを、情報・時間・トポロジー・観測・通信・位相遷移の語彙を用いて物理位相へ展開する非公開中核理論として扱います。

これらを公開しないのは、無関係だからではありません。  
現段階では、主張強度、解釈密度、科学的または疑似科学的に読まれるリスクが高く、直接公開に適さないためです。

---

# English Commensurated Version

## 0. Status

This document defines the publication, translation, commensuration, terminology revision, and term-collision policy of Scientific Ontology.

The canonical language of this project is Japanese.  
English documents are not simple word-for-word translations. They are commensurated renderings intended to connect the Japanese conceptual structure to English-language contexts.

## 1. Canonical Language

Japanese is the canonical language of Scientific Ontology.

When determining the meaning, scope, claim strength, public boundary, or cautionary notes of a term, the Japanese text takes priority.

## 2. Translation as Commensuration

In this project, translation does not mean literal substitution.

Translation is treated as commensuration: the process of connecting a Japanese conceptual structure to another linguistic and conceptual field.

English renderings should distinguish, when necessary:

- Japanese canonical term
- English commensurated term
- Literal translation
- Intended meaning within Scientific Ontology
- Collision with existing terms
- Public handling
- Deprecated or replaced renderings

## 3. Term Revision Policy

When a public term, rendering, definition, or scope is changed, the change should be recorded.

Within the same major version, old and new terms should generally be shown together.  
At a major version update, the primary term may be replaced.  
However, the old term, reason for replacement, and new term should remain in a terminology changelog.

## 4. Research Notes Exception

Research Notes may contain stronger hypotheses, analogies, physical correspondence candidates, cosmological applications, consciousness-related notes, or literary-ontological readings than the main public layer.

When a note exceeds the standard public layer, it should state:

- why the deviation is necessary
- its claim strength
- what it does not claim
- whether it is a metaphor, structural analogy, ontological reinterpretation, or research hypothesis
- why it belongs in Research Notes

## 5. Term Collision Management

When a Scientific Ontology term collides with existing terminology in philosophy, science, AI, social theory, religion, psychology, medicine, or literary theory, the collision should be recorded.

Collisions are managed in `TERM_COLLISION_REGISTRY.md`.

## 6. Japanese-only Files

Public documents should, in principle, connect the Japanese canonical text with an English commensurated version.

Japanese-only files may be temporarily allowed when they are drafts, culturally specific texts, not yet commensurated, or too risky to render into English without additional context.

Such files should be marked as `Japanese-only draft`, `Not yet commensurated`, or `Internal`.

## 7. Private Core Boundary

The public repository does not include the full AMP Core or the full ITS Theory.

AMP Core is treated as the private axiomatic source text of the system.  
ITS Theory is treated as a private core expansion that unfolds AMP toward a physical-phase model using information, time, topology, observation, communication, and phase-transition vocabulary.

These materials are not excluded because they are irrelevant, but because their claim strength, interpretive density, and risk of scientific or pseudo-scientific misreading are too high for direct public presentation at this stage.
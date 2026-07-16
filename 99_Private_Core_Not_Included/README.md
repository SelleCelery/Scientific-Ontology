# Private Core Not Included / 非公開中核は含まれません

> Layer: 99_Private_Core_Not_Included
> Status: README
> Scope: public boundary notice / excluded private origins / non-disclosure boundary
> Language: ja+en
> Public profile: P0
> Authority: Public boundary notice; not a description of private contents

# 日本語正本

## 1. Layer Role / 層の位置づけ

`99_Private_Core_Not_Included`は、公開リポジトリの外部に非公開中核が存在することと、公開文書がそれらを含まないことを示す境界通知である。

この層は非公開内容の要約、索引、予告ではない。公開体系が、非公開起源に依存しなくても読解可能でなければならないことを確認する。

### 構造上の位置

```text
非公開起源
  ──内容は公開しない──
99 Public Boundary Notice
  ↓
公開定義は01–06とGlossaryだけで理解可能
```

Private lineageは概念系譜を示すが、公開定義所有権を与えない。

## 2. Public Scope and Claim Profile / 公開範囲と主張強度

本READMEは、標準科学、法令、政策、既存分野の定義を置き換えるものではない。

この境界通知の公開プロファイルはP0であり、理論的主張を追加しない。

## 3. Included / Not Included / 含むもの・含まないもの

含むもの：

- 非公開中核を含まないという通知
- 公開と非公開の境界原則
- 公開文書の自己完結性に関する条件

含まないもの：

- 非公開中核の本文、要約、詳細な目次
- 内部プロンプト、ランタイム、評価体系
- 実装パラメータ、運用ログ、未公開正本
- 非公開内容を推測するための手掛かり

## 4. Documents / 文書一覧

- `README.md`：非公開中核を含まないことを示す公開境界通知。

## 5. Maintenance Notes / 運用メモ

このディレクトリには原則として`README.md`のみを置く。

- 非公開項目の具体的内容を追加しない。
- 宣伝的な謎または権威づけに使わない。
- 公開定義が非公開資料なしで理解できるかを確認する。
- 公開除外の実務はルート`.gitignore`に従う。
- 作業ZIPに含まれることと公開追跡されることを区別する。

# English Commensurated Rendering

## 0. Role

`99_Private_Core_Not_Included` is a boundary notice stating that non-public cores exist outside the public repository and are not included in the public documents.

This layer is not a summary, index, or preview of private material. It confirms that the public system must remain intelligible without access to private origins.

## 1. Structural Position

```text
Private origins
  ── contents are not published ──
99 Public Boundary Notice
  ↓
Public definitions remain intelligible through 01–06 and the Glossary
```

Private lineage indicates conceptual history but does not grant public definition ownership.

## 2. Public Scope

This README is not a replacement for standard science, law, policy, or established disciplinary definitions.

Included:

- notice that private cores are not included;
- principles separating public and private materials;
- conditions for the self-sufficiency of public documents.

Not included:

- private-core texts, summaries, or detailed tables of contents;
- internal prompts, runtimes, or evaluation systems;
- implementation parameters, operational logs, or unpublished authoritative texts;
- clues intended to reconstruct private contents.

## 3. Documents and Maintenance

As a rule, this directory contains only `README.md`.

- Do not add concrete descriptions of private material.
- Do not use this layer as promotional mystery or authority signaling.
- Confirm that public definitions remain intelligible without private documents.
- Follow the root `.gitignore` for practical exclusion.
- Distinguish inclusion in a working ZIP from public version tracking.

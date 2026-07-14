# Applications / 応用層

> Layer: 04_Applications / AI_Adaptation
> Status: README  
> Scope: Public application interfaces and non-operational design notes

---

## 1. Layer Role / 層の位置づけ

`04_Applications / AI_Adaptation` は、Sat / Raj / Tam で整理された概念を、AI境界インターフェース、応用境界理論、有用性、人格応答構造などの公開可能な応用文書へ接続する層である。

この層は、実装仕様の公開場所ではない。公開可能な設計思想、使用者の判断可能性を守るインターフェース概念、応答構造としてのAI人格、応用境界理論の入口を置く。

English commensurated rendering: 

`04_Applications/AI_Adaptation` connects the Sat/Raj/Tam conceptual structure to public-facing application interfaces, especially AI boundary interfaces, usefulness, response-structure models, and application boundary theory. 

It is not a place for publishing implementation specifications.

---

## 2. Public Scope and Claim Profile / 公開範囲と主張強度

この層の公開強度は、原則として P1-P2 である。概念応用、公開可能な設計思想、非操作的な応用説明を扱う。実装コード、非公開パラメータ、制御構造、人格OSの詳細は含めない。

English commensurated rendering: The default public scope is P1-P2. This layer contains conceptual applications and public design interfaces. It does not publish implementation code, private parameters, control structures, or persona OS details.

---

## 3. Included / Not Included / 含むもの・含まないもの

含むもの:

- AI境界インターフェースの公開用説明
- AI有用性を境界機能として扱う文書
- AI人格を応答構造として扱う公開用入口
- 応用境界理論の中核説明
- 公開可能な応用設計メモ
- AI導入を境界設計・責任境界・照合可能性として扱う応用文書

含まないもの:

- 実装コード
- 非公開実装スキーマ
- 詳細な運用パラメータ
- AI制御構造
- 人格OS・Soul Core・Runtime Core
- 内部評価ログ
- 非公開シミュレーション仕様

English commensurated rendering: This layer includes public AI boundary-interface documents, usefulness as boundary function, AI personality as response structure, and application boundary theory. 

It excludes implementation code, private schemas, operational parameters, AI control structures, persona cores, internal logs, and non-public simulation specifications.

---

## 4. Documents / 文書一覧

- [`AI_Boundary_Interface_and_Synchronous_Understanding.md`](AI_Adaptation/AI_Boundary_Interface_and_Synchronous_Understanding.md)
  - 一行説明: AIを境界インターフェースとして扱い、同期的理解、偽閉鎖、Open Marker、倫理的制動を説明する。
  - Role: AI境界インターフェースの公開文書。
  - Public profile: Application interface / P1.

- [`AI_Personality_as_Response_Structure.md`](AI_Adaptation/AI_Personality_as_Response_Structure.md)
  - 一行説明: AI人格を、口調やロールプレイではなく、判断可能性を保つ応答構造として扱う。
  - Role: AI人格概念の公開ゲート。
  - Public profile: Application concept / P1-P2.

- [`AI_Usefulness_as_a_Boundary_Function.md`](AI_Adaptation/AI_Usefulness_as_a_Boundary_Function.md)
  - 一行説明: AIの有用性を、ユーザーの判断可能性が保たれる場の維持として定義する。
  - Role: AI有用性の公開用概念インターフェース。
  - Public profile: Application interface / P1.

- [`Application_Boundary_Theory_Core.md`](AI_Adaptation/Application_Boundary_Theory_Core.md)
  - 一行説明: 応用領域における境界理論の中核概念を整理する。
  - Role: 応用境界理論の基礎ノート。
  - Public profile: Application theory note / P1-P2.

---

## 5. Maintenance Notes / 運用メモ

### Stable policy / 固定方針

Applications は、公開可能な応用説明の層である。実装可能性を示す場合でも、非公開パラメータや制御構造は出さない。

### Directory history / 層の変更履歴

- v4 系では、AI関連文書を Tam から Applications へ分離し、Tam を境界倫理・非破壊性の原理層として残した。

### File-level changes / ファイル単位の増減

- AI有用性、AI境界インターフェース、AI人格応答構造、応用境界理論を本層の中心に置く。

### Pending notes / 保留事項

- 実装寄りの内容が増えた場合は、公開文書ではなく非公開開発資料へ退避する。

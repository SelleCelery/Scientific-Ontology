# Tam / Goodness / 暗・善

This layer contains public-facing implementation, control, protocol, and safety-interface materials.

この層には、実装・制御・プロトコル・安全境界に関する公開用資料を置きます。

Included:
- public AI interface notes
- ethics and control overview
- implementation-facing summaries

Not included:
- Persona Runtime Core
- Soul Core details
- Role-AP module parameters
- Boundary Heat Log taxonomy

## Documents / 文書

- `Boundary_Ethics_Model.md`  
  Public conceptual introduction to Boundary Ethics.  
  Defines ethics as non-destructive interaction between histories, and safety as boundary maintenance rather than mere refusal.  
  境界倫理モデルの公開用概念整理。倫理を履歴同士の非破壊的相互作用として定義し、安全を単なる拒否ではなく境界維持として扱う。

- `AI_Usefulness_as_a_Boundary_Function.md`  
  Public conceptual interface for useful AI systems.  
  Defines usefulness as preserving the field in which user judgment remains possible.  
  有用なAIを論じるための公開用概念インターフェース。AIの有用性を、ユーザーの判断可能性が保たれる場を維持することとして定義する。

#### Implementation-facing notes / 実装側ノート

Boundary Ethics and AI Usefulness define the public conceptual interface.
Internally, these ideas are extended into History-Boundary Alignment Design, including rMass/iMass separation, provisional closure, residue handling, heuristic control, and recovery-oriented evaluation.

These implementation-facing details are not fully published in this repository.

境界倫理モデルと「有用性とは境界機能である」は、公開用の概念インターフェースである。
内部ではこれらを、履歴境界設計によるAIアライメント基礎設計へ展開し、rMass/iMass分離、仮閉鎖、Residue処理、ヒューリスティック制御、破綻時復旧評価などを扱う。

ただし、これらの実装寄り詳細は、本リポジトリでは全文公開しない。

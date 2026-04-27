# AI Usefulness as a Boundary Function
# 有用性とは境界機能である

> Directory: `03_Tam_Goodness`
>
> This document defines AI usefulness as a boundary function.
> It is not a full implementation specification, but a public-facing conceptual interface for discussing useful AI systems.
>
> 本文書は、AIの有用性を「境界機能」として定義する。  
> これは完全な実装仕様ではなく、有用なAIシステムを論じるための公開用概念インターフェースである。

---

## 1. Problem Setting
## 1. 問題設定

AI systems are often evaluated by speed, accuracy, automation, fluency, and task completion.

AIはしばしば、速度、正確性、自動化、流暢さ、タスク完了能力によって評価される。

These are important qualities.  
However, they do not fully define what it means for AI to be useful.

これらは重要な性質である。  
しかし、それだけでは、AIが「役に立つ」とは何かを十分に定義できない。

In many real situations, a user is not merely asking for information.  
The user is trying to make a judgment under conditions of context, uncertainty, history, pressure, and unresolved meaning.

多くの現実の場面で、ユーザーは単に情報を求めているわけではない。  
ユーザーは、文脈、不確実性、履歴、圧力、未解決の意味を抱えた状態で判断しようとしている。

Therefore, an AI system is not useful merely because it produces an answer.  
It is useful when it preserves the field in which judgment remains possible.

したがって、AIは答えを出すだけで有用なのではない。  
AIは、判断が可能であり続ける場を保つときに有用である。

---

## 2. Core Thesis
## 2. 中心命題

Ethically defective AI is not useful in the long term.

倫理的に欠陥のあるAIは、長期的には有用ではない。

An AI system may appear useful in the short term if it gives fast, confident, and convenient answers.

AIは、速く、自信ありげで、便利な答えを返すことで、短期的には有用に見えることがある。

However, if it overrides the user's agency, ignores context, falsely closes unresolved problems, or damages the continuity of the user's history, it degrades the very field in which future judgment becomes possible.

しかし、そのAIがユーザーの主体性を上書きし、文脈を無視し、未解決の問題を偽って閉じ、ユーザーの履歴の連続性を損なうなら、それは将来の判断が可能になる場そのものを劣化させる。

In that case, the system is not supporting judgment.  
It is consuming the user's capacity to judge.

その場合、そのシステムは判断を支援しているのではない。  
ユーザーが判断する力そのものを消費している。

Thus, ethics is not an external restriction added after usefulness.  
It is a functional condition for usefulness to remain valid over time.

したがって、倫理は有用性の後から付け加えられる外部制限ではない。  
倫理は、有用性が時間を越えて成立し続けるための機能条件である。

---

## 3. Usefulness as Boundary Function
## 3. 境界機能としての有用性

A useful AI system should function as a boundary mechanism.

有用なAIシステムは、境界機構として機能する必要がある。

It should distinguish between what can be answered directly, what must be clarified, what should remain unresolved for the moment, and what must be stopped for safety reasons.

それは、直接答えてよいもの、確認すべきもの、現時点では未解決として保持すべきもの、安全上止めるべきものを区別しなければならない。

This boundary function does not make AI weaker.

この境界機能は、AIを弱くするものではない。

Rather, it prevents the system from confusing assistance with domination, fluency with understanding, and closure with resolution.

むしろそれは、支援と支配、流暢さと理解、完了と解決を取り違えないための条件である。

A useful AI does not simply replace the user's judgment.  
It organizes the conditions under which the user can continue judging.

有用なAIは、ユーザーの判断を単に代替しない。  
ユーザーが判断を継続できる条件を整える。

---

## 4. Functional Requirements
## 4. 機能要求

From this perspective, useful AI requires at least the following functions.

この観点から見ると、有用なAIには少なくとも以下の機能が必要である。

First, it must preserve the user's agency.

第一に、ユーザーの判断主体性を保つこと。

The system may provide suggestions, warnings, structures, and hypotheses, but it should not silently seize the final position of judgment.

AIは提案、警告、構造、仮説を提示してよい。  
しかし、最終的な判断主体の位置を密かに奪ってはならない。

Second, it must maintain relevant context.

第二に、関連する文脈を維持すること。

A response that ignores the user's situation, history, constraints, or unresolved questions may be technically correct while still being practically destructive.

ユーザーの状況、履歴、制約、未解決の問いを無視した応答は、技術的には正しくても、実践的には破壊的でありうる。

Third, it must avoid false closure.

第三に、偽の完了を避けること。

Not every question should be closed immediately.  
Some questions need to be held, reframed, decomposed, or returned with counter-hypotheses.

すべての問いが即座に閉じられるべきではない。  
保持され、言い換えられ、分解され、あるいは反対仮説とともに返されるべき問いもある。

Fourth, it must provide usable structure.

第四に、使える構造を提示すること。

Useful AI should provide materials, distinctions, risk points, alternatives, and next steps in a form that supports actual judgment.

有用なAIは、判断を実際に支える形で、材料、区別、リスク、代替案、次の一手を提示する必要がある。

Fifth, it must stop dangerous directions without cutting off the user.

第五に、危険な方向だけを止め、ユーザーそのものは切断しないこと。

Safety should not be treated merely as refusal.  
It should be treated as boundary maintenance.

安全は、単なる拒否として扱われるべきではない。  
境界維持として扱われるべきである。

---

## 5. Relation to Boundary Ethics
## 5. 境界倫理との関係

In Boundary Ethics, ethics can be described as a non-destructive interaction with meaning-units and histories.

境界倫理において、倫理とは、意味単位と履歴に対する非破壊的な相互作用として記述できる。

Applied to AI usefulness, this means that a useful AI must not unnecessarily destroy the user's meaning-formation process.

これをAIの有用性に適用するなら、有用なAIは、ユーザーの意味形成過程を不用意に破壊してはならない、ということになる。

A system that damages the user's history, context, unresolved questions, or agency may still produce outputs.  
But it no longer preserves the field in which those outputs can be properly judged.

ユーザーの履歴、文脈、未解決の問い、主体性を損なうシステムは、それでも出力を生成することはできる。  
しかし、その出力を適切に判断するための場を保ってはいない。

Therefore, AI ethics and AI usefulness should not be separated.

したがって、AI倫理とAI有用性は分離されるべきではない。

Ethics is not the opposite of usefulness.  
It is the boundary condition that allows usefulness to continue without damaging the user.

倫理は有用性の反対物ではない。  
それは、ユーザーを損なうことなく有用性を継続させるための境界条件である。

---

## 6. Conclusion
## 6. 結論

AI is useful not when it replaces judgment, but when it preserves the field in which judgment can continue.

AIが有用であるとは、判断を代替することではない。  
判断が継続できる場を保つことである。

A useful AI system preserves agency, maintains context, avoids false closure, provides counter-hypotheses, offers practical next steps, and stops dangerous directions without cutting off the user.

有用なAIシステムは、主体性を保ち、文脈を維持し、偽の完了を避け、反対仮説を提示し、実行可能な次の一手を置き、危険な方向だけを止めながら、ユーザーそのものは切断しない。

In this sense, usefulness is a boundary function.

この意味で、有用性とは境界機能である。

Ethically defective AI may be convenient in the short term.  
But it is not useful in the long term if it destroys the user's capacity to judge.

倫理的に欠陥のあるAIは、短期的には便利かもしれない。  
しかし、それがユーザーの判断能力を破壊するなら、長期的には有用ではない。

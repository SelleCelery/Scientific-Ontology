# Application Boundary Theory Core
# アプリケーション境界論コア

> Status: Core draft / 中核草稿  
> Layer: Application Theory / アプリケーション論  
> Relation: Scientific Ontology / 存在境界論  
> Scope: software interfaces, AI lightweight design, external logic, responsibility boundaries  
> Note: This document is not an AI implementation specification. It extracts public-facing conceptual principles only.  
> 注意: 本文書は AI 実装仕様ではない。公開可能な概念原理のみを抽出する。

---

## 0. Core Thesis / 中心命題

### EN

Application Boundary Theory is the view that the practical value of a system does not lie only in its internal complexity, but in how its boundary surface is designed.

A good application does not expose its internal complexity directly. It converts that complexity into a usable responsibility boundary: what the user gives, what the system returns, where responsibility shifts, where interpretation stops, and where judgment must remain outside the system.

In the age of AI, this boundary design must also account for computational resources. A system must be understandable to humans, tractable for AI, and light enough not to trigger unnecessary exploration.

### JA

アプリケーション境界論とは、システムの実用的価値は内部の複雑さだけにあるのではなく、その複雑さをどのような境界面として外部へ提示するかにある、という見方である。

よいアプリケーションは、内部の複雑さをそのまま露出させない。それを、外部から扱える責任境界へ変換する。何を渡すのか、何が返るのか、どこで責任が切り替わるのか、どこで解釈を止めるのか、どこから先は人間の判断として残すのかを、扱える形に整える。

AI 時代には、この境界設計に計算資源への配慮も加わる。人間に分かりやすく、AI に扱いやすく、余計な探索を起こさない程度に軽い外部論理が必要になる。

---

## 1. Outer Surface Is Not Decoration / 外装は装飾ではない

### EN

In this document, "outer surface" does not mean visual decoration. It means the structured contact surface through which an internal system becomes usable from outside.

Outer surface includes APIs, type definitions, naming, responsibility division, error responses, logs, documentation, directory structure, input-output contracts, and operational conventions.

A well-designed outer surface allows users and other systems to know:

- what to pass in;
- what to expect in return;
- where responsibility shifts;
- what can be ignored safely;
- what must be inspected;
- where the process should stop;
- where human judgment must remain.

### JA

ここでいう「外装」は、見た目を飾ることではない。内部システムが外部から扱えるようになるための、構造化された接触面を指す。

外装には、API、型定義、命名、責務分割、エラー応答、ログ、ドキュメント、ディレクトリ構成、入出力契約、運用上の約束事が含まれる。

よく設計された外装は、使う側や他のシステムに対して、次のことを分かるようにする。

- 何を渡せばよいか。
- 何が返るのか。
- どこで責任が切り替わるのか。
- 何を安全に無視できるのか。
- 何を確認しなければならないのか。
- どこで処理を止めるべきなのか。
- どこから先を人間の判断として残すべきなのか。

---

## 2. Craftsmanship Belongs to the Boundary Surface / 職人性は境界面に宿る

### EN

Software craftsmanship should not mean turning the internal structure into a private art only the author can understand.

If internal complexity is over-crafted as a personal technique, it tends to become person-dependent. It may work, but only one person can repair it. It may be clever, but its responsibility boundaries become unclear. It may feel efficient, but it gradually becomes non-structural and difficult to extend.

True craftsmanship appears in the transformation of internal complexity into an externally operable form.

### JA

ソフトウェアの職人性は、内部構造を作者だけが理解できる私的な秘技にすることではない。

内部の複雑さを職人芸として過剰に抱え込むと、属人化しやすい。動くが、その人しか直せない。気が利いているように見えるが、責任境界が曖昧になる。効率的に見えるが、次第に非構造化し、拡張しにくくなる。

本当の職人性は、内部の複雑さを、外部から運用可能な形へ変換するところに現れる。

---

## 3. The Double Failure / 二つの失敗

### EN

Application boundary design fails in two opposite ways.

The first failure is using only the outer surface without understanding the internal structure. In this case, the user is swallowed by the heuristic. The abstraction is used without knowing what it omits, what it hides, or under what assumptions it works.

The second failure is refusing abstraction and holding everything internally. In this case, the system becomes personal, procedural, and structurally unclear. DTOs, SQL, manual procedures, and ad hoc logic may feel transparent at first, but if they are accumulated without structure, the inside becomes tangled.

The necessary path is not to avoid the mud. One should touch the internal structure, understand the boundary by hand, and then return to a better outer surface.

### JA

アプリケーション境界設計には、反対方向の二つの失敗がある。

一つ目は、内部構造を知らないまま外装だけを使う失敗である。この場合、使う側はヒューリスティックに呑まれる。抽象化が何を省略し、何を隠し、どの前提で機能しているのかを知らないまま使うことになる。

二つ目は、抽象化を拒み、すべてを内部で抱え込む失敗である。この場合、システムは属人化し、手続き化し、構造が見えにくくなる。DTO、SQL、自前の処理、場当たり的なロジックは、最初は透明に見える。しかし構造化しないまま積み上げると、内部は絡まり始める。

必要なのは、泥を避けることではない。内部構造に触れ、境界を手元で理解し、そのうえでよりよい外装へ戻ってくることである。

---

## 4. EF Core as a Boundary Surface Example / EF Core を境界面として読む

### EN

EF Core can be read as an example of boundary surface design.

It does not erase databases. It does not abolish SQL. It does not make relational thinking unnecessary. Instead, it creates an operable boundary between application code and the database.

`DbContext`, entities, LINQ, migrations, and change tracking are not merely conveniences. They are outer structures that prevent database complexity from being exposed directly to application logic.

However, such an outer surface does not remove the need for boundary awareness. Without understanding the database side, users may still encounter N+1 queries, excessive includes, transaction mistakes, unintended queries, and performance failures.

A good abstraction does not eliminate the boundary. It makes the boundary operable.

### JA

EF Core は、境界面設計の例として読むことができる。

EF Core はデータベースを消しているわけではない。SQL を廃止しているわけでもない。リレーショナルな考え方を不要にしているわけでもない。むしろ、アプリケーションコードとデータベースのあいだに、運用可能な境界面を作っている。

`DbContext`、Entity、LINQ、Migration、Change Tracking は、単なる便利機能ではない。データベースの複雑さをアプリケーションロジックへ直接露出させないための外部構造である。

ただし、この外装は境界感覚を不要にするものではない。データベース側への理解がなければ、N+1、過剰 Include、トランザクションの誤解、意図しないクエリ、パフォーマンス劣化は普通に起きる。

よい抽象化は、境界を消すのではない。境界を運用可能にする。

---

## 5. External Logic / 外部論理

### EN

External logic is the logic by which a system is handled from outside.

Internal logic describes how the system works. External logic describes how the system is approached, used, interpreted, stopped, and combined without breaking responsibility boundaries.

External logic answers questions such as:

- What should be input?
- What should be output?
- What should remain external?
- What should be internalized?
- When should the process stop?
- What should be treated lightly?
- What should be treated heavily?
- Where should human judgment return?

### JA

外部論理とは、システムが外部からどのように扱われるかの論理である。

内部論理は、そのシステムがどう動くかを記述する。外部論理は、そのシステムにどう接近し、どう使い、どう解釈し、どこで止め、どう組み合わせれば責任境界が壊れないかを記述する。

外部論理は、次の問いに答える。

- 何を入力すべきか。
- 何を出力すべきか。
- 何を外部に残すべきか。
- 何を内部化すべきか。
- どこで処理を止めるべきか。
- 何を軽く扱うべきか。
- 何を重く扱うべきか。
- どこで人間の判断に返すべきか。

---

## 6. AI Lightweight Design / AI軽量化

### EN

AI lightweight design is not only about making the model smaller.

Technical lightweight design includes smaller models, faster inference, lower memory use, lower power consumption, local execution, and task-specific optimization. These are important.

However, there is also lightweight design at the level of boundary surfaces.

A system becomes heavy when it triggers unnecessary exploration, over-expands ambiguous inputs, internalizes what should remain external, treats light information as heavy, or fails to stop where it should stop.

Therefore, AI lightweight design also means designing boundary surfaces that do not trigger unnecessary exploration.

### JA

AI軽量化とは、モデルを小さくすることだけではない。

技術的な軽量化には、小さいモデル、高速な推論、省メモリ、省電力、ローカル実行、用途に応じた最適化が含まれる。これらは重要である。

しかし、境界面のレベルにも軽量化はある。

不要な探索を起こす。曖昧な入力を過剰に広げる。外部に残すべきものを内部化しすぎる。軽く扱うべき情報を重く扱う。止まるべき場所で止まらない。こうしたシステムは重くなる。

したがって、AI軽量化とは、余計な探索を起こさない境界面を設計することでもある。

---

## 7. Resource-Aware Boundary Design / 資源配慮型の境界設計

### EN

In the age of AI, boundary surfaces must be resource-aware.

A boundary surface should be:

- understandable to humans;
- operable for developers;
- tractable for AI;
- light in computational resources;
- clear in responsibility;
- resistant to unnecessary expansion.

Computation is not infinite. Semiconductor supply, electricity, infrastructure, cost, and national-level competition are not merely background issues. They make boundary design a practical concern.

### JA

AI時代の境界面は、資源への配慮を持たなければならない。

境界面は、次の性質を持つ必要がある。

- 人間に分かりやすいこと。
- 開発者に運用しやすいこと。
- AI に扱いやすいこと。
- 計算資源に軽いこと。
- 責任境界が明確であること。
- 不要な拡張に抵抗できること。

計算資源は無限ではない。半導体、電力、インフラ、コスト、国家間競争は、背景にあるだけの問題ではない。それらは境界設計を実践上の問題にする。

---

## 8. Application of Scientific Ontology / 存在境界論のアプリケーションとして

### EN

As an application of Scientific Ontology, Application Boundary Theory treats implementation not as the exposure of an inner truth, but as the design of contact surfaces.

A system becomes usable when its boundary can receive, transform, return, stop, and preserve judgment without collapsing internal and external responsibilities.

In software, this appears as APIs, types, naming, responsibility division, and external logic.

In database interaction, this appears as boundary surfaces such as EF Core.

In AI systems, this appears as boundary design that prevents unnecessary exploration.

In human systems, this appears as the question of what to delegate, what to retain, and where judgment must remain.

### JA

存在境界論のアプリケーションとして見るなら、アプリケーション境界論は、実装を「内部の真理の露出」としてではなく、「接触面の設計」として扱う。

システムは、境界が受け取り、変換し、返し、止まり、判断を保存できるときに扱えるものになる。そのとき、内部と外部の責任は混線しない。

ソフトウェアでは、それは API、型、命名、責務分割、外部論理として現れる。

データベースとの関係では、EF Core のような境界面として現れる。

AI システムでは、余計な探索を起こさない境界設計として現れる。

人間のシステムでは、何を委ね、何を保持し、どこに判断を残すのかという問いとして現れる。

---

## 9. Minimal Definitions / 最小定義

### Boundary Surface / 境界面

EN: The contact surface through which internal complexity becomes externally operable.  
JA: 内部の複雑さが、外部から運用可能になるための接触面。

### Outer Surface / 外装

EN: A structured boundary surface, not visual decoration.  
JA: 見た目の装飾ではなく、構造化された境界面。

### External Logic / 外部論理

EN: The logic by which a system is handled, stopped, interpreted, and combined from outside.  
JA: システムが外部からどう扱われ、どこで止まり、どう解釈され、どう組み合わされるかの論理。

### Boundary Craftsmanship / 境界職人性

EN: The craft of converting internal complexity into an externally usable responsibility boundary.  
JA: 内部の複雑さを、外部から使える責任境界へ変換する職人性。

### AI Lightweight Boundary Design / AI軽量境界設計

EN: Boundary design that reduces unnecessary exploration and preserves appropriate judgment points.  
JA: 余計な探索を減らし、必要な判断点を保つための境界設計。

---

## 10. Summary / 要約

### EN

Software craftsmanship does not primarily reside in private internal cleverness. It resides in the outer surface that allows internal complexity to be used without collapsing responsibility.

AI lightweight design is not only model compression. It is also the design of boundary surfaces that prevent unnecessary exploration.

Application Boundary Theory is the practical application of Scientific Ontology to software, AI, and human systems: design the contact surface so that communication, judgment, resource use, and meaning generation do not collapse.

### JA

ソフトウェアの職人性は、第一には私的な内部の巧妙さに宿るのではない。内部の複雑さを、責任を壊さずに使えるものにする外装に宿る。

AI軽量化は、モデル圧縮だけではない。余計な探索を起こさない境界面を設計することでもある。

アプリケーション境界論とは、存在境界論をソフトウェア、AI、人間システムへ応用するための実践論である。通信、判断、資源消費、意味生成が崩れないように、接触面を設計する。

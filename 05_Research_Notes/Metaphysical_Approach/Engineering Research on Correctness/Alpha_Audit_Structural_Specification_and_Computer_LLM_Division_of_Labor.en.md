# α Audit — Structural Specification for Machine-Auditing Closure, Contradiction, Spine, and Surplus on a Logical Plane

> Status: Research draft / implementation-specification candidate
> Layer: equivalent to 05_Research_Notes / α-audit implementation design
> Language: English commensurated rendering
> Japanese authoritative source: `α監査_構造仕様と計算機LLM分担設計.ja.md`
> Scope: α audit. β audit appears only as a boundary condition.
> Authority: This document does not rewrite the current canonical text. It consolidates present research judgment into an implementable form on the basis of existing audit research, the 2026-10-17 α-audit pilot, and Boundary Epistemological Critique.
> Non-claim: It does not claim that natural-language documents can be completely reduced to first-order predicate logic. Establishment of closure does not imply truth, consistency of the whole system, or decidability.

---

## 0. Purpose

The purpose of α audit is to take the present logical plane—composed of prose, equations, definitions, and rules—and output, in a re-inspectable structure, what is closed within the assumptions, meanings, scopes, and support relations adopted there; what remains unclosed; where contradictions occur; what constitutes the Spine that makes closure possible; and what remains as surplus not indispensable to the current closure.

α audit does not directly determine whether “the theory is correct about reality.” A theory that is wrong about reality may nevertheless be locally closed under its own premises and inference rules. Conversely, a theory whose content appears plausible may contain broken support, unmarked scope shifts, false closure of unresolved differences, or internal contradictions.

Accordingly, α audit separates at least two axes.

1. **Closure state** — whether the internal requirements currently recognized as necessary for establishing the target proposition or proposition set are satisfied within the present logical plane.
2. **Contradiction state** — whether propositions that cannot be held simultaneously are detected on the same logical plane, concerning the same object, under compatible conditions, times, and scopes.

“Closure established / contradiction detected” is an admissible audit result. The auditor exists in part to detect contradiction; it must not be absorbed into the audited system's inference rules at the moment a contradiction is found.

---

## 1. Relation between α Audit and the Completeness-Theorem Side

This research designs α audit by reference to the completeness-theorem side.

It does not directly transplant the completeness theorem of formal logic into natural language. The design reference is narrower: for a proposition treated as established on a given plane, it should be possible to construct an establishment path using premises, rules, and support permitted on that plane.

In formalized regions, the design prototype may be viewed in:

$$
\Gamma \models \varphi \Rightarrow \Gamma \vdash \varphi
$$

Natural-language audit, however, does not assume that semantic consequence can be completely decided by machine. What α checks in implementation is whether the propositions, definitions, rules, support relations, and scopes adopted on the current logical plane can be converted into an explicit structure, and whether an internal path to the target proposition can be inspected.

Failure to detect a contradiction in α audit does not establish consistency of the whole system. The result is limited to: no contradiction reached by the current detectors within the currently extracted plane. Likewise, a proposition being closed on the current plane does not imply decidability of the entire system. This outside region marks a boundary toward β audit.

---

## 2. Basic Objects

### 2.1 Logical Plane

A logical plane is the set of propositions, definitions, inference and transformation rules, support relations, scopes, and unresolved differences that are currently handled together as one system.

When symbols are used, the Japanese-side objects are conceptually fixed first; the following symbols are implementation aliases.

- Let the proposition set be $P$.
- Let the rule set be $R$.
- Let the support-relation set be $S$.
- Let the scope and condition set be $C$.
- Let the unresolved-difference and residual set be $Q$.

The logical plane is written as:

$$
L=(P,R,S,C,Q)
$$

This $L$ is not the world itself. It is a plane cut from the current document or system into a form that can be audited.

### 2.2 Proposition Unit

A proposition unit preserves its source location and at least the following fields:

- proposition identifier;
- source text;
- source file, section, line, or number;
- parent proposition;
- object;
- asserted content;
- polarity (affirmative / negative / unspecified);
- conditions;
- scope;
- time or temporal condition;
- modality / claim strength;
- definition reference;
- explicit unresolved status;
- extraction method;
- type of extraction evidence, rather than an undifferentiated “confidence score.”

Unknown concepts must not be silently translated into known ones. Even when their meaning cannot yet be fixed, they can be retained as opaque nodes and audited in terms of how those nodes connect to other propositions.

### 2.3 Relations

At minimum, relations among propositions distinguish:

- definition;
- support;
- premise;
- condition;
- derivation;
- restriction;
- negation;
- exception;
- join;
- branch;
- external reference;
- reopening condition;
- handoff of an unresolved issue.

The existence of a relation must be distinguished from the correctness of that relation. If an LLM reads something as “apparently a support relation,” that is candidate generation, not a confirmed relation.

---

## 3. Closure

### 3.1 Working Definition of Closure

For a target proposition or proposition set, trace the premises, definitions, conditions, support, and transformations recognized within the present plane as necessary for its establishment. If no unsatisfied mandatory requirement remains, the target is treated as locally closed on the present plane.

The important point is not to define closure as “having no external connections.” A closed structure may retain ports to the outside. An external connection that is required for current establishment but remains unsupplied is called a **mandatory opening**.

Local closure may therefore hold even when external ports exist, so long as no mandatory opening remains unsatisfied.

### 3.2 Closure Operator

Let $K$ be an operation that adds the premises, definitions, conditions, and support required to establish a proposition set.

For a target set $X_0$, repeat:

$$
X_{n+1}=K(X_n)
$$

If, at some stage:

$$
K(X_n)=X_n
$$

and no unsatisfied mandatory opening remains, the structure becomes a closure candidate.

A fixed point produced only by circular reference does not count as closure. If A supports B and B supports A, while neither reaches an external premise, explicit premise, definition, observation, or adopted axiom, the structure is separately detected as circular support.

### 3.3 Closure States

Closure state is not restricted to a binary flag.

- **Closure established:** no mandatory opening remains, and the support structure is auditable.
- **Closure not established:** a mandatory opening, support break, unsupported join, or similar defect can be identified.
- **Indeterminate:** the current extracted structure lacks enough information to decide closure or non-closure.

The mere presence of words such as “unresolved,” “residual,” or “false closure” in the source text is not evidence that closure has failed. A document discussing unresolved states as its object language is different from the proposition structure itself being unclosed.

### 3.4 Provisional Closure

Being reopenable through external recollation, falsification, or additional observation is compatible with being closed internally on the present logical plane.

Closure recognized by α audit is therefore, in principle, local, history-bearing, reopenable **provisional closure**. It does not mean final truth or closure of the world as a whole.

---

## 4. Composite Closure

### 4.1 Closure Is Not Always a Simple Union

When multiple closed structures contact one another, relations may arise that did not exist while each was closed independently, producing a larger closure.

For two closed structures $C_1$ and $C_2$, a new closure $C_3$ need not be the simple set union:

$$
C_3=C_1\cup C_2
$$

If contact opens part of the earlier relation structure and new connections form, it may be that:

$$
K(C_1\cup C_2)\supsetneq C_1\cup C_2
$$

The added elements may include new derivations, joining propositions, resetting of scopes, or connection through a shared concept.

α audit therefore targets not only closure of individual propositions but also the joins through which multiple local closures compose a higher-level closure.

### 4.2 Join Points

A join point is a position where one local closure receives a mandatory opening or explicitly stated insufficiency left by another.

Join-point candidates include expressions such as:

- “therefore, X is required”;
- “X alone is not sufficient”;
- “the difference remaining here is handled as Y”;
- “under this condition A, under another condition B”;
- a relation in which the next section defines, supports, or repositions an unresolved issue left by the previous section.

An LLM may extract join candidates. Closure establishment itself is computed on the explicit graph.

---

## 5. Contradiction

### 5.1 Keep Closure and Contradiction Independent

α audit retains closure and contradiction as separate axes.

All of the following are admissible results:

- closure established / no contradiction detected;
- closure established / contradiction detected;
- closure not established / no contradiction detected;
- closure not established / contradiction detected;
- indeterminate.

Even when the audited system adopts classical logic, the audit meta-layer must not fall into explosion after contradiction is detected. It must retain opposing propositions and their respective support paths simultaneously and isolate the location as a contradiction site.

### 5.2 Normalization of Contradiction Candidates

Natural-language contradiction detection must not rely only on lexical opposites. At minimum, compare:

- whether the object is the same;
- whether the predicate or relation is the same;
- whether polarity is opposed;
- whether the conditions are compatible;
- whether the scopes overlap;
- whether the relevant times overlap;
- whether the claim strengths are comparable.

For example, “A” and “under condition X, not A” are not confirmed as contradictory until it is established whether condition X falls within the first statement's scope.

The LLM extracts candidate-equivalent propositions and candidate-negation relations. Deterministic computation compares normalized conditions, scopes, and times; cases that cannot be confirmed remain pending contradiction candidates.

### 5.3 Non-Proof of Consistency

Failure to detect contradiction in α audit must not be promoted into a claim that the whole system is consistent.

The output should not say “no contradiction.” In principle it should say: **no contradiction detected on the current plane, under the current extraction, by the current detectors**.

---

## 6. Spine

### 6.1 Target Dependence of Spine

A document need not contain exactly one Spine. Spine changes depending on which closure is being examined.

Let the family of minimal closure structures for a target proposition $T$ be:

$$
\mathcal{C}_T=\{C_1,C_2,\ldots,C_n\}
$$

As one implementation candidate, the portion common to every minimal closure structure can be treated as a Spine candidate:

$$
Spine(T)=\bigcap_{i=1}^{n} C_i
$$

This is an implementation candidate, not a uniquely fixed definition at the present stage.

### 6.2 Removal Test

In implementation, remove nodes or relations one by one and test whether closure of the target proposition remains.

- If removing an element destroys every closure path: Spine candidate.
- If closure remains through another path: alternative support or redundant support.
- If the target closure is unaffected: surplus candidate.

If multiple completely independent closure paths exist, the common Spine may be empty. The auditor must not force a Spine into existence.

### 6.3 Roles Change between Local and Higher-Level Closure

A proposition that is surplus in a small closure may become part of the Spine when it joins several closures in a higher-level structure. Every Spine or surplus determination must therefore be tagged with the identifier of the target closure.

---

## 7. Surplus

What is not indispensable to closure must not be collapsed into “unnecessary material.” At minimum, distinguish the following.

### 7.1 Expressive Surplus

Notation, word order, metaphor, rhetoric, symbol choice, and similar features that remain in the source after the logical structure has been normalized. Expressive surplus is not identical with semantic surplus.

### 7.2 Redundant Support

An alternative route for closing the target proposition. Closure survives removal because another route exists, but the route may still matter for fault tolerance, extension under different conditions, or provenance tracing.

### 7.3 Unused Connection Potential

A relation not used by the present target closure but potentially usable as a join point to another closure, a future extension, or a reopening route.

### 7.4 Unresolved Residual

A difference retained outside the present target closure. A local closure may still hold if the unresolved residual is not part of the establishment conditions of that closure.

### 7.5 Semantic Surplus

Meaning that acts in the source text but cannot be adequately mapped into the present logical intermediate representation. Semantic surplus requires LLM or human interpretation and cannot be confirmed by deterministic computation alone.

Surplus is not a failure of closure. Zero surplus must not be an α-audit success condition.

---

## 8. Separation of Responsibilities among Computer, LLM, and Human

For α audit to work, natural-language interpretation, deterministic computation, and final adjudication must not be concentrated in one agent.

### 8.1 Responsibilities of Deterministic Computation

The computer handles operations that can reproduce the same result from the same input and the same rules.

1. Fix the target file set, version, and hashes.
2. Acquire proposition numbering, heading hierarchy, explicit links, and definition references.
3. Validate LLM output format.
4. Construct proposition and relation graphs.
5. Separate explicit, structural, and inferred relations.
6. Iterate closure operators and compute fixed points.
7. Detect mandatory openings, Cuts, Unsupported Joins, and circular support.
8. Compare contradictions among normalized propositions.
9. Search for minimal closure structures.
10. Compute Spine candidates, alternative support, and surplus candidates through removal tests.
11. Generate the audit certificate.
12. Compute differences from the previous audit.

The computer does not autonomously complete the meaning of natural language. It does not invent relations absent from the input structure.

### 8.2 Responsibilities of the LLM

The LLM extracts computable structural candidates from natural language. It is not the final closure adjudicator.

1. Segment proposition candidates.
2. Extract candidate relations such as definition, support, premise, condition, restriction, negation, exception, join, and branch.
3. Generate normalization candidates for object, predicate, polarity, condition, scope, time, and claim strength.
4. Propose synonym and paraphrase candidates.
5. Propose contradiction candidates.
6. Propose implicit-premise candidates.
7. Extract candidate unresolved differences, external references, and reopening conditions.
8. Flag candidate semantic surplus that does not map into the current logical intermediate representation.

Do not ask the LLM directly, “Is this text closed?” The LLM's role is limited to creating candidate structures required for closure computation.

### 8.3 Responsibilities of the Human

The human owns the logical plane being audited and the research meaning of the audit.

1. Fix the audit target, version, scope, and purpose.
2. Approve what range is to be treated as one logical plane.
3. Decide whether a new concept may be replaced by an existing concept.
4. Approve, reject, or suspend ambiguous relations inferred by the LLM.
5. Adjudicate conflicts of scope, time, and condition.
6. Interpret the theoretical meaning of structural determinations such as Spine and surplus.
7. Decide whether and how α-audit results return to canonical texts, research notes, or implementation.

AI does not replace the human as the judgment subject. Nor does the human need to manually read every item. What should return to the human first are differences machines cannot decide, differences that can change the conclusion, and structurally high-impact points.

---

## 9. Evidence Hierarchy for Relations

Extracted relations are separated by the basis on which they are established.

### 9.1 Explicit Relation

A relation directly indicated by the source itself.

Examples:

- “A means B.”
- “If A, then B.”
- “Therefore B.”
- “A alone is insufficient.”
- “B is required.”
- an explicit reference or definition link.

### 9.2 Structural Relation

A relation obtainable from document structure with little or no semantic interpretation.

Examples:

- 7.3.1 is subordinate to 7.3;
- a proposition belongs under a heading;
- an explicit reference target exists;
- the same definition identifier is used.

### 9.3 Inferred Relation

A relation that requires semantic interpretation by an LLM.

Examples:

- one proposition is an implicit premise of another;
- two different expressions refer to the same proposition;
- an example supports a general proposition;
- one paragraph receives an unclosed issue left by the preceding section.

Every inferred relation must preserve its source location and the reason for inference. A closure that holds only through inferred relations must not be reported with the same evidential strength as a closure that holds through explicit and structural relations alone.

---

## 10. Handoff Structure

The center of α audit is not handing a “summary of the text” from the LLM to deterministic computation. It is handing over structured records that preserve a path back to the source.

### 10.1 Source-Proposition Record

```text
Proposition ID:
Source file:
Source location:
Source text:
Parent proposition:
Object:
Assertion:
Polarity:
Conditions:
Scope:
Time:
Claim strength:
Definition references:
Explicit unresolved marker:
Extraction evidence:
Extractor:
Pending items:
```

### 10.2 Relation-Candidate Record

```text
Relation ID:
Source proposition:
Target proposition:
Relation type:
Evidence type: explicit / structural / inferred
Source location supporting the relation:
LLM inference rationale:
Machine-validation state:
Human-adjudication state:
```

### 10.3 Closure-Unit Record

```text
Closure-unit ID:
Target proposition:
Logical-plane ID:
Included propositions:
Relations used:
Support origins:
Mandatory openings:
External ports:
Circular support:
Closure state:
Contradiction state:
Contradiction candidates:
Spine candidates:
Alternative support:
Surplus candidates:
Unresolved residuals:
Reopening conditions:
```

### 10.4 α-Audit Certificate

```text
Target version / hash:
Auditor version:
LLM extractor version:
Logical plane:
Target closure:
Accepted relations:
Rejected relations:
Pending relations:
Closure-computation trace:
Mandatory openings:
Contradictions detected:
Spine removal tests:
Surplus classification:
Indeterminate regions:
Human adjudication items:
Re-audit conditions:
```

The certificate is not a proof of truth. It is a re-collation surface for returning to the inputs, extractions, relations, and calculations that produced the current α result.

---

## 11. Execution Process

α audit is divided into the following stages.

### Stage A — Fix the Target

Deterministic computation fixes the target files, versions, hashes, target sections, and audit purpose. If the target changes, the same audit result is not reused.

### Stage B — Deterministic Preprocessing

The computer extracts headings, numbering hierarchy, explicit links, definition references, equations, lists, and related structural features.

### Stage C — LLM Structural-Candidate Extraction

The LLM outputs proposition, condition, scope, and relation candidates. It does not output a closure determination. It does not automatically translate unknown concepts into known theories.

### Stage D — Handoff Validation

The computer validates record format, source locations, reference consistency, duplicates, and missing fields. LLM output that cannot return to the source is not admitted as audit evidence.

### Stage E — Construct the Logical Plane

A proposition graph is built while explicit, structural, and inferred relations remain separated. Scope, conditions, and time remain separate attributes.

### Stage F — Closure Search

Trace required relations backward from the target proposition and iterate the closure operator. Detect mandatory openings, support breaks, unsupported joins, and circular support.

### Stage G — Contradiction Search

Search for opposed normalized propositions on the same plane. Differences in condition, scope, or time prevent immediate classification as contradiction.

### Stage H — Spine and Surplus Analysis

Compute minimal closure structures, removal tests, and alternative routes; output Spine candidates, redundant support, and surplus candidates.

### Stage I — Generate Falsification Candidates

If the LLM is used again, its role at this stage is not to finalize the audit result. It generates candidate missed implicit premises, scope conflicts, contradiction candidates, or alternative closure candidates. New candidates return to Stage D and pass through the same validation path.

### Stage J — Human Adjudication

The human adjudicates ambiguous points that change the result, inferred relations, high-impact Spine candidates, and contradiction candidates. Approval, rejection, or suspension is recorded.

### Stage K — Recompute and Fix the Certificate

The computer recomputes using the adjudication results and fixes the α-audit certificate.

---

## 12. Boundaries inside the Auditor

### 12.1 Do Not Promote the LLM's Internal Sense of Coherence into Judgment

An LLM can infer contextual coherence, semantic proximity, and implicit relations at high capability. Yet these inferences are inseparable from its capacity to complete natural language toward known patterns.

In auditing novel theory, that completion capacity can generate false closure. The LLM's sense that “this hangs together” is therefore used only to generate structural candidates.

### 12.2 Permit Unknown Concepts as Opaque Nodes

α audit must work even when it cannot understand a novel concept through external knowledge.

For an unknown concept X, even if X cannot be translated into an existing concept Y, it is still possible to audit:

- in which proposition X is defined;
- which propositions depend on X;
- under which conditions X is negated or restricted;
- which closures fail if X is removed.

### 12.3 The Auditor's Meta-Layer Must Tolerate Contradiction

Even if both $P$ and $\neg P$ are supported inside the audited system, the auditor preserves and reports both support paths. The auditor itself must not derive arbitrary propositions from the audited system's contradiction.

---

## 13. Relation to Existing Mechanisms

The 2026-10-17 α-audit pilot decided not to extend the existing Repository machine audit into α, but to establish a separate lane. That decision is retained.

The existing Repository machine audit handles deterministic observations such as files, Manifest entries, links, contract fields, and structural consistency. α audit operates above that surface and addresses logical planes, closure units, support paths, contradictions, Spine, and surplus.

The pilot showed that directly using words such as “unresolved” or “residual” in the source as OPEN-status indicators fails because it confuses object language with audit state. It also showed that document-level logical contracts are too coarse to distinguish a document's closure kernel from its open research region.

The next α implementation therefore forms closure units from propositions, sections, and support bundles rather than treating the entire document as one unit.

---

## 14. First Test through Boundary Epistemological Critique

`Boundary_Epistemological_Critique` is suitable as the first α-audit test object.

Reasons include:

- each statement is written as a numbered proposition;
- child numbers have a structure that presupposes higher-level propositions;
- there are many joining expressions such as “therefore,” “however,” “is required,” and “does not close with X alone”;
- synchronization, collation, and residual retention progress from local closure toward composite closure;
- the conclusion and Appendix A contain author-side compression and skeleton descriptions that can be used for comparison against audit output.

### 14.1 Information Hidden from the Auditor during the Test

To avoid self-circular audit results, at least the following should be isolated on the answer-comparison side:

- the final compression in Chapter 15;
- the “skeleton of the text” declaration in Appendix A.6.

If necessary, the summary in Chapter 0 can also be separated between target-proposition presentation and Spine extraction.

### 14.2 Major Test Points

The first test should check at least the following.

1. Can “synchronization” in Chapter 7 be extracted as a local closure candidate?
2. Can 7.3.5–7.4 be detected as the join from synchronization closure toward collation?
3. Can “collation” in Chapter 8 be extracted as a separate local closure?
4. Can 8.5–8.8 retain the residual and limit structure of collation?
5. Can 9.1 be treated as a declaration of a mandatory opening: “synchronization + collation alone does not close”?
6. Can 9.10 be treated as a local closure condition for residual retention?
7. Can a higher-level closure composed from Chapters 7–9 be reconstructed?
8. Can removal tests determine whether Chapter 5 functions as a main Spine, a closure-monitoring constraint, or a different closure?
9. Can Chapters 2–4, 6, and 10–14 be placed computationally as Spine, extension, surplus, or separate closure relative to the main closure?
10. Can the final result be compared against Chapter 15 and Appendix A as an answer check, reporting both agreement and disagreement?

Perfect agreement is not the success criterion. The author's own self-description can itself become an audit object. What matters is whether differences can be returned to source positions and structural calculations.

---

## 15. Success Conditions

The first-stage success conditions for the α auditor are:

1. Do not directly delegate closure determination to the LLM.
2. Every determination can return to source propositions and relation records.
3. Explicit, structural, and inferred relations are not conflated.
4. Closure and contradiction are reported independently.
5. “No contradiction detected” is not promoted into whole-system consistency.
6. Simple cycles are not mistaken for closure.
7. A document is not classified as unclosed merely because the word “unresolved” appears in it.
8. Local closure and composite closure can be distinguished.
9. Spine is allowed to vary by target closure.
10. Surplus is not automatically deleted as an error.
11. Unknown concepts can be audited as opaque nodes without being completed into known concepts.
12. Indeterminate can be returned as a normal result.
13. Closure, contradiction, and Spine calculations are reproducible from the same target version and accepted relations.
14. If an LLM inference is changed, the resulting difference in output can be computed.
15. A human can inspect how the audit result was established and correct erroneous extraction, relation, or scope assignments.

---

## 16. Boundary toward β Audit

α audit examines closure, contradiction, Spine, and surplus within the present logical plane.

Even if closure is established and no contradiction is detected in α, the system has not thereby proven its own consistency. Nor does it mean that every proposition in the system is decidable.

β audit begins from this limitation and moves toward structural health involving self-reference, externalization, commensuration with other planes, and the return of audit results that moved outside the plane. The α certificate may therefore become an input to β, but α output does not substitute for β.

---

## 17. Unresolved Issues at the Present Stage

1. The minimal relation set to include in closure operator $K$.
2. How far “required for establishment” can be decided using explicit relations alone.
3. Whether an inferred relation, once human-approved, should be promoted to equal status with an explicit relation or retain its provenance permanently.
4. Computational complexity and approximation methods for enumerating minimal closure structures.
5. Whether Spine should be defined through the intersection of minimal closure families or combined with cut points, dominators, and removal impact.
6. Conditions for deciding that “a new relation was generated” in composite closure.
7. How to distinguish semantic surplus from extraction failure.
8. Accuracy of normalization for condition, scope, and time.
9. How to determine the granularity of one logical plane.
10. How much search for defeating candidates within the present plane must be included as a mandatory condition of closure determination.
11. A shared kernel for mapping mathematical and natural-language forms into the same intermediate representation.
12. From which separate system the α auditor itself should be audited. This returns to the β side.

---

## 18. Minimal Implementation Policy

The next implementation should not modify the existing Repository machine audit so as to absorb α. It should be built as an independent α lane.

The minimal implementation sequence is:

```text
fix source text
  ↓
deterministic document-structure extraction
  ↓
LLM proposition and relation candidate extraction
  ↓
candidate-record validation
  ↓
logical-plane graph construction
  ↓
closure search
  ↓
contradiction search
  ↓
Spine and surplus analysis
  ↓
LLM falsification-candidate generation
  ↓
revalidation and recomputation
  ↓
human adjudication
  ↓
fix α-audit certificate
```

The first target is `Boundary_Epistemological_Critique.ja.md`, using its numbered propositions directly as audit units wherever possible.

If the first test cannot extract composite closure, contradiction candidates, join points, Spine, and surplus in a form that can return to the source, do not generalize immediately to ordinary prose.

---

## 19. Present Compression

α audit is not a mechanism that uses an LLM's “this seems coherent” impression as a closure determination.

The LLM extracts propositions and relation candidates from natural language.

Deterministic computation fixes those candidates as explicit structure and computes closure, contradiction, Spine, and surplus.

The human adjudicates the boundary of the logical plane and ambiguous semantic relations, and decides how audit results return to theory.

Closure is not disappearance of external connection. It is a local state in which the mandatory openings required to establish the present target are satisfied.

Closure is not consistency. A closed system may contain contradiction; contradiction detection must therefore run independently.

Spine is the indispensable structure that establishes a target closure. Surplus, while unnecessary for the present closure, may still serve as alternative support, part of another closure, a reopening path, or material for later generation.

The output of α audit is not a declaration of truth. It is a **structural certificate that makes it recomputable what closes the present logical plane, where it contradicts itself, what remains, and from where it can reopen**.

---

## Reference Basis

This document was constructed with reference at least to:

- `正しさ・個性・無・切断_論理通信トポロジー.ja.md` — 01_Sat_Truth / engineering operational definition of “correct,” internal establishment, support paths, Absence and Cut, communication topology, reopening.
- `論理平面・論理深度・次元変換から読むαβ監査試論.ja.md` — research note / earlier working definition of α as internal validity on a logical plane. The β portion remains under re-examination.
- `存在境界論における監査理論.ja.md` — research draft / separation of adjudication and audit, responsibility boundary between detector and judgment, and pre-audit of audit itself.
- `ALPHA_AUDIT_PILOT_REPORT.ja.md` — 2026-10-17 implementation pilot / separation between existing machine audit and α, failure caused by confusing object language with audit state, and excessive coarseness of document-level audit.
- `Boundary_Epistemological_Critique.ja.md` — 01_Sat_Truth / first α-audit test candidate. Numbered propositions concerning synchronization, collation, residual retention, false closure, and re-collatable provisional closure.

The division of responsibilities among deterministic computation, LLM, and human; the closure operator; composite closure; formalization of Spine through minimal closure families; and the handoff records proposed in this document are **implementation hypotheses** constructed from the above materials and the current research conversation. They are not pre-existing specifications of the current canonical text.

# Claim Strength and Publication-Layer Table for Scientific Ontology

> Status: Public control table  
> Scope: claim strength / epistemic risk / use and safety risk / publication layer / verification / rendering distance  
> Language: English commensurated rendering  
> Japanese authoritative source: ./Claim_Strength_and_Publication_Layer_Table.md  
> Claim strength: classifier  

---

## 0. What This Table Governs

This table is a public control table for distinguishing and managing the following dimensions of propositions, documents, and terminology in Scientific Ontology:

- The strength of the proposition itself
- The likelihood of misreading or criticism
- Risks arising from application or transfer
- The degree of deceleration required for publication
- Future stages of verification and formalization
- The distance from core vocabulary to the language games of other fields

These are not the same scale.

A strong claim is not necessarily empirically established.

A high risk of misreading does not mean that the proposition is false.

High applicability does not mean that something should be published.

A lower publication layer does not mean lower importance.

The labels in this table do not confer authority or establish rankings for readers.

They are used to manage what may be stated in which context, where qualification is required, what must remain reserved, and from which point responsibility should be delegated to another document.

---

## 1. Evaluation Order

S / E / U / P / V / R are not parallel scores.

- **S / Claim Strength:** How strong an ontological or theoretical claim the proposition itself makes.
- **E / Epistemic Risk:** Risks of misreading or criticism, including collision with established fields, pseudoscientific interpretation, and overgeneralization.
- **U / Use Risk:** Risks of transfer into diagnosis, manipulation, governance, safety avoidance, or other applications.
- **P / Publication Layer:** The final publication layer determined in light of S, E, and U.
- **V / Verification Stage:** The stage of verification or formalization that may be pursued next.
- **R / Rendering Distance:** The distance through which public core vocabulary is projected into another language game, application field, physical-near vocabulary, or metaphysical layer.

Evaluation proceeds in the following order.

```text
1. Confirm the proposition's claim responsibility and scope of application.
2. Determine claim strength using the S code.
3. Assign a provisional publication layer, P_base, from the S code.
4. Apply deceleration for epistemic and critical risk using the E code.
5. Apply abstraction or non-public handling for use and safety risk using the U code.
6. Use the R code to identify the language game into which the proposition is projected.
7. Determine the final publication layer, P_final.
8. Manage the future verification or formalization stage separately using the V code.
```

In simplified form:

```text
P_final = decelerate(P_base(S), E, U, context(R))
```

R does not independently determine whether publication is permitted.

However, R4 or R5 vocabulary is more likely to approach E3 even where the wording is otherwise unchanged. It therefore requires stronger qualification and more explicit non-claim boundaries than ordinary public vocabulary.

---

## 2. S Code — Claim Strength

| Code | Label | Meaning | Default public handling |
|---|---|---|---|
| S0 | Terminological organization | A working definition, index, or classification internal to the framework, without a strong claim toward an external theory. | P0 by default. |
| S1 | Structural analogy | Compares structurally similar relations across different domains. | State explicitly that the relation is analogical or comparative. |
| S2 | Ontological reinterpretation | Rereads an existing object or phenomenon through boundary, history, return, or related concepts. | Publish with stated limiting conditions. |
| S3 | Working hypothesis | Used for explanation or connection within the framework, but not yet sufficiently verified externally. | Mark explicitly as a hypothesis or exploratory model. |
| S4 | Formalization candidate | A candidate that may be expressed through state variables, operations, update rules, mapping tables, or evaluation indicators. | Handle carefully in Overview documents or Research Notes. |
| S5 | High-strength ontological or scientific candidate | A strong proposition that may directly engage established fields concerning things-in-themselves, physics, life, consciousness, or related domains. | Do not allow it to govern the ordinary public layer directly; apply strong deceleration or keep it non-public. |

### 2.1 Provisional Publication Layer Derived from S

| S | P_base | Basic rationale |
|---|---|---|
| S0 | P0 | Publicly manageable as terminology, classification, or indexing. |
| S1 | P0-P1 | Publicly manageable as structural comparison, but must not be presented as fact. |
| S2 | P1 | An ontological reinterpretation whose scope of application must be stated. |
| S3 | P1-P2 | Publish as a working hypothesis and distinguish it from established theory. |
| S4 | P2 | Place in an Overview document or Research Notes as a formalization candidate. |
| S5 | P2-P3 | Prioritize internal examination within a high-strength research layer. |

---

## 3. E Code — Epistemic Risk

| Code | Label | Primary risk | Required handling |
|---|---|---|---|
| E0 | Low | Little likelihood of misunderstanding as an ordinary definition or index entry. | Ordinary publication. |
| E1 | Definition risk | Insufficient terminology or scope may cause misunderstanding. | Add definitions, examples, or related-document links. |
| E2 | Disciplinary collision | May be read as replacing established concepts in philosophy, psychology, economics, law, or another field. | State that the established field is not being replaced and specify the range of the SO-specific use. |
| E3 | Pseudoscientific or doctrinal risk | May be read as a physical or medical claim, religious reality claim, universal theory, or literary proof. | Decelerate to P2 or higher and state non-claim boundaries, standard definitions, and lack of verification. |

### 3.1 Adjustment by E Code

| E | Adjustment |
|---|---|
| E0 | Maintain P_base. |
| E1 | Add definitions, examples, and links. P normally remains unchanged. |
| E2 | Use at least P1 and state the boundary from the established field. |
| E3 | In principle move to P2 or higher, and use P2.5 or P3 where necessary. |

---

## 4. U Code — Use and Safety Risk

| Code | Label | Primary risk | Publication decision |
|---|---|---|---|
| U0 | Low | Provides little direct capacity for manipulation, diagnosis, or circumvention. | Ordinary publication. |
| U1 | Misuse | May be quoted carelessly, overgeneralized, treated as fact rather than metaphor, or attached to other persons as a label. | Publish with cautions. |
| U2 | Transfer risk | May be transferred into classification of persons, organizational manipulation, persuasion, institutional judgment, or safety judgment. | Abstract the presentation and state prohibited uses. |
| U3 | Operational integrity risk | Detailed publication may weaken boundary protection, security, or non-public evaluation mechanisms. | P3 in principle. Only a conceptually distilled version may be published at P2.5. |
| U4 | Restricted | Publication beyond classification is likely to produce concrete harm or reduce operational integrity. | Fixed at P3. |

### 4.1 Adjustment by U Code

| U | Adjustment |
|---|---|
| U0 | Maintain P_base. |
| U1 | Use P1 or higher in principle and show likely forms of misuse. |
| U2 | Consider P2-P2.5 and do not publish operational procedures or diagnostic tables. |
| U3 | Keep details non-public. Only conceptual explanation may be published at P2.5. |
| U4 | Keep non-public. Do not publish beyond classification. |

---

## 5. P Code — Publication Layer

| Code | Label | Meaning |
|---|---|---|
| P0 | Public core | May ordinarily be published as a definition, entry point, or basic structure. |
| P1 | Decelerated public | Publish with scope, non-claims, and distinctions from established fields. |
| P2 | Research publication | Publish as a strong hypothesis, correspondence candidate, or exploratory model, separately from established theory. |
| P2.5 | Abstracted publication | Publish the core concept while withholding diagnostic, manipulative, bodily-correspondence, or safety-evaluation details. |
| P3 | Non-public | Do not include in the ordinary public system. Classification, existence, or policy may sometimes be disclosed. |

Publication layers may differ not only by file but also by section within a single document.

For example, the public core of a cognitive-axis formation model may be P1, while bodily correspondence, diagnosis, or induction procedures may move to P2.5-P3.

---

## 6. V Code — Verification Stage

| Code | Label | Meaning |
|---|---|---|
| V0 | Conceptual coherence | Check terminology, responsibility, non-contradiction, and inter-document connection. |
| V1 | Mapping and counterexample table | Organize correspondences, differences, limits of application, and counterexamples relative to established theories. |
| V2 | Toy model / Minimal model | Test operating conditions through a minimal model, protocol, or fictional example. |
| V3 | Evaluation | Evaluate through AI responses, dialogue logs, organizational cases, creative structures, or related materials. |
| V4 | Formalization and simulation | Introduce variables, states, update rules, transitions, and evaluation indicators. |
| V5 | Predictive comparison | Connect to predictions or calculations that can be compared with established science or empirical domains. |

A higher V code does not mean that the proposition is true.

It indicates which form of examination may be pursued next.

---

## 7. R Code — Rendering Distance from Core Vocabulary

The R code is a supplementary axis indicating the language game into which a proposition has been projected from the public core of Scientific Ontology.

Greater distance does not mean inferiority.

It means that more rendering layers and non-claim boundaries are required.

| Code | Label | Primary domains | Handling |
|---|---|---|---|
| R0 | Core vocabulary | boundary, contact, history, difference, return, cutoff, residual, collation | Stabilize definitions and do not change them casually by field. |
| R1 | Near-core extension | meaning loop, cognitive axis, synchronization, desynchronization, responsibility boundary, aporia | State the connection to core vocabulary. |
| R2 | Cross-domain commensuration | epistemology, ethics, truth, narrative, culture, value | Respect standard concepts in each field and distinguish them from SO-specific definitions. |
| R3 | Organizational and applied rendering | organizational boundary, port, AI adoption, DSSI, social design | Require implementation examples, responsible actors, and stopping conditions. |
| R4 | Physical-near rendering | field, particle, boson, entanglement, Feynman diagram, BlackHole | Treat as E3 in principle and state non-identity with standard physical definitions. |
| R5 | High-strength metaphysical projection | AMP, ITS, the thing-in-itself side, foundational hypotheses | Do not use as an authority source for the ordinary public layer; use P3 or strong distillation by default. |

### 7.1 Language-Game Groups

Peripheral vocabulary is not managed only through a single dictionary meaning.

The relevant language game must also be recorded.

| Language game | Examples | Primary caution |
|---|---|---|
| Ontological | boundary, history, nothingness, existence, relation | Do not confuse with direct possession of the thing-in-itself. |
| Epistemological | sensibility, understanding, cognitive axis, synchronization, collation | Do not replace psychological diagnosis or the history of philosophy. |
| Ethical | return, responsibility, non-destructive distance, retaliation conversion | Do not turn into procedures for legal punishment or private self-help remedies. |
| Organizational | port, protocol, audit, diplomacy | Do not treat analogy with network engineering as factual identity. |
| Economic | negentropy, exchange heat, value, cost | Do not treat as established quantities in economics or thermodynamics. |
| Physical-near | boson field, fermionic soliton rendering, entanglement | Apply the Physics Correspondence Policy first. |
| Literary and mythic | reincarnation, belief-gravity domain, God, demon, Meifu | Do not treat as proof of religious or scientific reality. |
| Implementation | AI boundary function, DSSI, judgment-field maintenance | Require an implementing actor, responsibility, logs, and withdrawal conditions. |

---

## 8. Core Vocabulary

The following constitutes the public core vocabulary of the current public system.

| Item | Public definition | Type | S | E | U | P | V | R |
|---|---|---|---|---|---|---|---|---|
| Scientific Ontology / 存在境界論 | A public conceptual system that does not claim direct possession of existence itself, but treats boundaries, contact, history, return, and downstream conditions as real. | Public framework | S2-S3 | E1-E2 | U0 | P0-P1 | V0-V1 | R0-R2 |
| Boundary / 境界 | A surface at which external input and internal history meet, allowing passage, suspension, cutoff, transformation, recoding, or reflection. | Core definition | S2 | E1 | U0 | P0 | V0-V1 | R0 |
| Contact / 接触 | An event in which distinct existences, histories, or fields enter a relation capable of changing one another's downstream conditions. | Core definition | S2 | E1 | U0 | P0 | V0 | R0 |
| History / 履歴 | Not merely a record of the past, but a structure that changes later reception, reaction, judgment, and meaning formation. | Core definition | S2 | E0-E1 | U0 | P0 | V0-V1 | R0 |
| Difference / 差分 | A difference that reaches a boundary and generates reaction, discomfort, meaning, cutoff, or residuals. | Core definition | S2 | E1 | U0 | P0 | V0-V1 | R0 |
| Return / 返り | A reaction, response, demand for repair, learning process, or meaning update that appears after contact and historical change. | Core definition | S2-S3 | E1 | U1 | P0-P1 | V0-V2 | R0-R1 |
| Cutoff / 切断 | The interruption of communication, historical connection, return paths, or observability. | Core definition | S2-S3 | E1 | U1 | P0-P1 | V0-V1 | R0 |
| Residual / 残差 | A difference that cannot be closed by observation, classification, explanation, or collation and remains available for re-collation. | Core definition | S2-S3 | E1 | U0 | P0-P1 | V0-V1 | R0 |
| Residue / 残渣 | A historical burden that remains deposited in bodies, institutions, relationships, environments, signs, or futures and continues to act after processing. | Ontological reinterpretation | S2-S3 | E1-E2 | U1 | P1 | V1-V2 | R1-R2 |
| Collation / 照合 | An operation that compares distinct histories, definitions, evidence, and boundary conditions while retaining agreements, disagreements, and residuals. | Core definition | S2-S3 | E1 | U0-U1 | P0-P1 | V0-V3 | R0-R2 |
| Return Path / 返路 | A path through which outputs, responsibility, objections, corrections, or meaning return to the originating actor or the next responsible actor. | Near-core concept | S2-S3 | E1 | U1 | P1 | V1-V3 | R1-R3 |
| Aporia / アポリア | A contradiction, branch, or disconnection that cannot close on the same plane and is retained as a future object of collation. | Methodological concept | S2-S4 | E1-E2 | U0 | P1-P2 | V1-V4 | R1-R2 |

---

## 9. Cognition, Meaning, and Cognitive Bridge

| Item | Public definition | Type | S | E | U | P | V | R |
|---|---|---|---|---|---|---|---|---|
| Entropy-Attributed Difference / エントロピー属性つき差分 | Reads difference as appearing at a boundary with history, diffusibility, condensability, and the capacity to be rendered as value or cost. | Cognitive model | S2-S3 | E2-E3 | U1 | P1-P2.5 | V0-V2 | R1-R2 |
| Attention / 関心 | A direction that retains and tracks difference, bringing it to the foreground as reality. | Cognitive concept | S2 | E1-E2 | U1 | P1 | V0-V2 | R1-R2 |
| Abstraction / 捨象 | An operation that backgrounds, suspends, cuts off, or redirects difference so that cognition can form. | Cognitive concept | S2 | E1-E2 | U1 | P1 | V0-V2 | R1-R2 |
| Sensibility / 感性 | An opening through which something arises as a difference that can be felt; not a strict redefinition of Kantian philosophy. | SO auxiliary vocabulary | S2-S3 | E2 | U1 | P1 | V0-V2 | R2 |
| Understanding / 悟性 | An organization through which a felt difference is arranged as an object, relation, cause, responsibility, or other intelligible form. | SO auxiliary vocabulary | S2-S3 | E2 | U1 | P1 | V0-V2 | R2 |
| Cognitive Axis / 認識軸 | A stabilized direction of observation produced through attention, abstraction, value, cost, residuals, and repetition. | Dynamic model | S2-S3 | E2-E3 | U1-U2 | P1-P2.5 | V0-V3 | R1-R2 |
| Cognitive Field / 認識場 | An operational concept for the interpenetrating whole of cognition involving body, sensation, history, attention, meaning, relation, and value. | Cognitive metamodel | S2-S3 | E2 | U1 | P1-P2 | V0-V2 | R2-R3 |
| Cognitive Phase / 認識相 | A quasi-stable configuration temporarily formed within a cognitive field through purpose, attention, bodily state, role, and history. | Cognitive metamodel | S2-S3 | E2 | U1-U2 | P1-P2 | V0-V2 | R2-R3 |
| Operational Discretization / 操作的離散化 | Provisionally cuts continuous cognition or existence into units for communication, judgment, responsibility, recording, and implementation. | Operational metamodel | S2-S3 | E1-E2 | U1-U2 | P1-P2 | V0-V3 | R2 |
| Existence Phase / 存在相 | A relational configuration of role, meaning, responsibility, history, evaluative space, and time horizon within a boundary relation. | Cross-domain existence model | S2 | E1-E2 | U1 | P1 | V0-V2 | R2-R3 |
| Existence-Phase Compression / 存在相圧縮 | Aggregates multiple existence phases into fewer evaluative axes, producing both processability and loss or externalization. | Cross-domain diagnostic model | S2-S3 | E1-E2 | U1-U2 | P1-P2 | V0-V3 | R2-R3 |
| Meaning Loop / 意味ループ | A cycle in which difference is integrated into history and closes as meaning while retaining suspension, cutoff, return, and downstream conditions. | Meaning-generation model | S2-S3 | E2 | U0-U1 | P1 | V0-V3 | R1-R2 |
| Optional Axiom Module / 選択公理モジュール | A unit for comparing worldviews through attention, abstraction, value, cost, Core Invariant, and Operational Drift. | Cognitive bridge | S2-S3 | E1-E2 | U1-U2 | P1-P2.5 | V0-V3 | R2 |
| Cognitive Bridge Protocol / 認識ブリッジ | A boundary protocol that performs translation, suspension, connection, cutoff, and residual retention without destroying the core of distinct cognitive forms. | Commensuration protocol | S3-S4 | E2 | U1-U2 | P1-P2.5 | V1-V4 | R2-R3 |
| Core Invariant | The core of attention, abstraction, value, cost, and collation procedures whose loss would make the system no longer the same system. | Comparative concept | S2-S3 | E1-E2 | U1 | P1 | V1-V3 | R2 |
| Operational Drift | A layer that changes across periods, cultures, institutions, or operations while retaining the same name or nominal core. | Comparative concept | S2-S3 | E1 | U1 | P1 | V1-V3 | R2-R3 |

Prohibited developments: bodily-part correspondence tables, ideological diagnosis, personality types, or classification tables for hiring, education, treatment, or governance.

---

## 10. Truth, Purpose, and Organization

| Item | Public definition | Type | S | E | U | P | V | R |
|---|---|---|---|---|---|---|---|---|
| Truth Management / 真理の経営学 | A method that places a purpose as First Purpose, examines through Boundary CA the world formed by its sharing, and revises, continues, or abandons that purpose. | Methodology | S3-S4 | E2 | U1-U2 | P1-P2 | V0-V3 | R2-R3 |
| First Purpose / 第一義 | What is to be protected, increased, or treated as non-disposable, together with stopping conditions and a responsible actor. | Purpose concept | S2-S3 | E1-E2 | U1-U2 | P1 | V0-V3 | R2-R3 |
| Shared Purpose / 第二義 | The joint operation of a purpose across distinct boundaries by translating it into language, roles, authority, procedures, and objection channels. | Operational concept | S2-S3 | E1 | U1 | P1 | V1-V3 | R3 |
| World Formation / 第三義 | The world formed when a shared purpose redistributes evaluation, resources, institutions, visibility, exceptions, and possibilities for action. | Operational truth concept | S3-S4 | E2 | U1 | P1-P2 | V1-V3 | R2-R3 |
| Boundary CA / 境界CA | An operation that examines exhaustion, externalization, anomalies, residuals, and residues at the boundaries of a formed world, then revises the purpose, boundary, or operation. | Operational protocol | S3-S4 | E2 | U1-U2 | P1-P2 | V1-V4 | R3 |
| Organizational Boundary / 組織境界 | A dynamic boundary through which an organization defines inside and outside, communication, responsibility, history, and processing capacity. | Organizational model | S3 | E2 | U1 | P1-P2 | V1-V4 | R3 |
| Responsibility Boundary / 責任境界 | The boundary of the actor who assumes not only action but also authorization, supervision, improvement, history retention, and exception handling. | Ethical and organizational concept | S2-S3 | E1-E2 | U1 | P1 | V1-V3 | R1-R3 |
| Port / ポート | A provisional and potentially overlapping operational unit that cuts contact at a boundary into finite communication under specified purpose, attention, history, and responsibility conditions. | Cognitive and communication metamodel | S2-S3 | E2 | U1-U2 | P1-P2 | V0-V3 | R2-R3 |
| Organizational Port / 組織ポート | Implements the general port concept as an organizational communication opening with actors, authority, capacity, protocols, logs, audit, and stop/reopen conditions. | Organizational implementation model | S3 | E2 | U1-U2 | P1-P2 | V1-V4 | R2-R3 |
| Port Allocation / ポート配分 | Allocates ports to use, hold, transform, block, or reopen according to purpose, urgency, reversibility, capacity, responsibility boundaries, and re-collatability. | Dynamic control model | S3 | E2 | U1-U2 | P1-P2 | V0-V3 | R2-R3 |
| Multi-Port Potentiality / 複数ポート潜在性 | Preserves unused cognitive forms, language games, and responsibility routes so they can be reopened or newly established when required. | Peace and communication condition | S2-S3 | E1-E2 | U1 | P1-P2 | V1-V3 | R2-R3 |
| Scoped Port Operation / 限定ポート運用 | Limits currently used ports while retaining holding destinations, return paths, and reopening conditions for material outside the active scope. | Operational protocol | S2-S3 | E1-E2 | U1-U2 | P1-P2 | V1-V3 | R2 |
| Boundary Diplomacy / 境界外交 | Maintains communicability among distinct boundary systems without forcing identity, while preserving histories, purposes, language games, and responsibility boundaries. | Boundary-control model | S3 | E2 | U1-U2 | P1-P2 | V0-V3 | R2-R3 |
| Boundary Update / 境界更新 | Reconstructs boundaries, authority, ports, protocols, and audit in response to recurring anomalies, externalization, or unclear responsibility. | Organizational-update model | S3 | E1-E2 | U1-U2 | P1-P2 | V1-V4 | R2 |
| Gateway Capture / ゲートウェイ捕捉 | A failure mode in which an intermediary monopolizes communication routes, translation criteria, and destinations, reducing direct communication and auditability. | Failure mode | S2-S3 | E1-E2 | U2 | P1-P2 | V1-V3 | R2-R3 |
| Single-Metric Compression / 単一指標圧縮 | A destructive compression in which one external metric is treated as representing multiple existence phases, histories, responsibilities, and time horizons. | Failure mode | S2-S3 | E1-E2 | U1-U2 | P1-P2 | V1-V3 | R2-R3 |
| Protocol / プロトコル | A boundary procedure specifying who transforms what, under which conditions, into which form, and where it returns. | Operational concept | S2-S3 | E1 | U1-U2 | P1-P2 | V1-V4 | R3 |
| Negentropy Definition / ネゲントロピー定義 | An organization's self-definition of what burden it accepts, what it transforms that burden into, and what order, meaning, care, or capacity for judgment it returns. | Organizational and value model | S2-S3 | E2 | U1 | P1-P2 | V1-V3 | R2-R3 |

---

## 11. AI, Institutions, and Social Design

| Item | Public definition | Type | S | E | U | P | V | R |
|---|---|---|---|---|---|---|---|---|
| AI as Boundary Function / AI境界機能 | Evaluates AI not merely as a substitute answerer, but as a boundary function that maintains judgment, collation, suspension, objection channels, and return paths for responsibility. | AI philosophy and design concept | S2-S3 | E1-E2 | U1 | P1 | V1-V3 | R3 |
| Judgment-Field Maintenance / 判断場維持 | Maintains a state in which users retain options, grounds, uncertainty, withdrawal, and objection. | Implementation principle | S2-S3 | E1 | U1-U2 | P1-P2 | V2-V4 | R3 |
| AI Adoption | Treats AI adoption as organizational boundary design encompassing procurement, authority, explanation, audit, exceptions, and withdrawal, rather than model performance alone. | Social implementation model | S3-S4 | E2 | U2 | P2-P2.5 | V2-V4 | R3 |
| DSSI | An implementation candidate for a boundary interface supporting digital sovereignty and the judgment field. | Implementation candidate | S3-S4 | E1-E2 | U2-U3 | P2.5 | V2-V4 | R3 |
| Peace Specification / 平和仕様 | Addresses conditions under which distinct modes of existence can continue non-destructive interaction while retaining their boundaries and histories. | Social-boundary model | S2-S3 | E2 | U1 | P1-P2 | V1-V3 | R2-R3 |
| Meaning-Experience Field / 意味・経験場 | An application concept for the cycle through which differences connect to history, become meaning, judgment, action, or response, and return to the world. | Applied field model | S2 | E2 | U1 | P1-P2 | V0-V2 | R2-R3 |
| Meaning Capacity / 意味容量 | The capacity to retain differences, contradictions, and meaning pressure for holding, commensuration, and reconstruction without immediate cutoff, false closure, or destructive discharge. | Applied capacity concept | S2 | E1-E2 | U1-U2 | P1-P2 | V0-V2 | R2-R3 |
| Meaning-Experience Capacitor / 意味経験キャパシタ | An application model that reads retention, depth routing, reconstruction, and return through structural correspondence with a capacitor. | Structural analogy | S1-S2 | E3 | U1 | P2 | V0-V2 | R4 |
| Existence Strength / 存在強度 | An application concept for the capacity to sustain interaction and form, maintain, and revise histories, meanings, relations, and structures. | Social and peace application concept | S2 | E2 | U1 | P1-P2 | V0-V2 | R2-R3 |
| Negentropy Economy / ネゲントロピー経済 | Reads economy as work that recovers, retains, and reorganizes meaning, order, responsibility, history, and capacity for action. It is not presented as an economic theory, thermodynamic proof, or policy proposal. | Economic-philosophy model | S2-S3 | E2 | U1-U2 | P1-P2 | V1-V3 | R2-R3 |

Negentropy Economy is not presented as an economic theory, thermodynamic proof, or policy proposal. It is limited to a conceptual model for reading value circulation and organizational transformation.

In implementation domains, the U code must not be treated as identical to the risk assigned to conceptual explanation.

Specific warning conditions, blocking conditions, security evaluation, person-level judgments, and operational circumvention procedures are managed separately.

---

## 12. Physical-Near Rendering

| Item | Public definition | Type | S | E | U | P | V | R |
|---|---|---|---|---|---|---|---|---|
| History-Field Topology / 履歴場トポロジー | Reads fields bearing history as structures that form contact, nodes, return paths, cutoffs, and residuals. | Ontological reinterpretation | S2-S4 | E2 | U0 | P1-P2 | V1-V4 | R1-R4 |
| Intrinsic Time / 内在時間 | A local depth-order that progresses through commitment within meaning loops, history updating, and reconnection. | High-strength concept | S3-S5 | E3 | U1 | P2 | V1-V5 | R4-R5 |
| Logical-Depth Axis / 論理-深度軸 | A direction for retaining and reconstructing unresolved matters, contradictions, branches, residuals, and semantic pressure rather than ordering them by before and after in external time. | Formalization candidate | S3-S4 | E2 | U1 | P1-P2 | V1-V4 | R2-R4 |
| PINGER Hypothesis | A physical-near hypothesis in which a historical and communicative path connecting a generative phase to a present section appears particle-like on an observational section. | High-strength hypothesis | S4-S5 | E3 | U1 | P2 | V1-V5 | R4 |
| Particle as Observed Section / 粒子＝観測断面 | Reads a field or historical path as appearing as a stable section under boundary conditions. | Physical correspondence candidate | S4-S5 | E3 | U0 | P2 | V1-V5 | R4 |
| Boson as Synchronization Mediator / ボソン＝同期媒介 | Reads the boson from the ontological aspect of mediating interaction history and operational correspondence. | Physical correspondence candidate | S4-S5 | E3 | U0 | P2 | V1-V5 | R4 |
| Fermionic Soliton Rendering / フェルミオン的ソリトン | A high-strength candidate that reads a locally stable structure through field cutoff, history retention, and observational section. | High-strength hypothesis | S5 | E3 | U1 | P2-P3 | V1-V5 | R4-R5 |
| Feynman Diagram as History Topology / ファインマンダイアグラム＝履歴トポロジー | Structurally reads interaction, exchange, vertices, loops, return paths, and cutoffs as a diagrammatic arrangement. | Structural analogy and correspondence candidate | S2-S4 | E3 | U0 | P2 | V1 | R4 |
| Entanglement as History-Field Correspondence | Reads non-separable correspondence between history-fields while distinguishing it from quantum entanglement. | Physical-near correspondence candidate | S4-S5 | E3 | U0 | P2 | V1-V5 | R4 |
| BlackHole as Return-Path Loss | Reads `BlackHole` as a boundary model of historical-connection cutoff and surface return. | Physical-near correspondence candidate | S4-S5 | E3 | U0 | P2 | V1-V5 | R4 |

All entries in this section are governed by [`Physics_Correspondence_Policy.en.md`](./Physics_Correspondence_Policy.en.md).

Standard physical terminology, calculations, and experimental findings must be respected. SO-internal conceptual projections must not be identified with them.

---

## 13. High-Strength and Non-Public Layer

| Item | Public positioning | S | E | U | P | V | R |
|---|---|---|---|---|---|---|---|
| AMP | An internal core that hypothetically describes, as applied metaphysics, what lies beyond the reserve maintained by Boundary Realism. | S5 | E3 | U1-U2 | P3 | V0-V5 | R5 |
| ITS | A high-strength theoretical candidate integrating fields, time operators, observational sections, information-time solitons, and related structures. | S5 | E3 | U1-U2 | P3 | V0-V5 | R5 |
| Private Core | An internal layer that may include individual wounds, induction conditions, safety evaluations, and non-public operations. | S3-S5 | E1-E3 | U3-U4 | P3 | V0-V4 | R3-R5 |
| iMass / rMass | ITS- and PINGER-derived high-depth identifiers retained as axiomatic identifiers and exploratory operators without expansion into a single fixed English phrase. | S4-S5 | E3 | U1 | P2-P3 | V0-V5 | R4-R5 |

The high-strength and non-public layer is not a secret authority over the public system.

It must not be used to justify public documents by claiming that the theory is complete internally.

Its roles are to:

- Retain places where the public system does not close.
- Supply aporias for future examination.
- Accumulate formalization candidates and counterexamples.
- Be revised by constraints returned from Boundary Realism.

---

## 14. Classification of Major Documents

| Document | Function | S | E | U | P | V | R |
|---|---|---|---|---|---|---|---|
| `Scientific_Ontology_Concept_Network.en.md` | Presents the overall arrangement, methodological non-completion, reading order, and document responsibilities. | S4-S5 | E3 | U1 | P1-P2 | V0-V1 | R0-R5 |
| `Entropy_Attributed_Difference_and_Cognitive_Axis_Formation.en.md` | Addresses the generation, stabilization, rigidity, drift, branching, and re-collation of cognitive axes. | S2-S3 | E2-E3 | U1 | P1-P2.5 | V0-V3 | R1-R2 |
| `Optional_Axiom_Modules_as_Cognitive_Bridge.en.md` | Compares cognitive forms and performs commensuration, suspension, cutoff, and residual retention. | S2-S3 | E1-E2 | U1-U2 | P1-P2.5 | V0-V3 | R2-R3 |
| `Truth_Management_and_Boundary_PDCA.en.md` | Examines purpose through First Purpose, sharing, world formation, and Boundary CA. | S3-S4 | E2 | U1-U2 | P1-P2 | V0-V3 | R2-R3 |
| `Cognitive_Dynamics_Communication_Model.ja.md` | Maps a seamless cognitive field into provisional operational units while preventing backward projection from implementation. | S2-S3 | E1 | U1 | P1-P2 | V0-V1 | R2-R3 |
| `Compression_of_Existence_Phases.ja.md` | Diagnoses the benefits, losses, externalizations, and reopening conditions of existence-phase compression. | S2-S3 | E1-E2 | U1 | P1-P2 | V0-V2 | R2-R3 |
| `Boundary_Diplomacy_and_Port_Allocation.ja.md` | Addresses allocation, commensuration, holding, reopening, and gateway capture across multiple ports. | S3 | E2 | U1-U2 | P1-P2 | V0-V2 | R2-R3 |
| `Organizational_Boundary_and_Port_Model.ja.md` | Implements selected ports through responsibility boundaries, authority, protocols, and audit. | S3-S4 | E2 | U1-U2 | P1-P2 | V1-V4 | R3 |
| `Specification_for_Peace.ja.md` | Connects existence phases, meaning capacity, and boundary diplomacy to a public application specification for peace. | S2 | E1-E2 | U1 | P1-P2 | V0-V1 | R2-R4 |
| `Boundary_Realism_Principle.md` | Controls the range of reality that humans may treat through boundary, history, and return. | S2-S3 | E1-E2 | U0 | P0-P1 | V0-V1 | R0-R2 |
| `Boundary_Epistemological_Critique.en.md` | Critiques the conditions of knowledge through operational correspondence, collation, residual retention, and false closure. | S3-S4 | E2-E3 | U1 | P1-P2 | V0-V4 | R1-R4 |
| `Meaning_Generation_Model.md` | Addresses the conditions under which difference is integrated into history and forms meaning loops and return paths. | S2-S4 | E2 | U1 | P1-P2 | V0-V4 | R1-R3 |
| `PINGER_Hypothesis_and_History_Field_Topology.en.md` | Projects history-field concepts into physical-near vocabulary. | S4-S5 | E3 | U1 | P2 | V1-V5 | R4 |

A classification of the file as a whole does not replace section-level classification.

---

## 15. Publication Deceleration Rules

### 15.1 When Using Terms from Established Fields

1. Respect the standard definition first.  
2. State the SO-internal meaning.  
3. Indicate whether the relation is borrowing, analogy, reinterpretation, or a correspondence candidate rather than identity.  
4. State the scope of application and non-claims.  

### 15.2 When Approaching the Body or Psychology

- Do not produce bodily-part correspondence tables.
- Do not diagnose pathology, constitution, personality, or ability.
- Do not publish treatment, intervention, or induction procedures.
- Separate first-person descriptions of felt texture from medical explanation.

### 15.3 When Approaching Ideology, Religion, or Myth

- Do not present the material as proof of empirical reality.
- Do not attach fixed labels to persons or groups.
- Do not replace standard accounts in the history of philosophy or religious studies.
- Compare through attention, abstraction, value, cost, and collation procedures.

### 15.4 When Approaching Organizations, Policy, or AI

- Identify the responsible actor.
- Specify ports for objection, audit, stopping, and withdrawal.
- Do not make operational-integrity-level safety claims without implementation examples.
- Confirm that the theory maintains the judgment field rather than substituting for judgment.

### 15.5 When Using Physical-Near Vocabulary

- Apply the Physics Correspondence Policy.
- State that the claim does not replace standard physics.
- Distinguish mathematical isomorphism, structural analogy, ontological projection, and physical prediction.
- Do not present a proposition that has not reached V5 as an empirically established physical claim.

---

## 16. Do Not Overload the Main Text with Labels

As a rule, individual document headers should contain:

```text
Status
Scope
Language
Claim strength
A brief Public handling note only where necessary
```

Detailed document characteristics, typical misreadings, dependencies, prohibited uses, and rendering distance should be managed in YAML registries, README files, and this table.

Do not assume that readers already understand the meanings of S / E / U / P / V / R.

Labels are not substitutes for explanation.

Public-facing navigation should first provide plain-language non-claim boundaries and a reading order, allowing only readers who need the detailed controls to return to this table.

---

## 17. Overall Assessment

In the current public system, the following cycle is made more explicit than the addition of any single concept:

```text
contact with difference
  ↓
cognitive-axis formation
  ↓
explication and commensuration of cognitive form
  ↓
setting purpose as First Purpose
  ↓
sharing and world formation
  ↓
organizational boundary, responsibility boundary, and ports
  ↓
implementation in AI, institutions, and society
  ↓
Boundary CA
  ↓
residuals, residues, and aporias
  ↓
re-collation of epistemology, ontology, and metaphysics
```

The public core of this cycle centers on R0-R3 and S2-S4.

Physical-near rendering is decelerated as R4, S4-S5, and E3.

AMP / ITS are treated by default as R5, S5, and P3 and are not introduced directly as first-order claims of the public system.

Cognitive-axis formation and cognitive bridges must not be transferred into person classification, ideological diagnosis, or bodily diagnosis.

Truth Management must not be used as a theory under which authorities determine truth.

The Organizational Boundary and Port Model must not be used as a replacement for network engineering, management studies, public administration, or law.

This table does not exist to weaken Scientific Ontology.

It exists to make explicit how far a strong question may close as a public claim, and from which point it must instead remain a hypothesis, commensuration, implementation candidate, or aporia.

---

## 18. Related Documents

- [`Scientific_Ontology_Concept_Network.en.md`](./Scientific_Ontology_Concept_Network.en.md)
- [`Truth_Management_and_Boundary_PDCA.en.md`](./Truth_Management_and_Boundary_PDCA.en.md)
- [`Physics_Correspondence_Policy.en.md`](./Physics_Correspondence_Policy.en.md)
- [`Boundary_Realism_Principle.md`](../01_Sat_Truth/Boundary_Realism_Principle.md)
- [`Boundary_Epistemological_Critique.en.md`](../01_Sat_Truth/Boundary_Epistemological_Critique.en.md)
- [`Meaning_Generation_Model.md`](../01_Sat_Truth/Meaning_Generation_Model.md)
- [`Entropy_Attributed_Difference_and_Cognitive_Axis_Formation.en.md`](../02_Raj_Beauty/Entropy_Attributed_Difference_and_Cognitive_Axis_Formation.en.md)
- [`Optional_Axiom_Modules_as_Cognitive_Bridge.en.md`](../03_Tam_Goodness/Optional_Axiom_Modules_as_Cognitive_Bridge.en.md)
- [`Organizational_Boundary_and_Port_Model.ja.md`](../05_Research_Notes/Cognitive_Dynamics_Communication_Studies/Organizational_Boundary_and_Port_Model.ja.md)
- [`Publication_and_Commensuration_Policy.md`](../90_Repository_Governance/Publication_and_Commensuration_Policy.md)
- [`TERM_COLLISION_REGISTRY.en.md`](../90_Repository_Governance/Terminology/TERM_COLLISION_REGISTRY.en.md)

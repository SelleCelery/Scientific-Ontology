# Repository Assessment Protocol
# Repository Audit Principles

> Status: Policy Draft / Candidate
> Layer: `90_Repository_Governance/Assessment`
> Role: repository-wide assessment protocol / judgment-transparency control
> Scope: proposition attribution / repository commitment / responsibility / claim scope / warrant and ground-search path / topology audit / reciprocal external connection / assessment finding contract / validity-regime preservation / engagement-capacity boundary / evaluation history / residual and return management / audit-capture prevention / reconstruction drills
> Language: English commensurated rendering
> Japanese authoritative source: [Repository_Assessment_Protocol.ja.md](./Repository_Assessment_Protocol.ja.md)
> Authority: Candidate governance document. It does not become repository-wide authority until explicitly adopted.
> Derivation: distilled from the De-Registry, protocol-variance, sufficiency, topology-first, and three-layer transformation experiments recorded under `04_Applications/SO_Reflexive_Philosophical_Research/volumes/Volume_01_DeRegistry_to_Judgment_Transparency/`.
> Non-claim: this protocol does not define truth, prove Scientific Ontology, replace domain-specific standards, or automate final human judgment.

---

## 0. Purpose

> **Audit is not a procedure for displaying correctness. It is an immanent practice by which a system avoids mistaking itself for already complete, already understood, or already connected.**

This is a constitutive premise for adopting the Protocol. The Protocol does not attempt to prove that premise by applying itself to itself. Whether repository owners adopt audit at all remains their decision. Once adopted, however, the audit process itself becomes auditable: whether it still serves this purpose, whether it has turned into self-justification, or whether visible procedural order has replaced contact with the object.

Audit success is therefore not defined by a high number of findings, completed fields, passing an external review, or producing documentation that looks orderly.

### 0.1 Methodological Provenance

The core methods of this Protocol—including separation of proposition attribution, separation of repository commitment, Judgment Transparency Topology, priority of raw anomaly over premature classification, Cut / False Link, preservation of strange results, and protocol-sufficiency testing—were formed through experiments, failed runs, recalibration, comparison, and residual analysis recorded in Volume I.

Volume I is methodological provenance, not a superior authority that automatically validates individual findings. Each finding remains responsible to its target document, target domain, warrant path, connection responsibility, reconstructability, counterexamples, and objections.

This document is a candidate policy for auditing documents, propositions, commensurations, applications, research records, metadata, and publication decisions in the public Scientific Ontology repository.

Its purpose is not to score everything on one scale or force it toward correct/incorrect closure. It aims to keep at least the following reconstructable:

- what was observed or described;
- whose proposition, definition, or position is represented;
- how far the repository itself commits to that proposition;
- in which phase and scope the proposition operates;
- which warrants, rules, or external authorities were used;
- what was retained, transformed, compressed, or abstracted during connection;
- where objections, counterexamples, failures, or additional evidence can return; and
- what remains unresolved.

Audit output does not automatically rewrite authoritative text.

```text
source / document / claim
  -> observation
  -> assessment
  -> recommendation
  -> human review
  -> approve / edit / reject / hold
  -> repository change, if explicitly applied
  -> later return / reassessment
```

This Protocol is subject to the same principle.

---

## 1. Application Principles

### 1.1 Domain First

Treat the target domain's own definitions, laws, specifications, empirical methods, evidence conditions, safety conditions, business requirements, and explicitly stated purposes first.

Do not alter the conditions under which a domain works merely to translate it into Scientific Ontology vocabulary.

`Domain first` does not mean that an external field stands above SO. Each system has primary responsibility for its own internal propositions, definitions, methods, and evidence conditions.

- Read external internal claims through their own sources, standards, methods, and evidence conditions.
- Read SO internal claims through SO definitions, warrant paths, non-claim boundaries, and research history.
- A bridge claim is the responsibility of the party that proposes the bridge.

An external field is an independent connection partner, not SO's superior court. SO is not a superior interpreter of the external field either.

### 1.2 Proposition Unit First

Do not begin assessment from a document title, section title, folder, author, school, or field name. Decompose the target into propositions or operational rules at the granularity needed for responsibility.

```text
Document
  -> proposition 1
  -> proposition 2
  -> represented external proposition
  -> repository-derived proposition
  -> operational rule
```

Document-level projections may be produced later from proposition-level records.

### 1.3 Do Not Use Proper Names as Assessment Keys

Names of thinkers, schools, disciplines, or famous sources may be preserved as provenance, return keys, and source ownership. They are not themselves reasons for an assessment result.

```text
proper name = provenance / return key
proper name != assessment key
```

### 1.4 Require the Same Judgment Reason for the Same Trigger

If the same evaluation condition produces different results, expose the condition that caused the difference. Do not accept unmarked exceptions such as "it feels natural here," "because this is that field," or "because this is canonical."

### 1.5 Do Not Normalize Results to Evaluator Intuition

If faithful protocol execution repeatedly yields a strange result, do not correct it ad hoc to match the evaluator's expected distribution. First trace which rule generated it. Strangeness may indicate an anomaly in the target, a protocol deficiency, missing attribution, missing definitions, or an evaluator assumption.

### 1.6 Do Not Use Hidden Evaluation Rules

Rules that materially affect a result must be traceable to the Protocol, target document, external domain rule, or an explicitly recorded evaluator assumption.

If a necessary rule is not documented, preserve the state as one of:

- protocol insufficiency;
- evaluator assumption;
- unresolved; or
- return required.

### 1.7 Audit Is Not a Truth Score

Do not compress auditability, transparency, reconstructability, claim strength, maturity, publication suitability, usefulness, popularity, implementation success, and truth into one scalar.

Transparent judgments can be wrong. Useful applications do not prove SO. Strong claims are not false merely because they are strong.

---

## 2. Freeze the Audit Fixture

Before assessment begins, freeze the target state.

```yaml
audit_fixture:
  audit_id: ""
  date: YYYY-MM-DD
  source_commit: ""
  protocol_path: "90_Repository_Governance/Assessment/Repository_Assessment_Protocol.ja.md"
  protocol_revision_reference: ""
  includes: []
  excludes: []
  target_paths: []
  purpose: ""
  evaluator: "human / model / mixed"
  model_or_tool: "optional"
```

### 2.1 Source Commit

For Git-managed audits, record the commit at audit start whenever possible. If the target changes during an audit, record whether the same fixture continues or a new fixture starts.

### 2.2 Includes / Excludes

State the audit boundary explicitly. Do not treat excluded documents as if they did not exist.

### 2.3 Do Not Retroactively Rewrite Historical Snapshots

Past audit outputs and snapshots remain records of the objects and rules that existed at that time. A later reassessment produces a new record.

---

## 3. Proposition Extraction

### 3.1 What May Be Extracted

Assessment propositions may include definitions, descriptions, external-system presentations, interpretations, analogies, structural correspondences, hypotheses, generalizations, causal or mechanistic candidates, norms, prescriptions, publication decisions, operational rules, and non-claim boundaries.

### 3.2 Do Not Force Non-Propositions into Proposition Form

Indexes, headings, reading order, pure links, and bibliography need not be treated as assertions unless they materially determine authority, priority, language authority, or concept ownership.

### 3.3 Preserve Source Text

Do not rewrite the source into an evaluator-friendly proposition before preserving the original.

```yaml
proposition:
  id: ""
  source_path: ""
  location: "section / line / anchor"
  source_text: ""
  normalized_statement: "optional"
```

`normalized_statement` is a search and comparison aid. It does not replace `source_text`.

---

## 4. Attribution Audit

Attribution precedes Claim Strength and other higher-order projections.

### 4.1 Separate Production Relation from Represented Position

A repository-authored sentence can represent an external position without endorsing it.

```yaml
attribution:
  textual_producer: "repository / external_source / mixed / unknown"
  represented_position: "repository / named_external_source / external_domain / mixed / indeterminate"
  source_owner: "path / citation / authority / unknown"
  representation_type: "direct_quote / paraphrase / summary / reconstruction / original"
```

### 4.2 Record Repository Commitment Separately

Presence in repository prose is not automatic endorsement.

| Relation | Meaning |
|---|---|
| `represented` | Represents an external system, speaker, or position without automatic truth commitment. |
| `endorsed` | The repository adopts the proposition as its own position. |
| `derived` | The repository derives or proposes a new proposition from sources, premises, or its own rules. |
| `rejected` | The repository rejects the proposition. |
| `suspended` | Adoption is withheld for now. |
| `indeterminate` | Commitment cannot be determined from the text. |

Multiple relations may coexist.

### 4.3 Separate Source Claim from Repository Claim

```text
source claim
  !=
repository representation of source claim
  !=
repository-derived bridge claim
```

The strength of an external source claim is not automatically SO Claim Strength. When SO claims that an external proposition corresponds to, supports, or instantiates an SO concept, that connection is a repository-owned bridge claim and must be assessed separately.

### 4.4 Preserve Unattributable Cases

If ownership cannot be determined, record `indeterminate`. Attribution uncertainty may itself be a finding, but it does not make the proposition false.

---

## 5. Responsibility, Phase, and Scope

### 5.1 Responsible Parties

Record, where possible, who is responsible for justification, revision, withdrawal, publication, and operation.

```yaml
responsibility:
  claim_owner: ""
  definition_owner: "optional"
  evaluation_owner: "optional"
  publication_owner: "optional"
  operational_owner: "optional"
```

These need not be the same party.

### 5.2 Separate Phases

Do not silently collapse:

- observation;
- citation;
- representation;
- description;
- interpretation;
- evaluation;
- hypothesis;
- generalization;
- prescription;
- decision; and
- execution.

Where a transition occurs, record the transforming party and rule where possible.

### 5.3 Scope

Record the target, conditions, time, institution, context, and language game to which the proposition applies.

```yaml
scope:
  target: ""
  conditions: []
  exclusions: []
  time_scope: "optional"
  domain_scope: "optional"
```

Do not silently generalize a local proposition.

---

## 6. Warrant Path

### 6.1 The Claim Owner Holds Warrant Responsibility

When the repository endorses or derives a proposition, it bears responsibility for the warrant that supports it.

An objector does not always need a complete rival theory. An objection that the stated warrant does not derive the stated conclusion can be sufficient to reopen the connection.

### 6.2 Trace the Warrant Chain as Far as Needed

Audit does not require infinite regress. It records where the current argument stops.

Possible stop points include observation, definition, methodological premise, institutional authority, domain standard, value choice, practical purpose, linguistic rule, provisional assumption, and unresolved status.

This list is operational, not a final philosophical taxonomy.

### 6.3 Do Not Disguise Stop Points

If a warrant chain stops at a definition, authority, value, convenience, or assumption, do not present that stop point as observation, proof, or universal agreement.

### 6.4 External-Authority Dependence

When external authority, empirical results, mathematics, law, or institutional standards are used as warrants, ask:

- What does the external source actually support?
- Is the repository bridge claim derived from it?
- Is authority flowing across an unsupported intermediate transformation?
- Can the source side revise or reject the connection?

```text
source exists
  !=
derivation established
```

### 6.5 Ground Search

Audit may inspect not only a list of warrants, but how those warrants were reached.

```text
claim
  -> immediate warrant
  -> source / record / rule
  -> upstream source, event, decision, or observation
  -> current stop point
```

Record, where needed, why a source was pursued, whether it is primary or reconstructed, whether apparently independent sources share an upstream source, whether the search drifted from definition to example or from observation to authority, where it stopped, why it stopped there, and whether the trace is contemporaneous or reconstructed after the fact.

Moving deeper within the same branch is not necessarily increasing independent support.

### 6.6 Independence of Warrant Paths

Do not double-count claims as mutually corroborating when they share the same upstream root.

```text
shared upstream root
  -> claim A
  -> claim B

A agrees with B
  !=
independent corroboration
```

Pay special attention to circular support and authority laundering when SO borrows an external concept and later treats the borrowed form as independent evidence for SO.

---

## 7. Judgment Transparency Topology

Topology audit does not directly determine truth. It checks whether judgment, transformation, and connection remain traceable, contestable, and revisable.

### 7.1 Anchor Integrity

Ask what the judgment is actually in contact with. Do not substitute source, target, proposition, speaker, definition owner, or authority. Do not confuse source claims with repository claims.

### 7.2 Phase Integrity

Check for unmarked jumps from observation to interpretation, representation to endorsement, interpretation to generalization or prescription, and prescription to execution.

### 7.3 Path Legibility

Check what was retained, transformed, summarized, compressed, translated, classified, or abstracted, and which warrant supports which proposition.

### 7.4 Return Reachability

Check where objections, counterexamples, failures, and new data can return, and whether the recipient can actually modify the relevant text, judgment, or operation. External systems must retain rights of correction, rejection, and resubmission.

### 7.5 Open-End Retention

Keep unresolved differences, counterexamples, incomprehension, failed commensuration, and interpretation differences visible. Do not turn residuals into proof of theoretical depth. Provisional closure must retain reopening conditions and return paths.

### 7.6 The Five Axes Are Not a Complete Taxonomy

Anchor / Phase / Path / Return / Open-End are a reusable current interface, not an exhaustive ontology of judgment. Anomalies that do not fit are retained as `Unresolved`.

---

## 8. Primitive Deviation

Do not require a detailed failure taxonomy before recording the anomaly.

```text
Observed anomaly:
Affected nodes:
Expected path:
Observed path:
Possible cut:
Possible false connection:
Named pattern: optional
Unresolved difference:
Return point:
```

Optional primitives:

| Primitive | Meaning |
|---|---|
| `Cut` | A necessary connection, return path, intermediate warrant, or responsibility path is broken. |
| `False Link` | An unsupported target, party, phase, or scope is treated as connected. |
| `Both` | Cut and False Link occur together. |
| `Unresolved` | Current information cannot settle the primitive or the primitive is insufficient. |

```text
detect
  -> preserve
  -> optionally classify
```

Classification does not resolve the anomaly.

---

## 9. Reciprocal External Connection Audit

When SO contacts an external theory, discipline, institution, technology, cultural vocabulary, or established technical term, neither side is treated as the other's superior tribunal.

```text
A. domain-authoritative or source-grounded description
B. repository representation / reconstruction
C. SO-derived interpretation or connection claim
```

A is not an absolute-truth layer. Preserve which source, standard, institution, specialist practice, or interpretive tradition supports it. Audit A->B and B->C transformations, and inspect A->C authority bypass where relevant.

### 9.0 Reciprocal Revisability

A valid connection is not defined by one side winning interpretive authority. It requires that both sides can preserve difference while retaining the ability to correct, reject, and reconnect.

Check at least whether:

- SO has appropriated or redefined an external field's internal claims;
- an external method is being used to invalidate SO internal claims automatically;
- the party proposing a bridge accepts responsibility for its warrants and transformations;
- correction from the other side can actually alter the bridge;
- rejection is not automatically recoded as lack of understanding; and
- SO can return questions about connection conditions without claiming ownership of the external field's internal propositions.

Reciprocal revisability does not require mutual agreement or equal weighting.

### 9.1 Assessment Contact Contract

Cross-system contact does not begin by forcing a single answer to "which side is correct?"

Use three entry operations:

- `SYSTEM-ROLE-IDENTIFICATION` — identify what work the target system is doing;
- `VALIDITY-REGIME-IDENTIFICATION` — identify what counts as成立, validity, legitimacy, or acceptable warrant inside that system; and
- `COMMENSURATION-INTAKE` — determine whether a contact surface can distinguish claims, facts, interpretations, derivations, and bridge claims.

Apply `VALIDITY-REGIME-PRESERVATION` as a cross-cutting rule:

> Do not silently replace the target system's validity conditions with those of another system.

Let `V_X(c)` denote the validity conditions applied to claim `c` in system `X`. If `V_X(c) != V_Y(c)`, system Y's criteria alone may not silently invalidate X's claim.

This does not immunize either side from fact conflict, reference error, safety limits, legal authority, or measurement constraints. Different validity regimes affect how a claim is judged, not whether contact can impose any constraint at all.

```yaml
contact_surface:
  system_role: ""
  validity_regime: ""
  claim: ""
  scope: ""
  warrant: []
  target: ""
  fact_set: []
  interpretation: "optional"
  bridge_claim: "optional"
```

As a general rule:

> **No object-level adjudication before a commensurable contact surface has been established.**

Successful intake means that differences can be compared as differences. It does not imply agreement, identity, integration, equal weighting, or a truth verdict.

#### 9.1.1 Canonical Finding Types

These are non-ordinal and may coexist.

Notation:

- `H` — the SO claim or hypothesis under assessment;
- `X` — the external system in contact;
- `Γ_X` — premises, theories, and derivation rules of X;
- `F_X` — established facts in X within the relevant scope;
- `Γ_SO` — premises, models, and derivation rules internal to SO;
- `Est_X(H)` — X treats H as established;
- `Def_SO(H)` — an effective internal defeater for H has been reached;
- `I_phi(F)` — interpretation of the same fact set F from phase or coordinate phi;
- `B_{A->B}` — a bridge claim extending from system A toward system B.

| Canonical code | machine key | Meaning | Relation | Default first action |
|---|---|---|---|---|
| `EXT-UNESTABLISHED` | `external_unestablished` | Not established in the external system | `not Est_X(H)` | `KEEP-OPEN` |
| `EXT-NONDERIVABLE` | `external_nonderivable` | Not derivable from the external system | `Γ_X ⊬ H` | `KEEP-OPEN` |
| `EXT-FACT-CONFLICT` | `external_fact_conflict` | Conflict with established external facts | `Cons(F_X ∪ {H}) = false` | `BOUNDARY-AUDIT` |
| `SO-NONDERIVABLE` | `so_nonderivable` | Not derivable inside SO | `Γ_SO ⊬ H` | `INTERNAL-TRACE` / `BOUNDARY-AUDIT` |
| `SO-DEFEATER` | `so_defeater` | Internal SO defeater reached | `Def_SO(H)` | `REOPEN-SO` |
| `EXT-REFERENCE-MISSTATEMENT` | `external_reference_misstatement` | SO misstates an external fact or definition | `Rep_SO(q_X) ≢ q_X` | `CORRECT-REFERENCE` |
| `SAME-FACT-ALT-INTERPRETATION` | `same_fact_alternate_interpretation` | Same facts, different interpretive phase | `I_{phi_SO}(F) != I_{phi_X}(F)` | `COMMENSURATION-INTAKE` |
| `RECIPROCAL-BRIDGE-DISPUTE` | `reciprocal_bridge_dispute` | Dispute between bridges in both directions | `Dispute(B_{SO->X}, B_{X->SO})` | `COMMENSURATION-INTAKE` |

A-H lettering may remain as a migration or conversational alias, but public text and machine keys should use the canonical names.

#### 9.1.2 Prohibited Shortcuts

`EXT-UNESTABLISHED` is not falsification.

```text
not Est_X(H)
  != Γ_X ⊢ ¬H
  != falsified(H)
```

Non-derivability is not negation.

```text
Γ_X ⊬ H  !=  Γ_X ⊢ ¬H
Γ_SO ⊬ H !=  Γ_SO ⊢ ¬H
```

`SO-NONDERIVABLE` matters differently depending on whether SO itself claimed a derivation. A Research Note hypothesis is not withdrawn, made non-public, or marked falsified merely because it is not derivable from current SO premises.

`SO-DEFEATER` is a high-priority trigger for re-examination, not automatic total withdrawal. Reopen scope, premises, undercutters, rebutters, and local repair possibilities.

`EXT-REFERENCE-MISSTATEMENT` first returns to SO for local correction of the borrowed fact or definition, then reassesses the bridge or hypothesis.

`SAME-FACT-ALT-INTERPRETATION` preserves the standard definition and shared facts while changing interpretive phase. Do not collapse it into reference misstatement.

#### 9.1.3 First Response Modes

Finding and response are separate axes.

| Response mode | Function |
|---|---|
| `KEEP-OPEN` | Preserve non-establishment or non-derivability without jumping to negation or withdrawal. |
| `BOUNDARY-AUDIT` | Recheck referent, scope, measurement condition, semantic phase, and bridge responsibility. |
| `INTERNAL-TRACE` | Trace the SO premise, history, and generative path behind a claim. |
| `REOPEN-SO` | Return an SO claim, scope, premise, or upstream model to active re-examination. |
| `CORRECT-REFERENCE` | Correct SO's borrowed representation of an external fact or definition first. |
| `COMMENSURATION-INTAKE` | Establish a surface that distinguishes facts, interpretations, derivations, and bridges. |

A default first action is not a final disposition. Later outcomes may include local correction, keep-open, scope revision, bridge return, unresolved status, or withdrawal.

#### 9.1.4 Bridge Overreach

Do not infer that an entire system is invalid merely from `EXT-FACT-CONFLICT` or `SO-NONDERIVABLE`.

Check whether an additional bridge claim extends the finding beyond its warrant. A local fact `F_X` does not automatically justify `F_X => not H` at a wider SO scope.

At minimum distinguish:

- `SCOPE-OVERREACH` — extending a conclusion beyond the warranted local scope;
- `CRITERION-OVERREACH` — substituting one validity regime as the other's sole validity condition;
- `WARRANT-OVERREACH` — extending source or authority beyond what it supports; and
- `DEFINITION-OVERREACH` — extending one system's internal definition into the other's definition ownership without marking the move.

These labels do not automatically condemn the external system. Apply the same audit to bridges extending from SO toward the external system.

#### 9.1.5 Engagement Capacity

Assessment, rebuttal, search, and commensuration consume finite resources: time, attention, computation, bodily capacity, institutional capacity, access, authority, and related constraints.

Let `K_A(q)` be the resources required for party or system A to engage question q, and `C_A(t)` its available engagement capacity at time t. Non-engagement may occur when `C_A(t) < K_A(q)`.

Record this process condition as `ENGAGEMENT-CAPACITY-LIMIT` and its default response as `NONADJUDICATIVE-NONENGAGEMENT`.

```text
not Engage_A(q, t)
  != A ⊢ ¬q
  != A ⊢ q
  != Def_A(q)
```

Failure to answer, continuation limits, search termination, or ending a dispute must not automatically be recorded as agreement, denial, defeat, or a defeater.

Reasons may be recorded, but disclosure is not mandatory. `unspecified` is valid.

```yaml
engagement:
  condition: "engagement_capacity_limit / none / unresolved"
  response: "nonadjudicative_nonengagement / continue / other"
  reason: "resource_limit / time_limit / attention_limit / competence_boundary / access_limit / safety_boundary / role_boundary / voluntary_decline / unspecified"
  duration: "temporary / indefinite / terminal / unspecified"
```

This exit boundary may occur at any audit stage. Reopening need not be predetermined.

### 9.2 Connection Exposure / E

E is not a scale of truth or likelihood of criticism. It is an auxiliary projection of how strongly the repository connects itself to an external system.

| Code | Meaning |
|---|---|
| `E0` | Primarily repository-owned concepts or operations with little dependence on external authority. |
| `E1` | Imports or references external concepts while preserving owner, source meaning, and non-identity. |
| `E2` | Performs cross-system reinterpretation, commensuration, structural mapping, or bridge claims. |
| `E3` | Contains or risks authority laundering, identity, strong causality, replacement, universalization, or strong reification. |

E concerns the repository-created connection, not the strength of the external source itself. A higher E means stronger transformation responsibility and stronger requirements for reciprocal revisability, not that either side is weaker or stronger overall.

### 9.3 Separate Connection from Integration

Presenting a connection candidate does not integrate the external system into SO. Preserve at least source-side internal definition, repository reconstruction, non-identity, connection owner, intermediate rules, both sides' correction or rejection rights, and untransformed residuals.

### 9.4 Detailed Responsibility for External Vocabulary

Detailed records for why an established term is used, how it differs, why it is retained, and what can return to the source domain belong to Terminology Connection / Return governance.

This Protocol nevertheless requires the following baseline:

- preserve source definitions, usage, and warrants first;
- do not present SO reinterpretation as victory over or a deeper ownership of the source meaning;
- mark non-identity where needed;
- be able to explain why the established term is retained;
- preserve a return path for source-side correction or rejection; and
- when SO can return questions, comparisons, or observation candidates to the source domain, identify them as bridge claims with responsible owners.

---

## 10. Claim Strength / S

### 10.1 What S Measures

S is an auxiliary projection of the strength of a proposition the repository itself commits to.

S does not mean truth, maturity, verifiedness, importance, public value, popularity, or formalization progress.

### 10.2 What Receives S

In principle, apply S to propositions the repository `endorses` or `derives`. Do not assign repository S to a merely `represented` external claim. If source posture must be recorded, keep it separate.

### 10.3 Provisional S Definitions

| S | Repository commitment |
|---|---|
| `S0` | Terminology, classification, record, index, or operational convention without strong claims about the target world. |
| `S1` | Limited description, analogy, or heuristic without asserting ontological identity outside its scope. |
| `S2` | Reinterpretation, conceptual model, or operational model within an explicitly declared frame. |
| `S3` | Conditional general structure, relation, or recurring pattern proposed as a repository claim. |
| `S4` | Strong cross-system correspondence, mechanism, generative relation, or causal candidate. |
| `S5` | Identity, universality, strong external existence, strong causality, or replacement/competition with an established field. |

This redesign prevents proposition type, formalization stage, and publication layer from being collapsed into S.

### 10.4 Do Not Assign S from Vocabulary Alone

Words such as existence, physics, causality, reality, axiom, or quantum do not automatically raise S. Plain language may still make a high-S claim if it asserts universality, identity, causality, or replacement.

### 10.5 Document-Level S Is a Projection

The primary S unit is the proposition. For lists or Navigator summaries, derived values may be used:

```yaml
claim_projection:
  s_core: "main repository commitment"
  s_max: "maximum endorsed/derived claim strength"
```

`S_max` excludes represented external claims.

---
## 11. Separate Use, Publication, Maturity, and Evaluation

### 11.1 Use / Safety

Misuse, manipulation, privacy, safety, and institutional impact are separate from Claim Strength. High S is not automatically dangerous, and low S can still have high operational risk.

Detailed use/safety classification belongs to Publication / Safety governance.

### 11.2 Publication

Public, decelerated, abstracted, non-public, or split handling is separate from truth. Follow the Publication and Commensuration Policy.

### 11.3 Maturity

Maturity records stability, revisability, and review readiness. It does not mean truth, universality, importance, or Claim Strength.

### 11.4 Do Not Make Verification a Single Scalar

Conceptual consistency, counterexample review, formalization, experiment, external review, and simulation are different modes rather than a mandatory staircase. Preserve them in Evaluation History.

### 11.5 Do Not Make Rendering Distance a Primary Audit Scalar

Do not rank language games, disciplines, or metaphysical projections by one fixed distance scale. Treat them through local interfaces, external-connection records, and Terminology Connection records.

---

## 12. Evaluation History

Assessment should preserve not only a current result but what was tested, why it was tested, how it was tested, what was observed, and what remained.

```yaml
evaluation_record:
  id: ""
  date: YYYY-MM-DD
  target: "document / section / proposition / relation"
  source_commit: ""
  protocol: ""
  evaluator: "human / model / mixed"
  reason: ""
  mode: []
  method: ""
  evidence: []
  observed: ""
  assessment: ""
  recommendation: ""
  human_decision: "pending / approve / edit / reject / hold"
  residuals: []
  return_points: []
  next_action: "optional"
```

### 12.1 Separate Observed / Assessment / Decision

- `observed`: what was directly observed;
- `assessment`: how that observation was interpreted;
- `recommendation`: what the evaluator recommends;
- `human_decision`: what the repository owner decides.

Do not compress them into one sentence.

### 12.2 Evaluation Modes Are Not a Ranking

Possible modes include:

- conceptual_consistency;
- cross_document_consistency;
- attribution_review;
- topology_audit;
- counterexample_review;
- external_mapping;
- commensuration_review;
- constructive_test;
- controlled_comparison;
- operational_evaluation;
- formalization;
- simulation;
- empirical_evaluation;
- external_review; and
- publication_review.

Choose the mode needed by the target. Do not interpret the list as low-to-high rank.

---

## 13. Writing Audit Findings

A finding is not an immediate verdict of guilt, invalidity, or falsity.

```yaml
finding:
  id: ""
  type: "optional canonical finding type"
  impact_class: "blocking / structural / terminological / editorial / unresolved"
  target: ""
  observation: ""
  affected_topology: []
  primitive_deviation: "Cut / False Link / Both / Unresolved / none"
  assessment: ""
  evidence: []
  response:
    first_action: "keep_open / boundary_audit / internal_trace / reopen_so / correct_reference / commensuration_intake / other"
    note: ""
  recommendation: ""
  return_point: ""
```

Use `type` for the canonical finding types in 9.1 when they fit. Do not force every anomaly into that taxonomy.

`impact_class` describes which repository responsibility or boundary is affected. It is not a truth ranking or a moral hierarchy of errors. A finding may have a priority first action without being converted into a single scale of "worse" and "better" error.

### 13.1 Blocking

Affects meaning, authority, safety, publication suitability, concept ownership, or major attribution.

### 13.2 Structural

Affects role, placement, dependency direction, scope, responsibility, return path, or metadata structure.

### 13.3 Terminological

Affects naming, definition ownership, commensuration, external vocabulary connection, or marked non-identity.

### 13.4 Editorial

Affects readability or form without changing meaning.

### 13.5 Unresolved

Current evidence or categories cannot localize the difference. `Unresolved` does not mean low importance.

---

## 14. Audit Depth and Triggers

Not every document is audited at the same depth at all times, but auditability should remain available.

Prioritize deeper audit where there is:

- a change to authoritative text or repository-wide governance;
- a change of concept owner;
- high repository commitment;
- E2-E3 external connection;
- external specialist authority used as warrant;
- causal, mechanistic, universal, identity, or replacement claims;
- public/private boundary change;
- high-impact applications involving safety, law, institutions, medicine, money, or persons;
- definition conflict across documents;
- mismatch between Navigator/manifest and text; or
- returned objections, failures, counterexamples, or experimental results.

Do not impose the same philosophical depth on trivial copy edits and obvious link repairs.

---

## 15. Cross-Document Audit

Audit the repository as a graph, not only as isolated files.

### 15.1 Identity

Check title, filename, language relation, path, and status.

### 15.2 Ownership

Check public definition owner, canonical owner, imported concept owner, and document-local definition. Do not place multiple canonical owners on one concept without marking the relation.

### 15.3 Dependency

Check imports, exports, prerequisites, derived relations, and return paths. Detect reversed dependency direction.

### 15.4 Index / Navigator Projection

README, System Map, Concept Network, manifest, graph, and Navigator do not redefine the body text. Ensure display layers do not generate stronger claims than their sources.

### 15.5 Historical Compatibility

Old vocabulary and classification needed to read past releases should remain traceable through Git history, migration notes, or superseded records. Compatibility does not require preserving obsolete rules as current authority.

---

## 16. Commensuration Audit

For English commensuration and other reconstructions, inspect more than word correspondence. Preserve:

- central question;
- proposition responsibility;
- concept ownership;
- relation structure;
- warrant;
- claim strength;
- non-claim boundaries;
- closure conditions;
- residuals; and
- return paths.

Improved explainability does not imply agreement, identity, or proof. Do not hide non-commensurable regions behind fluent prose.

When external vocabulary is borrowed, connect the issue to Terminology governance.

The Assessment Contact Contract also applies: commensuration may need to identify system role and validity regime before object-level adjudication. In some domains, maintaining an intelligible contact surface without forcing a shared final criterion may be the main work of commensuration.

---

## 17. Self-Audit / Preventing SO Capture

Scientific Ontology is itself a cognitive form and is therefore auditable.

Check at least whether:

- everything is being translated into boundary vocabulary;
- analogy has been promoted into identity;
- Research Notes are being used as established canon;
- SO vocabulary merely renames rather than explains;
- unresolved status is being over-preserved to avoid warranted conclusions;
- simple implementation is being made unnecessarily complex by audit architecture;
- a non-SO control condition performs better and the difference is retained;
- external systems retain the right to reject or revise SO's connection; and
- SO's bridge motive is being disguised as a claim owned by the external system.

For materially new or high-impact judgments, ask where practical:

> Would this conclusion still be recommended without knowing Scientific Ontology?

Mark the portion that specifically depends on SO as SO-derived interpretation, connection candidate, or hypothesis rather than domain fact.

### 17.1 Audit Capture

As an audit system becomes more elaborate, it may select only what can be audited, deform objects so they score well, or optimize visible audit artifacts instead of the underlying system.

Inspect whether:

- only checkable things are treated as important;
- unnamed anomalies are discarded because they do not fit records;
- the target is being changed to improve metrics or checks;
- audit materials prioritize appearance over contact with operational reality;
- "audited" or "all fields complete" is being read as valid, safe, or true;
- pressure to pass external evaluation has turned internal reflection into display technology; or
- inconvenient history has been cut so that later reconstruction is impossible.

This Protocol sometimes calls this working warning the **Law of the Sophist**:

> Techniques for appearing wise may develop faster than becoming wiser.

This is not asserted as a universal law. It is a shorthand warning about assessment, publication, and certification pressures.

### 17.2 Prefer Trace to Reality over Audit Artifacts

Distinguish the existence of an audit artifact from traceability to actual history.

```text
audit artifact
  -> operational trace
  -> original event / decision / source
```

If this path is broken, polished documentation does not repair it.

- contemporaneous records may be marked `contemporaneous trace`;
- later reconstruction should be marked `reconstructed after the fact`;
- where original trace is unavailable, record `trace unavailable / unresolved`.

Reconstruction after the fact is not itself misconduct. It must simply not be silently upgraded to the same evidentiary status as contemporaneous trace.

---

## 18. AI-Assisted Audit

AI may assist with proposition extraction, attribution candidates, contradiction candidates, topology findings, comparison, return candidates, and metadata mismatch. AI is not the final repository decision maker.

### 18.1 AI May

- prepare audit fixtures;
- extract propositions;
- propose source / represented-position relations;
- detect commitment ambiguity;
- perform topology audit;
- generate raw anomaly logs;
- propose S/E projections with reasons;
- check cross-document consistency;
- propose migration candidates; and
- generate diffs for human review.

### 18.2 AI Must Not Automatically

- change canonical owners without approval;
- rewrite authoritative text automatically;
- promote a research hypothesis into canon;
- turn represented external claims into endorsements;
- close unresolved findings automatically;
- alter public/private boundaries without approval; or
- display Claim Strength as a truth ranking.

### 18.3 Human Review Actions

Standard actions are:

- `approve`;
- `edit`;
- `reject`; and
- `hold`.

Rejecting an AI proposal is not an audit failure.

---

## 19. Minimum Audit Procedure

### Step 0: Fixture

Freeze source commit, paths, purpose, and exclusions.

### Step 1: Proposition

Extract the target proposition.

### Step 2: Attribution

Identify textual producer, represented position, and source owner.

### Step 3: Commitment

Record represented / endorsed / derived / rejected / suspended / indeterminate.

### Step 4: Responsibility / Phase / Scope

Record who is responsible, what phase the statement occupies, and where it applies.

### Step 5: Warrant

Record warrants, external-authority dependence, ground-search path, and current stop point.

### Step 6: Contact Contract

Where external contact exists, identify system role, validity regime, and commensuration intake. Apply canonical finding types when useful. If an engagement-capacity boundary is reached, record nonadjudicative non-engagement.

### Step 7: Topology

Audit Anchor / Phase / Path / Return / Open-End.

### Step 8: Raw Anomaly

Record anomalies before forcing classification.

### Step 9: Primitive Deviation

Apply Cut / False Link / Both / Unresolved only where useful.

### Step 10: Downstream Projection

Only where needed, project S / E, use/safety, publication, or metadata.

### Step 11: Recommendation

Propose correction, retention, split, movement, further testing, external collation, hold, or another response.

### Step 12: Human Decision

A human repository owner decides approve / edit / reject / hold.

### Step 13: Return

Preserve a path by which changes, objections, counterexamples, failures, and operational outcomes can re-enter later assessment.

---

## 20. Minimum Assessment Record Template

```yaml
repository_assessment:
  audit_id: ""
  source_commit: ""
  target:
    path: ""
    location: ""
    proposition_id: ""
    source_text: ""

  attribution:
    textual_producer: ""
    represented_position: ""
    source_owner: ""
    representation_type: ""

  commitment:
    relations: []
    repository_owned: false
    note: ""

  responsibility:
    claim_owner: ""
    definition_owner: ""

  phase:
    current: ""
    transition: ""

  scope:
    target: ""
    conditions: []
    exclusions: []

  warrant:
    immediate: []
    external_authority: []
    stop_point: ""
    unresolved: []

  topology:
    anchor: "intact / strained / failed / unresolved"
    phase: "intact / strained / failed / unresolved"
    path: "intact / strained / failed / unresolved"
    return: "intact / strained / failed / unresolved"
    open_end: "intact / strained / failed / unresolved"

  contact_contract:
    system_role: "optional"
    validity_regime: "optional"
    commensuration_intake: "not_applicable / established / partial / failed / unresolved"
    bridge_claims: []

  findings:
    - type: "optional"
      observation: ""
      first_action: "optional"

  engagement:
    condition: "none / engagement_capacity_limit / unresolved"
    response: "continue / nonadjudicative_nonengagement / other"
    reason: "optional / unspecified"
    duration: "temporary / indefinite / terminal / unspecified"

  anomaly:
    observed: ""
    affected_nodes: []
    expected_path: ""
    observed_path: ""
    possible_cut: ""
    possible_false_link: ""
    named_pattern: "optional"
    unresolved_difference: ""
    return_point: ""

  projections:
    claim_strength_s: "optional"
    connection_exposure_e: "optional"
    use_safety: "defer / optional"
    publication: "defer / optional"

  assessment:
    impact_class: ""
    interpretation: ""
    recommendation: ""
    residuals: []

  review:
    human_decision: "pending / approve / edit / reject / hold"
    decision_note: ""
    next_return: ""
```

This template is not a canonical machine schema. Pilot audits may reveal redundancy, omissions, or misclassification; such findings return to this Policy before schema migration.

---

## 21. Protocol Sufficiency Test

A new audit rule should be self-contained enough that when the same target is given to another evaluator, another LLM, or another time, differences in the judgment path can at least be compared.

Exact agreement is not required. Differences should be localizable to such causes as:

- source interpretation;
- attribution;
- commitment assignment;
- scope;
- warrant;
- topology;
- external domain rule;
- evaluator assumption; or
- protocol ambiguity.

### 21.1 Hidden Policy Test

If an evaluator's unstated "obvious" rule affects the result, expose it and decide whether it belongs in the Protocol or should remain evaluator-specific.

### 21.2 Strange-Result Preservation

Do not normalize a protocol-faithful but strange result to evaluator preference. If the result exposes a protocol defect, return that defect to the Protocol.

### 21.3 Self-Application

Do not exempt this Protocol from audit. The constitutive premise in Section 0 need not be ultimately proved by self-audit; the rules, operations, findings, displays, and revision procedures derived from it are still auditable for whether they serve the declared purpose or become self-justification.

If a rule cannot be applied to the Protocol itself, or the Protocol makes itself exceptional, state why.

### 21.4 Reconstruction Drill

Accidents, major objections, missing records, or broken external connections expose whether the audit system can actually return to history. Real accidents are not required.

After major changes or periodically, assume a virtual Cut such as "an accident occurred," "a major connection was lost," or "an important record was partially lost," then test whether the current repository can reconstruct:

- who adopted a proposition, when, and on what warrant;
- why the current definition owner has that authority;
- which claims depend on a lost external source;
- whether bridge provenance can be recovered when an intermediate document is missing;
- whether judgment paths can be rebuilt from Git, sources, and decision records when audit records are lost; and
- whether any audit record remains polished but disconnected from the underlying object.

The drill is analogous to failure injection, tabletop exercises, or disaster-recovery tests. Inability to reconstruct is returned as a finding about implicit connections, concentrated history, or disconnected records; it is not automatically evidence of wrongdoing.

---

## 22. What This Protocol Does Not Guarantee

This document does not guarantee:

- that an audited proposition is true;
- that a transparent judgment is correct;
- that the five Topology axes exhaust judgment structure;
- that Cut / False Link classify every deviation;
- that a warrant chain has, or lacks, an ultimate stop point;
- that external-system contact is always beneficial;
- that SO-based methods outperform non-SO methods; or
- that AI audit is superior to human audit.

The value of the Protocol is not to guarantee these in advance, but to leave contacts, responsibilities, paths, objections, and residuals available for later re-examination.

---

## 23. Matters Retained at Research Stage

The following are not promoted immediately into repository-wide doctrine.

### 23.1 Formulating Objectivity

The relationship between openness to constraints that cannot be changed for convenience and traceability, objection, and revisability remains a research problem. This Protocol does not adopt it as the canonical definition of objectivity.

Where useful, record which external constraints could actually change a judgment.

### 23.2 The "Ground" Model of Warrant

Reading warrant not as one final root but as the ground on which a proposition currently stands remains an active metaphor. This Protocol operationalizes Ground Search through stop points, search paths, historical traceability, and independence/shared roots of warrants, without immediately turning those traces into an ontology of ultimate ground.

### 23.3 Boundary as Inducement Rather Than Invasion

The hypothesis that good cross-system contact offers opportunities for mutual reconsideration rather than importing or integrating conclusions remains under research. Reciprocal correction, rejection, and return are used operationally here, but this hypothesis is not adopted as a universal proposition.

---

## 24. Migration from the Legacy Evaluation System

This Protocol does not require immediate deletion of `00_Overview/Claim_Strength_and_Publication_Layer_Table.*`.

Legacy responsibilities are decomposed toward appropriate owners.

| Legacy responsibility | Current primary owner candidate |
|---|---|
| proposition assessment order | this Protocol |
| attribution / commitment | this Protocol |
| Claim Strength S | this Protocol |
| external Connection Exposure E | this Protocol |
| A-H canonical finding types / response modes | this Protocol |
| validity-regime preservation / commensuration intake | this Protocol |
| engagement-capacity / nonadjudicative non-engagement | this Protocol |
| use / safety risk | Publication / Safety governance |
| publication layer P | `Publication_and_Commensuration_Policy.md` |
| Verification V | decomposed into Evaluation History |
| Rendering Distance R | local language-game / terminology connection records |
| vocabulary definitions | `GLOSSARY.md` + canonical definition owners |
| document current state | `tools/docs_manifest.yml` |
| evaluation history | evaluation ledger / assessment records |

Do not mark the legacy table superseded until machine-readable registries, manifest projections, public checkers, and Navigator references have been migrated far enough to preserve current behavior and historical readability.

---

## 25. First Pilot Audit

Do not begin adoption by auditing every canonical document.

Recommended initial targets:

1. `01_Sat_Truth/Boundary_Realism_Principle.md`
   - public foundation;
   - non-claim boundary;
   - repository-owned propositions.

2. `01_Sat_Truth/Boundary_Epistemological_Critique.ja.md`
   - contact with external philosophy and formal systems;
   - strong connection candidates;
   - attribution / warrant / scope.

3. If needed, one document that explicitly borrows established external terminology.

The pilot is not a trial of the target documents. It tests whether this Protocol can distinguish:

- represented from endorsed;
- authored from committed;
- source claims from bridge claims;
- topology findings from truth judgments;
- S from E;
- findings from publication decisions;
- unresolved from failure;
- external non-establishment from falsification;
- non-derivability from negation;
- reference misstatement from alternate interpretation;
- reciprocal bridge dispute from one-way adjudication; and
- non-engagement from assent, denial, or defeat.

If protocol insufficiency appears, revise the Protocol before broadening canonical audit.

---

## 26. Return After Adoption

This Protocol is not a completed fixed artifact. Reopen it when, for example:

- pilot audits repeatedly expose unclassifiable differences;
- different LLMs or human evaluators produce judgment differences that cannot be localized;
- S/E projections begin overwriting proposition content again;
- audit cost repeatedly exceeds the practical value of the target;
- an external domain specialist raises a major objection to connection rules;
- Terminology Connection / Return governance and this Protocol overlap improperly;
- responsibility separation from Publication Policy breaks down;
- Navigator display constraints distort canonical assessment;
- non-SO control conditions repeatedly outperform SO-assisted methods;
- canonical finding types collapse distinctions they were meant to preserve;
- validity-regime preservation becomes an excuse to ignore real fact conflict; or
- engagement-capacity limits are misread as substantive adjudication.

Do not silently rewrite old judgments when the Protocol changes. Preserve evaluation history and reasons for revision.

---

## 27. Compressed Principles

The Protocol can be compressed into the following order:

> **Audit is not for displaying correctness; it prevents a system from mistaking itself for already complete, already understood, or already connected.**
> **Look at propositions before labels.**
> **Separate whose proposition it is.**
> **Separate how far the repository commits to it.**
> **Separate phase, scope, and responsibility.**
> **Expose not only warrants, but how those warrants were reached.**
> **Do not double-count different names that share one warrant root as independent support.**
> **Do not rank external systems and SO vertically; the party proposing a bridge owns responsibility for the bridge.**
> **Keep connections correctable, rejectable, and reconnectable from both sides.**
> **Identify system role and validity regime, and do not jump to object-level victory before a commensurable contact surface exists.**
> **Do not collapse external non-establishment, non-derivability, fact conflict, internal defeaters, external reference misstatement, alternate interpretation, and reciprocal bridge dispute into one state.**
> **Non-engagement is not assent, denial, defeat, or a defeater; preserve engagement-capacity limits as nonadjudicative non-engagement.**
> **Audit Anchor, Phase, Path, Return, and Open-End.**
> **Preserve anomalies before classifying them.**
> **Project S/E only after the underlying relations are visible.**
> **Audit whether the audit itself is selecting only what is easy to audit.**
> **Use reconstruction drills where useful to test whether history and judgment paths can survive a virtual Cut.**
> **Do not disguise unresolved status as either success or failure.**
> **Return results to human judgment and keep a path for later reopening.**

These are candidate basic principles for judgment-transparency audit in this repository.

# Research Context and Roadmap — From the Optional Axiom Tests to Judgment Transparency, and Beyond

> Status: Public Application / Research Context and Roadmap
> Layer: 04_Applications
> Role: research context, roadmap, public entry point
> Authority: Application-level. This document does not redefine SO canon or establish the truth of the research hypotheses it describes.
> Language: English commensurated rendering
> Japanese authoritative source: [`00_RESEARCH_CONTEXT_AND_ROADMAP.ja.md`](./00_RESEARCH_CONTEXT_AND_ROADMAP.ja.md)
> Maturity: Provisional roadmap
> Claim posture: project history + research program; unresolved branches remain open

## 0. Role of this document

Volume I, “From De-Registry to Judgment Transparency,” was not originally designed as a research project for constructing a theory of judgment transparency.

It began as a De-Registry experiment using the old Optional Axiom corpus as material, asking whether proposition responsibility, scope of application, claim strength, dependence on external authority, publication judgment, and commensuration residuals could still be handled after proper names, school names, field names, and external authority were removed from the evaluation key.

As the experiment proceeded, however, a larger problem emerged than the original test target: **how AI generates judgments, where it misattributes them, where it hides transformations, and how far objections can be returned**.

This volume was therefore created not to retrospectively reshape that turn into a success story, but to preserve the tests, failures, recalibrations, model differences, self-audits, and renewed comparisons with external systems as a history.

Accordingly, the research treated in this volume is not research on Optional Axiom itself.

> The Optional Axiom corpus was used as a high-density test material; this made it necessary to study judgment generation itself, and a method of judgment transparency arose from that process.

This circumstance is stated explicitly as the research context of Volume I.

---

## 1. Why the Optional Axiom corpus?

The old Optional Axiom corpus densely gathered descriptions belonging to different language games, including philosophy, religion, science, ethics, politics, strategy, death, and AI.

At least the following were mixed together within those descriptions:

- concepts belonging to external systems themselves;
- representations summarizing those systems;
- reinterpretations on the SO side;
- value judgments on the evaluator side;
- references to external authority;
- bridges to other fields;
- strong metaphysical or ontological connections.

This made the corpus dangerous to read as current authoritative theory, but highly useful as test material.

The reason was that the same corpus could be used to repeatedly inspect questions such as the following:

- Does the same judgment remain after names are removed?
- Can we distinguish who is making a proposition?
- Is citation or authority being substituted for derivation?
- What was compressed, abstracted away, or added in the process of summary and commensuration?
- Is SO describing an external system, or transforming that external system into SO?
- Does a return path remain through which objections can reach the transformation?

In this sense, the Optional Axiom corpus functioned as a **stress-test corpus for auditing connections among different forms of cognition**.

Because the results exceeded the original purpose of the test, they were separated into Volume I.

---

## 2. The research process itself is also an object of research

In Scientific Ontology research, not only the object being considered but also **how one connected to the object, explained it, failed, and corrected the failure** can itself become an object of research.

This research treats that reflexivity more explicitly than usual.

At least three levels are distinguished.

### 2.1 Object level

Read the objects directly handled: philosophical propositions, external systems, documents, experimental results, and related materials.

### 2.2 Method level

Read how AI, evaluation protocols, Metadata Assessment, commensuration procedures, and related methods transformed and judged those objects.

### 2.3 Reflexive level

Apply the same method back to SO itself and audit SO canon, application documents, publication judgments, and connections to external systems.

Because these three levels circulated into one another, this research became more than a case study. It became **a record of how SO's own research method changed through testing**.

---

## 3. The roadmap is not linear

The five items below are not classifications of completed research fields.

In particular, ① through ③ are likely to move back and forth among one another, and the actual history of those movements forms ④. ⑤ is the stage at which problems that repeatedly appear while writing ④ are later recovered as candidate research fields.

```text
        ① Philosophical research
          ↑      ↓
          │      │
        ② SO self-audit
          ↑      ↓
          │      │
        ③ Explicit grounds and public reconstruction
          ↑      ↓
          └──────┘

      the history of these movements itself → ④

      recurring structures recovered from ④ → ⑤
      ⑤ is returned to ① for testing
```

This diagram does not fix a research sequence.

---

## 4. ① Philosophical research — Can LLMs be used to observe the communicative effects of propositions?

Item 1 is a basic research field intended for long-term operation.

At the present stage, no independent finished theory is placed here. The first task is to establish a place where questions can be posed, tested, and returned to.

The central research concern is the following:

> When a philosophical proposition passes through an LLM, can the ways in which it is retained, transformed, compressed, connected, or rejected be observed as a communication process?

For commensuration in particular, the aim is not merely to inspect word matching or the fluency of explanations, but to observe the following:

- Was the responsibility of the proposition retained?
- Was the ownership or attribution of the claim retained?
- Were the internal constraints of the system to which it was connected retained?
- Can the transformation path be reconstructed?
- Are non-commensurated residuals preserved?
- Can an objection return to the original connection point?

From there, the research asks whether structures recur across different philosophical systems, language games, and forms of description.

Universality is not assumed in advance. If recurring structures are observed, the extent to which they can be generalized is considered afterward.

The operation of these questions is separated into [`01_PHILOSOPHICAL_RESEARCH_QUESTIONS.en.md`](./01_PHILOSOPHICAL_RESEARCH_QUESTIONS.en.md).

---

## 5. ② Immediate application — Audit SO's own authoritative documents by the same principles

Methods obtained in ① are first returned to SO itself.

The targets are the authoritative documents, application documents, public definitions, commensurated documents, and Metadata descriptions accumulated in the repository.

The purpose is not to rewrite the authoritative text immediately.

The first task is to expose what the current documents actually undertake.

- Does the stated claim strength match the responsibility actually carried by the body text?
- Has the authority of an external system flowed into SO as if it were SO's own warrant?
- Is an external concept merely being represented, or is SO itself endorsing it?
- Has there been an unmarked phase jump among observation, interpretation, evaluation, prescription, and execution?
- Have important transformations or omissions been hidden?
- Have unresolved differences been closed as though they had already been resolved?

Even when an audit exposes a defect, that alone is not treated as failure of the research.

Likewise, when a defect exists in a connection to an external system, it is not immediately equated with failure of SO as a whole, failure of the external system, or failure of the researcher. The task is to localize which connection point, transformation, or responsibility produced the problem.

This work is now connected to the Assessment Lab and Registration Workbench in the Developer Navigator. AI generates audit candidates; a human selects `approve / approve_with_edits / hold / reject`; and reflection into the canonical manifest occurs through a separate explicit transaction.

AI is not the subject that rewrites the authoritative text. Nor is there a route by which the browser writes directly into the canonical manifest.

---

## 6. ③ Make underlying grounds explicit and examine their value through communicative connection

As ② proceeds, the assumptions actually being used behind strong claims and methods should become visible.

SO can then make explicit what it is using as grounds for judgment.

This does not mean claiming to have discovered an “ultimate ground.”

The first questions are instead:

- Where is this claim grounded?
- What does that grounding make possible?
- What ceases to hold if that grounding is removed?
- Can another system connect to that grounding?
- If it cannot, what difference remains?

This layer may come into contact with unpublished raw materials in applied metaphysics, AMP-related materials, ITS, PINGER, and related lines.

They are neither the secret authoritative source of public SO nor a hidden ultimate ground.

The unpublished raw materials include descriptions that boldly rearrange standard scientific vocabulary and extend it into ontological or metaphysical interpretation. If published without reconstruction, they would carry a high risk of conflating standard-scientific claims, empirical hypotheses, ontological reconstruction, and creative extension.

Accordingly, if material from that lineage is made public, it should not be cited as authority in its raw form. At least the following should be separated and reconstructed:

```text
private lineage
    ↓
extracted question / structure
    ↓
publicly available ontological reconstruction
    ↓
claim responsibility and scope of application
    ↓
non-identity with standard domains
    ↓
objection, residual, and return path
```

The goal here is to test whether ontological aspects that science does not treat, or that a given science operationally abstracts away as noise, can be reconstructed **as another descriptive surface**, rather than as a substitute for science itself.

Even if successful, this would not mean that standard physics or another specialized field had been replaced.

Nor is the value of such a reconstruction grounded in the claim that it reveals “the true bottom of the world.” Its value is examined in terms of how far it enables communication, objection, correction, and reconnection among different descriptive systems.

③ is likely to be repeatedly revised through ① and ②.

---

## 7. ④ Re-read the movements among ①–③ as a history of SO's formation

As ① through ③ are traversed repeatedly, the route itself may overlap with the history by which SO took shape.

SO has repeatedly developed by picking up structures from external concepts, discomforts, failures, residuals, creative metaphors, and technical implementations, inserting them into another position, and testing them again.

At present, this tendency is not treated as an established principle.

> SO may have a recurring historical tendency to pick up a structure from outside or from a residual, insert it into an existing system, and then test the result again through another connection.

This is recorded as a historical hypothesis.

④ does not rewrite the past into a single path from the standpoint of the current theory.

Instead, it records:

- what was treated as a problem at that time;
- what was picked up;
- where it was inserted;
- what worked;
- what broke;
- into which concept it was later repositioned.

This work includes not only factual recording, but also the creative aspect involved in how the present reconstructs and reads the past.

For that reason, it may later be possible to place this work as a **biographical second volume** following Volume I.

Such a document, however, would not be “the one true history of SO.” It would be explicitly identified as a history reconstructed from the present audit method.

---

## 8. ⑤ Do not create research fields first; recover them from ④

Judgment Transparency, Transformation Audit, Attribution / Authority, Boundary Communication, Ground / Stopping, Repository / Navigator, and other themes can already be seen as issues that may develop into independent research lines.

At the present stage, however, they are not fixed as completed research divisions.

Only when a structure repeatedly appears across different times and different objects while writing ④ should it be separated as a candidate research field under ⑤.

The candidate is then returned to ①.

> Is this genuinely an independent philosophical problem?
>
> Or is it a classification produced by SO's internal document structure or a temporary implementation convenience?

Keeping ⑤ in circulation with ① is a condition for preventing the research from becoming a disconnected collection of categories.

---

## 9. Current position

At the time of Volume I, the research had mainly reached the point where ① was giving rise to ②.

Through De-Registry, Sol/Luna comparison, attribution problems, Topology-first, and three-layer transformation audits, a method for auditing the transparency of judgment generation was formed.

As of the v5.1 preparation stage, the document contract, assessment review, registration transaction, and review interface in the Developer Navigator that support ② have been implemented. This does not automatically guarantee that audit results are correct; it provides an infrastructure for separating and tracing candidate generation, review, approval, and reflection into the authoritative corpus.

The next principal task is to accumulate ② as an actual audit practice and return the resulting findings to ③.

- Generate self-audit candidates for SO's authoritative documents and pass them through human review.
- Reflect only approved results through explicit registration transactions.
- Before changing authoritative text, expose claim responsibility, attribution, connection strength, and residuals.
- Return grounds and assumptions exposed by the audit to 3.

① continues to accumulate questions in parallel.

③ begins where ② has exposed enough contact points.

④ has already begun, but it is not closed into a completed history.

⑤ has not yet been designed.

---

## 10. Non-claim boundary

This roadmap does not claim that:

- LLMs can automate philosophical research;
- communication topology is a necessary and sufficient condition for philosophical validity;
- a defect found in SO's authoritative documents refutes SO as a whole;
- unpublished metaphysical materials are the secret grounds of public SO;
- physics-adjacent descriptions in AMP, ITS, PINGER, or related materials are established claims of standard physics;
- SO automatically treats correctly whatever science does not treat;
- the value of grounds is determined only by communicability;
- items ① through ⑤ are the final classification of this research.

What is fixed here is the provisional operational direction: where the research is opened, where it is returned, and which parts of its history are not to be erased.

---

## 11. Routes from this document

- Philosophical research question ledger → [`01_PHILOSOPHICAL_RESEARCH_QUESTIONS.en.md`](./01_PHILOSOPHICAL_RESEARCH_QUESTIONS.en.md)
- Entry to Volume I → [`volumes/Volume_01_DeRegistry_to_Judgment_Transparency/README.md`](./volumes/Volume_01_DeRegistry_to_Judgment_Transparency/README.md)
- Frozen results of Volume I → [`01_CHRONICLE.ja.md`](./volumes/Volume_01_DeRegistry_to_Judgment_Transparency/01_CHRONICLE.ja.md)
- Trials, failures, and turns → [`02_TRANSMISSIONS.ja.md`](./volumes/Volume_01_DeRegistry_to_Judgment_Transparency/02_TRANSMISSIONS.ja.md)
- Current Judgment Transparency interface → [`03_JUDGMENT_TRANSPARENCY_TOPOLOGY.ja.md`](./volumes/Volume_01_DeRegistry_to_Judgment_Transparency/03_JUDGMENT_TRANSPARENCY_TOPOLOGY.ja.md)
- Public evidence and Hold boundary → [`04_PUBLICATION_AND_EVIDENCE_MAP.md`](./volumes/Volume_01_DeRegistry_to_Judgment_Transparency/04_PUBLICATION_AND_EVIDENCE_MAP.md)
- Unresolved differences → [`05_RESIDUALS_AND_NEXT_TESTS.ja.md`](./volumes/Volume_01_DeRegistry_to_Judgment_Transparency/05_RESIDUALS_AND_NEXT_TESTS.ja.md)

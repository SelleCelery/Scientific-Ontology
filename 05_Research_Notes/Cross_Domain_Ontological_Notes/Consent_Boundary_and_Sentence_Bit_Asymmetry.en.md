# Consent Boundary and Sentence/Bit Asymmetry
## Compression of the Right of Response in Terms Presentation, Medical Explanation, and Constrained Acceptance

> Status: Research Note / Application Bridge  
> Language: English commensurated rendering  
> Japanese authoritative source: [`Consent_Boundary_and_Sentence_Bit_Asymmetry.ja.md`](./Consent_Boundary_and_Sentence_Bit_Asymmetry.ja.md)  
> Related application: DSSI / Digital Sovereignty Support Interface  
> Claim strength: Conceptual model / design hypothesis  
> Legal status: This document does not determine the legal validity or invalidity of any agreement.

---

## 0. Position of This Note

This note addresses a structural asymmetry between the presenting side and the responding side that appears in terms of service, privacy policies, medical explanations, permission interfaces, and related contexts.

The central problem is not merely that "terms are long" or that "users do not read them."

The presenting side can describe conditions, exceptions, reservations, disclaimers, future changes, third-party provision, limitations of responsibility, governing law, uncertainty, and other matters as a bundle of sentences.

The responding side, by contrast, is often compressed into a single bit:

- agree;
- disagree.

Such a response format cannot adequately return the user's actual cognitive state, limits of understanding, necessity, reservations, available alternatives, or practical ability to refuse.

This note describes the problem as **Sentence/Bit Asymmetry at the Consent Boundary**.

---

## 1. Central Proposition

### 1.1 The Presenting Side Has Sentences; the Responding Side Is Compressed into a Bit

The party presenting terms or explanations can accumulate multiple conditions in documentary form.

The user's response is meanwhile reduced to one state by a checkbox or button.

```text
presenting side
  conditions
  definitions
  exceptions
  disclaimers
  reservations
  future changes
  uncertainty
  scope of responsibility
        ↓
user side
  agree / disagree
```

Here, the binary character of the final action is confused with binary recording of the judgment process itself.

Even where the action ultimately takes a binary form—execute or do not execute—the history leading to that judgment is not binary.

### 1.2 A Consent Bit Identifies Distinct Cognitive States as the Same

Behind the same operation of "agree," at least the following states may exist:

1. I read the entire text, understood it, and accepted it.
2. I read the principal conditions and understood the important parts.
3. Some parts remain unclear, but I judged them acceptable.
4. I could not evaluate the disclaimer or future effects, but accepted because use was necessary.
5. There were few practical alternatives, so I proceeded reluctantly in order to continue using the service.
6. I exercised the degree of care reasonably expected in ordinary practice, but more extensive review was not realistically possible.

Current consent interfaces often save all of these as the same bit.

As a result, the distinction is lost between full understanding and approval, on the one hand, and practical acceptance that retained limits of understanding, on the other.

---

## 2. Constrained Acceptance

### 2.1 Practical Acceptance Rather Than Full Assent

Even when a service is attractive or necessary, users may not be able to evaluate its disclaimers, data use, future modifications, or allocation of responsibility adequately.

They may nevertheless face pressure to choose for reasons such as:

- the service is necessary for work or daily life;
- there is no substantive alternative;
- they lack the time or expertise required to review the entire text;
- the cost of not using the service is high; or
- it would be unrealistic, under ordinary social expectations, to require further investigation from an individual.

This state is not necessarily free and comprehensive assent.

The following formulation may be closer:

> I did not fully understand or approve the entire content. I exercised reasonable care within the range in which obvious risks could be checked, retained what I could not understand as unresolved, and continued use because of necessity and practical constraints.

This note provisionally calls such a state **Constrained Acceptance**.

### 2.2 Do Not Automatically Classify It as Coercion

Constrained Acceptance is not a concept for immediately classifying every such case as coerced consent.

DSSI or another observation system should avoid automatically determining that:

- the user was coerced;
- consent is invalid;
- no agreement was formed; or
- the operator acted illegally.

Instead, observed facts and user declarations should be separated.

#### Observed Facts

- the interface did not allow progression without agreement;
- no refusal surface could be detected;
- an agreement button was presented as the primary operation;
- the terms appeared on a separate screen or inside a collapsed section;
- the display time was short relative to the apparent length of the document;
- multiple permissions were bundled together.

#### User Declarations

- I did not read the entire text;
- I did not understand part of the text;
- I could not evaluate the scope of the disclaimer;
- continued use was necessary;
- there was no substantive alternative;
- I accepted with reservations rather than with full assent.

This separation prevents the system from making proxy determinations about the user's inner state or legal conclusion.

---

## 3. Functions and Limits of Documentary Form

### 3.1 Terms Documents Have a Function as a Preservation Format

Presenting terms in documentary form has genuine functions:

- detailed conditions can be described;
- definitions can be related to exceptions;
- the text can be consulted later;
- a version can be fixed;
- the same conditions can be presented to many users; and
- relations among clauses can be preserved.

The problem is therefore not the use of documents itself.

### 3.2 Documents Are Strong at Preserving Conditions but Insufficient as Consent Interfaces

A document can preserve the meaning articulated by the presenting side.

It does not, however, necessarily provide a Port through which the responding side can return their state of understanding or reservations.

```text
terms document
  strong at preserving conditions and detailed description

consent button
  weak at describing the user's response
```

The problem lies in the extreme difference between the resolution of presentation and the expressive capacity of response.

### 3.3 Sentences Preserve Reservations on the Presenting Side

Through sentences, the presenting side can preserve formulations such as:

- as a general rule, we do not assume responsibility;
- except where exemption is not permitted by law;
- conditions may be changed as necessary;
- we are not responsible for third-party services.

These sentences retain rules, exceptions, interpretive space, and future conditions.

The user, however, may have no format for returning statements such as:

- I agree to the conditions required for the principal function;
- I do not agree to secondary use;
- I cannot evaluate the scope of the disclaimer;
- I reserve judgment on the future-change clause;
- I provisionally accept because use is necessary.

When only the presenting side has sentences and the responding side is restricted to a bit, semantic asymmetry expands.

---

## 4. Structural Commonality with Medical Explanation

Medical explanations also contain multiple layers of meaning on the presenting side:

- diagnosis;
- treatment options;
- probability of success;
- side effects;
- prognosis;
- alternative treatment;
- uncertainty;
- consequences of non-treatment.

Yet the patient's final response may also be compressed into consent/non-consent.

The patient's actual state can be composite:

- I understand the need for treatment;
- I understood part of the explanation;
- I do not fully understand the meaning of the probabilities;
- I lack sufficient time to compare alternatives;
- I feel anxiety or fear;
- I proceed partly on the basis of trust in the physician;
- I also find the consequences of refusal difficult to bear.

Here again, the binary form of the final action does not mean that the judgment process itself is binary.

Contractual consent and medical consent are not the same. They nevertheless share a structural feature: **the asymmetry between a side that explains through sentences and a side that responds through a bit**.

---

## 5. The Consent Boundary

### 5.1 Consent Is Not a Point but a History

Formally, the moment at which the user presses an agreement button may be treated as the point of consent.

In practice, a history leads to that point:

```text
presentation
contact
viewing
non-viewing
understanding
non-understanding
confirmation
reservation
necessity
availability of alternatives
ability to refuse
operation
```

The consent button compresses this history into one bit.

The problem at the Consent Boundary is not compression itself.

It is **treating the post-compression bit as though it were the whole history**.

### 5.2 Distinctions Required at the Consent Boundary

The process by which consent is formed can be divided into at least the following layers.

1. **Presentation Conditions**  
   What was presented, where, and in what form.

2. **Contact Conditions**  
   Whether the user could access the document or its key points.

3. **Viewing Conditions**  
   Whether it was opened, display duration, scrolling, contact with headings, and similar observations.

4. **Comprehension Declaration**  
   How much the user reports having understood.

5. **Reservation State**  
   What remained unclear, unevaluable, or unconfirmed.

6. **Choice Conditions**  
   Whether refusal, holding, partial consent, or alternatives existed.

7. **Final Operation**  
   Whether the user agreed, refused, held, or exited.

8. **Legal Evaluation**  
   Not determined automatically; retained for separate professional judgment.

---

## 6. Application to DSSI

### 6.1 Consent Boundary Log

DSSI does not need to judge the morality or legal validity of terms on behalf of the user.

What DSSI can address are observable conditions around a consent operation and the user's own declarations.

Possible future modules include the following.

#### Consent Surface Detection

- consent checkbox;
- agreement button;
- refusal button;
- hold or decide-later operation;
- link to terms of service or privacy policy;
- indication of mandatory/optional permissions.

#### Terms Presentation Observation

- whether the document was opened;
- display duration;
- approximate document length;
- number of headings;
- last-updated date or version;
- presence of highlighted important matters;
- presence of a refusal route.

#### Comprehension Self-Declaration

- read the entire text;
- reviewed key points only;
- partially unread;
- partially incomprehensible;
- unable to perform specialist evaluation.

#### Constraint Declaration

- continued use required;
- required for work;
- few practical alternatives;
- insufficient time;
- reluctant acceptance;
- acceptance with reservations.

#### Consent History Receipt

- terms version;
- presentation conditions;
- viewing history;
- self-declaration;
- final operation;
- observation limits.

### 6.2 Do Not Record Legal Conclusions

A Consent Boundary Log should not automatically generate conclusions such as:

```text
the agreement is invalid
consent was not formed
the operator acted illegally
the user bears no responsibility
```

Instead, it should preserve the history preceding legal evaluation.

```text
the terms were presented
no summary of key points was detected
no refusal route was detected
the user declared partial incomprehension
the user declared a need to continue using the service
the user performed the consent operation
```

### 6.3 A User-Side Copy of Consent History

Operators can often preserve the date and time, terms version, consent operation, and related records.

Users are less likely to retain the presentation conditions, limits of understanding, reservations, and refusal possibilities present at the time of consent.

A DSSI Consent Boundary Log could reduce this asymmetry in retained records.

This is not a function for destroying agreements, but for **making contract history more symmetrical**.

---

## 7. A Design That Does Not Require AI

### 7.1 Standardized Presentation Can Reduce the Need for AI Interpretation

Support for understanding terms is easily connected to AI summarization.

AI summarization, however, inserts a new interpreter.

```text
source text
  ↓
selection and summarization by AI
  ↓
user
```

Important clauses can be omitted, meaning can shift, or responsibility can become unclear.

DSSI's primary design direction therefore need not be full-text AI interpretation.

If the presenting side provides machine-readable declarations of the following, DSSI can display principal conditions without AI:

- important clauses;
- mandatory consent items;
- optional consent items;
- effects of refusal;
- purposes of data use;
- retention period;
- third-party provision;
- scope of disclaimers;
- cancellation and withdrawal procedures;
- changes from the previous version;
- references to the full text.

### 7.2 Reversible Hierarchy Rather Than Irreversible Compression

What is needed is not mere shortening.

The following layers should remain connected:

```text
full text
key points
material clauses
exceptions
effects on the user
reference to source clause
```

The user should be able to return from a summary to the original clause.

This is not compression that discards meaning, but hierarchy that preserves connection and reversibility.

### 7.3 Standardizing Response Buttons

The responding side also needs a standard capable of returning multiple states.

Examples:

- understand and agree;
- reviewed key points and agree;
- continue use while retaining unresolved points;
- accept mandatory items only;
- reject optional items;
- decide later;
- decline and exit.

If these become machine-readable attributes rather than mere display labels, DSSI could read the state without AI.

Provisional conceptual examples:

```text
consent-full
consent-essential-only
consent-with-reservation
decline-optional
defer
decline-all
```

These are not proposals for an existing standard. They are placeholders indicating a design direction.

---

## 8. Hypothesis Concerning Social Effects

If the existence of user-side Consent Boundary Logs became widely recognized, operators might face pressure to improve:

- layered presentation of terms;
- explicit presentation of material clauses;
- display of differences from the prior version;
- separation of mandatory and optional permissions;
- explanation of effects of refusal;
- acceptance of responses with reservations;
- standardization of the meaning of consent buttons;
- explicit terms-version information; and
- machine-readable consent conditions.

Where presentation remains ambiguous, user-side history could retain states such as:

```text
material conditions could not be identified
no refusal route was detected
user declared incomprehension
accepted because continued use was necessary
```

By contrast, operators with well-designed consent processes could make their clarity and refusal options verifiable.

A Consent Boundary Log is therefore not merely a device for attacking operators.

It can also become a device for **making good consent design identifiable**.

---

## 9. Non-Goals and Cautions

This model does not aim to provide:

- an excuse not to read terms;
- automatic denial of contractual obligations;
- invalidation of all agreements;
- automatic accusation of operators;
- automatic inference of the user's understanding;
- a substitute for legal advice; or
- unconditional justification of AI summarization.

Scrolling and display time do not prove reading or understanding.

```text
scrolled to the bottom
≠ read the entire text
≠ understood its meaning
≠ accepted it
```

Observed facts, correlations, estimates, self-declarations, and legal evaluations must remain separate.

---

## 10. Central Public Formulations

### Short Definition

> A Consent Boundary is the boundary history through which conditions are presented, a user encounters them, carries understanding or non-understanding together with constraints and reservations, and reaches a final operation.

### Central Proposition

> If the presenting side can state conditions in sentences, the responding side also needs a Port through which reservations can be returned in sentences.

### Connection to DSSI

> DSSI does not adjudicate the legal validity of consent. It returns to the user the presentation conditions, observed facts, limits of understanding, declared constraints, and final operation that existed before they were compressed into a consent bit.

### AI Is Not Required

> If material conditions in terms and response states are standardized in machine-readable form, DSSI can visualize the Consent Boundary without requiring AI interpretation of the full text.

---

## 11. Future Research Questions

1. Formal modeling of sentence presentation / bit response.
2. Distinguishing Constrained Acceptance from free will.
3. The status of observed facts and self-declarations in evidentiary contexts.
4. A reversible hierarchy specification for terms documents.
5. Machine-readable attributes for consent operation surfaces.
6. Minimum common vocabulary for material-clause classification.
7. Terms-version differences and version collation.
8. Hash-based collation without retaining full text.
9. Tamper resistance of local logs.
10. Limits of application to medicine, employment, administrative procedures, and educational permissions.
11. Relation between accessibility and comprehensibility.
12. Risk that DSSI judgment support itself becomes a new formalism.

---

## 12. Future Bridge to DSSI Implementation

Future modules that can be bridged directly from this note into DSSI include:

```text
Consent Boundary Protocol
  ├─ Consent Surface Detector
  ├─ Terms Presentation Observer
  ├─ Choice Availability Detector
  ├─ User Reservation Declaration
  ├─ Consent Trace Receipt
  └─ Consent Boundary Export
```

Initial implementation should not begin with legal evaluation or AI summarization.

The priorities should be:

1. detecting consent surfaces and links to terms;
2. detecting the presence of mandatory / optional / refusal / hold operations;
3. collecting observable information such as terms version, update date, and approximate length;
4. allowing users to self-declare understanding state and constraints;
5. retaining a local receipt at the time of the consent operation; and
6. making unobservable matters explicit.

In this order, DSSI can increase the resolution of the consent-formation process without replacing user judgment.

---

## 13. Provisional Conclusion

Current consent interfaces give the presenting side the freedom of sentences while restricting the responding side to a single bit.

This asymmetry cannot be explained solely by user negligence. It is a problem of the consent environment, including document volume, specialization, necessity, availability of alternatives, refusal routes, and time constraints.

DSSI does not need to be a device that judges terms on the user's behalf.

Its value may instead lie in retaining the history that exists before consent is compressed into a bit and restoring a Port through which users can respond while preserving reservations.

This requires attention not only to AI interpretation of terms, but also to non-AI improvements in institutions and interfaces: layered terms presentation, explicit material conditions, standardized response buttons, and user-side copies of consent history.

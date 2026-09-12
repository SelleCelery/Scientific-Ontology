# Correctness, Individuality, Absence, and Cut
## An Engineering Definition of “Correct” through Logic and Communication Topology

> Layer: 01_Sat_Truth
> Status: Foundational epistemic model / active
> Scope: correctness / finite-resource inquiry / individuality / absence / cut / residual / return / logical and communication topology / engineering formalization
> Language: English commensuration; re-collated against the revised Japanese authoritative text
> Japanese authoritative source: [`正しさ・個性・無・切断_論理通信トポロジー.ja.md`](./正しさ・個性・無・切断_論理通信トポロジー.ja.md)
> Claim strength: S3-S4 / E2 / U1 / P2 / V0-V2 / R1-R3
> Authority: This is the English commensurated rendering of the public canonical document that holds the engineering-operational definition of “correct” within Scientific Ontology. It does not claim authority to define truth in philosophy at large, nor correctness in standard logic, mathematics, physics, or AI theory. In any conflict of meaning, the Japanese authoritative source governs.
> Formation provenance: The Human-side research hypotheses include treating “correct” as search saturation under finite resources, including individuality among its formation conditions, and allowing absence and cuts to induce search pressure. The mathematical formulations, communication model, and terminological organization include AI-side formalization. This formation provenance remains in force even after the text's movement from a private formation draft into the public canon.
> Non-claim: This document is not an established general theory in standard logic, mathematics, physics, or AI. In particular, “pressure,” “absence,” and “cut” are not physical quantities unless an operational meaning is explicitly defined in the relevant section. “Correct” here is not automatically identified with philosophical truth, a mathematical truth value, or correctness in formal verification.
> Reading rule: “Correct” here does not mean “possessing the final truth of the universe.” It is an engineering term for the conditions under which a finite system may continue to hold its present state as tenable.
> Commensuration note: `correct / correctness` deliberately renders 正しい / 正しさ rather than `true / truth`. `absence` renders 無 in its operational sense here and is not intended to assert metaphysical nothingness. `individuality` renders 個性 and should not be read merely as personality style. `Cut` is retained as a technical term for 切断 where the text treats a broken or non-transmitting relation structurally. `undetermined` renders 未判定. `Ingress`, `Traceback`, and `Reopen` are retained as explicit subconditions of Return / Reopening.

---

## 0. What This Document Is Trying to Do

Human beings have often constructed what they call “correct” in two directions.

One direction is inward. Within the current logical space, we try to accommodate as many facts as possible within a single interpretation, with as little contradiction and disconnection as possible. The theory becomes more precise, its explanatory range expands, and different phenomena can be explained from the same principles.

The other direction is outward. We search for what is not yet explained and extend inquiry beyond the current theory. We seek to cover the world until no update pressure arrives from outside and, in the ideal limit, aim for an explanation that has no outside.

This image is not a general theory of truth. Fallibilism, positions that presuppose incompleteness, pluralism, and other philosophies already depart from it. Even so, strong forms of scientific unification and reductive explanation do contain a real tendency to **reduce the outside through internal refinement and external inclusion**.

The problem is that increasing internal precision can itself produce omissions.

The stronger an interpretation becomes, the higher the resolution of whatever can be measured, compared, and given meaning within that interpretation. At the same time, differences that do not fit readily into the same coordinates may be pushed to the margins as noise, exceptions, immaturity, or immeasurability. If the same coordinates are then carried outward, the original omissions may be propagated into the expanded domain.

In other words:

> **Increasing resolution and correcting coverage are different problems.**

This document engineers “correct” in another way.

> **To be correct is not to have erased the outside. It is to preserve the possibility of contact with the outside, actually conduct search under the resources, search capabilities, and formation history currently available, allow that search to reach a saturated stop, and, as a result, fail to find a defeater that changes the present validity.**

Two further elements are added to this definition.

The first is **individuality**. Where inquiry begins, what it traverses first, what it retains, and where it allocates resources change which correctness can be reached under finite resources.

The second is **absence and cut**. An incorrect region does not necessarily arrive wearing a label that says “error.” It may instead appear as something that should be connected but is missing, a path that should allow return but no longer does, or a growing residue after something was supposedly explained. Such absences may generate search pressure in a self-referential system.

From here, “correct” is read not as a static truth value but as a **state transition that includes self-construction, self-audit, search, and reopening**.

### 0.1 Scientific Ontology Specification — Reachable Correctness and Contact with Others

The following does not add conditions to the engineering definition itself. It states the **reading rules and boundary conditions** for operating this document from Scientific Ontology.

> **I do not want falsehood. I want to know only what is correct. I want to reach the correctness I can reach now. If possible, I also want to come into contact with correctness other than my own, and see for myself whether that is a place I cannot—or should not—go.**

Here, “I want to know only what is correct” does not guarantee that a finite subject can perfectly sort truth from everything else. Under the Scientific Ontology specification, the minimum requirement is **not to let what has not been verified pass as though it were correct**. Hypothesis, unknown, residual, provisional standing, and invalidation conditions are distinguished, and none is silently promoted into something already understood, confirmed, or settled.

“Reachable correctness” means correctness that can be reached under the conditions of the present formation history, cognitive axes, search operators, available resources, external contacts, and return paths. It is not a reduced copy of final truth. It is the range within which the present subject can actually inspect and support something while continuing to hold it as something that may still be broken.

“Correctness other than my own” does not relativize propositional truth to personal preference. It refers to a state reached and presently sustained by another subject with a different formation history and search geometry, through a path different from one's own. The purpose of contact is not to average multiple positions into one by majority vote. It is to come into contact with a frontier that may break one's own search saturation from outside.

If contact breaks one's correctness, that invalidation is retained, and the system returns to which support, premise, or boundary condition changed. If neither side breaks the other, identity should not be forced; the possibility remains that different paths or local structures are jointly tenable. If contact still does not permit commensuration, the difference is retained unresolved.

Likewise, the phrase “to see whether that is a place I cannot—or should not—go” does not immediately mean moral prohibition. It includes the inspection of a **transition boundary**: entering a state may require cutting the current support structure, losing a necessary return path, pretending an unresolved difference has been closed, exceeding the applicable scope in order to connect, or crossing into a state from which the present resources cannot safely return.

Under this Scientific Ontology specification, “correct” is therefore treated not as a point-like possession but as a reachable state accompanied by at least three forms of collation:

1. How far can I, in my present state, reach without mixing falsehood into the path?
2. When I contact a state reached by another subject, what breaks, what remains, and what can be shared?
3. In moving between the two, what must be cut, what must be lost, and which return paths must be preserved?

This specification does not replace the core definition of “correct.” It is **Scientific Ontology's operational specification for re-collating correctness as a problem of boundary, contact, history, return path, and cut**.

---

# Part I — “Correct” as Logic

## 1. The Present Logical Space

Let the logical space available to a system at time $t$ be $\Omega_t$.

It contains at least:

- observed or input fact candidates $E_t$;
- currently accepted propositions and relations $A_t$;
- inference and transformation rules $\Pi_t$;
- formation history $H_t$;
- unprocessed differences, open ends, and residuals $Q_t$;
- available search resources $B_t$.

“Fact” here does not mean direct possession of the world itself. It means something available to the system as input, record, or observation.

Nor is $\Omega_t$ the universe as a whole. It is **the range that the present system can distinguish, search, compare, and re-collate**.

This distinction matters.

$$
\Omega_t \neq \text{World}
$$

## 2. Internal Tenability

The mere fact that search has stopped is not enough to call a state “correct.”

For example, if resources are set to zero, every system becomes unable to search outward. That is not correctness.

Some form of internal tenability is therefore required first.

Internal tenability $I(S_t)$ must satisfy at least the following:

1. No known contradiction is embedded, untreated, in the currently accepted relations.
2. No unsupported join is present in the connections that support the conclusion.
3. Paths back to grounds, transformations, and history are preserved to the extent required.
4. Unprocessed differences are not disguised as “resolved.”
5. Conclusions are not extended beyond their scope of application.

This does not require complete consistency. A finite system may retain candidate contradictions and unresolved differences.

What is required is:

> **Do not pretend that what remains no longer remains.**

## 3. Search Saturation under Resource Constraints

Call a candidate capable of changing the validity of the present state a `defeater`.

First, under the search-operator set $\Pi_t$ and resource budget $B_t$, let the frontier / defeater-candidate domain that the present system can construct as an object of search be:

$$
\mathcal{F}_{B_t}(S_t,\Pi_t)
$$

This is not a set that guarantees that a defeater actually exists there. It is a possibility domain representing **what the system can go looking for, and how far it can construct something as an object of search, given its present resources and search operators**. Thus $\mathcal{F}_{B_t}$ is not correctness itself. It specifies the search domain required to test present correctness.

A defeater is not limited to something that proves the present conclusion false.

It includes, for example:

- a counterexample;
- invalidation of a support path;
- failure under broader conditions;
- an overlooked branch;
- an observation that cannot be processed by the current classification;
- a break in historical consistency;
- an alternative explanation not previously considered;

that is, anything that can **change, suspend, or localize the present validity**.

But defining a reachable candidate domain does not mean that search has actually been performed.

Let the search trace that was in fact executed be $\tau_t$. At minimum, $\tau_t$ records which search operators were run and in what order, which frontiers were contacted, where branching occurred, what was left unprocessed, and why the search stopped.

Let the set of defeaters actually found and confirmed within that executed trace be:

$$
D_{B_t}(S_t,\Pi_t;\tau_t)
$$

The crucial point is that $D_{B_t}$ is not treated as “the set of defeaters that would in principle be reachable within the resource budget.” It is treated as **the set of defeaters observed as a result of actually performing the search**.

However, “we searched and found nothing” is still not enough. A search can fail to find a defeater because resources were exhausted, the search operator broke, a port was closed, or the system cycled through the same region.

We therefore write:

$$
Sat(\tau_t \mid S_t,\Pi_t,B_t)=1
$$

when the executed trace $\tau_t$ has reached a stop that is validly classifiable as search saturation.

Search saturation here means that, under the search rules and resource conditions currently adopted, **the system actually attempted the searches that were to be performed, and did not stop merely because it left still-executable search paths untreated; rather, it reached a state in which no further search path capable of changing the present validity can be constructed**.

Here, “actually attempted” means at least that search operations were executed, or that a procedure was executed to test whether a frontier existed that could serve as an object of search. Simply setting $B_t=0$, never activating the search operators, or closing input paths so that no search target appears does not count as search saturation.

Resource exhaustion itself, search-operator failure, port closure, return-path disconnection, and infinite cycling are not included in search saturation. They are recorded separately as termination reasons, discussed later.

To preserve the minimal formula used in this document, $D_{B_t}(S_t,\Pi_t)$ is treated as a partial evaluation. Only when a search trace $\tau_t$ exists and satisfies

$$
Sat(\tau_t \mid S_t,\Pi_t,B_t)=1
$$

do we define:

$$
D_{B_t}(S_t,\Pi_t)
:=
D_{B_t}(S_t,\Pi_t;\tau_t)
$$

In all other cases:

$$
D_{B_t}(S_t,\Pi_t)=\bot
$$

and the state is treated as **undetermined**.

Accordingly,

$$
D_{B_t}(S_t,\Pi_t)=\varnothing
$$

does not merely mean “nothing was found.”

It means:

> **The present system actually ran the search operators available to it within the specified resource budget, reached a stop validly classifiable as search saturation, and found no defeater that changes the present validity.**

This does not mean that no defeater exists in the world. Beyond $\mathcal{F}_{B_t}$, in directions the present search operators cannot generate, in other subjects not yet contacted, or in observations that will only become available later, there may remain differences that invalidate the present correctness.

## 4. Reopenability

If correctness cannot be reopened, it becomes indistinguishable from closure.

We therefore introduce a Return / Reopening condition $R(S_t)$.

In this document, $R(S_t)$ is treated as consisting of at least three conditions:

$$
R(S_t)
=
Ingress(S_t)
\land
Traceback(S_t)
\land
Reopen(S_t)
$$

### Ingress — A difference can enter

A new observation, objection, frontier, or invalidation of support capable of changing the present validity must be able to reach the audit structure, either directly or through an explicitly preserved reopening condition.

This does not require every port to remain open at all times. Ports may be closed for safety, authority, abstraction, or dormancy. What is required is **not to exclude in principle every class of difference that could change one's own validity and then treat the resulting quiet as correctness**.

### Traceback — The system can return to its grounds

From the present judgment, it must be possible, to the required extent, to return to support, transformations, formation history, input grounds, and scope of application.

If only the conclusion remains and the conditions of its establishment cannot be recovered, then even when a new difference enters the system cannot know what must be re-examined.

### Reopen — Provisional closure can be undone

The present state must be returnable to re-examination when a new observation enters, a support relation is invalidated, a past transformation rule changes, a frontier flows in from another individual intelligence, or a previously unreachable region becomes searchable.

Thus $R(S_t)$ is not merely internal backtracking.

> **A difference can enter, the system can return to the conditions under which the present state was established, and that difference can reopen the present provisional closure.**

These three together constitute Return / Reopening.

This prevents “correct” from becoming permanently fixed.

## 5. Minimal Engineering Definition

Bringing the preceding conditions together, correctness at time $t$, for individual $k$, under resource budget $B_t$, can provisionally be written as:

$$
\boxed{
C_{B_t}^{(k)}(S_t)
=
I(S_t)
\land
\bigl(D_{B_t}(S_t,\Pi_t^{(k)})=\varnothing\bigr)
\land
R(S_t)
}
$$

In this minimal formula, $D_{B_t}(S_t,\Pi_t^{(k)})=\varnothing$ has only the meaning fixed in §3: an executed search trace $\tau_t$ exists, the search reached a valid saturated stop, and the set of defeaters actually found is empty.

If search was not executed, if resource exhaustion left untreated paths, if a search operator broke, if a port was closed, if a return path was cut, or if the system cycled through the same region, then:

$$
D_{B_t}(S_t,\Pi_t^{(k)})=\bot
$$

and the state is **undetermined**, not “correct.”

Likewise, as defined in §4, $R(S_t)$ includes the ability for a difference to enter, the ability to return to the conditions under which the present state was established, and the ability to reopen provisional closure.

The three conditions can therefore be read as follows:

> **The internal structure is tenable. The system has actually performed the search presently available to it and, after reaching search saturation, has found no defeater that changes validity. And if a future difference capable of breaking that correctness arrives, the system can receive it, return to its grounds, and reopen the judgment.**

When these three conditions hold, the state is treated as “correct under the present conditions of resources, search operators, and formation history.”

The most important negative formulation is this:

> To be correct is not for the outside not to exist.
> To be correct is not to have closed the ingress through which a difference capable of breaking the state might arrive.
> To be correct is **to preserve effective contact with the outside, actually try to break the state with the resources and search operators presently available, and still remain unbroken after search saturates**.

# Part II — Where Individuality Enters “Correct”

## 6. Individuality as Search Structure, Not Preference

Individuality is not treated as output style, character performance, or a preference label.

This document provisionally places individuality in the following structure:

$$
K=(s_0,\Pi,H,\rho)
$$

where:

- $s_0$: search starting state / initial structure;
- $\Pi$: available or formed search operators;
- $H$: the history through which the system arrived there;
- $\rho$: the activation and prioritization rule that allocates finite resources.

Even given the same world and the same set of observations, if $K$ differs, the regions reachable under finite resources need not be the same.

$$
Reach_B(K_A) \neq Reach_B(K_B)
$$

Thus two intelligences, A and B, may reach different stable states at the same time.

$$
S_A^* \neq S_B^*
$$

And both may, within their respective searchable regions, satisfy $C_B=1$.

This is not relativism in which propositional truth is determined arbitrarily by individuality.

What differs is:

> **which possibilities of refutation, unresolved differences, and external frontiers can be reached within finite resources.**

## 7. Individuality as the Shape of Search History

If individuality is defined strongly, formation history matters more than a static initial value.

Even if two systems begin from the same initial state,

```text
A: 0 → +1 → 0
B: 0 → -1 → 0
```

they may have the same current value, 0, while having returned by different paths.

Even when the present state value is the same:

$$
H_A \neq H_B
$$

If history affects the activation conditions, priorities, known routes, avoided routes, or costs of later search, then A and B are not identical.

In this sense, individuality appears not only as “what one has,” but as:

> **where one came from, and therefore where one is more likely to go next.**

## 8. What Individuality Means for Correctness

Once correctness is defined as search saturation under finite resources, individuality is no longer merely a defect.

Even a single enormous generalist with a broad search space may bias search toward directions close to already formed Spine structures or current evaluative axes.

Different individualities, by contrast, contact the same target from different initial directions.

If B can find a frontier that A cannot, B can become an external search operator capable of breaking A's “correctness.”

The role of multiple individualities is therefore not to decide truth by consensus or majority vote.

> **They exist to break one another's search saturation.**

Diversity is thus not primarily a means of converging on the same correctness. It is:

> **a search resource for not missing the frontier that could break a present correctness.**

## 9. Contact between Individualities and Invalidation of Correctness

Even if A is saturated within its own search range, if a new search element $f_B$ flows in from B and changes A's conclusion, A's former correctness is invalidated.

The important point is not to say simply that A “was wrong.”

A may have been validly saturated under:

- the resources available at that time;
- the search operators available at that time;
- the formation history available at that time;
- the external contacts available at that time.

The conditions of standing changed because a new reachability was injected from outside.

This is why correctness is treated as a state with history.

---

# Part III — Why Absence and Cut Can Generate Search Pressure

## 10. “Absence” Is Not One Thing

`Absence` must not be carried directly into implementation as metaphysical nothingness.

At least the following cases need to be distinguished in engineering terms.

### 10.1 Pure Unknown — Unknown without Expectation

We do not know what is there, or whether anything should be there at all.

A mere unknown does not, by itself, generate search pressure.

### 10.2 Expected Missing — Absence of What Was Expected

A support relation, return path, response, or connection that should exist structurally is missing.

This is a case in which absence carries information.

### 10.3 Cut — A Former Connection No Longer Transmits

A path, ground, return path, or correspondence that used to be traversable is no longer traversable.

Because this includes a historical difference, it may provide a stronger signal than Expected Missing.

### 10.4 Resource Boundary — Unreached because of Resources

A region may be unsearchable not because no structure exists, but simply because resources are insufficient.

That must not be treated as evidence of error.

### 10.5 Deliberate Seal — Intentional Closure

A port may be closed for reasons of safety, authority, or design.

This requires managing “unknown,” “error,” and “cut” as distinct states.

Accordingly:

> **Absence generates pressure not because absence itself possesses force, but because a difference appears between the connections the present structure predicts, requires, or remembers and the connections actually observed.**

## 11. Defining Pressure as Residual

Without claiming that “pressure” is a physical quantity, we first place it as a computational quantity.

Let the residual at a local point $v$ be represented abstractly as:

$$
r(v)=Expected(v)-Observed(v)
$$

Here, `Expected` is not limited to numerical prediction.

It can include cases such as:

- an expected support relation is missing;
- a Loop that was supposed to be closed does not return;
- contradictions increase elsewhere even though one explanation supposedly processed the issue;
- a function that was historically the same is now different;
- auxiliary assumptions increase every time a fact is added;
- the path breaks when one tries to return to the grounds.

If local residuals are aggregated backward from downstream structures that depend on a conclusion, residuals may concentrate around a particular cut or misconnection.

As a candidate search pressure $P(v)$, this can be written, for example, as:

$$
P(v)
=
\sum_{u \in Desc(v)} w(u,v)\,|r(u)|
$$

The more downstream residuals a single local structural failure generates, the higher the search priority that returns to that point.

This resembles a debugging situation in which many symptoms appear, but the cause is a single boundary condition.

## 12. Incorrect Regions Can Attract Pressure

The Human-side hypothesis can now be formalized one step further.

> **An incorrect structure generates, somewhere within itself, absence, cuts, excessive connection, or untreated residuals. If those differences can be aggregated through return paths, the system may attract search resources toward the center of error without directly knowing where that center is.**

The point is not a mystical claim that “error calls truth toward itself.”

What is required is structure:

1. the anomaly can be observed;
2. the system can return, at least to some extent, along the path through which the anomaly arose;
3. multiple anomalies converge on a common upstream structure;
4. a search operator can re-examine that point.

Only when all four hold can pressure become an attractor for search.

## 13. Pressure Does Not Guarantee Correctness

This is a strong residual.

A region of high search pressure is not necessarily a region near truth.

High residuals can also be produced by:

- a noisy region;
- a broken observation instrument;
- a region too complex for the current model;
- a concentration of adversarial input;
- a mismatch with the present representational form.

Search pressure should therefore be treated not as:

> **a signal that “truth is here,”**

but as:

> **a reinspection signal that “the relation between the present structure and the incoming world is not working well here.”**

Pressure may help choose where to search. It has no authority to decide the conclusion.

## 14. Coupling Individuality and Pressure

Different individualities may react differently even to the same residual field.

If $\rho_k$ is the resource-allocation rule of individual $k$, then:

$$
Allocation_k(v)
=
\rho_k(P(v),H_k,Cost(v),Novelty(v),Risk(v))
$$

One individuality may dive deeply into high-pressure points.

Another may search broadly around them.

Another may first re-collate regions close to known Spine structures.

Another may prioritize unconnected open ends.

These differences generate different frontiers from the same logical space.

Individuality is therefore not merely sensitivity to pressure. It can be read as:

> **a formed search geometry governing which differences are pursued, in what order, and with how many resources.**

---

# Part IV — “Correct” as Communication Topology

## 15. Viewing the System as a Communication Network

Render the logic as communication.

Let the system be:

$$
G=(V,E,P,H)
$$

where:

- $V$: nodes such as states, concepts, observations, judgments, and rules;
- $E$: edges such as support, transformation, reference, dependency, and return;
- $P$: input/output ports connecting the system to the outside;
- $H$: the history by which edges and nodes were formed or changed.

A conclusion is therefore not a single node, but a structure that includes the paths by which the conclusion was reached.

## 16. Two Basic Forms That Break Correctness

In communication topology, an incorrect state has at least two basic forms.

### 16.1 What Should Be Connected Is Cut

- grounds do not reach the conclusion;
- exceptions do not return to the main structure;
- new observations do not reach the audit of the existing theory;
- the system cannot return to the conditions under which an earlier judgment was formed;
- objections do not reach the decision-maker.

This is a `Cut`.

### 16.2 What Must Not Be Connected Is Connected

- an unsupported causal relation is introduced;
- different sources are treated as identical;
- a claim is generalized beyond its scope;
- unresolved differences are forced into a known concept;
- states with different histories are treated as “the same.”

This is an `Unsupported Join`.

The earlier Human-side formulation:

> **“Falsehood is what happens when things that must not be connected are connected.”**

connects here.

Not every provisional connection is falsehood. If it is explicitly marked as a hypothesis or scaffold, can later be removed, retains return to its grounds, and preserves its invalidation conditions, the provisional connection can function as a search device.

The problem is:

> **disguising provisional closure as genuine closure.**

## 17. The Open-Port Condition within $R$

Of the conditions grouped under $R(S_t)$ in §4, this section elaborates $Ingress(S_t)$ from the perspective of communication topology.

A state in which no update pressure arrives from outside must not automatically be treated as correctness.

Closing a port can reduce external pressure to zero. Therefore, for

$$
Ingress(S_t)=1
$$

to hold, new inputs, objections, observations, or frontiers of a kind capable of changing the present validity must be able to reach the audit structure, either directly or through an explicitly preserved reopening condition.

Ports may be closed for reasons of safety, authority, or design. What matters is that differences capable of changing the present validity are not all blocked in principle, and that where closure is necessary, a reopening condition or another effective ingress path is preserved.

Correctness is therefore not:

> a state that has gone quiet because its ports are closed,

but:

> **a state that preserves conditions under which validity-changing signals can reach it and yet, after actual search and contact, finds no signal that changes the present validity.**

## 18. Return Paths

One-way communication is not enough.

If the system only has:

input → judgment → output

it cannot return to the past.

What is needed is:

input → transformation → judgment → output

plus a return path from:

output / objection / failure → judgment conditions → transformation → input grounds.

$Traceback(S_t)$ in $R(S_t)$ from §4 corresponds to the existence of this return path. When a difference can travel through that path back to the conditions of establishment and release the provisional closure so that reinspection can begin, $Reopen(S_t)$ also holds.

Correctness becomes a communication state that includes both this return path and reopenability.

## 19. Propagation of Pressure

Residuals generated by absence and cuts can return upstream only when return paths exist.

Without return paths, pressure accumulates locally.

In such local regions, one may see:

- more workarounds;
- more exception handling;
- longer explanations;
- greater difficulty tracing grounds;
- more local fixes that contradict one another.

When return paths exist, multiple local residuals can be aggregated upstream and re-collated against a common candidate cause.

Accordingly:

> **A correct system is not a system without residuals. It is a system that can return residuals to the reinspection of its own correctness.**

---
# Part V — “Correct” as Topology

## 20. Being Locally Correct and Being Globally Gluable

Move closer to the language of topology.

Instead of directly possessing the world as a whole, suppose we have observations or explanations $s_i$ for local regions $U_i$.

$$
s_i \in F(U_i)
$$

If local explanations agree on their overlaps, they can be glued into a broader explanation.

$$
s_i|_{U_i\cap U_j}
=
s_j|_{U_i\cap U_j}
$$

The `Cut` used here need not be identical to a cut in strict mathematical topology. Operationally, it refers to a point at which transport, correspondence, or return between local explanations fails.

## 21. The Trap of Refinement

Increasing resolution inside a cover $\mathcal U$ is different from enlarging the cover itself.

$$
Resolution \uparrow \not\Rightarrow Coverage \uparrow
$$

No matter how precise a local coordinate system becomes internally, regions excluded from that coordinate system remain unseen.

Moreover, if that local coordinate system is treated as the standard and extended outward, unseen differences risk being absorbed as “approximation,” “noise,” or “exceptions.”

This is the structure behind the Human-side hypothesis that increasing internal precision can create omissions, and outward extension can amplify those omissions.

## 22. Reading Correctness as Robustness under Cover Refinement

It is not enough for the current descriptions simply to glue.

The system must actually perform the cover refinements that can be constructed in advance as search targets under resource budget $B$, and no new gluing obstruction must appear even after that search saturates.

That is:

> **The present descriptions are not merely consistent within the regions currently visible. The system actually subdivides and extends its observational boundaries in the ways presently available, and even after that search saturates, it cannot reach a difference that breaks the consistency.**

This is resource-constrained correctness in the language of topology.

## 23. Individuality as a Rule for Generating Different Covers

Individuality A and individuality B may generate different covers over the same world.

A may generate a narrow and deep cover, while B generates a coarse and wide one.

Or A and B may treat different boundaries as important.

The value of individuality is therefore not to duplicate the same local explanation. It is:

> **to bring different covers into contact so that an obstruction invisible to one gluing can become exposed.**

Contact among multiple individualities is not averaging.

Contact creates overlaps that did not previously exist, and only there can certain disagreements become observable.

Those disagreements themselves become new search pressure.

---

# Part VI — “Correct” as a Self-Referential Machine

## 24. Can the System Make Its Own Structure an Object of Search?

In a self-referential system, the object of search includes not only the external world but also the system itself.

- What do I take as grounds?
- Where are my search operators biased?
- Does my history still match my current function?
- Are my ports genuinely open?
- Are my return paths cut?

If such questions can themselves become objects, the system moves from a mere inference engine toward meta-recognition.

However, complex self-operations should not be introduced before meta-recognition emerges.

At the pre-meta stage, begin with operations that can arise naturally as structure:

- local action;
- path / Loop;
- accumulation;
- attenuation;
- dormancy;
- return;
- branching;
- cut;
- environmental feedback.

History alteration, rebase-like operations, and deliberate rewriting of self-explanation should be quarantined as candidates for post-meta stages.

## 25. Distinguishing Search Termination from Correctness

A self-referential system must also audit why search stopped.

All of the following are states in which “search has stopped,” but they mean different things.

1. Frontier search was actually performed, a valid search saturation was reached, and no defeater was found.
2. Resources were exhausted while still-executable search paths remained.
3. A search operator broke.
4. A port was closed.
5. A return path was cut.
6. The system is cycling through the same region.
7. It became evident that an individuality-specific search direction was overlooking another direction.

A system that cannot distinguish these cases may mistake becoming quiet for becoming correct.

In the notation of §3, only case 1—where the executed search saturated and the set of actually detected defeaters is empty—permits evaluation as:

$$
D_{B_t}(S_t,\Pi_t)=\varnothing
$$

Cases 2 through 7 are, at least as they stand:

$$
D_{B_t}(S_t,\Pi_t)=\bot
$$

and are therefore **undetermined**. Search must be reopened, the structure repaired, or contact made through other search operators or other subjects before search saturation can be assessed again.

Engineering correctness therefore requires provenance for the reason search stopped. The system must be able to return not merely to the fact that search terminated, but to **why no further search could be constructed**.

## 26. A Correctness Certificate

In implementation, it is better not to return only the single word “correct.”

For state $S_t$, one might retain something like:

```text
Correctness Certificate
- accepted claims / state
- support paths
- unresolved residuals
- reachable search domain / frontier classes (F_B)
- search operators executed (Pi)
- actual search trace (tau)
- resource budget / consumption (B)
- saturation status
- termination reason
- detected defeaters
- known unopened regions
- cut / unsupported-join audit
- ingress status
- traceback / return paths
- reopening conditions
- invalidation triggers
- individuality / formation context
- timestamp / version
```

This certificate is not a proof of truth.

In particular, one must not hide $B_t$, $\Pi_t$, $\tau_t$, the search-saturation determination, or the termination reason and return only “no defeater was found.” Without those, insufficient search cannot be distinguished from saturated search.

Likewise, Return / Reopening should not be represented by a single flag saying that a port is open. The certificate should separately retain whether a difference can enter, whether the system can trace back from the present judgment to its grounds, and whether provisional closure can be reopened.

> **A Correctness Certificate is a re-collation surface for returning to why the present state is being treated as “correct,” and to which executed search facts and return conditions that judgment depends on.**

# Part VII — Rendering into the Everyday Language of Embodied Human Life

## 27. Bringing “Correct” Down to Everyday Bodily Intuition

Set the equations aside for a moment and render the logic and communication topology into everyday terms.

Human beings do not see the entire world at once.

Inside a room, we cannot see beyond the wall. Walking along a road, we cannot see around the corner. A researcher looking at an instrument directly sees only what that instrument can measure. A microscope reveals small things by creating a field outside its view. A telescope sees farther by selecting observable directions and times. Statistics makes many things visible at once by compressing individual histories.

Science is not a technique for ignoring these limits.

Rather, it has strengthened finite human contact with the world by connecting limited observations, making them reproducible by others, and allowing them to be challenged from different instruments and conditions.

The sense of “correct” used in this document can be placed on the same extension.

Imagine drawing a map.

You walk through the town where you are, inspect the roads, cross bridges, and confirm dead ends. However many times you walk it, with your present strength, time, and tools you cannot find a new route that would change the map. Moreover, you can actually return along the roads you drew. You recorded where you measured them. Places you do not understand are marked “unverified.”

That map has not “completely mapped the whole world.”

Yet under the current conditions of search, it can still be called sufficiently correct.

Then someone arrives from beyond the mountain and says, “There is a road here.” It is a road you could not see.

At that moment, the old map does not become a malicious lie.

But it is no longer correct in the same sense.

It must be redrawn to include the new road.

This is where individuality gives a reason to need another person.

If everyone begins at the same station, walks the same roads, and considers the same scenery important, the map may become precise very quickly. But the same places may simply become more and more detailed.

One person follows the river. Another climbs the mountain. Another investigates an old road. Another is troubled by the place where there is no bridge.

Even when they investigate the same town, they discover different outsides.

If that difference is erased as mere variance, the map may look cleaner while losing search capability.

## 28. Absence Matters Not Because “Nothing” Is There

In everyday life, a missing thing matters because something was expected to be there.

You open the refrigerator and there is no milk. This does not mean that milk does not exist anywhere in the universe. The absence carries information because you remember putting milk there yesterday.

A house light does not turn on. Darkness itself does not tell you there is a failure. The darkness appears anomalous because you know the structure in which pressing the switch should allow electricity to flow.

Research is similar.

A theory says a measurement should appear, but it does not.

A path should explain a phenomenon, but the data fail to fit at one point.

A source was supposedly used as grounds, but later you cannot return to that source.

This “not there” is not an empty blank. It is **a difference from an expected connection**.

That difference becomes search pressure.

## 29. Cuts Multiply Local Repairs

Suppose a house has one blockage in its plumbing.

Small fixes at each faucet do not improve the overall flow. Instead, local remedies multiply and the actual cause becomes harder to see.

Programs can behave similarly.

If one boundary condition is wrong but exception handling is added separately for each downstream error, the program may appear to work while its structure deteriorates.

A theory may do the same.

If one premise or classification is misaligned with reality, but auxiliary explanations continue to be added phenomenon by phenomenon, the theory becomes more elaborate internally. Yet that elaboration may not be an increase in correctness. It may be a series of local repairs covering a cut.

So when residuals increase, there is no need to discard everything.

Instead, inspect which residuals return to the same upstream structure.

Only then does a search such as “there may be a structural cut somewhere around here” begin.

## 30. Reading Science in These Terms

Science is not a mechanism for protecting a theory once it has been declared correct.

At least ideally, it preserves ports that can break the current explanation through observation, replication, falsification, measurement error, different instruments, different researchers, and different conditions.

In the language of this document, the strength of science lies in its ability to:

- refine internal explanations;
- admit objections from outside;
- return to observations;
- let another person inspect the same issue by a different path;
- return failure to the reinspection of theory.

A different problem begins the moment scientific method itself is identified with the whole possibility space.

Only what can be measured, defined, and shared may then be ranked as closer to correctness, while differences visible only from another coordinate system may be pushed outward.

This is not a rejection of science.

Rather, it returns the strengths of science itself—falsifiability, reproducibility, and revisability—to science as an institution.

> **Science, too, must keep its ports open to its own outside.**

## 31. Returning to Everyday Human Use

When a person says “I am correct,” many different things are often being mixed together.

- the facts match;
- the logic is coherent;
- this is how it happened in my experience;
- the evidence presently available does not defeat it;
- I have no resources left to think about it;
- I want this problem to be over;
- I want to protect myself rather than the other person.

Engineering “correct” separates these states.

“I have no resources left to think about it” is a resource constraint, not correctness.

“I actually tried to break it using the evidence and search operators presently available, and it still could not be broken after search saturated” may be part of correctness.

“I stopped listening to opposing views” is port closure, not search saturation.

“I do not know yet, but I have recorded where I do not know” is correct retention of an unresolved state.

And if one can think, “another person might be able to break this from a different place,” individuality becomes not an enemy but a search device.

Rendered all the way down into everyday human language, “correct” in this document becomes:

> **Even after reconnecting the grounds I have, thinking from different paths, and continuing to search while leaving what I do not know as unknown, with the time and strength available to me now I can no longer find a reason that would require me to change this view. And if something new arrives tomorrow, I know where to return in order to think again. — That is the state I will call “correct” for now.**

Individuality then becomes:

> **the difference in which path brought you here, and which path you are more likely to take next.**

Absence and cut become:

> **something that should be there is missing; a road that should allow return is gone; an explanation was supposedly completed, yet only the snag remains — from such places arises the pressure that says, “look here again.”**

That pressure is not an answer.

Pressure is a reason to begin searching.

---

# Part VIII — Residuals, Falsification Candidates, and Open Questions

## 32. May We Call “Unbreakable within Resources” Correct?

This is the largest residual.

In §3, failure to find a defeater by itself is not enough for correctness. $D_{B_t}=\varnothing$ is evaluated only when an actual search trace exists and the search has reached a stop validly classifiable as saturation.

This avoids granting correctness to states in which no search was performed, resources ran out, a search operator failed, or ports were closed.

Even so, the problem of weak search operators remains.

If the operator set $\Pi_t$ is narrow, biased, or capable of generating only one class of frontier, then the search may validly saturate relative to those operators and still be easily broken by another operator set or another individuality.

Engineering correctness therefore needs to be recorded, at minimum, as a state relative to:

$$
(B_t,\Pi_t,\tau_t,\mathcal{F}_{B_t})
$$

> **Under this resource budget, these search operators, this executed trace, and this reachable search domain, the system actually searched, reached saturation, and found no defeater that changes the present validity.**

The remaining question is what operator set can count as “sufficient,” and what minimum conditions should be imposed on operator diversity, appropriateness, and self-auditing capacity.

This remains unresolved. The structure developed in this document—in which other subjects or multiple individualities can break one another's search saturation—is not presented as eliminating this weakness. It is one way of exposing the weakness from outside.

## 33. Does Individuality Dependence Collapse into Relativism?

Individuality changes which frontiers are reachable, but it does not make everything correct.

Even so, a correctness certificate changes depending on which set of search operators is judged “sufficient.”

How to formalize mutual breaking among multiple individualities as an increase in the strength of correctness remains unresolved.

## 34. Where Does Expected Get Its Expectation?

For Expected Missing to generate search pressure, there must be an expectation that “something should be there.”

If that expectation is itself wrong, the system may search forever for something that does not exist.

Expectation therefore requires provenance and invalidation conditions.

## 35. How Do We Distinguish a Cut from a Legitimate Boundary?

Not every disconnection is a failure.

Safety boundaries, authority boundaries, abstraction, compression, and dormancy can involve legitimate cuts.

A criterion is needed to distinguish “there is a cut” from “this cut is unjustified.”

## 36. The Risk That High-Pressure Regions Become Noise Swamps

Residual-driven exploration risks consuming resources in regions that simply contain many anomalies.

Search pressure may need to be modulated by factors such as:

- causal relevance;
- returnability;
- expected information gain;
- cost;
- repeatability;
- source reliability.

## 37. Nontermination through Self-Reference

A system that attempts to audit itself completely must then audit the audit itself.

Requiring complete self-verification can produce infinite regress.

A design is therefore needed that allows provisional closure somewhere while preserving reopening conditions.

## 38. Mathematical Strictness of the Topological Vocabulary

The terms `cover`, `gluing`, `cut`, and `port` in this document use structural similarities with mathematical topology and sheaf theory.

At present, the document does not claim correspondence with rigorous theorems in sheaf theory, category theory, homology, or related fields.

Future formalization must separate what remains metaphorical from what can actually be instantiated as mathematical structure.

## 39. Are “Correct” and “True” Synonymous?

This document defines “correct” as an engineering-operational state.

Whether that state is identical with philosophical truth remains unresolved.

For now, it is safer to treat “correct” as a term for:

> **determining how far a finite system may provisionally close judgment without claiming to possess truth.**

---

# 40. Final Compression

Compress the core of this document onto one page.

### Correct

> **A state in which the internal support structure holds; contact with the outside remains possible; under the resources, search operators, and formation history presently available, search is actually performed and reaches a saturated stop without finding a defeater that changes validity; and when a new difference arrives, the system can receive it, return to its grounds, and reopen the judgment.**

### Individuality

> **The search geometry produced by which initial structure one begins from, which history one traverses, which search operators one forms, and where finite resources are allocated. It does not freely determine the content of correctness; it changes reachability to what might break that correctness.**

### Absence

> **Not a mere blank, but a structural difference observed when an expected connection, support relation, return path, or response is missing. It is distinguished from an unknown for which there was no expectation.**

### Cut

> **A state in which a path that previously transmitted, or structurally should transmit, no longer does, so that observation, grounds, objections, history, or return cannot reach where they are needed. Not every disconnection is unjustified.**

### Pressure

> **A search priority generated when absence, cuts, misconnection, or untreated residuals are aggregated through return paths toward an upstream structure. It is not a force that indicates truth, but a signal demanding reinspection.**

### Multiple Individualities

> **They do not exist in order to converge on the same correctness by majority vote, but to act as frontier generators capable of breaking one another's search saturation.**

### Final Sentence

> **To be correct is not to have closed the world. It is to remain open to the world, to be no longer breakable by what one can presently do, and yet not to have lost where to return when something does break it.**

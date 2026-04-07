# Comparison Table

## Purpose

This table provides a compact comparison of the three execution modes used in the Bridge Lite pilot:

- `plain`
- `basis_on`
- `bridge_on`

It is intended as a quick reference alongside the raw logs and `comparison_notes.md`.

The table does **not** replace the raw JSON files.  
It is a human-readable summary of their main differences.

---

## Comparison Overview

| mode | basis reference | bridge transformation | kernel handling | main role | main gain | main risk |
|---|---|---|---|---|---|---|
| `plain` | no | no | implicit / heuristic | structural clarification of the source text itself | reveals the basic internal skeleton without importing external theory | may still perform latent kernel extraction without explicit control |
| `basis_on` | yes | no | basis-aligned implicit handling | conceptual stabilization through basis-aligned restatement | places the text into a more stable interpretive coordinate system | may over-stabilize the text and move too close to bridge behavior |
| `bridge_on` | yes | yes | explicit / governed kernel preservation | structure-preserving transfer with preservation rules | separates invariant kernels from transformable structure and clarifies reading conditions | may over-formalize if basis or preservation rules are too strong |

---

## Mode-by-mode detail

### 1. plain

| item | description |
|---|---|
| execution condition | no basis files, no explicit bridge activation |
| output regime | common explanatory register |
| what it does | reorganizes the source text into a readable structural outline |
| what it does not formally do | no explicit basis alignment, no explicit governed bridge transformation |
| what was observed in the pilot | despite being plain, the output still showed kernel-like structuring |
| interpretation | suggests that ordinary LLM clarification may already include implicit bridge-like behavior |

Reference: raw `plain` run. :contentReference[oaicite:0]{index=0}

---

### 2. basis_on

| item | description |
|---|---|
| execution condition | basis files referenced, bridge inactive |
| output regime | common explanatory register |
| what it does | aligns the source text with basis vocabulary and conceptual coordinates |
| what it does not formally do | no full bridge rewrite with explicit preservation-first governance |
| what was observed in the pilot | terms such as root, void, boundary membrane, and structural language became more stable and interpretable |
| interpretation | adds conceptual grounding and alignment, but still remains close to implicit kernel handling |

Reference: raw `basis_on` run. :contentReference[oaicite:1]{index=1}

---

### 3. bridge_on

| item | description |
|---|---|
| execution condition | basis files referenced, bridge active |
| output regime | common explanatory register |
| what it does | separates invariant kernels from transformable structure and rewrites accordingly |
| what it explicitly adds | protected boundaries, forbidden readings, explicit kernel handling, preservation-first transformation logic |
| what was observed in the pilot | three kernels were made explicit: cross-domain integration, boundary operation, and phase-latent presentation with AI-assisted organization |
| interpretation | turns latent bridge-like behavior into a more explicit, governed, and inspectable process |

Reference: raw `bridge_on` run. :contentReference[oaicite:2]{index=2}

---

## Key interpretive distinction

The present pilot supports the following distinction:

| level | description |
|---|---|
| implicit bridge-like behavior | structure is clarified and kernel-like units may appear without formal preservation rules |
| explicit bridge transformation | preservation targets, protected boundaries, forbidden readings, and audit criteria are made explicit |

This means that Bridge Lite should not be understood simply as “adding bridge ability where none existed.”  
Rather, it may be better understood as a framework for externalizing, stabilizing, and auditing structuring behavior that ordinary LLM processing may already perform in weaker form. :contentReference[oaicite:3]{index=3}

---

## Caution

This table summarizes a **single pilot case**.

It should not be treated as proof of universal behavior across all texts or all models.  
The comparison is useful as an anchor, but further work is needed on:

- multiple text types,
- basis strength variation,
- axiom-profile variation,
- failure cases,
- filter-effect metrics,
- compatibility and conflict measures. 

---

## Suggested use in the repository

This file should be read together with:

- `comparison_notes.md`
- `excerpt_policy.md`
- `raw_plain.json`
- `raw_basis_on.json`
- `raw_bridge_on.json`

Recommended reading order:

1. `comparison_table.md`
2. `comparison_notes.md`
3. raw logs
4. article / note draft
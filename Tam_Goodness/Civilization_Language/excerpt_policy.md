# Excerpt Policy

## Purpose

This document defines how logs from the Bridge Lite pilot may be quoted, excerpted, and presented in public-facing materials such as:

- note articles
- GitHub README files
- short essays
- reports
- presentation drafts

The purpose of this policy is to preserve transparency while avoiding distortion, over-editing, or accidental rewriting of raw comparison data.

---

## Basic principle

Raw logs are treated as primary records.

They should not be silently rewritten for presentation.  
If a cleaner or shorter version is shown in public, that version must be clearly marked as:

- an excerpt,
- a summary,
- or an interpretive note.

The raw JSON files remain the authoritative record.

---

## Primary files covered by this policy

This policy applies in particular to:

- `raw_plain.json`
- `raw_basis_on.json`
- `raw_bridge_on.json`

These files should be stored unchanged in the repository.

---

## What counts as an acceptable excerpt

An acceptable excerpt must satisfy all of the following:

1. **It must be copied verbatim from the raw log.**
2. **It must not alter wording inside the quoted section.**
3. **If text is omitted, omission must be obvious from context or formatting.**
4. **Interpretation must be separated from quotation.**
5. **The mode must always be identified.**

In practice, the safest public excerpt format is:

- `mode`
- `basis_state.active`
- `bridge_state.active`
- `output.title`
- a verbatim excerpt from `output.text`

This format is preferred because it shows the execution condition and the resulting prose without forcing readers to inspect the entire JSON structure. :contentReference[oaicite:12]{index=12}

---

## Recommended public excerpt format

Use the following structure:

### Mode label
Example:
- `plain`
- `basis_on`
- `bridge_on`

### Minimal metadata
Example:
- `"mode":"plain"`
- `"basis_state":{"active":false}`
- `"bridge_state":{"active":false}`

### Verbatim text excerpt
Quote a short section from `output.text` exactly as written.

### Commentary block
After the quote, place a separate commentary paragraph explaining why the excerpt matters.

The commentary must not be presented as part of the raw log.

---

## What should not be done

The following practices are disallowed:

### 1. Silent rewriting
Do not rewrite raw log text for style while presenting it as if it were the original output.

### 2. Selective alteration
Do not adjust terms inside a quote to make the result look cleaner or more favorable.

### 3. Collapsing quotation and interpretation
Do not mix explanatory commentary into the quoted text block.

### 4. Mode concealment
Do not present an excerpt without making clear whether it came from `plain`, `basis_on`, or `bridge_on`.

### 5. Overclaiming from the logs
Do not claim more than the logs show.  
For example:

- do not claim that `plain` performs zero kernel extraction if the raw structure already contains kernel-like units,
- do not claim that `basis_on` is fully non-bridge if its internal structure already shows aligned kernel handling,
- do not claim universal validity from a single pilot case. :contentReference[oaicite:13]{index=13}

---

## Interpretation guidance

The current pilot supports a careful interpretation:

- `plain` shows implicit or heuristic bridge-like structuring,
- `basis_on` shows basis-aligned implicit structuring,
- `bridge_on` shows explicit and governed kernel-preserving bridge transformation. :contentReference[oaicite:14]{index=14}

Public-facing commentary may state this interpretation, but should frame it as a reading of the current pilot, not as a universal claim.

Recommended wording:

> The present pilot suggests that general LLM clarification may already include implicit bridge-like structuring, while Bridge Lite makes such structuring more explicit, governed, and inspectable. :contentReference[oaicite:15]{index=15}

---

## Distinguishing raw data from derived materials

The repository should separate at least three levels:

### 1. Raw logs
Unchanged JSON files.

### 2. Comparison notes
A human-written file such as `comparison_notes.md` explaining the differences between modes.

### 3. Public excerpts
Short quotations reproduced from the raw logs and used in note articles, README files, or essays.

This separation prevents accidental drift between the original data and later presentation.

---

## Recommended repository note

A short note like the following may be placed in README or article drafts:

> Quotations from the comparison runs are reproduced as verbatim excerpts from the raw logs. Interpretive comments are added separately. The raw JSON files remain the authoritative record. :contentReference[oaicite:16]{index=16}

---

## Future extension

If later comparisons introduce:

- basis strength switches,
- axiom-profile switches,
- filter-effect metrics,
- translation-rate metrics,
- compatibility checks,

this policy should be extended so that public excerpts also record the option state under which the quoted result was generated. 

Until then, the current policy is sufficient for the Bridge Lite pilot stage.
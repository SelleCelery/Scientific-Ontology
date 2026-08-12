# Developer Registration Workbench

> Status: Repository maintenance tooling
> Track: Document Navigation Infrastructure
> Stage: DN-5.4C

The Developer Navigator turns document-registration and registered-metadata revision into explicit review transactions instead of direct YAML editing.

## 1. Unified review pool

Two states share one Developer review surface:

```text
Provisional candidate
  = public-readable/searchable candidate not yet canonical in docs_manifest.yml

Registered revision proposal
  = proposed metadata change to an already canonical document
```

The current candidate ledger supplies provisional candidates. Registered reader-question audit proposals are loaded as revision seeds through the Developer-only preview artifact.

A registered document remains registered while its revision proposal is pending.

## 2. Review flow

```text
candidate preview --------------------┐
                                      ├─> unified review pool
registered revision seed preview -----┘
                                      ↓
approve / approve with edits / hold / reject
                                      ↓
browser local review state
                                      ↓ explicit user action
export docs_registration_review.json
                                      ↓
validate_registration_review.py
                                      ↓
apply_registration_review.py --dry-run
                                      ↓ explicit apply
canonical docs_manifest.yml
                                      ↓
rebuild index / graph / public catalog
```

The browser does not write `docs_manifest.yml` directly.

## 3. Public provisional use is separate from canonical approval

Searchable candidate metadata may already be projected into `tools/docs_public_catalog.json` for public Read/Search while review is pending.

That public projection is sanitized. Developer-only confidence, evidence, judgment flags, and review state are not exported to the public catalog. Candidate metadata never creates concept ownership or typed logical relations.

Therefore:

```text
public provisional availability != canonical registration
human review != prerequisite for provisional discoverability
manifest approval != automatic browser action
```

## 4. Review decisions

For provisional candidates:

- `approve`: accept candidate metadata as shown for canonical registration.
- `approve_with_edits`: accept after explicit field edits; export records `before` and `after`.
- `hold`: leave unresolved without changing the manifest.
- `reject`: reject the canonical registration proposal.

For registered revision proposals:

- `approve`: apply the proposed revision on the next explicit repository apply.
- `hold`: keep the current canonical metadata and leave the proposal unresolved.
- `reject`: keep the current canonical metadata and reject the proposal.

`concept_ownership` and typed logical relations are not inferred or added by this workbench.

## 5. Local autosave vs file export

In-progress review state is automatically kept in browser `localStorage` so a page reload does not discard ordinary review work.

No review file is created automatically.

A file is produced only when the user explicitly chooses **レビュー結果を書き出す / Export review**.

The exported transaction uses schema 0.2 and binds itself to:

```text
candidate ledger SHA-256
canonical manifest SHA-256
graph SHA-256
registered revision-seed SHA-256
```

This protects against applying a decision to a materially different source set.

## 6. Export and resume

Use **レビュー結果を書き出す** in Developer Navigator to create:

```text
docs_registration_review.json
```

Use **レビュー結果を読み込む** to resume from an explicitly exported transaction. Source-hash mismatch is refused rather than silently merged.

## 7. Validate

```powershell
python scripts/validate_registration_review.py "$HOME\Downloads\docs_registration_review.json"
```

## 8. Dry-run manifest application

```powershell
python scripts/apply_registration_review.py "$HOME\Downloads\docs_registration_review.json"
```

Default mode writes nothing. The proposed manifest is compiled through the current index and graph builders before the dry-run is accepted.

To produce a separate reviewed manifest:

```powershell
python scripts/apply_registration_review.py `
  "$HOME\Downloads\docs_registration_review.json" `
  --output tools/docs_manifest.reviewed.yml
```

Only after inspection should canonical application be considered:

```powershell
python scripts/apply_registration_review.py `
  "$HOME\Downloads\docs_registration_review.json" `
  --apply
```

After an actual manifest change, rebuild and validate all downstream read models, including the Public catalog.

## 9. Generated Developer inputs

```text
tools/docs_registration_candidates.yml
  -> scripts/build_registration_candidates_preview.py
  -> tools/docs_registration_candidates.preview.json

tools/docs_registered_reader_question_review.yml
  -> scripts/build_registered_reader_question_review_preview.py
  -> tools/docs_registered_reader_question_review.preview.json
```

Both JSON files are generated read models and must not be edited by hand.

## 10. Manual and ad-hoc revision candidates

The Developer Navigator may also export manually created candidates and ad-hoc revision requests. Each carries an explicit approve/hold/reject state.

Only approved items are eligible for repository-side application. A revision request never unregisters an existing public document merely because review has begun.

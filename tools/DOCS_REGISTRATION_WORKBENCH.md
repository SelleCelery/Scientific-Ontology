# Developer Registration Workbench

> Status: Repository maintenance tooling
> Track: Document Navigation Infrastructure
> Stage: DN-5.4B

The Developer Navigator turns candidate review into an explicit transaction instead of requiring direct YAML editing.

## Review flow

```text
candidate preview
  -> approve / approve with edits / hold / reject
  -> browser local review state
  -> export docs_registration_review.json
  -> validate_registration_review.py
  -> apply_registration_review.py --dry-run
  -> reviewed manifest copy or explicit --apply
  -> rebuild index / graph
  -> Public Navigator
```

The browser does not write `docs_manifest.yml` directly. Review state is kept in local browser storage and can be exported/imported.

## Review decisions

- `approve`: accept the candidate metadata as shown.
- `approve_with_edits`: accept after explicit field edits; the export records `before` and `after`.
- `hold`: leave unresolved without changing the manifest.
- `reject`: reject this candidate registration proposal.

`concept_ownership` and typed logical relations are not inferred or added by this workbench.

## Export and resume

Use **レビュー結果を書き出す** in the Developer Navigator. The exported JSON contains candidate/manifest/graph source hashes. Importing or applying a stale review is refused.

To resume work on another browser session, use **レビュー結果を読み込む** and select the exported JSON.

## Validate

```powershell
python scripts/validate_registration_review.py "$HOME\Downloads\docs_registration_review.json"
```

## Dry-run manifest application

```powershell
python scripts/apply_registration_review.py "$HOME\Downloads\docs_registration_review.json"
```

No file is written in the default mode. The proposed manifest is also compiled through the current index and graph builders before the dry-run is accepted.

To produce a separate reviewed manifest first:

```powershell
python scripts/apply_registration_review.py `
  "$HOME\Downloads\docs_registration_review.json" `
  --output tools/docs_manifest.reviewed.yml
```

Only after inspecting that output should canonical application be considered:

```powershell
python scripts/apply_registration_review.py `
  "$HOME\Downloads\docs_registration_review.json" `
  --apply
```

After an actual manifest change, rebuild the public read models and rerun checks.

## Manual and revision candidates

The Developer Navigator may export manually created candidates and revision requests. Each carries an explicit approve/hold/reject state. Only approved manual/revision items are eligible for repository-side application. A revision request does not unregister an existing public document while review is pending.

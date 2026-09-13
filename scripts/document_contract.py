#!/usr/bin/env python3
"""Role-aware manifest contract. No document content is rewritten or re-scored.

The current metadata ledger owns identity, placement and language relation.
Historical labels and frozen assessment runs are not approved assessments.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path, PurePosixPath
from typing import Any, Mapping

import yaml
from jsonschema import Draft202012Validator

CONTRACT_VERSION = 'document-contract/1.0'
ROLES = ('theory_model', 'research_note', 'application_protocol', 'methodological_governance',
         'navigation', 'reference_index', 'operational_specification', 'historical_record',
         'creative_reading')
ASSET_ROLES = ('fixed_research_source', 'provenance_asset', 'historical_support', 'internal_support')
CLAIM_ROLES = set(ROLES) - {'navigation', 'reference_index', 'operational_specification', 'historical_record'}
FORBIDDEN_PARTS = {'.git', '.github', '.venv', 'node_modules', '__pycache__', '_build'}
ID_PATTERN = r'^[a-z0-9]+(?:_[a-z0-9]+)*$'
SHA_PATTERN = r'^[0-9a-f]{64}$'


def load_manifest(root: Path) -> dict[str, Any]:
    data = yaml.safe_load((root / 'tools/docs_manifest.yml').read_text(encoding='utf-8'))
    if not isinstance(data, dict):
        raise ValueError('Manifest must be a mapping')
    return data


def enabled(manifest: Mapping[str, Any]) -> bool:
    return manifest.get('manifest', {}).get('metadata_contract') == CONTRACT_VERSION


def catalog_entry(entry: Mapping[str, Any]) -> bool:
    return entry.get('catalog_document', True) is True and entry.get('state') in {'public', 'public-candidate'}


def asset_paths(manifest: Mapping[str, Any]) -> set[str]:
    return {str(x['path']) for x in manifest.get('managed_assets', [])}


def retired_paths(manifest: Mapping[str, Any]) -> set[str]:
    return {str(x['path']) for x in manifest.get('retired_documents', [])}


def resolve_repo_path(root: Path, value: str) -> Path:
    if not isinstance(value, str) or not value or '\\' in value or ':' in value:
        raise ValueError(f'Unsafe repository path: {value!r}')
    parts = PurePosixPath(value)
    if parts.is_absolute() or '..' in parts.parts or any(p in FORBIDDEN_PARTS for p in parts.parts):
        raise ValueError(f'Unsafe repository path: {value!r}')
    resolved = (root / value).resolve()
    if not resolved.is_relative_to(root.resolve()):
        raise ValueError(f'Path escapes repository: {value!r}')
    return resolved


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def record_map(manifest: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    return {str(e['path']): e for e in [*manifest.get('documents', []), *manifest.get('managed_assets', [])]}


def public_assessment(entry: Mapping[str, Any]) -> dict[str, Any]:
    """Allowlist projection. Never leak a candidate score, hash, note, or raw run."""
    a = entry.get('assessment') or {}
    state = a.get('review_state', 'unreviewed')
    out: dict[str, Any] = {'status': state, 'applicability': a.get('applicability', 'not_applicable')}
    if state == 'approved':
        rep = a.get('representative') or {}
        out['representative'] = {k: rep[k] for k in ('strength', 'exposure') if k in rep}
        out['protocol'] = {k: a.get('protocol', {}).get(k) for k in ('id', 'revision')}
        out['hotspots'] = [
            {k: h[k] for k in ('label', 'locator', 'strength', 'exposure') if k in h}
            for h in a.get('hotspots', [])
        ]
        out['nonclaim_boundaries'] = list(a.get('nonclaim_boundaries', []))
    # Only purpose-written, public-safe unresolved descriptions; no review notes.
    out['unresolved'] = list(a.get('unresolved', []))
    return out


def schema_errors(root: Path, manifest: Mapping[str, Any]) -> list[str]:
    schema = json.loads((root / 'tools/docs_manifest.schema.json').read_text(encoding='utf-8'))
    return [f"{'.'.join(map(str, e.absolute_path))}: {e.message}" for e in
            sorted(Draft202012Validator(schema).iter_errors(manifest), key=lambda e: str(e.absolute_path))]


def _checksum_manifest_entries(path: Path) -> tuple[list[tuple[str, str]], int, list[str]]:
    entries: list[tuple[str, str]] = []
    invalid = 0
    duplicates: list[str] = []
    seen: set[str] = set()
    for line in path.read_text(encoding='utf-8-sig').splitlines():
        if not line.strip() or line.lstrip().startswith('#'):
            continue
        match = re.match(r'^([0-9a-fA-F]{64})\s+\*?(.+?)\s*$', line)
        if not match:
            invalid += 1
            continue
        rel = match[2]
        if rel in seen:
            invalid += 1
            duplicates.append(rel)
            continue
        seen.add(rel)
        entries.append((match[1].lower(), rel))
    return entries, invalid, duplicates


def historical_manifest_status(root: Path, spec: Mapping[str, Any]) -> dict[str, Any]:
    base = resolve_repo_path(root, str(spec['root']))
    path = resolve_repo_path(root, str(spec['path']))
    entries, invalid, duplicates = _checksum_manifest_entries(path)
    result: dict[str, Any] = {
        'id': spec['id'], 'matched': 0, 'mismatched': 0, 'missing': 0, 'invalid': invalid,
        'paths': [], 'matched_paths': [], 'mismatched_paths': [], 'missing_paths': [],
        'duplicates': duplicates,
    }
    for expected, rel in entries:
        target = (base / rel).resolve()
        if not target.is_relative_to(base.resolve()):
            result['invalid'] += 1
            continue
        result['paths'].append(rel)
        if not target.is_file():
            result['missing'] += 1
            result['missing_paths'].append(rel)
        elif sha256(target) == expected:
            result['matched'] += 1
            result['matched_paths'].append(rel)
        else:
            result['mismatched'] += 1
            result['mismatched_paths'].append(rel)
    return result


def historical_attestation_errors(
    root: Path,
    spec: Mapping[str, Any],
    status: Mapping[str, Any],
    *,
    records: Mapping[str, Mapping[str, Any]] | None = None,
) -> list[str]:
    """Validate an explicit present-day acceptance of known historical divergence.

    The historical checksum manifest remains immutable. The attested current snapshot
    binds the exact bytes reviewed at attestation time, so later drift reopens review
    even when historical matched/mismatched counts happen to stay unchanged.
    """
    errors: list[str] = []
    att = spec.get('attestation')
    if not isinstance(att, Mapping):
        return [f"Historical attestation is missing for {spec.get('id', '<unknown>')}"]
    if att.get('status') != 'accepted_as_historical_method_record':
        errors.append(f"Historical attestation status is not accepted_as_historical_method_record: {spec['id']}")
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', str(att.get('attested_at', ''))):
        errors.append(f"Historical attestation date is invalid: {spec['id']}")
    if not str(att.get('acceptance_scope', '')).strip():
        errors.append(f"Historical attestation acceptance_scope is missing: {spec['id']}")
    if spec.get('release_review_required') is not False:
        errors.append(f"Attested provenance set must set release_review_required: false: {spec['id']}")

    expected = att.get('expected_historical_relation')
    if not isinstance(expected, Mapping):
        errors.append(f"Historical attestation expected relation is missing: {spec['id']}")
    else:
        for key in ('matched', 'mismatched', 'missing', 'invalid'):
            value = expected.get(key)
            if not isinstance(value, int) or value < 0:
                errors.append(f"Historical attestation expected relation has invalid {key}: {spec['id']}")
            elif value != status.get(key):
                errors.append(
                    f"Historical attestation relation drift for {spec['id']}: {key} expected={value} actual={status.get(key)}"
                )

    classes = att.get('mismatch_classification')
    if not isinstance(classes, Mapping):
        errors.append(f"Historical attestation mismatch classification is missing: {spec['id']}")
    else:
        formatting = classes.get('formatting_level')
        wrapper = classes.get('later_wrapper_or_provenance_evolution')
        if not isinstance(formatting, int) or formatting < 0 or not isinstance(wrapper, int) or wrapper < 0:
            errors.append(f"Historical attestation mismatch classification counts are invalid: {spec['id']}")
        elif formatting + wrapper != status.get('mismatched'):
            errors.append(
                f"Historical attestation mismatch classification total differs from actual mismatches: {spec['id']}"
            )

    attestation_path_value = str(att.get('attestation_path', ''))
    snapshot_path_value = str(att.get('current_snapshot_path', ''))
    try:
        attestation_path = resolve_repo_path(root, attestation_path_value)
        snapshot_path = resolve_repo_path(root, snapshot_path_value)
    except ValueError as exc:
        errors.append(str(exc))
        return errors
    if not attestation_path.is_file():
        errors.append(f"Historical attestation record is missing: {attestation_path_value}")
    if not snapshot_path.is_file():
        errors.append(f"Historical attested-current snapshot is missing: {snapshot_path_value}")
        return errors

    if records is not None:
        att_entry = records.get(attestation_path_value)
        snap_entry = records.get(snapshot_path_value)
        if not att_entry or att_entry.get('document_role') != 'historical_support':
            errors.append(f"Historical attestation record is not registered as historical_support: {attestation_path_value}")
        if not snap_entry or snap_entry.get('document_role') != 'provenance_asset':
            errors.append(f"Historical current snapshot is not registered as provenance_asset: {snapshot_path_value}")

    base = resolve_repo_path(root, str(spec['root']))
    snapshot_entries, snapshot_invalid, snapshot_duplicates = _checksum_manifest_entries(snapshot_path)
    if snapshot_invalid:
        errors.append(
            f"Historical attested-current snapshot has invalid or duplicate entries: {snapshot_path_value} invalid={snapshot_invalid}"
        )
    if snapshot_duplicates:
        errors.append(f"Historical attested-current snapshot duplicates paths: {', '.join(snapshot_duplicates)}")

    historical_paths = set(status.get('paths', []))
    snapshot_paths = {rel for _, rel in snapshot_entries}
    if snapshot_paths != historical_paths:
        missing_from_snapshot = sorted(historical_paths - snapshot_paths)
        extra_in_snapshot = sorted(snapshot_paths - historical_paths)
        errors.append(
            f"Historical attested-current snapshot path set differs from historical manifest: {spec['id']} "
            f"missing={missing_from_snapshot} extra={extra_in_snapshot}"
        )

    drifted: list[str] = []
    unsafe: list[str] = []
    missing_current: list[str] = []
    for expected_digest, rel in snapshot_entries:
        target = (base / rel).resolve()
        if not target.is_relative_to(base.resolve()):
            unsafe.append(rel)
            continue
        if not target.is_file():
            missing_current.append(rel)
        elif sha256(target) != expected_digest:
            drifted.append(rel)
    if unsafe:
        errors.append(f"Historical attested-current snapshot contains unsafe paths: {unsafe}")
    if missing_current:
        errors.append(f"Historical attested-current snapshot paths are now missing: {missing_current}")
    if drifted:
        errors.append(f"Historical attested-current snapshot drift detected: {drifted}")
    return errors



def asset_bytes_match(entry: Mapping[str, Any], data: bytes) -> bool:
    integrity = entry.get('integrity') or {}
    digest = hashlib.sha256(data).hexdigest()
    if digest == integrity.get('sha256'):
        return True
    # Two observed rc004 CSV working copies differ from their existing Git blobs
    # only by CRLF. Keep both observed digests; never normalize historical hashes.
    return (entry.get('document_role') == 'provenance_asset'
            and integrity.get('basis') == 'rc004_snapshot_not_historical_certification'
            and integrity.get('git_lf_basis') == 'rc004_HEAD_blob_CRLF_only_difference'
            and b'\r' not in data
            and digest == integrity.get('git_lf_sha256'))

def validate_manifest(root: Path, manifest: Mapping[str, Any], *, coverage: bool = True) -> tuple[list[str], list[str]]:
    errors = schema_errors(root, manifest)
    warnings: list[str] = []
    if errors: return errors, warnings
    docs = manifest.get('documents', [])
    assets = manifest.get('managed_assets', [])
    entries = [*docs, *assets]
    paths: set[str] = set(); ids: set[str] = set()
    bypath: dict[str, Any] = {}
    retired = retired_paths(manifest)
    for e in entries:
        path, ident = str(e['path']), str(e.get('doc_id') or e.get('asset_id'))
        if path in paths: errors.append(f'Duplicate current path: {path}')
        if ident in ids: errors.append(f'Duplicate identity: {ident}')
        paths.add(path);ids.add(ident);bypath[path]=e
        if path in retired: errors.append(f'Retired path remains current: {path}')
        try: target = resolve_repo_path(root, path)
        except ValueError as exc: errors.append(str(exc));continue
        if not target.is_file(): errors.append(f'Current entry does not exist: {path}');continue
        if path.endswith('.md'):
            try: target.read_bytes().decode('utf-8',errors='strict')
            except UnicodeError: errors.append(f'Invalid UTF-8: {path}')
        integrity = e.get('integrity') or {}
        if integrity.get('sha256') and not asset_bytes_match(e, target.read_bytes()):
            errors.append(f'Fixed asset differs from bound snapshot: {path}')
    for e in docs:
        path=e['path'];lr=e['language_relation'];a=e['assessment']
        if path.startswith(('tools/', '99_Private_Core_Not_Included/')):
            errors.append(f'Internal/support path cannot be a catalog document: {path}')
        if a['applicability']=='current_claim' and e['document_role'] not in CLAIM_ROLES:
            errors.append(f'Nonclaim-bearing role given claim assessment: {path}')
        if a['applicability']!='current_claim' and a.get('representative'):
            errors.append(f'Non-applicable or commensurated document given duplicate score: {path}')
        if a['review_state']!='approved' and any(k in a for k in ('representative','hotspots','nonclaim_boundaries','approval')):
            errors.append(f'Unapproved assessment must not carry canonical scores: {path}')
        if a['review_state']=='approved':
            if not a.get('approval') or not a.get('representative') or not a.get('protocol'):
                errors.append(f'Approved assessment lacks binding: {path}')
            elif a['approval']['document_sha256']!=sha256(root/path):
                errors.append(f'Approved assessment refers to changed document bytes: {path}')
        cp=lr.get('counterpart_path')
        if cp:
            other=bypath.get(cp)
            if other is None or other.get('language_relation',{}).get('counterpart_path')!=path:
                errors.append(f'Non-reciprocal language counterpart: {path} -> {cp}')
        auth=lr.get('authoritative_path')
        if auth and auth not in paths: errors.append(f'Authority target absent from ledger: {path} -> {auth}')
        if lr['role']=='commensuration' and (not auth or auth==path):
            errors.append(f'Commensuration cannot own its Japanese source: {path}')
        if lr['role']=='coauthoritative_root_interface' and path!='README.md':
            errors.append(f'Root coauthority exception cannot spread: {path}')
        primary=e.get('discovery',{}).get('primary_question',{})
        if not isinstance(primary,dict): errors.append(f'Primary question must be language keyed: {path}')
    artifact_ids={a['artifact_id'] for a in manifest.get('external_artifacts',[])}
    relation_types=set(manifest.get('artifact_relation_types',{}))
    for e in [*docs,*manifest.get('external_artifacts',[])]:
        for rel in [*e.get('artifact_relations',[]), *e.get('relationships',[])]:
            if rel['type'] not in relation_types: errors.append(f'Unknown external relation: {rel}')
            if rel['target_artifact'] not in artifact_ids: errors.append(f'Unknown external target: {rel}')
    for spec in manifest.get('provenance_sets',[]):
        try: status=historical_manifest_status(root,spec)
        except (ValueError,OSError) as exc: errors.append(str(exc));continue
        if spec.get('integrity_claim') == 'attested_historical_manifest_with_current_divergence':
            errors.extend(historical_attestation_errors(root,spec,status,records=bypath))
        elif any(status[k] for k in ('mismatched','missing','invalid')):
            warnings.append(f"Historical integrity remains unresolved: {status['id']} matched={status['matched']} mismatched={status['mismatched']} missing={status['missing']} invalid={status['invalid']}. Snapshot binding is not historical certification.")
    if coverage:
        for p in root.rglob('*.md'):
            rel=p.relative_to(root).as_posix();parts=PurePosixPath(rel).parts
            if any(t in FORBIDDEN_PARTS or t.startswith('000') for t in parts): continue
            if rel not in paths and rel not in retired:
                errors.append(f'Markdown has no document/asset contract: {rel}')
    return errors,warnings

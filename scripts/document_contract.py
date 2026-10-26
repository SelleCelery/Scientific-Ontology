#!/usr/bin/env python3
"""Role-aware manifest contract. No document content is rewritten or re-scored.

The current metadata ledger owns identity, placement and language relation.
Historical labels and frozen assessment runs are not approved assessments.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path, PurePosixPath
from typing import Any, Mapping

import yaml
from jsonschema import Draft202012Validator

from historical_attestation import (
    evaluate_policy as evaluate_historical_attestation_policy,
    load_policy as load_historical_attestation_policy,
    observe_historical_attestation,
)

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


def historical_manifest_status(root: Path, spec: Mapping[str, Any]) -> dict[str, Any]:
    """Compatibility projection of the generated historical observation.

    Declared EOL-equivalent representations count as effective matches. The
    returned aggregate is derived at runtime and is not an acceptance contract.
    """
    observation = observe_historical_attestation(root, spec)
    relation = observation.get('historical_relation') or {}
    exact = relation.get('exact_paths', [])
    equivalent = relation.get('equivalent_paths', [])
    divergent = relation.get('divergent_paths', [])
    missing = relation.get('missing_paths', [])
    unsafe = relation.get('unsafe_paths', [])
    invalid = relation.get('parse_issues', [])
    return {
        'id': observation.get('id'),
        'matched': len(exact) + len(equivalent),
        'mismatched': len(divergent),
        'missing': len(missing),
        'invalid': len(unsafe) + len(invalid),
        'paths': [x['path'] for x in relation.get('path_digests', [])],
        'matched_paths': [x['path'] for x in [*exact, *equivalent]],
        'mismatched_paths': [x['path'] for x in divergent],
        'missing_paths': list(missing),
        'equivalent_paths': [x['path'] for x in equivalent],
        'duplicates': [str(x.get('path', '')) for x in invalid if x.get('code') == 'duplicate_checksum_path'],
    }


def historical_attestation_errors(
    root: Path,
    spec: Mapping[str, Any],
    status: Mapping[str, Any] | None = None,
    *,
    records: Mapping[str, Mapping[str, Any]] | None = None,
    policy: Mapping[str, Any] | None = None,
) -> list[str]:
    """Compatibility wrapper returning only policy-blocking findings."""
    observation = observe_historical_attestation(root, spec, records=records)
    effective_policy = policy or load_historical_attestation_policy(root)
    findings = evaluate_historical_attestation_policy(observation, effective_policy, release_gate=True)
    return [f"{f['code']}: {f['message']}" for f in findings if f.get('action') == 'block']


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

def validate_manifest(
    root: Path,
    manifest: Mapping[str, Any],
    *,
    coverage: bool = True,
    release_gate: bool = False,
    historical_policy: Mapping[str, Any] | None = None,
    historical_observations: list[dict[str, Any]] | None = None,
) -> tuple[list[str], list[str]]:
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
    policy = historical_policy or load_historical_attestation_policy(root)
    for spec in manifest.get('provenance_sets',[]):
        try:
            observation = observe_historical_attestation(root, spec, records=bypath)
            findings = evaluate_historical_attestation_policy(
                observation,
                policy,
                release_gate=release_gate,
            )
        except (ValueError, OSError) as exc:
            errors.append(str(exc))
            continue
        if historical_observations is not None:
            historical_observations.append({
                'observation': observation,
                'policy_findings': findings,
            })
        for finding in findings:
            message = f"{finding['code']}: {finding['message']}"
            if finding.get('paths'):
                message += f" paths={finding['paths']}"
            if finding['action'] == 'block':
                errors.append(message)
            elif finding['action'] == 'warn':
                warnings.append(message)
    if coverage:
        for p in root.rglob('*.md'):
            rel=p.relative_to(root).as_posix();parts=PurePosixPath(rel).parts
            if any(t in FORBIDDEN_PARTS or t.startswith('000') for t in parts): continue
            if rel not in paths and rel not in retired:
                errors.append(f'Markdown has no document/asset contract: {rel}')
    return errors,warnings

#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys
import yaml


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', default='.')
    ap.add_argument('--candidates', default='tools/docs_registration_candidates.yml')
    args = ap.parse_args()
    root = Path(args.root).resolve()
    data = yaml.safe_load((root / args.candidates).read_text(encoding='utf-8'))['registration_candidates']
    manifest = yaml.safe_load((root / 'tools/docs_manifest.yml').read_text(encoding='utf-8'))
    search = yaml.safe_load((root / 'tools/docs_search.yml').read_text(encoding='utf-8'))
    graph = json.loads((root / 'tools/docs_graph.json').read_text(encoding='utf-8'))

    registered = {str(d['path']) for d in manifest.get('documents', []) if d.get('path')}
    observed = {str(n['path']) for n in graph.get('nodes', []) if n.get('type') == 'observed_document'}
    topics = set(search['search']['navigation_topics'])
    candidates = data['candidates']
    errors = []

    paths = [c['path'] for c in candidates]
    ids = [c['proposed']['doc_id'] for c in candidates]
    if len(paths) != len(set(paths)):
        errors.append('duplicate candidate path')
    if len(ids) != len(set(ids)):
        errors.append('duplicate proposed doc_id')
    if set(paths) != observed:
        errors.append(f'candidate/observed mismatch: candidates={len(set(paths))}, observed={len(observed)}')
    overlap = set(paths) & registered
    if overlap:
        errors.append(f'already registered paths included: {sorted(overlap)[:5]}')
    for c in candidates:
        rel = c['path']
        if not (root / rel).is_file():
            errors.append(f'missing source path: {rel}')
        for topic in c['proposed']['discovery'].get('topics', []):
            if topic not in topics:
                errors.append(f'unknown topic {topic}: {rel}')
        if 'concept_ownership' in c['proposed']:
            errors.append(f'candidate must not assign concept_ownership: {rel}')
        if len(c['proposed']['discovery'].get('topics', [])) > 6:
            errors.append(f'too many topics: {rel}')
        for lang in ('ja', 'en'):
            if len(c['proposed']['discovery'].get('aliases', {}).get(lang, [])) > 8:
                errors.append(f'too many aliases {lang}: {rel}')
            if len(c['proposed']['discovery'].get('reader_questions', {}).get(lang, [])) > 5:
                errors.append(f'too many reader questions {lang}: {rel}')

    if len(candidates) != data['source']['observed_unregistered_count']:
        errors.append('summary observed count mismatch')

    if errors:
        print('REGISTRATION CANDIDATE CHECK FAILED')
        for e in errors:
            print('ERROR', e)
        return 1
    print(f'REGISTRATION CANDIDATE CHECK PASS: {len(candidates)} candidates')
    return 0

if __name__ == '__main__':
    sys.exit(main())

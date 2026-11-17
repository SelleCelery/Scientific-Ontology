#!/usr/bin/env python3
"""Conservative, provenance-preserving term-candidate triage; NOT semantic adjudication.

Input: an exact archived term-dictionary draft ZIP. No Repository edits.
The manual 67-item judgment is scoped to one sha256-locked input file.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import re
import unicodedata
import zipfile

BASE = 'tools/assessment/term_dictionary/corpus_wide_draft/'
INPUT_HASHES = {
    'unreviewed_literal_definition_candidates.jsonl': '88ba24ef8ad13df73a73b3e44518ed47f9317b833d9b3f12bb42d4bfedde80be',
    'dictionary_reviewed.jsonl': '93d724f97e90f6b3e98155a8612d81d0d249bcbb1f036ae3feb8d6bbc27dff00',
    'all_japanese_surface_candidates.jsonl': 'f5a2b930c4bff13192aaba054c00768f54e159c308817293d41ad27cd21107a4',
}
# Manual evaluation by an editor of the source literals. Index-dependent and
# intentionally refused for any other input hash. No canonical adoption.
PROVISIONAL = set((1, 2, 4, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 30, 41, 50, 51, 55, 56))
LOCAL_LABEL = set((3, 5, 10, 21, 22, 23, 24, 25, 38, 39, 40, 43, 44, 45, 49, 57, 59, 60, 61, 62, 63))
LIMITATION_ONLY = set((26, 27, 28, 29, 31, 32, 33, 34, 35, 36, 37, 42, 46, 47, 48, 64, 65, 66))
NOT_HEADWORD = set((0, 52, 53, 54, 58))
assert len(PROVISIONAL | LOCAL_LABEL | LIMITATION_ONLY | NOT_HEADWORD) == 67
assert not (PROVISIONAL & LOCAL_LABEL | PROVISIONAL & LIMITATION_ONLY | PROVISIONAL & NOT_HEADWORD | LOCAL_LABEL & LIMITATION_ONLY | LOCAL_LABEL & NOT_HEADWORD | LIMITATION_ONLY & NOT_HEADWORD)

FUNCTION_CUES = {'de', 'to', 'no'}  # Never used to exclude Japanese source terms.


def hash_bytes(blob):
    return hashlib.sha256(blob).hexdigest()


def load_jsonl(blob):
    return [json.loads(s) for s in blob.splitlines() if s.strip()]


def dump_jsonl(path, items):
    with open(path, 'w', encoding='utf-8', newline='\n') as fp:
        for obj in items:
            fp.write(json.dumps(obj, ensure_ascii=False, separators=(',', ':')) + '\n')


def lexical_hint(term, kinds, review_status):
    """Mechanic hint only; does not decide whether a term exists or is meaningful."""
    if review_status.startswith('assistant_editorial_'):
        return 'existing_editorial_draft'
    if review_status == 'literal_source_candidate':
        return 'literal_explanation_candidate'
    if term and all(unicodedata.category(c)[0] in 'NPS' for c in term):
        return 'symbol_or_numeric_candidate'
    if len(term) == 1 and ('\u3040' <= term <= '\u309f'):
        return 'single_hiragana_needs_context'
    if 'definition_headword' in kinds:
        return 'headword_in_source_format'
    if 'quoted_expression' in kinds:
        return 'quoted_expression_needs_context'
    if 'compound_run' in kinds:
        return 'compound_surface_needs_segmentation'
    if 'supplemental_jp' in kinds:
        return 'supplemental_surface_check_scope'
    return 'unclassified_surface_needs_context'


def local_literal_definition(row):
    text = row['senses'][0]['definition'].strip()
    term = row['term']
    for sep in ('\uff1a', ':'):
        pref = term + sep
        if text.startswith(pref):
            return text[len(pref):].strip()
    # The positive statement for the specific AI persona belongs to that model;
    # keep its precise local formulation, not a claim about all AI agents.
    if text.startswith(term + '\u3068\u306f'):
        return text[len(term + '\u3068\u306f'):].lstrip('\u3001 ').strip()
    return text


def write_summary_json(path, summary):
    """Write canonical LF-delimited JSON regardless of host platform."""
    path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n',
                    encoding='utf-8', newline='\n')


def collision_key(term):
    first = re.split(r'\s*/\s*', term, maxsplit=1)[0]
    return re.sub(r'[\s\-\u3000\uff0d\u30fb]', '', first).casefold()


def run(source_zip, out_dir):
    out_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(source_zip) as z:
        for fn, digest in INPUT_HASHES.items():
            raw = z.read(BASE + fn)
            if hash_bytes(raw) != digest:
                raise ValueError('Input mismatch: manual review is invalid for ' + fn)
        surfaces = load_jsonl(z.read(BASE + 'all_japanese_surface_candidates.jsonl'))
        definitions = load_jsonl(z.read(BASE + 'dictionary_reviewed.jsonl'))
        literals = load_jsonl(z.read(BASE + 'unreviewed_literal_definition_candidates.jsonl'))
        coverage = json.loads(z.read(BASE + 'scope_and_coverage.json'))
    if len(literals) != 67 or len(surfaces) != 27901 or len(definitions) != 1365:
        raise ValueError('Source count mismatch')
    terms = {x['term'] for x in definitions}
    if len(terms) != len(definitions):
        raise ValueError('Duplicate term in input draft')
    review_rows, addition_rows = [], []
    actions = Counter()
    for i, row in enumerate(literals):
        if i in PROVISIONAL:
            action = 'scoped_provisional_entry_candidate'
            new_def = local_literal_definition(row)
            if row['term'] in terms:
                raise ValueError('New candidate collides with an existing editorial draft')
            addition_rows.append({
                'term': row['term'],
                'definition_candidate': new_def,
                'scope': 'local_source_usage_only',
                'source_status': 'literal_excerpt_without_document_location',
                'editorial_status': 'assistant_scoped_review_pending_human',
                'canonical': False,
                'document_path_in_public_dictionary': False,
                'literal_review_number': i,
            })
        elif i in LOCAL_LABEL:
            action = 'local_label_or_claim_not_general_term'
        elif i in LIMITATION_ONLY:
            action = 'negative_limit_not_positive_definition'
        else:
            action = 'rhetoric_or_fragment_not_dictionary_headword'
        actions[action] += 1
        review_rows.append({
            'number': i,
            'literal_heading': row['term'],
            'source_literal': row['senses'][0]['definition'],
            'decision': action,
            'source_location': None,
            'source_layer': 'not_reconstructible_from_this_registry',
            'editorial_status': 'assistant_provisional_not_human_accepted',
            'meaning_completeness': 'not_verified_against_full_rc008_source',
        })
    reviewed_status = Counter(x.get('review_status', '') for x in surfaces)
    cohorts = Counter()
    triage_rows = []
    for row in surfaces:
        kinds = row.get('surface_kinds') or []
        category = lexical_hint(row['term'], kinds, row.get('review_status', ''))
        cohorts[category] += 1
        triage_rows.append({
            'term': row['term'],
            'source_review_status': row.get('review_status'),
            'observed_form_kinds': kinds,
            'literal_observations': row.get('literal_observations'),
            'nonsemantic_hint': category,
            'lexical_identity_established': False,
            'sense_identity_established': False,
            'canonical_adoption': False,
        })
    variants = defaultdict(list)
    for row in definitions:
        variants[collision_key(row['term'])].append(row)
    collisions = []
    for key, rows in sorted(variants.items()):
        if len(rows) > 1:
            collisions.append({
                'normalization_key': key,
                'terms': [x['term'] for x in rows],
                'definitions': [x['definition'] for x in rows],
                'relationship': 'candidate_only_not_semantically_adjudicated',
            })
    dump_jsonl(out_dir / 'surface_review_hints.jsonl', triage_rows)
    dump_jsonl(out_dir / 'literal_candidate_review.jsonl', review_rows)
    dump_jsonl(out_dir / 'dictionary_delta_local_labels.jsonl', addition_rows)
    dump_jsonl(out_dir / 'variant_collision_candidates.jsonl', collisions)
    source_blob = Path(source_zip).read_bytes()
    summary = {
        'source_zip_sha256': hash_bytes(source_blob),
        'source_archive_sha256_attested_in_prior_coverage': coverage.get('source_archive_sha256'),
        'source_archive_present_in_this_run': False,
        'total_candidate_surfaces': len(surfaces),
        'existing_editorial_drafts_unchanged': len(definitions),
        'literal_candidates_manually_triaged': len(literals),
        'manual_review_actions': dict(sorted(actions.items())),
        'separate_scoped_definition_candidates': len(addition_rows),
        'mechanical_hint_counts': dict(sorted(cohorts.items())),
        'incoming_status_counts': dict(sorted(reviewed_status.items())),
        'normalization_collision_groups_for_existing_1365': len(collisions),
        'semantic_review_of_27901_completed': False,
        'definitions_verified_against_complete_rc008': False,
        'dictionary_is_canonical': False,
        'repository_applied': False,
        'human_review_done': False,
        'mechanical_hints_are_not_term_segmentation_or_semantic_judgments': True,
        'main_dictionary_contains_source_pointers': False,
    }
    write_summary_json(out_dir / 'coverage_and_limits.json', summary)
    return summary


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--source-zip', required=True, type=Path)
    ap.add_argument('--out', required=True, type=Path)
    args = ap.parse_args()
    print(json.dumps(run(args.source_zip, args.out), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()

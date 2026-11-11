#!/usr/bin/env python3
"""Source-identity and bounded lexical pilot tests; no semantic assertion."""
from __future__ import annotations

import csv
import hashlib
import json
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from probe_sentence_dictionary import parse_sentences
from probe_collation_dependency import (
    ROOT, SYNC, RESIDUAL, SOURCE_REL, EXPECTED_SHA256,
    lexicon_from, mentions, root_match_kind, definitions, dependency_layers,
    run, exact_feature_reference, feature_set, coverage,
)


class CollationDependencyProbe(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.repo = Path(__file__).resolve().parents[1]
        cls.source = cls.repo / SOURCE_REL
        cls.unchanged_sha = hashlib.sha256(cls.source.read_bytes()).hexdigest()
        cls.sentences = parse_sentences(cls.source)
        cls.temp = tempfile.TemporaryDirectory()
        cls.out = Path(cls.temp.name)
        cls.summary = run(cls.source, cls.out)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def table(self, name):
        with (self.out/name).open(encoding='utf-8',newline='') as f:
            return list(csv.DictReader(f))

    def test_exact_source_identity(self):
        self.assertEqual(self.unchanged_sha, EXPECTED_SHA256)
        self.assertEqual(hashlib.sha256(self.source.read_bytes()).hexdigest(), self.unchanged_sha)

    def test_whole_sentence_inventory(self):
        self.assertEqual(len(self.sentences), 346)
        self.assertEqual(self.summary['sentences'], 346)
        self.assertEqual(len(self.table('collation_uses.csv')), 61)

    def test_compound_protected_from_root_identity(self):
        self.assertEqual(self.summary['compound_only_sentences'], 18)
        self.assertEqual(self.summary['direct_root_sentences'], 43)
        self.assertEqual(root_match_kind('re' + ROOT), 'direct')
        self.assertEqual(root_match_kind('\u518d' + ROOT), 'compound_only')
        self.assertEqual(root_match_kind(ROOT + '\u898f\u5247'), 'compound_only')

    def test_dependency_expansion_includes_unmentioned_definition(self):
        rows=self.table('definition_reference_paths.csv')
        self.assertTrue(any(x['source_sentence'].startswith('SAT:7.3:') and
                            x['source_term']==SYNC for x in rows))
        self.assertTrue(any(x['source_sentence'].startswith('SAT:9.5.1:') and
                            x['source_term']==RESIDUAL for x in rows))

    def test_cycle_is_reference_only(self):
        self.assertIn(ROOT+' > '+RESIDUAL+' > '+ROOT,
                      self.summary['definition_cycle_back_to_root'])
        rows=self.table('definition_reference_paths.csv')
        self.assertTrue(all(x['relation'].endswith('not_entailment') for x in rows))

    def test_source_order_does_not_preload_future_definitions(self):
        rows=[x for x in self.table('dependency_update_trace.csv')
              if x['order']=='seed_sync_residual']
        self.assertEqual([x['added_number'] for x in rows], ['8.1','7.3','9.5.1','7.1','7.2'])
        self.assertEqual([int(x['reached_term_count']) for x in rows[:3]], [7,9,13])
        self.assertEqual([int(x['has_reference_cycle_back_to_root']) for x in rows[:3]], [0,0,1])
        self.assertEqual(rows[1]['contains_root'], 'False')

    def test_registration_order_changes_intermediate_reach(self):
        rows=self.table('dependency_update_trace.csv')
        ab=[x for x in rows if x['order']=='seed_sync_residual']
        ba=[x for x in rows if x['order']=='seed_residual_sync']
        self.assertNotEqual(ab[1]['newly_reached_terms'],ba[1]['newly_reached_terms'])
        self.assertEqual(ab[-1]['reachable_terms'],ba[-1]['reachable_terms'])

    def test_uncompressed_raw_examples(self):
        raw=self.table('collation_uses.csv')
        ids={x['sentence_id'] for x in raw if x['root_match']=='direct'}
        histories=self.table('representative_history.csv')
        for order in {x['order'] for x in histories}:
            self.assertEqual({x['added_sentence'] for x in histories if x['order']==order},ids)
            self.assertEqual(len([x for x in histories if x['order']==order]),len(ids))

    def test_exact_surface_reference_is_at_least_each_online_order(self):
        rows=self.table('representative_orders.csv')
        self.assertEqual(len(rows),10)
        max_cov=float(rows[0]['exact_surface_feature_max'])
        self.assertEqual(self.summary['exact_feature_combinations_checked'],962598)
        self.assertTrue(all(float(x['representative_coverage']) <= max_cov+1e-7 for x in rows))
        self.assertGreater(max_cov,0.7)

    def test_different_orders_leave_different_representatives(self):
        rows=self.table('representative_orders.csv')
        signatures={x['representative_sentence_ids'] for x in rows}
        self.assertGreater(len(signatures),1)
        self.assertTrue(all(x['registered_examples']=='43' for x in rows))

    def test_surface_optimum_can_omit_a_necessary_relation_candidate(self):
        canaries={x['number']:x for x in self.table('surface_coverage_canaries.csv')}
        self.assertEqual(canaries['7.4']['exact_feature_representative'],'0')
        self.assertIn('role:cue_necessary',canaries['7.4']['unrepresented_feature_cues'])
        self.assertEqual(canaries['7.4']['semantic_necessity'],'not_audited')

    def test_graphml_xml_and_utf8(self):
        root=ET.parse(self.out/'collation_dependency.graphml').getroot()
        self.assertTrue(root.tag.endswith('graphml'))
        self.assertIn(ROOT,(self.out/'collation_uses.csv').read_text(encoding='utf-8'))

    def test_no_latent_distance_or_entropy_claim(self):
        self.assertTrue(any('No LLM latent training-data distance' in x for x in self.summary['limits']))
        self.assertFalse(any('entropy_bits' in x for x in self.summary))


if __name__ == '__main__':
    unittest.main()

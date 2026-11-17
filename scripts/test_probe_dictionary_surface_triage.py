#!/usr/bin/env python3
import importlib.util
from pathlib import Path
import unittest
import tempfile
import json

SCRIPT = Path(__file__).with_name('probe_dictionary_surface_triage.py')
spec = importlib.util.spec_from_file_location('triage', SCRIPT)
triage = importlib.util.module_from_spec(spec)
spec.loader.exec_module(triage)


class CandidateTriageTests(unittest.TestCase):
    def test_symbol_hints_do_not_claim_semantics(self):
        self.assertEqual(triage.lexical_hint('007', ['surface_run'], 'surface_only_not_semantically_reviewed'), 'symbol_or_numeric_candidate')
        self.assertEqual(triage.lexical_hint('de', ['surface_run'], 'surface_only_not_semantically_reviewed'), 'unclassified_surface_needs_context')
        self.assertEqual(triage.lexical_hint('A', ['definition_headword'], 'literal_source_candidate'), 'literal_explanation_candidate')

    def test_preexisting_draft_takes_precedence(self):
        self.assertEqual(triage.lexical_hint('X', ['quoted_expression'], 'assistant_editorial_previous'), 'existing_editorial_draft')

    def test_all_sixty_seven_are_uniquely_covered(self):
        groups = [triage.PROVISIONAL, triage.LOCAL_LABEL, triage.LIMITATION_ONLY, triage.NOT_HEADWORD]
        self.assertEqual(len(set.union(*groups)), 67)
        self.assertEqual(sum(map(len, groups)), 67)

    def test_literal_normalization_retains_scope(self):
        self.assertEqual(triage.local_literal_definition({'term':'AB','senses':[{'definition':'AB: local'}]}), 'local')
        self.assertEqual(triage.local_literal_definition({'term':'AB','senses':[{'definition':'AB not defined here'}]}), 'AB not defined here')

    def test_summary_json_has_platform_independent_lf(self):
        summary = {'probe': '日本語', 'count': 67}
        with tempfile.TemporaryDirectory() as scratch:
            output = Path(scratch) / 'coverage_and_limits.json'
            triage.write_summary_json(output, summary)
            expected = (json.dumps(summary, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
            self.assertEqual(output.read_bytes(), expected)
            self.assertNotIn(b'\r\n', output.read_bytes())

    def test_normalization_is_candidate_only(self):
        self.assertEqual(triage.collision_key('one / example'), triage.collision_key('one'))
        self.assertNotEqual(triage.collision_key('one'), triage.collision_key('two'))


if __name__ == '__main__':
    unittest.main()

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT=Path(__file__).with_name('build_so_navigator_dictionary_seed.py')
spec=importlib.util.spec_from_file_location('so_nav_dictionary_seed_builder',SCRIPT)
mod=importlib.util.module_from_spec(spec)
sys.modules[spec.name]=mod
spec.loader.exec_module(mod)
BASE=Path('tools/assessment/term_dictionary/corpus_lexicon_classification')
DEST=Path('tools/assessment/term_dictionary/navigator_seed')

class DictionarySeedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base=BASE/'categorized_dictionary_entries.jsonl'
        cls.att=BASE/'source_attestation_sidecar.jsonl'
        cls.extra=DEST/'additions_113.jsonl'
        if not all(p.exists() for p in [cls.base,cls.att,cls.extra]):
            raise AssertionError('Required previously applied dictionary source files missing')
        cls.entries=mod.prepare(cls.base,cls.att,cls.extra)

    def test_1500(self):
        self.assertEqual(len(self.entries),1500)
        self.assertEqual(len({e['term'] for e in self.entries}),1500)
    def test_113_new(self):
        self.assertEqual(sum(e['status']==mod.ADDED_STATUS for e in self.entries),113)
    def test_no_blank_definitions(self):
        self.assertTrue(all(len(e['definition'])>=12 for e in self.entries))
    def test_no_canonical_promotion(self):
        self.assertTrue(all(e['authority']=='unreviewed_editorial' for e in self.entries))
    def test_group(self):
        self.assertEqual(set(e['group'] for e in self.entries),set(mod.CLASS_LABEL))
    def test_source_examples_are_not_evidence_of_definition(self):
        self.assertTrue(all(x['evidence_status']=='surface_context_only_not_sense_verification'
           for e in self.entries for x in e['source_attestations']))
    def test_roundtrip(self):
        self.assertEqual([json.loads(mod.jd(e)) for e in self.entries],self.entries)
    def test_critical_entries(self):
        terms={e['term']:e for e in self.entries}
        for term in ['境界','α監査','量子エンタングルメント','AI','認識ブリッジ']:
            self.assertTrue(terms[term]['definition'])
    def test_technical_proximity_not_equivalence(self):
        by_term={e['term']:e for e in self.entries}
        self.assertTrue(by_term['境界エントロピー']['technical_adjacency'])
        self.assertFalse(by_term['境界エントロピー']['external_definition_verified'])
        self.assertEqual(by_term['境界エントロピー']['borrowed_domain_candidates'],['熱力学','情報理論'])
    def test_build_is_deterministic(self):
        with tempfile.TemporaryDirectory() as a,tempfile.TemporaryDirectory() as b:
            mod.build(self.base,self.att,self.extra,Path(a))
            mod.build(self.base,self.att,self.extra,Path(b))
            for x in mod.OUTPUT_FILES:
                self.assertEqual((Path(a)/x).read_bytes(),(Path(b)/x).read_bytes())
                self.assertTrue((Path(a)/x).read_bytes().endswith(b'\n'))

if __name__=='__main__':unittest.main()

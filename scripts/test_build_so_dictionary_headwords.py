import importlib.util
import json
import pathlib
import unittest

SCRIPT = pathlib.Path(__file__).with_name('build_so_dictionary_headwords.py')
spec=importlib.util.spec_from_file_location('so_headword_builder',SCRIPT)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
RULES=pathlib.Path(__file__).resolve().parent.parent / 'tools/assessment/term_dictionary/corpus_lexicon_classification/taxonomy_rules.json'
CONFIG=json.loads(RULES.read_text(encoding='utf-8'))

def row(term,kinds=None):
    return {'term':term,'surface_kinds':kinds or ['surface_run'],'review_status':'surface_only_not_semantically_reviewed','literal_observations':1}

class DictionaryHeadwordTests(unittest.TestCase):
    def test_common_grammar_separate_from_dictionary(self):
        r=m.classify('は',row('は',['function_expression']),{'は':{'definition':'example'}},CONFIG)
        self.assertEqual((r['group'],r['candidate_status']),(None,'grammar_not_dictionary'))

    def test_so_special_and_technical_adjacent_are_distinct(self):
        so=m.classify('エントロピー属性',row('エントロピー属性'),{'エントロピー属性':{}},CONFIG)
        imported=m.classify('エントロピー',row('エントロピー'),{'エントロピー':{}},CONFIG)
        self.assertEqual(so['group'],'so');self.assertTrue(so['technical_adjacency'])
        self.assertEqual(imported['group'],'technical');self.assertTrue(imported['technical_adjacency'])

    def test_operational_redefinition_is_not_forced_to_general(self):
        r=m.classify('境界',row('境界'),{'境界':{}},CONFIG)
        self.assertEqual(r['group'],'so')
        self.assertIn('ordinary_or_imported_word_used_operationally_in_so',r['flags'])
        r=m.classify('接触',row('接触'),{'接触':{}},CONFIG)
        self.assertEqual(r['group'],'so')

    def test_imported_technical_terms_are_review_alarms(self):
        for term in ('不完全性定理','量子力学','ファインマン図','ソリトン','クオリア'):
            r=m.classify(term,row(term),{},CONFIG)
            self.assertEqual(r['group'],'technical',term)
            self.assertTrue(r['technical_adjacency'],term)

    def test_no_unreviewed_kana_fragment_promotion(self):
        for term in ('ける','ている','じか'):
            r=m.classify(term,row(term),{},CONFIG)
            self.assertIsNone(r['group'])
            self.assertNotIn(r['candidate_status'],('headword_candidate','headword_seed'))

    def test_character_context_keeps_incomplete_embedding_visible(self):
        self.assertTrue(m.likely_embedded_in_compound('ゲーデルの不完全性定理を',len('ゲーデルの不完全性定理')-1,'完全性定理'))
        self.assertFalse(m.likely_embedded_in_compound('完全性定理とは',len('完全性定理')-1,'完全性定理'))

    def test_no_source_pointers_in_definitions(self):
        # Procedure-level contract: serialized dictionary entries contain definitions
        # and classification only; source_path lives in an independent sidecar.
        self.assertEqual(m.OUTS.count('source_attestation_sidecar.jsonl'),1)
        self.assertNotIn('source_path',m.dump_json({'definition':'境界の用法','group':'so'}))

    def test_ahocorasick_substring_match_is_not_term_judgment(self):
        aho=m.AhoMatcher(['境界','量子','定理'])
        found={['境界','量子','定理'][i] for _,i in aho.iter_hits('量子理論の境界を検査する定理')}
        self.assertEqual(found,{'量子','境界','定理'})

    def test_rule_model_is_separate_from_human_approval(self):
        s=m.classify('量子場理論',row('量子場理論'),{},CONFIG)
        self.assertEqual(s['semantic_verification'],'not_human_confirmed')
        self.assertNotEqual(s['confidence'],'human_approved')

if __name__=='__main__':unittest.main()

#!/usr/bin/env python3
"""Tests for lexical-only epistemic dictionary pilot; no theoretical validity claims."""
import importlib.util
import hashlib
import itertools
from pathlib import Path
import tempfile
import unittest
from xml.etree import ElementTree as ET

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location('dictionary_probe', HERE/'probe_epistemic_dictionary.py')
probe = importlib.util.module_from_spec(SPEC)
import sys
sys.modules[SPEC.name] = probe
SPEC.loader.exec_module(probe)
SOURCE = Path('01_Sat_Truth/Boundary_Epistemological_Critique.ja.md')
SOURCE_SHA256='2f902285215ffac36f850cc118034787244f1c882f9274549da468960059d534'


class DictionaryExperiment(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.props = probe.extract_props(SOURCE)
        cls.defs, cls.words = probe.lexicon_from(cls.props)
        cls.base = probe.dictionary_edges(cls.props, cls.words)

    def test_source_identity(self):
        self.assertEqual(hashlib.sha256(SOURCE.read_bytes()).hexdigest(), SOURCE_SHA256)
        self.assertEqual(len(self.props), 265)
        self.assertEqual(len(self.defs), 38)
        self.assertEqual(sum(len(v) for v in self.defs.values()), 51)

    def test_dictionary_and_open_vocabulary(self):
        self.assertIn('境界', self.words)
        self.assertNotIn('境界', self.defs)  # Uses '境界は', not captured by 'とは' parser.
        self.assertIn('照合', self.defs)
        self.assertEqual(len(self.words), 59)
        self.assertEqual(len(self.base),111)

    def test_reference_is_not_entailment(self):
        self.assertIn(('未解決','偽'), self.base)
        self.assertIn('偽ではない',self.props['10.7'].body)
        self.assertIn(('照合','残差'),self.base)
        self.assertIn(('残差','照合'),self.base)

    def test_cycle_detected(self):
        groups=probe.scc(probe.adjacency(self.words,self.base))
        self.assertIn(tuple(sorted(('偽','偽閉鎖','未解決','残差','照合'))),groups)

    def test_single_lexical_replacement_changes_references(self):
        orig=self.props['12.9'].body
        mutated=probe.mutated_props(self.props, (0,0,0,0,1,0))
        self.assertEqual(self.props['12.9'].body, orig)
        self.assertIn('学問',mutated['12.9'].body)
        delta=probe.dictionary_edges(mutated,self.words)
        self.assertIn(('通約','学問'),delta)
        self.assertNotIn(('通約','学問'),self.base)

    def test_six_qualifiers_not_represented_by_lexical_edges(self):
        for i,(num,qualifier,_) in enumerate(probe.QUALIFIER_EXPERIMENTS):
            new=probe.mutated_props(self.props,qualifier_mask=1<<i)
            self.assertNotEqual(new[num].body,self.props[num].body)
            self.assertEqual(set(probe.dictionary_edges(new,self.words)),set(self.base))

    def test_factorized_joint_changes_have_same_references(self):
        # Check dispersed combinations, including all-on, not just 6 isolated switches.
        lcs=[(0,0,0,0,0,0),(1,2,0,1,2,0),(2,0,2,2,1,1),(2,2,2,2,2,2)]
        for lc in lcs:
            without=probe.dictionary_edges(probe.mutated_props(self.props,lc),self.words)
            for mask in (0,1,2,3,7,15,32,63):
                with_mods=probe.dictionary_edges(probe.mutated_props(self.props,lc,mask),self.words)
                self.assertEqual(with_mods,without)

    def test_symbol_rename_isomorphic_control(self):
        result=probe.alpha_rename_control(self.props,self.words,self.base)
        self.assertTrue(result['対応する全語を一括改名したあと元のラベルへ戻すと定義参照が一致'])
        self.assertGreater(result['変更した語の出現数'],10)

    def test_unit_capacity_edge_disjoint(self):
        g={'a':{'b','c'}, 'b':{'d'}, 'c':{'d'}, 'd':set()}
        self.assertEqual(probe.edge_disjoint_count(g,'a','d'),2)
        self.assertEqual(probe.shortest(g,'a','d'),['a','b','d'])

    def test_outputs_parseable(self):
        with tempfile.TemporaryDirectory() as folder:
            result=probe.run(SOURCE,Path(folder),full=False)
            self.assertEqual(result['numbers'],265)
            self.assertEqual(result['lexical_cases'],1)
            self.assertEqual(result['all_factorial_cases'],64)
            ET.parse(Path(folder)/'辞書・使用グラフ.graphml')
            self.assertIn('辞書', (Path(folder)/'境界認識批判_語の使用と変更の辞書ビューア.html').read_text(encoding="utf-8"))

if __name__=='__main__': unittest.main()

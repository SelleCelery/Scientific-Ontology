#!/usr/bin/env python3
"""Regression tests for the provisional Euclid beta entropy model."""
import csv
import importlib.util
import os
import tempfile
import unittest
from pathlib import Path

SCRIPT=Path(__file__).resolve().with_name('euclid_beta_entropy_widecount.py')
spec=importlib.util.spec_from_file_location('euclid_beta_entropy_widecount',SCRIPT)
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
PROJECT_ROOT=SCRIPT.parent.parent
DEFAULT_SOURCE=PROJECT_ROOT/'euclid-elements-13books.json'
if not DEFAULT_SOURCE.exists():DEFAULT_SOURCE=Path('/mnt/data/euclid-elements-13books.json')
ROOT=Path(os.environ.get('EUCLID_SOURCE',str(DEFAULT_SOURCE)))
RECON=Path(os.environ.get('EUCLID_RECON',str(PROJECT_ROOT/'tools/euclid_13_beta_audit/euclid_definition_id_reconciliation.csv')))
ALPHA=Path(os.environ.get('EUCLID_ALPHA',str(PROJECT_ROOT/'tools/euclid_13_beta_audit/euclid_465_alpha_exergy_recorded_scope.csv')))

class BetaEntropyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sha,cls.props,cls.defs,cls.aux=mod.load_source(ROOT)
        cls.cross=mod.load_reconciliation(RECON)
        cls.nodes0,cls.edges0,_=mod.build(cls.props,cls.defs,cls.aux,cls.cross,False)
        cls.nodes,cls.edges,cls.aliases=mod.build(cls.props,cls.defs,cls.aux,cls.cross,True)
        cls.values,cls.parents,_=mod.path_counts(cls.nodes,cls.edges)
        cls.base,_,_=mod.path_counts(cls.nodes0,cls.edges0)

    def test_sha_and_corpus_size(self):
        self.assertEqual(self.sha,mod.EXPECTED_SHA)
        self.assertEqual((len(self.props),len(self.defs),len(self.aux)),(465,132,10))

    def test_p1_two_seeds(self):
        self.assertEqual(self.values['P1'],2)
        self.assertEqual(self.parents['P1'],{'I.Definition1','I.Definition4'})

    def test_all_theorem_values_integer_and_at_least_one(self):
        self.assertEqual(len([x for x in self.values if x in self.props]),465)
        self.assertTrue(all(isinstance(self.values[x],int) and self.values[x]>=1 for x in self.props))

    def test_wide_is_no_less_than_references(self):
        self.assertTrue(all(self.values[x]>=self.base[x] for x in self.props))

    def test_definition_id_16_and_viii_4(self):
        self.assertEqual(len(self.cross),16)
        self.assertIn('VII.Definition20',self.parents['VIII.4'])
        self.assertNotIn('VIII.Definition20',self.nodes)

    def test_book_x_group_with_distinct_concepts_recorded(self):
        self.assertIn('X.Definitions_I',self.parents['X.19'])
        self.assertIn('X.Definition1.4',self.edges[('X.Definitions_I','X.19')]['concepts'])
        self.assertEqual(mod.definition_unit('X.Definition1.1'),mod.definition_unit('X.Definition1.4'))

    def test_i1_equilateral_triangles_direct_concept(self):
        self.assertIn('I.Definition20',self.parents['I.1'])
        self.assertIn('concept_lexical_wide',self.edges[('I.Definition20','I.1')]['provenance'])

    def test_i6_later_edition_and_uncertainty_provenance(self):
        for src in ('I.3','I.4','P1','CN5'):
            self.assertIn(src,self.parents['I.6'])
        self.assertIn('later_edition_Lardner1855',self.edges[('I.3','I.6')]['provenance'])
        self.assertIn('later_editor_Joyce',self.edges[('P1','I.6')]['provenance'])

    def test_x_definition_group_ii_proof_annotation(self):
        self.assertIn('X.Definition2.1',self.parents['X.54'])
        self.assertIn('proof_bracket_definition',self.edges[('X.Definition2.1','X.54')]['provenance'])

    def test_same_direct_edge_deduplicated(self):
        matches=[k for k in self.edges if k==('I.Definition1','P1')]
        self.assertEqual(len(matches),1)

    def test_reference_alpha_exergy_19220(self):
        alpha=mod.read_alpha_exergy(ALPHA)
        self.assertEqual(mod.check_alpha_graph(self.props,self.edges0,alpha),19220)

    def test_path_recurrence_and_converging_branches(self):
        n={'root','branch_a','branch_b','goal'}
        e={('root','branch_a'):None,('root','branch_b'):None,
           ('branch_a','goal'):None,('branch_b','goal'):None}
        v,_,_=mod.path_counts(n,e)
        self.assertEqual((v['root'],v['branch_a'],v['branch_b'],v['goal']),(1,1,1,2))

    def test_detect_cycle(self):
        with self.assertRaisesRegex(ValueError,'CYCLE'):
            mod.path_counts({'a','b'},{('a','b'):None,('b','a'):None})

    def test_context_sensitive_square_number(self):
        selection=mod.select_lexical_concepts('An even square number is a square number.',7,self.aliases)
        self.assertIn('VII.Definition18',selection)
        self.assertNotIn('I.Definition22',selection)

    def test_batch_outputs(self):
        with tempfile.TemporaryDirectory() as td:
            m=mod.run(ROOT,RECON,ALPHA,Path(td))
            self.assertEqual(m['scope']['theorems'],465)
            r=list(csv.DictReader((Path(td)/'euclid_465_alpha_beta_entropy_exergy.csv').open(encoding='utf-8-sig')))
            self.assertEqual(len(r),465)
            self.assertEqual(int(r[0]['beta_entropy_wide_admitted_concepts']),self.values['I.1'])

if __name__=='__main__':unittest.main(verbosity=2)

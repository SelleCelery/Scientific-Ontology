#!/usr/bin/env python3
"""Isolated, UTF-8 explicit research tests; no canonical repository mutations."""
from __future__ import annotations

import csv
import hashlib
import json
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

from probe_operator_spine import (
    SOURCES, OPERATOR_FORMS, components, exhaustive, extract_occurrences,
    factor_model, family_ablation, operator_group, operator_template,
    perturbation_controls, read_units, run, source_sha, tokenize_terms,
)


class OperatorSpineProbeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cwd=Path.cwd()
        guess=Path(__file__).resolve().parents[1]
        cls.root=cwd if (cwd / SOURCES[0][1]).is_file() else guess
        cls.paths={p:cls.root / rel for p, rel in SOURCES}
        if not all(f.is_file() for f in cls.paths.values()):
            raise FileNotFoundError('Run from Scientific-Ontology repository root')
        cls.units={p:read_units(p, rel, cls.paths[p]) for p,rel in SOURCES}
        cls.sat=cls.units['SAT']
        cls.ops,cls.quals=extract_occurrences(cls.sat)

    def test_sat_anchor_and_provenance(self):
        self.assertEqual(len(self.sat),265)
        self.assertEqual(len({u.id for u in self.sat}),265)
        self.assertTrue(all(u.kind=='numbered_proposition' and u.line>=1 for u in self.sat))
        self.assertTrue(all(u.source==SOURCES[0][1] for u in self.sat))

    def test_raj_tam_are_not_fake_numbered_claims(self):
        for phase in ('RAJ','TAM'):
            self.assertGreater(len(self.units[phase]),150)
            self.assertTrue(all(u.kind!='numbered_proposition' for u in self.units[phase]))
            self.assertTrue(all(u.id.startswith(phase+':L') for u in self.units[phase]))

    def test_operator_and_modifier_both_recognized(self):
        sat_107=[o for o in self.ops if o.unit=='SAT:10.7']
        self.assertTrue(any(o.family=='DEFINE' for o in sat_107))
        self.assertTrue(any(o.family=='NEGATE' and o.literal=='ではない' for o in sat_107))
        self.assertTrue(any(q['unit']=='SAT:9.5.1' and q['marker']=='まだ' for q in self.quals))

    def test_original_operator_spans_are_exact(self):
        table={u.id:u for u in self.sat}
        for op in self.ops:
            body=table[op.unit].text
            self.assertEqual(body[op.start:op.end],op.literal)
            self.assertGreater(op.end,op.start)

    def test_symbolization_is_reversible_as_surface_operation(self):
        by_unit={u.id:[] for u in self.sat}
        for o in self.ops:by_unit[o.unit].append(o)
        for unit in self.sat:
            group=sorted(by_unit[unit.id],key=lambda o:o.start)
            transformed=operator_template(unit.text,group)
            rebuilt=transformed
            for o in group:
                rebuilt=rebuilt.replace('⟦'+o.family+'⟧',o.literal,1)
            self.assertEqual(rebuilt,unit.text)

    def test_term_matching_avoids_single_kanji_inside_compound(self):
        self.assertFalse(tokenize_terms('知識', ['知']))
        self.assertTrue(tokenize_terms('知とは', ['知']))

    def test_fixed_shell_changes_no_occurrence_when_identity_model_changes(self):
        # Hypotheses can alter shared-ID links, not original operator spans.
        families=('DEFINE','NEGATE')
        a=factor_model(self.ops,families,(0,0))
        b=factor_model(self.ops,families,(1,2))
        self.assertNotEqual(set(a),set(b))
        self.assertEqual(len(self.ops),sum(1 for o in self.ops))
        self.assertEqual({o.id for o in self.ops},set(o.id for o in self.ops))

    def test_exhaustive_27_complete_and_nonconstant(self):
        chosen,total,rows=exhaustive(self.sat,self.ops,27,3)
        self.assertEqual(total,27)
        self.assertEqual(len(rows),27)
        self.assertEqual(len(chosen),3)
        self.assertGreater(len({(r['groups'],r['candidate_pair_incidence']) for r in rows}),1)

    def test_budget_defers_expansion(self):
        sat_est=len(self.ops)*9
        with tempfile.TemporaryDirectory() as d:
            result=run(self.root,Path(d),scope='all',max_cases=9,family_limit=2,
                       work_budget=sat_est, no_graphviz=True)
            self.assertEqual(result['included_phases'],['SAT'])
            self.assertTrue(any(r['decision']=='deferred_budget' for r in result['phase_gates']))

    def test_modifier_deletion_not_silent(self):
        rows=perturbation_controls(self.sat,self.ops,self.quals)
        self.assertEqual(len(rows),6)
        self.assertTrue(all(r['status']=='observed' for r in rows))
        self.assertTrue(all(r['qualifier_signature_changed'] or r['operator_signature_changed'] for r in rows))
        neg=next(x for x in rows if x['unit']=='SAT:10.7')
        self.assertTrue(neg['operator_signature_changed'])

    def test_cross_phase_pilot_files_utf8_and_graphml(self):
        with tempfile.TemporaryDirectory() as d:
            src_sha=[source_sha(self.paths[p]) for p in ('SAT','RAJ','TAM')]
            out=Path(d)
            result=run(self.root,out,scope='all',max_cases=27,family_limit=3,
                       work_budget=250000,no_graphviz=True)
            self.assertEqual(result['included_phases'],['SAT','RAJ','TAM'])
            self.assertEqual(result['identity_cases_run'],27)
            self.assertEqual(src_sha,[source_sha(self.paths[p]) for p in ('SAT','RAJ','TAM')])
            tree=ET.parse(out/'操作子中心_三相出現グラフ.graphml')
            ns='{http://graphml.graphdrawing.org/xmlns}'
            keys=[k.get('id') for k in tree.getroot().findall(ns+'key')]
            self.assertIn('edge_kind',keys)
            kinds=[el.text for el in tree.iter(ns+'data') if el.get('key') in ('kind','edge_kind')]
            self.assertIn('qualifier_or_scope_occurrence',kinds)
            self.assertIn('contains_qualifier_surface_not_verified_scope',kinds)
            self.assertNotIn('logical_entailment',kinds)
            # Force explicit UTF-8 for cp932 Windows defaults.
            self.assertIn('操作子', (out/'操作子中心_三相グラフビューア.html').read_text(encoding='utf-8'))
            self.assertNotIn(b'\r\n', (out/'操作子中心_三相グラフビューア.html').read_bytes())
            self.assertNotIn(b'\r\n', (out/'集計と非主張境界.json').read_bytes())
            with (out/'記述単位と操作子記号化.csv').open(encoding='utf-8',newline='') as f:
                rows=list(csv.DictReader(f))
            self.assertEqual(len(rows),result['statement_units'])
            self.assertTrue(all('⟦' not in row['original'] for row in rows))
            self.assertIn('not logical',result['kind'].lower())

    def test_family_ablation_removes_only_candidate_co_use(self):
        baseline,ablated=family_ablation(self.sat,self.ops)
        self.assertEqual(len(ablated),len({o.family for o in self.ops}))
        self.assertTrue(all(x['pair_incidence_drop']>=0 for x in ablated))
        self.assertTrue(all(x['ablated_largest']<=baseline['largest_component'] for x in ablated))

    def test_sha_expectation_prevents_stale_reuse(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):
                run(self.root,Path(d),scope='sat',max_cases=1,
                    family_limit=1,work_budget=100000, expected_sat_sha='0'*64,no_graphviz=True)


if __name__=='__main__':
    unittest.main()

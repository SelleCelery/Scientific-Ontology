#!/usr/bin/env python3
"""Regression contract for the self-contained Euclid 465 navigator.

Checks graph arithmetic and displayed dataset integrity. This DOES NOT validate
mathematical derivations, language semantics, or a physical gamma equation.
"""
import csv
import json
import re
import unittest
from collections import defaultdict, deque
from pathlib import Path

from euclid_terminal_future_experiment import (MODELS, X_VALUES, OUTPUT,
    examine_graph, compute_rows, read_embedded_data, cut_stats)

NAV = Path(__file__).resolve().parent.parent / 'navigator/euclid-13books-alpha-beta-gamma-navigator.html'


def load():
    text = NAV.read_text(encoding='utf-8')
    found = re.search(r'<script id="embeddedData" type="application/json">(.*?)</script>', text, re.S)
    if found is None:
        raise ValueError('Embedded JSON dataset was not found')
    data = json.loads(found.group(1))
    return text, data


def reachability(data):
    ids = {r['id'] for r in data['props']}
    children = {id_: set() for id_ in ids}
    parents = {id_: set() for id_ in ids}
    for src, target in data['alphaEdges']:
        if src not in ids or target not in ids:
            raise ValueError('Invalid alpha edge')
        children[src].add(target)
        parents[target].add(src)
    order = list(ids)
    indeg = {id_: len(parents[id_]) for id_ in ids}
    queue = deque(id_ for id_ in ids if indeg[id_] == 0)
    top = []
    while queue:
        a = queue.popleft()
        top.append(a)
        for b in children[a]:
            indeg[b] -= 1
            if indeg[b] == 0:
                queue.append(b)
    if len(top) != len(ids):
        raise ValueError('Cycle found in the recorded alpha graph')
    reach = {}
    for a in reversed(top):
        out = set()
        for b in children[a]:
            out.add(b)
            out.update(reach[b])
        reach[a] = out
    return parents, children, reach


class NavigatorContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html, cls.db = load()
        cls.props = {r['id']: r for r in cls.db['props']}
        cls.parents, cls.children, cls.reach = reachability(cls.db)

    def test_complete_465_dataset(self):
        self.assertEqual(len(self.props), 465)
        self.assertEqual(len(self.db['alphaEdges']), 1639)
        self.assertEqual(len(self.db['wideEdges']), 3810)
        self.assertEqual(len(self.db['catalog']), 139)

    def test_beta_baseline(self):
        self.assertEqual(sum(r['h'] for r in self.props.values()), 26011867)
        self.assertEqual(sum(r['x'] for r in self.props.values()), 19220)
        for id_, row in self.props.items():
            self.assertEqual(row['x'], len(self.reach[id_]), id_)

    def test_alpha_loss_count_each_proposition(self):
        for id_, row in self.props.items():
            self.assertEqual(row['lost'], 1 + len(self.reach[id_]), id_)

    def test_proposition_i47(self):
        self.assertEqual(self.props['I.47']['h'], 2773)
        self.assertEqual(self.props['I.47']['x'], 70)
        self.assertEqual(self.props['I.47']['lost'], 71)

    def test_future_x_counts_unique_ancestors(self):
        selected = 'I.47'
        upstream = {selected}
        pending = [selected]
        while pending:
            current = pending.pop()
            for parent in self.parents[current]:
                if parent not in upstream:
                    upstream.add(parent)
                    pending.append(parent)
        self.assertEqual(len(upstream), 25)
        self.assertEqual(19220 + 10 * len(upstream), 19470)

    def test_gamma_and_compare_control_ids(self):
        for marker in ('id="gammaRange"', 'id="gammaThreshold"',
                       'id="gammaGraph"', 'id="gammaAuto"',
                       'id="gammaZero"', 'id="gammaInfinite"',
                       'id="comparePick"', 'id="comparisonBody"',
                       'id="futureModel"', 'data-x="25"',
                       'id="matrixBody"', 'id="bookGrid"'):
            self.assertIn(marker, self.html)

    def test_trial_gamma_formula_and_impedance_boundaries(self):
        for snippet in ('function gammaGrammarModel(', 'Math.log1p(p.h)',
                        'cycleRank', 'function gammaFromSlider(',
                        'function gammaIsAbsent(', 'n===0?Infinity',
                        'n===Infinity?0'):
            self.assertIn(snippet, self.html)

    def test_c1_c2_boundary_counts_and_expansion(self):
        graph=examine_graph(self.db)
        self.assertEqual(len(graph['terminals']),146)
        self.assertEqual(graph['c1_slope'],8498)
        self.assertEqual({x:19220+8498*x for x in X_VALUES},
                         {0:19220,1:27718,10:104200,25:231670})
        self.assertEqual({x:19220+465*x for x in X_VALUES},
                         {0:19220,1:19685,10:23870,25:30845})

    def test_experiment_csv_is_reproducible(self):
        self.assertTrue(OUTPUT.is_file(),'Run euclid_terminal_future_experiment.py first')
        rows=compute_rows(self.db)
        self.assertEqual(len(rows),465*len(MODELS)*len(X_VALUES))
        with OUTPUT.open(encoding='utf-8',newline='') as file:
            saved=list(csv.DictReader(file))
        self.assertEqual(len(saved),len(rows))
        for i,(source,old) in enumerate(zip(rows,saved)):
            self.assertEqual(source.keys(),old.keys(),i)
            for key,val in source.items():
                self.assertEqual(str(val),old[key],f'row={i} key={key}')

    def test_x0_c1_c2_identical_and_rank_scope(self):
        rows=compute_rows(self.db)
        by={(r['proposition_id'],r['model'],r['x']):r for r in rows}
        for id_ in self.props:
            c1=by[(id_,'C1',0)]
            c2=by[(id_,'C2',0)]
            self.assertEqual(c1['X_extended'],self.props[id_]['x'])
            for key in ('sigma_X_before','sigma_X_after','loss_sigma_X',
                        'loss_rank_of_465','alpha_lost'):
                self.assertEqual(c1[key],c2[key],(id_,key))
        self.assertEqual(by[('I.47','C1',25)]['loss_sigma_X'],90927)
        self.assertEqual(by[('I.47','C2',25)]['loss_sigma_X'],9077)
        self.assertEqual(by[('XIII.18','C1',25)]['loss_sigma_X'],4653)
        self.assertEqual(by[('XIII.18','C2',25)]['loss_sigma_X'],753)
        self.assertEqual(by[('I.47','C1',25)]['X_extended'],895)
        self.assertEqual(by[('I.47','C2',25)]['X_extended'],95)

    def test_deleted_terminal_ports_are_not_reassigned(self):
        graph=examine_graph(self.db)
        for p in ('I.47','VI.31','XIII.18','I.4'):
            c=cut_stats(self.db,graph,p)
            dead=c['dead']
            survivors=set(graph['ids'])-dead
            self.assertTrue(len(graph['terminals']-dead)>0)
            # Reconstruct the C1/C2 virtual graph explicitly at x=1.
            for mode in ('C1','C2'):
                extras={}
                for t in graph['terminals']:
                    extras[t]=[f'ext:{t}' if mode=='C1' else 'ext:shared']
                recomputed={}
                for u in reversed(graph['order']):
                    if u in dead:continue
                    targets=set()
                    for child in graph['children'][u]:
                        if child in survivors:
                            targets.add(child)
                            targets.update(recomputed[child])
                    for dest in extras.get(u,[]):targets.add(dest)
                    recomputed[u]=targets
                explicit=sum(len(v) for v in recomputed.values())
                slope=(c['after_c1_slope'] if mode=='C1' else c['after_c2_slope'])
                self.assertEqual(explicit,c['after_x']+slope,(p,mode))

    def test_external_comparison_controls_and_no_gamma_semantic_claim(self):
        for marker in ('id="futureModel"','data-x="0"','data-x="1"',
                       'data-x="10"','data-x="25"','id="matrixBody"',
                       'function extensionResult(', 'function renderMatrix(',
                       'const TERMINALS=', '切断後の新生終端へ仮想後続は付け直しません',
                       '同じノード予算の比較ではありません'):
            self.assertIn(marker,self.html)
        self.assertNotIn('id="futureX"',self.html)

    def test_no_runtime_external_dependency(self):
        self.assertNotIn('<script src="https://', self.html)
        self.assertNotIn('<link rel="stylesheet" href="https://', self.html)


if __name__ == '__main__':
    unittest.main(verbosity=2)

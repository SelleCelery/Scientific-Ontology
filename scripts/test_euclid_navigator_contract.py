#!/usr/bin/env python3
"""Regression contract for the self-contained Euclid 465 navigator.

Checks graph arithmetic and displayed dataset integrity. This DOES NOT validate
mathematical derivations, language semantics, or a physical gamma equation.
"""
import json
import re
import unittest
from collections import defaultdict, deque
from pathlib import Path

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
                       'id="futureX"', 'id="bookGrid"'):
            self.assertIn(marker, self.html)

    def test_trial_gamma_formula_and_impedance_boundaries(self):
        for snippet in ('function gammaGrammarModel(', 'Math.log1p(p.h)',
                        'cycleRank', 'function gammaFromSlider(',
                        'function gammaIsAbsent(', 'n===0?Infinity',
                        'n===Infinity?0'):
            self.assertIn(snippet, self.html)

    def test_no_runtime_external_dependency(self):
        self.assertNotIn('<script src="https://', self.html)
        self.assertNotIn('<link rel="stylesheet" href="https://', self.html)


if __name__ == '__main__':
    unittest.main(verbosity=2)

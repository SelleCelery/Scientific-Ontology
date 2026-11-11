#!/usr/bin/env python3
"""Research probe tests; stdlib-only and Windows UTF-8-safe."""
from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPEC = importlib.util.spec_from_file_location('probe_sentence_dictionary',
                                           Path(__file__).with_name('probe_sentence_dictionary.py'))
probe = importlib.util.module_from_spec(SPEC)
import sys
sys.modules[SPEC.name] = probe
SPEC.loader.exec_module(probe)


def dummy(identifier: str, words: tuple[str, ...], exp: tuple[str, ...] = ()):
    return probe.Sentence(id=identifier, source='fixture', line=1, column=0,
                          numbered='', section='', text='例。', kind='prose',
                          alpha_flags=('終止表面あり',), terms=words,
                          expressions=exp, pairs=tuple(' | '.join(pair) for pair in
                          __import__('itertools').combinations(sorted(words), 2)),
                          frames=tuple(f'{e} | {w}' for e in exp for w in words),
                          headword='')


class SentenceDictionaryProbe(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.src = ROOT / probe.SOURCE_REL
        cls.corpus = probe.parse_sentences(cls.src)

    def test_source_sha(self):
        self.assertEqual(probe.sha256(self.src), probe.EXPECTED_SHA256)

    def test_full_corpus_includes_nonnumbered(self):
        self.assertGreater(len(self.corpus), 265)
        self.assertEqual(sum(bool(s.numbered) for s in self.corpus), 265)
        self.assertTrue(any(not s.numbered for s in self.corpus))
        self.assertTrue(any(s.kind.startswith('fragment:') for s in self.corpus))
        self.assertEqual(len(set(s.id for s in self.corpus)), len(self.corpus))

    def test_anchor_preserves_original_line(self):
        lines = self.src.read_text(encoding='utf-8').splitlines()
        for s in self.corpus:
            self.assertEqual(lines[s.line-1][s.column:s.column+len(s.text)], s.text)
        self.assertTrue(any(s.numbered == '0.2' and s.text.startswith('知とは') for s in self.corpus))

    def test_definition_is_candidate_not_proof(self):
        s = next(x for x in self.corpus if x.numbered == '0.2')
        self.assertEqual(s.headword, '知')
        self.assertIn('定義形式候補', s.alpha_flags)
        self.assertNotIn('成立性証明', s.alpha_flags)
        other = next(x for x in self.corpus if x.numbered == '0.3')
        self.assertEqual(other.headword, '認識')

    def test_negation_marked_without_false_judgment(self):
        s = next(x for x in self.corpus if x.numbered == '0.2.1')
        self.assertIn('否定作用域未解析', s.alpha_flags)
        self.assertFalse(any('偽' in label for label in s.alpha_flags))
        self.assertIn('疑問・非断定候補', probe.alpha_flags_for('何を照合するのか？', True))

    def test_open_vocabulary_does_not_filter_unrelated_terms(self):
        self.assertIn('銀河', probe.terms_for('銀河の望遠鏡で観測した。'))
        self.assertIn('望遠鏡', probe.terms_for('銀河の望遠鏡で観測した。'))
        self.assertNotIn('Translation_Note', probe.terms_for(
            '翻訳は[`原文`](../Translation_Note.md)に従う。'))

    def test_isolated_sentence_is_provisionally_registered(self):
        a, b = dummy('a', ('同期',)), dummy('b', ('天体',))
        result = probe.replay([a,b], [dummy('q',('天体',))], warmup=0,
                              save_history=True)
        self.assertEqual(result['admitted'], 2)
        self.assertEqual(result['deferred'], 0)
        self.assertEqual(result['isolated'], 2)
        self.assertEqual(result['history'][1]['action'], 'provisional_register')

    def test_early_filter_can_destroy_later_use(self):
        a = dummy('a', ('通信',))
        b = dummy('b', ('未知', '接触'))
        c = dummy('c', ('通信', '未知'))
        query = dummy('q', ('接触',))
        full = probe.replay([a,b,c], [query], policy='all', warmup=1)
        early = probe.replay([a,b,c], [query], policy='early-filter', warmup=1)
        self.assertEqual(early['deferred'], 1)
        self.assertGreater(full['final'], early['final'])
        self.assertEqual(full['admitted'], 3)
        self.assertEqual(early['admitted'], 2)

    def test_order_changes_path_not_final_all_registered(self):
        a, b = dummy('a', ('通信',)), dummy('b', ('天体',))
        c = dummy('c', ('通信', '天体'))
        q = dummy('q', ('通信', '天体'))
        left = probe.replay([a,b,c], [q])
        right = probe.replay([c,b,a], [q])
        self.assertNotEqual(left['auc'], right['auc'])
        self.assertEqual(left['final'], right['final'])

    def test_split_fixed_across_permutations(self):
        first = probe.stable_split(self.corpus, 17)
        second = probe.stable_split(list(reversed(self.corpus)), 17)
        # Input permutation does not change the split itself.
        for group in ('register','tune','test'):
            self.assertEqual({x.id for x in first[group]}, {x.id for x in second[group]})
        self.assertTrue(set(x.id for x in first['test']).isdisjoint(
                        set(x.id for x in first['register'])))
        self.assertTrue(set(x.id for x in first['tune']).isdisjoint(
                        set(x.id for x in first['test'])))

    def test_optimizer_cannot_select_from_test_set(self):
        xs = [dummy(f's{i}', (f'word{i}', '共通' if i % 2 else '別語'))
              for i in range(18)]
        train, tune = xs[:12], xs[12:15]
        _, origin1, trace1, _ = probe.optimize_order(train,tune,xs[15:],
                                                      seed=1,rounds=2,swaps=2,warmup=1)
        _, origin2, trace2, _ = probe.optimize_order(train,tune,
                         [dummy('different_test', ('まったく別',))],
                         seed=1,rounds=2,swaps=2,warmup=1)
        self.assertEqual(origin1,origin2)
        self.assertEqual(trace1,trace2)

    def test_full_pipeline_preserves_source_and_outputs_parse(self):
        before = hashlib.sha256(self.src.read_bytes()).hexdigest()
        with tempfile.TemporaryDirectory() as folder:
            out = Path(folder)
            got = probe.run(self.src,out,rounds=2,swaps=2)
            self.assertGreater(got['sentence_count'],265)
            self.assertEqual(got['all_register']['deferred'],0)
            self.assertGreater(got['all_register']['zero_overlap_when_added'],0)
            self.assertEqual(hashlib.sha256(self.src.read_bytes()).hexdigest(),before)
            with (out/'全文収録とα表面監査.csv').open(encoding='utf-8', newline='') as fp:
                table=list(csv.DictReader(fp))
            self.assertEqual(len(table),len(self.corpus))
            self.assertIn('知とは', (out/'全文収録とα表面監査.csv').read_text(encoding='utf-8'))
            with (out/'後続文の辞書照合と未登録表現.csv').open(encoding='utf-8', newline='') as fp:
                self.assertGreater(len(list(csv.DictReader(fp))),0)
            ET.parse(out/'文と用語表現の使用関係.graphml')
            j=json.loads((out/'実験集計と非主張境界.json').read_text(encoding='utf-8'))
            self.assertIn('no logical inference',j['reference_graph'])
            self.assertTrue(any(x['kind'] == 'numbered' for x in table))

    def test_hash_mismatch_stops(self):
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaisesRegex(ValueError, 'SHA-256 changed'):
                probe.run(self.src,Path(folder),rounds=1,swaps=0,
                          expect_sha256='0'*64)


if __name__=='__main__':
    unittest.main()

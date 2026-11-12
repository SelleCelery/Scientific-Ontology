#!/usr/bin/env python3
"""Contract and behavior checks for the meaning-neutral literal-context probe."""
from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import probe_collation_blind_structure as probe


def obs(id_: str, left: str, right: str, line: int = 1):
    return probe.Observation(id_, line, 1, 1, left + probe.ANCHOR + right, left, right)


class BlindStructureTests(unittest.TestCase):
    def test_all_literal_occurrences_including_compounds_and_heading(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td)/'text.md'
            p.write_text('## 再照合可能性\nA照合B照合C\n', encoding='utf-8')
            xs=probe.gather(p)
            self.assertEqual([x.line for x in xs], [1,2,2])
            self.assertEqual(xs[0].left[-1:], '再')
            self.assertEqual(xs[0].right[0], '可')
            self.assertEqual(xs[1].right[0], 'B')
            self.assertEqual(xs[2].right[0], 'C')
            for x in xs:
                self.assertEqual(x.original_line[x.column-1:x.column-1+2], probe.ANCHOR)

    def test_no_word_segmentation_or_semantic_relation_required(self):
        xs=[obs('a','ABC-X','1'),obs('b','ABC-X','2')]
        self.assertEqual([x.preceding(2) for x in xs], ['-X','-X'])
        m=probe.ContextCode(2, probe.alphabet_for(xs))
        m.register(xs[0])
        self.assertEqual(m.estimate(xs[1]),m.estimate(obs('c','何を比較するか-X','2')))

    def test_inadequate_contexts_are_not_discarded(self):
        xs=[obs('a','X','a'),obs('b','Y','b'),obs('c','Z','c')]
        m,_,trace=probe.replay(xs,1,probe.alphabet_for(xs),trace=True)
        self.assertEqual(m.total,3)
        self.assertEqual(len(m.registered),3)
        self.assertEqual([z['previous_context_count'] for z in trace],[0,0,0])

    def test_line_disjoint_splits(self):
        xs=[obs(f'x{i}', 'L',str(i),i) for i in range(1,23)]
        xs.extend([obs('extra','Y','Z',4)])
        chunks=probe.split_by_line(xs,20261112)
        self.assertEqual(sum(len(v) for v in chunks.values()), len(xs))
        self.assertEqual({x.id for c in chunks.values() for x in c}, {x.id for x in xs})
        sets=[{x.line for x in c} for c in chunks.values()]
        for i in range(len(sets)):
            for j in range(i+1,len(sets)):
                self.assertFalse(sets[i] & sets[j])

    def test_split_reproducible(self):
        xs=[obs(f'x{i}','L',str(i),i) for i in range(1,23)]
        a=probe.split_by_line(xs,42)
        b=probe.split_by_line(xs,42)
        self.assertEqual(a,b)

    def test_missing_anchor_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'x.md'; p.write_text('ABC\n',encoding='utf-8')
            self.assertEqual(probe.gather(p),[])
            with self.assertRaises(ValueError): probe.gather(p,anchor='')

    def test_prior_distribution_valid(self):
        xs=[obs('a','再','可'),obs('b','再','可'),obs('c','、','が')]
        model=probe.ContextCode(1,probe.alphabet_for(xs))
        for x in xs:model.register(x)
        for context in ('再','、','X'):
            probsum=sum(model.estimate_pair(context,category)[1] for category in model.alphabet)
            self.assertAlmostEqual(probsum,1,places=10)

    def test_unseen_context_is_baseline(self):
        model=probe.ContextCode(1,probe.alphabet_for([obs('a','X','a')]))
        model.register(obs('a','X','a'))
        base,conditional,count=model.estimate(obs('b','Y','a'))
        self.assertEqual(count,0)
        self.assertAlmostEqual(base,conditional)

    def test_unknown_response_escape(self):
        model=probe.ContextCode(1,('あ',probe.UNKNOWN))
        model.register(obs('a','X','あ'))
        self.assertAlmostEqual(model.estimate_pair('X','非')[1], model.estimate_pair('X',probe.UNKNOWN)[1])

    def test_empty_context_and_right_boundary(self):
        x=obs('a','','')
        self.assertEqual(x.preceding(3),'\u2400\u2400\u2400')
        self.assertEqual(x.response,probe.BORDER)
        model=probe.ContextCode(1,probe.alphabet_for([x]))
        model.register(x)
        self.assertAlmostEqual(model.estimate(x)[1], model.estimate_pair('\u2400',probe.BORDER)[1])

    def test_register_twice_is_error(self):
        x=obs('a','X','b')
        model=probe.ContextCode(1,probe.alphabet_for([x]))
        model.register(x)
        with self.assertRaises(ValueError):model.register(x)

    def test_historical_orders_same_final_counts(self):
        xs=[obs('a','再','可'),obs('b','X','あ'),obs('c','再','可'),obs('d','X','あ')]
        alpha=probe.alphabet_for(xs)
        m1,s1,_=probe.replay(xs,1,alpha)
        m2,s2,_=probe.replay(list(reversed(xs)),1,alpha)
        self.assertEqual(m1.pairs,m2.pairs)
        self.assertEqual(m1.response_counts,m2.response_counts)
        self.assertEqual(m1.context_counts,m2.context_counts)
        self.assertEqual(m1.total,4)
        # Prequential order is allowed to change; not required for every fixture.
        self.assertEqual(s1['n'],s2['n'])

    def test_shuffled_control_preserves_marginals_and_ids(self):
        xs=[obs(str(i),f'pre{i}',f'suffix{i}',i) for i in range(15)]
        ys=probe.pair_control(xs,424)
        self.assertEqual([x.id for x in xs],[x.id for x in ys])
        self.assertEqual(sorted(x.right for x in xs),sorted(x.right for x in ys))
        self.assertEqual([x.left for x in xs],[x.left for x in ys])
        self.assertNotEqual([x.right for x in xs],[x.right for x in ys])

    def test_semantic_underdetermination_is_preserved(self):
        xs=[obs('a','は','が',1),obs('b','は','が',2)]
        collision=probe.unidentifiable_classes(xs,1)
        self.assertEqual(len(collision),1)
        self.assertEqual(collision[0]['count'],2)
        self.assertIn('未判定',collision[0]['interpretation'])

    def test_automated_literal_motifs_without_named_vocabulary(self):
        xs=[obs('a','ABC同期','可ABC'),obs('b','DEF同期','可DEF')]
        patterns,pairs=probe.observed_motifs(xs)
        self.assertIn(('L','同期'),{(x['side'],x['literal']) for x in patterns})
        self.assertIn(('L','期','R','可'),{('L',r['left_literal'],'R',r['right_literal']) for r in pairs if r['left_width']==1 and r['right_width']==1})
        windows=probe.window_recurrences(xs)
        self.assertIn('同期',[r['substring'] for r in windows])

    def test_holdout_is_not_inserted_into_trained_model(self):
        train=[obs('a','再','可'),obs('b','再','可')]
        test=[obs('c','再','不')]
        model,_,_=probe.replay(train,1,probe.alphabet_for(train))
        before=(model.total,dict(model.pairs))
        _=probe.heldout_score(model,test)
        self.assertEqual((model.total,dict(model.pairs)),before)

    def test_source_sha_rejection(self):
        with tempfile.TemporaryDirectory() as td:
            src=Path(td)/'src.md'; src.write_text('照合\n',encoding='utf-8')
            with self.assertRaisesRegex(ValueError,'SHA-256 mismatch'):
                probe.compute(src,Path(td)/'out',41,2,2,'0'*64)
            self.assertFalse((Path(td)/'out').exists())

    def test_end_to_end_determinism_and_no_assigned_roles(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            src=root/'corpus.md'
            lines=[f'{i:02d}\u3000X{i%3}照合Y{i%4}。' for i in range(1,25)]
            lines[2] = '03\u3000再照合可能性と照合。'
            src.write_text('\n'.join(lines)+'\n',encoding='utf-8')
            expected=hashlib.sha256(src.read_bytes()).hexdigest()
            a=probe.compute(src,root/'a',2026,4,6,expected)
            b=probe.compute(src,root/'b',2026,4,6,expected)
            self.assertEqual(a,b)
            f1={p.name:p.read_bytes() for p in (root/'a').iterdir()}
            f2={p.name:p.read_bytes() for p in (root/'b').iterdir()}
            self.assertEqual(f1,f2)
            self.assertEqual(a['occurrence_count'],25)
            self.assertEqual(len(f1),13)
            self.assertEqual(a['splits']['train']['occurrences']+a['splits']['tune']['occurrences']+a['splits']['test']['occurrences'],25)
            self.assertTrue(a['orders']['final_state_same_across_orders'])
            output='\n'.join(p.read_text(encoding='utf-8') for p in (root/'a').iterdir() if p.suffix=='.csv')
            self.assertNotIn('definition_reference',output)

    def test_actual_source_if_present(self):
        source=Path(__file__).resolve().parents[1]/probe.SOURCE_REL
        if not source.is_file():
            self.skipTest('source not packaged in isolated test distribution')
        self.assertEqual(probe.sha256_file(source),probe.SOURCE_SHA)
        xs=probe.gather(source)
        self.assertEqual((len(xs),len({x.line for x in xs})),(75,67))
        row=[x for x in xs if x.line==273]
        self.assertEqual(len(row),1)
        self.assertEqual((row[0].preceding(1),row[0].response),('は','が'))


if __name__ == '__main__':
    unittest.main()

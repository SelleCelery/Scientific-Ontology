from __future__ import annotations
import json
import tempfile
import unittest
from pathlib import Path
import build_so_term_dictionary as b
import render_so_term_dictionary as render

class DictionaryIsolationTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.root=Path(self.temp.name);self.repo=self.root/'repo';self.repo.mkdir()
        self.raw='照合とは、一致と不一致を確認する操作である。\n\n未解決とは、偽ではない。\n\n再照合可能性を保持する。\n\nまれな語も残す。\n'
        self.source=self.repo/'body.md';self.source.write_text(self.raw,encoding='utf-8')
        (self.repo/'GLOSSARY.md').write_text('# 比較辞書\n\n## 照合\n比較辞書の秘密定義。\n',encoding='utf-8')
        self.plan=self.root/'plan.json'
        self.plan_data={'archive_sha256':'fixture','files':[{'path':'body.md','sha256':b.sha_bytes(self.source.read_bytes()),'selection':'include','layer':'fixture','stage':'fixture'},{'path':'GLOSSARY.md','sha256':'not-consumed','selection':'exclude','reason':'isolated_reference'}]}
        b.dump_json(self.plan,self.plan_data)
        self.stage=self.root/'stage';self.out=self.root/'out';self.updates=self.root/'updates.jsonl'
    def tearDown(self):self.temp.cleanup()
    def prepare(self):return b.prepare(self.repo,self.plan,self.stage)
    def update(self,text=None,evidence=None):
        return {'term':'照合','definition':text or '一致・不一致を確認する操作。','evidence_texts':evidence or ['照合とは、一致と不一致を確認する操作である。'],'batch':'fixture','reason':'用例整理'}
    def finish(self,updates=None):
        b.dump_lines(self.updates,updates or [self.update()])
        return b.finish(self.stage,self.updates,self.out)
    def test_reference_glossary_is_not_read_by_prepare(self):
        self.prepare();first=(self.stage/'input_sentences.jsonl').read_bytes()
        (self.repo/'GLOSSARY.md').write_bytes(b'\xff\xfe\x00poison')
        self.prepare();self.assertEqual(first,(self.stage/'input_sentences.jsonl').read_bytes())
    def test_source_hash_change_stops(self):
        self.source.write_text('changed',encoding='utf-8')
        with self.assertRaises(ValueError):self.prepare()
    def test_source_traversal_is_rejected(self):
        with self.assertRaises(ValueError):b.safe_path(self.repo,'../outside.md')
    def test_only_text_is_passed_as_content_input(self):
        self.prepare()
        for row in b.load_lines(self.stage/'input_sentences.jsonl'):self.assertEqual(set(row),{'text'})
    def test_source_location_is_retained_separately(self):
        self.prepare();row=b.load_lines(self.stage/'source_map.jsonl')[0]
        self.assertEqual(row['source_path'],'body.md');self.assertEqual(row['line_start'],1)
    def test_source_layer_does_not_change_dictionary(self):
        self.prepare();self.finish();first=(self.out/'dictionary.jsonl').read_bytes()
        self.plan_data['files'][0]['layer']='pretend-canonical-authority'
        self.plan_data['files'][0]['stage']='reordered-label-only';b.dump_json(self.plan,self.plan_data)
        self.prepare();self.finish();self.assertEqual(first,(self.out/'dictionary.jsonl').read_bytes())
    def test_source_map_not_a_finish_input(self):
        self.prepare();self.finish();first=(self.out/'dictionary.jsonl').read_bytes()
        (self.stage/'source_map.jsonl').write_text('not json',encoding='utf-8')
        self.finish();self.assertEqual(first,(self.out/'dictionary.jsonl').read_bytes())
    def test_markdown_link_keeps_words_not_target(self):
        t=b.clean_inline('[照合](01_Sat_Truth/owner.md)が必要。')
        self.assertIn('照合',t);self.assertNotIn('owner.md',t);self.assertNotIn('01_Sat',t)
    def test_directory_pointer_is_removed(self):
        t=b.clean_inline('05_Research_Notes/Example/ に置く。')
        self.assertNotIn('05_Research_Notes',t)
    def test_fences_and_metadata_are_not_examples(self):
        ps,_=b.paragraphs('> Status: Draft\n\n```text\n秘密参照\n```\n\n日本語の本文。\n')
        self.assertEqual([p[0] for p in ps],['日本語の本文。'])
    def test_quoted_sentence_is_not_split_inside_quote(self):
        self.assertEqual(b.split_sentences('「まだだ。待つ」と述べる。次へ。'),['「まだだ。待つ」と述べる。','次へ。'])
    def test_negative_definition_is_not_positive_identity(self):
        ds=b.explicit_definitions('未解決とは、偽ではない。')
        self.assertEqual(ds[0][0],'未解決');self.assertIn('ではない',ds[0][1])
    def test_not_necessarily_is_not_a_definition(self):
        self.assertEqual(b.explicit_definitions('照合とは限らない。'),[])
    def test_function_forms_are_retained(self):
        c=b.headword_candidates('同期には照合が必要ではない。')
        self.assertIn('ではない',c);self.assertIn('は',c);self.assertIn('照合',c)
    def test_compound_and_singleton_survive(self):
        self.prepare();r={x['term']:x for x in b.load_lines(self.stage/'automatic_drafts.jsonl')}
        self.assertIn('再照合可能性',r);self.assertIn('語',r)
    def test_missing_editorial_evidence_rejected(self):
        self.prepare();u=self.update();u['evidence_texts']=[]
        with self.assertRaises(ValueError):self.finish([u])
    def test_invented_editorial_evidence_rejected(self):
        self.prepare()
        with self.assertRaises(ValueError):self.finish([self.update(evidence=['照合は万能である。'])])
    def test_entry_without_own_term_in_support_rejected(self):
        self.prepare();u=self.update();u['term']='存在しない見出し'
        with self.assertRaises(ValueError):self.finish([u])
    def test_pointer_fields_rejected(self):
        with self.assertRaises(ValueError):b.assert_no_pointers({'term':'照合','source_path':'a.md'})
    def test_pointer_in_definition_rejected(self):
        self.prepare()
        with self.assertRaises(ValueError):self.finish([self.update(text='owner.md を参照する。')])
    def test_editorial_changes_keep_before_and_after(self):
        self.prepare();self.finish([self.update(),self.update(text='比較した結果の差を確認する操作。')])
        h=b.load_lines(self.out/'definition_revision_log.jsonl')
        self.assertEqual(h[1]['before']['definition'],h[0]['after']['definition'])
        self.assertNotEqual(h[1]['before'],h[1]['after'])
    def test_unresolved_terms_not_invented_definitions(self):
        self.prepare();self.finish()
        r={x['term']:x for x in b.load_lines(self.out/'dictionary.jsonl')}
        self.assertEqual(r['再照合可能性']['status'],'usage_only');self.assertIsNone(r['再照合可能性']['definition'])
    def test_replay_is_deterministic(self):
        self.prepare();self.finish();first={f.name:f.read_bytes() for f in self.out.iterdir()}
        self.finish();self.assertEqual(first,{f.name:f.read_bytes() for f in self.out.iterdir()})
    def test_compare_requires_unchanged_freeze(self):
        self.prepare();self.finish();p=self.out/'dictionary.jsonl';p.write_bytes(p.read_bytes()+b'\n')
        with self.assertRaises(ValueError):b.compare(p,self.out/'dictionary_freeze.json',self.repo/'GLOSSARY.md',self.root/'comparison.json')
    def test_compare_does_not_change_created_dictionary(self):
        self.prepare();self.finish();p=self.out/'dictionary.jsonl';before=p.read_bytes()
        b.compare(p,self.out/'dictionary_freeze.json',self.repo/'GLOSSARY.md',self.root/'comparison.json')
        self.assertEqual(before,p.read_bytes())
        self.assertNotIn('秘密定義',p.read_text(encoding='utf-8'))
    def test_render_has_no_source_map_or_reference_read(self):
        self.prepare();self.finish();out=self.root/'dictionary.html'
        render.render(self.out/'dictionary.jsonl',self.out/'dictionary_freeze.json',self.stage/'lexicon_observations.jsonl',out)
        text=out.read_text(encoding='utf-8')
        self.assertIn('一致・不一致',text);self.assertNotIn('body.md',text);self.assertNotIn('秘密定義',text)
        self.assertNotIn('src="https://',text);self.assertNotIn('source_path',text)
    def test_real_packaged_dictionary_matches_freeze(self):
        data=Path(__file__).resolve().parents[1]/'tools'/'assessment'/'term_dictionary'
        if not (data/'created/dictionary.jsonl').exists():self.skipTest('Package results not installed')
        frozen=json.loads((data/'created/dictionary_freeze.json').read_text(encoding='utf-8'))
        self.assertEqual(b.sha_bytes((data/'created/dictionary.jsonl').read_bytes()),frozen['dictionary_sha256'])
        for row in b.load_lines(data/'created/dictionary.jsonl'):b.assert_no_pointers(row)
    def test_real_editorial_evidence_is_in_text_input(self):
        data=Path(__file__).resolve().parents[1]/'tools'/'assessment'/'term_dictionary'
        if not (data/'formation/input_sentences.jsonl').exists():self.skipTest('Package results not installed')
        corpus={r['text'] for r in b.load_lines(data/'formation/input_sentences.jsonl')}
        for u in b.load_lines(data/'data/editorial_updates.jsonl'):
            self.assertTrue(u['evidence_texts'])
            for s in u['evidence_texts']:self.assertIn(s,corpus)

if __name__=='__main__':unittest.main()

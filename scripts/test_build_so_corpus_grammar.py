# -*- coding: utf-8 -*-
"""Tests for the corpus-wide Japanese grammar surface atlas."""
import importlib.util
import json
import re
import tempfile
import unittest
from pathlib import Path

SCRIPT=Path(__file__).with_name('build_so_corpus_grammar.py')
spec=importlib.util.spec_from_file_location('build_so_corpus_grammar',SCRIPT)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class GrammarAtlasTests(unittest.TestCase):
    def test_pattern_ids_unique_and_stable(self):
        patterns=m.compile_patterns()
        self.assertEqual(len(patterns),170)
        self.assertEqual(len({x['id'] for x in patterns}),len(patterns))
        self.assertEqual(patterns[0]['id'],'G01-001')

    def test_single_character_particle_is_weak_not_confirmed(self):
        g=next(x for x in m.compile_patterns() if x['group']=='助詞・係り' and x['label']=='は')
        self.assertEqual(g['mode'],'weak')
        self.assertIn('固有語',g['risk'])
        self.assertIsNotNone(g['re'].search('はたらき'))

    def test_connection_marker_not_logical_proof(self):
        g=next(x for x in m.compile_patterns() if x['label']=='したがって')
        self.assertIn('導出',g['risk'])

    def test_quotes_and_url_masking(self):
        s='接触 [`file.md`](https://example.test/h) と `ではない` を検討する'
        o=m.mask_line(s)
        self.assertNotIn('file.md',o)
        self.assertNotIn('https:',o)
        self.assertNotIn('`ではない`',o)
        self.assertIn('を検討する',o)

    def test_regex_is_local_and_bounded(self):
        g=next(x for x in m.compile_patterns() if x['label']=='だけ.*?とは限らない')
        self.assertIsNotNone(g['re'].search('その条件だけで成立するとは限らない。'))
        self.assertIsNone(g['re'].search('だけ'+'長'*70+'とは限らない'))

    def test_html_escapes_source_text(self):
        html=m.render_viewer([{'group':'助詞・係り','surface':'</script><script>alert(1)</script>',
                  'id':'G01-001','matching_mode':'weak','explanation':'test','risk':'risk',
                  'surface_hits':0,'documents_with_hits':0,'examples':[]}],{'scanned_documents':1,
                  'grammar_patterns':1,'all_surface_hits_including_overlaps':0,
                  'weak_single_character_substring_hits':0,'nonweak_surface_hits':0,
                  'unmatched_japanese_lines':0})
        self.assertNotIn('</script><script>alert(1)</script>',html)
        self.assertIn('\\u003c/script\\u003e',html)
        self.assertNotIn('https://cdn.',html)

    def test_textfile_enforces_final_lf_without_duplication(self):
        with tempfile.TemporaryDirectory() as td:
            target=Path(td)/'grammar_viewer.html'
            m.textfile(target,'<html>ok</html>')
            self.assertEqual(target.read_bytes(),b'<html>ok</html>\n')
            m.textfile(target,'<html>ok</html>\n')
            self.assertEqual(target.read_bytes(),b'<html>ok</html>\n')

    def test_source_sha_stable(self):
        self.assertEqual(m.sha(b'test'), '9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08')

if __name__=='__main__':unittest.main()

#!/usr/bin/env python3
"""Pure stdlib regression tests for the term reference overlay."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).with_name("build_so_term_reference_graph.py")
spec = importlib.util.spec_from_file_location("term_graph_builder", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class ReferenceGraphTest(unittest.TestCase):
    def test_longest_match_no_duplicate_tokenization(self):
        forms = [("AI", "a"), ("AI導入", "b"), ("境界", "c"), ("無", "d")]
        hits = mod.lexical_matches("AI導入と境界と無", forms)
        self.assertEqual([h["term_id"] for h in hits], ["b", "c"])

    def test_latin_identifier_boundary(self):
        self.assertEqual(mod.lexical_matches("AIM AID AI", [("AI", "a")]),
                         [{"term_id": "a", "surface": "AI", "start": 8, "end": 10}])

    def test_path_safety(self):
        for path in ["../bad.md", "C:\\bad.md", "/etc/passwd", "x/../bad.md"]:
            self.assertFalse(mod.valid_path(path))
        self.assertTrue(mod.valid_path("01_Sat_Truth/Good.ja.md"))

    def test_build_edges_are_surface_only_and_source_checked(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "a.md").write_bytes("境界の概念。\n".encode("utf-8"))
            d = {"entries": [
                {"id": "x", "term": "境界", "definition": "概念の条件", "group": "so", "aliases": [],
                 "source_attestations": [{"path": "a.md", "line": 1, "excerpt": "境界の概念。"}]},
                {"id": "y", "term": "条件", "definition": "境界の扱い", "group": "general", "aliases": [],
                 "source_attestations": [{"path": "a.md", "line": 1, "excerpt": "条件"}]},
            ], "source_snapshot_sha256": "dummy"}
            g = {"nodes": [{"id": "doc:a", "type": "document", "path": "a.md", "title": {"ja": "A"}, "state": "public"}]}
            dictionary = root / "dict.json"; graph = root / "docs.json"
            mod.dump(dictionary, d); mod.dump(graph, g)
            overlay, index, summary = mod.build(dictionary, graph, root)
            self.assertEqual(summary["original_source_attestations"], 2)
            self.assertEqual(summary["attestation_checks"]["verified_surface_on_line"], 1)
            self.assertEqual(len(overlay["diagnostics"]["unverified_attestations"]), 1)
            self.assertEqual(sum(e["relation"] == mod.REL_ATTESTED for e in overlay["edges"]), 1)
            self.assertEqual(sum(e["relation"] == mod.REL_DEFINITION for e in overlay["edges"]), 2)
            self.assertEqual(index["entries"][0]["senses"][0]["scope"], "undetermined_draft")
            self.assertNotIn("logical_support", [e["relation"] for e in overlay["edges"]])

    def test_reproducible_serialization_and_newline(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "test.json"
            mod.dump(p, {"ja": "境界", "entries": []})
            before = p.read_bytes(); mod.dump(p, {"entries": [], "ja": "境界"})
            self.assertEqual(before, p.read_bytes())
            self.assertTrue(before.endswith(b"\n"))
            self.assertFalse(before.endswith(b"\r\n"))

    def test_explicit_single_character_policy(self):
        self.assertEqual(mod.lexical_matches("無と境界", [("無", "x"), ("境界", "y")]),
                         [{"term_id": "y", "surface": "境界", "start": 2, "end": 4}])


if __name__ == "__main__":
    unittest.main()

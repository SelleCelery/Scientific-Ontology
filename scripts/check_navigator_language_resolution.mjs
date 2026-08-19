#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import {
  collapseDocumentsForLanguage,
  collapseSearchResultsForLanguage,
  documentLanguage,
  preferredDocumentForLanguage,
  preferredPathForLanguage,
  presentationKeyForDocument,
} from "../navigator/dist/language-core.js";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const catalog = JSON.parse(fs.readFileSync(path.join(ROOT, "tools/docs_public_catalog.json"), "utf8"));
const docs = catalog.documents ?? [];
const byPath = new Map(docs.map((doc) => [String(doc.path ?? ""), doc]));

function fail(message) {
  console.error(`NAVIGATOR LANGUAGE RESOLUTION CHECK FAILED: ${message}`);
  process.exit(1);
}

function assert(condition, message) {
  if (!condition) fail(message);
}

assert(docs.length === 130, `expected 130 public catalog documents, got ${docs.length}`);

const families = new Map();
for (const doc of docs) {
  const key = presentationKeyForDocument(doc);
  if (!families.has(key)) families.set(key, []);
  families.get(key).push(doc);
}

let pairedFamilies = 0;
for (const [key, members] of families) {
  const ja = members.find((doc) => documentLanguage(doc) === "ja");
  const en = members.find((doc) => documentLanguage(doc) === "en");
  if (!ja && !en) continue;
  if (ja && en) {
    pairedFamilies += 1;
    const jaPath = String(ja.path);
    const enPath = String(en.path);
    assert(preferredPathForLanguage(jaPath, docs, "en") === enPath, `${key}: JA -> EN did not resolve to counterpart`);
    assert(preferredPathForLanguage(enPath, docs, "ja") === jaPath, `${key}: EN -> JA did not resolve to counterpart`);
    assert(preferredDocumentForLanguage(ja, docs, "en") === en, `${key}: preferred EN document mismatch`);
    assert(preferredDocumentForLanguage(en, docs, "ja") === ja, `${key}: preferred JA document mismatch`);
  } else {
    const only = ja ?? en;
    const lang = documentLanguage(only);
    const other = lang === "ja" ? "en" : "ja";
    assert(preferredDocumentForLanguage(only, docs, other) === only, `${key}: unmatched language-specific document must fall back to itself`);
  }
}

assert(pairedFamilies === 39, `expected 39 JA/EN pair families, got ${pairedFamilies}`);
assert(Number(catalog.source?.language_pair_families ?? -1) === 39, "catalog source language_pair_families must be 39");
assert(Number(catalog.source?.unmatched_language_specific_documents ?? -1) === 7, "expected seven intentional single-language fallback documents");
const unmatchedSuffixed = docs.filter((doc) => /\.(ja|en)\.md$/i.test(String(doc.path ?? "")) && !doc.presentation?.counterpart_path);
const expectedPendingCommensurations = new Set([
  "05_Research_Notes/Language_Meaning_and_Communication_Phase_Studies/Sentence_Cloud_Bit_Probe_and_LLM_Learning.ja.md",
  "05_Research_Notes/Literary_Ontological_Notes/The_Transparent_Ghost_and_the_Bit.ja.md",
]);
assert(unmatchedSuffixed.length === expectedPendingCommensurations.size, `expected two declared pending commensurations; unmatched=${unmatchedSuffixed.length}`);
for (const doc of unmatchedSuffixed) {
  assert(expectedPendingCommensurations.has(String(doc.path)), `undeclared unmatched language-specific document: ${doc.path}`);
  assert(doc.language_relation?.role === "authoritative", `pending commensuration must retain Japanese authoritative role: ${doc.path}`);
}

for (const lang of ["ja", "en"]) {
  const visible = collapseDocumentsForLanguage(docs, docs, lang);
  const keys = new Set(visible.map(presentationKeyForDocument));
  assert(visible.length === keys.size, `${lang}: duplicate presentation families remain after collapse`);
  assert(visible.length === 91, `${lang}: expected 91 logical public entries after collapsing 39 pairs, got ${visible.length}`);
  for (const doc of visible) {
    const docLang = documentLanguage(doc);
    if ((docLang === "ja" || docLang === "en") && docLang !== lang) {
      assert(!doc.presentation?.counterpart_path, `${lang}: opposite-language document surfaced despite available counterpart: ${doc.path}`);
    }
  }
}

const exampleJa = docs.find((doc) => String(doc.path).endsWith("Claim_Strength_and_Publication_Layer_Table.ja.md"));
const exampleEn = docs.find((doc) => String(doc.path).endsWith("Claim_Strength_and_Publication_Layer_Table.en.md"));
assert(exampleJa && exampleEn, "example language pair missing");
const collapsedSearch = collapseSearchResultsForLanguage(
  [
    { ...exampleJa, score: 9.5, matches: [{ field: "title", text: "主張強度" }] },
    { ...exampleEn, score: 8.0, matches: [{ field: "title", text: "claim strength" }] },
  ],
  docs,
  "en",
  12,
);
assert(collapsedSearch.length === 1, "paired search results must collapse to one logical result");
assert(String(collapsedSearch[0].path).endsWith(".en.md"), "EN search presentation must resolve to EN document");
assert(Number(collapsedSearch[0].score) === 9.5, "collapsed search must preserve best logical-family score");

for (const doc of docs) {
  const counterpart = doc.presentation?.counterpart_path;
  if (counterpart) assert(byPath.has(String(counterpart)), `counterpart path missing from catalog: ${counterpart}`);
}

console.log(`NAVIGATOR LANGUAGE RESOLUTION CHECK PASS: 130 documents, ${pairedFamilies} JA/EN pairs, 91 logical entries per UI language`);

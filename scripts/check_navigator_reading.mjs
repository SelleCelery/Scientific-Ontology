#!/usr/bin/env node
/** Reader/editorial presentation checks. Run after: tsc -p navigator/tsconfig.json */
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import {
  publicDocumentTitle, publicLinkLabel, isTechnicalLabel,
  readingChannels, readingChannelEntries, documentForEditorialId,
  sectionSlug, fragmentFromLink, sourceHeaderLines, readerText,
} from '../navigator/dist/reader-core.js';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const read = (rel) => JSON.parse(fs.readFileSync(path.join(root, rel), 'utf8'));
const docs = read('tools/docs_public_catalog.json').documents;
const content = read('navigator/public-content.json');
let assertions = 0;
function check(condition, message) { assertions++; assert.ok(condition, message); }

for (const lang of ['ja', 'en']) {
  for (const doc of docs) {
    const title = publicDocumentTitle(doc, lang);
    check(Boolean(title), `${lang}: empty title: ${doc.path}`);
    check(!isTechnicalLabel(title, doc), `${lang}: technical title: ${doc.path}`);
    check(title !== readerText(lang, 'document'), `${lang}: existing catalog title was lost: ${doc.path}`);
    check(publicLinkLabel(String(doc.path), doc, lang) === title, `${lang}: link path is not masked: ${doc.path}`);
    check(publicLinkLabel(String(doc.path).split('/').at(-1), doc, lang) === title, `${lang}: filename is not masked: ${doc.path}`);
    check(publicLinkLabel('An authored description', doc, lang) === 'An authored description', 'Authored prose must remain unchanged');
  }
  for (const channel of readingChannels(content)) {
    const entries = readingChannelEntries(channel, docs, lang);
    check(entries.length <= (channel.documents ?? []).length, `${lang}: reading channel expansion is invalid: ${channel.id}`);
    for (const entry of entries) {
      check(Boolean(documentForEditorialId(docs, entry.documentId)), `Unknown editorial document: ${entry.documentId}`);
      check(fs.existsSync(path.join(root, entry.document.path)), `Reading-channel source is missing: ${entry.document.path}`);
    }
  }
  for (const layer of content.layers) {
    check(Boolean(layer.label?.[lang]), `Missing localized layer label: ${layer.id}`);
    check(!String(layer.label[lang]).includes(String(layer.path)), `Raw layer path shown in ${lang}`);
  }
}

const rootReadme = docs.find((doc) => doc.path === 'README.md');
const literaryFixture = docs.find((doc) => doc.id === 'inorganic_alternating_lamp_and_holiday_reading');
check(Boolean(rootReadme), 'Root README must remain eligible for editorial selection');
check(Boolean(literaryFixture), '07 literary fixture must remain eligible for editorial selection');
for (const lang of ['ja', 'en']) {
  const entries = readingChannelEntries({documents:[rootReadme.id,literaryFixture.id]}, docs, lang);
  check(entries.length === 2, `${lang}: arbitrary README + 07 editorial selection did not resolve`);
  check(entries.every((entry) => Boolean(publicDocumentTitle(entry.document, lang))), `${lang}: editorial selection lost readable title`);
}

const mock = {id:'example',path:'sub/Example.ja.md',title:{ja:'例の文書',en:'Example document'}};
check(publicDocumentTitle({id:'raw_id',title:{}}, 'en') === 'Document', 'Missing title must not leak an ID');
check(publicDocumentTitle({...mock,title:{en:'sub/Example.ja.md',ja:'例の文書'}}, 'en') === '例の文書', 'Technical titles must fall back to a real localized title');
check(publicLinkLabel('`Example.ja.md`',mock,'en') === 'Example document', 'Inline code filenames must be masked');
check(publicLinkLabel('Example.en.md',mock,'ja') === '例の文書', 'Counterpart filenames must be masked');
check(sectionSlug('Chapter I. Definitions') === 'chapter-i-definitions', 'English section slug');
check(sectionSlug('第1章 境界') === '第1章-境界', 'Japanese section slug');
check(fragmentFromLink('file.md#chapter%20one') === 'chapter one', 'Decoded section fragment');
check(fragmentFromLink('#bad%escape') === 'bad%escape', 'Invalid URL escape must not crash');
check(sourceHeaderLines('Status: Draft\nScope: conceptual model\nLanguage: en'), 'Known metadata must be masked');
check(sourceHeaderLines('Status: Literary essay\nLayer: 07_Creative_Offshoots / Literary_Essays\nScope: holiday reading\nLanguage: Japanese authoritative; English commensuration pending\nClaim strength: S1-S2/E1/U0/P1/V0\nAuthority: Creative offshoot; not a concept-definition owner\nPublic handling: not a scientific proof'), 'Full public metadata header must be recognized');
check(!sourceHeaderLines('Status: Draft\nThis is not an empirical claim.'), 'Unstructured caveats must not be masked as metadata');
check(!sourceHeaderLines('A quotation\nwith two lines'), 'Ordinary quotation must not be masked');

const app = fs.readFileSync(path.join(root,'navigator/src/app.ts'),'utf8');
check(app.includes('if (!page.isConnected) return;'), 'Detached-reader race protection is required');
check(app.includes('removePublicSourceHeader(article)'), 'Public source metadata must be removed from the reading surface');
check(app.includes('selectionSearchTools(article)'), 'Selection-to-search assistance is required');
check(app.includes('function renderReadingEditor()'), 'Developer reading editor is required');
check(app.includes('for (const doc of allDocuments())'), 'Developer editor must enumerate all public-catalog documents');
check(!fs.readFileSync(path.join(root,'navigator/src/reader-core.ts'),'utf8').includes('fetch('), 'Reader presentation must not add a network/analytics service');
console.log(`NAVIGATOR READING CHECK PASS: ${docs.length} documents in JA and EN; ${readingChannels(content).length} editorial channels; ${assertions} assertions`);

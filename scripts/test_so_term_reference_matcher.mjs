import assert from 'node:assert/strict';
import {test} from 'node:test';
import {createTermLookup, linksForTerm} from './so_term_reference_matcher.mjs';
const runtime = {kind: 'so.term_dictionary_runtime_seed', entries: [
  {id:'x', label:'境界', forms:['境界'], senses:[]},
  {id:'y', label:'存在境界論', forms:['存在境界論'], senses:[]},
  {id:'z', label:'AI', forms:['AI'], senses:[]},
  {id:'w', label:'無', forms:['無'], senses:[]},
  {id:'q', label:'境界別義', forms:['境界'], senses:[]},
]};

test('selection returns ambiguous form candidates without silent disambiguation', () => {
  const idx = createTermLookup(runtime);
  assert.deepEqual(idx.exactSelection(' 境界 ').map(x => x.id), ['x','q']);
  assert.equal(idx.exactSelection('無').length, 1);
});
test('caret uses longest surface without splitting inside longer term', () => {
  const idx = createTermLookup(runtime);
  assert.equal(idx.matchCaret('存在境界論を読む', 3).candidates[0].id, 'y');
  assert.equal(idx.matchCaret('無を調べる', 1), null);
});
test('ASCII word boundary forbids accidental identifier match', () => {
  const idx = createTermLookup(runtime);
  assert.equal(idx.matchCaret('AIM', 1), null);
  assert.equal(idx.matchCaret('AIです', 1).candidates[0].id, 'z');
});
test('term links distinguish documents from nonregistered source', () => {
  const g = {nodes:[
      {id:'dictterm:x',type:'dictionary_term',label:'境界',dictionary_id:'x'},
      {id:'dictterm:y',type:'dictionary_term',label:'存在境界論',dictionary_id:'y'},
      {id:'doc:main',type:'registered_document_reference',path:'main.md',label:'Main'},
      {id:'unregistered_source:other',type:'unregistered_source_reference',path:'other.md'},
    ], edges:[
      {from:'dictterm:x',to:'doc:main',relation:'surface_attested_in',provenance:[{line:4}]},
      {from:'dictterm:x',to:'unregistered_source:other',relation:'surface_attested_in',provenance:[{line:6}]},
      {from:'dictterm:x',to:'dictterm:y',relation:'definition_lexically_mentions',provenance:[{start:0,end:6}]}
    ]};
  const r=linksForTerm(g,'x');
  assert.equal(r.documents.length,1);assert.equal(r.unregisteredSources.length,1);assert.equal(r.terms.length,1);
});

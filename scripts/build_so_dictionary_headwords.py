#!/usr/bin/env python3
"""Exploratory headword classification across the full rc008 SO surface registry.

Provenance/limits: This is NOT an LLM forward pass over all 27,901 items, nor a
semantic correctness validator. The rules include AI-edited seed judgments; they
route ALL candidates without treating spelling alone as verified meaning.
Original GLOSSARY.md and private placeholder never enter the input corpus.
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict, deque
from datetime import datetime, timezone
import hashlib
import html
import json
import pathlib
import re
import sys
import time
import zipfile

BASE = pathlib.Path(__file__).resolve().parent.parent
RULES_DEFAULT = BASE / 'tools/assessment/term_dictionary/corpus_lexicon_classification/taxonomy_rules.json'
DICT_SHA = '4954945d30c5391aa9418257bd2289d8e0ec6aeba8106df589a662f3298707fc'
RC008_SHA = 'bcf56409d091a67b8314fce5ac6e0676a7bc79e23d517b92ac56138595ae166e'
OUTS = ('all_surface_headword_decisions.jsonl','categorized_dictionary_entries.jsonl',
        'headword_candidates.tsv','source_attestation_sidecar.jsonl','technical_proximity_watchlist.jsonl','classification_coverage.json',
        'dictionary_viewer.html')
JP = re.compile(r'[\u3040-\u30ff\u3400-\u9fff]')
KANJI = re.compile(r'[\u3400-\u9fff]')
KATA = re.compile(r'[\u30a0-\u30ff]')
HIRA_ONLY = re.compile(r'^[\u3040-\u309fー]+$')
KANJI_ONLY = re.compile(r'^[\u3400-\u9fff々〆]+$')
KATA_ONLY = re.compile(r'^[\u30a0-\u30ffー・]+$')
IDENTIFIER = re.compile(r'^[A-Za-z][A-Za-z0-9_./:+-]*$')
ALNUM = re.compile(r'^[0-9A-Za-z_./#-]+$')
SENTENCE_MARKERS = ('。','！','？','!','?','「','」','（','）','(',')','、','；',';',':','：','→','⇒','=', '＝','|','／','…','\n')
CLAUSE_INSIDE = ('という','ではない','ではなく','である','であれば','に対して','によって','として','のため','であること','すること','なければ','にある','のように','がある','をする','であった','ができ','について','ている','ときは','のでは','のか','のだ')
CLAUSE_END = ('ではない','ている','となる','である','のだ','ために','から','ならば','だった','であった','でした','できる','できない','すべき','ではなく','という','とする','ないか','のか','ものである','ことも','するか','なるか')
WEAK_PREFIX = ('的','という','して','され','として','ので','から','けれど','った','れば','こう','そう')
WEAK_SUFFIX = ('なら','あれば','によって','にとって','とは','ほど','からである','しながら','でもある')


def sha256_file(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()


def member(z:zipfile.ZipFile, suffix:str) -> bytes:
    matched=[n for n in z.namelist() if n.endswith('/'+suffix)]
    if len(matched)!=1:raise ValueError(f'expected one ZIP member {suffix}, got {matched}')
    return z.read(matched[0])


def read_jsonl(data:bytes)->list[dict]:
    return [json.loads(line) for line in data.decode('utf-8').splitlines() if line.strip()]


def dump_json(x):
    return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))


def write_jsonl(path,items):
    with pathlib.Path(path).open('w',encoding='utf-8',newline='\n') as f:
        for item in items:f.write(dump_json(item)+'\n')


def write_json(path,obj):
    with pathlib.Path(path).open('w',encoding='utf-8',newline='\n') as f:
        f.write(json.dumps(obj,ensure_ascii=False,sort_keys=True,indent=2)+'\n')


def classify(term:str, row:dict, defs:dict, rules:dict)->dict:
    """Distinguish candidate admission from speculative lexical category."""
    known=term in defs
    kinds=set(row['surface_kinds'])
    near=[r for r in rules['technical_neighbor_roots'] if r['root'].lower() in term.lower()]
    fields=sorted(set(r['field'] for r in near))
    risk=sorted(set(r['risk'] for r in near))
    exacttech=rules['technical_exact'].get(term,[])
    so_exact=term in rules['so_exact']
    so_operational=term in rules['so_operational_general_origin']
    so_marker=next((m for m in sorted(rules['so_markers'],key=lambda x:-len(x)) if term.startswith(m)),None)
    grammar=(term in rules['grammar_exact'] or 'function_expression' in kinds) and not so_exact and not exacttech
    notes=[]
    if near:notes.append('technical_adjacent_automatic_review')
    if so_operational:notes.append('ordinary_or_imported_word_used_operationally_in_so')
    if term in ('事実候補 / fact candidate','根拠仮説 / ground hypothesis'):
        notes.append('existing_normalization_collision_candidate_no_merge')

    if grammar:
        state='grammar_not_dictionary'; why=['G01:function_expression_or_editorial_grammar_form']; group=None
    elif not term.strip() or (not JP.search(term) and not re.search(r'[A-Za-z]',term)):
        state='nonheadword_notation';why=['N01:nonlexical_or_numeric'];group=None
    elif so_exact or exacttech or term in rules.get('editorially_new_definitions',{}):
        state='provisional_defined' if known else 'headword_seed'
        why=['D01:existing_editorial_draft' if known else 'M01:editorially_selected_seed']
        group = 'so' if so_exact else 'technical' if exacttech or near else 'so' if so_operational else 'general'
        why+=['S01:explicit_so_seed' if so_exact else 'T01:explicit_technical_seed' if exacttech else 'M02:editorial_seed']
    elif known:
        state='provisional_defined';why=['D01:existing_editorial_draft_not_authoritatively_accepted']
        if so_marker:
            group='so';why.append('S02:so_marker_candidate:'+so_marker)
        elif so_operational and not exacttech:
            group='so';why.append('S03:ordinary_origin_with_specific_so_sense')
        elif near:
            group='technical';why.append('T02:borrowed_root_candidate')
        else:
            group='general';why.append('L01:ordinary_headword_default_not_semantic_verification')
    elif 'definition_headword' in kinds and len(term)<24 and not any(c in term for c in SENTENCE_MARKERS):
        state='headword_candidate';why=['L02:literal_definition_headword_unreviewed']
        if so_marker:group='so';why.append('S02:so_marker_candidate:'+so_marker)
        elif so_operational and not exacttech:group='so';why.append('S03:ordinary_origin_with_specific_so_sense')
        elif near:group='technical';why.append('T02:borrowed_root_candidate')
        else:group='general';why.append('L01:ordinary_headword_default_not_semantic_verification')
    else:
        shape=word_shape(term,row,rules)
        state=shape[0];why=[shape[1]]
        if state=='headword_candidate':
            if so_marker:group='so';why.append('S02:so_marker_candidate:'+so_marker)
            elif so_operational and not exacttech:group='so';why.append('S03:ordinary_origin_with_specific_so_sense')
            elif exacttech or near:group='technical';why.append('T02:borrowed_root_candidate')
            else:group='general';why.append('L01:ordinary_headword_default_not_semantic_verification')
        else:group=None
    if 'quoted_expression' in kinds and not known and state=='headword_candidate' and not so_exact and not exacttech:
        state='hold_quoted_context';group=None;why.append('Q01:quoted_use_not_headword_confirmation')
    if term in rules['reserved_nonheadwords'] and not known and not so_exact and not exacttech:
        state='hold_fragment';group=None;why.append('F01:known_fragment_not_promoted')
    priority=('01_existing_draft' if state=='provisional_defined' else
              '02_curated_seed' if state=='headword_seed' else
              '03_literal_definition_candidate' if 'definition_headword' in kinds and state=='headword_candidate' else
              '04_compound_candidate' if 'compound_run' in kinds and state=='headword_candidate' else
              '05_supplemental_candidate' if 'supplemental_jp' in kinds and state=='headword_candidate' else
              '06_surface_shape_only' if state=='headword_candidate' else '09_hold_or_exclude')
    return {
      'term':term,'candidate_status':state,'review_priority':priority,'group':group,
      'group_ja':rules['group_japanese'].get(group,'保留・対象外'),
      'rules':why, 'confidence':'curated_provisional' if ('S01:explicit_so_seed' in why or 'T01:explicit_technical_seed' in why or 'M02:editorial_seed' in why) else 'legacy_editorial_provisional' if known else 'heuristic_unverified',
      'definition_status': 'existing_assistant_draft' if known else 'new_assistant_cautious_draft' if term in rules['editorially_new_definitions'] and state not in ('grammar_not_dictionary','nonheadword_notation') else 'no_definition',
      'technical_adjacency':bool(near or exacttech),'borrowed_domain_candidates':sorted(set(fields+exacttech)),
      'technical_boundary_alerts':risk,
      'flags':notes, 'source_kinds':sorted(kinds), 'source_registry_status':row['review_status'],
      'literal_observations':row.get('literal_observations'),
      'evidence_key':hashlib.sha256(term.encode('utf-8')).hexdigest()[:16],
      'semantic_verification':'not_human_confirmed',
    }


def word_shape(t:str, row:dict, rules:dict)->tuple[str,str]:
    if HIRA_ONLY.fullmatch(t):
        return ('hold_grammar_or_fragment','F10:unsegmented_hiragana_sequence')
    if t.startswith(('http://','https://')) or '/' in t or '\\' in t or t.count('.')>=2 or '@' in t:
        return ('hold_identifier_or_compound','I01:path_url_alias_or_identifier')
    if any(x in t for x in SENTENCE_MARKERS) or (len(t)>13 and JP.search(t)):
        return ('hold_clause_or_example','C01:punctuation_long_phrase_or_statement')
    if any(x in t for x in CLAUSE_INSIDE) or t.endswith(CLAUSE_END):
        return ('hold_clause_or_example','C02:inflected_clause_or_particle_sequence')
    if t.startswith(WEAK_PREFIX) or t.endswith(WEAK_SUFFIX):
        return ('hold_fragment','F02:suspicious_fragment_boundary')
    if ' ' in t or '\t' in t:
        return ('hold_identifier_or_compound','I02:multiple_whitespace_tokens')
    if IDENTIFIER.fullmatch(t):
        return ('hold_identifier_or_compound','I03:latin_word_or_identifier_without_term_attestation')
    if re.search(r'\d',t) and not KANJI_ONLY.fullmatch(t):
        return ('hold_identifier_or_compound','I04:version_or_number_mixed')
    if len(t)==1:
        return ('hold_fragment','F03:unreviewed_single_character')
    if KANJI_ONLY.fullmatch(t) and 2<=len(t)<=7:
        return ('headword_candidate','L10:possible_kanji_noun_shape_not_segmented')
    if KATA_ONLY.fullmatch(t) and 3<=len(t)<=16:
        return ('headword_candidate','L11:possible_katakana_noun_shape_not_segmented')
    if JP.search(t) and len(t)<=11 and (KANJI.search(t) or KATA.search(t)):
        # Kanji with hiragana is often a valid inflected word or noun, but frequent
        # prose suffixes are not dependable dictionary headwords.
        if len(t)>5 and re.search(r'([あ-ん]{3,}|の|も|を|が|は|で|に)',t):
            return ('hold_segmentation','F04:possible_clause_or_compound_requires_segmentation')
        return ('headword_candidate','L12:mixed_script_lexeme_candidate_not_semantically_read')
    return ('hold_segmentation','U01:unresolved_headword_boundary')


class AhoMatcher:
    """Exact substring locator, not a Japanese tokenizer or sense disambiguator."""
    def __init__(self,terms):
        self.next=[{}];self.fail=[0];self.out=[[]]
        for i,t in enumerate(terms):
            s=0
            for c in t:
                nxt=self.next[s]
                if c not in nxt:
                    nxt[c]=len(self.next)
                    self.next.append({});self.fail.append(0);self.out.append([])
                s=nxt[c]
            self.out[s].append(i)
        q=deque(self.next[0].values())
        while q:
            v=q.popleft()
            for c,u in self.next[v].items():
                q.append(u)
                f=self.fail[v]
                while f and c not in self.next[f]:f=self.fail[f]
                self.fail[u]=self.next[f].get(c,0)
                self.out[u].extend(self.out[self.fail[u]])
    def iter_hits(self,text):
        s=0
        for pos,c in enumerate(text):
            while s and c not in self.next[s]:s=self.fail[s]
            s=self.next[s].get(c,0)
            for i in self.out[s]:yield pos,i


def likely_embedded_in_compound(text:str,end_pos:int,term:str)->bool:
    """Conservative character-neighbor hint, NOT lexical segmentation."""
    beg=end_pos-len(term)+1
    before=text[beg-1] if beg>0 else ''
    after=text[end_pos+1] if end_pos+1<len(text) else ''
    # A prefix character joined to a kanji word (e.g. 不 + 完全性定理) or
    # a kanji suffix joined to it means we saw a substring, not an independent headword.
    if before and KANJI.search(before) and (KANJI.search(term[0]) or KATA.search(term[0])):return True
    if after and KANJI.search(after) and (KANJI.search(term[-1]) or KATA.search(term[-1])):return True
    if before and KATA.search(before) and KATA.search(term[0]):return True
    if after and KATA.search(after) and KATA.search(term[-1]):return True
    if before and before.isascii() and before.isalnum() and term[0].isascii():return True
    if after and after.isascii() and after.isalnum() and term[-1].isascii():return True
    return False


def attest(decisions: list[dict],src:zipfile.ZipFile, inventory:dict):
    indices=[i for i,x in enumerate(decisions) if x['candidate_status'] in ('provisional_defined','headword_candidate','headword_seed')]
    terms=[decisions[i]['term'] for i in indices]
    matcher=AhoMatcher(terms)
    samples={};lines_matched=Counter();matched_primary=Counter();independent_like=Counter()
    data=sorted((v for v in inventory['files'] if v['read_for_creation']),key=lambda v:(v['reading_layer']!='japanese_original_prose',v['path']))
    read_bytes=0;scanned_lines=0;max_hits=0
    for info in data:
        path=info['path']
        if path=='GLOSSARY.md' or 'Private' in path:raise ValueError('Excluded file in inventory read')
        b=src.read('Scientific-Ontology/'+path)
        if hashlib.sha256(b).hexdigest()!=info['sha256']:raise ValueError('Source bytes changed: '+path)
        read_bytes+=len(b)
        text=b.decode('utf-8-sig',errors='replace')
        for line_no,line in enumerate(text.splitlines(),1):
            scanned_lines+=1
            if not JP.search(line) and not re.search(r'[A-Za-z]',line):continue
            found={}
            for pos,li in matcher.iter_hits(line):
                t=terms[li]
                embedded=likely_embedded_in_compound(line,pos,t)
                # Prefer a plausible whole-term occurrence over an embedded one.
                if li not in found or (found[li][1] and not embedded): found[li]=(pos,embedded)
            max_hits=max(max_hits,len(found))
            for li,(pos,embedded) in found.items():
                idx=indices[li];lines_matched[idx]+=1
                if info['reading_layer']=='japanese_original_prose':matched_primary[idx]+=1
                if not embedded:independent_like[idx]+=1
                existing=samples.setdefault(idx,[])
                same_doc=next((v for v in existing if v['source_path']==path),None)
                if same_doc and (not same_doc['embedded_in_larger_surface'] or embedded):continue
                if same_doc:existing.remove(same_doc)
                if len(existing)>=3:
                    if embedded or not any(x['embedded_in_larger_surface'] for x in existing):continue
                    first_embedded=next(k for k,x in enumerate(existing) if x['embedded_in_larger_surface'])
                    existing.pop(first_embedded)
                tt=terms[li];first=max(0,pos-len(tt)+1);start=max(0,first-52);end=min(len(line),pos+53)
                excerpt=line[start:end].replace('\t',' ')
                existing.append({'source_path':path,'line':line_no,'source_layer':info['reading_layer'],
                                 'excerpt':excerpt,'embedded_in_larger_surface':embedded,
                                 'match_status':'character_context_hint_not_true_token_segmentation'})
    side=[]
    for i in indices:
        rec=decisions[i]
        side.append({'term':rec['term'],'evidence_key':rec['evidence_key'],
                     'substring_matching_lines':lines_matched.get(i,0),
                     'whole_term_like_char_context_lines':independent_like.get(i,0),
                     'primary_japanese_matching_lines':matched_primary.get(i,0),
                     'examples':samples.get(i,[]),
                     'evidence_scope':'up_to_three_distinct_documents; character-neighbor hint, not token or sense verification'})
    return side,{'scanned_docs':len(data),'scanned_lines':scanned_lines,'scanned_utf8_bytes':read_bytes,
                 'matching_trie_nodes':len(matcher.next),'max_distinct_matching_candidates_in_line':max_hits,
                 'headwords_with_any_literal_source_examples':sum(bool(v['examples']) for v in side),
                 'headwords_with_at_least_one_whole_term_like_character_context':sum(v['whole_term_like_char_context_lines']>0 for v in side)}

def html_viewer(decisions, entries, source_by_term, summary):
    labels={'general':'一般用語','so':'SO用語','technical':'テクニカルターム'}
    definition={d['term']:d['definition'] for d in entries if d.get('definition')}
    view_order=sorted(decisions,key=lambda r:(r['review_priority'],r['term']))
    data=[[r['term'],r['group'] or '',r['candidate_status'],r['definition_status'],
           r['technical_adjacency'],','.join(r['borrowed_domain_candidates']),
           definition.get(r['term'],''),','.join(r['rules']),
           r['literal_observations'] or 0, bool(source_by_term.get(r['term'],{}).get('examples'))]
          for r in view_order]
    safe=json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')
    stats=json.dumps({'total':len(decisions),'states':summary['candidate_status_counts'],'groups':summary['headword_group_counts']},ensure_ascii=False,separators=(',',':'))
    return '''<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>SO Repository 全域辞書：見出し語分類と既存暫定定義</title>
<style>
:root{color-scheme:light;font-family:system-ui,'Noto Sans JP',sans-serif;background:#f6f8fb;color:#172235}
body{max-width:1290px;margin:auto;padding:22px}.panel{background:white;border:1px solid #dbe4ee;border-radius:12px;padding:18px;margin:16px 0}
h1{font-size:1.7rem;line-height:1.4}p{line-height:1.75}label{display:inline-flex;gap:7px;align-items:center;margin:6px}
input[type=search]{width:min(98%,360px);padding:10px;font-size:1rem;border:1px solid #c6d4e0;border-radius:8px}
select,button{padding:10px;border:1px solid #c6d4e0;border-radius:8px;background:white;color:#172235}
button{cursor:pointer}table{width:100%;border-collapse:collapse;font-size:.92rem}th{background:#edf3f9;text-align:left}td,th{padding:10px;border-bottom:1px solid #e2eaf2;vertical-align:top}
.term{font-weight:700}.small{font-size:.8rem;color:#516174}.alert{color:#8e4520;font-weight:700}
.long{max-width:550px;line-height:1.6}.badge{display:inline-block;padding:2px 8px;border-radius:6px;background:#e7f0fc}
.count{font-weight:700}#out-count{margin:12px}details{margin-top:8px}summary{cursor:pointer}a{color:#28509a}
@media(max-width:700px){table{display:block;overflow:auto}td{min-width:105px}.long{min-width:260px}body{padding:10px}}
</style></head><body>
<h1>SO Repository 全域辞書｜見出し語分類と暫定定義</h1>
<div class="panel"><p>27,901件の<strong>元の表記候補を全件残した</strong>検査用閲覧版。<strong>SO用語／一般用語／テクニカルターム</strong>は暫定分類です。文法・句・断片・未確定も検索できます。<strong>専門近接</strong>は警告であり、外部学説とSOの対応の承認ではありません。</p>
<p class="small">主分類は見出し語の現在の扱い。普通語をSOが独自に使う場合、一般語との二義性が残ります。既存の定義はLLM草案であり、人間による内容承認を意味しません。原文出典は辞書本文ではなく別台帳にあります。</p>
<div id="global-stats"></div></div>
<div class="panel"><input type="search" id="q" placeholder="語・定義・判定理由を検索" aria-label="検索">
<label>主分類<select id="group"><option value="">すべて</option><option value="general">一般用語</option><option value="so">SO用語</option><option value="technical">テクニカルターム</option><option value="other">保留・対象外</option></select></label>
<label>収録段階<select id="status"><option value="">すべて</option><option value="provisional_defined">既存草案</option><option value="headword_seed">新規編集候補</option><option value="headword_candidate">見出し候補・定義未作成</option><option value="other">文法・保留・対象外</option></select></label>
<label><input type="checkbox" id="near">専門近接だけ</label>
<button id="reset">条件クリア</button><div id="out-count"></div>
<div style="overflow-x:auto"><table><thead><tr><th>見出し／表記</th><th>主分類</th><th>状態・警告</th><th>定義案・判定経路</th></tr></thead><tbody id="tbody"></tbody></table></div>
<p><button id="more">さらに200件</button></p></div>
<script id="payload" type="application/json">'''+safe+'''</script>
<script>
const D=JSON.parse(document.getElementById('payload').textContent);
const STATS='''+stats+''';
const names={general:'一般用語',so:'SO用語',technical:'テクニカルターム'};
const states={provisional_defined:'既存暫定定義',headword_seed:'新規編集候補',headword_candidate:'見出し候補',grammar_not_dictionary:'文法へ',nonheadword_notation:'記号等',hold_fragment:'断片保留',hold_grammar_or_fragment:'かな・文法保留',hold_segmentation:'語分割保留',hold_clause_or_example:'文・例保留',hold_quoted_context:'引用保留',hold_identifier_or_compound:'識別子・複合保留'};
const el=x=>document.getElementById(x);
let matched=D,shown=0;
function txt(s){const x=document.createElement('span');x.textContent=String(s);return x.outerHTML}
function render(reset){if(reset){el('tbody').textContent='';shown=0};const n=Math.min(matched.length,shown+200);let buf='';
for(let i=shown;i<n;i++){let r=matched[i];let warnings=r[4]?'<span class="alert">専門近接：'+txt(r[5])+'</span>':'';
let def=r[6]?txt(r[6]):'<span class="small">定義未作成・未承認</span>';
buf+='<tr><td class="term">'+txt(r[0])+'</td><td><span class="badge">'+txt(names[r[1]]||'保留・対象外')+'</span></td><td>'+txt(states[r[2]]||r[2])+'<br>'+warnings+'</td><td class="long">'+def+'<details><summary>判定規則・出現数</summary><span class="small">'+txt(r[7])+' ／ 元台帳観測 '+r[8]+' ／ 原文例 '+(r[9]?'あり':'未検出')+'</span></details></td></tr>';}
el('tbody').insertAdjacentHTML('beforeend',buf);shown=n;el('more').hidden=shown>=matched.length;el('out-count').textContent='表示 '+shown+' / '+matched.length+' 件（元の候補は '+D.length+' 件）'}
function filter(){let q=el('q').value.trim().toLowerCase(),g=el('group').value,s=el('status').value,near=el('near').checked;
matched=D.filter(r=>(!q||[r[0],r[5],r[6],r[7]].some(x=>String(x).toLowerCase().includes(q))) && (!g||(g==='other'?!r[1]:r[1]===g)) && (!s||(s==='other'?!['provisional_defined','headword_seed','headword_candidate'].includes(r[2]):r[2]===s)) && (!near||r[4]));render(true)}
for (let x of ['q','group','status','near'])el(x).addEventListener(x==='q'?'input':'change',filter);
el('more').addEventListener('click',()=>render(false));el('reset').addEventListener('click',()=>{el('q').value='';el('group').value='';el('status').value='';el('near').checked=false;filter()});
el('global-stats').textContent='全表記 '+STATS.total+' 件／暫定見出し分類 '+Object.entries(STATS.groups).map(([g,v])=>(names[g]||g)+' '+v+'件').join('、');filter();
</script></body></html>\n'''


def build(args):
    t0=time.perf_counter()
    dz=pathlib.Path(args.dictionary_zip); rz=pathlib.Path(args.source_zip)
    if sha256_file(dz)!=DICT_SHA:raise ValueError('Dictionary source ZIP SHA mismatch')
    if sha256_file(rz)!=RC008_SHA:raise ValueError('rc008 source ZIP SHA mismatch')
    rules=json.loads(pathlib.Path(args.rules).read_text(encoding='utf-8'))
    with zipfile.ZipFile(dz) as z:
        raw=read_jsonl(member(z,'all_japanese_surface_candidates.jsonl'))
        defs={v['term']:v for v in read_jsonl(member(z,'dictionary_reviewed.jsonl'))}
        inventory=json.loads(member(z,'provenance/source_inventory.json'))
        assert inventory['source_archive_sha256']==RC008_SHA
        literal=read_jsonl(member(z,'unreviewed_literal_definition_candidates.jsonl'))
    if len(raw)!=27901 or len(defs)!=1365:raise ValueError('Unexpected source inventory cardinality')
    decisions=[classify(v['term'],v,defs,rules) for v in raw]
    if len(set(x['term'] for x in decisions))!=len(raw):raise ValueError('Duplicate input surface')
    dmap={x['term']:x for x in decisions}
    missing_dict=set(defs)-set(dmap)
    if missing_dict:raise ValueError(f'Existing drafts absent from raw registry: {len(missing_dict)}')
    entries=[]
    for t,v in sorted(defs.items()):
        r=dmap[t]
        if r['candidate_status']=='grammar_not_dictionary':continue
        entries.append({'term':t,'group':r['group'],'group_ja':r['group_ja'],'definition':v.get('definition'),
                        'senses':v.get('senses',[]),'notes':v.get('notes',[]),
                        'technical_adjacency':r['technical_adjacency'],
                        'borrowed_domain_candidates':r['borrowed_domain_candidates'],
                        'source':'prior_assistant_editorial_draft','definition_status':'unreviewed_provisional_not_canonical'})
    for t,defn in sorted(rules['editorially_new_definitions'].items()):
        if t in defs:continue
        r=dmap.get(t)
        if not r or r['candidate_status'] not in ('headword_seed','headword_candidate'):continue
        entries.append({'term':t,'group':r['group'],'group_ja':r['group_ja'],'definition':defn,
                        'senses':[],'notes':['専門分野の標準語義と原文のSO用法の個別照合は未完了。'],
                        'technical_adjacency':r['technical_adjacency'],
                        'borrowed_domain_candidates':r['borrowed_domain_candidates'],
                        'source':'new_assistant_cautious_editorial_seed','definition_status':'unreviewed_provisional_not_canonical'})
    entries.sort(key=lambda x:(x['group'] or '',x['term']))
    with zipfile.ZipFile(rz) as z:
        evidence, scanstats=attest(decisions,z,inventory)
    evidence_by_term={x['term']:x for x in evidence}
    groups=Counter(x['group'] for x in decisions if x['candidate_status'] in ('provisional_defined','headword_candidate','headword_seed'))
    states=Counter(x['candidate_status'] for x in decisions)
    candidate_count=sum(x['candidate_status'] in ('provisional_defined','headword_candidate','headword_seed') for x in decisions)
    by_kind=Counter(k for x in raw for k in x['surface_kinds'])
    technical_alert_count=sum(x['technical_adjacency'] for x in decisions)
    summary={
      'status':'AI exploratory; human semantic review and canonical adoption not done',
      'dictionary_source_sha256':DICT_SHA,'rc008_source_sha256':RC008_SHA,
      'excluded_generation_inputs':['GLOSSARY.md','99_Private_Core_Not_Included/README.md'],
      'source_registry_unique':len(raw),'all_source_surfaces_accounted_for':len(decisions)==len(raw),
      'previous_assistant_definitions':len(defs),'previous_definitions_not_canonically_adopted':True,
      'new_definitions_included':sum(x['source']=='new_assistant_cautious_editorial_seed' for x in entries),
      'all_provisional_dictionary_entries':len(entries),
      'candidate_status_counts':dict(sorted(states.items())),
      'headword_candidate_total':candidate_count,
      'candidate_review_priority_counts':dict(sorted(Counter(x['review_priority'] for x in decisions).items())),
      'headword_group_counts':dict(sorted(groups.items())),
      'technical_nearby_in_all_surfaces':technical_alert_count,
      'technical_nearby_among_candidate_headwords':sum(x['technical_adjacency'] and x['candidate_status'] in ('provisional_defined','headword_candidate','headword_seed') for x in decisions),
      'source_surface_kinds':dict(sorted(by_kind.items())),
      'unreviewed_literal_definition_candidates_count':len(literal),
      'seed_count_so':len(rules['so_exact']),
      'seed_count_technical':len(rules['technical_exact']),
      'additional_editorial_seed_count':len(rules['editorially_new_definitions']),
      'additional_editorial_seed_not_in_registry':[t for t in rules['editorially_new_definitions'] if t not in dmap],
      'scan':scanstats,
      'all_27901_semantically_read_one_by_one':False,
      'automated_japanese_morphological_analysis':False,
      'external_field_definitions_verified_against_external_sources':False,
      'headword_grouping_is_not_imported_term_equivalence':True,
      'source_evidence_is_substring_not_semantic_validation':True,
      'source_pointers_in_dictionary_body':False,
      'human_approval_of_entries':False,
    }
    out=pathlib.Path(args.out);out.mkdir(parents=True,exist_ok=True)
    write_jsonl(out/'all_surface_headword_decisions.jsonl',decisions)
    write_jsonl(out/'categorized_dictionary_entries.jsonl',entries)
    write_jsonl(out/'source_attestation_sidecar.jsonl',evidence)
    watchlist=[]
    for r in decisions:
        if r['candidate_status'] in ('provisional_defined','headword_candidate','headword_seed') and (r['group']=='technical' or r['technical_adjacency']):
            info=evidence_by_term.get(r['term'],{})
            watchlist.append({'term':r['term'],'primary_group':r['group'],'group_ja':r['group_ja'],
                              'borrowed_field_candidates':r['borrowed_domain_candidates'],
                              'technical_boundary_alerts':r['technical_boundary_alerts'],
                              'candidate_status':r['candidate_status'],
                              'standalone_like_context_lines':info.get('whole_term_like_char_context_lines',0),
                              'example_source_reference':info.get('examples',[])[:1],
                              'external_comparison_result':'not_verified',
                              'so_to_external_equivalence':'not_asserted'})
    write_jsonl(out/'technical_proximity_watchlist.jsonl',watchlist)
    with (out/'headword_candidates.tsv').open('w',encoding='utf-8',newline='\n') as f:
        headers=['term','group_ja','candidate_status','review_priority','confidence','definition_status','technical_adjacency','borrowed_domain_candidates','source_registry_status','literal_observations','rules']
        f.write('\t'.join(headers)+'\n')
        for r in decisions:
            if r['candidate_status'] not in ('provisional_defined','headword_candidate','headword_seed'):continue
            vals=[r['term'],r['group_ja'],r['candidate_status'],r['review_priority'],r['confidence'],r['definition_status'],
                  '1' if r['technical_adjacency'] else '0',','.join(r['borrowed_domain_candidates']),
                  r['source_registry_status'],str(r['literal_observations'] or ''),','.join(r['rules'])]
            f.write('\t'.join(str(x).replace('\t',' ').replace('\n',' ') for x in vals)+'\n')
    write_json(out/'classification_coverage.json',summary)
    with (out/'dictionary_viewer.html').open('w',encoding='utf-8',newline='\n') as f:f.write(html_viewer(decisions,entries,evidence_by_term,summary))
    elapsed=time.perf_counter()-t0
    try:
        import resource
        mem=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024
        cpu=resource.getrusage(resource.RUSAGE_SELF).ru_utime+resource.getrusage(resource.RUSAGE_SELF).ru_stime
    except ImportError:mem=None;cpu=None
    metrics={'wall_seconds':round(elapsed,3),'process_cpu_seconds':round(cpu,3) if cpu is not None else None,
             'peak_rss_mib':round(mem,1) if mem is not None else None,
             'original_zip_bytes':dz.stat().st_size+rz.stat().st_size,
             'output_bytes':sum((out/n).stat().st_size for n in OUTS),
             'external_llm_api_calls':0,
             'note':'Deterministic Python routing and substring attestation. Conversational model editorial effort and inference tokens unavailable.'}
    write_json(out/'runtime_metrics.json',metrics)
    print(json.dumps({'summary':summary,'runtime':metrics},ensure_ascii=False,indent=2))


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--dictionary-zip',required=True)
    p.add_argument('--source-zip',required=True)
    p.add_argument('--out',required=True)
    p.add_argument('--rules',default=str(RULES_DEFAULT))
    args=p.parse_args();build(args)
if __name__=='__main__':main()

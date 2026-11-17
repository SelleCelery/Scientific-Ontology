#!/usr/bin/env python3
"""Build a portable, unapproved 1,500-entry SO navigator dictionary from existing drafts.

The current v6 Navigator format has NOT been adopted: outputs are a v5.2 research
handoff/portable import candidate, not a change to canonical terminology.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import html
import io
import json
import re
from collections import Counter
from pathlib import Path

BASE = Path('tools/assessment/term_dictionary/corpus_lexicon_classification')
DEST = Path('tools/assessment/term_dictionary/navigator_seed')
SOURCE_SHA = 'bcf56409d091a67b8314fce5ac6e0676a7bc79e23d517b92ac56138595ae166e'
CLASS_LABEL = {'general': '一般用語', 'so': 'SO用語', 'technical': 'テクニカルターム'}
# Candidate proximity, never a claim that SO and an imported discipline are equivalent.
NEW_ADJACENCY_CANDIDATES = {
    '境界インターフェース': ['情報技術'],
    '境界プロトコル': ['情報技術'],
    '通約プロトコル': ['情報技術'],
    '認識軸生成モデル': ['認知科学'],
    '意味経験キャパシタ': ['電気・回路工学'],
    'フラクタル監査': ['数学・フラクタル幾何'],
    'ビッグバン境界': ['宇宙論'],
    'ボソン履歴': ['量子場理論'],
    'ポート境界': ['情報技術・通信工学'],
    '境界ノイズ論': ['情報理論'],
    '境界エントロピー': ['熱力学', '情報理論'],
    '境界膜クオリア': ['心の哲学・認知科学'],
    '境界制御モデル': ['制御理論'],
    '履歴トポロジー': ['数学・位相', '物理学・対応図式'],
    '時間レンダリング': ['物理学・時間'],
    '監査ポート': ['情報技術・通信工学'],
    '境界通信モデル': ['通信工学'],
    '履歴ロック': ['物理学・固定モデル'],
}

ADDED_STATUS = 'assistant_new_draft_unreviewed'
EXISTING_STATUS = 'assistant_inherited_draft_unreviewed'
OUTPUT_FILES = [
    'dictionary_1500.json', 'dictionary_1500.jsonl', 'dictionary_1500.tsv',
    'dictionary_demo.html', 'dictionary_quality.json',
]


def dump_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8', newline='\n') as fh:
        fh.write(value.rstrip('\n') + '\n')


def jd(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def read_jsonl(path: Path):
    with path.open('r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                yield json.loads(line)


def load_additions(path: Path):
    # Accept a user-editable TSV as an alternative to the installed JSONL.
    if path.suffix == '.tsv':
        with path.open(encoding='utf-8', newline='') as f:
            return list(csv.DictReader(f, delimiter='\t'))
    return list(read_jsonl(path))


def prepare(entries_path: Path, attestation_path: Path, additions_path: Path):
    original = list(read_jsonl(entries_path))
    addition = load_additions(additions_path)
    assert len(original) == 1387, f'expecting frozen 1387 base entries, got {len(original)}'
    assert len(addition) == 113, f'expecting 113 additions, got {len(addition)}'
    unique = {x['term'] for x in original + addition}
    assert len(unique) == 1500, f'entries are not unique: {len(unique)}'
    evidence = {}
    for row in read_jsonl(attestation_path):
        if row['term'] in unique:
            evidence[row['term']] = row
    result = []
    for row in original:
        result.append(_entry(row, False, evidence.get(row['term'])))
    for row in addition:
        result.append(_entry(row, True, evidence.get(row['term'])))
    result.sort(key=lambda r: r['term'].casefold())
    assert sum(bool(e['definition']) for e in result) == 1500
    assert all(e['authority'] == 'unreviewed_editorial' for e in result)
    return result


def _entry(row, newly_written, evidence):
    term = row['term'].strip()
    definition = row['definition'].strip()
    group = row['group']
    if group not in CLASS_LABEL: raise ValueError('unknown category for ' + term)
    if len(definition) < 12: raise ValueError('definition suspiciously short: ' + term)
    examples = []
    for it in (evidence or {}).get('examples', [])[:3]:
        if it.get('source_path') and isinstance(it.get('line'), int):
            examples.append({
                'path': it['source_path'], 'line': it['line'],
                'excerpt': it.get('excerpt', '')[:280],
                'source_layer': it.get('source_layer', 'unknown'),
                'evidence_status': 'surface_context_only_not_sense_verification',
            })
    note = row.get('usage_note', '') if newly_written else ' '.join(row.get('notes', []))
    nearby = NEW_ADJACENCY_CANDIDATES.get(term, []) if newly_written else row.get('borrowed_domain_candidates', [])
    adj = (group == 'technical' or bool(nearby)) if newly_written else bool(row.get('technical_adjacency', False))
    return {
        'id': 'term_' + hashlib.sha256(term.encode('utf-8')).hexdigest()[:14],
        'term': term,
        'reading': None, # reading / furigana will require separate pronunciation review
        'aliases': [], # do NOT invent Japanese/English equivalent forms
        'group': group,
        'group_ja': CLASS_LABEL[group],
        'definition': definition,
        'usage_note': note.strip(),
        'status': ADDED_STATUS if newly_written else EXISTING_STATUS,
        'authority': 'unreviewed_editorial',
        'technical_adjacency': adj,
        'borrowed_domain_candidates': nearby,
        'external_definition_verified': False,
        'source_snapshot_sha256': SOURCE_SHA,
        'source_attestations': examples,
        'source_evidence_scope': 'source excerpts show term-like string context; not proof of sense or definition',
    }


def make_html(entries):
    # Embedded JSON makes offline preview usable without a local server or browser fetch.
    client = [{k:e[k] for k in ('term','group','group_ja','definition','usage_note','status','technical_adjacency','borrowed_domain_candidates','source_attestations')} for e in entries]
    data = json.dumps(client, ensure_ascii=False, separators=(',', ':'))
    data = data.replace('&', '\\u0026').replace('<','\\u003c').replace('>','\\u003e').replace('\u2028', '\\u2028')
    page = r'''<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>存在境界論 1,500語 辞書の試験表示</title>
<style>
:root{font-family:system-ui,"Yu Gothic UI","Hiragino Kaku Gothic ProN",sans-serif;color:#253149;background:#f1f5f9}
*{box-sizing:border-box}body{margin:0}header{background:linear-gradient(130deg,#16263e,#284f78);color:#fff;padding:30px max(24px,calc((100vw - 1100px)/2))}header h1{font-size:26px;margin:0 0 8px}header p{opacity:.86;line-height:1.7;margin:0}main{max-width:1110px;margin:26px auto;padding:0 17px}.toolbar{background:#fff;padding:15px;border-radius:12px;box-shadow:0 6px 18px #253a5414;display:flex;gap:12px;flex-wrap:wrap}.toolbar input,.toolbar select{border:1px solid #cbd5e1;border-radius:8px;padding:11px 13px;font-size:15px;flex:1;min-width:180px}.counter{font-size:13px;color:#566781;margin:14px 0}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:12px}.card{background:#fff;padding:16px 17px;border-radius:11px;border:1px solid #e1e7ef;line-height:1.72;cursor:pointer}.card:hover{box-shadow:0 5px 17px #20365d16;border-color:#a4bad4}.card h3{font-size:17px;margin:0 0 5px}.tag{font-size:11px;border-radius:99px;padding:3px 8px;margin-left:7px;color:#125380;background:#e5f2fa}.tag.so{background:#ede9fe;color:#5b3bab}.tag.technical{background:#fff0dc;color:#8d5200}.definition{margin:0;color:#374458;font-size:14px}.note{font-size:12px;color:#59677d}.explainer{background:#fff;border:1px solid #dfebf5;border-radius:12px;padding:16px 20px;margin-bottom:19px;line-height:1.9}.explainer strong{color:#244f85}.demo{background:#eaf3fc;border-left:3px solid #3b79b7;padding:14px;border-radius:6px;line-height:2.2;user-select:text}.modal{position:fixed;z-index:200;max-width:410px;min-width:290px;max-height:70vh;overflow:auto;background:white;color:#28344b;border:1px solid #8da8c5;border-radius:11px;padding:18px;box-shadow:0 16px 45px #0b24444f;display:none}.modal h2{font-size:19px;margin:0}.modal .close{float:right;border:0;background:#edf2fa;color:#43597b;padding:4px 9px;border-radius:6px;cursor:pointer}.modal p{line-height:1.78}.modal small{color:#6a7c92}.modal details{font-size:12px;margin-top:9px;word-break:break-all}.modal summary{cursor:pointer}.pages{display:flex;gap:8px;margin:20px 0}.pages button{padding:9px 16px;background:white;border:1px solid #cad5e2;border-radius:7px;cursor:pointer}.warn{font-size:12px;color:#60728c;margin:10px 0}
</style></head><body>
<header><h1>存在境界論｜辞書1500項目・試験表示</h1><p>v5.2を基礎資料とする編集草案。v6 Navigatorの確定UIではありません。意味と専門語の対応は未承認です。</p></header>
<main><div class="explainer"><strong>右クリック参照のデモ</strong>：下の文章中で語を選択して右クリックするか、語の上で右クリックすると、辞書ポップアップを表示します。普通のページ操作を妨げないよう、デモ領域だけで動作します。<div class="demo" id="demo">境界への接触によって形成された履歴は、探索資源を変える。認識ブリッジを通じて通約するとき、量子エンタングルメントや相対性理論の専門語との区別も必要となる。α監査とβ監査は、現在の論理構造とその後続条件を異なる位置から調べる。</div></div>
<div class="toolbar"><input id="query" placeholder="用語または定義文で検索（例：境界、AI、履歴）" aria-label="検索語"><select id="category"><option value="all">全分野</option><option value="general">一般用語</option><option value="so">SO用語</option><option value="technical">テクニカルターム</option></select></div>
<div class="counter" id="count"></div><div id="cards" class="grid"></div><div class="pages"><button id="prev">前へ</button><button id="next">次へ</button></div>
<div class="warn">各項目はAI作成草案。文書への表面一致は語義の裏付けではなく、正式な正本や他分野との同義性を保証しません。出典位置は移行用の参照ヒントです。</div>
</main><aside id="popup" class="modal" role="dialog" aria-label="用語の解説"></aside>
<script id="dictdata" type="application/json">__DATA__</script>
<script>
'use strict';
const ITEMS=JSON.parse(document.getElementById('dictdata').textContent);
const byTerm=new Map(ITEMS.map(x=>[x.term,x]));
const wordList=Array.from(byTerm.keys()).sort((a,b)=>b.length-a.length);
const query=document.getElementById('query'),category=document.getElementById('category'),cards=document.getElementById('cards'),count=document.getElementById('count'),pop=document.getElementById('popup');
let list=ITEMS,page=0;const PAGE=30;
function node(tag,cls,txt){const e=document.createElement(tag);if(cls)e.className=cls;if(txt!==undefined)e.textContent=txt;return e;}
function render(){const q=query.value.trim().toLocaleLowerCase(),cat=category.value;
  list=ITEMS.filter(x=>(cat==='all'||x.group===cat)&&(!q||x.term.toLocaleLowerCase().includes(q)||x.definition.toLocaleLowerCase().includes(q)));if(page*PAGE>=list.length)page=0;
  cards.replaceChildren();count.textContent=`${list.length.toLocaleString()}件表示・${Math.floor(page)+1}ページ目（全${Math.ceil(list.length/PAGE)||1}ページ）`;
  for(const x of list.slice(page*PAGE,(page+1)*PAGE)){const a=node('article','card'),h=node('h3','',x.term),badge=node('span','tag '+x.group,x.group_ja);h.append(badge);a.append(h,node('p','definition',x.definition));a.addEventListener('click',ev=>show(x,ev.clientX,ev.clientY));cards.append(a);}}
function show(x,clientX,clientY){pop.replaceChildren();const b=node('button','close','閉じる');b.addEventListener('click',()=>pop.style.display='none');pop.append(b,node('h2','',x.term));pop.append(node('small','',x.group_ja+'｜AI編集草案・未審理'+(x.technical_adjacency?'｜専門用語への近接注意':'')));pop.append(node('p','',x.definition));
  if(x.usage_note)pop.append(node('p','note','注意：'+x.usage_note));const src=x.source_attestations||[];
  if(src.length){const det=node('details');det.append(node('summary','',`原文への参照候補（${src.length}件）`));for(const s of src)det.append(node('p','note',`${s.path}:${s.line}｜${s.excerpt}`));pop.append(det);}
  pop.style.display='block';const w=pop.offsetWidth,h=pop.offsetHeight;pop.style.left=Math.max(10,Math.min(clientX+8,innerWidth-w-10))+'px';pop.style.top=Math.max(10,Math.min(clientY+8,innerHeight-h-10))+'px';}
function isAscii(c){return /[A-Za-z0-9_]/.test(c||'');}
function exactFind(t){return byTerm.get(t)||byTerm.get(t.trim());}
function atPoint(ev){let caret=null;
  if(document.caretRangeFromPoint)caret=document.caretRangeFromPoint(ev.clientX,ev.clientY);
  else if(document.caretPositionFromPoint){const a=document.caretPositionFromPoint(ev.clientX,ev.clientY);if(a)caret={startContainer:a.offsetNode,startOffset:a.offset};}
  if(!caret||caret.startContainer.nodeType!==3)return null;
  const text=caret.startContainer.textContent,offset=caret.startOffset;
  for(const t of wordList){if(t.length<2)continue;let at=text.indexOf(t);while(at>=0){if(at<=offset&&offset<=at+t.length){if(isAscii(t[0])&&isAscii(text[at-1]))break;if(isAscii(t[t.length-1])&&isAscii(text[at+t.length]))break;return byTerm.get(t);}at=text.indexOf(t,at+1);}}
  return null;}
query.addEventListener('input',()=>{page=0;render()});category.addEventListener('change',()=>{page=0;render()});
document.getElementById('prev').addEventListener('click',()=>{page=Math.max(0,page-1);render();window.scrollTo({top:460,behavior:'smooth'})});
document.getElementById('next').addEventListener('click',()=>{page=Math.min(Math.max(0,Math.ceil(list.length/PAGE)-1),page+1);render();window.scrollTo({top:460,behavior:'smooth'})});
document.getElementById('demo').addEventListener('contextmenu',ev=>{const sel=String(window.getSelection()).trim();const x=exactFind(sel)||atPoint(ev);if(x){ev.preventDefault();show(x,ev.clientX,ev.clientY);}});
document.addEventListener('keydown',e=>{if(e.key==='Escape')pop.style.display='none'});
document.addEventListener('pointerdown',e=>{if(pop.style.display==='block'&&!pop.contains(e.target)&&!e.target.closest('.card'))pop.style.display='none'});
render();
</script></body></html>
'''
    return page.replace('__DATA__', data)


def build(entries_path: Path, attestation_path: Path, additions_path: Path, out: Path):
    entries=prepare(entries_path,attestation_path,additions_path)
    out.mkdir(parents=True,exist_ok=True)
    package={
        'schema_version': '0.1.0-provisional',
        'purpose':'portable dictionary data for later v6 navigator integration; not adopted v6 interface',
        'source_corpus': 'Scientific-Ontology v5.2.0 rc008 archival snapshot',
        'source_snapshot_sha256': SOURCE_SHA,
        'authoritative_status': 'not_approved_not_canonical',
        'entries': entries,
    }
    dump_text(out/'dictionary_1500.json',json.dumps(package,ensure_ascii=False,sort_keys=True,indent=2))
    dump_text(out/'dictionary_1500.jsonl','\n'.join(jd(x) for x in entries))
    io_s=io.StringIO(newline='')
    writer=csv.writer(io_s,delimiter='\t',lineterminator='\n')
    writer.writerow(['id','term','group','group_ja','definition','usage_note','status','evidence_path','evidence_line'])
    for e in entries:
        ex=e['source_attestations'][0] if e['source_attestations'] else {}
        writer.writerow([e['id'],e['term'],e['group'],e['group_ja'],e['definition'],e['usage_note'],e['status'],ex.get('path',''),ex.get('line','')])
    dump_text(out/'dictionary_1500.tsv',io_s.getvalue())
    dump_text(out/'dictionary_demo.html',make_html(entries))
    stat=Counter(e['group'] for e in entries)
    evid=sum(bool(e['source_attestations']) for e in entries)
    qa={
        'total_entries':len(entries),
        'inherited_entry_count':sum(e['status']==EXISTING_STATUS for e in entries),
        'new_definition_count':sum(e['status']==ADDED_STATUS for e in entries),
        'groups':dict(sorted(stat.items())),
        'entries_with_source_surface_examples':evid,
        'technical_adjacency_count':sum(e['technical_adjacency'] for e in entries),
        'entries_without_source_surface_examples':len(entries)-evid,
        'unique_id_count':len({e['id'] for e in entries}),
        'nonempty_definitions':sum(bool(e['definition']) for e in entries),
        'duplicate_headwords':len(entries)-len({e['term'] for e in entries}),
        'confirmed_external_definitions':0,
        'human_reviewed_definitions':0,
        'right_click_demo':'standalone HTML only; v6 integration not performed',
        'source_attestation_caveat':'character/surface hints; term sense and definition not independently verified',
        'v6_schema_adoption':'not_decided',
    }
    dump_text(out/'dictionary_quality.json',json.dumps(qa,ensure_ascii=False,sort_keys=True,indent=2))
    return qa


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--entries',type=Path,default=BASE/'categorized_dictionary_entries.jsonl')
    p.add_argument('--attestations',type=Path,default=BASE/'source_attestation_sidecar.jsonl')
    p.add_argument('--additions',type=Path,default=DEST/'additions_113.jsonl')
    p.add_argument('--out',type=Path,default=DEST)
    args=p.parse_args()
    print(json.dumps(build(args.entries,args.attestations,args.additions,args.out),ensure_ascii=False,sort_keys=True,indent=2))

if __name__=='__main__':main()

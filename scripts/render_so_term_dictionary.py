#!/usr/bin/env python3
"""Render the created dictionary. No source map or reference glossary is read."""
from __future__ import annotations
import argparse
import json
import html
from pathlib import Path
from build_so_term_dictionary import load_lines, dump_json, sha_bytes, assert_no_pointers

HTML = r'''<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>SO 用例形成辞書</title>
<style>
:root{color-scheme:light;--ink:#172d36;--muted:#536871;--line:#d7e0e2;--accent:#116b72;--paper:#f5f8f8}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.8 system-ui,"Yu Gothic",Meiryo,sans-serif}
header{background:#143943;color:white;padding:26px 5vw}header p{margin:5px 0 0;font-size:14px;color:#d1e3e6}h1{font-size:27px;margin:0;letter-spacing:.08em}
.stats{display:flex;gap:24px;flex-wrap:wrap;padding:14px 5vw;background:white;border-bottom:1px solid var(--line);font-size:14px}.stats b{font-size:21px;color:var(--accent)}
.layout{display:grid;grid-template-columns:340px minmax(0,1fr);gap:26px;max-width:1400px;margin:26px auto;padding:0 24px}
aside,.entry{background:white;border:1px solid var(--line);border-radius:12px}aside{padding:18px;height:calc(100vh - 230px);min-height:520px;display:flex;flex-direction:column}
label{font-size:13px;color:var(--muted)}input,select,button{font:inherit}input,select{width:100%;padding:9px;border:1px solid #b5c7cd;border-radius:6px;margin:5px 0 10px;background:white;color:var(--ink)}
.list{overflow:auto;flex:1;margin-top:6px}.item{display:block;width:100%;text-align:left;background:white;border:0;border-bottom:1px solid #edf1f2;padding:8px 9px;cursor:pointer}.item:hover,.item.selected{background:#e9f3f4}.item span{display:block;font-size:12px;color:var(--muted)}
.nav{display:flex;align-items:center;justify-content:space-between;gap:8px;margin-top:8px}.nav button{border:1px solid var(--line);background:white;border-radius:5px;padding:3px 12px}.small{font-size:12px;color:var(--muted)}
.entry{padding:30px 36px;min-height:520px}.entry h2{font-size:30px;margin:5px 0 12px;overflow-wrap:anywhere}.badge{display:inline-block;font-size:12px;padding:2px 9px;border-radius:18px;background:#e6f2f1;color:#175a5a}.definition{font-size:18px;line-height:1.95;padding-bottom:16px;border-bottom:1px solid var(--line)}
h3{font-size:16px;margin:24px 0 10px}blockquote{margin:10px 0;padding:12px 16px;border-left:3px solid #b8ced2;background:#f6f9fa;white-space:pre-wrap;overflow-wrap:anywhere}.sense{margin:12px 0}.sense strong{display:block;color:var(--accent)}.note{padding:10px 14px;background:#faf5e9;font-size:14px;margin:10px 0;border-radius:5px}.empty{color:var(--muted)}details{margin-top:20px;font-size:14px}footer{max-width:1400px;padding:0 24px 25px;margin:auto;font-size:12px;color:var(--muted)}
@media(max-width:850px){.layout{grid-template-columns:1fr;padding:0 14px;gap:16px}aside{height:360px;min-height:0}.entry{padding:20px}header{padding:20px}h1{font-size:23px}.stats{padding:12px 20px;gap:14px}.definition{font-size:17px}}
</style></head><body>
<header><h1>SO 用例形成辞書</h1><p>文例から定義をまとめる。出典ポインタと既存用語集は、ここへ混ぜない。</p></header>
<div class="stats"><div>AI整理の定義 <b id="n-editorial"></b></div><div>未整理の原文定義候補 <b id="n-literal"></b></div><div>用例のみ <b id="n-usage"></b></div></div>
<div class="layout"><aside><label for="q">語・説明を検索</label><input id="q" placeholder="照合、残差、内在時間…" autocomplete="off"><label for="filter">表示する項目</label><select id="filter"><option value="editorial_candidate">AI整理の定義</option><option value="defined">定義・定義候補</option><option value="all">全表記候補（未整理を含む）</option><option value="usage_only">用例のみ</option></select><div id="count" class="small"></div><div id="list" class="list"></div><div class="nav"><button id="prev" aria-label="前ページ">前</button><span id="page" class="small"></span><button id="next" aria-label="次ページ">次</button></div></aside>
<main><article class="entry" id="entry"></article></main></div>
<footer>対象はrc008の日本語本文86文書。生成元へのリンク・出典位置・定義所有者は含めていません。原文本文中の語は残ります。定義は研究用の候補であり、正本の改訂・承認ではありません。表記候補には複合語、機能表現、未分割の文字列、数・記号を含みます。「全項目」は完成した全語辞典を意味しません。</footer>
<script type="application/json" id="payload">__DATA__</script>
<script>
'use strict';
const payload=JSON.parse(document.getElementById('payload').textContent), rows=payload.entries, samples=payload.examples;
const $=id=>document.getElementById(id), labels={editorial_candidate:'文例から整理した定義（AI・未承認）',literal_candidates:'原文の定義候補（未整理）',usage_only:'用例のみ・定義未作成'};
let page=0, current='照合', hits=[];const perPage=60;
for(const [status,id] of [['editorial_candidate','n-editorial'],['literal_candidates','n-literal'],['usage_only','n-usage']])$(id).textContent=rows.filter(r=>r.status===status).length.toLocaleString('ja');
function el(tag,text,cls){const e=document.createElement(tag);if(text!==undefined)e.textContent=text;if(cls)e.className=cls;return e;}
function show(r){current=r.term;const box=$('entry');box.replaceChildren();box.append(el('span',labels[r.status],'badge'),el('h2',r.term));box.append(el('p',r.definition||'この表記は本文に現れますが、独立した定義はまだ作成していません。用例から読み取れる範囲を保持しています。','definition'+(r.definition?'':' empty')));
if(r.senses.length){box.append(el('h3',r.status==='literal_candidates'?'原文に現れた説明候補':'残した用法・差異'));r.senses.forEach(s=>{const d=el('div',undefined,'sense');if(s.label)d.append(el('strong',s.label));d.append(el('p',s.definition));box.append(d);});}
if(r.notes.length){box.append(el('h3','留保'));r.notes.forEach(n=>box.append(el('p',n,'note')));}
const ex=samples[r.term]||[];box.append(el('h3','文例（所在情報なし）'));if(!ex.length)box.append(el('p','用例は別の原文台帳に保持されています。','empty'));else ex.forEach(s=>box.append(el('blockquote',s)));
const detail=el('details'), summary=el('summary','この画面で確認できること');detail.append(summary,el('p','これは作成辞書の閲覧面です。文例本文は読めますが、参照元辞書・source map・版や行の対応は読み込みません。定義候補の妥当性や収束が証明されたわけではありません。未整理の候補には語として切り直す必要のある文字列もあります。'));box.append(detail);
renderList();}
function refresh(){page=0;const q=$('q').value.trim().toLocaleLowerCase(),filter=$('filter').value;
hits=rows.filter(r=>(filter==='all'||filter==='defined'&&r.status!=='usage_only'||r.status===filter)&&(!q||(r.term+' '+(r.definition||'')+' '+r.senses.map(s=>s.definition).join(' ')).toLocaleLowerCase().includes(q)));
renderList();}
function renderList(){const max=Math.max(1,Math.ceil(hits.length/perPage));page=Math.min(page,max-1);$('count').textContent=hits.length.toLocaleString('ja')+' 件';$('page').textContent=(page+1)+' / '+max;$('prev').disabled=page===0;$('next').disabled=page>=max-1;const list=$('list');list.replaceChildren();for(const r of hits.slice(page*perPage,(page+1)*perPage)){const b=el('button',r.term,'item'+(r.term===current?' selected':''));b.append(el('span',labels[r.status]));b.onclick=()=>show(r);list.append(b);}if(!hits.length)list.append(el('p','該当する項目がありません。全表記候補での検索も確認してください。','small'));}
let timer;$('q').addEventListener('input',()=>{clearTimeout(timer);timer=setTimeout(refresh,100)});$('filter').onchange=refresh;$('prev').onclick=()=>{page--;renderList()};$('next').onclick=()=>{page++;renderList()};refresh();show(rows.find(r=>r.term===current)||rows[0]);
</script></body></html>
'''


def render(dictionary: Path, freeze: Path, observations: Path, out_html: Path, out_md: Path | None = None, updates: Path | None = None):
    rows=load_lines(dictionary)
    frozen=json.loads(freeze.read_text(encoding='utf-8'))
    if sha_bytes(dictionary.read_bytes()) != frozen['dictionary_sha256']:
        raise ValueError('Dictionary differs from frozen bytes')
    for r in rows:assert_no_pointers(r)
    # Only sentence text is copied. No counts, identifiers, paths or source roles.
    examples={r['term']:r['examples'][:3] for r in load_lines(observations)}
    if updates is not None:
        for update in load_lines(updates):
            examples[update['term']] = list(dict.fromkeys(update['evidence_texts']))[:5]
    # An editorially created compound may not be a tokenizer headword.
    for r in rows:examples.setdefault(r['term'],[])
    data={'entries':rows,'examples':examples}
    # Source text can contain literal angle brackets; never execute them as markup.
    encoded=json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c').replace('\u2028','\\u2028').replace('\u2029','\\u2029')
    out_html.parent.mkdir(parents=True,exist_ok=True)
    out_html.write_text(HTML.replace('__DATA__',encoded),encoding='utf-8',newline='\n')
    if out_md:
        out_md.parent.mkdir(parents=True,exist_ok=True)
        text=['# SO 用例形成辞書――定義整理稿','',
              '日本語本文86文書を対象に、既存用語集を生成入力へ渡さず作成した研究用の辞書。以下はAIが用例から整理した定義候補であり、正本への採用ではない。',
              '出典の所在、概念所有者、文書間の参照先は別台帳に隔離している。原文に複数の用法があるときは、その差を消さない。',
              '全表記候補と未定義語の用例はHTML・JSONLに収録している。この文書だけが全語の完成辞典ではない。','']
        for r in rows:
            if r['status']!='editorial_candidate':continue
            text.extend(['## '+r['term'],'',r['definition'],''])
            for s in r['senses']:
                text.append(('**'+s['label']+'。** ' if s.get('label') else '')+s['definition']);text.append('')
            for note in r['notes']:text.extend(['留保：'+note,''])
        out_md.write_text('\n'.join(text).rstrip()+'\n',encoding='utf-8',newline='\n')
    return {'dictionary_entries':len(rows),'editorial_entries':frozen['editorial_entries'],'html_bytes':out_html.stat().st_size}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--dictionary',type=Path,required=True);p.add_argument('--freeze',type=Path,required=True)
    p.add_argument('--observations',type=Path,required=True);p.add_argument('--out-html',type=Path,required=True);p.add_argument('--out-md',type=Path);p.add_argument('--updates',type=Path)
    a=p.parse_args();print(json.dumps(render(a.dictionary,a.freeze,a.observations,a.out_html,a.out_md,a.updates),ensure_ascii=False,indent=2))
if __name__=='__main__':main()

#!/usr/bin/env python3
"""Research-only lexical dictionary and perturbation probe for Boundary Epistemological Critique.

Definition-reference and token co-use are lexical evidence, NOT logical support or a
complete Japanese morphological analysis. Textual substitutions are counterfactual.
Pure stdlib and deterministic output, source never modified.
"""
from __future__ import annotations
import argparse
import collections
import csv
import hashlib
import itertools
import json
import re
import statistics
from dataclasses import dataclass
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape

SOURCE_REL = '01_Sat_Truth/Boundary_Epistemological_Critique.ja.md'
NUM_RE = re.compile(r'^(\d+(?:\.\d+)+)[ \t\u3000]+(.+)$')
DEF_RE = re.compile(r'^(.{1,24}?)とは(?:、|，|\s|$)')
# Added as non-defined reference points, not claimed to be canonical definitions.
OPEN_TERMS = (
    '境界', '観測', '判断可能性', '意味', '経験', '条件', '外部入力', '接触',
    '再照合', '一致', '不一致', '分類不能性', '更新', '差分', '記録',
    '有限観測系', '形式空間', '外部', '内部', '残差処理', '理解',
)
# Each lexical experiment rewrites ONE occurrence inside an actual numbered proposition.
# Substitute choices are corpus-used headwords, but are not approved paraphrases.
LEXICAL_EXPERIMENTS = (
    ('0.3', '境界', ('境界', '履歴', '分類')),
    ('7.3', '外部ヒューリスティック', ('外部ヒューリスティック', '内部ヒューリスティック', '言語ゲーム')),
    ('8.1', '残差', ('残差', '履歴', '分類')),
    ('9.5.1', '照合', ('照合', '同期', '分類')),
    ('12.9', '言語ゲーム', ('言語ゲーム', '学問', '理性')),
    ('15.12.1', '同期', ('同期', '分類', '理性')),
)
# Modifier/qualifier deletion trials; deletion may be semantically destructive.
# They do not themselves contain lexicon headwords in this probe.
QUALIFIER_EXPERIMENTS = (
    ('1.2.1', '単なる', '限定・対比'),
    ('7.3', '運用上', '適用条件'),
    ('8.1', 'だけでなく', '対比・包含'),
    ('9.5.1', 'まだ', '未確定性'),
    ('10.5.1', '特定の', '範囲制限'),
    ('15.12.1', '次の', '時間・継続'),
)
QUERIES = (
    ('知る', '照合'), ('知る', '履歴'), ('知る', '分類'),
    ('照合', '履歴'), ('残差', '同期'), ('通約', '学問'),
    ('認識', '分類'), ('同期', '言語ゲーム'),
)

@dataclass(frozen=True)
class Proposition:
    num: str
    body: str
    line: int


def extract_props(source: Path):
    records = []
    for i, line in enumerate(source.read_text(encoding='utf-8-sig').splitlines(), 1):
        m = NUM_RE.match(line)
        if m:
            records.append(Proposition(m.group(1), m.group(2).strip(), i))
    nums = [p.num for p in records]
    if len(nums) != len(set(nums)):
        raise ValueError('duplicate proposition numbers')
    return {p.num: p for p in records}


def def_head(body: str):
    m = DEF_RE.match(body)
    if not m:
        return None
    head = m.group(1)
    if (head.endswith('こと') or head.endswith('するこ') or
            head.startswith('すべての') or head.startswith('経験を')):
        return None
    if any(c in head for c in '、。：「」()（）'):
        return None
    return head


def lexicon_from(props):
    definitions = collections.defaultdict(list)
    for p in props.values():
        head = def_head(p.body)
        if head is not None:
            definitions[head].append(p.num)
    words = tuple(sorted(set(definitions) | set(OPEN_TERMS), key=lambda w: (-len(w), w)))
    return dict(definitions), words


def hits(text: str, words):
    """Leftmost-longest lexicon scan, not proper morphological segmentation."""
    out = []
    i = 0
    while i < len(text):
        found = None
        for w in words:
            if not text.startswith(w, i):
                continue
            # Prevent one-character CJK atoms from splitting unknown compounds.
            if len(w) == 1:
                left = text[i-1] if i else ''
                right = text[i+1] if i+1 < len(text) else ''
                if (left and '\u4e00' <= left <= '\u9fff') or (right and '\u4e00' <= right <= '\u9fff'):
                    continue
            found = w
            break
        if found:
            out.append((found, i, i + len(found)))
            i += len(found)
        else:
            i += 1
    return out


def def_terms_for_body(body, words):
    head = def_head(body)
    if head is None:
        return None, ()
    split = body.split('とは', 1)
    assert len(split) == 2
    tail = split[1]
    return head, tuple(sorted({t for t, _, _ in hits(tail, words) if t != head}))


def dictionary_edges(props, words):
    # lexical reference within definition text; neither entailment nor affirmed support.
    edges = collections.defaultdict(list)
    for p in props.values():
        head, tails = def_terms_for_body(p.body, words)
        if head is not None:
            for term in tails:
                edges[(head, term)].append(p.num)
    return {edge: tuple(ids) for edge, ids in edges.items()}


def adjacency(nodes, edges):
    ans = {n: set() for n in nodes}
    for (u, v) in edges:
        ans[u].add(v)
    return ans


def shortest(adj, source, target):
    if source not in adj or target not in adj:
        return None
    if source == target:
        return [source]
    seen = {source}
    q = collections.deque([(source, [source])])
    while q:
        u, path = q.popleft()
        for v in sorted(adj[u]):
            if v == target:
                return path + [v]
            if v not in seen:
                seen.add(v)
                q.append((v, path + [v]))
    return None


def scc(adj):
    index = 0
    stack, onstack = [], set()
    ind, low, components = {}, {}, []
    def visit(v):
        nonlocal index
        ind[v] = low[v] = index
        index += 1
        stack.append(v); onstack.add(v)
        for w in sorted(adj[v]):
            if w not in ind:
                visit(w); low[v] = min(low[v], low[w])
            elif w in onstack:
                low[v] = min(low[v], ind[w])
        if ind[v] == low[v]:
            comp = []
            while True:
                w = stack.pop(); onstack.remove(w)
                comp.append(w)
                if w == v: break
            components.append(tuple(sorted(comp)))
    for v in sorted(adj):
        if v not in ind: visit(v)
    return sorted(components, key=lambda c: (-len(c), c))


def edge_disjoint_count(adj, source, target):
    """Max flow on unit-capacity directed arcs (exact within this lexical graph)."""
    if source == target or source not in adj or target not in adj:
        return 0
    residual = collections.defaultdict(int)
    for u in adj:
        for v in adj[u]:
            residual[(u, v)] += 1
            residual[(v, u)] += 0
    flow = 0
    while True:
        pred = {source: None}
        queue = collections.deque([source])
        while queue and target not in pred:
            u = queue.popleft()
            for v in sorted(adj):
                if v not in pred and residual[(u, v)] > 0:
                    pred[v] = u; queue.append(v)
        if target not in pred:
            return flow
        v = target
        while pred[v] is not None:
            u = pred[v]
            residual[(u, v)] -= 1; residual[(v, u)] += 1
            v = u
        flow += 1


def apply_one(body, old, new):
    # Only change in the definitional tail; headword must remain unchanged.
    if 'とは' in body:
        pre, tail = body.split('とは', 1)
        if old not in tail:
            raise ValueError(f'expected lexical occurrence missing: {old!r} in {body}')
        return pre + 'とは' + tail.replace(old, new, 1)
    if old not in body:
        raise ValueError(f'expected occurrence missing: {old!r} in {body}')
    return body.replace(old, new, 1)


def mutated_props(props, lex_choices=(0,)*6, qualifier_mask=0):
    changed = {num: p for num, p in props.items()}
    texts = {num: p.body for num, p in props.items()}
    for (num, old, options), idx in zip(LEXICAL_EXPERIMENTS, lex_choices):
        texts[num] = apply_one(texts[num], old, options[idx])
    for i, (num, modifier, _) in enumerate(QUALIFIER_EXPERIMENTS):
        if (qualifier_mask >> i) & 1:
            if modifier not in texts[num]:
                raise ValueError(f'expected modifier missing: {modifier}')
            texts[num] = texts[num].replace(modifier, '', 1)
    return {num: Proposition(num, texts[num], p.line) for num, p in changed.items()}


def metrics_for_edges(words, edges):
    adj = adjacency(words, edges)
    components = scc(adj)
    pairs = []
    for a, b in QUERIES:
        path = shortest(adj, a, b)
        pairs.append((len(path)-1 if path else None, edge_disjoint_count(adj, a, b)))
    return {
        'edge_count': len(edges),
        'cyclic_groups': sum(len(c) > 1 for c in components),
        'largest_cycle_group': max((len(c) for c in components if len(c)>1), default=0),
        'paths': pairs,
    }


def signature(edges):
    text = '\n'.join(f'{a}>{b}:{",".join(sorted(refs))}' for (a,b),refs in sorted(edges.items()))
    return hashlib.sha256(text.encode('utf-8')).hexdigest()[:16]


def csv_write(path, fields, rows):
    with Path(path).open('w', encoding='utf-8-sig', newline='') as fh:
        wr=csv.DictWriter(fh, fieldnames=fields, extrasaction='ignore')
        wr.writeheader(); wr.writerows(rows)



def alpha_rename_control(props, words, baseline, old='照合', new='仮語甲'):
    """Rename ALL tokenized uses incl. headwords, preserving formal reference shape.

    This is not a synonym experiment: it is a pure placeholder-renaming control.
    """
    assert old in words and new not in words
    altered = {}
    changed_clauses=0
    changed_occurrences=0
    for num,p in props.items():
        spans=[(a,b) for t,a,b in hits(p.body,words) if t==old]
        body=p.body
        for a,b in reversed(spans):
            body=body[:a]+new+body[b:]
        if spans:
            changed_clauses+=1; changed_occurrences+=len(spans)
        altered[num]=Proposition(p.num,body,p.line)
    renamed_words=tuple(sorted((new if x==old else x for x in words),key=lambda w:(-len(w),w)))
    new_edges=dictionary_edges(altered,renamed_words)
    normalized={(old if a==new else a,old if b==new else b):ids for (a,b),ids in new_edges.items()}
    return {'改名する語':old, '改名後の仮符号':new,
            '変更した命題数':changed_clauses,'変更した語の出現数':changed_occurrences,
            '対応する全語を一括改名したあと元のラベルへ戻すと定義参照が一致': normalized==baseline,
            '注記':'単なる記号の一括改名対照。異なる語義・実際の意味不変性の証明ではない。'}

def write_graphml(path, props, words, definitions, edges):
    # Baseline two-mode usage graph, plus distinct definition reference arcs.
    lines=['<?xml version="1.0" encoding="UTF-8"?>',
           '<graphml xmlns="http://graphml.graphdrawing.org/xmlns">',
           '<key id="kind" for="node" attr.name="kind" attr.type="string"/>',
           '<key id="label" for="node" attr.name="label" attr.type="string"/>',
           '<key id="etype" for="edge" attr.name="edge_type" attr.type="string"/>',
           '<key id="origin" for="edge" attr.name="provenance_numbers" attr.type="string"/>',
           '<graph id="dictionary_usage" edgedefault="directed">']
    nid={w:f't{i}' for i,w in enumerate(sorted(words))}
    for term in sorted(words):
        kind='defined_term' if term in definitions else 'open_term'
        lines.append(f'<node id="{nid[term]}"><data key="kind">{kind}</data><data key="label">{xml_escape(term)}</data></node>')
    for num in props:
        lines.append(f'<node id="p{num}"><data key="kind">proposition</data><data key="label">{num}</data></node>')
    eid=0
    def append(u,v,typ,refs=''):
        nonlocal eid
        lines.append(f'<edge id="e{eid}" source="{u}" target="{v}"><data key="etype">{typ}</data><data key="origin">{xml_escape(str(refs))}</data></edge>'); eid+=1
    for term, nums in definitions.items():
        for num in nums: append(nid[term],f'p{num}','defined_at',num)
    for num,p in props.items():
        for term in sorted({t for t,_,_ in hits(p.body,words)}):
            append(f'p{num}',nid[term],'literal_use',num)
    for (a,b),nums in sorted(edges.items()):
        append(nid[a],nid[b],'definition_mentions',','.join(nums))
    lines+=['</graph>','</graphml>']
    Path(path).write_text('\n'.join(lines)+'\n',encoding='utf-8')


def dot_graph(path, words, definitions, edges, focus=None):
    # Headwords and their direct dictionary references; non-semantic visualization.
    if focus:
        allowed=set(focus)
        for a,b in edges:
            if a in focus or b in focus:
                allowed.add(a);allowed.add(b)
        words=[w for w in words if w in allowed]
    else:
        allowed=set(words)
    def q(s): return json.dumps(s,ensure_ascii=False)
    lines=['digraph lexical_dictionary {', 'graph [rankdir=LR, overlap=false, splines=true, bgcolor="white", fontname="Noto Sans CJK JP", label="境界認識批判：辞書的参照（推論・含意ではない）", labelloc="t"];', 'node [fontname="Noto Sans CJK JP", fontsize=11, shape=ellipse, style=filled, fillcolor="#f1f5f9", color="#64748b"];', 'edge [color="#8896a9", arrowsize=0.6];']
    for w in words:
        color='#dff3ed' if w in definitions else '#faf0db'
        lines.append(f'{q(w)} [fillcolor="{color}"];')
    for (a,b),refs in edges.items():
        if a in allowed and b in allowed:
            lines.append(f'{q(a)} -> {q(b)} [tooltip={q(",".join(refs))}];')
    lines+=['}']
    Path(path).write_text('\n'.join(lines)+'\n', encoding='utf-8')


def write_viewer(path, props, words, definitions, summary):
    """Offline inspectable source/definition usage + literal lexical interventions."""
    payload = {
        'props': [{'num':p.num,'body':p.body,'line':p.line} for p in props.values()],
        'words': list(words),
        'definitions': definitions,
        'lexical': [{'num':n,'old':old,'options':list(opts)} for n,old,opts in LEXICAL_EXPERIMENTS],
        'qualifiers': [{'num':n,'text':modifier,'role':role} for n,modifier,role in QUALIFIER_EXPERIMENTS],
        'summary': {k:v for k,v in summary.items() if k not in ('baseline_cycles','paths')},
    }
    data = json.dumps(payload, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    html = r'''<!doctype html><html lang="ja"><head><meta charset="utf-8">
<title>境界認識批判｜使用と定義の辞書グラフ実験</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
:root{--ink:#142939;--muted:#526575;--line:#dae3eb;--card:white;--bg:#f4f7f8;--accent:#156b70;--warning:#8a4f21}
*{box-sizing:border-box}body{margin:0;font-family:"Noto Sans CJK JP",Meiryo,system-ui,sans-serif;background:var(--bg);color:var(--ink);line-height:1.62}
header{background:#133b46;color:white;padding:28px clamp(16px,4vw,58px)}header h1{font-size:clamp(21px,2.8vw,32px);margin:0 0 6px}header p{max-width:1100px;margin:8px 0;color:#d6e8ea}
.wrap{max-width:1440px;margin:auto;padding:20px} .grid{display:grid;grid-template-columns:minmax(320px,420px) minmax(0,1fr);gap:18px}
@media(max-width:950px){.grid{grid-template-columns:1fr}}.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:20px;margin-bottom:18px;box-shadow:0 1px 3px #1730480b}
h2{font-size:17px;color:#113e4b;margin:0 0 13px}h3{font-size:15px;margin:16px 0 8px}.note{font-size:13px;color:var(--muted)}.alert{border-left:4px solid #b26a2a;padding:10px 14px;background:#fff6e9;font-size:13px}
label{font-size:13px;font-weight:600;display:block;margin:9px 0 3px}input[type=text],select{border:1px solid #b9cdd7;border-radius:7px;padding:8px 10px;width:100%;background:#fbfeff;color:var(--ink)}
.options{display:grid;grid-template-columns:1fr 1fr;gap:7px 13px}@media(max-width:550px){.options{grid-template-columns:1fr}}
.variation{border-top:1px solid #e7eef0;padding:9px 0}.variation strong{font-size:12px}
button{padding:7px 11px;border:1px solid #a6c4c7;background:#eaf5f4;color:#125963;border-radius:7px;cursor:pointer}button:hover{background:#d8ece9}
.chip{display:inline-block;border:1px solid #c7d8df;border-radius:14px;padding:2px 8px;margin:2px;color:#254851;font-size:12px;cursor:pointer}
.chip:hover{background:#e6f2f2}.numb{color:#597583;font-size:12px}.mono{font-family:ui-monospace,monospace}
#graph{height:400px;width:100%;background:#fcfefe;border:1px solid #e0eaee;border-radius:9px}.side{height:260px;overflow:auto}
.entry{border-bottom:1px solid #edf1f3;padding:7px 0;font-size:13px}.entry:last-child{border:0}
strong.term{color:#08747b}.stats{display:flex;flex-wrap:wrap;gap:8px}.stat{padding:8px 10px;background:#eaf2f4;border-radius:7px;font-size:13px}
small{color:var(--muted)}.snapshot{max-height:220px;overflow:auto;font-size:12px}.sourceLine{border-top:1px solid #edf1f3;padding:7px 0}.sourceLine em{color:#8a4f21}
</style></head><body>
<header><h1>境界認識批判｜語の使用・定義・変更の実験辞書</h1><p>本文265命題の原文を保持し、語を局所置換／修飾表現を削除して辞書型参照グラフの変化を観察します。変更は表示内だけで、原文・Repository・正本を変更しません。</p></header>
<main class="wrap"><div class="alert">このグラフの矢印は「定義文に語が現れた」ことだけを示します。論理的な支持・含意・賛成を意味しません。修飾語、否定、様相を落としても矢印が変わらない場合があります。語の変更は意味の言い換えとして承認されたものではなく、反事実的な試験入力です。</div>
<div class="grid" style="margin-top:18px"><section>
<div class="card"><h2>① 語の辞書索引</h2><input id="search" type="text" placeholder="語・命題番号・本文を検索"><div id="terms" class="side"></div></div>
<div class="card"><h2>② 局所的な語の置換（6箇所×3通り）</h2><p class="note">同じ語の全出現を置換するのではなく、指定された定義文の一箇所だけを変更します。</p><div id="variants"></div><button id="reset">すべて原文に戻す</button></div>
<div class="card"><h2>③ 修飾表現の削除（6箇所）</h2><div id="qualifiers"></div><p class="note">削除は意味の変化を伴い得ます。辞書グラフが反応しない場合は抽出方式の盲点です。</p></div>
</section><section>
<div class="card"><h2>選択語の参照構造 <span id="currentTerm" class="term"></span></h2><div id="stats" class="stats"></div>
<svg id="graph" viewBox="0 0 850 380" aria-label="中心語とその定義参照のネットワーク"></svg><div class="note">中心から外向きの矢印：定義文に現れる語。中心へ向く矢印：この語を参照する定義見出し語。節点をクリックすると辞書を切り替えます。</div>
<h3>この語の定義文</h3><div id="definitionList"></div><h3>この語を使用する命題</h3><div id="usageList" class="snapshot"></div></div>
<div class="card"><h2>④ 現在の変更による差分</h2><div id="diffStats" class="stats"></div><div id="alteredLines" class="snapshot"></div>
<h3>試験対象の辞書経路</h3><div id="queryStats"></div><p class="note">経路長＝定義文参照の最短辺数。径の代理候補＝辺を共有しない参照経路の最大本数。物理的な径・インピーダンスや意味的な容量ではありません。</p></div>
</section></div>
<div class="card"><h2>成立層・未判定</h2><p>観測したのは、文字列から構成した定義参照と語の使用です。見かけの循環は論理的な循環論証ではありません。文法構造・肯否・様相・量化・条件文・参照先の同一性は、このビューアでは監査対象にしていません。局所置換の結果が不変でも、意味の不変性を証明しません。</p></div>
</main><script id="dictionaryData" type="application/json">__DATA__</script>
<script>
'use strict';const D=JSON.parse(document.getElementById('dictionaryData').textContent), orig=new Map(D.props.map(x=>[x.num,x])), qsel=[], choices=new Array(D.lexical.length).fill(0), mods=new Array(D.qualifiers.length).fill(false); let selected='照合';
const terms=document.getElementById('terms'),graph=document.getElementById('graph');
const E=(s)=>String(s).replace(/[&<>\"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function head(b){const m=b.match(/^(.{1,24}?)とは(?:、|，|\s|$)/); if(!m)return null;const h=m[1];if(h.endsWith('こと')||h.endsWith('するこ')||h.startsWith('すべての')||h.startsWith('経験を')||/[、。：「」()（）]/.test(h))return null;return h;}
function lexhits(s){let res=[];for(let i=0;i<s.length;){let w=D.words.find(x=>s.startsWith(x,i) && (x.length>1|| !((i>0&&/[\u4e00-\u9fff]/.test(s[i-1]))||(i+1<s.length&&/[\u4e00-\u9fff]/.test(s[i+1])))));if(w){res.push(w);i+=w.length;}else i++;}return [...new Set(res)];}
function current(){let p=new Map(D.props.map(x=>[x.num,x.body]));D.lexical.forEach((v,i)=>{let s=p.get(v.num);let k=s.indexOf('とは');if(k<0)k=0;let tail=s.slice(k+2);p.set(v.num,s.slice(0,k+2)+tail.replace(v.old,v.options[choices[i]]));});D.qualifiers.forEach((v,i)=>{if(mods[i])p.set(v.num,p.get(v.num).replace(v.text,''));});return p;}
function buildEdges(p){let g=new Map();D.words.forEach(x=>g.set(x,new Set()));D.props.forEach(row=>{const s=p.get(row.num),h=head(s);if(!h||!g.has(h))return;const tail=s.split('とは').slice(1).join('とは');lexhits(tail).filter(t=>t!==h).forEach(t=>g.get(h).add(t));});return g;}
function edgeSet(g){const ans=new Set();g.forEach((vs,u)=>vs.forEach(v=>ans.add(u+'\u0001'+v)));return ans;}
function shortest(g,a,b){if(!g.has(a)||!g.has(b))return null;let Q=[[a,[a]]],seen=new Set([a]);while(Q.length){let [u,path]=Q.shift();if(u===b)return path;for(const v of [...g.get(u)].sort()){if(!seen.has(v)){seen.add(v);Q.push([v,[...path,v]]);}}}return null;}
const base=buildEdges(new Map(D.props.map(x=>[x.num,x.body]))),baseSet=edgeSet(base);
function renderTerms(){let text=document.getElementById('search').value.trim(), matches=D.words.filter(w=>!text||w.includes(text)||D.props.some(p=>p.num.includes(text)&&lexhits(p.body).includes(w)));terms.innerHTML=matches.map(w=>`<span class="chip" data-t="${E(w)}" style="${w===selected?'background:#ceefec;font-weight:700':''}">${E(w)}${D.definitions[w]?'':' ◌'}</span>`).join('')||'一致する語がありません';terms.querySelectorAll('.chip').forEach(x=>x.onclick=()=>{selected=x.dataset.t;render();});}
function node(svg,x,y,name,style){let t=document.createElementNS('http://www.w3.org/2000/svg','g');t.setAttribute('cursor','pointer');let circle=document.createElementNS('http://www.w3.org/2000/svg','circle');circle.setAttribute('cx',x);circle.setAttribute('cy',y);circle.setAttribute('r',name===selected?34:26);circle.setAttribute('stroke','#417c83');circle.setAttribute('fill',style);let label=document.createElementNS('http://www.w3.org/2000/svg','text');label.setAttribute('x',x);label.setAttribute('y',y+4);label.setAttribute('text-anchor','middle');label.setAttribute('font-size',name.length>8?10:12);label.textContent=name;t.appendChild(circle);t.appendChild(label);t.onclick=()=>{selected=name;render();};let tip=document.createElementNS('http://www.w3.org/2000/svg','title');tip.textContent=name;t.appendChild(tip);svg.appendChild(t);}
function draw(g){graph.innerHTML='<defs><marker id="tip" markerWidth="7" markerHeight="7" refX="5" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6" fill="none" stroke="#708a93"/></marker></defs>';
const out=[...(g.get(selected)||[])].sort(),input=[...D.words].filter(w=>g.get(w)?.has(selected)).sort();let peers=[...new Set([...out,...input])].slice(0,17),x=425,y=190;for(let i=0;i<peers.length;i++){let ang=-Math.PI/2+i*2*Math.PI/peers.length,r=148,px=x+r*Math.cos(ang)*2.0,py=y+r*Math.sin(ang)*.92;const edge=document.createElementNS('http://www.w3.org/2000/svg','line');edge.setAttribute('x1',out.includes(peers[i])?x:px);edge.setAttribute('y1',out.includes(peers[i])?y:py);edge.setAttribute('x2',out.includes(peers[i])?px:x);edge.setAttribute('y2',out.includes(peers[i])?py:y);edge.setAttribute('stroke','#8da4aa');edge.setAttribute('stroke-width','1.6');edge.setAttribute('marker-end','url(#tip)');graph.appendChild(edge);node(graph,px,py,peers[i],out.includes(peers[i])?'#e4f1ec':'#fbecdc');}
node(graph,x,y,selected,'#95d5cb');if(out.length+input.length>17){const n=document.createElementNS('http://www.w3.org/2000/svg','text');n.textContent='周辺は17語まで表示';n.setAttribute('x','10');n.setAttribute('y','368');n.setAttribute('font-size','12');graph.appendChild(n);}}
function render(){const p=current(),g=buildEdges(p),arcs=edgeSet(g);document.getElementById('currentTerm').textContent=selected;
let out=[...(g.get(selected)||[])],incoming=D.words.filter(w=>g.get(w)?.has(selected));document.getElementById('stats').innerHTML=`<div class="stat">明示定義：${D.definitions[selected]?'あり':'なし'}</div><div class="stat">参照先：${out.length}</div><div class="stat">被参照：${incoming.length}</div><div class="stat">全語：${D.words.length}</div>`;draw(g);
const defs=D.props.filter(x=>head(p.get(x.num))===selected);document.getElementById('definitionList').innerHTML=defs.length?defs.map(x=>`<div class="entry"><span class="numb">${x.num}（原文${x.line}行）</span> ${E(p.get(x.num))}</div>`).join(''):'<div class="note">本文に「〜とは」の明示定義は見つかりません。</div>';
const usage=D.props.filter(x=>lexhits(p.get(x.num)).includes(selected));document.getElementById('usageList').innerHTML=`<small>${usage.length}命題</small>`+usage.slice(0,100).map(x=>`<div class="entry"><b>${x.num}</b> ${E(p.get(x.num))}</div>`).join('');
let plus=[...arcs].filter(x=>!baseSet.has(x)),minus=[...baseSet].filter(x=>!arcs.has(x));let mcount=mods.filter(Boolean).length;document.getElementById('diffStats').innerHTML=`<div class="stat">辞書参照辺：${arcs.size}（基準${baseSet.size}）</div><div class="stat">追加：${plus.length}</div><div class="stat">消滅：${minus.length}</div><div class="stat">未表現の削除条件：${mcount}</div>`;
const changed=[...p].filter(([num,b])=>orig.get(num).body!==b);document.getElementById('alteredLines').innerHTML=changed.length?changed.map(([num,b])=>`<div class="sourceLine"><span class="numb">${num}</span><div><s>${E(orig.get(num).body)}</s></div><div><em>${E(b)}</em></div></div>`).join(''):'<div class="note">変更なし（原文の状態）</div>';
let q=[['知る','履歴'],['照合','履歴'],['認識','分類'],['同期','言語ゲーム'],['通約','学問']];document.getElementById('queryStats').innerHTML=q.map(([a,b])=>{let path=shortest(g,a,b);return `<div class="entry">${E(a)} → ${E(b)}：${path?path.length-1+'辺｜'+E(path.join(' → ')):'現グラフ内で経路なし'}</div>`;}).join('');renderTerms();}
const vars=document.getElementById('variants');vars.innerHTML=D.lexical.map((x,i)=>`<div class="variation"><strong>${x.num}：「${E(x.old)}」を変更</strong><select data-i="${i}">${x.options.map((v,j)=>`<option value="${j}">${j===0?'原文：':'変更：'}${E(v)}</option>`).join('')}</select></div>`).join('');vars.querySelectorAll('select').forEach(x=>x.onchange=()=>{choices[+x.dataset.i]=+x.value;render();});
const qs=document.getElementById('qualifiers');qs.innerHTML=D.qualifiers.map((x,i)=>`<div class="variation"><label><input type="checkbox" data-i="${i}"> ${x.num}：「${E(x.text)}」を削除 <small>（${E(x.role)}）</small></label></div>`).join('');qs.querySelectorAll('input').forEach(x=>x.onchange=()=>{mods[+x.dataset.i]=x.checked;render();});
document.getElementById('reset').onclick=()=>{choices.fill(0);mods.fill(false);vars.querySelectorAll('select').forEach(x=>x.value='0');qs.querySelectorAll('input').forEach(x=>x.checked=false);render();};
document.getElementById('search').oninput=renderTerms;render();
</script></body></html>'''
    Path(path).write_text(html.replace('__DATA__',data)+'\n',encoding='utf-8')


def run(source: Path, out: Path, full=True):
    out.mkdir(parents=True,exist_ok=True)
    props=extract_props(source)
    definitions, words=lexicon_from(props)
    for num, old, opts in LEXICAL_EXPERIMENTS:
        assert num in props and old in props[num].body, (num,old)
        for w in opts:
            assert w in words, (w, 'not in lexicon')
    for num, term, kind in QUALIFIER_EXPERIMENTS:
        assert num in props and term in props[num].body, (num,term)
        assert term not in words, 'This modifier accidentally creates a lexicon term'

    base_edges=dictionary_edges(props,words)
    base_metrics=metrics_for_edges(words,base_edges)
    rename_check=alpha_rename_control(props,words,base_edges)
    all_edges=[]; graph_rows=[]; case_rows=[]; per_case=[]
    base_sig=signature(base_edges)
    memo={}
    cases=itertools.product(range(3),repeat=len(LEXICAL_EXPERIMENTS)) if full else [(0,)*len(LEXICAL_EXPERIMENTS)]
    for lc in cases:
        altered=mutated_props(props,lc)
        edges=dictionary_edges(altered,words)
        sig=signature(edges)
        if sig not in memo:
            memo[sig]=metrics_for_edges(words,edges)
        m=memo[sig]
        all_edges.append(set(edges))
        delta_plus=set(edges)-set(base_edges)
        delta_minus=set(base_edges)-set(edges)
        row={'lex_choices':''.join(map(str,lc)), 'graph_signature':sig,
             'changed_arcs_added':len(delta_plus), 'changed_arcs_removed':len(delta_minus),
             'edge_count':m['edge_count'], 'cyclic_groups':m['cyclic_groups'],
             'largest_cycle_group':m['largest_cycle_group']}
        for (a,b), (dist,width) in zip(QUERIES,m['paths']):
            tag=a+'→'+b
            row['距離_'+tag]='' if dist is None else dist
            row['経路本数_'+tag]=width
        graph_rows.append(row)
        # The modifier sets are factorially enumerated, but are graph-invisible
        # when they contain no lexicon term: we also verify that explicitly.
        for mask in range(1<<len(QUALIFIER_EXPERIMENTS)):
            case_rows.append({'lex_choices':row['lex_choices'],
                              'qualifier_bits':format(mask,f'0{len(QUALIFIER_EXPERIMENTS)}b'),
                              'deletion_count':mask.bit_count(),
                              'graph_signature':sig,
                              'same_arcs_as_baseline':int(set(edges)==set(base_edges)),
                              'same_distance_vector_as_baseline':int(m['paths']==base_metrics['paths']),
                              'qualifier_changes_unrepresented':mask.bit_count()})
        # Diagnostic lex-only change from baseline, for all 12 single-term alternatives.
    # Direct text re-extraction on independent qualifiers verifies the analytical shortcut.
    check_rows=[]
    for i,(num,mod,kind) in enumerate(QUALIFIER_EXPERIMENTS):
        mutated=mutated_props(props,qualifier_mask=(1<<i))
        check_edges=dictionary_edges(mutated,words)
        check_rows.append({'命題番号':num,'修飾表現':mod,'機能仮説':kind,
                           '原文':props[num].body,'除去後':mutated[num].body,
                           '辞書参照グラフの変化辺数':len(set(check_edges)^set(base_edges)),
                           '語彙参照が検出した意味変化': '対象外'})
    single_rows=[]
    for k,(num,old,options) in enumerate(LEXICAL_EXPERIMENTS):
        for alt in (1,2):
            lc=[0]*len(LEXICAL_EXPERIMENTS); lc[k]=alt
            mutated=mutated_props(props,lc)
            e=dictionary_edges(mutated,words)
            now=metrics_for_edges(words,e)
            single_rows.append({'命題番号':num,'変更箇所':old,'置換語':options[alt],
                                '原文':props[num].body,'置換後':mutated[num].body,
                                '参照追加': ' / '.join('→'.join(p) for p in sorted(set(e)-set(base_edges))),
                                '参照消滅':' / '.join('→'.join(p) for p in sorted(set(base_edges)-set(e))),
                                '有向参照の変化本数':len(set(base_edges)^set(e)),
                                '距離ベクトル変化':sum(x!=y for x,y in zip(base_metrics['paths'],now['paths']))})
    # single-row fully source-grounded index
    index_rows=[]
    for num,p in props.items():
        seen=sorted({t for t,_,_ in hits(p.body,words)})
        index_rows.append({'番号':num,'行':p.line,'原文':p.body,
                           '命題SHA256':hashlib.sha256(p.body.encode('utf-8')).hexdigest(),
                           '出現辞書語':' | '.join(seen),
                           '定義見出し':def_head(p.body) or ''})
    defrows=[]
    for term in sorted(words):
        use_nums=sorted(p.num for p in props.values() if term in {t for t,_,_ in hits(p.body,words)})
        refs=sorted({v for (u,v) in base_edges if u==term})
        defrows.append({'語':term,'出典定義番号':' | '.join(definitions.get(term,[])),
                        '使用命題数':len(use_nums),'使用命題番号':' | '.join(use_nums),
                        '定義文から参照する語':' | '.join(refs),
                        '原文内での明示定義':int(term in definitions)})
    component_rows=[]
    for i,comp in enumerate(scc(adjacency(words,base_edges)),1):
        if len(comp)>1:
            component_rows.append({'循環群':i,'語数':len(comp),'語集合':' | '.join(comp),
                                   '性格':'定義文の字面参照が相互到達（意味の同値・論理循環ではない）'})
    # stable edges among ALL lexical scenarios, not semantic invariance.
    intersection=set.intersection(*all_edges) if all_edges else set()
    union=set.union(*all_edges) if all_edges else set()
    changed_baseline=set(base_edges)&(union-intersection)
    ngraph=len(graph_rows)
    dist_rows=[]
    for i,(a,b) in enumerate(QUERIES):
        dists=[r[f'距離_{a}→{b}'] for r in graph_rows]
        widths=[r[f'経路本数_{a}→{b}'] for r in graph_rows]
        dist_rows.append({'照会':a+'→'+b,
                          '基準距離':base_metrics['paths'][i][0],
                          '語置換729通りで到達':sum(x!='' for x in dists),
                          '語置換729通りで経路長の種類':len(set(map(str,dists))),
                          '基準辺素な経路数':base_metrics['paths'][i][1],
                          '経路数の最小':min(widths), '経路数の最大':max(widths)})
    csv_write(out/'命題265件と辞書語の使用.csv', ['番号','行','原文','命題SHA256','出現辞書語','定義見出し'],index_rows)
    csv_write(out/'辞書見出しと使用・定義参照.csv',['語','出典定義番号','使用命題数','使用命題番号','定義文から参照する語','原文内での明示定義'],defrows)
    csv_write(out/'定義文の循環参照群.csv',['循環群','語数','語集合','性格'],component_rows)
    csv_write(out/'局所語置換12件の応答.csv', ['命題番号','変更箇所','置換語','原文','置換後','参照追加','参照消滅','有向参照の変化本数','距離ベクトル変化'],single_rows)
    csv_write(out/'修飾表現削除6件の盲点.csv',['命題番号','修飾表現','機能仮説','原文','除去後','辞書参照グラフの変化辺数','語彙参照が検出した意味変化'],check_rows)
    dist_cols=list(graph_rows[0])
    csv_write(out/'語置換729グラフ指標.csv',dist_cols,graph_rows)
    csv_write(out/'語置換と修飾削除46656全ケース.csv',list(case_rows[0]),case_rows)
    csv_write(out/'経路長と経路径の代理指標.csv',list(dist_rows[0]),dist_rows)
    write_graphml(out/'辞書・使用グラフ.graphml',props,words,definitions,base_edges)
    focus={'知る','同期','照合','残差','残差保持','境界','履歴','分類','通約','認識','理性','学問','感性','悟性','内部ヒューリスティック','外部ヒューリスティック','言語ゲーム','判断可能性'}
    dot_graph(out/'辞書的参照の中心部分.dot',words,definitions,base_edges,focus)
    summary={
        'source':SOURCE_REL,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
        'numbers':len(props),'lexicon_terms':len(words),'defined_headwords':len(definitions),
        'definition_rows':sum(len(x) for x in definitions.values()),
        'baseline_reference_arcs':len(base_edges),
        'baseline_cyclic_groups':len(component_rows),
        'baseline_cycles':component_rows[:6],
        'lexical_slots':len(LEXICAL_EXPERIMENTS),
        'qualifier_slots':len(QUALIFIER_EXPERIMENTS),
        'lexical_cases':ngraph,'all_factorial_cases':len(case_rows),
        'distinct_reference_graphs':len(memo),
        'reference_arc_union':len(union),'reference_arc_intersection':len(intersection),
        'reference_arcs_sensitive_in_variable_scenarios':len(union-intersection),
        'baseline_arcs_sensitive_in_variable_scenarios':len(changed_baseline),
        'local_modifier_deletions_with_no_graph_change':sum(not r['辞書参照グラフの変化辺数'] for r in check_rows),
        'local_lexical_substitutions_with_arc_change':sum(bool(r['有向参照の変化本数']) for r in single_rows),
        'paths':dist_rows,
        'global_alpha_rename_preserves_graph':rename_check['対応する全語を一括改名したあと元のラベルへ戻すと定義参照が一致'],
        'ontology':'literal headword-reference and usage graph; not a logical proof graph',
        'major_limitation':'Only chosen word lexicon and exact string matching; all lexical substitutions are counterfactual, not approved meanings; modifier deletions are not encoded.',
    }
    (out/'実験集計.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (out/'一括改名の対照.json').write_text(json.dumps(rename_check,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    # Store selected experiment recipe, never upstream canonical definitions.
    recipe={'source_relative_path':SOURCE_REL,'source_sha256':summary['source_sha256'],
            'words_extra':list(OPEN_TERMS),
            'substitutions':[{'id':i,'proposition':n,'old':w,'candidates':list(opts)} for i,(n,w,opts) in enumerate(LEXICAL_EXPERIMENTS)],
            'modifier_deletions':[{'id':i,'proposition':n,'substring':w,'hypothesized_role':kind} for i,(n,w,kind) in enumerate(QUALIFIER_EXPERIMENTS)],
            'disclaimers':['Every output is research-only: no approved changes to the source',
                           'Definition mention is NOT logical implication or canonical support',
                           'No exhaustive enumeration of all possible Japanese meanings is claimed']}
    (out/'語彙変更と削除の実験条件.json').write_text(json.dumps(recipe,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    write_viewer(out/'境界認識批判_語の使用と変更の辞書ビューア.html', props, words, definitions, summary)
    return summary


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source',type=Path,default=Path(SOURCE_REL))
    ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--smoke',action='store_true')
    ap.add_argument('--expect-sha256',help='Refuse execution on a different source revision')
    a=ap.parse_args()
    if a.expect_sha256 and hashlib.sha256(a.source.read_bytes()).hexdigest().lower()!=a.expect_sha256.lower():
        ap.error('source SHA-256 does not match --expect-sha256')
    s=run(a.source,a.out,not a.smoke)
    print(json.dumps({k:v for k,v in s.items() if k not in ('baseline_cycles','paths')},ensure_ascii=False,indent=2))
if __name__=='__main__': main()

#!/usr/bin/env python3
"""Provisional Euclid beta entropy by routed dependency paths.

The input is a precise Wolfram export, but the wide lexical-concept layer is
interpretive. It is a reproducible OBSERVED-CANDIDATE MAXIMUM POLICY, not a
mathematical upper bound on all possible derivations or a semantic proof.
No input or alpha/exergy asset is modified.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import re
from collections import Counter, defaultdict, deque
from pathlib import Path

ROM = ('', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII')
EXPECTED_SHA = '901c9af2e18e45b2bc8f6951757561352cc8abba2978684574fafb4a6cdbd848'
EXPECTED_THEOREMS = (48, 14, 37, 16, 25, 33, 39, 27, 36, 115, 39, 18, 18)


def decode(node):
    if not isinstance(node, list):
        return node[1:-1] if isinstance(node, str) and len(node)>1 and node[0]==node[-1]=="'" else node
    if not node:
        return []
    head, *rest = node
    if head in ('Association','List'):
        if rest and all(isinstance(v,list) and len(v)==3 and v[0]=='Rule' for v in rest):
            out = {}
            for _,k,v in rest:
                key=decode(k)
                if key in out:raise ValueError('Repeated key')
                out[key]=decode(v)
            return out
        if head=='Association' and rest:raise ValueError('Malformed association')
        return [decode(v) for v in rest]
    if head=='Missing':return None
    return {'_head':head,'_args':[decode(v) for v in rest]}


def load_source(path):
    payload=path.read_bytes();sha=hashlib.sha256(payload).hexdigest()
    if sha!=EXPECTED_SHA:raise ValueError('Unexpected source hash: '+sha)
    raw=json.loads(payload)
    if not isinstance(raw,list) or raw[0]!='Association' or len(raw)!=608:raise ValueError('Invalid corpus')
    props={}; defs={};aux={}
    for r in raw[1:]:
        if not (len(r)==3 and r[0]=='Rule'):raise ValueError('Invalid entry')
        k,v=decode(r[1]),decode(r[2])
        if 'Theorem' in k:
            pid=f'{ROM[k["Book"]]}.{k["Theorem"]}'
            if pid in props:raise ValueError('Duplicate theorem '+pid)
            props[pid]={'key':k,'value':v}
        elif 'Definition' in k:
            did=f'{ROM[k["Book"]]}.Definition{k["Definition"]}'
            if did in defs:raise ValueError('Duplicate definition '+did)
            defs[did]={'key':k,'value':v}
        elif 'Postulate' in k:
            aux[f'P{k["Postulate"]}']={'key':k,'value':v}
        elif 'Common Notion' in k:
            aux[f'CN{k["Common Notion"]}']={'key':k,'value':v}
        else:raise ValueError('Unsupported source record: '+str(k))
    expected={f'{ROM[b]}.{n}' for b,cnt in enumerate(EXPECTED_THEOREMS,1) for n in range(1,cnt+1)}
    if set(props)!=expected or len(defs)!=132 or len(aux)!=10:raise ValueError('Corpus inventory mismatch')
    return sha,props,defs,aux


def order(pid):
    b,n=pid.split('.');return ROM.index(b),int(n)


def definition_unit(did):
    if did in {f'X.Definition1.{n}' for n in range(1,5)}:
        return 'X.Definitions_I'
    return did


def collect_aliases():
    """(definition, alias regex, min book, max book, intent).

    Phrase patterns have precedence via matched span. A narrow compound phrase
    is not an additional occurrence of its own generic component (e.g. P1
    straight line is not automatically both straight-line AND line).
    """
    x=[]
    def add(k,terms,lo=1,hi=13):
        for term in terms.split(' | '):
            x.append((k,term,lo,hi))
    add('I.Definition1',r'\bpoints?\b')
    add('I.Definition2',r'\blines?\b')
    add('I.Definition3',r'\bextremit(?:y|ies) of (?:a |the )?lines?\b')
    add('I.Definition4',r'\bstraight lines?\b')
    add('I.Definition5',r'\bsurfaces?\b')
    add('I.Definition6',r'\bextremit(?:y|ies) of (?:a |the )?surfaces?\b')
    add('I.Definition7',r'\bplane surfaces?\b')
    add('I.Definition8',r'\bplane angles?\b')
    add('I.Definition9',r'\brectilineal angles?\b')
    add('I.Definition10',r'\bright angles?\b | \bperpendiculars?\b')
    add('I.Definition11',r'\bobtuse angles?\b')
    add('I.Definition12',r'\bacute angles?\b')
    add('I.Definition13',r'\bboundar(?:y|ies)\b')
    add('I.Definition14',r'\bfigures?\b')
    add('I.Definition15',r'\bcircles?\b')
    add('I.Definition16',r'\bcent(?:er|re)s? of (?:the |a )?circles?\b | \bcent(?:er|re)s?\b')
    add('I.Definition17',r'\bdiameters? of (?:the |a )?circles?\b')
    add('I.Definition18',r'\bsemicircles?\b')
    add('I.Definition19',r'\brectilineal figures?\b | \btrilateral figures?\b | \bquadrilateral figures?\b | \bmultilateral figures?\b')
    add('I.Definition20',r'\bequilateral triangles?\b | \bisosceles triangles?\b | \bscalene triangles?\b')
    add('I.Definition21',r'\bright[- ]angled triangles?\b | \bobtuse[- ]angled triangles?\b | \bacute[- ]angled triangles?\b')
    add('I.Definition22',r'\bsquares?\b | \boblongs?\b | \brhombi?\b | \brhomboids?\b | \btrapezia\b')
    add('I.Definition23',r'\bparallel straight lines?\b | \bparallel lines?\b')
    add('II.Definition1',r'\brectangular parallelograms?\b | \brectangle(?:s)? contained by\b',2)
    add('II.Definition2',r'\bgnomons?\b',2)
    add('III.Definition1',r'\bequal circles?\b',3)
    add('III.Definition2',r'\btangent to (?:a |the )?circles?\b | \btouch(?:es|ing|ed)? (?:a |the )?circles?\b',3)
    add('III.Definition3',r'\bcircles? touch(?:ing|es)? (?:one another|each other)\b',3)
    add('III.Definition4',r'\bequally distant from (?:the |a )?cent(?:er|re)\b',3)
    add('III.Definition5',r'\bat a greater distance from (?:the |a )?cent(?:er|re)\b',3)
    add('III.Definition6',r'\bsegments? of (?:a |the )?circles?\b',3)
    add('III.Definition7',r'\bangles? of (?:a |the )?segments?\b',3)
    add('III.Definition8',r'\bangles? in (?:a |the )?segments?\b',3)
    add('III.Definition9',r'\bangles? (?:stand|stands|standing) upon\b',3)
    add('III.Definition10',r'\bsectors? of (?:a |the )?circles?\b',3)
    add('III.Definition11',r'\bsimilar segments?\b',3)
    add('IV.Definition1',r'\binscribed in (?:a |the )?rectilineal figure\b',4)
    add('IV.Definition2',r'\bcircumscribed about (?:a |the )?rectilineal figure\b',4)
    add('IV.Definition3',r'\binscribed in (?:a |the )?circle\b | \binscribe\b.{0,60}\bin (?:a |the )?circle\b',4)
    add('IV.Definition4',r'\bcircumscribed about (?:a |the )?circle\b',4)
    add('IV.Definition5',r'\bcircle.{0,20}\binscribed in (?:a |the )?figure\b',4)
    add('IV.Definition6',r'\bcircle.{0,20}\bcircumscribed about (?:a |the )?figure\b',4)
    add('IV.Definition7',r'\bfitted into (?:a |the )?circle\b',4)
    add('V.Definition1',r'\bmagnitudes?\b',5)
    add('V.Definition2',r'\bmultiples? of (?:a |the )?magnitude\b',5)
    add('V.Definition3',r'\bratios?\b',5)
    add('V.Definition4',r'\bmagnitudes? (?:which )?have a ratio\b',5)
    add('V.Definition5',r'\bsame ratio\b | \bequimultiples?\b',5)
    add('V.Definition6',r'\bproportional\b',5,6)
    add('V.Definition7',r'\bgreater ratio\b',5)
    add('V.Definition8',r'\bproportion in three terms\b',5)
    add('V.Definition9',r'\bduplicate ratio\b',5)
    add('V.Definition10',r'\btriplicate ratio\b',5)
    add('V.Definition11',r'\bcorresponding magnitudes?\b',5)
    add('V.Definition12',r'\balternate ratio\b | \balternately\b',5)
    add('V.Definition13',r'\binverse ratio\b | \binversely\b',5)
    add('V.Definition14',r'\bcomposition of (?:a |the )?ratio\b | \bcomponendo\b',5)
    add('V.Definition15',r'\bseparation of (?:a |the )?ratio\b | \bdividendo\b',5)
    add('V.Definition16',r'\bconversion of (?:a |the )?ratio\b | \bconvertendo\b',5)
    add('V.Definition17',r'\bex aequali\b',5)
    add('V.Definition18',r'\bperturbed proportion\b',5)
    add('VI.Definition1',r'\bsimilar rectilineal figures?\b | \bsimilar figures?\b',6)
    add('VI.Definition2',r'\breciprocally related\b',6)
    add('VI.Definition3',r'\bextreme and mean ratio\b',6)
    add('VI.Definition4',r'\bheight of (?:a |the |any )?figure\b',6)
    add('VI.Definition5',r'\bcompounded of ratios?\b',6)
    add('VII.Definition1',r'\bunits?\b',7,9)
    add('VII.Definition2',r'\bnumbers?\b',7,9)
    add('VII.Definition3',r'\bpart of (?:a |the )?number\b',7,9)
    add('VII.Definition4',r'\bparts of (?:a |the )?number\b',7,9)
    add('VII.Definition5',r'\bmultiple of (?:a |the )?number\b',7,9)
    add('VII.Definition6',r'\beven numbers?\b',7,9)
    add('VII.Definition7',r'\bodd numbers?\b',7,9)
    add('VII.Definition8',r'\beven[- ]times[- ]even numbers?\b',7,9)
    add('VII.Definition9',r'\beven[- ]times[- ]odd numbers?\b',7,9)
    add('VII.Definition10',r'\bodd[- ]times[- ]odd numbers?\b',7,9)
    add('VII.Definition11',r'\bprime numbers?\b',7,9)
    add('VII.Definition12',r'\b(?:numbers? )?prime to one another\b',7,9)
    add('VII.Definition13',r'\bcomposite numbers?\b',7,9)
    add('VII.Definition14',r'\b(?:numbers? )?composite to one another\b',7,9)
    add('VII.Definition15',r'\bnumbers? (?:which )?(?:multiply|multiplies) (?:a |the )?number\b',7,9)
    add('VII.Definition16',r'\bplane numbers?\b',7,9)
    add('VII.Definition17',r'\bsolid numbers?\b',7,9)
    add('VII.Definition18',r'\bsquare numbers?\b',7,9)
    add('VII.Definition19',r'\bcube numbers?\b',7,9)
    add('VII.Definition20',r'\b(?:numbers? (?:are|be) )?proportional\b',7,9)
    add('VII.Definition21',r'\bsimilar (?:plane|solid) numbers?\b',7,9)
    add('VII.Definition22',r'\bperfect numbers?\b',7,9)
    add('X.Definition1.1',r'\b(?:in)?commensurable (?:magnitudes?|quantities)\b | \b(?:in)?commensurab(?:le|ility)\b',10,10)
    add('X.Definition1.2',r'\b(?:in)?commensurable in square\b',10,10)
    add('X.Definition1.3',r'\brational straight lines?\b | \birrational straight lines?\b',10,10)
    add('X.Definition1.4',r'\brational (?:areas?|squares?)\b | \birrational (?:areas?|squares?)\b',10,10)
    ords=('first','second','third','fourth','fifth','sixth')
    for n,word in enumerate(ords,1):
        add(f'X.Definition2.{n}',rf'\b{word} binomial(?: straight line)?\b',10,10)
        add(f'X.Definition3.{n}',rf'\b{word} apotome\b',10,10)
    add('XI.Definition1',r'\bsolid figures?\b | \bsolids?\b',11,13)
    add('XI.Definition2',r'\bextremit(?:y|ies) of (?:a |the )?solid\b',11,13)
    add('XI.Definition3',r'\bstraight lines? (?:are|is) at right angles to (?:a |the )?plane\b',11,13)
    add('XI.Definition4',r'\bplane (?:is|are) at right angles to (?:a |the )?plane\b',11,13)
    add('XI.Definition5',r'\binclination of (?:a |the )?straight line to (?:a |the )?plane\b',11,13)
    add('XI.Definition6',r'\binclination of (?:a |the )?plane to (?:a |the )?plane\b',11,13)
    add('XI.Definition7',r'\bsimilarly inclined\b',11,13)
    add('XI.Definition8',r'\bparallel planes?\b',11,13)
    add('XI.Definition9',r'\bsimilar solid figures?\b',11,13)
    add('XI.Definition10',r'\bequal and similar solid figures?\b',11,13)
    add('XI.Definition11',r'\bsolid angles?\b',11,13)
    add('XI.Definition12',r'\bpyramids?\b',11,13)
    add('XI.Definition13',r'\bprisms?\b',11,13)
    add('XI.Definition14',r'\bspheres?\b',11,13)
    add('XI.Definition15',r'\baxes? of (?:a |the )?spheres?\b',11,13)
    add('XI.Definition16',r'\bcent(?:er|re) of (?:a |the )?sphere\b',11,13)
    add('XI.Definition17',r'\bdiameters? of (?:a |the )?spheres?\b',11,13)
    add('XI.Definition18',r'\bcones?\b',11,13)
    add('XI.Definition19',r'\baxes? of (?:a |the )?cones?\b',11,13)
    add('XI.Definition20',r'\bbases? of (?:a |the )?cones?\b',11,13)
    add('XI.Definition21',r'\bcylinders?\b',11,13)
    add('XI.Definition22',r'\baxes? of (?:a |the )?cylinders?\b',11,13)
    add('XI.Definition23',r'\bbases? of (?:a |the )?cylinders?\b',11,13)
    add('XI.Definition24',r'\bsimilar cones? and cylinders?\b',11,13)
    add('XI.Definition25',r'\bcubes?\b',11,13)
    add('XI.Definition26',r'\boctahedr(?:on|a)\b',11,13)
    add('XI.Definition27',r'\bicosahedr(?:on|a)\b',11,13)
    add('XI.Definition28',r'\bdodecahedr(?:on|a)\b',11,13)
    return x


def select_lexical_concepts(body,book,aliases):
    """Keep specific spans when they entirely cover generic occurrences.

    If a whole composite phrase is a named concept, its substrings do not
    create independent input edges from that same occurrence. Other occurrences
    of the generic concept in the text can still create their own one edge.
    """
    hits=[]
    for did,rx,lo,hi in aliases:
        if not lo<=book<=hi:continue
        for m in re.finditer(rx,body,re.I):
            hits.append({'did':did,'start':m.start(),'end':m.end(),
                         'matched':m.group(0).lower(),'alias':rx})
    hits.sort(key=lambda h:(-(h['end']-h['start']),h['start'],h['did']))
    selected=[]
    for h in hits:
        if any(q['start']<=h['start'] and q['end']>=h['end'] and q['did']!=h['did'] for q in selected):
            continue
        selected.append(h)
    out={}
    for hit in sorted(selected,key=lambda h:(h['start'],h['did'])):
        did=hit['did'];out.setdefault(did,hit['matched'])
    return out


def load_reconciliation(path):
    with path.open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
    if len(rows)!=16:raise ValueError('Expected exactly 16 reconciliations')
    cross={}
    for r in rows:
        key=(r['proposition'],int(r['source_slot']))
        if key in cross:raise ValueError('Reused input slot')
        cross[key]=r
    return cross


def source_ref_unit(ref,defs):
    if not isinstance(ref,dict) or len(ref)<1:raise ValueError('Unsupported reference '+repr(ref))
    if 'Theorem' in ref:return f'{ROM[ref["Book"]]}.{ref["Theorem"]}'
    if 'Definition' in ref:
        did=f'{ROM[ref["Book"]]}.Definition{ref["Definition"]}'
        if did not in defs:raise ValueError('Unresolved definition '+did)
        return definition_unit(did)
    if 'Postulate' in ref:return f'P{ref["Postulate"]}'
    if 'Common Notion' in ref:return f'CN{ref["Common Notion"]}'
    raise ValueError('Unknown reference '+repr(ref))


def proof_cites(text):
    """Only exact numeric theorem references in proof bracket annotations."""
    rx=re.compile(r'(?<![A-Za-z])(?:XIII|XII|XI|VIII|VII|VI|IV|IX|III|II|X|V|I)\s*\.\s*\d{1,3}(?!\d)')
    output=[]
    for group in re.findall(r'\[([^\]]+)\]',text or ''):
        if re.search(r'\b(?:cf\.|lemma|corollary)\b',group,re.I):continue
        strip=re.sub(r'\b(?:XIII|XII|XI|X|IX|VIII|VII|VI|V|IV|III|II|I)\s*\.\s*Deff?s?\.\s*(?:(?:I|II|III|IV)\s*\.\s*)?\d+(?:\.\d+)?',' ',group,flags=re.I)
        for m in rx.findall(strip):
            a,b=m.replace(' ','').split('.')
            output.append(f'{a}.{int(b)}')
    return set(output)


def proof_definition_cites(text,defs,current_book):
    """Extract only proof-annotated definition mentions where address maps.

    Book X 'X. Def. 4' is the fourth member of Definitions I; this context
    is NOT generalized to other Books and not treated as a proposition cite.
    """
    result=[]
    for group in re.findall(r'\[([^\]]+)\]',text or ''):
        if re.search(r'\bcf\.',group,re.I):continue
        for special in re.finditer(r'\bX\s*\.\s*Deff?s?\s*\.\s*(II|III)\s*\.\s*(\d+)\b',group,re.I):
            n=int(special.group(2))
            did=f'X.Definition{2 if special.group(1).upper()=="II" else 3}.{n}'
            if did in defs:result.append((did,'['+group+']'))
        for m in re.finditer(r'\b(XIII|XII|XI|VIII|VII|VI|IV|IX|III|II|X|V|I)\s*\.\s*Deff?s?\s*\.\s*(\d+)(?:\.(\d+))?',group,re.I):
            b=ROM.index(m.group(1).upper());n=int(m.group(2));decimal=m.group(3)
            if b==10 and n in (1,2,3,4) and decimal is None:
                did=f'X.Definition1.{n}'
            elif decimal is not None:
                did=f'{ROM[b]}.Definition{n}.{int(decimal)}'
            else:did=f'{ROM[b]}.Definition{n}'
            if did in defs:result.append((did,'['+group+']'))
        for local in re.finditer(r'(?<![A-Za-z.])Def\s*\.\s*(\d+)\b',group,re.I):
            did=f'{ROM[current_book]}.Definition{int(local.group(1))}'
            if did in defs:result.append((did,'['+group+']'))
    return result


def build(props,defs,aux,cross,include_wide=True):
    aliases=collect_aliases();units={definition_unit(d) for d in defs}
    nodes=set(props)|units|set(aux)
    if not {'I.Definition1','I.Definition4','X.Definitions_I'}<=nodes:raise ValueError('Required roots missing')
    edges=defaultdict(lambda:{'provenance':set(),'details':set(),'concepts':set()})
    def add(src,tgt,how,detail='',concept=''):
        if src not in nodes or tgt not in (set(props)|set(aux)):raise ValueError('Missing graph node: '+str((src,tgt)))
        if src==tgt:raise ValueError('Self citation '+src)
        z=edges[(src,tgt)];z['provenance'].add(how)
        if detail:z['details'].add(str(detail))
        if concept:z['concepts'].add(concept)
    for pid,entry in props.items():
        book=entry['key']['Book'];v=entry['value'];text=v.get('Text') or '';proof=v.get('Proof') or ''
        for slot,ref in enumerate(v.get('References') or [],1):
            if isinstance(ref,list):
                if pid!='IV.10' or not {'II.11','III.32'} <= proof_cites(proof):
                    raise ValueError('Unsupported special ref '+pid)
                for target in ('II.11','III.32'):
                    add(target,pid,'source_special_proof_confirmed',f'slot={slot}')
                continue
            if (pid,slot) in cross:
                r=cross[(pid,slot)];did=r['reconciled_definition']
                if did not in defs:raise ValueError('Crosswalk target absent')
                add(definition_unit(did),pid,'source_id_reconciled',f'slot={slot};{r["proof_evidence"]}',did)
            else:
                origin=source_ref_unit(ref,defs)
                add(origin,pid,'source_references',f'slot={slot}',str(ref))
        if include_wide:
            for source in sorted(proof_cites(proof),key=order):
                if source in props and source!=pid:
                    add(source,pid,'proof_bracket_citation','[exact theorem label]')
            for did,quote in proof_definition_cites(proof,defs,book):
                add(definition_unit(did),pid,'proof_bracket_definition',quote,did)
            for did,hit in select_lexical_concepts(text+' '+proof,book,aliases).items():
                if did not in defs:raise ValueError('Alias points to absent '+did)
                add(definition_unit(did),pid,'concept_lexical_wide',hit,did)
    if include_wide:
        # Human permits later editions. This is a named, not generalized, addition.
        # Joyce lists P1 and CN5; Lardner 1855 lists I.3 and I.4.
        for src in ('I.3','I.4'):
            add(src,'I.6','later_edition_Lardner1855','I.6 proof annotations')
        for src in ('P1','CN5'):
            add(src,'I.6','later_editor_Joyce','I.6 modern explanatory notes')
        # Postulates use defined concepts directly. In particular P1=point+straight line.
        for pid,entry in aux.items():
            book=1
            for did,hit in select_lexical_concepts(entry['value'].get('Text') or '',book,aliases).items():
                add(definition_unit(did),pid,'concept_lexical_wide',hit,did)
    return nodes,edges,aliases


def path_counts(nodes,edges):
    parents={n:set() for n in nodes}; children={n:set() for n in nodes}
    for src,tgt in edges:
        parents[tgt].add(src);children[src].add(tgt)
    waiting={n:len(parents[n]) for n in nodes}
    queue=deque(sorted(n for n in nodes if waiting[n]==0))
    values={};topo=[]
    while queue:
        n=queue.popleft();topo.append(n)
        values[n]=1 if not parents[n] else sum(values[src] for src in parents[n])
        for ch in sorted(children[n]):
            waiting[ch]-=1
            if waiting[ch]==0:queue.append(ch)
    if len(topo)!=len(nodes):
        rem=[n for n in nodes if n not in values]
        raise ValueError('SEMANTIC_OR_SOURCE_CYCLE: finite path count is undefined for '+str(rem[:30]))
    return values,parents,children


def read_alpha_exergy(path):
    with path.open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
    return {r['proposition']:r for r in rows}


def check_alpha_graph(props,ref_edges,alpha):
    # Recheck the recorded-only theorem graph against archived exergy, not the
    # wide additions. An independent topological transitive closure confirms.
    graph={p:set() for p in props}
    for src,tgt in ref_edges:
        if src in props and tgt in props:graph[src].add(tgt)
    if sum(map(len,graph.values()))!=1639:raise ValueError('Recorded alpha theorem graph changed')
    cache={}
    def reach(n):
        if n not in cache:
            visited=set();todo=list(graph[n])
            while todo:
                nxt=todo.pop()
                if nxt in visited:continue
                visited.add(nxt);todo.extend(graph[nxt]-visited)
            cache[n]=visited
        return cache[n]
    for n in props:
        if len(reach(n))!=int(alpha[n]['beta_exergy_distinct_descendants_source_references']):
            raise ValueError('Alpha exergy mismatch for '+n)
    return sum(map(len,cache.values()))


def csv_write(path,head,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=head,extrasaction='ignore')
        w.writeheader();w.writerows(rows)


def run(source,reconfile,alphafile,out):
    sha,props,defs,aux=load_source(source)
    cross=load_reconciliation(reconfile)
    alpha=read_alpha_exergy(alphafile)
    if set(alpha)!=set(props):raise ValueError('Alpha/exergy coverage mismatch')
    nodes0,ed0,_=build(props,defs,aux,cross,include_wide=False)
    values0,parents0,_=path_counts(nodes0,ed0)
    exergy_pairs=check_alpha_graph(props,ed0,alpha)
    nodes,ed,aliases=build(props,defs,aux,cross,include_wide=True)
    values,parents,children=path_counts(nodes,ed)
    if nodes0!=nodes:raise ValueError('Node set changed')
    if values['P1']!=2:raise ValueError('Human P1=2 check failed: '+str(values['P1']))
    if any(values[p]<values0[p] for p in props):raise ValueError('Wide count smaller than recorded')
    props_sorted=sorted(props,key=order)
    result=[]
    for pid in props_sorted:
        a=alpha[pid];p=parents[pid];channels=Counter()
        for e in p:
            channels.update(ed[(e,pid)]['provenance'])
        result.append({
            'proposition':pid,
            'alpha_recorded_proof_cut_lost_including_self':a['alpha_recorded_proof_cut_lost_including_self'],
            'alpha_spine_necessity_status':a['alpha_spine_necessity_status'],
            'beta_exergy_recorded_distinct_descendants':a['beta_exergy_distinct_descendants_source_references'],
            'beta_exergy_two_proof_supplements':a['beta_exergy_distinct_descendants_with_two_proof_text_supplements'],
            'beta_entropy_references_and_auxiliary_only':values0[pid],
            'beta_entropy_wide_admitted_concepts':values[pid],
            'wide_minus_reference_count':values[pid]-values0[pid],
            'direct_parents_recorded_count':len(parents0[pid]),
            'direct_parents_wide_count':len(p),
            'source_free_in_recorded_model':int(len(parents0[pid])==0),
            'source_free_in_wide_model':int(len(p)==0),
            'source_free_status_changed':int((len(parents0[pid])==0)!=(len(p)==0)),
            'direct_parents_theorems':sum(s in props for s in p),
            'direct_parents_definition_units':sum(s in {definition_unit(d) for d in defs} for s in p),
            'direct_parents_postulates_common_notions':sum(s in aux for s in p),
            'active_concept_lexical_edges':sum('concept_lexical_wide' in ed[(s,pid)]['provenance'] for s in p),
            'active_proof_annotation_edges':sum('proof_bracket_citation' in ed[(s,pid)]['provenance'] or 'proof_bracket_definition' in ed[(s,pid)]['provenance'] for s in p),
            'calculation_scope':'provisional_direct_concept_wide;NOT_complete_semantic_audit',
        })
    head=list(result[0]);csv_write(out/'euclid_465_alpha_beta_entropy_exergy.csv',head,result)
    edgerows=[]
    for (src,tgt),data in sorted(ed.items(),key=lambda kv:(order(kv[0][1]) if kv[0][1] in props else (0,0),kv[0][0])):
        edgerows.append({'source':src,'target':tgt,
                         'provenance':';'.join(sorted(data['provenance'])),
                         'source_concept_ids':';'.join(sorted(data['concepts'])),
                         'evidence_example':';'.join(sorted(data['details']))[:600],
                         'counted_once':1})
    csv_write(out/'euclid_465_beta_entropy_direct_edges.csv',list(edgerows[0]),edgerows)
    aliasrows=[{'concept_id':did,'count_unit':definition_unit(did),'regex':rx,
                'valid_from_book':ROM[lo],'valid_to_book':ROM[hi]}
               for did,rx,lo,hi in aliases]
    csv_write(out/'euclid_beta_concept_aliases.csv',list(aliasrows[0]),aliasrows)
    counts=Counter()
    for val in ed.values():counts.update(val['provenance'])
    matching_alias=set()
    for z in ed.values():
        if 'concept_lexical_wide' in z['provenance']:
            matching_alias.update(d for d in z['concepts'] if d in defs)
    manifest={
        'status':'PROVISIONAL_BETA_ENTROPY_465_COMPUTED_WIDE_POLICY',
        'scope_statement':'Numbers model admitted evidence/lexical concepts; not fully exhaustive meaning and not proof validity or mathematical upper bounds.',
        'source_sha256':sha,
        'source_url':'https://www.wolframcloud.com/obj/4577bf25-6f1c-4b29-98ca-12877d908956',
        'later_annotation_sources':{
            'Lardner_1855_I6':'https://www.maths.tcd.ie/~dwilkins/Courses/MA232A/Euclid_ETexts/EuclidBookI_Lardner1855/EuclidBookIProp06_Lardner1855.php',
            'Joyce_I6':'https://www.euclids-elements.org/elements/books/bookI/propositions/propI6/'},
        'user_decision':'Within interpretations of the SAME problem choose the largest supported path count. Do NOT merge semantically different concepts just to inflate a number.',
        'scope':{'theorems':465,'definitions':132,'postulates':5,'common_notions':5,'count_units':len({definition_unit(d) for d in defs}),
                 'theorem_graph_recorded_edges':1639,'exergy_ordered_pairs_recorded':exergy_pairs,
                 'entropy_reference_edges':len(ed0),'entropy_wide_edges':len(ed),
                 'counted_proof_or_lexical_edge_channels':dict(counts),
                 'explicit_16_definition_id_crosswalk':len(cross),
                 'lexical_alias_entries':len(aliases),
                 'distinct_definitions_matched_by_lexicon':len(matching_alias),
                 'numbers_with_at_least_one_lexical_concept':sum(r['active_concept_lexical_edges']>0 for r in result),
                 'source_free_recorded_theorems':sum(r['source_free_in_recorded_model'] for r in result),
                 'source_free_wide_theorems':sum(r['source_free_in_wide_model'] for r in result),
                 'theorems_whose_source_free_class_changes':sum(r['source_free_status_changed'] for r in result)},
        'models':{'recorded':'References and aux aliases only. It is NOT a proven lower bound on all mathematical derivations.',
                  'wide':'References plus proof annotations, explicit contextual definition wording, selected named later-edition I.6 premises, and conservative context-bounded lexical concept matches. Comparable alternative direct references deduplicated by count unit; does not claim all meanings captured.'},
        'example_counts':{k:{'entropy_recorded':values0[k],'entropy_wide':values[k],
                             'exergy_recorded':int(alpha[k]['beta_exergy_distinct_descendants_source_references'])}
                          for k in ('I.1','I.4','I.6','I.47','VI.31','X.15','XIII.18')},
        'source_free_class_changed_ids':[r['proposition'] for r in result if r['source_free_status_changed']],
        'top_10_entropy': [{'proposition':r['proposition'],'entropy':r['beta_entropy_wide_admitted_concepts']} for r in sorted(result,key=lambda r:-r['beta_entropy_wide_admitted_concepts'])[:10]],
        'boundary_cases':[
            'Only semantically compatible alternatives can be maximized; no blanket match of ambiguous labels (e.g. X rational lines versus areas).',
            'X.Definitions I subdefinitions 1.1-1.4 count as one parent origin per target, but their distinct conceptual identity is recorded.',
            'Broad name matching across all 132 definitions is neither certified exhaustive nor equivalent to semantic entailment.',
            'I.6 receives named later-edition premise candidates, not a fictional Euclid direct citation.',
            'No independent source H=1 automatically adds to a derived proposition H unless it is truly source-free.',
            'Recorded alpha necessity is unresolved. Exergy counts recorded descendants, not all possible derivations.',
            'Some plausibly implicit proof premises remain uncatalogued; current wide model is not a global maximum.',
            'Observed zero-reference theorem records become concept-supported in the wide model; this is a qualitative change of source-free classification, not proof of logical dependency.',
            'A future-pointing source label X.11 -> X.10 is retained because it is in the reference field and does not make a cycle; this historical/source anomaly is not repaired.',
        ],
        'user_repository_applied':False,
    }
    with (out/'euclid_beta_entropy_manifest.json').open('w',encoding='utf-8') as f:
        json.dump(manifest,f,ensure_ascii=False,indent=2);f.write('\n')
    print(json.dumps({'input_sha256':sha,'theorem_count':len(props),
                      'P1_entropy':values['P1'],'recorded_edges':len(ed0),'wide_edges':len(ed),
                      'counts_by_channel':dict(counts),
                      'example_counts':manifest['example_counts'],
                      'source_free_class_changed_ids':[r['proposition'] for r in result if r['source_free_status_changed']],
        'top_10_entropy':manifest['top_10_entropy'][:3]},indent=2))
    return manifest


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--source',required=True,type=Path)
    p.add_argument('--reconciliation',required=True,type=Path)
    p.add_argument('--alpha-exergy',required=True,type=Path)
    p.add_argument('--output',required=True,type=Path)
    args=p.parse_args()
    args.output.mkdir(parents=True,exist_ok=True)
    run(args.source,args.reconciliation,args.alpha_exergy,args.output)

if __name__=='__main__':main()

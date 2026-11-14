#!/usr/bin/env python3
"""SO text-only dictionary compiler. Reference glossary is NEVER a build input.

prepare: repository bytes -> content-only examples, source sidecar, lexical drafts.
finish: replay source-grounded editorial updates -> pointer-free dictionary.
compare: read a reference glossary ONLY AFTER verifying the dictionary freeze.

Only Python standard library is required. The code does not call an LLM.
Editorial updates are an explicitly saved AI-authored artifact, not disguised
as deterministic semantic inference. Replaying them is not a fresh LLM run.
"""
from __future__ import annotations
import argparse
import collections
import csv
import hashlib
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'tools' / 'assessment' / 'term_dictionary' / 'data'
KANJI = r'\u3400-\u4dbf\u4e00-\u9fff\u3005\u3007\u3006'
KATA = r'\u30a1-\u30fa\u30fc'
HIRA = r'\u3041-\u3096'
JP = re.compile('[' + KANJI + HIRA + KATA + ']')
PIECES = re.compile('['+KANJI+']+|['+KATA+']+|['+HIRA+']+|[A-Za-z][A-Za-z0-9_+-]*|[\u03b1-\u03c9\u0391-\u03a9]+|[0-9]+(?:[.][0-9]+)*|[\u2190-\u21ff\u2200-\u22ff]')
COMPOUNDS = re.compile('['+KANJI+KATA+']{2,40}')
FUNCTIONS = ['である','ではない','とは','として','において','だけでは','によって','必要である','とは限らない','しながら','したがって','しかし','ならば','であれば','のみ','ない','する','なる','いる','ある','は','が','を','に','の','と','も','へ','で','や']
SOURCE_FIELDS = {'source','source_path','file','path','line','line_start','line_end','source_id','source_ids','unit_id','unit_ids','citation','citations','owner','authority','definition_owner','references','url','href'}
REF_HEADING = re.compile(r'(?:参考文献|参照文献|主要参照|参照基盤|関連文書|関連資料|関連リンク|文書内リンク|改訂履歴|変更履歴|References|Related Documents|Revision History)', re.I)
META = re.compile(r'^(?:Status|Layer|Scope|Language|Claim strength|Authority|Revision|Version|Last updated|Lifecycle|Canonical scope|Definition ownership|Maintenance|Public handling|Formation provenance|Non-claim|Reading rule|Revision rule)\s*:',re.I)
PATH_TOKEN = re.compile(r'(?:[\w\-.\u3000\u3400-\u9fff\u3040-\u30ff]+[/\\])*[\w\-.\u3000\u3400-\u9fff\u3040-\u30ff]+\.(?:md|html?|jsonl?|ya?ml|csv|tsv|py|zip|svg|graphml)(?:#[^\s`）)]+)?',re.I)


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def digest(text: str) -> str:
    return sha_bytes(text.encode('utf-8'))


def dump_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n',encoding='utf-8',newline='\n')


def dump_lines(path: Path, rows) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w',encoding='utf-8',newline='\n') as f:
        for row in rows:
            f.write(json.dumps(row,ensure_ascii=False,separators=(',',':'))+'\n')


def load_lines(path: Path):
    with path.open(encoding='utf-8') as f:
        return [json.loads(x) for x in f if x.strip()]


def safe_path(root: Path, name: str) -> Path:
    p=(root/name).resolve()
    if root.resolve() not in p.parents:
        raise ValueError('Outside repository: '+name)
    return p


def clean_inline(line: str) -> str:
    line=re.sub(r'`[^`\n]*\.(?:md|html?|jsonl?|ya?ml|csv|tsv|py|zip|svg|graphml)[^`\n]*`','\u3014\u6240\u5728\u60c5\u5831\u7701\u7565\u3015',line)
    line=re.sub(r'!\[[^\]]*\]\([^)]*\)','',line)
    line=re.sub(r'\[([^\]]+)\]\([^)]*\)',r'\1',line)
    line=re.sub(r'https?://[^\s)）<>]+','',line)
    line=PATH_TOKEN.sub('〔所在情報省略〕',line)
    line=re.sub(r'(?:0[0-9]|90)_[A-Za-z0-9_]+/(?:[A-Za-z0-9_.*-]+/?)*','〔所在情報省略〕',line)
    line=re.sub(r'<[^>]+>','',line)
    line=re.sub(r'\[\^[^\]]+\]','',line)
    line=re.sub(r'^\s*(?:>\s*)+','',line)
    line=re.sub(r'^\s*(?:[-*+]\s+|[0-9]+[.)]\s+)','',line)
    line=re.sub(r'^\s*[0-9]+(?:\.[0-9]+)*[\s\u3000]+','',line)
    line=line.replace('**','').replace('__','').replace('`','')
    line=re.sub(r'\{#[^}]+\}','',line)
    return line.strip()


def split_sentences(text: str):
    # Keep punctuation inside quotations; no grammatical interpretation.
    out=[]; start=0; stack=[]; pairs={'「':'」','『':'』','（':'）','(' : ')','【':'】','[':']'}
    for i,c in enumerate(text):
        if c in pairs: stack.append(pairs[c])
        elif stack and c==stack[-1]:stack.pop()
        if c in '。！？' and not stack:
            s=text[start:i+1].strip()
            if s:out.append(s)
            start=i+1
    tail=text[start:].strip()
    if tail:out.append(tail)
    return out


def paragraphs(raw: str):
    """Yield content and source span; strip external navigation, not prose claims."""
    result=[]; omissions=[]; buf=[]; begin=None; fence=False; math=False; excluded_heading=None
    for n,line in enumerate(raw.splitlines(),1):
        stripped=line.strip()
        heading=re.match(r'^(#{1,6})\s+(.*)',stripped)
        if heading:
            if buf:result.append((' '.join(buf),begin,n-1));buf=[];begin=None
            level=len(heading.group(1))
            if excluded_heading is not None and level<=excluded_heading:excluded_heading=None
            if REF_HEADING.search(heading.group(2)):excluded_heading=level
            omissions.append((n,'heading_or_reference_section'))
            continue
        if excluded_heading is not None:
            omissions.append((n,'reference_section'));continue
        if stripped.startswith(('```','~~~')):
            if buf:result.append((' '.join(buf),begin,n-1));buf=[];begin=None
            fence=not fence;omissions.append((n,'fenced_block'));continue
        if fence:omissions.append((n,'fenced_block'));continue
        if stripped=='$$':math=not math;omissions.append((n,'display_math'));continue
        if math:omissions.append((n,'display_math'));continue
        stripped=re.sub(r'^>\s*','',stripped)
        if META.match(stripped) or re.match(r'^(?:\u72b6\u614b|\u5c64|\u8a00\u8a9e|\u9069\u7528\u7bc4\u56f2|\u6a29\u9650|Current definition owner|Source of release facts|Definition ownership)\s*[:\uff1a]',stripped) or re.match(r'^\[\^?[^\]]+\]:',stripped):
            omissions.append((n,'metadata_or_footnote_reference'));continue
        if not stripped or re.fullmatch(r'[-*_\s]+',stripped):
            if buf:result.append((' '.join(buf),begin,n-1));buf=[];begin=None
            continue
        # Links standing alone are navigation, not training examples.
        if re.fullmatch(r'(?:[-*]\s*)?\[[^\]]+\]\([^)]*\)[。.]?',stripped):
            omissions.append((n,'navigation_link'));continue
        cleaned=clean_inline(line)
        if not JP.search(cleaned):
            omissions.append((n,'non_japanese_line'));continue
        if not cleaned.replace('〔所在情報省略〕','').strip(' |:'):
            omissions.append((n,'pointer_only'));continue
        if line.lstrip().startswith('|'):
            if buf:result.append((' '.join(buf),begin,n-1));buf=[];begin=None
            if not re.fullmatch(r'[|:\-\s]+',cleaned):result.append((cleaned,n,n))
            continue
        if begin is None:begin=n
        buf.append(cleaned)
    if buf:result.append((' '.join(buf),begin,len(raw.splitlines())))
    return result,omissions


def headword_candidates(text: str):
    """Finite, declared surface inventory, not a claim of perfect Japanese word segmentation."""
    pairs={}
    for m in PIECES.finditer(text):
        t=m.group()
        if t=='所在情報省略':continue
        pairs.setdefault(t,'surface_run')
    for m in COMPOUNDS.finditer(text):
        t=m.group()
        if t!='所在情報省略':pairs.setdefault(t,'compound_run')
    for t in FUNCTIONS:
        if t in text:pairs.setdefault(t,'function_expression')
    for m in re.finditer(r'[「『]([^「」『』。！？\n]{1,40})[」』]',text):
        t=m.group(1).strip()
        if t and not any(x in t for x in ['〔所在','://','.md']):pairs.setdefault(t,'quoted_expression')
    return pairs


def explicit_definitions(sentence: str):
    """Literal source claims only. Alternatives are NOT assumed equivalent."""
    if re.search(r'とは(?:限ら|異な|違|別|無関係|主張しない|言えない)', sentence):
        return []
    found=[]
    text=re.sub(r'^(?:ここでいう|ここでの|本稿でいう|本書でいう|本モデルにおける|本原則における|本稿における|そして|つまり|したがって)\s*','',sentence)
    patterns=[
      r'^[「『]?([^。！？、，,：:「」『』]{1,24}?)[」』]?とは[、，,\s]*(.{5,})$',
      r'^[「『]?([^。！？、，,：:「」『』]{1,24}?)[」』]?[：:]\s*(.{5,})$',
    ]
    excluded={'注意','例','補足','Decision','Proposal','Recheck condition','Current definition owner','Display name','Related application','Revision note','参照','定義語','文書の位置づけ','状態','日本語正本語','Source boundary','Source of release facts','Claim phase','Residual','Safeguard','Rule','Notation rule','Non-claim boundary'}
    for pat in patterns:
        m=re.match(pat,text)
        if not m:continue
        term=m.group(1).strip();rest=m.group(2).strip()
        if term in excluded or re.fullmatch(r'注[0-9]+',term):continue
        if term.endswith('こ') or term.startswith('$'):continue
        if any(x in term for x in ['〔','|','=','\\','http','が','を','は','である','こと']):continue
        if not JP.search(rest) or len(rest.replace('〔所在情報省略〕','').strip())<5:continue
        if rest.endswith(('として、','として','ではなく、','次である。','次のものである。')):continue
        found.append((term,sentence));break
    return found

def prepare(repo: Path, plan_path: Path, out: Path) -> dict:
    plan=json.loads(plan_path.read_text('utf-8'));out.mkdir(parents=True,exist_ok=True)
    units=[]; source_map=[]; omitted=[]; corpus_docs=[]
    for record in plan['files']:
        if record['selection']!='include':continue
        path=safe_path(repo,record['path']);data=path.read_bytes()
        if sha_bytes(data)!=record['sha256']:raise ValueError('Source changed: '+record['path'])
        paras, omissions=paragraphs(data.decode('utf-8-sig'))
        corpus_docs.append({'path':record['path'],'sha256':record['sha256'],'paragraphs':len(paras)})
        for p,a,b in paras:
            sentences=split_sentences(p)
            for s in sentences:
                if not JP.search(s):continue
                units.append({'text':s})
                source_map.append({'sequence':len(units),'text_sha256':digest(s),'source_path':record['path'],'line_start':a,'line_end':b,'paragraph':p,'stage':record.get('stage','other'),'layer':record.get('layer','unknown')})
        omitted.extend({'source_path':record['path'],'line':n,'reason':why} for n,why in omissions)
    dump_lines(out/'input_sentences.jsonl',units)
    dump_lines(out/'source_map.jsonl',source_map)
    dump_lines(out/'excluded_lines.jsonl',omitted)
    # Pass one: build only from text, in input order. No reference names or pointers.
    terms={}; observations=[]; events=[]; seen_sentence=set(); total_hits=0
    for seq,unit in enumerate(units,1):
        text=unit['text']; h=digest(text); unique=h not in seen_sentence; seen_sentence.add(h)
        cs=headword_candidates(text)
        defs=explicit_definitions(text)
        for term,_ in defs:cs[term]='definition_headword'
        for term,kind in cs.items():
            if not term or len(term)>64:continue
            first=term not in terms
            d=terms.setdefault(term,{'term':term,'kinds':set(),'count':0,'unique_examples':0,'examples':[],'example_hashes':set(),'definition_candidates':[],'definition_hashes':set(),'first_seen':seq,'last_change':seq})
            d['kinds'].add(kind);d['count']+=text.count(term);total_hits+=text.count(term)
            if h not in d['example_hashes']:
                d['unique_examples']+=1;d['example_hashes'].add(h)
                if len(d['examples'])<5:d['examples'].append(text)
            observations.append({'sequence':seq,'term':term,'kind':kind,'count':text.count(term),'text_sha256':h})
            if first:events.append({'sequence':seq,'term':term,'operation':'register_surface','after':{'definition':None}})
        for term,definition in defs:
            d=terms[term];dh=digest(definition)
            if dh not in d['definition_hashes']:
                d['definition_candidates'].append(definition);d['definition_hashes'].add(dh);d['last_change']=seq
                events.append({'sequence':seq,'term':term,'operation':'append_literal_definition_candidate','after':{'definition':definition}})
    # Compound/discovered heads are located against the text corpus, NOT against the glossary.
    # No frequency cutoff; uncommon/isolated spans remain visible.
    lex=[]; drafts=[]
    for term,d in sorted(terms.items()):
        lex.append({'term':term,'kinds':sorted(d['kinds']),'occurrences_in_extracted_units':d['count'],'distinct_examples':d['unique_examples'],'first_seen':d['first_seen'],'last_definition_change':d['last_change'],'examples':d['examples'],'literal_candidates':d['definition_candidates']})
        cand=d['definition_candidates']
        drafts.append({'term':term,'status':'literal_candidates' if cand else 'usage_only','definition':None,'senses':[{'definition':s,'mode':'literal_candidate'} for s in cand],'notes':[]})
    dump_lines(out/'lexicon_observations.jsonl',lex)
    dump_lines(out/'occurrence_ledger.jsonl',observations)
    dump_lines(out/'automatic_drafts.jsonl',drafts)
    dump_lines(out/'formation_log.jsonl',events)
    summary={'source_archive_sha256':plan['archive_sha256'],'input_files':len(corpus_docs),'excluded_files':sum(r['selection']!='include' for r in plan['files']),'input_sentence_units':len(units),'distinct_sentence_texts':len(seen_sentence),'surface_candidates':len(terms),'literal_definition_headwords':sum(bool(d['definition_candidates']) for d in terms.values()),'literal_definition_sentences':sum(len(d['definition_candidates']) for d in terms.values()),'text_only_input_sha256':sha_bytes((out/'input_sentences.jsonl').read_bytes()),'lexical_rule':'Unicode script runs + compounds + quoted expressions + fixed function-expression forms; NOT exhaustive morphological word recognition','reference_glossary_read':False,'source_pointers_passed_to_reducer':False,'source_files':corpus_docs}
    dump_json(out/'intake_summary.json',summary)
    return {k:v for k,v in summary.items() if k!='source_files'}


def assert_no_pointers(x):
    if isinstance(x,dict):
        for k,v in x.items():
            if k in SOURCE_FIELDS:raise ValueError('Pointer field in dictionary: '+k)
            assert_no_pointers(v)
    elif isinstance(x,list):
        for v in x:assert_no_pointers(v)
    elif isinstance(x,str):
        if re.search(r'https?://|(?:^|[\s`])(?:0[0-9]|90)_[^\s]*[/\\]|\.(?:md|json|html)(?:#|[\s`]|$)',x):
            raise ValueError('Pointer text in dictionary: '+x[:100])


def finish(stage: Path, updates_path: Path, out: Path) -> dict:
    out.mkdir(parents=True,exist_ok=True)
    source_units=load_lines(stage/'input_sentences.jsonl')
    source_texts={digest(u['text']):u['text'] for u in source_units}
    last_sequence={u['text']:i for i,u in enumerate(source_units,1)}
    entries={d['term']:d for d in load_lines(stage/'automatic_drafts.jsonl')}
    updates=load_lines(updates_path) if updates_path.exists() else []
    history=[]; proof=[]
    for i,u in enumerate(updates,1):
        term=u['term']; supporting=u['evidence_texts']
        if not supporting:raise ValueError('No evidence: '+term)
        for s in supporting:
            if digest(s) not in source_texts:raise ValueError('Evidence not in content input: '+term+' / '+s[:100])
        if not any(term in s for s in supporting):raise ValueError('Headword absent from own evidence: '+term)
        previous=entries.get(term,{'term':term,'status':'usage_only','definition':None,'senses':[],'notes':[]})
        entry={'term':term,'status':u.get('status','editorial_candidate'),'definition':u['definition'],'senses':u.get('senses',[]),'notes':u.get('notes',[])}
        assert_no_pointers(entry)
        entries[term]=entry
        history.append({'revision':i,'batch':u.get('batch',1),'term':term,'operation':'create_or_revise_editorial_candidate','before':previous,'after':entry,'reason':u.get('reason','用例からの定義整理')})
        proof.append({'revision':i,'term':term,'evidence_text_sha256':[digest(s) for s in supporting],'evidence_texts':supporting,'last_evidence_sequence':max(last_sequence[t] for t in supporting)})
    rows=sorted(entries.values(),key=lambda d:d['term'])
    for row in rows:assert_no_pointers(row)
    dump_lines(out/'dictionary.jsonl',rows)
    dump_lines(out/'definition_revision_log.jsonl',history)
    dump_lines(out/'definition_evidence_sidecar.jsonl',proof)
    summary=json.loads((stage/'intake_summary.json').read_text('utf-8'))
    summary.pop('source_files',None)
    summary.update({'dictionary_entries':len(rows),'editorial_entries':sum(d['status']=='editorial_candidate' for d in rows),'literal_only_entries':sum(d['status']=='literal_candidates' for d in rows),'usage_only_entries':sum(d['status']=='usage_only' for d in rows),'editorial_revisions':len(history),'definition_convergence_claim':'not established; update history and unresolved alternatives are retained','dictionary_sha256':sha_bytes((out/'dictionary.jsonl').read_bytes()),'editorial_updates_sha256':sha_bytes(updates_path.read_bytes()) if updates_path.exists() else None,'reference_used_to_select_or_edit_definitions':False})
    dump_json(out/'dictionary_freeze.json',summary)
    return summary


def compare(dictionary: Path, freeze_path: Path, reference: Path, out: Path):
    frozen=json.loads(freeze_path.read_text('utf-8'))
    if sha_bytes(dictionary.read_bytes())!=frozen['dictionary_sha256']:raise ValueError('Dictionary changed after freeze')
    # Isolated comparison. No call to finish(), no mutation of the created dictionary.
    raw=reference.read_text('utf-8-sig');rows=load_lines(dictionary);by_term={x['term']:x for x in rows}
    chunks=[]; title=None;buf=[]
    for line in raw.splitlines():
        m=re.match(r'^#{2,4}\s+(.+)',line)
        if m:
            if title:chunks.append((title,'\n'.join(buf)))
            title=m.group(1);buf=[]
        else:buf.append(line)
    if title:chunks.append((title,'\n'.join(buf)))
    comparisons=[]
    for title,body in chunks:
        labels=[clean_inline(x).strip() for x in re.split(r'\s+/\s+|\s*[／|]\s*',title)]
        matches=[]
        for label in labels:
            label=re.sub(r'^\d+(?:\.\d+)*[.)]?\s*','',label)
            label=re.sub(r'\s*\([^)]*\)\s*$','',label)
            if label in by_term:matches.append(label)
        comparisons.append({'reference_heading':title,'exact_label_matches':sorted(set(matches)),'created_statuses':{t:by_term[t]['status'] for t in matches},'semantic_equivalence':'not_adjudicated'})
    result={'reference_sha256':sha_bytes(reference.read_bytes()),'dictionary_sha256':frozen['dictionary_sha256'],'phase':'post_freeze_comparison_only','reference_sections':len(chunks),'sections_with_exact_label_match':sum(bool(x['exact_label_matches']) for x in comparisons),'comparisons':comparisons}
    dump_json(out,result);return {k:v for k,v in result.items() if k!='comparisons'}


def main():
    p=argparse.ArgumentParser(description=__doc__);sp=p.add_subparsers(dest='command',required=True)
    a=sp.add_parser('prepare');a.add_argument('--repo-root',type=Path,default=ROOT);a.add_argument('--plan',type=Path,default=DATA/'source_plan.json');a.add_argument('--out',type=Path,required=True)
    a=sp.add_parser('finish');a.add_argument('--stage',type=Path,required=True);a.add_argument('--updates',type=Path,default=DATA/'editorial_updates.jsonl');a.add_argument('--out',type=Path,required=True)
    a=sp.add_parser('compare');a.add_argument('--dictionary',type=Path,required=True);a.add_argument('--freeze',type=Path,required=True);a.add_argument('--reference',type=Path,required=True);a.add_argument('--out',type=Path,required=True)
    args=p.parse_args()
    if args.command=='prepare':r=prepare(args.repo_root,args.plan,args.out)
    elif args.command=='finish':r=finish(args.stage,args.updates,args.out)
    else:r=compare(args.dictionary,args.freeze,args.reference,args.out)
    print(json.dumps(r,ensure_ascii=False,indent=2))
if __name__=='__main__':main()

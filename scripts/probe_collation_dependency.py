#!/usr/bin/env python3
"""Source-grounded, bounded lexical dependency and use-convergence pilot.

No interpretation of source statements is endorsed. Definition edges are
literal references within a candidate definition sentence, not proof,
necessity, or confirmed lexical identity. Corpus specificity and surface
rules are part of the experiment. Python 3.10+; standard library only.

Requires scripts/probe_sentence_dictionary.py from the previous pilot.
"""
from __future__ import annotations

import argparse
import collections
import csv
import itertools
import hashlib
import json
import random
import re
import xml.etree.ElementTree as ET
from pathlib import Path

from probe_sentence_dictionary import parse_sentences

SOURCE_REL = '01_Sat_Truth/Boundary_Epistemological_Critique.ja.md'
EXPECTED_SHA256 = '2f902285215ffac36f850cc118034787244f1c882f9274549da468960059d534'
ROOT = '\u7167\u5408'
SYNC = '\u540c\u671f'
RESIDUAL = '\u6b8b\u5dee'
MATCH = '\u4e00\u81f4'
MISMATCH = '\u4e0d\u4e00\u81f4'
MORE = (
    ROOT, SYNC, RESIDUAL, MATCH, MISMATCH,
    '\u89b3\u6e2c', '\u5206\u985e', '\u610f\u5473',
    '\u5c65\u6b74\u5834', '\u5c65\u6b74',
    '\u5185\u90e8\u30d2\u30e5\u30fc\u30ea\u30b9\u30c6\u30a3\u30c3\u30af',
    '\u5916\u90e8\u30d2\u30e5\u30fc\u30ea\u30b9\u30c6\u30a3\u30c3\u30af',
    '\u518d\u7167\u5408', '\u518d\u7167\u5408\u53ef\u80fd\u6027',
    '\u7167\u5408\u898f\u5247', '\u7167\u5408\u624b\u9806',
    '\u7167\u5408\u4e0d\u80fd', '\u4fdd\u6301', '\u66f4\u65b0',
    '\u77e5', '\u8a8d\u8b58', '\u5224\u65ad\u53ef\u80fd\u6027',
    '\u89e3\u91c8', '\u904e\u7a0b', '\u6761\u4ef6',
    '\u6bd4\u8f03', '\u9589\u9396', '\u5883\u754c',
    '\u8a00\u8a9e\u30b2\u30fc\u30e0', '\u5b66\u554f',
    '\u901a\u7d04', '\u63a5\u89e6', '\u64cd\u4f5c',
    '\u6b8b\u6e23', '\u672a\u89e3\u6c7a',
)
COMPOUND_BEFORE = ('\u518d',)  # re-collation is kept distinct
COMPOUND_AFTER = (
    '\u898f\u5247', '\u624b\u9806', '\u4e0d\u80fd',
    '\u53ef\u80fd\u6027',
)
NEGATION_MARKERS = ('\u3067\u306f\u306a\u3044', '\u3067\u306f\u306a\u304f', '\u306a\u3044')
QUALIFIER_MARKERS = ('\u3060\u3051', '\u307e\u3060', '\u6761\u4ef6', '\u3059\u3079\u3066', '\u7279\u5b9a')
SOURCE_CUES = {
    'necessary': ('\u5fc5\u8981',),
    'preserve': ('\u4fdd\u6301', '\u4fdd\u5b58'),
    'update': ('\u66f4\u65b0',),
    'question': ('\u554f\u3046', '\u554f\u308f\u308c'),
    'compare': ('\u6bd4\u8f03',),
}


def csv_save(path: Path, rows: list[dict], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore', lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def json_save(path: Path, item) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes((json.dumps(item, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode('utf-8'))


def lexicon_from(sentences) -> tuple[str, ...]:
    """Candidate terms: user-nominated items plus short explicit heads."""
    heads = {s.headword for s in sentences if s.headword and len(s.headword) <= 15}
    terms = set(MORE) | heads
    return tuple(sorted(terms, key=lambda t: (-len(t), t)))


def mentions(text: str, lexicon: tuple[str, ...]) -> tuple[str, ...]:
    """Greedy longest surface matching. *Not* a morphological parser."""
    occupied = [False] * len(text)
    found: set[str] = set()
    for term in lexicon:
        for m in re.finditer(re.escape(term), text):
            start, end = m.span()
            if not any(occupied[start:end]):
                found.add(term)
                occupied[start:end] = [True] * (end - start)
    return tuple(sorted(found))


def root_match_kind(text: str) -> str:
    positions = [m.start() for m in re.finditer(re.escape(ROOT), text)]
    if not positions:
        return 'none'
    for at in positions:
        before = text[at-1] if at else ''
        after = text[at+len(ROOT):]
        if before not in COMPOUND_BEFORE and not any(after.startswith(x) for x in COMPOUND_AFTER):
            return 'direct'
    return 'compound_only'


def role_markers(sentence) -> tuple[str, ...]:
    """Surface cues only; not validated syntactic or logical roles."""
    t = sentence.text
    r = []
    if sentence.headword == ROOT:
        r.append('explicit_definition_surface')
    if ROOT + '\u306f' in t:
        r.append('surface_topic')
    if any(x in t for x in NEGATION_MARKERS):
        r.append('negation_scope_unknown')
    if any(x in t for x in QUALIFIER_MARKERS):
        r.append('qualification_scope_unknown')
    for label, cues in SOURCE_CUES.items():
        if any(x in t for x in cues):
            r.append('cue_' + label)
    if '\u3068\u306f' in t and sentence.headword != ROOT:
        r.append('other_term_defined')
    if not r:
        r.append('unclassified_surface')
    return tuple(sorted(r))


def feature_set(sentence, lexicon: tuple[str, ...]) -> frozenset[str]:
    return frozenset(['role:' + x for x in role_markers(sentence)]
                    + ['neighbor:' + x for x in mentions(sentence.text, lexicon) if x != ROOT])


def feature_weight(feature: str) -> int:
    return 4 if feature.startswith('role:') else 1


def coverage(reps, available, features):
    all_f = set().union(*(features[x.id] for x in available)) if available else set()
    rep_f = set().union(*(features[x.id] for x in reps)) if reps else set()
    total = sum(feature_weight(f) for f in all_f)
    return (sum(feature_weight(f) for f in rep_f & all_f) / total) if total else 0.0


def offline_greedy(available, features, budget: int):
    """Post hoc compression baseline, never deletes raw examples."""
    selected = []
    remaining = list(available)
    while remaining and len(selected) < budget:
        picked = max(remaining, key=lambda s: (coverage(selected + [s], available, features), -s.line, s.id))
        selected.append(picked)
        remaining.remove(picked)
    return selected


def exact_feature_reference(available, features, budget: int):
    """Exact *surface-feature* coverage maximum for the tiny 43-example pilot.

    This is neither semantic optimality nor a global dictionary optimum.
    """
    all_features = sorted(set().union(*(features[x.id] for x in available)))
    by_feature = {f: i for i, f in enumerate(all_features)}
    roles = sum(1 << i for i, f in enumerate(all_features) if f.startswith('role:'))
    other = sum(1 << i for i, f in enumerate(all_features) if not f.startswith('role:'))
    masks = [sum(1 << by_feature[f] for f in features[s.id]) for s in available]
    total = 4 * roles.bit_count() + other.bit_count()
    best_score = -1
    best_combo = ()
    searched = 0
    for combo in itertools.combinations(range(len(available)), min(budget, len(available))):
        searched += 1
        mask = 0
        for i in combo:
            mask |= masks[i]
        score = 4 * (mask & roles).bit_count() + (mask & other).bit_count()
        if score > best_score:
            best_score, best_combo = score, combo
    return [available[i] for i in best_combo], best_score / total if total else 0.0, searched


def active_definition_replay(sentences, lexicon, depth):
    """Proof of indirect cache invalidation without looking at future entries.

    The sentence IDs are an explicit miniature intervention, not discovered
    proof relations or a claim that this is a uniquely correct formation order.
    """
    by_no = {s.numbered:s for s in sentences if s.numbered}
    chosen = ('8.1', '7.3', '9.5.1', '7.1', '7.2')
    if not all(key in by_no for key in chosen):
        raise ValueError('Required numbered sentences missing for the demonstration')
    orders = {
        'seed_sync_residual': chosen,
        'seed_residual_sync': ('8.1','9.5.1','7.3','7.2','7.1'),
    }
    rows=[]
    for name, order in orders.items():
        seen=[]
        before=set()
        for i, number in enumerate(order,1):
            s=by_no[number]
            seen.append(s)
            active_defs=definitions(seen,lexicon)
            active_edges, reached=dependency_layers(ROOT,active_defs,lexicon,depth)
            current=set(reached)
            rows.append(dict(order=name,step=i,added_number=number,
                added_sentence=s.id,contains_root=root_match_kind(s.text) != 'none',
                active_definition_head=s.headword,
                reached_term_count=len(current),
                newly_reached_terms=';'.join(sorted(current-before)),
                root_definition_reference_edges=len(active_edges),
                has_reference_cycle_back_to_root=int(any(
                    e['target_term']==ROOT and e['source_term']!=ROOT for e in active_edges)),
                reachable_terms=';'.join(sorted(current))))
            before=current
    return rows


def online_order(order, features, budget: int):
    """An explicit *heuristic* with path dependence; retains every example."""
    seen, reps, history = [], [], []
    for at, s in enumerate(order, 1):
        before = coverage(reps, seen, features)
        seen.append(s)
        changed = ''
        if len(reps) < budget:
            reps.append(s)
            changed = 'append'
        else:
            current = coverage(reps, seen, features)
            best_score, best_index = current, None
            for i in range(len(reps)):
                proposed = reps[:i] + [s] + reps[i+1:]
                value = coverage(proposed, seen, features)
                if value > best_score + 1e-12:
                    best_score, best_index = value, i
            if best_index is not None:
                changed = 'swap:' + reps[best_index].id
                reps[best_index] = s
            else:
                changed = 'retain_prior_representatives'
        history.append(dict(step=at, added_sentence=s.id, added_number=s.numbered,
                            line=s.line, captured_all_raw=1, representative_event=changed,
                            before_score=round(before, 6), after_score=round(coverage(reps, seen, features), 6),
                            representatives=';'.join(x.id for x in reps)))
    return reps, history


def definitions(sentences, lexicon):
    out = collections.defaultdict(list)
    terms = set(lexicon)
    for s in sentences:
        if s.headword in terms and s.headword:
            out[s.headword].append(s)
    return out


def dependency_layers(root, defs, lexicon, max_depth=2):
    """Definitional *literal-use* chains. Retains cycles as edges."""
    edges = []
    q = [(root, 0, root)]
    expanded = set()
    visited = {root: 0}
    while q:
        term, depth, path = q.pop(0)
        if depth >= max_depth or term in expanded:
            continue
        expanded.add(term)
        for s in defs.get(term, ()):
            for ref in mentions(s.text, lexicon):
                if ref == term:
                    continue
                new_path = path + ' > ' + ref
                edges.append(dict(depth=depth+1, source_term=term, target_term=ref,
                                  source_sentence=s.id, source_line=s.line,
                                  source_text=s.text, path=new_path,
                                  relation='definition_sentence_literal_reference_not_entailment',
                                  target_has_definition=int(bool(defs.get(ref)))))
                if depth+1 < visited.get(ref, 999):
                    visited[ref] = depth+1
                    q.append((ref, depth+1, new_path))
    return edges, visited


def graphml_save(path, sentences, use_records, edges):
    ns = 'http://graphml.graphdrawing.org/xmlns'
    ET.register_namespace('', ns)
    root = ET.Element('{%s}graphml' % ns)
    for k in ('type', 'label', 'provenance', 'relation'):
        ET.SubElement(root, '{%s}key' % ns, {'id':k,'for':'all','attr.name':k,'attr.type':'string'})
    g = ET.SubElement(root, '{%s}graph' % ns, {'id':'literal_usage_and_dependency','edgedefault':'directed'})
    nodes = set()
    ncounter = 0
    def node(nid, typ, label, provenance=''):
        if nid in nodes:return
        nodes.add(nid)
        x = ET.SubElement(g, '{%s}node' % ns, {'id':nid})
        for k, v in [('type',typ),('label',label),('provenance',provenance)]:
            ET.SubElement(x, '{%s}data'%ns, {'key':k}).text = v
    def edge(a,b,rel):
        nonlocal ncounter
        e = ET.SubElement(g, '{%s}edge'%ns, {'id':f'e{ncounter}', 'source':a,'target':b})
        ncounter += 1
        ET.SubElement(e, '{%s}data'%ns, {'key':'relation'}).text = rel
    by_id={s.id:s for s in sentences}
    for r in use_records:
        s=by_id[r['sentence_id']]
        sid='s:'+s.id
        node(sid,'sentence',s.text,f'{SOURCE_REL}:L{s.line}')
        node('t:'+ROOT,'term',ROOT)
        edge(sid,'t:'+ROOT,'direct_surface_use_not_inference' if r['root_match']=='direct' else 'compound_surface_overlap')
        for t in r['other_terms'].split(';'):
            if not t:continue
            node('t:'+t,'term',t)
            edge(sid,'t:'+t,'same_sentence_usage_not_inference')
    for r in edges:
        for term in (r['source_term'],r['target_term']):node('t:'+term,'term',term)
        sid='s:'+r['source_sentence']
        s=by_id[r['source_sentence']]
        node(sid,'definition_sentence',s.text,f'{SOURCE_REL}:L{s.line}')
        edge('t:'+r['source_term'],sid,'candidate_definition_statement')
        edge(sid,'t:'+r['target_term'],'literal_reference_in_definition_not_entailment')
    path.parent.mkdir(parents=True, exist_ok=True)
    data=ET.tostring(root,encoding='utf-8',xml_declaration=True)
    path.write_bytes(data+b'\n')


def run(source: Path, out: Path, *, expect_sha256=EXPECTED_SHA256,
        budget: int=5, seed: int=20261112, max_depth: int=2):
    actual=hashlib.sha256(source.read_bytes()).hexdigest()
    if expect_sha256 and expect_sha256 != actual:
        raise ValueError('Source changed. Expected %s got %s' % (expect_sha256,actual))
    if budget < 1 or max_depth < 1 or max_depth > 3:
        raise ValueError('budget >= 1; max_depth in 1..3')
    sentences=parse_sentences(source)
    lexicon=lexicon_from(sentences)
    defs=definitions(sentences,lexicon)
    use=[]
    direct=[]
    for s in sentences:
        kind=root_match_kind(s.text)
        if kind == 'none': continue
        terms=[t for t in mentions(s.text,lexicon) if t != ROOT]
        use.append(dict(sentence_id=s.id,number=s.numbered,line=s.line,root_match=kind,
                        text=s.text,other_terms=';'.join(terms),
                        surface_role_cues=';'.join(role_markers(s)),
                        alpha_status='unassessed_logic',interpretation_status='candidate_only'))
        if kind == 'direct':direct.append(s)
    edges, layer=dependency_layers(ROOT,defs,lexicon,max_depth)
    # Use all raw example sentences. The representative dictionary alone is compressed.
    features={s.id: feature_set(s,lexicon) for s in direct}
    orders={'source':direct[:], 'reverse':list(reversed(direct))}
    for i in range(8):
        x=direct[:]
        random.Random(seed+i).shuffle(x)
        orders[f'random_{i:02d}']=x
    greedy=offline_greedy(direct,features,budget)
    greedy_cov=coverage(greedy,direct,features)
    optimum, exact_cov, combinations_checked = exact_feature_reference(direct, features, budget)
    histories=[]
    comparisons=[]
    for name, order in orders.items():
        reps, hist=online_order(order,features,budget)
        comparisons.append(dict(order=name,registered_examples=len(order),
              unique_representatives=len(reps),representative_coverage=round(coverage(reps,direct,features),6),
              full_corpus_greedy_coverage=round(greedy_cov,6),
              exact_surface_feature_max=round(exact_cov,6),
              representative_sentence_ids=';'.join(s.id for s in reps)))
        for x in hist:x['order']=name
        histories.extend(hist)
    # Index: all use evidence is retained under every term it actually mentions.
    companion=collections.defaultdict(set)
    for s in direct:
        for t in mentions(s.text,lexicon):
            if t != ROOT:companion[t].add(s.id)
    companion_rows=[]
    for term,refs in sorted(companion.items(),key=lambda t:(-len(t[1]),t[0])):
        companion_rows.append(dict(term=term,cooccurring_direct_examples=len(refs),
                     example_sentence_ids=';'.join(sorted(refs)),
                     explicit_definition_sentences=';'.join(x.id for x in defs.get(term,())),
                     evidence_type='literal_same_sentence_not_semantic_dependency'))
    out.mkdir(parents=True,exist_ok=True)
    csv_save(out/'collation_uses.csv',use,['sentence_id','number','line','root_match','text','other_terms','surface_role_cues','alpha_status','interpretation_status'])
    csv_save(out/'cooccurring_terms.csv',companion_rows,['term','cooccurring_direct_examples','example_sentence_ids','explicit_definition_sentences','evidence_type'])
    csv_save(out/'definition_reference_paths.csv',edges,['depth','source_term','target_term','source_sentence','source_line','source_text','path','relation','target_has_definition'])
    csv_save(out/'representative_orders.csv',comparisons,['order','registered_examples','unique_representatives','representative_coverage','full_corpus_greedy_coverage','exact_surface_feature_max','representative_sentence_ids'])
    csv_save(out/'representative_history.csv',histories,['order','step','added_sentence','added_number','line','captured_all_raw','representative_event','before_score','after_score','representatives'])
    # Investigator-specified canaries expose the limits of a feature-only optimum.
    canary_numbers=('7.4','8.1','8.2','8.3','8.6','8.8','9.5.1')
    selected_features=set().union(*(features[x.id] for x in optimum))
    by_number={x.numbered:x for x in direct if x.numbered}
    canaries=[]
    for number in canary_numbers:
        if number not in by_number:
            raise ValueError('Missing audit canary '+number)
        s=by_number[number]
        canaries.append(dict(number=number,sentence_id=s.id,text=s.text,
            exact_feature_representative=int(s in optimum),
            unrepresented_feature_cues=';'.join(sorted(features[s.id]-selected_features)),
            semantic_necessity='not_audited',
            review_reason='Protection against mistaking feature coverage for logical spine'))
    csv_save(out/'surface_coverage_canaries.csv',canaries,
        ['number','sentence_id','text','exact_feature_representative','unrepresented_feature_cues',
         'semantic_necessity','review_reason'])
    trace=active_definition_replay(sentences,lexicon,max_depth)
    csv_save(out/'dependency_update_trace.csv',trace,['order','step','added_number','added_sentence','contains_root','active_definition_head','reached_term_count','newly_reached_terms','root_definition_reference_edges','has_reference_cycle_back_to_root','reachable_terms'])
    graphml_save(out/'collation_dependency.graphml',sentences,use,edges)
    total_compound=sum(x['root_match']=='compound_only' for x in use)
    cycles=[x for x in edges if x['target_term']==ROOT and x['source_term']!=ROOT]
    stats=dict(source=SOURCE_REL,source_sha256=actual,sentences=len(sentences),root=ROOT,
        literal_root_surface_sentences=len(use),direct_root_sentences=len(direct),
        compound_only_sentences=total_compound,cooccurring_lexicon_terms=len(companion),
        definition_reference_edges=len(edges),reached_terms=len(layer),
        reached_depths=layer,definition_cycle_back_to_root=[x['path'] for x in cycles],
        representative_budget=budget,full_corpus_greedy_coverage=round(greedy_cov,6),
        exact_surface_feature_max=round(exact_cov,6),
        exact_feature_combinations_checked=combinations_checked,
        exact_representatives=[s.id for s in optimum],
        orders_compared=len(comparisons),max_depth=max_depth,
        limits=['Lexicon and longest string matching, not parsing or semantic equivalence.',
                'A same-sentence edge is not logical implication or required dependency.',
                'Only pre-specified surface role cues; no syntax scope resolution.',
                'Surface-feature coverage is NOT entropy, negentropy, MDL in bits, or alpha/beta audit.',
                'Exact optimization covers only the fixed surface-feature model, not semantic correctness.',
                'No LLM latent training-data distance or external corpus probability is measured.',
                'All source evidence is retained; representative changes are reversible.',
                'The complete-source definition reference graph is retrospective and is not used in online selection.'])
    json_save(out/'experiment_summary.json',stats)
    return stats


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--repo-root',default='.')
    p.add_argument('--source',default=SOURCE_REL)
    p.add_argument('--expect-sha256',default=EXPECTED_SHA256)
    p.add_argument('--out',default='_build/collation_usage_probe')
    p.add_argument('--budget',type=int,default=5)
    p.add_argument('--max-depth',type=int,default=2)
    p.add_argument('--seed',type=int,default=20261112)
    a=p.parse_args()
    root=Path(a.repo_root).resolve()
    src=Path(a.source)
    if not src.is_absolute():src=root/src
    out=Path(a.out)
    if not out.is_absolute():out=root/out
    summary=run(src,out,expect_sha256=a.expect_sha256,budget=a.budget,max_depth=a.max_depth,seed=a.seed)
    print(json.dumps(summary,ensure_ascii=True,sort_keys=True,indent=2))


if __name__=='__main__':
    main()

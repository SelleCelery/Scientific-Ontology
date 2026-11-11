#!/usr/bin/env python3
"""Exploratory sentence-dictionary formation / alpha-beta proxy experiment.

A sentence is recorded before any usefulness judgment. Source text is immutable.
'Alpha' is a surface-use audit, NOT proof of validity or consistency.
'Beta' is held-out *feature reuse*, NOT semantic understanding or physical energy.
Neither surface similarity nor generated graph edges imply logical support.

Python 3.10+, standard library only. Usage from the repository root:
    python scripts/probe_sentence_dictionary.py --repo-root . --out _build/sentence_dictionary
"""
from __future__ import annotations

import argparse
import collections
import csv
import hashlib
import itertools
import json
import random
import re
import unicodedata
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path

SOURCE_REL = '01_Sat_Truth/Boundary_Epistemological_Critique.ja.md'
EXPECTED_SHA256 = '2f902285215ffac36f850cc118034787244f1c882f9274549da468960059d534'
NUMERIC = re.compile(r'^(\d+(?:\.\d+)+)[ \t\u3000]+')
SENTENCE = re.compile(r'[^。！？!?]+[。！？!?]?')
WORD = re.compile(r'[一-龯々〆ヵヶ]+|[ァ-ヴー]{2,}|[A-Za-z][A-Za-z0-9_\-]+')
EXPRESSION_FORMS = (
    'とは限らない', 'だけでなく', 'ではない', 'でなければ', 'であっても',
    'にもかかわらず', 'しなければならない', '必要である', '必要がある',
    'ならば', '場合は', '場合に', 'したがって', 'すなわち',
    'ということ', 'である', 'とは', 'として', 'とする', 'しながら',
    'によって', 'において', 'を通じて', 'に限り', 'とき',
    'ただし', '一方', 'しかし', '問う', 'できない', '成立する',
    '保持する', '更新する', '照合する', '同期する',
)
EXPRESSION_CHOICES = tuple(sorted(set(EXPRESSION_FORMS), key=lambda w: (-len(w), w)))
SINGLE_KANJI = frozenset({'知', '偽', '無', '善', '美'})
TOKEN_LIMIT_FOR_RELATION = 14  # Resource cap, not linguistic boundary.
FEATURE_WEIGHTS = (('terms', .35), ('pairs', .25), ('frames', .25), ('expressions', .15))
MISSING = 'none'


@dataclass(frozen=True)
class Sentence:
    id: str
    source: str
    line: int
    column: int
    numbered: str
    section: str
    text: str
    kind: str
    alpha_flags: tuple[str, ...]
    terms: tuple[str, ...]
    expressions: tuple[str, ...]
    pairs: tuple[str, ...]
    frames: tuple[str, ...]
    headword: str


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normal(text: str) -> str:
    return unicodedata.normalize('NFKC', text)


def terms_for(text: str) -> tuple[str, ...]:
    """Open-vocabulary orthographic candidates, excluding markup targets."""
    # Preserve original text separately: this normalization only affects indexing.
    text = re.sub(r'\[`[^`]+`\]\([^)]*\)', ' ', text)
    text = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', text)
    text = text.replace('`', '').replace('**', '')
    seq: list[str] = []
    for m in WORD.finditer(normal(text)):
        word = m.group(0)
        if len(word) >= 2 or word in SINGLE_KANJI:
            seq.append(word)
    return tuple(dict.fromkeys(seq))


def expressions_for(text: str) -> tuple[str, ...]:
    """Longest nonoverlapping registered surface expressions."""
    matches = []
    for form in EXPRESSION_CHOICES:
        for m in re.finditer(re.escape(form), text):
            matches.append((m.start(), -(m.end()-m.start()), m.end(), form))
    matches.sort()
    result = []
    right_edge = -1
    for start, _neglen, end, form in matches:
        if start >= right_edge:
            result.append(form)
            right_edge = end
    return tuple(dict.fromkeys(result))


def alpha_flags_for(text: str, is_complete: bool) -> tuple[str, ...]:
    flags = []
    if is_complete:
        flags.append('終止表面あり')
    else:
        flags.append('非終止・文脈依存候補')
    if re.search('[？?]', text):
        flags.append('疑問・非断定候補')
    if re.search(r'ではない|とは限らない|できない|成立しない|でなく|ではなく|しない|ならない', text):
        flags.append('否定作用域未解析')
    if re.search('ならば|場合|とき|限り|しなければ', text):
        flags.append('条件作用域未解析')
    if re.search('ただし|まだ|だけでなく|少なくとも|すべて|単なる|特定の|一方', text):
        flags.append('限定・対比作用域未解析')
    if re.match(r'^(本稿|ここでは|この節|以下では|本節|さて|では、)', text):
        flags.append('話題・枠組み設定候補')
    if re.match(r'^.{1,28}?とは[、\s]', text):
        flags.append('定義形式候補')
    return tuple(flags)


def parse_sentences(source_path: Path, source_label: str = SOURCE_REL) -> list[Sentence]:
    lines = source_path.read_text(encoding='utf-8-sig').splitlines()
    section = ''
    in_fence = False
    collected = []
    for line, raw in enumerate(lines, 1):
        stripped = raw.strip()
        if stripped.startswith(('```', '~~~')):
            in_fence = not in_fence
            continue
        if in_fence or not stripped or re.fullmatch(r'[-_* ]{3,}', stripped):
            continue
        if stripped.startswith('#'):
            section = re.sub(r'^#+\s*', '', stripped)
            continue
        if stripped.startswith('|') or stripped.startswith('<!--'):
            continue
        if re.match(r'^>\s*(?:Status|Scope|Language|Claim strength|Layer):', stripped):
            continue
        if stripped.startswith('[`') and '](' in stripped:
            # Index/navigation line; not a sentence, source remains untouched.
            continue
        begin = len(raw) - len(raw.lstrip())
        kind = 'prose'
        if stripped.startswith('>'):
            begin = raw.find('>') + 1
            while begin < len(raw) and raw[begin].isspace():
                begin += 1
            kind = 'blockquote'
        if re.match(r'[-*+]\s+', raw[begin:]):
            x = re.match(r'[-*+]\s+', raw[begin:])
            begin += len(x.group())
            kind = 'list'
        number = ''
        numbered = NUMERIC.match(raw[begin:])
        if numbered:
            number = numbered.group(1)
            begin += numbered.end()
            kind = 'numbered'
        raw_body = raw[begin:]
        for segment in SENTENCE.finditer(raw_body):
            rawpart = segment.group()
            left_spaces = len(rawpart) - len(rawpart.lstrip())
            text = rawpart.strip()
            if not text or len(text) < 2:
                continue
            if not re.search(r'[\u3040-\u30ff\u3400-\u9fff]', text):
                continue
            # The verbatim string and its (line, column) locator are retained.
            column = begin + segment.start() + left_spaces
            complete = text.endswith(('。', '！', '？', '!', '?'))
            kind_here = kind if complete else 'fragment:' + kind
            ts = terms_for(text)
            ex = expressions_for(text)
            limited = ts[:TOKEN_LIMIT_FOR_RELATION]
            pairs = tuple(' | '.join(p) for p in itertools.combinations(sorted(limited), 2))
            frames = tuple(f'{f} | {term}' for f in ex for term in limited)
            m = re.match(r'^(.{1,28}?)とは[、\s]', text)
            headword = m.group(1).strip() if m else ''
            id_suffix = number or f'L{line}'
            if any(x.id == f'SAT:{id_suffix}:C{column}' for x in collected):
                raise ValueError('Duplicate location key: '+id_suffix)
            collected.append(Sentence(
                id=f'SAT:{id_suffix}:C{column}', source=source_label, line=line,
                column=column, numbered=number, section=section, text=text,
                kind=kind_here, alpha_flags=alpha_flags_for(text, complete),
                terms=ts, expressions=ex, pairs=pairs, frames=frames, headword=headword))
    return collected


def stable_split(items: list[Sentence], seed: int, train_share: float = .70,
                 tune_share: float = .15) -> dict[str, list[Sentence]]:
    """Split is fixed independently of every registration permutation."""
    xs = sorted(items, key=lambda s: (s.source, s.line, s.column, s.id))
    random.Random(seed).shuffle(xs)
    if len(xs) < 12:
        raise ValueError('At least 12 sentences needed for the three-way test')
    a = max(1, int(len(xs) * train_share))
    b = max(1, int(len(xs) * tune_share))
    if a+b >= len(xs):
        b = len(xs)-a-1
    groups = {'register': xs[:a], 'tune': xs[a:a+b], 'test': xs[a+b:]}
    return {k: sorted(v, key=lambda s: (s.line, s.column)) for k,v in groups.items()}


class DictionaryState:
    def __init__(self):
        self.features = {category: set() for category, _ in FEATURE_WEIGHTS}
        self.registered = set()
        self.term_users = collections.defaultdict(set)
        self.expr_users = collections.defaultdict(set)

    def overlap(self, sentence: Sentence) -> int:
        return len(set(sentence.terms) & self.features['terms'])

    def insert(self, sentence: Sentence) -> None:
        if sentence.id in self.registered:
            raise ValueError('Sentence registered twice: '+sentence.id)
        self.registered.add(sentence.id)
        for label, _ in FEATURE_WEIGHTS:
            self.features[label].update(getattr(sentence, label))
        for term in sentence.terms:
            self.term_users[term].add(sentence.id)
        for form in sentence.expressions:
            self.expr_users[form].add(sentence.id)


def coverage(state: DictionaryState, target: Sentence) -> float:
    if not (target.terms or target.expressions or target.pairs or target.frames):
        return 0.0
    numerator, denominator = 0.0, 0.0
    for feature, weight in FEATURE_WEIGHTS:
        elems = getattr(target, feature)
        if not elems:
            continue
        numerator += weight * len(set(elems) & state.features[feature]) / len(elems)
        denominator += weight
    return numerator / denominator if denominator else 0.0


def score(state: DictionaryState, holdouts: list[Sentence]) -> float:
    return sum(coverage(state, s) for s in holdouts) / len(holdouts) if holdouts else 0.0


def replay(order: list[Sentence], holdouts: list[Sentence], *, policy: str = 'all',
           warmup: int = 8, save_history: bool = False):
    """Single complete replay. A skipped item is still in the raw inventory."""
    dictionary = DictionaryState()
    weighted_sum = 0.0
    history = []
    previous = 0.0
    admitted = 0
    skipped = 0
    isolated_at_registration = 0
    for step, sentence in enumerate(order, 1):
        overlap = dictionary.overlap(sentence)
        isolated_at_registration += int(overlap == 0)
        if policy == 'all' or (admitted < warmup or overlap > 0):
            dictionary.insert(sentence)
            admitted += 1
            decision = 'provisional_register'
        elif policy == 'early-filter':
            skipped += 1
            decision = 'defer_from_active_dictionary'
        else:
            raise ValueError('Unknown policy: '+policy)
        current = score(dictionary, holdouts)
        delta = current - previous
        previous = current
        weighted_sum += current
        if save_history:
            history.append(dict(step=step, sentence_id=sentence.id, line=sentence.line,
                                zero_lexical_overlap=int(overlap == 0),
                                preceding_shared_terms=overlap, action=decision,
                                registered_so_far=admitted, deferred_so_far=skipped,
                                eval_proxy_coverage=round(current, 8),
                                eval_proxy_increment=round(delta, 8),
                                alpha_flags='; '.join(sentence.alpha_flags)))
    return dict(auc=weighted_sum / len(order), final=score(dictionary, holdouts),
                admitted=admitted, deferred=skipped, isolated=isolated_at_registration,
                dictionary=dictionary, history=history)


def candidate_orders(train: list[Sentence], seed: int, rounds: int):
    yield 'source_order', train[:]
    yield 'reverse_source', list(reversed(train))
    freq = collections.Counter(t for x in train for t in x.terms)
    weighted = lambda s: sum(freq[x] for x in s.terms)
    yield 'common_terms_first', sorted(train, key=lambda s: (-weighted(s), s.id))
    yield 'rare_terms_first', sorted(train, key=lambda s: (weighted(s), s.id))
    for i in range(rounds):
        xs = train[:]
        random.Random(seed + 10000 + i).shuffle(xs)
        yield f'random_{i:03d}', xs


def optimize_order(train: list[Sentence], tune: list[Sentence], test: list[Sentence],
                   seed: int = 20261111, rounds: int = 32, swaps: int = 70,
                   warmup: int = 8):
    if rounds < 1 or swaps < 0:
        raise ValueError('rounds >= 1 and swaps >= 0 required')
    results = []
    best_score = float('-inf')
    best = []
    best_name = ''
    for name, order in candidate_orders(train, seed, rounds):
        s = replay(order, tune, warmup=warmup)['auc']
        results.append(dict(order=name, selection_tune_auc=round(s, 8),
                            accepted_as_new_best=int(s > best_score + 1e-12)))
        if s > best_score + 1e-12:
            best_score, best, best_name = s, order[:], name
    rng = random.Random(seed + 29001)
    current = best[:]
    for i in range(swaps):
        if len(current) < 2:
            break
        a, b = rng.sample(range(len(current)), 2)
        proposal = current[:]
        proposal[a], proposal[b] = proposal[b], proposal[a]
        s = replay(proposal, tune, warmup=warmup)['auc']
        results.append(dict(order=f'swap_attempt_{i:03d}',
                            selection_tune_auc=round(s, 8),
                            accepted_as_new_best=int(s > best_score + 1e-12)))
        if s > best_score + 1e-12:
            best_score, best, best_name = s, proposal, f'swap_improvement_{i:03d}'
            current = proposal
    # The test set is consulted only after selection is completed.
    named = {'source_order': train[:], 'reverse_source': list(reversed(train)),
             'selected_on_tune': best}
    named.update({name: order for name, order in candidate_orders(train, seed, rounds)
                  if name in ('common_terms_first', 'rare_terms_first')
                  or name in {f'random_{i:03d}' for i in range(min(rounds, 10))}})
    evaluated = []
    for name, order in named.items():
        all_tune = replay(order, tune, warmup=warmup)
        all_test = replay(order, test, warmup=warmup)
        early = replay(order, test, policy='early-filter', warmup=warmup)
        evaluated.append(dict(strategy=name, tune_auc=round(all_tune['auc'], 8),
                              test_auc=round(all_test['auc'], 8),
                              test_final=round(all_test['final'], 8),
                              early_filter_test_auc=round(early['auc'], 8),
                              early_filter_test_final=round(early['final'], 8),
                              early_deferred=early['deferred'],
                              full_isolated_while_registering=all_test['isolated']))
    return best, best_name, results, evaluated


def export_csv(path: Path, rows: list[dict], cols: list[str]):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8', newline='') as fp:
        writer = csv.DictWriter(fp, fieldnames=cols, lineterminator='\n', extrasaction='ignore')
        writer.writeheader()
        writer.writerows(rows)


def export_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes((json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + '\n').encode('utf-8'))


def export_graphml(path: Path, sentences: list[Sentence], split_by_id: dict[str, str]):
    """Bipartite usage graph. Links mean surface occurrence only."""
    ns='http://graphml.graphdrawing.org/xmlns'
    ET.register_namespace('', ns)
    root=ET.Element(f'{{{ns}}}graphml')
    for name in ('node_type','display','source_anchor','split','relation'):
        ET.SubElement(root, f'{{{ns}}}key', id=name, **{'for':'all'}, attr_name=name, attr_type='string')
    g=ET.SubElement(root, f'{{{ns}}}graph', edgedefault='undirected', id='sentence_usage_only')
    def node(nid, typ, label, source='', split=''):
        n=ET.SubElement(g, f'{{{ns}}}node', id=nid)
        for key, val in [('node_type',typ),('display',label),('source_anchor',source),('split',split)]:
            d=ET.SubElement(n, f'{{{ns}}}data', key=key)
            d.text=val
    def edge(source, target, relation):
        e=ET.SubElement(g,f'{{{ns}}}edge',source=source,target=target,id=f'e{edge.counter}')
        edge.counter+=1
        ET.SubElement(e,f'{{{ns}}}data',key='relation').text=relation
    edge.counter=0
    seen_terms=set()
    seen_forms=set()
    for s in sentences:
        sid='s:'+s.id
        node(sid,'sentence',s.text[:150],f'{s.source}:L{s.line}:C{s.column}',split_by_id[s.id])
        for term in s.terms:
            tid='t:'+term
            if tid not in seen_terms:
                node(tid,'term_candidate',term)
                seen_terms.add(tid)
            edge(sid,tid,'literal_term_use_not_entailment')
        for form in s.expressions:
            fid='f:'+form
            if fid not in seen_forms:
                node(fid,'expression_candidate',form)
                seen_forms.add(fid)
            edge(sid,fid,'literal_expression_use_not_entailment')
    ET.ElementTree(root).write(path, encoding='utf-8',xml_declaration=True, short_empty_elements=True)
    with path.open('ab') as stream:
        stream.write(b'\n')


def run(source_path: Path, out: Path, *, seed: int = 20261111,
        rounds: int = 32, swaps: int = 70, warmup: int = 8,
        expect_sha256: str = EXPECTED_SHA256, source_label: str = SOURCE_REL) -> dict:
    actual_sha = sha256(source_path)
    if expect_sha256 and actual_sha.lower() != expect_sha256.lower():
        raise ValueError(f'Source SHA-256 changed; inspect before rerun: {actual_sha}')
    sentences = parse_sentences(source_path, source_label)
    if len({s.id for s in sentences}) != len(sentences):
        raise ValueError('Duplicate source location')
    parts = stable_split(sentences, seed)
    train, tune, test = (parts[k] for k in ('register','tune','test'))
    best, best_name, searched, compared = optimize_order(train, tune, test, seed, rounds, swaps, warmup)
    full = replay(best, test, warmup=warmup, save_history=True)
    train_by_id = {x.id:x for x in train}
    early = replay(best, test, policy='early-filter', warmup=warmup, save_history=True)
    ids = {x.id: k for k, group in parts.items() for x in group}
    out.mkdir(parents=True,exist_ok=True)
    export_csv(out/'全文収録とα表面監査.csv', [dict(
        id=s.id, split=ids[s.id], source=s.source, line=s.line, column=s.column,
        numbered=s.numbered, section=s.section, kind=s.kind, text=s.text,
        alpha_flags='; '.join(s.alpha_flags), headword=s.headword,
        terms='; '.join(s.terms), expressions='; '.join(s.expressions),
        pairs=len(s.pairs), frames=len(s.frames)) for s in sentences],
        ['id','split','source','line','column','numbered','section','kind','text',
         'alpha_flags','headword','terms','expressions','pairs','frames'])
    byterm=collections.defaultdict(list)
    byform=collections.defaultdict(list)
    for s in sentences:
        for t in s.terms:
            byterm[t].append(s.id)
        for form in s.expressions:
            byform[form].append(s.id)
    export_csv(out/'用語候補と出現参照.csv', [dict(term=term, occurrences=len(users),
             sentence_ids='; '.join(users), definition_candidate_heads='; '.join(
                 s.id for s in sentences if s.headword == term))
             for term, users in sorted(byterm.items(),key=lambda x:(-len(x[1]),x[0]))],
             ['term','occurrences','sentence_ids','definition_candidate_heads'])
    export_csv(out/'言い回し候補と出現参照.csv', [dict(expression=form,occurrences=len(users),
             sentence_ids='; '.join(users)) for form,users in sorted(byform.items(),
             key=lambda x:(-len(x[1]),x[0]))],['expression','occurrences','sentence_ids'])
    export_csv(out/'登録順序の探索履歴.csv',searched,['order','selection_tune_auc','accepted_as_new_best'])
    export_csv(out/'登録順序と早期除外の比較.csv',compared,
         ['strategy','tune_auc','test_auc','test_final','early_filter_test_auc',
          'early_filter_test_final','early_deferred','full_isolated_while_registering'])
    export_csv(out/'全件仮登録の形成履歴.csv', full['history'],
         ['step','sentence_id','line','zero_lexical_overlap','preceding_shared_terms',
          'action','registered_so_far','deferred_so_far','eval_proxy_coverage',
          'eval_proxy_increment','alpha_flags'])
    export_csv(out/'早期除外の形成履歴.csv',early['history'],
         ['step','sentence_id','line','zero_lexical_overlap','preceding_shared_terms',
          'action','registered_so_far','deferred_so_far','eval_proxy_coverage',
          'eval_proxy_increment','alpha_flags'])
    # Show actual lookup candidates and what remained unknown, without asserting
    # that retrieved sentences establish a valid inference.
    lookup_rows=[]
    for sentence in sorted(tune + test, key=lambda x:(x.line,x.column)):
        matched_terms=[t for t in sentence.terms if t in full['dictionary'].features['terms']]
        missing_terms=[t for t in sentence.terms if t not in full['dictionary'].features['terms']]
        matched_forms=[f for f in sentence.expressions if f in full['dictionary'].features['expressions']]
        missing_forms=[f for f in sentence.expressions if f not in full['dictionary'].features['expressions']]
        citation_votes=collections.Counter(sid for term in matched_terms
                          for sid in full['dictionary'].term_users.get(term,set()))
        citations=[sid for sid,_ in sorted(citation_votes.items(),
                                     key=lambda x:(-x[1],x[0]))[:10]]
        lookup_rows.append(dict(sentence_id=sentence.id,group=ids[sentence.id],line=sentence.line,
                                text=sentence.text,known_terms='; '.join(matched_terms),
                                unknown_terms='; '.join(missing_terms),
                                known_expressions='; '.join(matched_forms),
                                unknown_expressions='; '.join(missing_forms),
                                candidate_use_reference_ids='; '.join(citations),
                                candidate_use_reference_count=len(citation_votes),
                                surface_reuse_proxy=round(coverage(full['dictionary'],sentence),8),
                                interpretation_status='not_semantically_audited'))
    export_csv(out/'後続文の辞書照合と未登録表現.csv',lookup_rows,
         ['sentence_id','group','line','text','known_terms','unknown_terms',
          'known_expressions','unknown_expressions','candidate_use_reference_ids',
          'candidate_use_reference_count','surface_reuse_proxy','interpretation_status'])
    # Retrospective inspection of items excluded by the deliberately weak early filter.
    order_at={x.id:i for i,x in enumerate(best)}
    deferred_rows=[]
    for row in early['history']:
        if row['action']!='defer_from_active_dictionary':
            continue
        item=train_by_id[row['sentence_id']]
        later=best[order_at[item.id]+1:]
        later_intersection=sorted(set(item.terms) & set(
                     term for s in later for term in s.terms))
        test_intersection=sorted(set(item.terms) & set(
                     term for s in test for term in s.terms))
        deferred_rows.append(dict(sentence_id=item.id,line=item.line,
                     text=item.text,at_step=row['step'],
                     later_overlap_terms='; '.join(later_intersection),
                     test_overlap_terms='; '.join(test_intersection),
                     future_contact=bool(later_intersection),
                     test_usage_contact=bool(test_intersection)))
    export_csv(out/'早期除外文の後続接続.csv',deferred_rows,
         ['sentence_id','line','text','at_step','later_overlap_terms',
          'test_overlap_terms','future_contact','test_usage_contact'])
    export_graphml(out/'文と用語表現の使用関係.graphml',sentences,ids)
    retrospective_late_connect=0
    final_terms = full['dictionary'].features['terms']
    for row in full['history']:
        if row['zero_lexical_overlap']:
            s=train_by_id[row['sentence_id']]
            if any(len(full['dictionary'].term_users[t]) >= 2 for t in s.terms):
                retrospective_late_connect+=1
    summary = {
        'research_status':'research pilot / no authoritative revisions',
        'source':source_label,'source_sha256':actual_sha,
        'sentence_count':len(sentences),'numbered_sentence_count':sum(bool(s.numbered) for s in sentences),
        'unnumbered_sentence_count':sum(not s.numbered for s in sentences),
        'nonterminal_fragment_count':sum(s.kind.startswith('fragment:') for s in sentences),
        'alpha_flag_counts':dict(sorted(collections.Counter(f for s in sentences for f in s.alpha_flags).items())),
        'definition_head_candidate_count':sum(bool(s.headword) for s in sentences),
        'term_candidates_count':len(byterm), 'expression_candidates_count':len(byform),
        'splits':{k:len(v) for k,v in parts.items()},
        'split_rule':'random seed fixed before any order selection; tune for selection, test only for final check',
        'seed':seed,'rounds':rounds,'swaps':swaps,'warmup':warmup,
        'selection_basis':'best observed tune-area; heuristic search, not global optimum',
        'selected_order_origin':best_name,
        'selected_metrics':next(x for x in compared if x['strategy']=='selected_on_tune'),
        'early_filter_deferred_with_future_lexical_contact':sum(x['future_contact'] for x in deferred_rows),
        'early_filter_deferred_with_test_contact':sum(x['test_usage_contact'] for x in deferred_rows),
        'all_register':{'deferred':full['deferred'],'admitted':full['admitted'],
                        'zero_overlap_when_added':full['isolated'],
                        'zero_overlap_with_later_term_contact':retrospective_late_connect},
        'early_filter':{'deferred':early['deferred'],'admitted':early['admitted']},
        'reference_graph':'only surface word/expression use; no logical inference edges',
        'alpha_limit':'flags for form, negation, scope, topic, question; no truth/validity/consistency proof',
        'beta_limit':'held-out surface-feature reuse; not verified meaning, dictionary fitness, entropy or exergy',
        'feature_weights':dict(FEATURE_WEIGHTS),
        'not_implemented':['grammatical roles','logical entailment','operator identity across contexts',
                           'true semantic analysis','optimal-order proof','physical entropy'],
    }
    export_json(out/'実験集計と非主張境界.json', summary)
    return summary


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo-root',type=Path,default=Path('.'))
    parser.add_argument('--source',default=SOURCE_REL,
                        help='Relative path under repo-root')
    parser.add_argument('--out',type=Path,default=Path('_build/sentence_dictionary'))
    parser.add_argument('--expect-sha256',default=EXPECTED_SHA256)
    parser.add_argument('--seed',type=int,default=20261111)
    parser.add_argument('--rounds',type=int,default=32)
    parser.add_argument('--swaps',type=int,default=70)
    parser.add_argument('--warmup',type=int,default=8)
    args=parser.parse_args()
    if not (0 <= args.warmup <= 10000):
        parser.error('--warmup must be a nonnegative integer <=10000')
    src=args.repo_root / args.source
    if not src.is_file():
        parser.error('Source not found: '+str(src))
    # Always render relative output paths inside the user-selected repository.
    out = args.out if args.out.is_absolute() else args.repo_root / args.out
    result=run(src,out,seed=args.seed,rounds=args.rounds,
               swaps=args.swaps,warmup=args.warmup,
               expect_sha256=args.expect_sha256, source_label=args.source)
    print(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True))


if __name__=='__main__':
    main()

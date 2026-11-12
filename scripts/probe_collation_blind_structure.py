#!/usr/bin/env python3
"""Unlabeled structure-first pilot around a literal string in an immutable corpus.

Discovery inputs: raw character positions around the selected literal, occurrence order,
source line boundaries, and pseudorandom seeds. No definition, dependency, negation,
necessity, semantic role, or named neighboring-term labels enter discovery or scoring.

A conditional character model estimates P(next character | preceding characters)
vs P(next character) with Dirichlet interpolation. Gains are *predictive code-length
proxies*, NOT semantic validity, information-theoretic entropy of a physical system,
or an explanation of meaning. A holdout and shuffled pairing serve as controls.

Python 3.10+, standard library; no prior SO probe imports needed.
"""
from __future__ import annotations

import argparse
import collections
import csv
from dataclasses import dataclass, replace
import hashlib
import json
import math
from pathlib import Path
import random
from typing import Iterable

SOURCE_REL = '01_Sat_Truth/Boundary_Epistemological_Critique.ja.md'
SOURCE_SHA = '2f902285215ffac36f850cc118034787244f1c882f9274549da468960059d534'
ANCHOR = '照合'  # User-chosen *surface locator*, not a presumed semantic class.
LEFT_WINDOW = 22
RIGHT_WINDOW = 22
ALPHA = 3.0  # conditional prior strength; fixed before tune/test
LAMBDA = 3.0  # unconditional symmetric prior strength
UNKNOWN = '<UNSEEN>'
BORDER = '<BORDER>'
CHOSEN_K = (1, 2, 3)
SHUFFLE_ROUNDS = 127


@dataclass(frozen=True)
class Observation:
    id: str
    line: int
    column: int  # one-based Unicode codepoint position in source line
    occurrence_in_line: int
    original_line: str
    left: str
    right: str

    @property
    def response(self) -> str:
        return self.right[0] if self.right else BORDER

    def preceding(self, k: int) -> str:
        # Preserve word-boundary uncertainty, including source-boundary absence.
        return self.left[-k:].rjust(k, '\u2400')


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def gather(source: Path, anchor: str = ANCHOR) -> list[Observation]:
    """Record all literal occurrences, including headings and compounds.

    Does not segment words or pre-decide whether '再照合' is a separate meaning.
    Does not drop awkward or initially isolated examples.
    """
    if not anchor:
        raise ValueError('Anchor may not be empty')
    out = []
    for ln, line in enumerate(source.read_text(encoding='utf-8-sig').splitlines(), 1):
        at, nth = 0, 0
        while (p := line.find(anchor, at)) >= 0:
            nth += 1
            out.append(Observation(
                id=f'SAT:L{ln}:C{p+1}', line=ln, column=p + 1,
                occurrence_in_line=nth, original_line=line,
                left=line[max(0, p-LEFT_WINDOW):p],
                right=line[p+len(anchor):p+len(anchor)+RIGHT_WINDOW],
            ))
            at = p + len(anchor)
    return out


def split_by_line(occ: list[Observation], seed: int) -> dict[str, list[Observation]]:
    """Do not let multiple occurrences from one source line cross train/tune/test."""
    lines = sorted({x.line for x in occ})
    if len(lines) < 12:
        raise ValueError('Need at least twelve source lines for three-way split')
    random.Random(seed).shuffle(lines)
    n1 = max(1, round(len(lines) * 0.60))
    n2 = max(1, round(len(lines) * 0.20))
    if n1+n2 >= len(lines):
        raise ValueError('No test lines')
    assignment = dict.fromkeys(lines[:n1], 'train') | dict.fromkeys(lines[n1:n1+n2], 'tune') | dict.fromkeys(lines[n1+n2:], 'test')
    result = {name: [] for name in ('train', 'tune', 'test')}
    for x in occ:
        result[assignment[x.line]].append(x)
    return result


def alphabet_for(train: Iterable[Observation]) -> tuple[str, ...]:
    # Only training examples define the possible one-character symbols.
    return tuple(sorted({x.response for x in train} | {UNKNOWN}))


class ContextCode:
    """Sequential count code; no semantic types and no word/definition graph."""

    def __init__(self, k: int, alphabet: tuple[str, ...]):
        if k < 1:
            raise ValueError('k must be positive')
        if UNKNOWN not in alphabet:
            raise ValueError('Missing escape category')
        self.k = k
        self.alphabet = tuple(alphabet)
        self.valid = frozenset(self.alphabet)
        self.total = 0
        self.response_counts: collections.Counter[str] = collections.Counter()
        self.context_counts: collections.Counter[str] = collections.Counter()
        self.pairs: collections.Counter[tuple[str, str]] = collections.Counter()
        self.registered: set[str] = set()

    def category(self, response: str) -> str:
        return response if response in self.valid else UNKNOWN

    def estimate_pair(self, c: str, response: str) -> tuple[float, float, int]:
        r = self.category(response)
        base = (self.response_counts[r] + LAMBDA / len(self.alphabet)) / (self.total + LAMBDA)
        # A context with zero observations gets exactly the base probability.
        conditional = (self.pairs[(c, r)] + ALPHA * base) / (self.context_counts[c] + ALPHA)
        if not (0.0 < base <= 1.0 and 0.0 < conditional <= 1.0):
            raise AssertionError('Invalid predictive probabilities')
        return base, conditional, self.context_counts[c]

    def estimate(self, x: Observation) -> tuple[float, float, int]:
        return self.estimate_pair(x.preceding(self.k), x.response)

    def register(self, x: Observation) -> None:
        if x.id in self.registered:
            raise ValueError(f'Duplicate register: {x.id}')
        self.registered.add(x.id)
        r, c = self.category(x.response), x.preceding(self.k)
        self.total += 1
        self.response_counts[r] += 1
        self.context_counts[c] += 1
        self.pairs[(c, r)] += 1


def gain_bits(base: float, cond: float) -> float:
    # log2 odds lift in predictive probability; not raw entropy or negentropy.
    return math.log2(cond / base)


def heldout_score(model: ContextCode, cases: Iterable[Observation]) -> dict:
    cases = list(cases)
    if not cases:
        return {'n':0, 'baseline_bits':0., 'conditional_bits':0., 'gain_bits':0., 'gain_per_example':0.}
    base_bits, cond_bits = 0., 0.
    for x in cases:
        b, c, _ = model.estimate(x)
        base_bits -= math.log2(b)
        cond_bits -= math.log2(c)
    return dict(n=len(cases), baseline_bits=base_bits,
                conditional_bits=cond_bits, gain_bits=base_bits-cond_bits,
                gain_per_example=(base_bits-cond_bits)/len(cases))


def replay(order: list[Observation], k: int, alphabet: tuple[str, ...], trace: bool = False):
    state = ContextCode(k, alphabet)
    sum_base = sum_cond = 0.
    rows = []
    for step, x in enumerate(order, 1):
        b, c, previous = state.estimate(x)
        sum_base -= math.log2(b)
        sum_cond -= math.log2(c)
        if trace:
            rows.append({
                'step': step, 'occurrence_id': x.id, 'line': x.line,
                'left_context': x.preceding(k), 'next_character': x.response,
                'previous_context_count': previous,
                'baseline_probability_before': round(b, 9),
                'context_probability_before': round(c, 9),
                'instant_gain_bits': round(gain_bits(b,c), 9),
                'cumulative_gain_bits': round(sum_base-sum_cond, 9),
                'registered_total': step,
            })
        state.register(x)
    return state, dict(n=len(order), baseline_bits=sum_base,
                       conditional_bits=sum_cond, gain_bits=sum_base-sum_cond,
                       gain_per_example=(sum_base-sum_cond)/max(1,len(order))), rows


def candidate_orders(train: list[Observation], seed: int, rounds: int) -> dict[str, list[Observation]]:
    base = sorted(train, key=lambda x: (x.line, x.column))
    orders = {'source': base, 'reverse': list(reversed(base))}
    for i in range(rounds):
        xs = list(base)
        random.Random(seed + 1009 * (i+1)).shuffle(xs)
        orders[f'shuffle_{i:03}'] = xs
    return orders


def pair_control(occ: list[Observation], seed: int) -> list[Observation]:
    """Null model: permute right strings without changing left contexts or split IDs.

    A test-only falsification/control. Never substitute these synthetic objects
    for real provenance rows; shuffle creates *no* new sentence or meaning.
    """
    ix = list(range(len(occ)))
    random.Random(seed).shuffle(ix)
    rights = [occ[i].right for i in ix]
    return [replace(x, right=rights[j]) for j,x in enumerate(occ)]


def observed_motifs(occ: list[Observation]) -> tuple[list[dict], list[dict]]:
    # Windowed *literal* character substrings; no morphology or part-of-speech labels.
    by_motif: dict[tuple[str,int,str], set[str]] = collections.defaultdict(set)
    for x in occ:
        for k in range(1, 5):
            l = x.left[-k:] if len(x.left) >= k else ''
            r = x.right[:k] if len(x.right) >= k else ''
            if l: by_motif[('L', k, l)].add(x.id)
            if r: by_motif[('R', k, r)].add(x.id)
    patterns = [dict(side=side, width=k, literal=lit, uses=len(ids),
                     occurrence_ids=';'.join(sorted(ids)))
                for (side,k,lit),ids in by_motif.items() if len(ids)>=2]
    patterns.sort(key=lambda z: (z['side'],z['width'],-z['uses'],z['literal']))
    pair_rows=[]
    for k in (1,2):
        for m in (1,2):
            a=collections.Counter(x.left[-k:] if len(x.left)>=k else '\u2400' for x in occ)
            b=collections.Counter(x.right[:m] if len(x.right)>=m else '\u2400' for x in occ)
            pairs: dict[tuple[str,str],set[str]] = collections.defaultdict(set)
            for x in occ:
                l=x.left[-k:] if len(x.left)>=k else '\u2400'
                r=x.right[:m] if len(x.right)>=m else '\u2400'
                pairs[(l,r)].add(x.id)
            for (l,r), ids in pairs.items():
                n = len(ids)
                if n < 2: continue
                pair_rows.append(dict(left_width=k,right_width=m,left_literal=l,right_literal=r,
                                      joint_count=n,left_count=a[l],right_count=b[r],
                                      observed_over_independent=round(n*len(occ)/(a[l]*b[r]),7),
                                      occurrence_ids=';'.join(sorted(ids))))
    pair_rows.sort(key=lambda z:(z['left_width'],z['right_width'],-z['joint_count'],z['left_literal'],z['right_literal']))
    return patterns, pair_rows


def window_recurrences(occ: list[Observation]) -> list[dict]:
    """All repeated raw 2..4-character fragments within 22 characters of anchor.

    This records unsegmented literal substrings, not discovered lexical words.
    """
    evidence: dict[tuple[str,int,str],set[str]] = collections.defaultdict(set)
    min_dist: dict[tuple[str,int,str],int] = {}
    for x in occ:
        for side,window in (('L',x.left),('R',x.right)):
            for width in (2,3,4):
                for at in range(len(window)-width+1):
                    text=window[at:at+width]
                    key=(side,width,text)
                    distance=len(window)-(at+width) if side=='L' else at
                    evidence[key].add(x.id)
                    min_dist[key]=min(distance,min_dist.get(key,distance))
    rows=[]
    for (side,width,text),ids in evidence.items():
        if len(ids)<2: continue
        rows.append(dict(side=side,width=width,substring=text,
                         occurrence_count=len(ids),nearest_distance_to_anchor=min_dist[(side,width,text)],
                         occurrence_ids=';'.join(sorted(ids))))
    rows.sort(key=lambda x:(x['side'],x['width'],-x['occurrence_count'],
                            x['nearest_distance_to_anchor'],x['substring']))
    return rows


def unidentifiable_classes(occ: list[Observation], k: int) -> list[dict]:
    """Identical measured signatures ≠ identical meanings: ambiguity inventory."""
    groups: dict[tuple[str,str],list[Observation]] = collections.defaultdict(list)
    for x in occ:
        groups[(x.preceding(k),x.response)].append(x)
    rows=[]
    for (left,right),xs in groups.items():
        if len(xs)<2: continue
        rows.append(dict(left_context=left, next_character=right, count=len(xs),
                         occurrence_ids=';'.join(x.id for x in xs),
                         distinct_source_lines=len({x.line for x in xs}),
                         example_A=xs[0].original_line,
                         example_B=next((x.original_line for x in xs[1:] if x.line!=xs[0].line),xs[-1].original_line),
                         interpretation='未判定（測定した配置が同じというだけ）'))
    rows.sort(key=lambda z:(-z['count'],z['left_context'],z['next_character']))
    return rows


def csv_write(path: Path, rows: list[dict], fields: list[str]):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n',extrasaction='ignore')
        w.writeheader(); w.writerows(rows)


def json_write(path: Path, value: dict):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,sort_keys=True,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')


def compute(source: Path, dest: Path, seed: int, rounds: int,
            control_rounds: int, expected_sha: str, anchor: str = ANCHOR) -> dict:
    actual=sha256_file(source)
    if actual != expected_sha:
        raise ValueError(f'Source SHA-256 mismatch: expected {expected_sha}, got {actual}')
    if not (1 <= rounds <= 2048 and 1 <= control_rounds <= 2048):
        raise ValueError('Round limits: 1..2048')
    occ=gather(source,anchor)
    if not occ: raise ValueError(f'No literal occurrences: {anchor}')
    parts=split_by_line(occ,seed)
    train,tune,test=(parts[p] for p in ('train','tune','test'))
    alphabet=alphabet_for(train)
    all_parts={x.id:p for p,items in parts.items() for x in items}
    dest.mkdir(parents=True,exist_ok=True)

    occurrence_rows=[dict(id=x.id,part=all_parts[x.id],line=x.line,column=x.column,
                           source=SOURCE_REL, original_line=x.original_line, substring=anchor,
                           left_context_22=x.left, right_context_22=x.right,
                           left_character=x.preceding(1),right_character=x.response)
                     for x in occ]
    csv_write(dest/'観測_文字列の全出現.csv',occurrence_rows,
              ['id','part','line','column','source','original_line','substring','left_context_22','right_context_22','left_character','right_character'])
    patterns,pairs=observed_motifs(occ)
    window_patterns=window_recurrences(occ)
    csv_write(dest/'抽出_窓内の反復部分文字列.csv',window_patterns,
              ['side','width','substring','occurrence_count','nearest_distance_to_anchor','occurrence_ids'])
    csv_write(dest/'抽出_左右の反復配置.csv',patterns,
              ['side','width','literal','uses','occurrence_ids'])
    csv_write(dest/'抽出_左右の結合候補.csv',pairs,
              ['left_width','right_width','left_literal','right_literal','joint_count',
               'left_count','right_count','observed_over_independent','occurrence_ids'])

    tuning=[]
    for k in CHOSEN_K:
        m,_,_=replay(sorted(train,key=lambda x:(x.line,x.column)),k,alphabet)
        s=heldout_score(m,tune)
        tuning.append(dict(k=k, **{a:round(b,9) if isinstance(b,float) else b for a,b in s.items()}))
    chosen=max(tuning,key=lambda row:(row['gain_per_example'],-row['k']))['k']
    csv_write(dest/'検証_文脈幅の選択.csv',tuning,
              ['k','n','baseline_bits','conditional_bits','gain_bits','gain_per_example'])

    orders=candidate_orders(train,seed,rounds)
    order_rows=[]
    detailed=[]
    for name,order in orders.items():
        model,preq,history=replay(order,chosen,alphabet,trace=(name in ('source','reverse','shuffle_000')))
        tune_final=heldout_score(model,tune)
        test_final=heldout_score(model,test)
        order_rows.append(dict(order=name,contexts_final=len(model.context_counts),
                               **{f'prequential_{key}':round(preq[key],9) for key in ('baseline_bits','conditional_bits','gain_bits','gain_per_example')},
                               tune_final_gain_bits=round(tune_final['gain_bits'],9),
                               test_final_gain_bits=round(test_final['gain_bits'],9)))
        for row in history: detailed.append(dict(order=name,**row))
    csv_write(dest/'形成_登録順序比較.csv',order_rows,
              ['order','contexts_final','prequential_baseline_bits','prequential_conditional_bits',
               'prequential_gain_bits','prequential_gain_per_example','tune_final_gain_bits','test_final_gain_bits'])
    csv_write(dest/'形成_逐次登録履歴.csv',detailed,
              ['order','step','occurrence_id','line','left_context','next_character',
               'previous_context_count','baseline_probability_before',
               'context_probability_before','instant_gain_bits',
               'cumulative_gain_bits','registered_total'])

    model,train_preq,_=replay(orders['source'],chosen,alphabet)
    test_score=heldout_score(model,test)
    tune_score=heldout_score(model,tune)
    # Sensitivity check chosen by frequency in training, without a semantic rule.
    dominant=collections.Counter(x.preceding(1) for x in train).most_common(1)[0][0]
    dominant_cases=[x for x in test if x.preceding(1)==dominant]
    other_cases=[x for x in test if x.preceding(1)!=dominant]
    ablation_rows=[]
    for group,cases in [('most_frequent_preceding_character',dominant_cases),
                        ('all_other_preceding_characters',other_cases)]:
        q=heldout_score(model,cases)
        ablation_rows.append(dict(group=group,dominant_train_character=dominant,
                                  **{key:round(v,9) if isinstance(v,float) else v
                                     for key,v in q.items()}))
    csv_write(dest/'対照_最多直前文字以外への汎化.csv',ablation_rows,
              ['group','dominant_train_character','n','baseline_bits',
               'conditional_bits','gain_bits','gain_per_example'])
    test_rows=[]
    for x in test:
        pb,pc,count=model.estimate(x)
        test_rows.append(dict(id=x.id,line=x.line,column=x.column,
                              left_context=x.preceding(chosen),right_character=x.response,
                              train_prior_context_count=count,
                              base_probability=round(pb,9),condition_probability=round(pc,9),
                              gain_bits=round(gain_bits(pb,pc),9),
                              original_line=x.original_line))
    csv_write(dest/'検証_未使用行への事前固定モデル.csv',test_rows,
              ['id','line','column','left_context','right_character','train_prior_context_count',
               'base_probability','condition_probability','gain_bits','original_line'])

    # Permutation test has the same source occurrence slots and the same line-level split.
    controls=[]
    ordered_ids={p:[x.id for x in xs] for p,xs in parts.items()}
    for trial in range(control_rounds):
        shuffled=pair_control(occ,seed+71839+trial*137)
        shuf_by_id={x.id:x for x in shuffled}
        perm_train=[shuf_by_id[i] for i in ordered_ids['train']]
        perm_test=[shuf_by_id[i] for i in ordered_ids['test']]
        # Rebuild the escape alphabet from each synthetic training set;
        # k remains fixed from the original tuning set.
        cm,_,_=replay(perm_train,chosen,alphabet_for(perm_train))
        scr=heldout_score(cm,perm_test)
        controls.append(dict(trial=trial, shuffled_test_gain_bits=round(scr['gain_bits'],9),
                             shuffled_test_gain_per_example=round(scr['gain_per_example'],9)))
    csv_write(dest/'対照_左右対応のシャッフル.csv',controls,
              ['trial','shuffled_test_gain_bits','shuffled_test_gain_per_example'])

    equivalence=unidentifiable_classes(occ,chosen)
    csv_write(dest/'残差_同じ測定配置を持つ用例.csv',equivalence,
              ['left_context','next_character','count','occurrence_ids',
               'distinct_source_lines','example_A','example_B','interpretation'])

    dictionary_rows=[]
    for c,n in sorted(model.context_counts.items(),key=lambda x:(-x[1],x[0])):
        candidate=[(r, cnt) for (left,r),cnt in model.pairs.items() if left==c]
        for r,count in sorted(candidate,key=lambda x:(-x[1],x[0])):
            pb,pc,_=model.estimate_pair(c,r)
            dictionary_rows.append(dict(context=c,context_count=n,following_character=r,
                                        joint_count=count,probability=round(pc,9),
                                        unconditional_probability=round(pb,9),
                                        ratio=round(pc/pb,6)))
    csv_write(dest/'辞書_文字配置の計算結果.csv',dictionary_rows,
              ['context','context_count','following_character','joint_count',
               'probability','unconditional_probability','ratio'])

    tail=[r['shuffled_test_gain_bits'] for r in controls]
    exceed=sum(x >= test_score['gain_bits'] for x in tail)
    summary={
        'scope':'unlabeled exploratory literal-context structure; no meaning labels in input/scoring',
        'source':SOURCE_REL,'source_sha256':actual,'anchor_literal':anchor,
        'occurrence_count':len(occ),'distinct_lines':len({x.line for x in occ}),
        'splits':{name:{'lines':len({x.line for x in xs}),'occurrences':len(xs)}
                  for name,xs in parts.items()},
        'model':{'response':'one code point immediately right of literal',
                 'conditioning':'last k code points immediately left of literal',
                 'candidate_k':list(CHOSEN_K),'selected_k_on_tune':chosen,
                 'alpha':ALPHA,'lambda':LAMBDA,'alphabet_train_size':len(alphabet),
                 'escape_character':UNKNOWN,'pad_character':'\u2400',
                 'joint_model':'interpolated empirical categorical conditional',
                 'baseline_model':'empirical unconditional categorical',
                 'complexity_of_dictionary_not_encoded':True},
        'tune':tune_score,'test_once':test_score,'train_source_order_preq':train_preq,
        'control':{'rounds':len(tail),'shuffled_test_gain_bits_mean':sum(tail)/len(tail),
                   'shuffled_test_gain_bits_min':min(tail),'shuffled_test_gain_bits_max':max(tail),
                   'control_at_least_real':exceed,
                   'empirical_one_sided_rank_fraction':(exceed+1)/(len(tail)+1)},
        'orders':{'trials':len(orders),'final_state_same_across_orders':
                  len({tuple(sorted([ (x.id,x.preceding(chosen),x.response) for x in order])) for order in orders.values()})==1,
                  'prequential_gain_bits_min':min(row['prequential_gain_bits'] for row in order_rows),
                  'prequential_gain_bits_max':max(row['prequential_gain_bits'] for row in order_rows)},
        'motif_count_support_ge_2':len(patterns),
        'window_substrings_support_ge_2':len(window_patterns),
        'left_right_pair_count_support_ge_2':len(pairs),
        'dominant_train_preceding_character':dominant,
        'test_dominant_character_ablation':ablation_rows,
        'identical_measured_signature_groups':len(equivalence),
        'boundary_and_residual':[
            'The search literal is an investigator-chosen anchor only, not a pre-defined concept.',
            'All raw occurrences, including headings and compound forms, are retained without role labels.',
            'A fixed-width character context is not syntax, a word segmentation, or semantic identity.',
            'The predictive target is one next character only. Semantic distinctions are not tested.',
            'Window n-grams are literal substrings, never preassigned words or conceptual edges.',
            'The code length excludes storing the trained dictionary and is not full MDL.',
            'Line-disjoint splits prevent identical-line leakage but not paraphrase/section leakage.',
            'The negative control destroys left/right pairing; exchangeability is a model assumption.',
            'The one-sided rank fraction is exploratory, not a published significance claim.',
            'No labels such as definition, necessity, relation type, scope or truth were applied to evidence.',
            'It is unresolved whether discovered formal differences correspond to differences in meaning.',
            'Source provenance and all dictionary state measurements are retained; no canonical changes.',
        ],
    }
    json_write(dest/'実験集計と非主張境界.json',summary)
    return summary


def main():
    ap=argparse.ArgumentParser(description='No-prior-meaning, structure-first anchored string pilot')
    ap.add_argument('--repo-root',type=Path,default=Path('.'))
    ap.add_argument('--source',type=Path,default=None)
    ap.add_argument('--expect-sha256',default=SOURCE_SHA)
    ap.add_argument('--anchor',default=ANCHOR)
    ap.add_argument('--seed',type=int,default=20261112)
    ap.add_argument('--rounds',type=int,default=32)
    ap.add_argument('--control-rounds',type=int,default=SHUFFLE_ROUNDS)
    ap.add_argument('--out',type=Path,default=Path('_build/collation_blind_structure_probe'))
    args=ap.parse_args()
    src=args.source or (args.repo_root/SOURCE_REL)
    summary=compute(src,args.out,args.seed,args.rounds,args.control_rounds,args.expect_sha256,args.anchor)
    print(json.dumps({key:summary[key] for key in ('source_sha256','occurrence_count','distinct_lines','splits','model','tune','test_once','control')},ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()

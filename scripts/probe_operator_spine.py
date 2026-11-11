#!/usr/bin/env python3
"""Research-only operator-centered graph probe for Satva / Rajas / Tamas.

Builds a **surface-expression** graph from the exact Japanese source texts.
An operator family is a revisable grouping hypothesis, NOT a proved logical
operator or a semantic equivalence. Edges express occurrence / candidate reuse,
NOT entailment, canonical adoption, or even correct parsing of Japanese.

Run (stdlib-only, Python >=3.10):
    python scripts/probe_operator_spine.py --repo-root . --out _build/operator_spine

Never rewrites source files; produces UTF-8/LF files with provenance.
"""
from __future__ import annotations

import argparse
import collections
import csv
import hashlib
import html
import itertools
import json
import re
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path

SOURCES = (
    ('SAT', '01_Sat_Truth/Boundary_Epistemological_Critique.ja.md'),
    ('RAJ', '02_Raj_Beauty/Entropy_Attributed_Difference_and_Cognitive_Axis_Formation.ja.md'),
    ('TAM', '03_Tam_Goodness/Optional_Axiom_Modules_as_Cognitive_Bridge.ja.md'),
)
# Explicitly experimental surface-pattern inventory, not a linguistic ontology.
OPERATOR_FORMS = {
    'DEFINE': ('として定義する', 'と定義する', 'とは', 'を指す', 'と呼ぶ'),
    'REQUIRE': ('しなければならない', '必要とする', '必要である', '必要がある', '必要になる'),
    'NEGATE': ('とは限らない', 'ではなくなる', 'ではない', 'ではなく', 'できない', 'しない', 'ならない'),
    'CONDITION': ('場合には', '場合は', '場合', 'ならば', 'なら', 'とき'),
    'ESTABLISH': ('成立しない', '成立して', '成立する', '成立した', '成立すれば', '成立し得る', '成立し'),
    'PREDICATE': ('として扱う', 'として読む', 'に相当する', 'とみなす', 'である', 'とする'),
    'SUPPORT': ('前提とする', '依存する', '支持する', '支える', '基づく', '導出する', '導かれる'),
    'POSSIBLE': ('可能となる', '可能になる', '可能である', 'しうる', 'し得る', 'できる'),
    'CONTACT': ('接触して', '接触する', '接触した', '接触し', '触れる'),
    'COLLATE': ('再照合する', '再照合し', '照合され', '照合して', '照合する', '照合し'),
    'RETAIN': ('保持される', '保持する', '保持し', '維持する', '維持し', '保存する', '残す', '残し'),
    'TRANSFORM': ('更新される', '更新する', '更新し', '変換する', '変換し', '変化する', '変化し',
                  '変形する', '形成される', '形成する', '形成し'),
    'CONNECT': ('接続する', '接続し', '通約する', '通約し', '翻訳する', '翻訳し'),
    'CUT': ('遮断する', '遮断し', '切断する', '切断し', '捨象する', '捨象し', '除外する', '落とす'),
    'SELECT': ('選択する', '採用する', '判断する', '判断し', '評価する', '選ぶ', '優先する'),
    'CAUSE': ('もたらす', '生じる', '生じた', '生まれる', '起こる'),
}
# The scope markers MUST NOT silently disappear as in the preceding lexical-only probe.
QUALIFIERS = ('必ずしも', 'だけでなく', '少なくとも', '運用上', '特定の', '単なる', 'すべて',
              'であっても', 'とは限らない', '現在は', '現時点', 'ただし', '場合',
              'のみ', 'まだ', '次の', '限り', '一方', 'だけ')
TERM_SEEDS = (
    '内部ヒューリスティック', '外部ヒューリスティック', '選択公理モジュール',
    '再照合可能性', '再照合', '認識軸', '観測者', '言語ゲーム', '探索資源', '境界',
    '知', '同期', '照合', '残差', '残渣', '履歴', '認識', '関心', '捨象',
    '価値', 'コスト', '意味', '使用', '観測', '判断', '自由', '責任',
    '内部', '外部', '未解決', '偽閉鎖', '偽', '必要条件', '十分条件',
    '成立', '機能', '形成', '構造', '通約', '規則', '分類', '差分',
    '翻訳', '保留', '遮断', '反射', '接続', '変換', '保持', '感性', '悟性',
    '中核', '前景化', '背景化', 'Core Invariant', 'Operational Drift',
)
SAT_NUM_RE = re.compile(r'^(\d+(?:\.\d+)+)[ \t\u3000]+(.+)$')
SENTENCE_RE = re.compile(r'[^。！？!?]+[。！？!?]?')
DEF_HEAD_RE = re.compile(r'^(.{1,24}?)とは(?:、|，|\s|$)')
ALL_OPERATOR_SPELLINGS = tuple(sorted(
    ((form, fam) for fam, forms in OPERATOR_FORMS.items() for form in forms),
    key=lambda x: (-len(x[0]), x[0], x[1]),
))
QUALIFIER_SPELLINGS = tuple(sorted(QUALIFIERS, key=lambda x: (-len(x), x)))

@dataclass(frozen=True)
class Unit:
    id: str
    phase: str
    source: str
    line: int
    section: str
    kind: str
    text: str

@dataclass(frozen=True)
class Occurrence:
    id: str
    unit: str
    phase: str
    family: str
    literal: str
    start: int
    end: int
    pre: str
    post: str
    markers: tuple[str, ...]


def source_sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_units(phase: str, source_rel: str, path: Path) -> list[Unit]:
    lines = path.read_text(encoding='utf-8-sig').splitlines()
    if phase == 'SAT':
        units = []
        for line_no, line in enumerate(lines, 1):
            m = SAT_NUM_RE.match(line)
            if m:
                units.append(Unit(f'{phase}:{m.group(1)}', phase, source_rel, line_no,
                                  m.group(1).split('.')[0], 'numbered_proposition', m.group(2).strip()))
        if len(units) != len(set(x.id for x in units)):
            raise ValueError('Duplicate numbered proposition identifier')
        return units
    # Rajas/Tamas use prose, bullets and section paragraphs rather than numbered propositions.
    # We retain source line and type, and deliberately call them *description candidates*.
    units: list[Unit] = []
    section = '0'
    in_fence = False
    for line_no, raw in enumerate(lines, 1):
        s = raw.strip()
        if s.startswith('```') or s.startswith('~~~'):
            in_fence = not in_fence
            continue
        if in_fence or not s or s == '---' or s.startswith('|'):
            continue
        if s.startswith('#'):
            m = re.match(r'^#{2,4}\s+(.+)$', s)
            if m:
                section = m.group(1)
            continue
        if s.startswith('> Status:') or s.startswith('> Scope:') or s.startswith('> Language:') or s.startswith('> Claim strength:'):
            continue
        if s.startswith('>'):
            s, kind = s.lstrip('> ').strip(), 'blockquote_candidate'
        elif re.match(r'^[-*+]\s+', s):
            s, kind = re.sub(r'^[-*+]\s+', '', s), 'list_candidate'
        else:
            kind = 'sentence_candidate'
        # Skip markdown link-only navigation, tables, and metadata-only fragments.
        if not s or s.startswith('[`') or s.startswith('![') or s.startswith('[:'):
            continue
        if re.fullmatch(r'[*_`\s\-]+', s):
            continue
        # Markdown decoration is removed only in the experimental working string;
        # untouched exact source line is always recoverable with the source/line anchor.
        s = re.sub(r'\*\*|(?<!\w)`(?!\w)', '', s)
        parts = [m.group(0).strip() for m in SENTENCE_RE.finditer(s)]
        for ix, part in enumerate(parts, 1):
            if len(part) >= 9 and any('\u3040' <= x <= '\u9fff' for x in part):
                units.append(Unit(f'{phase}:L{line_no}:S{ix}', phase, source_rel,
                                  line_no, section, kind, part))
    if len(units) != len(set(x.id for x in units)):
        raise ValueError('Duplicate prose candidate identifier')
    return units


def spans_longest(text: str, choices: tuple[tuple[str, str], ...]):
    candidates = []
    for literal, label in choices:
        for m in re.finditer(re.escape(literal), text):
            candidates.append((m.start(), m.end(), literal, label))
    candidates.sort(key=lambda x: (x[0], -(x[1] - x[0]), x[2], x[3]))
    result = []
    end = -1
    for row in candidates:
        if row[0] >= end:
            result.append(row)
            end = row[1]
    return result


def spans_qualifiers(text: str):
    return spans_longest(text, tuple((x, x) for x in QUALIFIER_SPELLINGS))


def extract_occurrences(units: list[Unit]) -> tuple[list[Occurrence], list[dict]]:
    ops: list[Occurrence] = []
    quals: list[dict] = []
    for u in units:
        found_q = spans_qualifiers(u.text)
        for a, b, value, _ in found_q:
            quals.append(dict(unit=u.id, phase=u.phase, source=u.source, line=u.line,
                              start=a, end=b, marker=value, context=u.text))
        op_matches = spans_longest(u.text, ALL_OPERATOR_SPELLINGS)
        for k, (a, b, literal, family) in enumerate(op_matches, 1):
            # This is proximity context, not a grammar-certified subject/argument.
            near_q = tuple(q[2] for q in found_q if abs(q[0] - a) <= 48 or abs(q[1] - b) <= 48)
            ops.append(Occurrence(f'{u.id}:O{k}', u.id, u.phase, family, literal,
                                  a, b, u.text[max(0, a-45):a], u.text[b:b+45], near_q))
    return ops, quals


def tokenize_terms(text: str, words):
    # A one-character CJK seed inside a longer CJK compound is not a dependable
    # lexical occurrence: avoid e.g. counting 知 in 知識 as an independent term.
    candidates = spans_longest(text, tuple((w, w) for w in words))
    retained = []
    for a, b, _s, label in candidates:
        if len(label) == 1 and '\u4e00' <= label <= '\u9fff':
            left = text[a-1] if a else ''
            right = text[b] if b < len(text) else ''
            if any('\u4e00' <= x <= '\u9fff' for x in (left, right) if x):
                continue
        retained.append((label, a, b))
    return retained


def term_vocabulary(units):
    vocabulary = set(TERM_SEEDS)
    for u in units:
        if u.phase == 'SAT':
            m = DEF_HEAD_RE.match(u.text)
            if m:
                h = m.group(1)
                if not any(z in h for z in '、。：「」()（）') and not h.endswith('こと'):
                    vocabulary.add(h)
    return sorted(vocabulary, key=lambda x: (-len(x), x))


def operator_template(text: str, ops: list[Occurrence]) -> str:
    result = text
    for o in reversed(sorted(ops, key=lambda x: x.start)):
        result = result[:o.start] + f'⟦{o.family}⟧' + result[o.end:]
    return result


def operator_group(o: Occurrence, mode: str):
    """Candidate identity hypotheses only, not alternative certified meanings."""
    if mode == 'family':
        return o.family
    if mode == 'surface':
        return o.family + '/' + o.literal
    if mode == 'phase':
        return o.family + '/' + o.phase
    if mode == 'occurrence':
        return o.id
    raise ValueError(mode)


def factor_model(ops: list[Occurrence], selected: tuple[str, ...], choices: tuple[int, ...]):
    # 0: family-wide shared candidate, 1: distinct surface forms, 2: each phase distinct.
    variants = ('family', 'surface', 'phase')
    assignment = dict(zip(selected, choices))
    groups = collections.defaultdict(set)
    for o in ops:
        mode = variants[assignment[o.family]] if o.family in assignment else 'surface'
        groups[f'{o.family}|{operator_group(o, mode)}'].add(o.unit)
    return groups


def components(groups, units: list[Unit]):
    """Only candidate operator co-use connectivity. No entailment edges."""
    parent = {u.id: u.id for u in units}
    size = {u.id: 1 for u in units}
    def root(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    def union(a, b):
        ra, rb = root(a), root(b)
        if ra != rb:
            if size[ra] < size[rb]:
                ra, rb = rb, ra
            parent[rb] = ra
            size[ra] += size[rb]
    pair_count = 0
    for keys in groups.values():
        pair_count += len(keys) * (len(keys) - 1) // 2  # with duplicates across groups; incidence, not distinct pairs
        keys = sorted(keys)
        if keys:
            first = keys[0]
            for next_key in keys[1:]:
                union(first, next_key)
    component_sizes = collections.Counter(root(x) for x in parent)
    return dict(groups=len(groups), candidate_pair_incidence=pair_count,
                component_count=len(component_sizes), largest_component=max(component_sizes.values(), default=0),
                connected_claims=sum(n for n in component_sizes.values() if n > 1))


def stage_boundaries(units, ops):
    records = []
    for phase_set in [('SAT',), ('SAT', 'RAJ'), ('SAT', 'RAJ', 'TAM')]:
        u = [x for x in units if x.phase in phase_set]
        o = [x for x in ops if x.phase in phase_set]
        for hypothesis in ('family', 'surface', 'phase'):
            gr = collections.defaultdict(set)
            for x in o:
                gr[x.family + '|' + operator_group(x, hypothesis)].add(x.unit)
            record = dict(phases='+'.join(phase_set), identity_hypothesis=hypothesis,
                          statements=len(u), occurrences=len(o), families=len(set(x.family for x in o)))
            record.update(components(gr, u))
            records.append(record)
    return records


def exhaustive(units: list[Unit], ops: list[Occurrence], limit: int, family_limit: int):
    freq = collections.Counter(x.family for x in ops)
    per_phase = collections.defaultdict(set)
    for x in ops:
        per_phase[x.family].add(x.phase)
    selected = tuple(sorted(freq, key=lambda x: (-len(per_phase[x]), -freq[x], x))[:family_limit])
    total = 3 ** len(selected)
    rows = []
    variants = ['family', 'surface', 'phase']
    for i, setting in enumerate(itertools.product(range(3), repeat=len(selected))):
        if i >= limit:
            break
        gr = factor_model(ops, selected, setting)
        stats = components(gr, units)
        rows.append(dict(case=i, setting=';'.join(f'{k}={variants[v]}' for k,v in zip(selected, setting)), **stats))
    return selected, total, rows



def family_ablation(units: list[Unit], ops: list[Occurrence]):
    """Check how much of the candidate co-use graph rests on a single family."""
    def stats_without(family):
        g=collections.defaultdict(set)
        for o in ops:
            if o.family != family:
                g[o.family+'|'+operator_group(o,'surface')].add(o.unit)
        return components(g,units)
    base=stats_without(None)
    rows=[]
    for family in sorted(set(x.family for x in ops)):
        s=stats_without(family)
        rows.append(dict(family=family, removed_occurrences=sum(o.family==family for o in ops),
                         baseline_largest=base['largest_component'], ablated_largest=s['largest_component'],
                         largest_drop=base['largest_component']-s['largest_component'],
                         baseline_pairs=base['candidate_pair_incidence'],
                         ablated_pairs=s['candidate_pair_incidence'],
                         pair_incidence_drop=base['candidate_pair_incidence']-s['candidate_pair_incidence'],
                         status='candidate co-use only; NOT a proved Spine'))
    return base,rows


def prioritized_review(ops: list[Occurrence], units: list[Unit]):
    """Small, provenance-attached list of operator-sharing decisions for Human review."""
    unit_by_id={u.id:u for u in units}
    by_family=collections.defaultdict(lambda:collections.defaultdict(list))
    for o in ops:
        by_family[o.family][o.phase].append(o)
    rows=[]
    for family, phases in by_family.items():
        for phase in ('SAT','RAJ','TAM'):
            for o in phases.get(phase,[])[:2]:
                u=unit_by_id[o.unit]
                rows.append(dict(family=family, phase=phase, unit=o.unit, source=u.source,
                                 line=u.line, literal=o.literal, excerpt=u.text[:240],
                                 review_question='同一操作子とする範囲・否定/条件/目的の作用域',
                                 review_status='AI候補・Human未審理'))
    return sorted(rows,key=lambda r:(r['family'],r['phase'],r['unit']))


def perturbation_controls(units: list[Unit], ops: list[Occurrence], qualifiers):
    by_unit = collections.defaultdict(list)
    for o in ops:
        by_unit[o.unit].append(o)
    # The operator-pattern inventory must respond to the loss of negative/quantifier markers
    # while same-word co-occurrence need not. Note the actual material, not projected semantics.
    results = []
    targets = [
        ('SAT:9.5.1', 'まだ'), ('SAT:10.7', 'ではない'),
        ('SAT:8.1', 'だけでなく'), ('SAT:1.2.1', '単なる'),
        ('SAT:7.3', '運用上'), ('SAT:15.12.1', '次の'),
    ]
    lookup = {x.id: x for x in units}
    for uid, token in targets:
        if uid not in lookup:
            continue
        u = lookup[uid]
        if token not in u.text:
            results.append(dict(unit=uid, marker=token, status='not_in_source',
                                before_ops='', after_ops='', before_qualifiers='', after_qualifiers=''))
            continue
        changed = u.text.replace(token, '', 1)
        before_ops = [x[3] for x in spans_longest(u.text, ALL_OPERATOR_SPELLINGS)]
        after_ops = [x[3] for x in spans_longest(changed, ALL_OPERATOR_SPELLINGS)]
        before_q = [x[2] for x in spans_qualifiers(u.text)]
        after_q = [x[2] for x in spans_qualifiers(changed)]
        results.append(dict(unit=uid, marker=token, status='observed',
                            before_ops='|'.join(before_ops), after_ops='|'.join(after_ops),
                            before_qualifiers='|'.join(before_q), after_qualifiers='|'.join(after_q),
                            operator_signature_changed=before_ops!=after_ops,
                            qualifier_signature_changed=before_q!=after_q))
    return results


def serialize_csv(path: Path, rows: list[dict], cols: list[str]):
    with path.open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=cols, lineterminator='\n', extrasaction='ignore')
        writer.writeheader()
        for r in rows:
            writer.writerow(r)


def serialize_json(path: Path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + '\n', encoding='utf-8', newline='\n')


def write_graphml(path: Path, units, ops, term_uses, qualifiers):
    ns = 'http://graphml.graphdrawing.org/xmlns'
    ET.register_namespace('', ns)
    def tag(x): return f'{{{ns}}}{x}'
    root = ET.Element(tag('graphml'))
    for attr in ('kind', 'label', 'phase', 'source', 'line', 'edge_kind', 'assumption'):
        ET.SubElement(root, tag('key'), id=attr, **({'for':'all','attr.name':attr,'attr.type':'string'}))
    graph = ET.SubElement(root, tag('graph'), id='operator_occurrence_graph', edgedefault='directed')
    def node(nid, **vals):
        n=ET.SubElement(graph, tag('node'), id=nid)
        for k,v in vals.items():
            ET.SubElement(n,tag('data'),key=k).text=str(v)
    def edge(a,b,etype,assumption='observed_surface'):
        e=ET.SubElement(graph,tag('edge'),source=a,target=b)
        ET.SubElement(e,tag('data'),key='edge_kind').text=etype
        ET.SubElement(e,tag('data'),key='assumption').text=assumption
    for u in units:
        node('U:'+u.id, kind=u.kind, label=u.text[:200], phase=u.phase,source=u.source,line=u.line)
    for family in OPERATOR_FORMS:
        node('F:'+family,kind='candidate_operator_family',label=family,phase='cross',source='',line='')
    for o in ops:
        node('O:'+o.id,kind='operator_occurrence',label=o.literal,phase=o.phase,source='',line='')
        edge('U:'+o.unit, 'O:'+o.id, 'contains_surface_operator')
        edge('O:'+o.id, 'F:'+o.family, 'hypothetical_family_assignment','not_semantically_adjudicated')
    for term in sorted(set(x['term'] for x in term_uses)):
        node('T:'+term,kind='lexical_argument_candidate',label=term,phase='cross',source='',line='')
    for t in term_uses:
        edge('U:'+t['unit'],'T:'+t['term'],'contains_term_string_not_argument_proof')
    for q in qualifiers:
        qid='Q:'+q['unit']+':'+str(q['start'])+':'+str(q['end'])
        node(qid,kind='qualifier_or_scope_occurrence',label=q['marker'],
             phase=q['phase'],source=q['source'],line=q['line'])
        edge('U:'+q['unit'],qid,'contains_qualifier_surface_not_verified_scope')
    ET.ElementTree(root).write(path, encoding='utf-8', xml_declaration=True)
    with path.open('ab') as f:
        f.write(b'\n')


def dot_escape(x):
    return x.replace('\\','\\\\').replace('"','\\"').replace('\n',' ')


def write_dot(path, ops, units, max_families=14):
    counts=collections.Counter(x.family for x in ops)
    families=[x for x,_ in counts.most_common(max_families)]
    by_family=collections.defaultdict(list)
    for o in ops:
        if o.family in families and not any(z.unit == o.unit for z in by_family[o.family]):
            by_family[o.family].append(o)
    unit_lookup={u.id:u for u in units}
    lines=['digraph OperatorPilot {','  graph [rankdir=LR, bgcolor="white", pad=0.4, nodesep=0.3];',
           '  node [fontname="Noto Sans CJK JP", fontsize=10];',
           '  edge [color="#7a8996", penwidth=1];']
    used=set()
    for family in families:
        lines.append(f'  "F:{family}" [shape=ellipse, style=filled, fillcolor="#d9e9f5", label="{family}\\n{counts[family]} 出現"];')
        samples=[]
        for phase in ('SAT','RAJ','TAM'):
            samples.extend([x for x in by_family[family] if x.phase==phase][:2])
        for o in samples[:6]:
            if o.unit not in used:
                u=unit_lookup[o.unit]
                label=dot_escape(u.id+' '+u.text[:30]+('…' if len(u.text)>30 else ''))
                lines.append(f'  "U:{o.unit}" [shape=box, style="rounded,filled", fillcolor="#f6f8fb",label="{label}"];')
                used.add(o.unit)
            lines.append(f'  "U:{o.unit}" -> "F:{family}" [label="{dot_escape(o.literal)}"];')
    lines.append('}')
    path.write_text('\n'.join(lines)+'\n',encoding='utf-8',newline='\n')


def write_viewer(path, units, ops, summary):
    by_family=collections.defaultdict(list)
    u_lookup={u.id:u for u in units}
    for o in ops:
        if len(by_family[o.family]) < 300:
            u=u_lookup[o.unit]
            by_family[o.family].append(dict(unit=o.unit, phase=o.phase, literal=o.literal,
                                            text=u.text, line=u.line, source=u.source,
                                            near_qualifiers=list(o.markers)))
    data=dict(summary=summary, families=dict(sorted(by_family.items())))
    raw=json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</','<\\/')
    page='''<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>三相・操作子中心の命題候補グラフ</title>
<style>
:root{color-scheme:light;font-family:system-ui,"Noto Sans CJK JP",sans-serif;background:#fafbfd;color:#1d2b38}
body{max-width:1190px;margin:0 auto;padding:28px}h1{font-size:1.7rem;margin-bottom:.3em}p{line-height:1.75}
.toolbar{display:flex;gap:1rem;flex-wrap:wrap;background:#fff;border:1px solid #d8e1e7;padding:12px;border-radius:12px;align-items:center}
select,input{padding:8px;border:1px solid #b4c2ce;border-radius:6px}#graph{width:100%;height:250px;background:#fff;border:1px solid #d8e1e7;border-radius:12px;margin:12px 0}
article{border:1px solid #d8e1e7;background:white;border-radius:8px;padding:10px 14px;margin:8px 0}article small{color:#456173}article p{margin:.4em 0}
.badge{display:inline-block;padding:2px 7px;border-radius:10px;background:#e6eef4;font-size:.77rem}
.warning{background:#fff3e4;padding:12px 16px;border-radius:9px;border:1px solid #e0c19b}#status{font-weight:600}
</style></head><body>
<h1>操作子の共有候補｜Satva → Rajas → Tamas</h1>
<p>原文の表現に繰り返し現れる<strong>操作子候補</strong>を探す試験。共通の候補記号は、意味の同一性・推論の支持・正本への採用を意味しません。</p>
<div class="warning">本図の矢印は「原文にその操作表現が現れた」関係だけです。定義の成立や論理的支持は示しません。Rajas / Tamasの節点は番号付き命題ではなく記述単位候補です。表示対象の原文位置は必ず併記します。</div>
<div class="toolbar"><label>操作子候補 <select id="family"></select></label><label>層 <select id="phase"><option value="ALL">全部</option><option value="SAT">Satva</option><option value="RAJ">Rajas</option><option value="TAM">Tamas</option></select></label><label>検索 <input id="filter" placeholder="原文語・番号・句"></label><span id="status"></span></div>
<svg id="graph" viewBox="0 0 1100 250" role="img" aria-label="候補操作子から使用箇所への観測上の接続"></svg><section id="items"></section>
<script type="application/json" id="data">__DATA__</script>
<script>
const D=JSON.parse(document.getElementById('data').textContent);
const f=document.getElementById('family'),p=document.getElementById('phase'),q=document.getElementById('filter');
const E=s=>{const d=document.createElement('span');d.textContent=s;return d.innerHTML};
Object.entries(D.families).sort((a,b)=>b[1].length-a[1].length).forEach(([k,v])=>{const o=document.createElement('option');o.value=k;o.textContent=`${k} (${v.length}表示)`;f.appendChild(o)});
function render(){const v=D.families[f.value]||[];const rows=v.filter(x=>(p.value==='ALL'||x.phase===p.value)&&(!q.value||[x.text,x.unit,x.literal].some(y=>y.includes(q.value))));
 document.getElementById('status').textContent=`${rows.length} 件（表示上限300 / 候補族）`;
 const graph=document.getElementById('graph');graph.textContent='';
 const ns='http://www.w3.org/2000/svg';const make=(tag,atts,txt)=>{let el=document.createElementNS(ns,tag);for(const[k,val]of Object.entries(atts))el.setAttribute(k,val);if(txt)el.textContent=txt;graph.appendChild(el)};
 make('rect',{x:40,y:90,width:170,height:68,rx:13,fill:'#d7e8f4',stroke:'#7299b2'});
 make('text',{x:125,y:129,fill:'#153c55','text-anchor':'middle','font-size':17},f.value);
 rows.slice(0,6).forEach((r,i)=>{let y=15+i*38;make('line',{x1:210,y1:125,x2:285,y2:y+14,stroke:'#91acbf','stroke-width':2});make('rect',{x:285,y,width:780,height:30,rx:6,fill:'#f0f5f8',stroke:'#d6e4ed'});make('text',{x:296,y:y+20,fill:'#27475d','font-size':12},(r.unit+'  '+r.text).slice(0,100))});
 let list=document.getElementById('items');list.textContent='';rows.slice(0,180).forEach(r=>{const x=document.createElement('article');x.innerHTML=`<small><span class="badge">${E(r.phase)}</span> ${E(r.unit)} ・ ${E(r.source)}:${r.line} ・ 操作表現「${E(r.literal)}」</small><p>${E(r.text)}</p><small>近接する条件・修飾表現：${E(r.near_qualifiers.join(' / ')||'検出なし')}</small>`;list.appendChild(x)}) }
[f,p,q].forEach(x=>x.addEventListener('input',render));render();
</script></body></html>
'''
    path.write_text(page.replace('__DATA__',raw),encoding='utf-8',newline='\n')


def run(repo_root: Path, out: Path, scope='all', max_cases=729, family_limit=6, work_budget=1500000,
        expected_sat_sha=None, no_graphviz=False):
    if family_limit < 1 or max_cases < 1 or work_budget < 1:
        raise ValueError('family-limit, max-cases and work-budget must be positive')
    root=repo_root.resolve()
    sources=[]
    loaded=[]
    for phase, rel in SOURCES:
        path=root / rel
        if not path.is_file():
            raise FileNotFoundError(path)
        sources.append(dict(phase=phase, source=rel, sha256=source_sha(path), bytes=path.stat().st_size))
        loaded.append(read_units(phase, rel, path))
    if expected_sat_sha and sources[0]['sha256'].lower() != expected_sat_sha.lower():
        raise ValueError(f'Satva source SHA mismatch: {sources[0]["sha256"]}')
    scope_count={'sat':1,'sat-raj':2,'all':3}[scope]
    # Budget accounts for a crude upper bound of repeated operator-occurrence processing.
    # This is an operational work proxy, not physical energy or explored semantic space.
    selected_units=[]
    stages=[]
    budget_remaining=work_budget
    for ix, (phase, _) in enumerate(SOURCES):
        if ix>=scope_count:
            break
        curr=loaded[ix]
        curr_ops,_=extract_occurrences(curr)
        work_estimate=len(curr_ops)*max_cases
        if ix>0 and work_estimate>budget_remaining:
            stages.append(dict(phase=phase, decision='deferred_budget', estimated_ops_work=work_estimate))
            break
        if ix==0 and work_estimate>budget_remaining:
            raise ValueError(f'Satva work estimate {work_estimate} exceeds budget {work_budget}; increase --work-budget or lower --max-cases')
        selected_units.extend(curr)
        budget_remaining-=work_estimate
        stages.append(dict(phase=phase,decision='included',estimated_ops_work=work_estimate,
                           statement_candidates=len(curr),operator_occurrences=len(curr_ops)))
    ops,quals=extract_occurrences(selected_units)
    per_unit=collections.defaultdict(list)
    for o in ops:per_unit[o.unit].append(o)
    words=term_vocabulary(selected_units)
    term_uses=[]
    for u in selected_units:
        for term,a,b in tokenize_terms(u.text,words):
            term_uses.append(dict(unit=u.id,phase=u.phase,source=u.source,line=u.line,term=term,start=a,end=b))
    all_vars,possible,scenario_rows=exhaustive(selected_units,ops,max_cases,family_limit)
    stage_rows=stage_boundaries(selected_units,ops)
    control_rows=perturbation_controls(selected_units,ops,quals)
    ablation_base,ablation_rows=family_ablation(selected_units,ops)
    review_rows=prioritized_review(ops,selected_units)
    summary=dict(
        kind='candidate operator occurrence and reuse graph, NOT logical entailment',
        source_status='snapshot; not confirmation of Human repository',
        sources=sources, scope_requested=scope, included_phases=sorted({x.phase for x in selected_units},
                                key=('SAT','RAJ','TAM').index), phase_gates=stages,
        statement_units=len(selected_units), numbered_sat_units=sum(x.phase=='SAT' for x in selected_units),
        prose_candidates_by_phase=dict(collections.Counter(u.phase for u in selected_units)),
        operator_occurrences=len(ops), candidate_operator_families=len(set(x.family for x in ops)),
        operatorless_units=sum(u.id not in per_unit for u in selected_units),
        qualifier_occurrences=len(quals), term_occurrences=len(term_uses),
        controlled_identity_families=list(all_vars), identity_alternatives=['family','surface','phase'],
        identity_total_possible=possible, identity_cases_run=len(scenario_rows),
        identity_exhaustive_in_selected_space=len(scenario_rows)==possible,
        # This invariance is BY CONSTRUCTION of the fixed occurrence layer.
        invariant_fixed_occurrence_layer='by construction, not an observed semantic invariance',
        distinct_identity_graph_statistics=len(set((r['groups'],r['candidate_pair_incidence'],
                       r['component_count'],r['largest_component']) for r in scenario_rows)),
        group_count_range=[min((r['groups'] for r in scenario_rows),default=0),max((r['groups'] for r in scenario_rows),default=0)],
        candidate_pair_incidence_range=[min((r['candidate_pair_incidence'] for r in scenario_rows),default=0),
                                        max((r['candidate_pair_incidence'] for r in scenario_rows),default=0)],
        largest_component_range=[min((r['largest_component'] for r in scenario_rows),default=0),
                                 max((r['largest_component'] for r in scenario_rows),default=0)],
        qualifier_deletion_controls=control_rows,
        baseline_surface_candidate_component=ablation_base,
        top_family_ablation_by_largest_drop=sorted(ablation_rows,
            key=lambda r:(-r['largest_drop'], -r['pair_incidence_drop'],r['family']))[:5],
        work_budget=work_budget, work_proxy_remaining=budget_remaining,
        claims_not_established=['operator semantics','logical entailment','alpha closure','beta exploratory exergy',
                                'information entropy','physical impedance','linguistic grammar completeness'],
    )
    out.mkdir(parents=True,exist_ok=True)
    unitrows=[dict(id=u.id,phase=u.phase,source=u.source,line=u.line,section=u.section,kind=u.kind,
                   original=u.text,normalized=operator_template(u.text,per_unit[u.id]),
                   operator_count=len(per_unit[u.id]),term_occurrences=sum(1 for x in term_uses if x['unit']==u.id))
              for u in selected_units]
    serialize_csv(out/'記述単位と操作子記号化.csv',unitrows,
                  ['id','phase','source','line','section','kind','original','normalized','operator_count','term_occurrences'])
    serialize_csv(out/'操作子の出現.csv',[
        dict(id=o.id,unit=o.unit,phase=o.phase,family=o.family,literal=o.literal,start=o.start,end=o.end,
             left_surface_context=o.pre,right_surface_context=o.post,near_scope_markers='|'.join(o.markers)) for o in ops],
             ['id','unit','phase','family','literal','start','end','left_surface_context','right_surface_context','near_scope_markers'])
    serialize_csv(out/'条件・修飾の検出.csv',quals,
                  ['unit','phase','source','line','start','end','marker','context'])
    serialize_csv(out/'対象語の使用.csv',term_uses,
                  ['unit','phase','source','line','term','start','end'])
    counts=collections.Counter(o.family for o in ops)
    form_phase=collections.defaultdict(lambda:collections.Counter())
    spellings=collections.defaultdict(lambda:collections.Counter())
    for o in ops:
        form_phase[o.family][o.phase]+=1
        spellings[o.family][o.literal]+=1
    serialize_csv(out/'操作子候補の索引.csv',[
        dict(family=f,forms='|'.join(f'{k}:{v}' for k,v in sorted(spellings[f].items())),
             occurrences=counts[f],SAT=form_phase[f]['SAT'],RAJ=form_phase[f]['RAJ'],
             TAM=form_phase[f]['TAM'],status='surface_grouping_hypothesis_not_semantics')
         for f in sorted(OPERATOR_FORMS)],
         ['family','forms','occurrences','SAT','RAJ','TAM','status'])
    serialize_csv(out/'三相拡張と同一視仮説.csv',stage_rows,
                  ['phases','identity_hypothesis','statements','occurrences','families','groups',
                   'candidate_pair_incidence','component_count','largest_component','connected_claims'])
    serialize_csv(out/'意味同一視仮説_組合せ全ケース.csv',scenario_rows,
                  ['case','setting','groups','candidate_pair_incidence','component_count',
                   'largest_component','connected_claims'])
    serialize_csv(out/'否定・条件・修飾の削除対照.csv',control_rows,
                  ['unit','marker','status','before_ops','after_ops','before_qualifiers','after_qualifiers',
                   'operator_signature_changed','qualifier_signature_changed'])
    serialize_csv(out/'操作子候補の除去対照.csv',ablation_rows,
        ['family','removed_occurrences','baseline_largest','ablated_largest','largest_drop',
         'baseline_pairs','ablated_pairs','pair_incidence_drop','status'])
    serialize_csv(out/'意味判断の審理候補.csv',review_rows,
        ['family','phase','unit','source','line','literal','excerpt','review_question','review_status'])
    serialize_json(out/'集計と非主張境界.json',summary)
    serialize_json(out/'入力原文SHAと抽出条件.json',dict(sources=sources,operator_forms=OPERATOR_FORMS,
           qualifiers=QUALIFIERS,seed_terms=TERM_SEEDS,scope=scope,max_cases=max_cases,
           family_limit=family_limit,work_budget=work_budget))
    write_graphml(out/'操作子中心_三相出現グラフ.graphml',selected_units,ops,term_uses,quals)
    write_dot(out/'操作子中心_候補接続プレビュー.dot',ops,selected_units)
    if not no_graphviz:
        import shutil, subprocess
        dot=shutil.which('dot')
        if dot:
            subprocess.run([dot,'-Tsvg',str(out/'操作子中心_候補接続プレビュー.dot'),
                '-o',str(out/'操作子中心_候補接続プレビュー.svg')],check=True)
    write_viewer(out/'操作子中心_三相グラフビューア.html',selected_units,ops,summary)
    return summary


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--repo-root',type=Path,default=Path('.'))
    p.add_argument('--out',type=Path,default=Path('_build/operator_spine'))
    p.add_argument('--scope',choices=['sat','sat-raj','all'],default='all')
    p.add_argument('--max-cases',type=int,default=729)
    p.add_argument('--family-limit',type=int,default=6)
    p.add_argument('--work-budget',type=int,default=1500000)
    p.add_argument('--expect-sat-sha256',default=None)
    p.add_argument('--no-graphviz',action='store_true')
    args=p.parse_args(argv)
    try:
        result=run(args.repo_root,args.out,args.scope,args.max_cases,args.family_limit,
                   args.work_budget,args.expect_sat_sha256,args.no_graphviz)
        print(json.dumps({k:v for k,v in result.items() if k not in ('phase_gates','sources','qualifier_deletion_controls')},
                         ensure_ascii=False,indent=2))
    except (ValueError,FileNotFoundError) as exc:
        p.error(str(exc))

if __name__=='__main__':
    main()

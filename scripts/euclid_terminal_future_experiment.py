#!/usr/bin/env python3
"""Recalculate one-step virtual-terminal experiments from the embedded Euclid navigator.

A:  x *distinct* successors attached directly to the selected proposition.
C1: x *distinct* successors after every original recorded-alpha terminal.
C2: the same x successors shared by every original recorded-alpha terminal.

The attachment ports are frozen before cutting. We remove the selected theorem
and all its recorded-alpha descendants (AND-reference model). Virtual successors
carry no H (entropy) value. Exergy X is reachability, not thermodynamic energy.
No semantic verification of hypothetical theorems or physical gamma is implied.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NAV = ROOT / 'navigator/euclid-13books-alpha-beta-gamma-navigator.html'
OUTPUT = ROOT / 'tools/euclid_13_beta_audit/euclid_terminal_future_experiment.csv'
MODELS = ('A', 'C1', 'C2')
X_VALUES = (0, 1, 10, 25)
FIELDS = (
    'proposition_id', 'model', 'x', 'original_terminals', 'reachable_terminals',
    'H_recorded_wide', 'X_recorded', 'X_extended', 'alpha_lost',
    'sigma_H_before', 'sigma_H_after', 'delta_sigma_H',
    'sigma_X_before', 'sigma_X_after', 'loss_sigma_X', 'delta_sigma_X',
    'loss_rank_of_465', 'virtual_nodes_total', 'virtual_nodes_lost',
)


def read_embedded_data(navigator: Path = NAV) -> dict:
    html = navigator.read_text(encoding='utf-8')
    pattern = r'<script id="embeddedData" type="application/json">(.*?)</script>'
    match = re.search(pattern, html, re.S)
    if match is None:
        raise ValueError('Embedded Euclid dataset not found')
    data = json.loads(match.group(1))
    if len(data['props']) != 465 or len(data['alphaEdges']) != 1639:
        raise ValueError('Unexpected recorded alpha dataset')
    return data


def examine_graph(data: dict) -> dict:
    ids = [p['id'] for p in data['props']]
    items = {p['id']: p for p in data['props']}
    children = {id_: set() for id_ in ids}
    parents = {id_: set() for id_ in ids}
    for u, v in data['alphaEdges']:
        if u not in children or v not in children:
            raise ValueError(f'Unknown recorded-alpha node: {u} -> {v}')
        children[u].add(v)
        parents[v].add(u)
    queue = deque(id_ for id_ in ids if not parents[id_])
    indegree = {id_: len(parents[id_]) for id_ in ids}
    order = []
    while queue:
        id_ = queue.popleft()
        order.append(id_)
        for child in sorted(children[id_]):
            indegree[child] -= 1
            if indegree[child] == 0:
                queue.append(child)
    if len(order) != len(ids):
        raise ValueError('Recorded-alpha graph contains a cycle')
    terminals = {id_ for id_ in ids if not children[id_]}
    reach = {}
    reached_terminals = {}
    for id_ in reversed(order):
        down = set()
        ends = {id_} if id_ in terminals else set()
        for child in children[id_]:
            down.add(child)
            down.update(reach[child])
            ends.update(reached_terminals[child])
        reach[id_] = down
        reached_terminals[id_] = ends
        if len(down) != items[id_]['x'] or len(down) + 1 != items[id_]['lost']:
            raise ValueError(f'X or alpha-lost baseline mismatch: {id_}')
    c1_slope = sum(len(reached_terminals[id_]) for id_ in ids)
    beta_parents = {id_: [] for id_ in data['betaOrder']}
    for edge in data['wideEdges']:
        beta_parents[edge['b']].append(edge['a'])
    return dict(ids=ids,items=items,children=children,parents=parents,order=order,
                terminals=terminals,reach=reach,reached_terminals=reached_terminals,
                c1_slope=c1_slope,beta_parents=beta_parents)


def cut_stats(data: dict, graph: dict, proposition: str) -> dict:
    dead = {proposition}
    pending = [proposition]
    while pending:
        for child in graph['children'][pending.pop()]:
            if child not in dead:
                dead.add(child)
                pending.append(child)
    alive = set(graph['ids']) - dead
    up = {proposition}
    pending = [proposition]
    while pending:
        for parent in graph['parents'][pending.pop()]:
            if parent not in up:
                up.add(parent)
                pending.append(parent)
    # Exact recorded reachability for each survivor after removing descendants.
    reach_after = {}
    sigma_x_after = 0
    for id_ in reversed(graph['order']):
        if id_ in dead:
            continue
        targets = set()
        for child in graph['children'][id_]:
            if child in alive:
                targets.add(child)
                targets.update(reach_after[child])
        reach_after[id_] = targets
        sigma_x_after += len(targets)
    # The cut set is descendant closed. If a surviving Q reaches a surviving
    # original terminal T, its paths to T cannot pass through removed nodes.
    after_c1_slope = 0
    after_c2_slope = 0
    for id_ in alive:
        count = len(graph['reached_terminals'][id_] - dead)
        after_c1_slope += count
        after_c2_slope += count > 0
    removed_terminal_count = len(graph['terminals'] & dead)
    # H recomputed using wide qualitative reference scope (unchanged from v2).
    beta_values = {}
    for id_ in data['betaOrder']:
        if id_ in dead:
            beta_values[id_] = 0
            continue
        remaining = [p for p in graph['beta_parents'].get(id_, []) if p not in dead]
        beta_values[id_] = sum(beta_values[p] for p in remaining) if remaining else 1
    sigma_h_after = sum(beta_values[id_] for id_ in alive)
    return dict(dead=dead,ancestor_count=len(up),after_x=sigma_x_after,
                after_h=sigma_h_after,after_c1_slope=after_c1_slope,
                after_c2_slope=after_c2_slope,removed_terminals=removed_terminal_count)


def compute_rows(data: dict) -> list[dict]:
    graph = examine_graph(data)
    original_x = sum(p['x'] for p in data['props'])
    original_h = sum(p['h'] for p in data['props'])
    if original_x != 19220 or original_h != 26011867:
        raise ValueError('Baseline sums mismatch')
    all_stats = {id_: cut_stats(data,graph,id_) for id_ in graph['ids']}
    rows = []
    for mode in MODELS:
        for x in X_VALUES:
            local = []
            for id_ in graph['ids']:
                p = graph['items'][id_]
                c = all_stats[id_]
                before_slope = (c['ancestor_count'] if mode=='A' else graph['c1_slope'] if mode=='C1' else len(graph['ids']))
                after_slope = (0 if mode=='A' else c['after_c1_slope'] if mode=='C1' else c['after_c2_slope'])
                original_terminal_count = len(graph['terminals'])
                virtual_total = x*(original_terminal_count if mode=='C1' else 1)
                virtual_lost = (x if mode=='A' else x*c['removed_terminals'] if mode=='C1'
                                else x if c['removed_terminals']==original_terminal_count else 0)
                before = original_x+x*before_slope
                after = c['after_x']+x*after_slope
                loss = before-after
                ext_x = p['x'] + x*(len(graph['reached_terminals'][id_]) if mode=='C1' else 1)
                local.append(dict(proposition_id=id_,model=mode,x=x,
                    original_terminals=original_terminal_count,
                    reachable_terminals=len(graph['reached_terminals'][id_]),
                    H_recorded_wide=p['h'],X_recorded=p['x'],X_extended=ext_x,
                    alpha_lost=len(c['dead']),sigma_H_before=original_h,
                    sigma_H_after=c['after_h'],delta_sigma_H=c['after_h']-original_h,
                    sigma_X_before=before,sigma_X_after=after,loss_sigma_X=loss,
                    delta_sigma_X=after-before,loss_rank_of_465=0,
                    virtual_nodes_total=virtual_total,virtual_nodes_lost=virtual_lost))
            distinct = sorted({r['loss_sigma_X'] for r in local},reverse=True)
            # Competition ranking: identical losses share a rank.
            ordinal = sorted((r['loss_sigma_X'] for r in local),reverse=True)
            rank = {}
            for i,loss in enumerate(ordinal):
                rank.setdefault(loss,i+1)
            for row in local:
                row['loss_rank_of_465'] = rank[row['loss_sigma_X']]
            rows.extend(local)
    return rows


def save_rows(rows: list[dict], output: Path = OUTPUT) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('w',newline='',encoding='utf-8') as stream:
        writer = csv.DictWriter(stream,fieldnames=FIELDS,lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--navigator',type=Path,default=NAV)
    parser.add_argument('--output',type=Path,default=OUTPUT)
    args=parser.parse_args()
    rows=compute_rows(read_embedded_data(args.navigator))
    save_rows(rows,args.output)
    print(f'{len(rows)} experiment rows written: {args.output}')
    for mode in ('C1','C2'):
        for x in X_VALUES:
            first=next(r for r in rows if r['model']==mode and r['x']==x)
            print(f'{mode} x={x}: expanded sigma X={first["sigma_X_before"]}; I.47 loss='+str(next(r['loss_sigma_X'] for r in rows if r['proposition_id']=='I.47' and r['model']==mode and r['x']==x)))


if __name__ == '__main__':
    main()

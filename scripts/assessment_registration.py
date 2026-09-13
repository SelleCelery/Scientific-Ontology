#!/usr/bin/env python3
"""Bridge explicit human assessment reviews to existing registration transactions.

This module neither re-scores a claim nor writes the canonical manifest. Raw runs,
reviews, quotes and hashes stay outside the public read model.
"""
from __future__ import annotations
import copy
import hashlib
import json
from pathlib import Path
from typing import Any
from jsonschema import Draft202012Validator
from document_contract import load_manifest, resolve_repo_path, sha256

APPROVE = {'approve', 'approve_with_edits'}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding='utf-8-sig'))


def summaries_from_review(root: Path, run_path: Path, review_path: Path) -> dict[str, dict[str, Any]]:
    run_file=load_json(run_path);review_file=load_json(review_path)
    for value,schema_name in [(run_file,'repository_assessment_run.schema.json'),(review_file,'repository_assessment_review.schema.json')]:
        schema=load_json(root/'tools/assessment'/schema_name)
        Draft202012Validator(schema).validate(value)
    run=run_file['repository_assessment_run'];review=review_file['repository_assessment_review']
    if review['source_run_sha256'] != sha256(run_path): raise ValueError('Assessment review does not bind to the exact run bytes')
    preview=load_json(root/'tools/assessment/repository_assessment_protocols.preview.json')['repository_assessment_protocols_preview']
    protocol=run['protocol']
    frozen=next((p for p in preview['protocols'] if p['id']==protocol['id'] and p['revision']==protocol['revision']),None)
    if not frozen or frozen['source_sha256']!=protocol['source_sha256']: raise ValueError('Assessment protocol revision/hash mismatch')
    targets={t['path']:t['sha256'] for t in run['fixture']['targets']}
    metadata={d['path']:d for d in load_manifest(root)['documents']}
    run_schema=load_json(root/'tools/assessment/repository_assessment_run.schema.json')
    raw_items: dict[str, tuple[str,str,dict[str,Any]]] = {}
    for doc in run['documents']:
        path=doc['path']
        if 'document_profile::'+path in raw_items: raise ValueError('Duplicate assessment document: '+path)
        raw_items['document_profile::'+path]=(path,'document_profile',doc['document_profile'])
        for key,kind,identity in [('representative_claims','representative_claim','claim_id'),('claim_hotspots','claim_hotspot','hotspot_id')]:
            for item in doc[key]:
                review_key=kind+'::'+item[identity]
                if review_key in raw_items: raise ValueError('Duplicate global assessment identity: '+review_key)
                raw_items[review_key]=(path,kind,item)
    decisions={}
    for d in review['decisions']:
        key=d['review_key']
        if key in decisions or key not in raw_items: raise ValueError('Duplicate/unknown assessment review key: '+key)
        path,kind,before=raw_items[key]
        if d['path']!=path or d['kind']!=kind or d['before']!=before: raise ValueError('Assessment before/path/kind no longer matches raw item: '+key)
        if d['decision']=='approve' and d['after']!=before: raise ValueError('Unedited approval changed assessment content: '+key)
        after=d['after']
        if d['decision'] in APPROVE:
            ref = {'document_profile': '#/$defs/documentAssessment/properties/document_profile', 'representative_claim': '#/$defs/representativeClaim', 'claim_hotspot': '#/$defs/claimHotspot'}[kind]
            Draft202012Validator({'$ref': ref, '$defs': run_schema['$defs']}).validate(after)
            for id_key in ('claim_id','hotspot_id'):
                if id_key in before and after.get(id_key)!=before[id_key]: raise ValueError('Assessment identity cannot be edited: '+key)
            c=after.get('classification',{})
            if c.get('strength') not in {'S0','S1','S2','S3','S4','S5'} or c.get('exposure') not in {'E0','E1','E2','E3'}:
                raise ValueError('Unresolved/null classification cannot be promoted: '+key)
        decisions[key]=d
    output={}
    for doc in run['documents']:
        path=doc['path'];profile_review=decisions.get('document_profile::'+path)
        if not profile_review or profile_review['decision'] not in APPROVE:continue
        entry=metadata.get(path)
        if not entry or entry['assessment']['applicability']!='current_claim': raise ValueError('Not a current claim-bearing metadata entry: '+path)
        current=resolve_repo_path(root,path)
        if targets.get(path)!=sha256(current): raise ValueError('Reviewed source has changed; re-audit or explicitly re-review: '+path)
        lines=current.read_text(encoding='utf-8').splitlines()
        # Verify every quoted range in the reviewed document, without repairing it.
        refs=[]
        for rep in doc['representative_claims']:refs.extend(rep.get('source_refs',[]))
        for h in doc['claim_hotspots']:
            refs.append(h['source']);refs.extend(h.get('source_refs',[]))
        for b in doc['nonclaim_boundaries']:refs.append(b['source'])
        for kind,items,idkey in [('representative_claim',doc['representative_claims'],'claim_id'),('claim_hotspot',doc['claim_hotspots'],'hotspot_id')]:
            for item in items:
                decision=decisions.get(kind+'::'+item[idkey])
                if decision and decision['decision'] in APPROVE:
                    refs.extend(decision['after'].get('source_refs',[]))
                    if kind=='claim_hotspot': refs.append(decision['after']['source'])
        basis=profile_review['after'].get('basis_claim_ids',[])
        if not basis or not set(basis)<=set(i['claim_id'] for i in doc['representative_claims']):
            raise ValueError('Document profile basis does not resolve to representative claims: '+path)
        for ref in refs:
            if ref.get('path')!=path or ref.get('sha256')!=targets[path]: raise ValueError('Quote does not bind to document: '+path)
            a,b=ref['line_start'],ref['line_end']
            if not 1<=a<=b<=len(lines) or '\n'.join(lines[a-1:b]).strip()!=str(ref['text']).strip(): raise ValueError('Quote/line range mismatch: '+path)
        effective_hotspots=[]; unreviewed_hotspots=0
        for kind,items,idkey in [('representative_claim',doc['representative_claims'],'claim_id'),('claim_hotspot',doc['claim_hotspots'],'hotspot_id')]:
            for item in items:
                d=decisions.get(kind+'::'+item[idkey])
                if d and d['decision'] not in APPROVE:raise ValueError('Unresolved detail review blocks promotion for this document: '+path)
                effective=d['after'] if d else item
                if kind=='claim_hotspot':
                    if not d:
                        unreviewed_hotspots+=1
                        continue
                    ref=effective['source']
                    effective_hotspots.append({'label':effective['proposition'],'locator':f"L{ref['line_start']}-L{ref['line_end']}",**effective['classification']})
        summary={'applicability':'current_claim','review_state':'approved','protocol':{'id':protocol['id'],'revision':protocol['revision']},'representative':copy.deepcopy(profile_review['after']['classification']), 'hotspots':effective_hotspots, 'nonclaim_boundaries':[b['proposition'] for b in doc['nonclaim_boundaries']], 'unresolved':list(entry['assessment'].get('unresolved',[])), 'approval':{'review_id':run['run_id'],'document_sha256':targets[path],'run_sha256':sha256(run_path),'review_sha256':sha256(review_path),'reviewed_at':profile_review['reviewed_at']}}
        if unreviewed_hotspots:
            summary['unresolved'].append(str(unreviewed_hotspots)+' local hotspot candidates remain unreviewed and are not projected as approved scores.')
        output[path]=summary
    return output

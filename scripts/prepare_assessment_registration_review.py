#!/usr/bin/env python3
"""Generate (do not apply) a registration transaction from an explicit assessment review."""
from __future__ import annotations
import argparse,copy,json,sys
from pathlib import Path
from assessment_registration import summaries_from_review
from build_registration_workbench_preview import build_payload


def prepare(root: Path,run: Path,review: Path) -> dict:
    summaries=summaries_from_review(root,run,review)
    if not summaries:raise ValueError('No explicitly approved document profiles; no registration transaction generated')
    w=build_payload(root)['registration_workbench'];decisions=[];revisions=[]
    for group in ['provisional_documents','registered_documents']:
        for doc in w[group]:
            path=doc['path']
            if path not in summaries:continue
            before=doc['baseline'];after=copy.deepcopy(before);after['assessment']=summaries[path]
            stamp=summaries[path]['approval']['reviewed_at']
            if group=='provisional_documents':
                decisions.append({'path':path,'doc_id':doc['doc_id'],'decision':'approve_with_edits','reviewed_at':stamp,'before':before,'after':after})
            else:
                revisions.append({'path':path,'doc_id':doc['doc_id'],'source_kind':'ad_hoc_registered_revision','created_at':stamp,'decision':'approve','before':before,'after':after})
    return {'registration_review':{'schema_version':'0.3','status':'in_progress','source':{k:w['source'][k] for k in ['manifest_sha256','graph_sha256','revision_proposals_sha256']}|{'provisional_count':len(w['provisional_documents']),'revision_proposal_count':len(w['revision_proposals'])},'decisions':decisions,'manual_candidates':[],'revision_candidates':revisions}}


def main() -> int:
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);p.add_argument('--run',type=Path,required=True);p.add_argument('--review',type=Path,required=True);p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    try:
        if args.output.resolve().is_relative_to(args.root.resolve()):raise ValueError('Write the review artifact outside the repository')
        data=prepare(args.root.resolve(),args.run,args.review);args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print('ASSESSMENT REGISTRATION PREVIEW CREATED; canonical manifest unchanged')
        return 0
    except Exception as exc:print('ASSESSMENT REGISTRATION BLOCKED: '+str(exc),file=sys.stderr);return 1
if __name__=='__main__':raise SystemExit(main())

#!/usr/bin/env python3
"""Deterministic regression tests for metadata boundaries and review transactions.

All approvals used below are synthetic test fixtures outside the repository.
No actual audit result, human decision or canonical document is changed.
"""
from __future__ import annotations
import copy
import json
from pathlib import Path
import tempfile
import unittest
import yaml
from jsonschema import Draft202012Validator

from document_contract import (load_manifest, validate_manifest, public_assessment, resolve_repo_path, sha256, asset_bytes_match,
                               historical_manifest_status, historical_attestation_errors)
from assessment_registration import summaries_from_review
from rebuild_document_read_models import transactional_rebuild, GENERATED_FILES, BUILD_DIRECTORY

ROOT=Path(__file__).resolve().parents[1]


def fixture(root: Path, folder: Path) -> tuple[Path,Path,dict,dict]:
    manifest=load_manifest(root)
    entry=next(e for e in manifest['documents'] if e['assessment']['applicability']=='current_claim' and e['assessment']['review_state']=='unreviewed')
    path=entry['path'];digest=sha256(root/path)
    text=(root/path).read_text(encoding='utf-8').splitlines()[0]
    ref={'path':path,'sha256':digest,'line_start':1,'line_end':1,'text':text}
    attribution={'represented_system':'synthetic-test','repository_commitment':'represented','responsibility':'test only','scope':'transaction validation'}
    rep={'claim_id':'TEST-R1','source_refs':[ref], 'proposition':'Synthetic fixture; not an SO claim.', 'argument_role':'central_claim', 'attribution':attribution,'classification':{'strength':'S1','exposure':'E0'},'rationale':'test only'}
    hotspot={'hotspot_id':'TEST-H1','source':ref,'proposition':'Synthetic high hotspot; never promoted to document maximum.','argument_role':'bridge','hotspot_reasons':['external_bridge'],'attribution':attribution,'ground':{'owner':'synthetic','relation':'test only'},'classification':{'strength':'S5','exposure':'E3'},'classification_effect':'local_only','rationale':'test only'}
    profile={'title':'Synthetic fixture','classification':{'strength':'S1','exposure':'E0'},'basis_claim_ids':['TEST-R1'],'rationale':'explicit profile, not maximum'}
    protocol=json.loads((root/'tools/assessment/repository_assessment_protocols.preview.json').read_text(encoding="utf-8"))['repository_assessment_protocols_preview']['protocols'][0]
    run={'repository_assessment_run':{'schema_version':'0.2','run_id':'SYNTHETIC_TEST_ONLY','protocol':{k:protocol[k] for k in ['id','revision','source_sha256']},'fixture':{'targets':[{'path':path,'sha256':digest}]},'documents':[{'path':path,'document_profile':profile,'representative_claims':[rep],'claim_hotspots':[hotspot],'nonclaim_boundaries':[]}]}}
    run_path=folder/'run.json';review_path=folder/'review.json'
    run_path.write_text(json.dumps(run),encoding='utf-8')
    review={'repository_assessment_review':{'schema_version':'0.2','source_run_sha256':sha256(run_path),'status':'in_progress','decisions':[{'review_key':'document_profile::'+path,'kind':'document_profile','path':path,'decision':'approve','reviewed_at':'synthetic-test','before':copy.deepcopy(profile),'after':copy.deepcopy(profile)}]}}
    review_path.write_text(json.dumps(review),encoding='utf-8')
    return run_path,review_path,run,review


class ContractTests(unittest.TestCase):
    def setUp(self):self.manifest=load_manifest(ROOT)
    def errors(self,m):return validate_manifest(ROOT,m)[0]
    def test_current_manifest_and_coverage(self):self.assertEqual(self.errors(self.manifest),[])
    def test_ids_unique(self):
        m=copy.deepcopy(self.manifest);m['documents'][1]['doc_id']=m['documents'][0]['doc_id'];self.assertTrue(self.errors(m))
    def test_missing_path_rejected(self):
        m=copy.deepcopy(self.manifest);m['documents'][0]['path']='00_Overview/NO_SUCH_DOCUMENT.md';self.assertTrue(self.errors(m))
    def test_retired_not_resurrected(self):
        for r in self.manifest['retired_documents']:
            self.assertNotIn(r['path'],{e['path'] for e in self.manifest['documents']})
    def test_retired_registration_rejected(self):
        m=copy.deepcopy(self.manifest);m['documents'][0]['path']=m['retired_documents'][0]['path'];self.assertTrue(self.errors(m))
    def test_fixed_source_bound(self):
        # A fixed research source may be intentionally withheld from the public repository.
        # Test the role contract with a synthetic repository asset instead of requiring
        # a real private-lineage fixture to be present in the canonical manifest.
        m=copy.deepcopy(self.manifest)
        template=next(x for x in m['managed_assets'] if x['document_role']=='provenance_asset')
        a=copy.deepcopy(template)
        a['asset_id']='synthetic_fixed_source_contract_test'
        a['document_role']='fixed_research_source'
        a['integrity']={'sha256':'0'*64,'basis':'synthetic_contract_test'}
        m['managed_assets'].append(a)
        self.assertTrue(self.errors(m))
    def test_current_historical_attestation_resolves_exact_declared_state(self):
        spec=next(x for x in self.manifest['provenance_sets'] if x['id']=='volume_01_historical_manifest')
        status=historical_manifest_status(ROOT,spec)
        self.assertEqual({k:status[k] for k in ('matched','mismatched','missing','invalid')},
                         {'matched':19,'mismatched':26,'missing':0,'invalid':0})
        records={str(e['path']):e for e in [*self.manifest['documents'],*self.manifest['managed_assets']]}
        self.assertEqual(historical_attestation_errors(ROOT,spec,status,records=records),[])

    def test_historical_attestation_reopens_on_current_snapshot_drift(self):
        import hashlib
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);base=root/'volume';base.mkdir()
            current=base/'record.md';current.write_bytes(b'current\n')
            old_digest=hashlib.sha256(b'historical\n').hexdigest()
            current_digest=hashlib.sha256(current.read_bytes()).hexdigest()
            (base/'MANIFEST.sha256').write_text(f'{old_digest}  record.md\n',encoding='utf-8')
            (base/'CURRENT.sha256').write_text(f'{current_digest}  record.md\n',encoding='utf-8')
            (base/'ATTESTATION.md').write_text('# synthetic attestation\n',encoding='utf-8')
            spec={
                'id':'synthetic_historical_set','root':'volume','path':'volume/MANIFEST.sha256',
                'integrity_claim':'attested_historical_manifest_with_current_divergence',
                'release_review_required':False,
                'attestation':{
                    'status':'accepted_as_historical_method_record','attested_at':'2026-09-13',
                    'acceptance_scope':'synthetic_test','attestation_path':'volume/ATTESTATION.md',
                    'current_snapshot_path':'volume/CURRENT.sha256',
                    'expected_historical_relation':{'matched':0,'mismatched':1,'missing':0,'invalid':0},
                    'mismatch_classification':{'formatting_level':1,'later_wrapper_or_provenance_evolution':0},
                },
            }
            records={
                'volume/ATTESTATION.md':{'document_role':'historical_support'},
                'volume/CURRENT.sha256':{'document_role':'provenance_asset'},
            }
            status=historical_manifest_status(root,spec)
            self.assertEqual(historical_attestation_errors(root,spec,status,records=records),[])
            current.write_bytes(b'drifted\n')
            status=historical_manifest_status(root,spec)
            errors=historical_attestation_errors(root,spec,status,records=records)
            self.assertTrue(any('snapshot drift detected' in e for e in errors))
    def test_unapproved_scores_rejected(self):
        m=copy.deepcopy(self.manifest);m['documents'][0]['assessment']['representative']={'strength':'S5','exposure':'E3'};self.assertTrue(self.errors(m))
    def test_nonclaim_role_not_forced_into_scoring(self):
        m=copy.deepcopy(self.manifest);d=next(x for x in m['documents'] if x['document_role']=='navigation');d['assessment']['applicability']='current_claim';self.assertTrue(self.errors(m))
    def test_commensuration_cannot_own_itself(self):
        m=copy.deepcopy(self.manifest);d=next(x for x in m['documents'] if x['language_relation']['role']=='commensuration');d['language_relation']['authoritative_path']=d['path'];self.assertTrue(self.errors(m))
    def test_counterpart_must_be_reciprocal(self):
        m=copy.deepcopy(self.manifest);d=next(x for x in m['documents'] if x['language_relation'].get('counterpart_path'));d['language_relation']['counterpart_path']='README.md';self.assertTrue(self.errors(m))
    def test_root_exception_cannot_spread(self):
        m=copy.deepcopy(self.manifest);d=next(x for x in m['documents'] if x['path']!='README.md');d['language_relation']['role']='coauthoritative_root_interface';self.assertTrue(self.errors(m))
    def test_external_reference_exists(self):
        m=copy.deepcopy(self.manifest);m['documents'][0]['artifact_relations']=[{'type':'implemented_as','target_artifact':'unknown'}];self.assertTrue(self.errors(m))
    def test_no_internal_support_catalog(self):
        self.assertFalse(any(d['path'].startswith('tools/') for d in self.manifest['documents']))
    def test_no_duplicate_english_scores(self):
        for d in self.manifest['documents']:
            if d['language_relation']['role']=='commensuration':self.assertNotIn('representative',d['assessment'])
    def test_public_projection_drops_unapproved_and_private_data(self):
        d={'assessment':{'applicability':'current_claim','review_state':'unreviewed','representative':{'strength':'S5','exposure':'E3'},'run_sha256':'secret','reviewer_note':'secret','confidence':1}}
        out=public_assessment(d);self.assertNotIn('representative',out);self.assertNotIn('secret',json.dumps(out))
    def test_public_projection_approved_allowlist(self):
        d={'assessment':{'applicability':'current_claim','review_state':'approved','representative':{'strength':'S1','exposure':'E0','secret':'hidden'},'approval':{'run_sha256':'hidden'},'hotspots':[{'label':'example','locator':'L1','strength':'S5','exposure':'E3','reviewer_note':'hidden'}]}}
        out=public_assessment(d);self.assertNotIn('hidden',json.dumps(out));self.assertEqual(out['representative']['strength'],'S1')
    def test_unsafe_paths(self):
        for path in ['../README.md','/tmp/x','.git/config','a/../../README.md','C:/x','a\\x']:
            with self.assertRaises(ValueError):resolve_repo_path(ROOT,path)
    def test_generated_json_schemas(self):
        for schema,data in [('docs_index.schema.json','docs_index.json'),('docs_graph.schema.json','docs_graph.json')]:
            Draft202012Validator(json.loads((ROOT/'tools'/schema).read_text(encoding="utf-8"))).validate(json.loads((ROOT/'tools'/data).read_text(encoding="utf-8")))
    def test_partial_translation_preserved(self):
        d=next(x for x in self.manifest['documents'] if x['path'].endswith('Return_Intake_Log.en.md'));self.assertEqual(d['language_relation']['coverage'],'partial')
    def test_rollback_restores_derived_files(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);p=root/GENERATED_FILES[0];p.parent.mkdir(parents=True);p.write_bytes(b'old');build=root/BUILD_DIRECTORY;build.mkdir(parents=True);(build/'index').write_bytes(b'old')
            def fail():
                p.write_bytes(b'new');(root/GENERATED_FILES[1]).write_bytes(b'new');(build/'index').write_bytes(b'new');raise ValueError('intentional failure')
            with self.assertRaises(ValueError):transactional_rebuild(root,fail)
            self.assertEqual(p.read_bytes(),b'old');self.assertFalse((root/GENERATED_FILES[1]).exists());self.assertEqual((build/'index').read_bytes(),b'old')
    def test_explicit_review_not_aggregate(self):
        with tempfile.TemporaryDirectory() as temp:
            rp,vp,run,review=fixture(ROOT,Path(temp));result=summaries_from_review(ROOT,rp,vp);summary=next(iter(result.values()));self.assertEqual(summary['representative']['strength'],'S1');self.assertEqual(summary['hotspots'],[]);self.assertTrue(summary['unresolved'])
            h=run['repository_assessment_run']['documents'][0]['claim_hotspots'][0];path=run['repository_assessment_run']['documents'][0]['path']
            review['repository_assessment_review']['decisions'].append({'review_key':'claim_hotspot::TEST-H1','kind':'claim_hotspot','path':path,'decision':'approve','reviewed_at':'synthetic-test','before':h,'after':h});vp.write_text(json.dumps(review), encoding="utf-8")
            summary=next(iter(summaries_from_review(ROOT,rp,vp).values()));self.assertEqual(summary['representative']['strength'],'S1');self.assertEqual(summary['hotspots'][0]['strength'],'S5')
    def test_review_must_match_exact_raw_run(self):
        with tempfile.TemporaryDirectory() as temp:
            rp,vp,run,review=fixture(ROOT,Path(temp));review['repository_assessment_review']['decisions'][0]['before']['title']='changed';vp.write_text(json.dumps(review), encoding="utf-8")
            with self.assertRaises(ValueError):summaries_from_review(ROOT,rp,vp)
    def test_no_implicit_approval(self):
        with tempfile.TemporaryDirectory() as temp:
            rp,vp,run,review=fixture(ROOT,Path(temp));review['repository_assessment_review']['decisions'][0]['decision']='hold';vp.write_text(json.dumps(review), encoding="utf-8");self.assertEqual(summaries_from_review(ROOT,rp,vp),{})
    def test_bad_excerpt_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            rp,vp,run,review=fixture(ROOT,Path(temp));run['repository_assessment_run']['documents'][0]['claim_hotspots'][0]['source']['text']='not the source';rp.write_text(json.dumps(run), encoding="utf-8");review['repository_assessment_review']['source_run_sha256']=sha256(rp);vp.write_text(json.dumps(review), encoding="utf-8")
            with self.assertRaises(ValueError):summaries_from_review(ROOT,rp,vp)
    def test_declared_git_eol_is_not_content_edit_permission(self):
        import hashlib
        raw=b'a\r\nb\r\n';lf=raw.replace(b'\r\n',b'\n')
        e={'document_role':'provenance_asset','integrity':{'sha256':hashlib.sha256(raw).hexdigest(),'basis':'rc004_snapshot_not_historical_certification','git_lf_sha256':hashlib.sha256(lf).hexdigest(),'git_lf_basis':'rc004_HEAD_blob_CRLF_only_difference'}}
        self.assertTrue(asset_bytes_match(e,raw));self.assertTrue(asset_bytes_match(e,lf));self.assertFalse(asset_bytes_match(e,b'changed\n'))
        e['document_role']='fixed_research_source';self.assertFalse(asset_bytes_match(e,lf))
    def test_registration_requires_assessment_evidence(self):
        from prepare_assessment_registration_review import prepare
        from validate_registration_review import validate
        from apply_registration_review import apply_review
        with tempfile.TemporaryDirectory() as temp:
            rp,vp,run,review=fixture(ROOT,Path(temp));txn=prepare(ROOT,rp,vp)
            self.assertTrue(validate(txn));self.assertEqual(validate(txn,assessment_run=rp,assessment_review=vp),[])
            modified=copy.deepcopy(self.manifest);apply_review(modified,txn);self.assertEqual(self.errors(modified),[])
            # The fixture is not written to the live manifest.
            self.assertEqual(load_manifest(ROOT),self.manifest)

if __name__=='__main__':unittest.main(verbosity=2)

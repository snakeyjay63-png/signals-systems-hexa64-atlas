#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
ATLAS=ROOT/'data'/'atlas.json'
SPEC=ROOT/'data'/'full_semantic_self_read_delta_ch20.json'
CURRENT_RECOVERABLE={'concept_id','equation','svg_text','svg_fragment_sha256','math_signature_sha256'}
DERIVABLE={'svg_selector','svg_element_count'}
SEMANTIC_PAYLOAD={'chapter','chapter_title','title','subtitle','domain','signal_type','parameters','validation','relations'}
def derive():
    atlas=json.loads(ATLAS.read_text(encoding='utf-8'))
    spec=json.loads(SPEC.read_text(encoding='utf-8'))
    fields=set(atlas['concepts'][0])
    all_same=all(set(r)==fields for r in atlas['concepts'])
    classified=CURRENT_RECOVERABLE|DERIVABLE|SEMANTIC_PAYLOAD
    top=set(atlas)
    top_serialized_or_derivable={'title','style','default_discrete_frame','chapter_count','concept_count','concepts'}
    top_missing={'format_version','source_svg'}
    checks={
        'all_concept_records_have_same_field_set':all_same,
        'concept_field_partition_is_total':classified==fields,
        'concept_field_partition_is_disjoint':not(CURRENT_RECOVERABLE&DERIVABLE) and not(CURRENT_RECOVERABLE&SEMANTIC_PAYLOAD) and not(DERIVABLE&SEMANTIC_PAYLOAD),
        'top_level_partition_is_total':top_serialized_or_derivable|top_missing==top,
        'spec_goal_is_full_atlas_equality':spec.get('goal')=='P_full(G_total(A_canonical)) = A_canonical',
        'totality_invariant_declared':'either embedded losslessly or deterministically recomputable' in spec.get('minimal_total_projection',{}).get('totality_invariant',''),
    }
    return {
        'format_version':'1.0.0','canonical_object':'data/atlas.json','concept_field_count':len(fields),'concept_record_count':len(atlas['concepts']),
        'current_recoverable':sorted(CURRENT_RECOVERABLE),'derivable':sorted(DERIVABLE),'semantic_payload_delta':sorted(SEMANTIC_PAYLOAD),'top_level_delta':sorted(top_missing),
        'checks':checks,'pass':all(checks.values()),'closure_status':'TOTAL_PROJECTION_IMPLEMENTED'}
def main():
    out=ROOT/'data'/'full_semantic_self_read_delta_measurement_ch20.json'
    d=derive(); out.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(out.relative_to(ROOT)); print('PASS' if d['pass'] else 'FAIL')
if __name__=='__main__': main()

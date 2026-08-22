#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def _canon(obj):
    return json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode("utf-8")

def canonical_discrete_field():
    abjad=json.loads((ROOT/"data/abjad_field.json").read_text(encoding="utf-8"))
    closure=json.loads((ROOT/"data/language_closure_7.json").read_text(encoding="utf-8"))
    ch18=json.loads((ROOT/"data/transformer_frame_ch18.json").read_text(encoding="utf-8"))
    ch19=json.loads((ROOT/"data/choice_geometry_ch19.json").read_text(encoding="utf-8"))

    # Exact/canonical subset only. No model weights, logits, embeddings or token IDs.
    return {
        "mod9_orbits":{
            "V1":[1,2,4,8,7,5],
            "V3":[3,6],
            "V9":[9],
            "transform":"T(r)=dr(2r)"
        },
        "closure_7_cardinality":{
            "prequotient":len(closure["prequotient"]["points"]),
            "quotient":len(closure["quotient"]["points"]),
            "carrier_count":len(closure["quotient"]["C_prime"]),
            "structure_count":len(closure["quotient"]["S_prime"])
        },
        "choice_accounting":{
            "used":ch19["choice_accounting"]["used_choice_ids"],
            "locked":ch19["choice_accounting"]["locked_choice_ids"],
            "routed_open":ch19["choice_accounting"]["routed_open_choice_ids"],
            "closure_complete":ch19["choice_accounting"]["closure_complete"],
            "closure_semantics":ch19["choice_accounting"]["closure_semantics"]
        },
        "chapter19_open_bridge":{
            k:v for k,v in next(x for x in ch19["choice_registry"] if x["id"]=="theta_bridge").items()
            if k in {"id","kind","status","lock_policy","endpoint","endpoint_network_status","default_route_prefix"}
        },
        "chapter18_slice_scope":{
            "status":ch18["status"],
            "scope":ch18["axiom_audit"]["scope"],
            "selected_boundary":ch18["frame_correspondence"][2]["selected_candidate"]
        }
    }

def canonical_sha256(field=None):
    if field is None:
        field=canonical_discrete_field()
    return hashlib.sha256(_canon(field)).hexdigest()

def through_carrier(carrier_id:str):
    # The carrier label is intentionally not part of D.
    # This function witnesses the interface contract for test adapters only.
    if not carrier_id:
        raise ValueError("carrier_id required")
    return canonical_discrete_field()

def derive():
    field=canonical_discrete_field()
    a=through_carrier("carrier_A")
    b=through_carrier("carrier_B")
    return {
        "format_version":"1.0.0",
        "canonicalization":"JSON sort_keys=true; separators=(',',':'); UTF-8; ensure_ascii=false",
        "field":field,
        "canonical_sha256":canonical_sha256(field),
        "carrier_A_sha256":canonical_sha256(a),
        "carrier_B_sha256":canonical_sha256(b),
        "deterministic_witness_match":a==b and canonical_sha256(a)==canonical_sha256(b),
        "carrier_content_consumed":False,
        "reader_independence_proven":False,
        "vacuity_status":"CURRENT ADAPTER IGNORES CARRIER CONTENT",
        "scope":"abstract label witnesses only; proves deterministic canonical-field reconstruction, not reader-independence"
    }

def main():
    out=ROOT/"data/carrier_invariance_measurement.json"
    out.write_text(json.dumps(derive(),ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(out.relative_to(ROOT))
    print(derive()["canonical_sha256"])

if __name__=="__main__":
    main()

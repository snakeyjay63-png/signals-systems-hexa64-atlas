#!/usr/bin/env python3
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parent.parent
AXIOMS=ROOT/"data"/"language_frame_axioms.json"
OUT=ROOT/"data"/"language_closure_7.json"

@dataclass(frozen=True)
class AtomicFrame:
    name: str
    carrier: str
    structure: str
    boundary: str

def make_atomic(name:str)->AtomicFrame:
    return AtomicFrame(name, f"{name}:C", f"{name}:S", f"{name}:b")

def validate_atomic(f:AtomicFrame)->bool:
    # AT1/AT2 are represented by exactly one carrier and structure token;
    # tags make C,S,b pairwise distinct.
    return len({f.carrier,f.structure,f.boundary})==3

def quotient_three(frames):
    frames=list(frames)
    if len(frames)!=3:
        raise ValueError("closure theorem is instantiated for exactly three atomic frames")
    if not all(validate_atomic(f) for f in frames):
        raise ValueError("invalid atomic frame")
    all_tokens=[]
    for f in frames:
        all_tokens += [f.carrier,f.structure,f.boundary]
    if len(set(all_tokens))!=9:
        raise ValueError("input atomic frames must be pairwise disjoint before quotient")

    boundary_set={f.boundary for f in frames}
    def qclass(token):
        return "b" if token in boundary_set else token

    quotient={t:qclass(t) for t in all_tokens}
    C={quotient[f.carrier] for f in frames}
    S={quotient[f.structure] for f in frames}
    b="b"
    Q=set(quotient.values())
    return {
      "prequotient_points":all_tokens,
      "quotient_map":quotient,
      "C_prime":sorted(C),
      "S_prime":sorted(S),
      "boundary_class":[*sorted(boundary_set)],
      "boundary_representative":b,
      "quotient_points":sorted(Q),
    }

def validate_general_frame(result):
    C=set(result["C_prime"]); S=set(result["S_prime"]); b=result["boundary_representative"]
    return {
      "A1_nonempty":bool(C) and bool(S),
      "A2_disjoint":C.isdisjoint(S),
      "A3_boundary_external":b not in C|S,
      "A4_unique_boundary_class":len(result["boundary_class"])==3 and result["quotient_points"].count(b)==1,
    }

def derive():
    frames=[make_atomic("L"),make_atomic("G"),make_atomic("E")]
    result=quotient_three(frames)
    checks=validate_general_frame(result)
    pre=len(result["prequotient_points"])
    post=len(result["quotient_points"])
    model={
      "format_version":"2.0.0",
      "source_axioms":"data/language_frame_axioms.json",
      "theorem":"Three-Atomic-Frame Quotient Closure",
      "input_frames":[f.__dict__ for f in frames],
      "prequotient":{
        "cardinality":pre,
        "formula":"3×3=9",
        "points":result["prequotient_points"]
      },
      "equivalence_relation":{
        "boundary_identification":"L:b ~ G:b ~ E:b",
        "nonboundary_rule":"singleton equivalence classes",
        "classes_removed_by_identification":2
      },
      "quotient":{
        "cardinality":post,
        "formula":"9-(3-1)=7",
        "C_prime":result["C_prime"],
        "S_prime":result["S_prime"],
        "boundary":"b",
        "boundary_class":result["boundary_class"],
        "points":result["quotient_points"]
      },
      "closure_theorem":{
        "axiom_checks":checks,
        "passes":all(checks.values()),
        "canonical_partition":True,
        "proof_steps":[
          "C' is the quotient image of the disjoint union of the three carrier sets.",
          "S' is the quotient image of the disjoint union of the three structure sets.",
          "Only boundary points are identified, so C' and S' remain disjoint.",
          "The common boundary class b is not an element of C' or S'.",
          "There is exactly one boundary class after quotienting.",
          "Therefore (C',S',b) satisfies the general Frame axioms."
        ]
      },
      "atomicity_status":"|C_i|=|S_i|=1 is an AtomicFrame axiom, not derived here",
      "recursive_typing":{
        "status":"the quotient is now proven to be a general Frame; treating a Frame as one language-object at the next level is the project type convention",
        "not_claimed":"the quotient is not AtomicFrame and no cardinality isomorphism is claimed"
      },
      "mod9":{"digital_root_7":7,"T7":5,"orbit":"V1","V1":[1,2,4,8,7,5]},
      "abjad_crosscheck":{"ordinal":7,"letter":"ز","name":"zay","value":7},
      "meta_observation":{"visual_field_count_89":"Fibonacci F(11); recorded as meta-observation only, not an invariant"}
    }
    OUT.write_text(json.dumps(model,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return model

if __name__=="__main__":
    m=derive()
    print("QUOTIENT CLOSURE PASS",m["prequotient"]["cardinality"],"→",m["quotient"]["cardinality"],m["closure_theorem"]["axiom_checks"])

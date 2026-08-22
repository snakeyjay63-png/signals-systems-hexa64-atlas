#!/usr/bin/env python3
from __future__ import annotations
import json, re
from pathlib import Path
from independent_property_reader import derive_from_text

ROOT=Path(__file__).resolve().parents[1]
SVG=ROOT/"assets"/"signals_systems_full_atlas_master.svg"
ATLAS=ROOT/"data"/"atlas.json"

def mutate_hash_char(text):
    # Target the visible Ch14 sha256(raw) field specifically; verification metadata
    # also contains 64-hex values and must not make this fault ambiguous.
    m=re.search(r'(sha256\(raw\)\s*=\s*)([0-9a-f]{64})', text)
    if not m:
        raise RuntimeError("visible Ch14 sha256(raw) not found in SVG")
    h=m.group(2)
    flip=('0' if h[0] != '0' else '1') + h[1:]
    return text[:m.start(2)] + flip + text[m.end(2):]

def mutate_remove_field(text):
    # Remove exactly one concept group's data-concept attribute so P_chi sees 102.
    return text.replace(' data-concept="', ' data-concept-removed="', 1)

def mutate_swap_ids(text):
    ids=re.findall(r'data-concept="([^"]+)"', text)
    if len(ids)<2:
        raise RuntimeError("not enough ids")
    a,b=ids[0],ids[1]
    token="__TMP_CONCEPT_ID__"
    text=text.replace(f'data-concept="{a}"',f'data-concept="{token}"',1)
    text=text.replace(f'data-concept="{b}"',f'data-concept="{a}"',1)
    text=text.replace(f'data-concept="{token}"',f'data-concept="{b}"',1)
    return text

def mutate_add_field(text):
    # Add one syntactically valid extra concept/equation pair: 103 -> 104.
    insertion='<g data-concept="fault_extra" data-equation=""></g>\n'
    return text.replace('</svg>',insertion+'</svg>',1)

def mutate_empty_equation(text):
    return re.sub(r'data-equation="[^"]+"','data-equation=""',text,count=1)

MUTATIONS={
    "M1_hash_char_flip":mutate_hash_char,
    "M2_remove_field":mutate_remove_field,
    "M3_swap_two_ids":mutate_swap_ids,
    "M4_add_field_103_to_104":mutate_add_field,
    "M5_empty_one_equation":mutate_empty_equation,
}

EXPECTED={
    "M1_hash_char_flip":True,
    "M2_remove_field":True,
    "M3_swap_two_ids":True,
    "M4_add_field_103_to_104":True,
    "M5_empty_one_equation":True,
}

def derive():
    text=SVG.read_text(encoding="utf-8")
    atlas=json.loads(ATLAS.read_text(encoding="utf-8"))
    baseline=derive_from_text(text,atlas)
    rows=[]
    for mid,fn in MUTATIONS.items():
        mutated=fn(text)
        result=derive_from_text(mutated,atlas)
        detected=not result["pass"]
        failed=[k for k,v in result["checks"].items() if not v]
        rows.append({
            "mutation":mid,
            "expected_detected":EXPECTED[mid],
            "detected":detected,
            "expectation_match":detected==EXPECTED[mid],
            "failed_checks":failed,
        })
    return {
        "format_version":"1.0.0",
        "reader":"P_χ",
        "baseline_pass":baseline["pass"],
        "mutations":rows,
        "all_expectations_match":baseline["pass"] and all(x["expectation_match"] for x in rows),
        "sensitivity_summary":{
            "detected":[x["mutation"] for x in rows if x["detected"]],
            "not_detected":[x["mutation"] for x in rows if not x["detected"]],
            "boundary":"P_χ now recomputes the Ch14 PNG SHA-256 independently and enforces non-empty equation content; broader semantic correctness remains out of scope"
        }
    }

def main():
    out=ROOT/"data"/"independent_reader_fault_injection_ch20.json"
    d=derive()
    out.write_text(json.dumps(d,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(out.relative_to(ROOT))
    print("PASS" if d["all_expectations_match"] else "FAIL")

if __name__=="__main__":
    main()

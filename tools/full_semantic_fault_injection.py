#!/usr/bin/env python3
from __future__ import annotations
import base64, json, xml.etree.ElementTree as ET
from pathlib import Path
from canonical_json import canonical_bytes
from full_semantic_self_read import derive_from_text

ROOT=Path(__file__).resolve().parents[1]
SVG=ROOT/"assets"/"signals_systems_full_atlas_master.svg"
ATLAS=ROOT/"data"/"atlas.json"

def mutate_parameter(text):
    root=ET.fromstring(text)
    attr="data-sem-parameters-b64"
    for g in root.iter():
        if not g.attrib.get("data-concept") or attr not in g.attrib:
            continue
        params=json.loads(base64.b64decode(g.attrib[attr]).decode())
        if params:
            # Add a deterministic mutation marker inside semantic parameters.
            params["__fault_injection__"]="M6"
            g.attrib[attr]=base64.b64encode(canonical_bytes(params)).decode()
            return ET.tostring(root,encoding="unicode")
    raise RuntimeError("no nonempty parameters found")

def mutate_record_reorder(text):
    root=ET.fromstring(text)
    groups=[g for g in list(root) if g.attrib.get("data-concept")]
    # Swap last concept of chapter 1 with first concept of chapter 2: crosses a chapter boundary.
    a,b=groups[4],groups[5]
    children=list(root); ia=children.index(a); ib=children.index(b)
    children[ia],children[ib]=children[ib],children[ia]
    root[:] = children
    return ET.tostring(root,encoding="unicode")

def derive():
    text=SVG.read_text(encoding="utf-8")
    committed=json.loads(ATLAS.read_text(encoding="utf-8"))
    base=derive_from_text(text,committed)
    m6=derive_from_text(mutate_parameter(text),committed)
    m7=derive_from_text(mutate_record_reorder(text),committed)
    return {
      "format_version":"1.0.0",
      "baseline_exact":base["status"]=="EXACT_FULL_SEMANTIC",
      "M6_parameter_corruption":{
        "detected":m6["status"]=="FAIL",
        "canonical_equal":m6["canonical_equal"],
        "local_math_failures":[x["concept_id"] for x in m6["local"] if not x["math_hash_match"]],
      },
      "M7_record_reorder":{
        "detected":m7["status"]=="FAIL",
        "canonical_equal":m7["canonical_equal"],
        "chapter_crosscheck_failures":[x["concept_id"] for x in m7["local"] if not x["chapter_crosscheck"]],
      },
      "pass":base["status"]=="EXACT_FULL_SEMANTIC" and m6["status"]=="FAIL" and m7["status"]=="FAIL",
      "scope":"semantic fault injection for local math-signature verification and chapter/order cross-check"
    }

def main():
    out=ROOT/"data"/"full_semantic_fault_injection_ch20.json"
    d=derive(); out.write_text(json.dumps(d,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(out.relative_to(ROOT)); print("PASS" if d["pass"] else "FAIL")
if __name__=="__main__": main()

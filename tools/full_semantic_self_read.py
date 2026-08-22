#!/usr/bin/env python3
from __future__ import annotations
import base64, hashlib, html, json, re, xml.etree.ElementTree as ET
from pathlib import Path
from canonical_json import canonical_bytes, canonical_json

ROOT=Path(__file__).resolve().parents[1]
SVG=ROOT/"assets"/"signals_systems_full_atlas_master.svg"
ATLAS=ROOT/"data"/"atlas.json"

PAYLOAD_FIELDS=["chapter","chapter_title","title","subtitle","domain","signal_type","parameters","validation","relations"]
def clean(s): return " ".join((s or "").split())
def attr_name(field): return "data-sem-"+field.replace("_","-")+"-b64"
def decode_payload(g):
    return {
        field:json.loads(base64.b64decode(g.attrib[attr_name(field)]).decode("utf-8"))
        for field in PAYLOAD_FIELDS
    }
def math_hash(r):
    p={"concept_id":r["concept_id"],"equation":r["equation"],"parameters":r["parameters"],"validation":r["validation"]}
    return hashlib.sha256(canonical_bytes(p)).hexdigest()

def derive_from_text(text, committed=None):
    if committed is None:
        committed=json.loads(ATLAS.read_text(encoding="utf-8"))
    root=ET.fromstring(text)
    ns={"svg":"http://www.w3.org/2000/svg"}
    md=json.loads(root.find("svg:metadata",ns).text)
    proj=md["canonical_projection"]; ver=md["verification"]
    groups=[g for g in root.iter() if g.attrib.get("data-concept")]
    counts={int(k):v for k,v in proj["chapter_concept_counts"].items()}
    derived_ch=[]
    for ch in range(1,len(md["chapters"])+1): derived_ch += [ch]*counts[ch]
    records=[]; local=[]
    for idx,g in enumerate(groups):
        cid=g.attrib["data-concept"]
        payload=decode_payload(g)
        texts=[clean("".join(e.itertext())) for e in g.iter() if e.tag.endswith("text")]
        texts=[x for x in texts if x]
        rec=dict(payload)
        rec.update({
            "concept_id":cid,
            "equation":html.unescape(g.attrib.get("data-equation","")),
            "svg_selector":f'[data-concept="{cid}"]',
            "svg_element_count":sum(1 for _ in g.iter()),
            "svg_text":texts,
        })
        rec["svg_fragment_sha256"]=hashlib.sha256(ET.tostring(g,encoding="utf-8")).hexdigest()
        rec["math_signature_sha256"]=math_hash(rec)
        local.append({
            "concept_id":cid,
            "math_hash_match":rec["math_signature_sha256"]==ver["math_signature_sha256"][cid],
            "svg_hash_match":rec["svg_fragment_sha256"]==ver["svg_fragment_sha256"][cid],
            "chapter_crosscheck":rec["chapter"]==derived_ch[idx] and rec["chapter_title"]==md["chapters"][derived_ch[idx]-1]["title"],
        })
        records.append(rec)
    rebuilt={
        "format_version":proj["format_version"],"title":md["title"],"style":md["style"],
        "default_discrete_frame":md["default_discrete_frame"],"chapter_count":len(md["chapters"]),
        "concept_count":len(records),"source_svg":proj["source_svg"],"concepts":records
    }
    return {
        "format_version":"1.0.0",
        "local_verification_pass":all(all(x[k] for k in ("math_hash_match","svg_hash_match","chapter_crosscheck")) for x in local),
        "local":local,
        "canonical_equal":canonical_json(rebuilt)==canonical_json(committed),
        "status":"EXACT_FULL_SEMANTIC" if canonical_json(rebuilt)==canonical_json(committed) and all(all(x[k] for k in ("math_hash_match","svg_hash_match","chapter_crosscheck")) for x in local) else "FAIL",
        "rebuilt_sha256":hashlib.sha256(canonical_bytes(rebuilt)).hexdigest(),
        "committed_sha256":hashlib.sha256(canonical_bytes(committed)).hexdigest(),
    }

def derive():
    return derive_from_text(SVG.read_text(encoding="utf-8"))

def main():
    out=ROOT/"data"/"full_semantic_self_read_measurement_ch20.json"
    d=derive(); out.write_text(json.dumps(d,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(out.relative_to(ROOT)); print(d["status"])
if __name__=="__main__": main()

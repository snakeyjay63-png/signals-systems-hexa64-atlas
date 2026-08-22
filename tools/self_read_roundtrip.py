#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
SVG=ROOT/"assets"/"signals_systems_full_atlas_master.svg"
ATLAS=ROOT/"data"/"atlas.json"

def clean(s):
    return " ".join((s or "").split())

def parse_svg():
    root=ET.fromstring(SVG.read_text(encoding="utf-8"))
    groups=[g for g in root.iter() if "data-concept" in g.attrib]
    records=[]
    for g in groups:
        texts=[clean("".join(el.itertext())) for el in g.iter() if el.tag.endswith("text")]
        texts=[x for x in texts if x]
        records.append({
            "concept_id":g.attrib["data-concept"],
            "equation":g.attrib.get("data-equation",""),
            "svg_text":texts,
            "svg_fragment_sha256":hashlib.sha256(ET.tostring(g,encoding="utf-8")).hexdigest()
        })
    ns={"svg":"http://www.w3.org/2000/svg"}
    metadata=json.loads(root.find("svg:metadata",ns).text)
    return records,metadata

def committed_subset():
    atlas=json.loads(ATLAS.read_text(encoding="utf-8"))
    records=[{
        "concept_id":r["concept_id"],
        "equation":r.get("equation",""),
        "svg_text":r.get("svg_text",[]),
        "svg_fragment_sha256":r.get("svg_fragment_sha256")
    } for r in atlas["concepts"]]
    titles=[next(r["chapter_title"] for r in atlas["concepts"] if r["chapter"]==i)
            for i in range(1,atlas["chapter_count"]+1)]
    return atlas,records,titles

def derive():
    parsed,metadata=parse_svg()
    atlas,committed,titles=committed_subset()
    eq=sum(a["equation"]==b["equation"] for a,b in zip(parsed,committed))
    txt=sum(a["svg_text"]==b["svg_text"] for a,b in zip(parsed,committed))
    frag=sum(a["svg_fragment_sha256"]==b["svg_fragment_sha256"] for a,b in zip(parsed,committed))
    ids=[a["concept_id"] for a in parsed]==[b["concept_id"] for b in committed]
    chapters=[x["title"] for x in metadata["chapters"]]==titles
    exact=(parsed==committed and chapters and len(metadata["chapters"])==atlas["chapter_count"])
    return {
        "format_version":"1.0.0",
        "parser":"XML ElementTree + exporter-compatible whitespace canonicalization",
        "serialized_subset":{
            "concept_id":"recoverable",
            "equation":"recoverable",
            "svg_text":"recoverable after canonical whitespace",
            "svg_fragment_sha256":"recomputable",
            "chapter_titles":"recoverable from SVG metadata"
        },
        "counts":{
            "concepts_parsed":len(parsed),
            "concepts_committed":len(committed),
            "equations_match":eq,
            "texts_match":txt,
            "fragment_hashes_match":frag,
            "chapters_in_metadata":len(metadata["chapters"])
        },
        "concept_order_match":ids,
        "chapter_titles_match":chapters,
        "roundtrip_exact_on_serialized_subset":exact,
        "not_recoverable_from_svg_alone":[
            "full concept parameters",
            "full validation objects",
            "full relation graph",
            "external data files not embedded in SVG"
        ],
        "status":"EXACT_ON_SERIALIZED_SUBSET" if exact else "FAIL",
        "full_self_reading":"OPEN"
    }

def main():
    out=ROOT/"data"/"self_read_roundtrip_ch20.json"
    d=derive()
    out.write_text(json.dumps(d,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(out.relative_to(ROOT))
    print(d["status"])

if __name__=="__main__":
    main()

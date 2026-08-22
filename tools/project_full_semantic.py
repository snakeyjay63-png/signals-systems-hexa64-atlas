#!/usr/bin/env python3
from __future__ import annotations
import base64, json, re
from pathlib import Path
from canonical_json import canonical_bytes

ROOT=Path(__file__).resolve().parents[1]
SVG=ROOT/"assets"/"signals_systems_full_atlas_master.svg"
ATLAS=ROOT/"data"/"atlas.json"
PAYLOAD_FIELDS=["chapter","chapter_title","title","subtitle","domain","signal_type","parameters","validation","relations"]

def attr_name(field:str)->str:
    return "data-sem-"+field.replace("_","-")+"-b64"

def encode(value)->str:
    return base64.b64encode(canonical_bytes(value)).decode("ascii")

def main():
    atlas=json.loads(ATLAS.read_text(encoding="utf-8"))
    text=SVG.read_text(encoding="utf-8")
    by={r["concept_id"]:r for r in atlas["concepts"]}

    for cid,r in by.items():
        pat=re.compile(r'(<g\b[^>]*\bdata-concept="'+re.escape(cid)+r'"[^>]*)(>)')
        m=pat.search(text)
        if not m:
            raise SystemExit(f"missing group {cid}")
        start=m.group(1)

        # Remove only projection-owned attributes from prior runs.
        start=re.sub(r'\sdata-semantic-b64="[^"]*"','',start)
        start=re.sub(r'\sdata-sem-[a-z0-9-]+-b64="[^"]*"','',start)

        # AGNI: additive projection. Existing data-concept/data-equation attributes
        # and all child SVG content are left untouched.
        attrs="".join(
            f' {attr_name(field)}="{encode(r[field])}"'
            for field in PAYLOAD_FIELDS
        )
        repl=start+attrs+">"
        text=text[:m.start()]+repl+text[m.end():]

    meta=re.search(r'<metadata id="atlas-data"><!\[CDATA\[(.*?)\]\]></metadata>',text,re.S)
    if not meta:
        raise SystemExit("atlas-data metadata missing")
    md=json.loads(meta.group(1))
    counts={}
    for r in atlas["concepts"]:
        counts[str(r["chapter"])]=counts.get(str(r["chapter"]),0)+1
    md["canonical_projection"]={
        "format_version":atlas["format_version"],
        "source_svg":atlas["source_svg"],
        "canonical_json_spec":"canonical-json-v1",
        "chapter_concept_counts":counts,
        "payload_fields":PAYLOAD_FIELDS,
        "payload_encoding":"one canonicalJSON(Base64) data-sem-*-b64 attribute per payload field",
        "agni_rule":"additive semantic projection; existing concept/equation/content is not replaced",
    }
    md["verification"]={
        "math_signature_sha256":{r["concept_id"]:r["math_signature_sha256"] for r in atlas["concepts"]},
        "svg_fragment_sha256":{r["concept_id"]:r["svg_fragment_sha256"] for r in atlas["concepts"]},
    }
    newmeta='<metadata id="atlas-data"><![CDATA['+json.dumps(md,ensure_ascii=False)+']]></metadata>'
    text=text[:meta.start()]+newmeta+text[meta.end():]
    SVG.write_text(text,encoding="utf-8")
    print(f"embedded {len(PAYLOAD_FIELDS)} additive payload attributes for {len(by)} concepts")

if __name__=="__main__":
    main()

#!/usr/bin/env python3
from __future__ import annotations
import html, json, re, hashlib
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SVG=ROOT/"assets"/"signals_systems_full_atlas_master.svg"
ATLAS=ROOT/"data"/"atlas.json"
CH14_PNG=ROOT/"assets"/"ch14_test_object.png"
HASH_LINE_RE=re.compile(r"sha256\(raw\)\s*=\s*([0-9a-f]{64})")

# Deliberately independent from the XML parser route used by self_read_roundtrip.py.
# No ElementTree; no exporter cleaning/parsing helpers.
CONCEPT_RE=re.compile(r'data-concept="([^"]+)"')
EQUATION_RE=re.compile(r'data-equation="([^"]*)"')
META_RE=re.compile(r'<metadata\b[^>]*>\s*(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?\s*</metadata>',re.S)
ID_RE=re.compile(r'^[a-z0-9][a-z0-9_]*$')

def derive_from_text(text, atlas=None):
    if atlas is None:
        atlas=json.loads(ATLAS.read_text(encoding="utf-8"))

    ids=CONCEPT_RE.findall(text)
    equations=[html.unescape(x) for x in EQUATION_RE.findall(text)]
    mm=META_RE.search(text)
    metadata=json.loads(mm.group(1)) if mm else {}

    committed_ids=[r["concept_id"] for r in atlas["concepts"]]
    committed_titles=[
        next(r["chapter_title"] for r in atlas["concepts"] if r["chapter"]==i)
        for i in range(1,atlas["chapter_count"]+1)
    ]
    metadata_titles=[x["title"] for x in metadata.get("chapters",[])]
    visible_raw_hash_match=HASH_LINE_RE.search(text)
    expected_raw_hash=hashlib.sha256(CH14_PNG.read_bytes()).hexdigest()
    visible_raw_hash=(visible_raw_hash_match.group(1) if visible_raw_hash_match else None)

    checks={
        "concept_count_103":len(ids)==103,
        "concept_ids_unique":len(set(ids))==103,
        "concept_order_matches_atlas":ids==committed_ids,
        "concept_id_syntax":all(ID_RE.fullmatch(x) for x in ids),
        "equation_attribute_count_103":len(equations)==103,
        "equation_content_nonempty":len(equations)==103 and all(bool(x.strip()) for x in equations),
        "ch14_png_sha256_recomputed":visible_raw_hash==expected_raw_hash,
        "metadata_chapter_count_20":len(metadata.get("chapters",[]))==20,
        "metadata_titles_match_atlas":metadata_titles==committed_titles,
    }
    return {
        "format_version":"1.0.0",
        "reader":"P_χ",
        "implementation":"raw SVG text + regular expressions + stdlib json/html/hashlib",
        "shared_parser_code_with_P_phi":False,
        "property_based":True,
        "checks":checks,
        "pass":all(checks.values()),
        "scope":"independent structural + selected semantic property agreement; does not prove full semantic correctness",
        "common_mode_mitigation":"uses a separate non-XML-parser implementation path"
    }

def derive():
    return derive_from_text(SVG.read_text(encoding="utf-8"))

def main():
    out=ROOT/"data"/"independent_reader_measurement_ch20.json"
    d=derive()
    out.write_text(json.dumps(d,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(out.relative_to(ROOT))
    print("PASS" if d["pass"] else "FAIL")

if __name__=="__main__":
    main()

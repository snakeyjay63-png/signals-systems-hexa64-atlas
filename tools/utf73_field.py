#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import json
import numpy as np

ROOT=Path(__file__).resolve().parent.parent
SPEC_PATH=ROOT/"data"/"utf73_field.json"

def load_spec():
    return json.loads(SPEC_PATH.read_text(encoding="utf-8"))

def symbols():
    s=load_spec()
    return [c["char"]+m["char"] for c in s["consonants"] for m in s["states12"]] + [s["shunya"]["char"]]

def rgb_to_state_scalar(r:int,g:int,b:int)->int:
    r=int(r); g=int(g); b=int(b)
    if not all(0 <= x <= 255 for x in (r,g,b)):
        raise ValueError("RGB channels must be 0..255")
    if r==0 and g==0 and b==0:
        return 72
    mx=max(r,g,b); mn=min(r,g,b); d=mx-mn
    if d==0:
        h6=0.0
    elif mx==r:
        h6=((g-b)/d) % 6.0
    elif mx==g:
        h6=((b-r)/d) + 2.0
    else:
        h6=((r-g)/d) + 4.0
    sector=int(np.floor(h6)) % 6
    brightness=min(11,(mx*12)//256)
    return sector*12+brightness

def exhaustive_rgb24_basins()->np.ndarray:
    counts=np.zeros(73,dtype=np.int64)
    gb=np.arange(256,dtype=np.float64)
    G,B=np.meshgrid(gb,gb,indexing="ij")
    for rv in range(256):
        R=np.full_like(G,float(rv))
        mx=np.maximum(np.maximum(R,G),B)
        mn=np.minimum(np.minimum(R,G),B)
        d=mx-mn
        h6=np.zeros_like(mx)
        nz=d!=0
        mr=nz & (mx==R)
        mg=nz & (mx==G) & ~mr
        mb=nz & ~(mr|mg)
        h6[mr]=np.mod((G[mr]-B[mr])/d[mr],6.0)
        h6[mg]=(B[mg]-R[mg])/d[mg]+2.0
        h6[mb]=(R[mb]-G[mb])/d[mb]+4.0
        sector=np.floor(h6).astype(np.int64)%6
        bright=np.minimum(11,(mx.astype(np.int64)*12)//256)
        idx=sector*12+bright
        if rv==0:
            idx[0,0]=72
        counts += np.bincount(idx.ravel(),minlength=73)
    return counts

def state_records(counts=None):
    spec=load_spec()
    rows=[]; idx=0
    for c in spec["consonants"]:
        for m in spec["states12"]:
            s=c["char"]+m["char"]
            row={
              "index":idx,"symbol":s,"consonant":c["roman"],"vowel_state":m["name"],
              "codepoints":[f"U+{ord(ch):04X}" for ch in s],
              "utf8_hex":s.encode("utf-8").hex(" "),
              "utf8_length":len(s.encode("utf-8")),
            }
            if counts is not None: row["rgb24_basin_size"]=int(counts[idx])
            rows.append(row); idx+=1
    sh=spec["shunya"]["char"]
    row={"index":72,"symbol":sh,"consonant":None,"vowel_state":"śūnya",
         "codepoints":[f"U+{ord(sh):04X}"],"utf8_hex":sh.encode().hex(" "),
         "utf8_length":len(sh.encode())}
    if counts is not None: row["rgb24_basin_size"]=int(counts[72])
    rows.append(row)
    return rows

def write_basins(path=None):
    if path is None: path=ROOT/"data"/"utf73_rgb24_basins.json"
    counts=exhaustive_rgb24_basins()
    rows=[{"index":r["index"],"symbol":r["symbol"],"rgb24_basin_size":r["rgb24_basin_size"]}
          for r in state_records(counts)]
    out={"encoder":"RGB24 → HSV hue sector × V bin; black → śūnya",
         "input_states":2**24,"state_count":73,"sum":int(counts.sum()),
         "min":int(counts.min()),"max":int(counts.max()),"states":rows}
    path.write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return out

def write_dataset(counts=None):
    if counts is None:
        basin=json.loads((ROOT/"data"/"utf73_rgb24_basins.json").read_text(encoding="utf-8"))
        counts=np.array([x["rgb24_basin_size"] for x in basin["states"]],dtype=np.int64)
    q,r=divmod(2**24,73)
    out={
      "format":"Sanskrit-UTF73 canonical field",
      "status":"custom 73-state field using standard Unicode code points; not a Unicode encoding standard",
      "state_count":73,
      "construction":"6 consonants × (inherent a + 11 explicit signs, anusvāra U+0902 in slot 12) + abstract śūnya displayed as U+00B7",
      "canonical_source":"data/utf73_field.json",
      "live_rgb24_encoder":"RGB24 → HSV hue sector × V bin; black → śūnya",
      "reference_quotient_model":{
        "status":"reference-model identity only; not the live pixel encoder",
        "encoder":"E73(n) = n mod 73",
        "decoder":"D73(s) = state index",
        "fixed_point_identity":"E73(D73(s)) = s",
        "basin_division":{"input_states":2**24,"quotient":q,"remainder":r,
          "large_basins":r,"large_size":q+1,"small_basins":73-r,"small_size":q}
      },
      "measured_rgb24_basins":{
        "input_states":2**24,"sum":int(counts.sum()),"min":int(counts.min()),
        "max":int(counts.max()),"shunya":int(counts[72])
      },
      "states":state_records(counts)
    }
    (ROOT/"data"/"sanskrit_utf73.json").write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return out

def write_browser_validator(dataset=None):
    if dataset is None:
        dataset=json.loads((ROOT/"data"/"sanskrit_utf73.json").read_text(encoding="utf-8"))
    js_states=json.dumps([{"i":s["index"],"symbol":s["symbol"],"name":s["vowel_state"],
                           "c":s["consonant"],"basin":s["rgb24_basin_size"]} for s in dataset["states"]],
                         ensure_ascii=False,separators=(",",":"))
    template = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>UTF73 Canonical Field Validator</title>
<style>
:root{--bg:#04060b;--panel:#07101b;--c:#65f4ff;--g:#6c7a94;--w:#edf6ff;--ok:#7dffb2}
body{margin:0;background:var(--bg);color:var(--w);font:14px ui-monospace,monospace}main{max-width:1200px;margin:auto;padding:28px}
.card{background:var(--panel);border:1px solid #6c7a9440;border-radius:14px;padding:16px;margin:14px 0}.ok{color:var(--ok)}.g{color:var(--g)}
table{width:100%;border-collapse:collapse}td,th{padding:6px;border-bottom:1px solid #6c7a9430;text-align:left}th{color:var(--c)}.sym{font:22px system-ui}
</style></head><body><main>
<h1>UTF73 · CANONICAL FIELD VALIDATOR</h1>
<p class="g">Custom field using standard Unicode code points. Not a Unicode/UTF standard. Canonical source: <code>data/utf73_field.json</code>.</p>
<div class="card" id="proof"></div><div class="card" id="basin"></div>
<div class="card"><table><thead><tr><th>#</th><th>symbol</th><th>codepoints</th><th>UTF-8</th><th>real RGB24 basin</th></tr></thead><tbody id="rows"></tbody></table></div>
<script>
const states=__STATES__;
const enc=new TextEncoder(),dec=new TextDecoder('utf-8',{fatal:true});
const cp=s=>[...s].map(ch=>'U+'+ch.codePointAt(0).toString(16).toUpperCase().padStart(4,'0'));
const hx=a=>[...a].map(x=>x.toString(16).padStart(2,'0')).join(' ');
const unique=new Set(states.map(s=>s.symbol)).size===73;
const utf8=states.every(s=>dec.decode(enc.encode(s.symbol))===s.symbol);
const E=n=>n%73,D=i=>i;
const fixed=states.every(s=>E(D(s.i))===s.i);
const basinSum=states.reduce((a,s)=>a+s.basin,0);
const q=Math.floor(2**24/73),r=(2**24)%73;
const b64Alphabet='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/';
const sample=String.fromCharCode(0x89,0x50,0x4e);
const sample64=btoa(sample);
const sampleBack=atob(sample64);
const b64Exact=sampleBack===sample;
document.querySelector('#proof').innerHTML=`<b>canonical states:</b> ${states.length} · unique: <span class="ok">${unique}</span> · UTF-8 roundtrip: <span class="ok">${utf8}</span><br>
<b>reference-model identity:</b> E(D(s))=s → <span class="ok">${fixed?'73/73 PASS':'FAIL'}</span><br>
<span class="g">This fixed-point is a construction identity, not the live encoder's lossiness proof.</span><br>
<b>native Base64 control:</b> ${sample64} · roundtrip=<span class="ok">${b64Exact}</span>`;
document.querySelector('#basin').innerHTML=`<b>live RGB24→HSV→Σ73 exhaustive basin sum:</b> <span class="ok">${basinSum.toLocaleString()}</span> = 2²⁴<br>
min=${Math.min(...states.map(s=>s.basin)).toLocaleString()} · max=${Math.max(...states.map(s=>s.basin)).toLocaleString()} · śūnya=${states[72].basin}<br>
<span class="g">reference quotient only: 2²⁴ = 73×${q.toLocaleString()} + ${r}</span>`;
document.querySelector('#rows').innerHTML=states.map(s=>{const u=enc.encode(s.symbol);return `<tr><td>${s.i}</td><td class="sym">${s.symbol}</td><td>${cp(s.symbol).join(' + ')}</td><td>${hx(u)}</td><td>${s.basin.toLocaleString()}</td></tr>`}).join('');
window.UTF73_VALIDATION={unique,utf8,fixed,basinSum,q,r,b64Exact};
</script></main></body></html>"""
    html=template.replace("__STATES__",js_states)
    out=ROOT/"validators"/"sanskrit_utf73.html"; out.parent.mkdir(exist_ok=True)
    out.write_text(html,encoding="utf-8")
    return out

def write_all():
    basin=write_basins()
    counts=np.array([x["rgb24_basin_size"] for x in basin["states"]],dtype=np.int64)
    dataset=write_dataset(counts)
    write_browser_validator(dataset)
    return basin,dataset

if __name__=="__main__":
    basin,_=write_all()
    print("RGB24 BASINS",basin["sum"],basin["min"],basin["max"])

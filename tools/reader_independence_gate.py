#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def evaluate_gate(adapter,c1,c2,cprime,D,independence_provenance:bool):
    r1=adapter(c1)
    r2=adapter(c2)
    rp=adapter(cprime)
    checks={
        "RI1":r1==D,
        "RI2":r2==D,
        "RI3":rp!=D,
        "independence_provenance":bool(independence_provenance),
    }
    return {"checks":checks,"pass":all(checks.values())}

def nonconstant_fixture(c):
    return "D" if c in {"c1","c2"} else "D_prime"

def constant_fixture(c):
    return "D"

def derive():
    valid=evaluate_gate(nonconstant_fixture,"c1","c2","cprime","D",True)
    constant=evaluate_gate(constant_fixture,"c1","c2","cprime","D",True)
    missing_provenance=evaluate_gate(nonconstant_fixture,"c1","c2","cprime","D",False)
    return {
        "format_version":"1.0.0",
        "valid_nonconstant_fixture":valid,
        "constant_fixture":constant,
        "missing_provenance_fixture":missing_provenance,
        "gate_logic_tested": valid["pass"] and (not constant["pass"]) and (not missing_provenance["pass"]),
        "scope":"synthetic unit test of gate logic only; not evidence for real model reader-independence"
    }

def main():
    out=ROOT/"data"/"reader_independence_gate_measurement_ch20.json"
    d=derive()
    out.write_text(json.dumps(d,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(out.relative_to(ROOT))
    print("PASS" if d["gate_logic_tested"] else "FAIL")

if __name__=="__main__":
    main()

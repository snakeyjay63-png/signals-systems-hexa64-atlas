#!/usr/bin/env python3
from __future__ import annotations
import subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
TOOLS=ROOT/"tools"
STEPS=[
 "generate_signals_systems_full_atlas.py",
 "export_concepts.py",
 "project_full_semantic.py",
 "export_concepts.py",
 "project_full_semantic.py",
 "carrier_invariance.py",
 "self_read_roundtrip.py",
 "independent_property_reader.py",
 "independent_reader_fault_injection.py",
 "reader_independence_gate.py",
 "full_semantic_delta.py",
 "full_semantic_self_read.py",
 "full_semantic_fault_injection.py",
 # Stabilize concept parameters that include committed measurement summaries.
 "export_concepts.py",
 "project_full_semantic.py",
 "export_concepts.py",
 "project_full_semantic.py",
 "self_read_roundtrip.py",
 "independent_property_reader.py",
 "independent_reader_fault_injection.py",
 "full_semantic_delta.py",
 "full_semantic_self_read.py",
 "full_semantic_fault_injection.py",
]
def main():
    for name in STEPS:
        p=subprocess.run([sys.executable,str(TOOLS/name)],cwd=ROOT)
        if p.returncode:
            raise SystemExit(p.returncode)
    print("TOTAL PROJECTION BUILD PASS")
if __name__=="__main__": main()

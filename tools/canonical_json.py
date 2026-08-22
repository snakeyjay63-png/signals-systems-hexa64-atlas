#!/usr/bin/env python3
from __future__ import annotations
import json, math, unicodedata
from typing import Any

SPEC_VERSION="canonical-json-v1"
SPEC={
    "unicode":"NFC recursively on every string value and object key",
    "object_keys":"lexicographic sort after NFC normalization",
    "whitespace":"none outside JSON string literals",
    "encoding":"UTF-8",
    "ensure_ascii":False,
    "floats":"Python JSON shortest round-trippable finite IEEE-754 binary64 decimal representation; NaN/Infinity rejected",
    "separators":[",",":"],
}

def normalize(value:Any)->Any:
    if isinstance(value,str):
        return unicodedata.normalize("NFC",value)
    if value is None or isinstance(value,(bool,int)):
        return value
    if isinstance(value,float):
        if not math.isfinite(value):
            raise ValueError("canonicalJSON rejects non-finite floats")
        return value
    if isinstance(value,list):
        return [normalize(x) for x in value]
    if isinstance(value,dict):
        out={}
        for k,v in value.items():
            if not isinstance(k,str):
                raise TypeError("canonicalJSON object keys must be strings")
            nk=unicodedata.normalize("NFC",k)
            if nk in out:
                raise ValueError("canonicalJSON NFC key collision")
            out[nk]=normalize(v)
        return out
    raise TypeError(f"unsupported canonicalJSON type: {type(value).__name__}")

def canonical_json(value:Any)->str:
    return json.dumps(normalize(value),ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False)

def canonical_bytes(value:Any)->bytes:
    return canonical_json(value).encode("utf-8")

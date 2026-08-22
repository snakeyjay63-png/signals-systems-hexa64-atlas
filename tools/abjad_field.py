#!/usr/bin/env python3
from pathlib import Path
import json, unicodedata

ROOT=Path(__file__).resolve().parent.parent
SPEC=ROOT/'data'/'abjad_field.json'


def load_spec():
    return json.loads(SPEC.read_text(encoding='utf-8'))


def table():
    return {x['char']:int(x['value']) for x in load_spec()['letters']}


def normalize(text:str)->str:
    spec=load_spec(); cmap=spec['normalization']['canonicalizations']; t=table()
    out=[]
    for ch in unicodedata.normalize(spec['normalization'].get('unicode_form','NFC'), text):
        if ch=='ـ':
            continue
        if unicodedata.combining(ch):
            continue
        ch=cmap.get(ch,ch)
        if ch in t:
            out.append(ch)
    return ''.join(out)


def encode(text:str):
    t=table(); return [t[ch] for ch in normalize(text)]


def abjad_sum(text:str)->int:
    return sum(encode(text))


def dr(v:int)->int:
    v=int(v)
    if v<=0:
        raise ValueError('digital root is defined here for positive integers')
    return 1+((v-1)%9)


def orbit_class(root:int)->str:
    root=dr(root)
    if root in {1,2,4,8,7,5}: return 'V1'
    if root in {3,6}: return 'V3'
    return 'V9'


def doubling_cycle(start:int):
    seen=[]; x=dr(start)
    while x not in seen:
        seen.append(x); x=dr(2*x)
    return seen


def validate():
    s=load_spec(); chars=[x['char'] for x in s['letters']]; vals=[x['value'] for x in s['letters']]
    assert len(chars)==28 and len(set(chars))==28 and len(set(vals))==28
    assert vals==[1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100,200,300,400,500,600,700,800,900,1000]
    assert doubling_cycle(1)==[1,2,4,8,7,5]
    assert doubling_cycle(3)==[3,6]
    assert doubling_cycle(9)==[9]
    # Orthographic aliases collapse into the same 28-letter carrier.
    assert normalize('أإآٱا')=='ااااا'
    assert normalize('ؤو')=='وو'
    assert normalize('ئیىي')=='يييي'
    assert normalize('ةه')=='هه'
    return True

if __name__=='__main__':
    validate(); print('ABJAD FIELD PASS · 28 direct letters · normalization explicit · V1/V3/V9 exact')

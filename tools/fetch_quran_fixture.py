#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import argparse, hashlib, json, urllib.request

ROOT=Path(__file__).resolve().parent.parent
DIR=ROOT/'corpora'/'quran_uthmani'
SOURCE=DIR/'source.json'
FIXTURE=DIR/'quran.jsonl'
LOCK=DIR/'fixture.lock.json'


def sha256_bytes(b:bytes)->str:
    return hashlib.sha256(b).hexdigest()


def validate_jsonl(raw:bytes, expected:int=6236):
    text=raw.decode('utf-8')
    lines=text.splitlines()
    if len(lines)!=expected:
        raise ValueError(f'expected {expected} JSONL ayahs, got {len(lines)}')
    keys=[]
    for i,line in enumerate(lines,1):
        obj=json.loads(line)
        if not isinstance(obj,dict) or not isinstance(obj.get('text'),str) or not obj['text']:
            raise ValueError(f'line {i}: missing non-empty text field')
        keys.append(obj.get('verse_key') or obj.get('global_number') or i)
    return lines,keys


def fetch(url:str, timeout:int=90):
    req=urllib.request.Request(url,headers={'User-Agent':'signals-systems-hexa64-atlas/1.0'})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        return r.read()


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--url',help='override source URL')
    ap.add_argument('--force',action='store_true')
    args=ap.parse_args()
    src=json.loads(SOURCE.read_text(encoding='utf-8'))
    url=args.url or src['source_url']
    if FIXTURE.exists() and not args.force:
        raw=FIXTURE.read_bytes()
    else:
        raw=fetch(url)
        FIXTURE.write_bytes(raw)
    lines,_=validate_jsonl(raw,int(src['expected_ayahs']))
    lock={
      'source_url':url,
      'sha256':sha256_bytes(raw),
      'bytes':len(raw),
      'ayah_lines':len(lines),
      'fixture_file':str(FIXTURE.relative_to(ROOT)),
      'content_pin':'sha256 of exact downloaded bytes; commit fixture + lock for offline reproducibility'
    }
    LOCK.write_text(json.dumps(lock,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f"FIXTURE PASS · {len(lines)} ayahs · sha256={lock['sha256']}")

if __name__=='__main__':
    main()

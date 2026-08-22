#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
from fractions import Fraction
import argparse, hashlib, json
from collections import Counter
from abjad_field import normalize, encode, dr, orbit_class

ROOT=Path(__file__).resolve().parent.parent
DIR=ROOT/'corpora'/'quran_uthmani'
FIXTURE=DIR/'quran.jsonl'
LOCK=DIR/'fixture.lock.json'
HYP=ROOT/'data'/'quran_abjad_hypothesis.json'
OUT=ROOT/'data'/'quran_abjad_measurement.json'


def sha256_file(p:Path)->str:
    h=hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda:f.read(1<<20),b''): h.update(chunk)
    return h.hexdigest()


def read_fixture():
    rows=[]
    for i,line in enumerate(FIXTURE.read_text(encoding='utf-8').splitlines(),1):
        obj=json.loads(line)
        rows.append((obj.get('verse_key') or str(i),obj['text']))
    return rows


def measure(rows):
    roots=Counter(); orbits=Counter(); transition=Counter(); detail=[]; prev=None
    total_letters=0
    for key,text in rows:
        norm=normalize(text); vals=encode(text); total_letters+=len(vals)
        if not vals:
            raise ValueError(f'ayah {key} normalizes to zero abjad letters')
        s=sum(vals); root=dr(s); orbit=orbit_class(root)
        roots[root]+=1; orbits[orbit]+=1
        if prev is not None: transition[(prev,root)]+=1
        prev=root
        detail.append({'verse_key':key,'letters':len(vals),'abjad_sum':s,'digital_root':root,'orbit':orbit})
    n=len(rows)
    orbit_counts={k:orbits[k] for k in ['V1','V3','V9']}
    orbit_stats={}
    for k,count in orbit_counts.items():
        gap=Fraction(1,3)-Fraction(count,n)
        orbit_stats[k]={'count':count,'total':n,'fraction':f'{count}/{n}',
                        'equal_class_baseline':'1/3',
                        'gap_fraction':f'{gap.numerator}/{gap.denominator}',
                        'gap_float':float(gap)}
    return {
      'ayahs':n,'normalized_abjad_letters':total_letters,
      'digital_root_counts':{str(k):roots[k] for k in range(1,10)},
      'orbit_counts':orbit_counts,
      'orbit_statistics':orbit_stats,
      'root_transition_counts':{f'{a}->{b}':c for (a,b),c in sorted(transition.items())},
      'ayah_measurements':detail
    }


def missing_result(hyp):
    c=hyp['measurement']['candidate_count']; n=hyp['measurement']['candidate_total']
    gap=Fraction(1,3)-Fraction(c,n)
    return {
      'status':'fixture_missing',
      'fixture':str(FIXTURE.relative_to(ROOT)),
      'candidate_only':{'count':c,'total':n,'gap_fraction':f'{gap.numerator}/{gap.denominator}'},
      'claim':'candidate is not marked reproduced until the exact fixture is present and measured'
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--allow-missing',action='store_true')
    ap.add_argument('--require-candidate',action='store_true',help='fail unless exactly one measured V1/V3/V9 class has count 2050 of 6236 and gap 43/9354')
    ap.add_argument('--no-detail',action='store_true',help='omit per-ayah rows from output')
    args=ap.parse_args()
    hyp=json.loads(HYP.read_text(encoding='utf-8'))
    if not FIXTURE.exists():
        result=missing_result(hyp); OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print('CORPUS FIXTURE MISSING · empirical result not reproduced')
        if args.allow_missing: return
        raise SystemExit(2)
    rows=read_fixture()
    if len(rows)!=6236: raise SystemExit(f'expected 6236 ayahs, got {len(rows)}')
    if LOCK.exists():
        lock=json.loads(LOCK.read_text(encoding='utf-8'))
        actual=sha256_file(FIXTURE)
        if actual!=lock.get('sha256'): raise SystemExit('fixture SHA-256 differs from lock')
    result=measure(rows)
    result['status']='measured'
    result['fixture_sha256']=sha256_file(FIXTURE)
    if args.no_detail: result.pop('ayah_measurements',None)
    OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    matches=[k for k,v in result['orbit_counts'].items() if v==2050]
    result['candidate_2050_matches']=matches
    # rewrite after adding match resolution
    OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f"CORPUS MEASURED · ayahs={result['ayahs']} · orbit_counts={result['orbit_counts']} · candidate_matches={matches}")
    if args.require_candidate:
        if result['ayahs']!=6236 or len(matches)!=1:
            raise SystemExit('candidate empirical result NOT reproduced: expected exactly one V1/V3/V9 count equal to 2050 of 6236')
        stat=result['orbit_statistics'][matches[0]]
        if stat['gap_fraction']!='43/9354':
            raise SystemExit(f"candidate count matched but exact gap differs: {stat['gap_fraction']}")
        print(f"CANDIDATE REPRODUCED · class={matches[0]} · 2050/6236 · gap 43/9354")

if __name__=='__main__':
    main()

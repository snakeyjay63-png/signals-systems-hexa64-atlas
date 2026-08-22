#!/usr/bin/env python3
from pathlib import Path
import hashlib, json, base64, math, unicodedata
from fractions import Fraction
import xml.etree.ElementTree as ET
import numpy as np
import jsonschema
import cairosvg
import hashlib as hashlib_std
from utf73_field import load_spec as load_utf73_spec, symbols as utf73_symbols, exhaustive_rgb24_basins
from abjad_field import load_spec as load_abjad_spec, validate as validate_abjad, dr as abjad_dr, doubling_cycle
from analyze_quran_abjad import read_fixture as read_quran_fixture, measure as measure_quran_abjad, sha256_file as sha256_quran_fixture
from language_frame_closure import derive as derive_language_closure
from carrier_invariance import derive as derive_carrier_invariance, canonical_sha256 as carrier_canonical_sha256
from self_read_roundtrip import derive as derive_self_read
from independent_property_reader import derive as derive_independent_reader
from independent_reader_fault_injection import derive as derive_fault_injection
from reader_independence_gate import derive as derive_ri_gate
from reader_independence import derive as derive_ri_real
from full_semantic_delta import derive as derive_full_semantic_delta
from full_semantic_self_read import derive as derive_full_semantic_self_read
from full_semantic_fault_injection import derive as derive_full_semantic_faults

from canonical_json import canonical_bytes, canonical_json

ROOT=Path(__file__).resolve().parent.parent
SVG=ROOT/'assets'/'signals_systems_full_atlas_master.svg'
ATLAS=ROOT/'data'/'atlas.json'
NDJSON=ROOT/'data'/'concepts.ndjson'
SCHEMA=ROOT/'data'/'schema.json'
ENCODING=ROOT/'data'/'encoding_geometry.json'
CH14_SOURCE=ROOT/'assets'/'ch14_test_object.svg'
CH14_PNG=ROOT/'assets'/'ch14_test_object.png'
CH14_B64=ROOT/'data'/'ch14_test_object.b64.txt'
UTF73=ROOT/'data'/'sanskrit_utf73.json'
UTF73_SPEC=ROOT/'data'/'utf73_field.json'
UTF73_BASINS=ROOT/'data'/'utf73_rgb24_basins.json'
UTF73_HTML=ROOT/'validators'/'sanskrit_utf73.html'
QHYP=ROOT/'data'/'quran_abjad_hypothesis.json'
QMEAS=ROOT/'data'/'quran_abjad_measurement.json'
QSOURCE=ROOT/'corpora'/'quran_uthmani'/'source.json'
QFIXTURE=ROOT/'corpora'/'quran_uthmani'/'quran.jsonl'
QLOCK=ROOT/'corpora'/'quran_uthmani'/'fixture.lock.json'

CLOSURE7=ROOT/'data'/'language_closure_7.json'

FRAME_AXIOMS=ROOT/'data'/'language_frame_axioms.json'

TF18=ROOT/'data'/'transformer_frame_ch18.json'

CG19=ROOT/'data'/'choice_geometry_ch19.json'
CI20=ROOT/'data'/'carrier_invariance_ch20.json'
CM20=ROOT/'data'/'carrier_invariance_measurement.json'
SR20=ROOT/'data'/'self_read_roundtrip_ch20.json'
QF20=ROOT/'data'/'quotient_factorization_ch20.json'
RIG20=ROOT/'data'/'reader_independence_gate_ch20.json'
IR20=ROOT/'data'/'independent_reader_measurement_ch20.json'
FI20=ROOT/'data'/'independent_reader_fault_injection_ch20.json'
RIGM20=ROOT/'data'/'reader_independence_gate_measurement_ch20.json'
RCC20=ROOT/'data'/'reader_independence_real_carriers_ch20.json'
FSD20=ROOT/'data'/'full_semantic_self_read_delta_ch20.json'
FSDM20=ROOT/'data'/'full_semantic_self_read_delta_measurement_ch20.json'
FSM20=ROOT/'data'/'full_semantic_self_read_measurement_ch20.json'
FSF20=ROOT/'data'/'full_semantic_fault_injection_ch20.json'
CJS20=ROOT/'data'/'canonical_json_spec_ch20.json'

def sha(b): return hashlib.sha256(b).hexdigest()
def mh(r):
    p={'concept_id':r['concept_id'],'equation':r['equation'],'parameters':r['parameters'],'validation':r['validation']}
    return sha(canonical_bytes(p))

errors=[]
root=ET.parse(SVG).getroot()
groups=[g for g in root.iter() if g.attrib.get('data-concept')]
ids=[g.attrib['data-concept'] for g in groups]
atlas=json.loads(ATLAS.read_text(encoding='utf-8'))
records=atlas['concepts']
nd=[json.loads(x) for x in NDJSON.read_text(encoding='utf-8').splitlines() if x.strip()]
schema=json.loads(SCHEMA.read_text(encoding='utf-8'))

expected=103
if len(groups)!=expected: errors.append(f'expected {expected} SVG concepts, got {len(groups)}')
if len(set(ids))!=expected: errors.append('SVG concept ids are not unique')
if len(records)!=expected or len(nd)!=expected: errors.append(f'dataset does not contain exactly {expected} records')
if atlas.get('chapter_count')!=20: errors.append('atlas chapter_count must be 20')
if [r['concept_id'] for r in records]!=ids: errors.append('atlas.json concept order differs from SVG')
if [r['concept_id'] for r in nd]!=ids: errors.append('concepts.ndjson concept order differs from SVG')

for r in records:
    try:
        jsonschema.validate(instance=r,schema=schema)
    except jsonschema.ValidationError as e:
        errors.append(f"{r.get('concept_id','?')}: JSON Schema: {e.message}")

by={r['concept_id']:r for r in records}
for g in groups:
    r=by[g.attrib['data-concept']]
    if r['svg_fragment_sha256']!=sha(ET.tostring(g,encoding='utf-8')): errors.append(r['concept_id']+': SVG hash mismatch')
    if r['math_signature_sha256']!=mh(r): errors.append(r['concept_id']+': math hash mismatch')

# Core executable invariants
N=64;n=np.arange(N);x=np.sin(2*np.pi*5*n/N)
support=np.where(np.abs(np.fft.fft(x))>1e-9)[0].tolist()
if support!=[5,59]: errors.append(f'dt_sinusoid support {support}')

N2=16;n2=np.arange(N2)
x2=np.cos(2*np.pi*3*n2/N2)+.5*np.cos(2*np.pi*5*n2/N2)
support2=np.where(np.abs(np.fft.fft(x2)/N2)>1e-9)[0].tolist()
if support2!=[3,5,11,13]: errors.append(f'dtfs support {support2}')

rect=np.r_[np.zeros(10),np.ones(12),np.zeros(42)]
h=np.exp(-np.arange(64)/10.0); y=np.convolve(rect,h)[:64]
if not np.all(np.isfinite(y)): errors.append('convolution invariant failed')

if by['nyquist']['parameters'].get('condition')!='fs > 2B': errors.append('Nyquist condition mismatch')

r=float(by['z_to_dtft']['parameters']['pole_radius'])
w=np.linspace(0,2*np.pi,1024,endpoint=False)
H=1/(1-r*np.exp(-1j*w))
if not np.all(np.isfinite(H)): errors.append('z_to_dtft invariant failed')

# Chapter 12 invariants
mask=(1<<32)-1; word=0x6A09E667; rot=7
rotr=((word>>rot)|((word<<(32-rot))&mask))&mask
if rotr.bit_count()!=word.bit_count(): errors.append('ROTR did not preserve Hamming weight')
if ((0xF0000011+0x30000022)&mask)!=0x20000033: errors.append('modular addition invariant failed')

m0=bytes(64); m1=bytes([1])+bytes(63)
d0=hashlib_std.sha256(m0).digest(); d1=hashlib_std.sha256(m1).digest()
hd=sum((a^b).bit_count() for a,b in zip(d0,d1))
if hd!=133: errors.append(f'avalanche Hamming distance expected 133, got {hd}')
if by['avalanche_diffusion']['parameters'].get('measured_hamming_distance')!=hd:
    errors.append('dataset avalanche Hamming distance does not match recomputation')

# Chapter 13 address-geometry invariants
import ipaddress
v4=ipaddress.IPv4Address('192.0.2.33')
v6=ipaddress.IPv6Address('::ffff:192.0.2.33')
if int(v4)!=0xC0000221:
    errors.append('IPv4 numeric value mismatch')
if (int(v6)&0xffffffff)!=int(v4):
    errors.append('IPv4-mapped IPv6 low 32 bits do not preserve IPv4 value')
if v6.ipv4_mapped != v4:
    errors.append('IPv4-mapped IPv6 semantic mapping failed')
if by['ipv6_lanes']['parameters'].get('bits') != 128 or by['ipv6_lanes']['parameters'].get('lanes_32') != 4:
    errors.append('IPv6 4×32 lane invariant failed')
if by['ipv4_mapped_ipv6']['parameters'].get('prefix_bits') != 96:
    errors.append('IPv4-mapped prefix length invariant failed')

# Chapter 14 encoding-geometry invariants
enc=json.loads(ENCODING.read_text(encoding='utf-8'))
source=CH14_SOURCE.read_bytes()
raw1=cairosvg.svg2png(bytestring=source,output_width=160,output_height=96)
raw2=cairosvg.svg2png(bytestring=source,output_width=160,output_height=96)
if raw1 != raw2:
    errors.append('CairoSVG rasterization is not deterministic across repeated runs')
if raw1 != CH14_PNG.read_bytes():
    errors.append('committed Chapter 14 PNG differs from fresh rasterization')
b64=base64.b64encode(raw1)
if base64.b64decode(b64) != raw1:
    errors.append('Base64 roundtrip is not byte-exact')
if len(b64) != math.ceil(len(raw1)/3)*4:
    errors.append('Base64 padding/length invariant failed')
alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
if len(alphabet)!=64 or len(set(alphabet))!=64:
    errors.append('Base64 alphabet is not a 64-symbol bijection')
indices=[alphabet.index(chr(c)) for c in b64 if chr(c)!="="]
if any(i<0 or i>63 for i in indices):
    errors.append('Base64 index outside 0..63')
# First 24 bits: 3 bytes and 4 six-bit indices reconstruct exactly.
raw3=raw1[:3]
first4=b64[:4].decode('ascii')
idx4=[alphabet.index(c) for c in first4]
bits_bytes=''.join(f'{b:08b}' for b in raw3)
bits_b64=''.join(f'{i:06b}' for i in idx4)
if bits_bytes != bits_b64:
    errors.append('24-bit 8+8+8 → 6+6+6+6 repartition invariant failed')
b64_hash=hashlib.sha256(b64).hexdigest()
if hashlib.sha256(base64.b64encode(raw2)).hexdigest()!=b64_hash:
    errors.append('Base64 hash differs across repeated identical renders')
if enc.get('png_length_bytes') != len(raw1):
    errors.append('encoding_geometry PNG length mismatch')
if enc.get('png_sha256') != hashlib.sha256(raw1).hexdigest():
    errors.append('encoding_geometry PNG SHA mismatch')
if enc.get('base64_length_chars') != len(b64):
    errors.append('encoding_geometry Base64 length mismatch')
if enc.get('base64_sha256') != b64_hash:
    errors.append('encoding_geometry Base64 SHA mismatch')
if enc.get('first_16_base64_chars') != b64[:16].decode('ascii'):
    errors.append('encoding_geometry first chars mismatch')
if CH14_B64.read_bytes().strip() != b64:
    errors.append('committed Base64 text differs from recomputation')

# Chapter 15 canonical field + live RGB24 basin invariants
utf73=json.loads(UTF73.read_text(encoding='utf-8'))
spec=load_utf73_spec()
states=utf73['states']
canonical_symbols=utf73_symbols()
if len(states)!=73 or len({s['symbol'] for s in states})!=73:
    errors.append('UTF73 field does not contain 73 unique symbol strings')
if [s['symbol'] for s in states] != canonical_symbols:
    errors.append('UTF73 dataset alphabet differs from canonical utf73_field.json')

# Exact chosen code points: anusvāra is slot 12; virāma is not part of canonical Σ73.
expected_cons={'क':0x0915,'च':0x091A,'ट':0x091F,'त':0x0924,'प':0x092A,'स':0x0938}
expected_marks={'ा':0x093E,'ि':0x093F,'ी':0x0940,'ु':0x0941,'ू':0x0942,'ृ':0x0943,'े':0x0947,'ै':0x0948,'ो':0x094B,'ौ':0x094C,'ं':0x0902}
for ch,cp in {**expected_cons,**expected_marks,'·':0x00B7}.items():
    if ord(ch)!=cp:
        errors.append(f'UTF73 codepoint mismatch for {ch}')
if unicodedata.name('ं')!='DEVANAGARI SIGN ANUSVARA':
    errors.append('U+0902 Unicode name mismatch')
if any('्' in s for s in canonical_symbols):
    errors.append('canonical UTF73 unexpectedly contains VIRAMA U+094D')
if unicodedata.name('·')!='MIDDLE DOT':
    errors.append('U+00B7 Unicode name mismatch')

# UTF-8 roundtrip and exact recorded bytes.
widths=set()
for s in states:
    raw=s['symbol'].encode('utf-8')
    if raw.decode('utf-8')!=s['symbol']:
        errors.append(f"UTF-8 roundtrip failed for state {s['index']}")
    if [f'U+{ord(ch):04X}' for ch in s['symbol']] != s['codepoints']:
        errors.append(f"codepoint list mismatch for state {s['index']}")
    if raw.hex(' ') != s['utf8_hex'] or len(raw)!=s['utf8_length']:
        errors.append(f"UTF-8 byte record mismatch for state {s['index']}")
    widths.add(len(raw))
if widths != {2,3,6}:
    errors.append(f'UTF73 expected UTF-8 widths {{2,3,6}}, got {widths}')

# Reference quotient identity: deliberately labeled construction identity.
def E73(n): return n % 73
def D73(i): return i
fixed=[E73(D73(i))==i for i in range(73)]
if not all(fixed):
    errors.append(f'UTF73 reference identity failed: {sum(fixed)}/73')
q,r=divmod(2**24,73)
if (q,r)!=(229824,64):
    errors.append(f'UTF73 reference quotient mismatch: q={q}, r={r}')

# Real live encoder: exhaustively recompute all 2^24 RGB inputs.
real=exhaustive_rgb24_basins()
recorded_basin=json.loads(UTF73_BASINS.read_text(encoding='utf-8'))
recorded_counts=np.array([x['rgb24_basin_size'] for x in recorded_basin['states']],dtype=np.int64)
if not np.array_equal(real,recorded_counts):
    errors.append('committed live RGB24 basin counts differ from exhaustive recomputation')
if int(real.sum()) != 2**24:
    errors.append('live RGB24 basin sum does not equal 2^24')
if int(real[72]) != 1:
    errors.append('śūnya live basin must contain black only')
if utf73['measured_rgb24_basins']['min'] != int(real.min()) or utf73['measured_rgb24_basins']['max'] != int(real.max()):
    errors.append('UTF73 dataset real basin min/max differs from recomputation')
if [s['rgb24_basin_size'] for s in states] != real.tolist():
    errors.append('UTF73 per-state live basin counts differ from recomputation')

# Browser validator is self-contained and uses native Unicode APIs.
html=UTF73_HTML.read_text(encoding='utf-8')
if '<script>' not in html or 'TextEncoder' not in html or 'TextDecoder' not in html:
    errors.append('UTF73 browser validator is missing native Unicode proof primitives')
for forbidden in ['<script src=','http://','https://']:
    if forbidden in html:
        errors.append(f'UTF73 browser validator is not self-contained: found {forbidden}')

# Chapter 16: three-layer abjad/corpus model
abjad=load_abjad_spec()
letters=abjad['letters']
if len(letters)!=28 or len({x['char'] for x in letters})!=28 or len({x['value'] for x in letters})!=28:
    errors.append('abjad field must contain 28 unique letters and values')
if [x['value'] for x in letters] != [1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100,200,300,400,500,600,700,800,900,1000]:
    errors.append('classical abjad value ladder mismatch')
if not validate_abjad():
    errors.append('abjad field validator failed')
if doubling_cycle(1)!=[1,2,4,8,7,5] or doubling_cycle(3)!=[3,6] or doubling_cycle(9)!=[9]:
    errors.append('abjad V1/V3/V9 orbit mismatch')
if 'charCode' not in abjad.get('mapping_semantics',''):
    errors.append('abjad spec must explicitly exclude codepoint-modulo mapping')
if abjad['corpus_claims']['status']!='candidate pending exact fixture reproduction':
    errors.append('abjad corpus status must remain candidate until fixture reproduces it')

# Candidate empirical arithmetic is exact independently of the corpus.
hyp=json.loads(QHYP.read_text(encoding='utf-8'))
m=hyp['measurement']
if (m['candidate_count'],m['candidate_total'])!=(2050,6236):
    errors.append('candidate Quran count/total differs from 2050/6236')
gap=Fraction(1,3)-Fraction(m['candidate_count'],m['candidate_total'])
if gap!=Fraction(43,9354):
    errors.append(f'candidate exact fraction mismatch: got {gap}')
if 'orbit-class frequency' not in m.get('tested_statistic',''):
    errors.append('candidate statistic definition drifted')
if not str(m.get('target_orbit_class','')).startswith('unresolved'):
    errors.append('target orbit class must remain unresolved until prior script/fixture identifies it')

# Fixture provenance is explicit even when bytes are not bundled.
source=json.loads(QSOURCE.read_text(encoding='utf-8'))
if source.get('expected_ayahs')!=6236:
    errors.append('Quran source manifest must require 6236 ayahs')
if 'quran.jsonl' not in source.get('source_url',''):
    errors.append('Quran source manifest URL does not identify quran.jsonl')

qmeas=json.loads(QMEAS.read_text(encoding='utf-8'))
if QFIXTURE.exists():
    rows=read_quran_fixture()
    if len(rows)!=6236:
        errors.append(f'Quran fixture expected 6236 ayahs, got {len(rows)}')
    measured=measure_quran_abjad(rows)
    if QLOCK.exists():
        lock=json.loads(QLOCK.read_text(encoding='utf-8'))
        if lock.get('sha256')!=sha256_quran_fixture(QFIXTURE):
            errors.append('Quran fixture SHA differs from fixture.lock.json')
    matches=[k for k,v in measured['orbit_counts'].items() if v==2050]
    # When a real fixture is present, the committed measurement must match the fresh orbit counts/statistics.
    if qmeas.get('status')!='measured':
        errors.append('Quran fixture exists but committed measurement is not marked measured')
    else:
        if qmeas.get('orbit_counts')!=measured['orbit_counts']:
            errors.append('committed Quran orbit counts differ from fresh recomputation')
        if qmeas.get('orbit_statistics')!=measured['orbit_statistics']:
            errors.append('committed Quran orbit statistics differ from fresh recomputation')
        if qmeas.get('candidate_2050_matches',[])!=matches:
            errors.append('committed candidate-match resolution differs from fresh recomputation')
    if len(matches)==1:
        stat=measured['orbit_statistics'][matches[0]]
        quran_status=f"MEASURED candidate class={matches[0]} {stat['count']}/{stat['total']} gap={stat['gap_fraction']}"
    else:
        quran_status=f"MEASURED orbit_counts={measured['orbit_counts']} candidate_matches={matches}"
else:
    if qmeas.get('status')!='fixture_missing':
        errors.append('Quran fixture absent but measurement status is not fixture_missing')
    cand=qmeas.get('candidate_only',{})
    if (cand.get('count'),cand.get('total'),cand.get('gap_fraction'))!=(2050,6236,'43/9354'):
        errors.append('fixture-missing placeholder does not preserve candidate arithmetic')
    quran_status='FIXTURE MISSING · candidate arithmetic only'

# Chapter 17 executable quotient-closure theorem
c7=json.loads(CLOSURE7.read_text(encoding='utf-8'))
ax17=json.loads(FRAME_AXIOMS.read_text(encoding='utf-8'))
fresh_c7=derive_language_closure()
if fresh_c7 != c7:
    errors.append('Chapter 17 committed quotient theorem data differs from fresh construction')

if ax17['atomic_frame']['cardinality']!=3:
    errors.append('AtomicFrame cardinality must be 3 = C+S+b')
if c7['prequotient']['cardinality']!=9 or len(c7['prequotient']['points'])!=9:
    errors.append('Chapter 17 prequotient must contain exactly 9 points')
if len(set(c7['prequotient']['points']))!=9:
    errors.append('Chapter 17 prequotient inputs are not pairwise disjoint')
if c7['equivalence_relation']['boundary_identification']!='L:b ~ G:b ~ E:b':
    errors.append('Chapter 17 boundary equivalence relation drifted')
if c7['equivalence_relation']['classes_removed_by_identification']!=2:
    errors.append('Chapter 17 quotient must remove exactly 2 classes relative to 9 distinct points')
if c7['quotient']['cardinality']!=7 or len(c7['quotient']['points'])!=7:
    errors.append('Chapter 17 quotient cardinality must be exactly 7')
if len(c7['quotient']['C_prime'])!=3 or len(c7['quotient']['S_prime'])!=3:
    errors.append('Chapter 17 quotient must canonically inherit 3 carrier and 3 structure points')
if set(c7['quotient']['C_prime']) & set(c7['quotient']['S_prime']):
    errors.append('Chapter 17 quotient carrier/structure images are not disjoint')
if c7['quotient']['boundary'] in set(c7['quotient']['C_prime'])|set(c7['quotient']['S_prime']):
    errors.append('Chapter 17 quotient boundary is not external to C′∪S′')
if c7['quotient']['boundary_class']!=['E:b','G:b','L:b']:
    errors.append('Chapter 17 boundary class does not contain exactly the three input boundaries')
checks=c7['closure_theorem']['axiom_checks']
if checks != {'A1_nonempty':True,'A2_disjoint':True,'A3_boundary_external':True,'A4_unique_boundary_class':True}:
    errors.append(f'Chapter 17 closure theorem A1–A4 failed: {checks}')
if not c7['closure_theorem']['passes'] or not c7['closure_theorem']['canonical_partition']:
    errors.append('Chapter 17 theorem must pass with canonical inherited partition')
if 'not derived here' not in c7['atomicity_status']:
    errors.append('Chapter 17 must keep atomicity explicitly axiomatic')
if 'not AtomicFrame' not in c7['recursive_typing']['not_claimed']:
    errors.append('Chapter 17 must not claim quotient output is atomic')
if c7['mod9']['digital_root_7']!=7 or c7['mod9']['T7']!=5 or c7['mod9']['V1']!=[1,2,4,8,7,5]:
    errors.append('Chapter 17 mod-9 crosscheck failed')
zay=abjad['letters'][6]
if (zay['char'],zay['value'])!=('ز',7):
    errors.append('Chapter 17 abjad zay/value crosscheck failed')
if 'meta-observation only' not in c7['meta_observation']['visual_field_count_89']:
    errors.append('Chapter 17 Fibonacci-89 note must remain meta-observation only')

# Chapter 18 audited slice-model invariants
tf18=json.loads(TF18.read_text(encoding='utf-8'))
if tf18.get('status')!='AUDITED SLICE MODEL':
    errors.append('Chapter 18 status must be AUDITED SLICE MODEL')
fc=tf18.get('frame_correspondence',[])
if len(fc)!=3:
    errors.append('Chapter 18 must contain exactly C/S/b correspondences')
if fc[0].get('scope')!='per-layer' or fc[1].get('scope')!='per-layer':
    errors.append('Chapter 18 C/S mapping must be explicitly per-layer')
if fc[0].get('audit_status')!='VALID' or fc[1].get('audit_status')!='VALID':
    errors.append('Chapter 18 C/S mapping audit status mismatch')
b=fc[2]
if b.get('selected_candidate')!='b1' or 'next layer' not in b.get('rejected_candidate',''):
    errors.append('Chapter 18 boundary candidate disambiguation failed')
if b.get('audit_status')!='VALID WITH DISAMBIGUATION':
    errors.append('Chapter 18 boundary audit status mismatch')
if tf18.get('axiom_audit',{}).get('scope')!='local/per-layer, not whole-network':
    errors.append('Chapter 18 A2 scope must be local/per-layer')
sg=tf18['seed_geometry']
if (sg.get('center'),sg.get('first_ring'),sg.get('total'),sg.get('coordination_number'))!=(1,6,7,6):
    errors.append('Chapter 18 6+1 seed geometry mismatch')
if not str(sg.get('audit_status','')).startswith('EXACT'):
    errors.append('Chapter 18 seed geometry must be exact under stated definition')
if tf18['orbit_rotation_bridge'].get('audit_status')!='ANALOGY CANDIDATE':
    errors.append('Chapter 18 orbit/rotation bridge must remain analogy candidate')
if tf18['self_reference'].get('status')!='PROVENANCE OBSERVATION':
    errors.append('Chapter 18 self-reference must remain provenance observation')
if tf18['ledger'].get('current_status')!='AUDITED SLICE MODEL':
    errors.append('Chapter 18 ledger status mismatch')

# Chapter 19 choice geometry / reflective closure invariants
cg19=json.loads(CG19.read_text(encoding='utf-8'))
if cg19.get('status')!='formal project-level choice registry':
    errors.append('Chapter 19 status mismatch')
if cg19.get('operator',{}).get('equation')!='F_θ : X → Y, θ ∈ Θ':
    errors.append('Chapter 19 choice operator equation drifted')
gchain=cg19.get('geometric_chain',[])
if len(gchain)!=4:
    errors.append('Chapter 19 geometric chain must contain 4 explicit steps')
if not any(x.get('operator')=='B' and x.get('invertibility','').startswith('bijective') for x in gchain):
    errors.append('Chapter 19 must record Base64 byte bijection')
if not any(x.get('operator')=='R' and x.get('invertibility')=='generally lossy' for x in gchain):
    errors.append('Chapter 19 must record rasterization lossiness')
schain=cg19.get('symbolic_chain',[])
if len(schain)!=5:
    errors.append('Chapter 19 symbolic chain must contain 5 explicit transitions')
registry=cg19.get('choice_registry',[])
ids=[x.get('id') for x in registry]
expected_ids=['theta_raster','theta_utf73','theta_bridge','theta_abjad','theta_atomic','theta_transformer']
if ids!=expected_ids:
    errors.append(f'Chapter 19 choice registry drifted: {ids}')
bridge=next((x for x in registry if x.get('id')=='theta_bridge'),None)
if not bridge or bridge.get('status')!='ROUTED_OPEN' or bridge.get('locked_by') is not None:
    errors.append('Chapter 19 theta_bridge must be explicitly ROUTED_OPEN and unlocked')
if bridge.get('lock_policy')!='NONE_BY_DESIGN':
    errors.append('Chapter 19 theta_bridge lock policy must be NONE_BY_DESIGN')
if bridge.get('endpoint')!='0.0.0.0' or bridge.get('endpoint_network_status')!='IPv4 unspecified address':
    errors.append('Chapter 19 theta_bridge endpoint/network semantics drifted')
if bridge.get('default_route_prefix')!='0.0.0.0/0':
    errors.append('Chapter 19 default route prefix must remain distinct from the endpoint')
if '0°N, 0°E' not in bridge.get('null_island_note',''):
    errors.append('Chapter 19 Null Island distinction missing')
account=cg19.get('choice_accounting',{})
if account.get('used_choice_ids')!=expected_ids:
    errors.append('Chapter 19 Θ_used does not match registry/chain choices')
if account.get('locked_choice_ids')!=['theta_raster','theta_utf73','theta_abjad','theta_atomic','theta_transformer']:
    errors.append('Chapter 19 Θ_locked drifted')
if account.get('pending_choice_ids')!=[]:
    errors.append('Chapter 19 must have no pending choices')
if account.get('routed_open_choice_ids')!=['theta_bridge']:
    errors.append('Chapter 19 routed-open choice set must be exactly {theta_bridge}')
if account.get('unlocked_by_design_choice_ids')!=['theta_bridge']:
    errors.append('Chapter 19 unlocked-by-design set must be exactly {theta_bridge}')
if account.get('closure_semantics')!='OPEN_BY_DESIGN':
    errors.append('Chapter 19 closure semantics must be OPEN_BY_DESIGN')
if account.get('invariant')!='Θ_used \\ Θ_locked = {θ_bridge}':
    errors.append('Chapter 19 used-minus-locked invariant drifted')
if account.get('closure_complete') is not False:
    errors.append('Chapter 19 closure_complete must remain false for the routed-open bridge')
if cg19.get('closure',{}).get('pending_gap') is not None:
    errors.append('Chapter 19 must keep theta_bridge pending_gap=null')
if cg19.get('closure',{}).get('open_port')!='theta_bridge':
    errors.append('Chapter 19 closure must explicitly name theta_bridge as open port')
reflection=cg19.get('reflection',{})
if reflection.get('equation')!='θ → F_θ → F_θ(X) → encode(θ,F_θ,results)':
    errors.append('Chapter 19 reflection equation drifted')
if reflection.get('status')!='exact project provenance property when the generator reads the same committed choice records it emits/validates':
    errors.append('Chapter 19 reflection status mismatch')
if 'not a claim that θ causes itself' not in reflection.get('self_reference_boundary',''):
    errors.append('Chapter 19 must bound reflection away from self-causation')
if cg19.get('closure',{}).get('pipeline')!='carrier → encoding → geometry → finite field → language → dynamics → quotient frame → transformer slice → choice operator → reflection':
    errors.append('Chapter 19 closure pipeline drifted')

# Chapter 20 carrier-invariance / read-route invariants
ci20=json.loads(CI20.read_text(encoding='utf-8'))
cm20=json.loads(CM20.read_text(encoding='utf-8'))
derived20=derive_carrier_invariance()
if ci20.get('status')!='self-consistent serialized atlas; reader-independence proven with real carriers':
    errors.append('Chapter 20 status mismatch')
formal=ci20.get('formalization',{})
if formal.get('carrier_route')!='(M,τ) → adapter → R → D':
    errors.append('Chapter 20 carrier route drifted')
if formal.get('invariance')!='R_(M1,τ1) ⇓ D ∧ R_(M2,τ2) ⇓ D':
    errors.append('Chapter 20 conditional invariance equation drifted')
if len(ci20.get('canonical_field_components',[]))!=5:
    errors.append('Chapter 20 canonical field must declare exactly 5 component groups')
if ci20.get('terms',{}).get('planck_data_field')!='project term for canonical D; not a physical Planck-scale claim':
    errors.append('Chapter 20 Planck-dataveld boundary label drifted')
if cm20!=derived20:
    errors.append('Chapter 20 committed measurement does not match executable derivation')
if not cm20.get('deterministic_witness_match'):
    errors.append('Chapter 20 deterministic A/B witness match failed')
if cm20.get('carrier_content_consumed') is not False:
    errors.append('Chapter 20 current adapter must explicitly report carrier_content_consumed=false')
if cm20.get('reader_independence_proven') is not False:
    errors.append('Chapter 20 reader-independence must remain false for the vacuous witness adapter')
if cm20.get('vacuity_status')!='CURRENT ADAPTER IGNORES CARRIER CONTENT':
    errors.append('Chapter 20 vacuity status drifted')
if cm20.get('carrier_A_sha256')!=cm20.get('carrier_B_sha256'):
    errors.append('Chapter 20 carrier A/B canonical hashes differ')
if cm20.get('canonical_sha256')!=cm20.get('carrier_A_sha256'):
    errors.append('Chapter 20 canonical hash does not match carrier witness hash')
if carrier_canonical_sha256(cm20.get('field'))!=cm20.get('canonical_sha256'):
    errors.append('Chapter 20 canonical field hash is not reproducible')
typing=ci20.get('typing',{})
if typing.get('0')!='carrier: (M,τ), replaceable within interface contract':
    errors.append('Chapter 20 carrier typing drifted')
if 'not arithmetic equality' not in typing.get('1_equiv_0',''):
    errors.append('Chapter 20 1≡0 must remain non-arithmetic project notation')
orth=ci20.get('orthogonal_claims',{})
if orth.get('self_consistency',{}).get('status')!='EXACT_ON_SERIALIZED_SUBSET':
    errors.append('Chapter 20 self-consistency status drifted')
if orth.get('reader_independence',{}).get('status')!='PROVEN_REAL_CARRIERS':
    errors.append('Chapter 20 reader-independence must be PROVEN_REAL_CARRIERS')
if orth.get('reader_independence',{}).get('real_carriers_status')!='PASS':
    errors.append('Chapter 20 reader-independence real carriers must be PASS')
if orth.get('reader_independence',{}).get('evidence')!='data/reader_independence_real_carriers_ch20.json':
    errors.append('Chapter 20 reader-independence evidence path drifted')
if orth.get('full_semantic_self_read',{}).get('status')!='EXACT_FULL_SEMANTIC':
    errors.append('Chapter 20 full semantic self-read must be EXACT_FULL_SEMANTIC')
q20=json.loads(QF20.read_text(encoding='utf-8'))
if q20.get('theorem',{}).get('factorization')!='f = i ∘ b ∘ p':
    errors.append('Chapter 20 quotient factorization drifted')
if q20.get('theorem',{}).get('result')!='X/~_f ≅ im(f)':
    errors.append('Chapter 20 quotient-image result drifted')
if q20.get('chapter17',{}).get('construction_direction')!='equivalence-first':
    errors.append('Chapter 20 Ch17 factorization direction drifted')
if q20.get('chapter20',{}).get('construction_direction')!='function-first':
    errors.append('Chapter 20 Ch20 factorization direction drifted')
if q20.get('chapter20',{}).get('distinguished_fiber',{}).get('nontriviality')!='A_ψ⁻¹(D) ≠ C':
    errors.append('Chapter 20 distinguished fiber nontriviality drifted')
if 'no algebraic homomorphism theorem is asserted' not in q20.get('theorem',{}).get('boundary',''):
    errors.append('Chapter 20 factorization scope boundary missing')

rig=json.loads(RIG20.read_text(encoding='utf-8'))
conds={x.get('id'):x.get('predicate') for x in rig.get('reader_independence',{}).get('conditions',[])}
if conds!={'RI1':'A_ψ(c₁)=D','RI2':'A_ψ(c₂)=D','RI3':'∃ c′ : A_ψ(c′) ≠ D'}:
    errors.append('Chapter 20 reader-independence 3-condition gate drifted')
if rig.get('reader_independence',{}).get('gate')!='EXACT only if RI1 ∧ RI2 ∧ RI3 and independence provenance all pass':
    errors.append('Chapter 20 reader-independence exact gate drifted')
if rig.get('reader_independence',{}).get('current',{}).get('reader_independence_proven') is not True:
    errors.append('Chapter 20 reader-independence must be proven')
cur=rig.get('reader_independence',{}).get('current',{})
if cur.get('RI1')!='PASS' or cur.get('RI2')!='PASS' or cur.get('RI3')!='PASS':
    errors.append('Chapter 20 reader-independence RI1/RI2/RI3 must be PASS')
if cur.get('carrier_content_consumed') is not True:
    errors.append('Chapter 20 reader-independence carriers must consume content')
if rig.get('reader_independence',{}).get('real_carriers',{}).get('carrier_A',{}).get('parser')!='xml.etree.ElementTree':
    errors.append('Chapter 20 carrier A parser drifted')
if 're (regex)' not in rig.get('reader_independence',{}).get('real_carriers',{}).get('carrier_B',{}).get('parser',''):
    errors.append('Chapter 20 carrier B parser drifted')
if rig.get('reader_independence',{}).get('optional_stronger_property',{}).get('name')!='component-wise sensitivity':
    errors.append('Chapter 20 component-wise sensitivity spec missing')

rcc20=json.loads(RCC20.read_text(encoding='utf-8'))
if rcc20!=derive_ri_real():
    errors.append('Chapter 20 real-carriers measurement drifted')
if not rcc20.get('reader_independence_proven'):
    errors.append('Chapter 20 real-carriers gate must pass')
if not rcc20.get('RI1') or not rcc20.get('RI2') or not rcc20.get('RI3'):
    errors.append('Chapter 20 real-carriers RI1/RI2/RI3 failed')
if rcc20.get('carriers',{}).get('A',{}).get('d_canonical_atlas_sha256')!=rcc20.get('carriers',{}).get('B',{}).get('d_canonical_atlas_sha256'):
    errors.append('Chapter 20 carriers A/B canonical atlas hashes differ')
if rcc20.get('carriers',{}).get('prime',{}).get('d_canonical_atlas_sha256')==rcc20.get('carriers',{}).get('A',{}).get('d_canonical_atlas_sha256'):
    errors.append('Chapter 20 corrupted carrier must produce different D')
if rcc20.get('independence_provenance',{}).get('shared_parsing_code') is not False:
    errors.append('Chapter 20 carriers must not share parsing code')

ir=json.loads(IR20.read_text(encoding='utf-8'))
if ir!=derive_independent_reader():
    errors.append('Chapter 20 independent-reader measurement drifted')
if not ir.get('pass') or ir.get('shared_parser_code_with_P_phi') is not False:
    errors.append('Chapter 20 independent property reader failed or shares parser route')
if not all(ir.get('checks',{}).values()):
    errors.append('Chapter 20 independent property reader has failing properties')
if ir.get('checks',{}).get('equation_content_nonempty') is not True:
    errors.append('Chapter 20 equation content invariant failed')
if ir.get('checks',{}).get('ch14_png_sha256_recomputed') is not True:
    errors.append('Chapter 20 independent SHA-256 recomputation failed')
if len(ir.get('checks',{}))!=9:
    errors.append('Chapter 20 independent reader must expose exactly 9 checks')
fi20=json.loads(FI20.read_text(encoding='utf-8'))
if fi20!=derive_fault_injection():
    errors.append('Chapter 20 fault-injection measurement drifted')
if not fi20.get('all_expectations_match'):
    errors.append('Chapter 20 P_chi fault-injection expectations failed')
det={x.get('mutation'):x.get('detected') for x in fi20.get('mutations',[])}
if det!={'M1_hash_char_flip':True,'M2_remove_field':True,'M3_swap_two_ids':True,'M4_add_field_103_to_104':True,'M5_empty_one_equation':True}:
    errors.append('Chapter 20 P_chi sensitivity matrix drifted')

rigm20=json.loads(RIGM20.read_text(encoding='utf-8'))
if rigm20!=derive_ri_gate():
    errors.append('Chapter 20 RI gate measurement drifted')
if not rigm20.get('gate_logic_tested'):
    errors.append('Chapter 20 RI gate logic unit test failed')
if not rigm20.get('valid_nonconstant_fixture',{}).get('pass'):
    errors.append('Chapter 20 RI gate must accept valid nonconstant fixture')
if rigm20.get('constant_fixture',{}).get('pass'):
    errors.append('Chapter 20 RI gate must reject constant fixture')
if rigm20.get('missing_provenance_fixture',{}).get('pass'):
    errors.append('Chapter 20 RI gate must reject missing provenance')
fsd20=json.loads(FSD20.read_text(encoding='utf-8'))
fsdm20=json.loads(FSDM20.read_text(encoding='utf-8'))
if fsdm20!=derive_full_semantic_delta(): errors.append('Chapter 20 full-semantic delta measurement drifted')
if not fsdm20.get('pass'): errors.append('Chapter 20 full-semantic delta partition failed')
if fsdm20.get('concept_field_count')!=16 or fsdm20.get('concept_record_count')!=103: errors.append('Chapter 20 full-semantic delta counts drifted')
if fsdm20.get('closure_status')!='TOTAL_PROJECTION_IMPLEMENTED': errors.append('Chapter 20 full-semantic closure status drifted')
if fsd20.get('minimal_total_projection',{}).get('equality_test')!='canonical_json(P_full(G_total(A_canonical))) == canonical_json(A_canonical)': errors.append('Chapter 20 total projection equality target drifted')

fsm20=json.loads(FSM20.read_text(encoding='utf-8'))
if fsm20!=derive_full_semantic_self_read(): errors.append('Chapter 20 full-semantic self-read measurement drifted')
if fsm20.get('status')!='EXACT_FULL_SEMANTIC' or not fsm20.get('local_verification_pass') or not fsm20.get('canonical_equal'):
    errors.append('Chapter 20 P_full equality/local verification failed')
if fsm20.get('rebuilt_sha256')!=fsm20.get('committed_sha256'):
    errors.append('Chapter 20 P_full canonical hashes differ')

fsf20=json.loads(FSF20.read_text(encoding='utf-8'))
if fsf20!=derive_full_semantic_faults(): errors.append('Chapter 20 semantic fault measurement drifted')
if not fsf20.get('pass'):
    errors.append('Chapter 20 semantic M6/M7 fault suite failed')
if not fsf20.get('M6_parameter_corruption',{}).get('local_math_failures'):
    errors.append('Chapter 20 M6 must localize a math-signature failure')
if not fsf20.get('M7_record_reorder',{}).get('chapter_crosscheck_failures'):
    errors.append('Chapter 20 M7 must trigger chapter cross-check')

cjs20=json.loads(CJS20.read_text(encoding='utf-8'))
from canonical_json import canonical_json as _cj
for vec in cjs20.get('known_answer_vectors',[]):
    if _cj(vec['input'])!=vec['canonical']:
        errors.append('canonicalJSON known-answer vector failed: '+vec.get('name','?'))



ladder=ci20.get('ladder_status',{})
if ladder!={'self_consistency':'EXACT_ON_SERIALIZED_SUBSET','independent_reader':'PROPERTY_CHECK_PASS + FAULT_SENSITIVITY_5_OF_5','RI_gate_logic':'TESTED','reader_independence':'REAL_CARRIERS_PASS','full_semantic_self_read':'EXACT_FULL_SEMANTIC'}:
    errors.append('Chapter 20 final ladder status drifted')

rr=ci20.get('read_route',{})
if rr.get('generation')!='G : atlas-data → SVG' or rr.get('parsing')!='P_φ : SVG → parsed structure' or rr.get('tokenization')!='T_τ : text → token sequence':
    errors.append('Chapter 20 read-route operator definitions drifted')
if rr.get('status',{}).get('full_self_reading')!='EXACT_FULL_SEMANTIC':
    errors.append('Chapter 20 full self-reading must be EXACT_FULL_SEMANTIC')
if len(ci20.get('carrier_classes',[]))!=2 or any('not an actual model execution' not in c.get('status','') for c in ci20['carrier_classes']):
    errors.append('Chapter 20 carrier fixtures must remain abstract interface witnesses')
# AGNI additive semantic projection invariant
payload_fields=["chapter","chapter_title","title","subtitle","domain","signal_type","parameters","validation","relations"]
for g in groups:
    sem=[k for k in g.attrib if k.startswith("data-sem-") and k.endswith("-b64")]
    expected_sem={"data-sem-"+f.replace("_","-")+"-b64" for f in payload_fields}
    if set(sem)!=expected_sem:
        errors.append(g.attrib.get("data-concept","?")+": AGNI projection must contain exactly 9 semantic payload attributes")
    if "data-semantic-b64" in g.attrib:
        errors.append(g.attrib.get("data-concept","?")+": legacy aggregate semantic payload attribute forbidden")
    if not g.attrib.get("data-equation","").strip():
        errors.append(g.attrib.get("data-concept","?")+": existing data-equation must remain non-empty")


# Chapter 20 self-read roundtrip
sr20=json.loads(SR20.read_text(encoding='utf-8'))
if sr20!=derive_self_read():
    errors.append('Chapter 20 self-read committed measurement drifted')
if sr20.get('status')!='EXACT_ON_SERIALIZED_SUBSET':
    errors.append('Chapter 20 serialized self-read must be exact')
if sr20.get('counts',{}).get('concepts_parsed')!=103 or sr20.get('counts',{}).get('fragment_hashes_match')!=103:
    errors.append('Chapter 20 self-read concept/hash counts mismatch')
if sr20.get('counts',{}).get('chapters_in_metadata')!=20 or not sr20.get('chapter_titles_match'):
    errors.append('Chapter 20 self-read chapter metadata mismatch')
if sr20.get('full_self_reading')!='OPEN':
    errors.append('Chapter 20 full self-reading must remain OPEN')

ns={'svg':'http://www.w3.org/2000/svg'}
meta=json.loads(root.find('svg:metadata',ns).text)
if len(meta.get('chapters',[]))!=20 or meta.get('default_discrete_frame')!=64:
    errors.append('SVG metadata invariant failed')

if errors:
    print('VALIDATION FAILED')
    for e in errors: print('-',e)
    raise SystemExit(1)

print('VALIDATION PASS')
print('- 20 chapters / 103 unique SVG concepts')
print('- atlas.json / concepts.ndjson synchronized')
print('- JSON Schema validation: PASS')
print('- per-concept SVG fragment hashes verified')
print('- per-concept math signature hashes verified')
print(f'- DT sinusoid DFT support: {support}')
print(f'- DTFS support: {support2}')
print(f'- Chapter 12 avalanche experiment: {hd}/256 output bits changed')
print('- convolution, Nyquist, z-plane, finite-state, address-geometry, encoding, UTF73 and abjad invariants: PASS')
print('- Chapter 16 abjad: 28-letter direct table · V1/V3/V9 exact · three layers separated')
print('- Chapter 17 quotient theorem: 9-point disjoint union → boundary quotient → 7-point general Frame · A1–A4 PASS')
print('- Chapter 17 crosschecks: 7∈V1 · T(7)=5 · zay↦7 · atomicity remains axiomatic')
print('- Chapter 18 transformer frame: AUDITED SLICE MODEL · C/S valid per-layer · b=b1 merge event · A2 local · Seed 6+1 exact')
print('- Chapter 19 choice geometry: 6 used θ entries · 5 locked · θ_bridge ROUTED_OPEN · Θ_used\\Θ_locked={θ_bridge} · closure OPEN_BY_DESIGN')
print(f'- Chapter 20 carrier witness: canonical D hash {cm20["canonical_sha256"][:16]}… · deterministic A/B MATCH · carrier content NOT consumed · reader-independence OPEN')
print('- Chapter 20 self-read: 103/103 concepts · equations/texts/hashes MATCH · 20/20 chapter metadata · EXACT_ON_SERIALIZED_SUBSET')
print('- Chapter 20 independent reader P_χ: 9/9 properties PASS · fault sensitivity 5/5 mutations detected · semantic guards active')
print('- Chapter 20 RI gate logic: valid nonconstant ACCEPT · constant REJECT · missing provenance REJECT')
print(f'- Chapter 20 reader independence: REAL CARRIERS PASS · A=XML DOM · B=regex scan · RI1/RI2/RI3 all PASS · D={rcc20["carriers"]["A"]["d_canonical_atlas_sha256"][:16]}… · prime≠D')
print('- Chapter 20 quotient factorization: f=i∘b∘p · X/~_f≅im(f) · RI1/RI2/RI3 gate registered · reader-independence PROVEN')
print('- Chapter 20 full semantic: 5 direct/recomputed + 2 derivable + 9 payload = 16 · P_full EXACT · canonicalJSON equality PASS')
print('- Chapter 20 semantic faults: M6 parameter corruption detected/localized · M7 cross-chapter reorder detected')
print(f'- Chapter 16 corpus: {quran_status}')
print(f'- Candidate arithmetic: 1/3 − 2050/6236 = {gap.numerator}/{gap.denominator}')
print(f'- Chapter 15 UTF73 reference identity: {sum(fixed)}/73 · reference quotient 64×{q+1} + 9×{q}')
print(f'- Chapter 15 live RGB24 basins: sum={int(real.sum())} · min={int(real.min())} · max={int(real.max())} · śūnya={int(real[72])}')
print(f'- Chapter 14 PNG: {len(raw1)} bytes · Base64: {len(b64)} chars · first4={first4} · indices={idx4}')
print(f'- IPv4 mapped slot: {v4} = 0x{int(v4):08X} → {v6.compressed}')

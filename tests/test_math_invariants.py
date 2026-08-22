from pathlib import Path
import json, subprocess, sys, unittest, hashlib
import numpy as np

ROOT=Path(__file__).resolve().parent.parent

class AtlasMathTests(unittest.TestCase):
    def test_dt_sinusoid_support(self):
        N=64;n=np.arange(N);x=np.sin(2*np.pi*5*n/N)
        self.assertEqual(np.where(np.abs(np.fft.fft(x))>1e-9)[0].tolist(),[5,59])

    def test_dtfs_support(self):
        N=16;n=np.arange(N);x=np.cos(2*np.pi*3*n/N)+.5*np.cos(2*np.pi*5*n/N)
        self.assertEqual(np.where(np.abs(np.fft.fft(x)/N)>1e-9)[0].tolist(),[3,5,11,13])

    def test_dataset_count(self):
        d=json.loads((ROOT/'data'/'atlas.json').read_text(encoding='utf-8'))
        self.assertEqual(d['chapter_count'],20)
        self.assertEqual(d['concept_count'],103)
        self.assertEqual(len({x['concept_id'] for x in d['concepts']}),103)

    def test_modular_addition(self):
        self.assertEqual((0xF0000011+0x30000022)&0xffffffff,0x20000033)

    def test_hash_avalanche_embedded_experiment(self):
        d0=hashlib.sha256(bytes(64)).digest()
        d1=hashlib.sha256(bytes([1])+bytes(63)).digest()
        self.assertEqual(sum((a^b).bit_count() for a,b in zip(d0,d1)),133)


    def test_ipv4_mapped_ipv6_slot(self):
        import ipaddress
        v4=ipaddress.IPv4Address("192.0.2.33")
        v6=ipaddress.IPv6Address("::ffff:192.0.2.33")
        self.assertEqual(int(v4),0xC0000221)
        self.assertEqual(int(v6)&0xffffffff,int(v4))
        self.assertEqual(v6.ipv4_mapped,v4)


    def test_base64_frame_shift(self):
        import base64
        raw=(ROOT/'assets'/'ch14_test_object.png').read_bytes()
        b64=base64.b64encode(raw)
        self.assertEqual(base64.b64decode(b64),raw)
        self.assertEqual(len(b64),((len(raw)+2)//3)*4)
        alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
        idx=[alphabet.index(chr(c)) for c in b64[:4]]
        self.assertEqual(''.join(f'{b:08b}' for b in raw[:3]),
                         ''.join(f'{i:06b}' for i in idx))

    def test_encoding_geometry_dataset(self):
        e=json.loads((ROOT/'data'/'encoding_geometry.json').read_text(encoding='utf-8'))
        raw=(ROOT/'assets'/'ch14_test_object.png').read_bytes()
        import base64
        self.assertEqual(e['png_length_bytes'],len(raw))
        self.assertEqual(e['base64_length_chars'],len(base64.b64encode(raw)))
        self.assertFalse(e['physical_planck_scale_claim'])


    def test_utf73_reference_identity_and_quotient(self):
        d=json.loads((ROOT/'data'/'sanskrit_utf73.json').read_text(encoding='utf-8'))
        self.assertEqual(len(d['states']),73)
        self.assertEqual(len({s['symbol'] for s in d['states']}),73)
        self.assertTrue(all((i%73)==i for i in range(73)))
        self.assertTrue(all('्' not in s['symbol'] for s in d['states']))
        self.assertTrue(any('ं' in s['symbol'] for s in d['states']))
        q,r=divmod(2**24,73)
        self.assertEqual((q,r),(229824,64))
        basins=[q+(i<r) for i in range(73)]
        self.assertEqual(sum(basins),2**24)
        self.assertEqual(basins.count(229825),64)
        self.assertEqual(basins.count(229824),9)

    def test_utf73_unicode_utf8(self):
        import unicodedata
        d=json.loads((ROOT/'data'/'sanskrit_utf73.json').read_text(encoding='utf-8'))
        self.assertEqual(ord('ं'),0x0902)
        self.assertEqual(unicodedata.name('ं'),'DEVANAGARI SIGN ANUSVARA')
        self.assertEqual(ord('·'),0x00B7)
        for s in d['states']:
            raw=s['symbol'].encode('utf-8')
            self.assertEqual(raw.decode('utf-8'),s['symbol'])
            self.assertEqual(raw.hex(' '),s['utf8_hex'])


    def test_utf73_live_encoder_spots_and_basin_sum(self):
        import importlib.util
        spec=importlib.util.spec_from_file_location("utf73_field",ROOT/'tools'/'utf73_field.py')
        mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
        self.assertEqual(mod.rgb_to_state_scalar(0,0,0),72)
        # Achromatic non-black follows hue sector 0 and brightness bin from V.
        self.assertEqual(mod.rgb_to_state_scalar(255,255,255),11)
        self.assertEqual(mod.rgb_to_state_scalar(255,0,0),11)
        data=json.loads((ROOT/'data'/'utf73_rgb24_basins.json').read_text(encoding='utf-8'))
        counts=[x['rgb24_basin_size'] for x in data['states']]
        self.assertEqual(sum(counts),2**24)
        self.assertEqual(counts[72],1)
        self.assertEqual(min(counts),1)
        self.assertEqual(max(counts),633241)

    def test_utf73_validator_is_self_contained(self):
        h=(ROOT/'validators'/'sanskrit_utf73.html').read_text(encoding='utf-8')
        self.assertIn('TextEncoder',h)
        self.assertIn('TextDecoder',h)
        self.assertIn('btoa',h)
        self.assertIn('atob',h)
        self.assertNotIn('<script src=',h)
        self.assertNotIn('http://',h)
        self.assertNotIn('https://',h)


    def test_abjad_field_and_orbits(self):
        import importlib.util
        spec=importlib.util.spec_from_file_location("abjad_field",ROOT/'tools'/'abjad_field.py')
        mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
        d=mod.load_spec()
        self.assertEqual(len(d['letters']),28)
        self.assertEqual(mod.doubling_cycle(1),[1,2,4,8,7,5])
        self.assertEqual(mod.doubling_cycle(3),[3,6])
        self.assertEqual(mod.doubling_cycle(9),[9])
        self.assertEqual(mod.encode("ابجد"),[1,2,3,4])

    def test_abjad_normalization_is_direct_and_explicit(self):
        import importlib.util
        spec=importlib.util.spec_from_file_location("abjad_field",ROOT/'tools'/'abjad_field.py')
        mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
        self.assertEqual(mod.normalize('أإآٱا'),'ااااا')
        self.assertEqual(mod.normalize('ؤو'),'وو')
        self.assertEqual(mod.normalize('ئیىي'),'يييي')
        self.assertEqual(mod.normalize('ةه'),'هه')
        self.assertEqual(mod.encode('ابجد'),[1,2,3,4])
        self.assertIn('charCode',mod.load_spec()['mapping_semantics'])

    def test_quran_candidate_fraction_is_exact(self):
        from fractions import Fraction
        h=json.loads((ROOT/'data'/'quran_abjad_hypothesis.json').read_text(encoding='utf-8'))
        m=h['measurement']
        self.assertEqual((m['candidate_count'],m['candidate_total']),(2050,6236))
        self.assertEqual(Fraction(1,3)-Fraction(2050,6236),Fraction(43,9354))
        self.assertIn('orbit-class frequency',m['tested_statistic'])
        self.assertTrue(m['target_orbit_class'].startswith('unresolved'))

    def test_quran_measure_function_on_synthetic_ayahs(self):
        import importlib.util, sys
        tools=str(ROOT/'tools')
        if tools not in sys.path: sys.path.insert(0,tools)
        import analyze_quran_abjad as aq
        # Sums: ا=1 -> root1/V1; ج=3 -> root3/V3; ط=9 -> root9/V9.
        result=aq.measure([('1:1','ا'),('1:2','ج'),('1:3','ط')])
        self.assertEqual(result['digital_root_counts']['1'],1)
        self.assertEqual(result['digital_root_counts']['3'],1)
        self.assertEqual(result['digital_root_counts']['9'],1)
        self.assertEqual(result['orbit_counts'],{'V1':1,'V3':1,'V9':1})
        self.assertEqual(result['orbit_statistics']['V1']['count'],1)
        self.assertEqual(result['orbit_statistics']['V3']['count'],1)
        self.assertEqual(result['orbit_statistics']['V9']['count'],1)
        self.assertEqual(result['orbit_statistics']['V1']['gap_fraction'],'0/1')

    def test_quran_fixture_boundary_status(self):
        src=json.loads((ROOT/'corpora'/'quran_uthmani'/'source.json').read_text(encoding='utf-8'))
        self.assertEqual(src['expected_ayahs'],6236)
        meas=json.loads((ROOT/'data'/'quran_abjad_measurement.json').read_text(encoding='utf-8'))
        fixture=ROOT/'corpora'/'quran_uthmani'/'quran.jsonl'
        if not fixture.exists():
            self.assertEqual(meas['status'],'fixture_missing')
            self.assertEqual(meas['candidate_only'],{'count':2050,'total':6236,'gap_fraction':'43/9354'})


    def test_language_frame_quotient_closure_theorem(self):
        import importlib, sys
        tools_path=str(ROOT/'tools')
        if tools_path not in sys.path:
            sys.path.insert(0,tools_path)
        mod=importlib.import_module("language_frame_closure")
        frames=[mod.make_atomic("L"),mod.make_atomic("G"),mod.make_atomic("E")]
        q=mod.quotient_three(frames)
        checks=mod.validate_general_frame(q)
        self.assertEqual(len(q['prequotient_points']),9)
        self.assertEqual(len(set(q['prequotient_points'])),9)
        self.assertEqual(len(q['quotient_points']),7)
        self.assertEqual(len(q['C_prime']),3)
        self.assertEqual(len(q['S_prime']),3)
        self.assertEqual(q['boundary_class'],['E:b','G:b','L:b'])
        self.assertTrue(all(checks.values()))

    def test_language_closure_7_is_quotient_not_added_point(self):
        d=json.loads((ROOT/'data'/'language_closure_7.json').read_text(encoding='utf-8'))
        self.assertEqual(d['prequotient']['cardinality'],9)
        self.assertEqual(d['equivalence_relation']['classes_removed_by_identification'],2)
        self.assertEqual(d['quotient']['cardinality'],7)
        self.assertEqual(9-(3-1),7)
        self.assertTrue(d['closure_theorem']['canonical_partition'])
        self.assertIn('not derived here',d['atomicity_status'])
        self.assertIn('not AtomicFrame',d['recursive_typing']['not_claimed'])

    def test_language_closure_7_v1_abjad_crosscheck(self):
        c=json.loads((ROOT/'data'/'language_closure_7.json').read_text(encoding='utf-8'))
        a=json.loads((ROOT/'data'/'abjad_field.json').read_text(encoding='utf-8'))
        self.assertEqual(c['mod9']['V1'],[1,2,4,8,7,5])
        self.assertIn(7,c['mod9']['V1'])
        self.assertEqual(c['mod9']['T7'],5)
        self.assertEqual((a['letters'][6]['char'],a['letters'][6]['value']),('ز',7))


    def test_ch18_audited_slice_model(self):
        d=json.loads((ROOT/'data'/'transformer_frame_ch18.json').read_text(encoding='utf-8'))
        self.assertEqual(d['ledger']['current_status'],'AUDITED SLICE MODEL')
        self.assertEqual(d['frame_correspondence'][0]['scope'],'per-layer')
        self.assertEqual(d['frame_correspondence'][1]['scope'],'per-layer')
        self.assertEqual(d['axiom_audit']['scope'],'local/per-layer, not whole-network')
        self.assertEqual(d['frame_correspondence'][2]['selected_candidate'],'b1')
        self.assertIn('next layer',d['frame_correspondence'][2]['rejected_candidate'])
        self.assertEqual(d['seed_geometry']['coordination_number'],6)
        self.assertEqual(d['seed_geometry']['center']+d['seed_geometry']['first_ring'],7)
        self.assertEqual(d['orbit_rotation_bridge']['audit_status'],'ANALOGY CANDIDATE')
        self.assertEqual(d['self_reference']['status'],'PROVENANCE OBSERVATION')


    def test_ch19_choice_registry_and_reflection(self):
        d=json.loads((ROOT/'data'/'choice_geometry_ch19.json').read_text(encoding='utf-8'))
        self.assertEqual(d['operator']['equation'],'F_θ : X → Y, θ ∈ Θ')
        self.assertEqual([x['id'] for x in d['choice_registry']],
                         ['theta_raster','theta_utf73','theta_bridge','theta_abjad','theta_atomic','theta_transformer'])
        self.assertEqual(d['choice_accounting']['pending_choice_ids'],[])
        self.assertEqual(d['choice_accounting']['routed_open_choice_ids'],['theta_bridge'])
        self.assertEqual(d['choice_accounting']['closure_semantics'],'OPEN_BY_DESIGN')
        self.assertFalse(d['choice_accounting']['closure_complete'])
        bridge=next(x for x in d['choice_registry'] if x['id']=='theta_bridge')
        self.assertEqual(bridge['status'],'ROUTED_OPEN')
        self.assertEqual(bridge['lock_policy'],'NONE_BY_DESIGN')
        self.assertEqual(bridge['endpoint'],'0.0.0.0')
        self.assertEqual(bridge['default_route_prefix'],'0.0.0.0/0')
        self.assertIsNone(bridge['locked_by'])
        self.assertEqual(len(d['geometric_chain']),4)
        self.assertEqual(len(d['symbolic_chain']),5)
        self.assertEqual(d['reflection']['equation'],'θ → F_θ → F_θ(X) → encode(θ,F_θ,results)')
        self.assertIn('not a claim that θ causes itself',d['reflection']['self_reference_boundary'])

    def test_ch19_base64_and_raster_statuses(self):
        d=json.loads((ROOT/'data'/'choice_geometry_ch19.json').read_text(encoding='utf-8'))
        byop={x['operator']:x for x in d['geometric_chain']}
        self.assertTrue(byop['B']['invertibility'].startswith('bijective'))
        self.assertEqual(byop['R']['invertibility'],'generally lossy')
        self.assertEqual(byop['V']['invertibility'],'not exact in general')


    def test_ch20_canonical_carrier_invariance(self):
        import sys
        sys.path.insert(0,str(ROOT/'tools'))
        from carrier_invariance import derive, canonical_sha256
        committed=json.loads((ROOT/'data'/'carrier_invariance_measurement.json').read_text(encoding='utf-8'))
        d=derive()
        self.assertEqual(committed,d)
        self.assertTrue(d['deterministic_witness_match'])
        self.assertFalse(d['carrier_content_consumed'])
        self.assertFalse(d['reader_independence_proven'])
        self.assertEqual(d['vacuity_status'],'CURRENT ADAPTER IGNORES CARRIER CONTENT')
        self.assertEqual(d['carrier_A_sha256'],d['carrier_B_sha256'])
        self.assertEqual(d['canonical_sha256'],canonical_sha256(d['field']))
        self.assertEqual(d['canonical_sha256'],d['carrier_A_sha256'])

    def test_ch20_scope_and_read_route(self):
        d=json.loads((ROOT/'data'/'carrier_invariance_ch20.json').read_text(encoding='utf-8'))
        self.assertEqual(d['formalization']['carrier_route'],'(M,τ) → adapter → R → D')
        self.assertIn('conditional',d['formalization']['scope'])
        self.assertEqual(d['terms']['planck_data_field'],
                         'project term for canonical D; not a physical Planck-scale claim')
        self.assertEqual(d['read_route']['generation'],'G : atlas-data → SVG')
        self.assertEqual(d['read_route']['parsing'],'P_φ : SVG → parsed structure')
        self.assertEqual(d['read_route']['tokenization'],'T_τ : text → token sequence')
        self.assertEqual(d['read_route']['status']['full_self_reading'],'EXACT_FULL_SEMANTIC')
        self.assertIn('not arithmetic equality',d['typing']['1_equiv_0'])


    def test_ch20_self_read_roundtrip(self):
        import sys
        sys.path.insert(0,str(ROOT/'tools'))
        from self_read_roundtrip import derive
        d=derive()
        self.assertEqual(d['status'],'EXACT_ON_SERIALIZED_SUBSET')
        self.assertEqual(d['counts']['concepts_parsed'],103)
        self.assertEqual(d['counts']['equations_match'],103)
        self.assertEqual(d['counts']['texts_match'],103)
        self.assertEqual(d['counts']['fragment_hashes_match'],103)
        self.assertEqual(d['counts']['chapters_in_metadata'],20)
        self.assertTrue(d['chapter_titles_match'])
        self.assertEqual(d['full_self_reading'],'OPEN')


    def test_ch20_quotient_factorization_spec(self):
        d=json.loads((ROOT/'data'/'quotient_factorization_ch20.json').read_text(encoding='utf-8'))
        self.assertEqual(d['theorem']['factorization'],'f = i ∘ b ∘ p')
        self.assertEqual(d['theorem']['result'],'X/~_f ≅ im(f)')
        self.assertEqual(d['chapter17']['construction_direction'],'equivalence-first')
        self.assertEqual(d['chapter17']['bijection'],'identity on X/~_b = im(q)')
        self.assertEqual(d['chapter20']['construction_direction'],'function-first')
        self.assertEqual(d['chapter20']['bijection'],'b([c])=A_ψ(c)')
        self.assertEqual(d['chapter20']['distinguished_fiber']['nontriviality'],'A_ψ⁻¹(D) ≠ C')

    def test_ch20_reader_independence_three_condition_gate(self):
        d=json.loads((ROOT/'data'/'reader_independence_gate_ch20.json').read_text(encoding='utf-8'))
        conds={x['id']:x['predicate'] for x in d['reader_independence']['conditions']}
        self.assertEqual(conds,{'RI1':'A_ψ(c₁)=D','RI2':'A_ψ(c₂)=D','RI3':'∃ c′ : A_ψ(c′) ≠ D'})
        self.assertEqual(d['reader_independence']['gate'],
                         'EXACT only if RI1 ∧ RI2 ∧ RI3 and independence provenance all pass')
        self.assertTrue(d['reader_independence']['current']['reader_independence_proven'])
        self.assertEqual(d['reader_independence']['current']['RI1'],'PASS')
        self.assertEqual(d['reader_independence']['current']['RI2'],'PASS')
        self.assertEqual(d['reader_independence']['current']['RI3'],'PASS')
        self.assertTrue(d['reader_independence']['current']['carrier_content_consumed'])
        self.assertEqual(d['reader_independence']['optional_stronger_property']['name'],
                         'component-wise sensitivity')

    def test_ch20_reader_independence_real_carriers(self):
        import sys
        sys.path.insert(0,str(ROOT/'tools'))
        from reader_independence import derive
        committed=json.loads((ROOT/'data'/'reader_independence_real_carriers_ch20.json').read_text(encoding='utf-8'))
        d=derive()
        self.assertEqual(committed,d)
        self.assertTrue(d['reader_independence_proven'])
        self.assertTrue(d['RI1'])
        self.assertTrue(d['RI2'])
        self.assertTrue(d['RI3'])
        # Both carriers produce same canonical atlas hash
        self.assertEqual(d['carriers']['A']['d_canonical_atlas_sha256'],
                         d['carriers']['B']['d_canonical_atlas_sha256'])
        # Corrupted carrier produces different hash
        self.assertNotEqual(d['carriers']['prime']['d_canonical_atlas_sha256'],
                            d['carriers']['A']['d_canonical_atlas_sha256'])
        # Structural independence
        self.assertFalse(d['independence_provenance']['shared_parsing_code'])
        self.assertTrue(d['independence_provenance']['both_consume_svg_text'])
        self.assertEqual(d['vacuity_status'],'NONE — both carriers parse SVG text independently')
        # D has expected structure
        self.assertEqual(d['D']['concept_count'],103)
        self.assertEqual(d['D']['chapter_count'],20)
        self.assertEqual(len(d['D']['concept_id_list']),103)
        self.assertEqual(len(d['D']['math_signature_map']),103)

    def test_ch20_independent_property_reader(self):
        import sys
        sys.path.insert(0,str(ROOT/'tools'))
        from independent_property_reader import derive
        committed=json.loads((ROOT/'data'/'independent_reader_measurement_ch20.json').read_text(encoding='utf-8'))
        d=derive()
        self.assertEqual(committed,d)
        self.assertTrue(d['pass'])
        self.assertFalse(d['shared_parser_code_with_P_phi'])
        self.assertTrue(d['property_based'])
        self.assertTrue(all(d['checks'].values()))
        self.assertEqual(len(d['checks']),9)


    def test_ch20_independent_reader_fault_injection(self):
        import sys
        sys.path.insert(0,str(ROOT/'tools'))
        from independent_reader_fault_injection import derive
        d=derive()
        self.assertTrue(d['all_expectations_match'])
        det={x['mutation']:x['detected'] for x in d['mutations']}
        self.assertEqual(det,{
            'M1_hash_char_flip':True,
            'M2_remove_field':True,
            'M3_swap_two_ids':True,
            'M4_add_field_103_to_104':True,
            'M5_empty_one_equation':True})
        self.assertEqual(d['sensitivity_summary']['not_detected'],[])


    def test_ch20_equation_content_and_independent_hash_guards(self):
        import sys
        sys.path.insert(0,str(ROOT/'tools'))
        from independent_property_reader import derive
        d=derive()
        self.assertTrue(d['checks']['equation_content_nonempty'])
        self.assertTrue(d['checks']['ch14_png_sha256_recomputed'])
        atlas=json.loads((ROOT/'data'/'atlas.json').read_text(encoding='utf-8'))
        self.assertTrue(all(r['equation'].strip() for r in atlas['concepts']))

    def test_ch20_ri_gate_logic_unit(self):
        import sys
        sys.path.insert(0,str(ROOT/'tools'))
        from reader_independence_gate import derive
        d=derive()
        self.assertTrue(d['gate_logic_tested'])
        self.assertTrue(d['valid_nonconstant_fixture']['pass'])
        self.assertFalse(d['constant_fixture']['pass'])
        self.assertFalse(d['missing_provenance_fixture']['pass'])
        self.assertFalse(d['constant_fixture']['checks']['RI3'])


    def test_ch20_full_semantic_delta_partition(self):
        import sys
        sys.path.insert(0,str(ROOT/'tools'))
        from full_semantic_delta import derive
        d=derive()
        self.assertTrue(d['pass'])
        self.assertEqual(d['concept_field_count'],16)
        self.assertEqual(d['concept_record_count'],103)
        self.assertEqual(d['closure_status'],'TOTAL_PROJECTION_IMPLEMENTED')
        self.assertEqual(set(d['current_recoverable']),
                         {'concept_id','equation','svg_fragment_sha256','math_signature_sha256','svg_text'})
        self.assertEqual(set(d['derivable']),{'svg_element_count','svg_selector'})
        self.assertEqual(len(d['semantic_payload_delta']),9)


    def test_ch20_canonical_json_known_answers(self):
        import sys
        sys.path.insert(0,str(ROOT/'tools'))
        from canonical_json import canonical_json
        spec=json.loads((ROOT/'data'/'canonical_json_spec_ch20.json').read_text(encoding='utf-8'))
        for v in spec['known_answer_vectors']:
            self.assertEqual(canonical_json(v['input']),v['canonical'],v['name'])

    def test_ch20_full_semantic_self_read(self):
        import sys
        sys.path.insert(0,str(ROOT/'tools'))
        from full_semantic_self_read import derive
        committed=json.loads((ROOT/'data'/'full_semantic_self_read_measurement_ch20.json').read_text(encoding='utf-8'))
        d=derive()
        self.assertEqual(committed,d)
        self.assertEqual(d['status'],'EXACT_FULL_SEMANTIC')
        self.assertTrue(d['local_verification_pass'])
        self.assertTrue(d['canonical_equal'])
        self.assertEqual(d['rebuilt_sha256'],d['committed_sha256'])
        self.assertEqual(len(d['local']),103)
        self.assertTrue(all(x['math_hash_match'] and x['svg_hash_match'] and x['chapter_crosscheck']
                            for x in d['local']))

    def test_ch20_full_semantic_faults(self):
        import sys
        sys.path.insert(0,str(ROOT/'tools'))
        from full_semantic_fault_injection import derive
        d=derive()
        self.assertTrue(d['pass'])
        self.assertTrue(d['M6_parameter_corruption']['detected'])
        self.assertTrue(d['M6_parameter_corruption']['local_math_failures'])
        self.assertTrue(d['M7_record_reorder']['detected'])
        self.assertTrue(d['M7_record_reorder']['chapter_crosscheck_failures'])


    def test_ch20_agni_additive_projection(self):
        import xml.etree.ElementTree as ET
        root=ET.parse(ROOT/'assets'/'signals_systems_full_atlas_master.svg').getroot()
        groups=[g for g in root.iter() if g.attrib.get('data-concept')]
        self.assertEqual(len(groups),103)
        expected={'data-sem-'+f.replace('_','-')+'-b64' for f in
                  ['chapter','chapter_title','title','subtitle','domain','signal_type','parameters','validation','relations']}
        for g in groups:
            sem={k for k in g.attrib if k.startswith('data-sem-') and k.endswith('-b64')}
            self.assertEqual(sem,expected)
            self.assertNotIn('data-semantic-b64',g.attrib)
            self.assertTrue(g.attrib['data-concept'])
            self.assertTrue(g.attrib['data-equation'].strip())

    def test_validator(self):
        p=subprocess.run([sys.executable,str(ROOT/'tools'/'validate_atlas.py')],cwd=ROOT,capture_output=True,text=True)
        self.assertEqual(p.returncode,0,p.stdout+p.stderr)

if __name__=='__main__':
    unittest.main()

#!/usr/bin/env python3
from pathlib import Path
import hashlib, html, json
import xml.etree.ElementTree as ET

from canonical_json import canonical_bytes

ROOT=Path(__file__).resolve().parent.parent
SVG=ROOT/'assets'/'signals_systems_full_atlas_master.svg'
DATA=ROOT/'data'
NS={'svg':'http://www.w3.org/2000/svg'}

DOMAIN={
'ct_sinusoid':'continuous-time','dt_sinusoid':'discrete-time','signal_transformations':'time-domain','impulse_step':'time-domain','system_properties':'systems',
'convolution_sum':'discrete-time','convolution_integral':'continuous-time','impulse_response':'systems','step_response':'systems','system_equations':'systems',
'ctfs':'frequency-domain','line_spectrum':'frequency-domain','dtfs':'frequency-domain','gibbs':'time-frequency','fourier_symmetry':'frequency-domain',
'ctft_rect_sinc':'time-frequency','ctft_gaussian':'time-frequency','ctft_modulation':'frequency-domain','ctft_convolution':'time-frequency','ctft_properties':'frequency-domain',
'dtft_periodic':'frequency-domain','dtft_rect':'time-frequency','dtft_shift':'frequency-domain','dtft_unit_circle':'z/frequency-domain','dtft_properties':'frequency-domain',
'freq_response':'frequency-domain','ideal_lpf':'frequency-domain','resonance':'frequency-domain','mag_phase':'frequency-domain','group_delay':'frequency-domain',
'sampling_train':'sampling','sampling_replicas':'sampling/frequency-domain','nyquist':'sampling','aliasing':'sampling/frequency-domain','reconstruction':'sampling',
'dsb_sc':'communications','sidebands':'communications/frequency-domain','demodulation':'communications','fdm':'communications/frequency-domain','communication_chain':'communications',
'laplace_plane':'s-domain','laplace_roc':'s-domain','laplace_causality_stability':'s-domain','inverse_laplace':'s-domain','laplace_system_function':'s-domain',
'z_plane':'z-domain','z_roc_unit_circle':'z-domain','difference_to_z':'z-domain','z_to_dtft':'z/frequency-domain','pole_radius_angle':'z-domain',
'feedback_loop':'feedback','sensitivity':'feedback','closed_loop_poles':'feedback/s-domain','root_locus_concept':'feedback/s-domain','feedback_tradeoffs':'feedback',
'finite_word_state':'finite-state','modular_addition':'finite-state/modular','rotate_xor_mix':'finite-state/boolean',
'compression_round':'finite-state/dynamics','avalanche_diffusion':'finite-state/diffusion','ipv4_word':'network/address','ipv6_lanes':'network/address','ipv4_mapped_ipv6':'network/address','ipv6_prefix_host':'network/address','address_inclusion':'network/address'}

SIGNAL_TYPE={'ct_sinusoid':'CT','dt_sinusoid':'DT','convolution_sum':'DT','convolution_integral':'CT','ctfs':'CT periodic','dtfs':'DT periodic',
'ctft_rect_sinc':'CT aperiodic','ctft_gaussian':'CT aperiodic','dtft_periodic':'DT','dtft_rect':'DT finite','sampling_train':'CT→DT','z_plane':'DT',
'finite_word_state':'32-bit finite word','modular_addition':'32-bit finite word','rotate_xor_mix':'32-bit finite word',
'compression_round':'8×32-bit state','avalanche_diffusion':'512-bit input → 256-bit output','ipv4_word':'32-bit address','ipv6_lanes':'128-bit address','ipv4_mapped_ipv6':'128-bit mapped address','ipv6_prefix_host':'128-bit prefix/host decomposition','address_inclusion':'32→128-bit embedding'}

PARAMETERS={
'dt_sinusoid':{'N':64,'bin':5,'period_samples':12.8},
'convolution_sum':{'N':64,'rect_length':12,'decay_constant_samples':10.0},
'dtfs':{'N':16,'bins':[3,5],'amplitudes':[1.0,0.5]},
'sampling_train':{'sample_count':17,'cycles_shown':2},
'nyquist':{'condition':'fs > 2B'},
'z_to_dtft':{'pole_radius':0.72,'unit_circle_samples':24},
'finite_word_state':{'word_bits':32,'example_word':'0x6A09E667'},
'modular_addition':{'modulus':4294967296,'x':'0xF0000011','y':'0x30000022','result':'0x20000033'},
'rotate_xor_mix':{'word_bits':32,'sigma0_rotations':[2,13,22],'sigma1_rotations':[6,11,25]},
'compression_round':{'state_words':8,'word_bits':32,'rounds':64},
'avalanche_diffusion':{'input_bits':512,'output_bits':256,'input_bit_difference':1,'measured_hamming_distance':133},'ipv4_word':{'address':'192.0.2.33','hex':'0xC0000221','bits':32},'ipv6_lanes':{'bits':128,'lanes_32':4,'text_groups_16':8},'ipv4_mapped_ipv6':{'ipv4':'192.0.2.33','ipv4_hex':'0xC0000221','ipv6':'::ffff:192.0.2.33','prefix_bits':96,'payload_bits':32},'ipv6_prefix_host':{'example_prefix_length':64,'prefix_bits':64,'interface_bits':64},'address_inclusion':{'prefix_words':['0x00000000','0x00000000','0x0000FFFF'],'payload_word':'0xC0000221'}}

VALIDATION={
'dt_sinusoid':{'invariants':['64 samples','DFT support at bins 5 and 59 in full FFT','one-sided dominant bin 5']},
'convolution_sum':{'invariants':['output equals first 64 samples of linear convolution']},
'dtfs':{'invariants':['nonzero DFT support at ±3 and ±5 modulo 16']},
'nyquist':{'invariants':['perfect ideal reconstruction requires sampling rate greater than twice bandwidth']},
'z_to_dtft':{'invariants':['frequency response is H(z) evaluated on |z|=1']},
'feedback_loop':{'invariants':['closed-loop transfer T=G/(1+GH) for negative feedback']},
'finite_word_state':{'invariants':['ROTR is a permutation of 32 indexed bit positions','rotation preserves Hamming weight']},
'modular_addition':{'invariants':['state remains in [0,2^32-1]','overflow wraps modulo 2^32']},
'rotate_xor_mix':{'invariants':['Ch, Maj and Σ functions operate bitwise on 32-bit words']},
'compression_round':{'invariants':['eight 32-bit state words','64 repeated rounds','all additions modulo 2^32']},
'avalanche_diffusion':{'invariants':['two 512-bit inputs differ by one bit','SHA-256 outputs differ in 133 of 256 bits for the embedded experiment']},'ipv4_word':{'invariants':['IPv4 address value is exactly 32 bits','192.0.2.33 equals 0xC0000221']},'ipv6_lanes':{'invariants':['IPv6 address value is exactly 128 bits','128 bits can be partitioned into four 32-bit lanes or eight 16-bit groups']},'ipv4_mapped_ipv6':{'invariants':['mapped prefix is 96 bits','low 32 bits equal the IPv4 address value','::ffff:192.0.2.33 maps 192.0.2.33']},'ipv6_prefix_host':{'invariants':['a /64 split contains 64 prefix bits and 64 remaining address bits']},'address_inclusion':{'invariants':['embedding preserves the 32-bit payload exactly','mapped representation uses a fixed 96-bit prefix']}}

RELATIONS={
'ct_sinusoid':{'transforms_to':['ctfs'],'prerequisites':[]},
'dt_sinusoid':{'transforms_to':['dtfs','dtft_periodic'],'prerequisites':[]},
'convolution_sum':{'transforms_to':['dtft_properties','difference_to_z'],'prerequisites':['impulse_response']},
'convolution_integral':{'transforms_to':['ctft_convolution'],'prerequisites':['impulse_response']},
'sampling_train':{'transforms_to':['sampling_replicas'],'prerequisites':['ctft_rect_sinc']},
'sampling_replicas':{'transforms_to':['nyquist','aliasing'],'prerequisites':['sampling_train']},
'z_plane':{'transforms_to':['z_roc_unit_circle','z_to_dtft'],'prerequisites':['difference_to_z']},
'feedback_loop':{'transforms_to':['sensitivity','closed_loop_poles'],'prerequisites':['laplace_system_function']},
'finite_word_state':{'transforms_to':['modular_addition','rotate_xor_mix'],'prerequisites':['dtft_unit_circle']},
'modular_addition':{'transforms_to':['compression_round'],'prerequisites':['finite_word_state']},
'rotate_xor_mix':{'transforms_to':['compression_round'],'prerequisites':['finite_word_state']},
'compression_round':{'transforms_to':['avalanche_diffusion'],'prerequisites':['modular_addition','rotate_xor_mix']},
'avalanche_diffusion':{'transforms_to':[],'prerequisites':['compression_round']},'ipv4_word':{'transforms_to':['ipv4_mapped_ipv6','address_inclusion'],'prerequisites':['finite_word_state']},'ipv6_lanes':{'transforms_to':['ipv4_mapped_ipv6','ipv6_prefix_host'],'prerequisites':['finite_word_state']},'ipv4_mapped_ipv6':{'transforms_to':['address_inclusion'],'prerequisites':['ipv4_word','ipv6_lanes']},'ipv6_prefix_host':{'transforms_to':[],'prerequisites':['ipv6_lanes']},'address_inclusion':{'transforms_to':[],'prerequisites':['ipv4_mapped_ipv6']}}


ENCODING=json.loads((ROOT/'data'/'encoding_geometry.json').read_text(encoding='utf-8'))
DOMAIN.update({
'vector_test_object':'encoding/vector','raster_frame_boundary':'encoding/raster',
'png_byte_space':'encoding/bytes','base64_frame_shift':'encoding/base64',
'base64_char_space':'encoding/base64','reconstruction_lossiness':'encoding/reconstruction'})
SIGNAL_TYPE.update({
'vector_test_object':'vector geometry','raster_frame_boundary':'160×96 raster',
'png_byte_space':'PNG byte stream','base64_frame_shift':'24-bit repartition',
'base64_char_space':'64-symbol alphabet','reconstruction_lossiness':'exact encoding / lossy geometry'})
PARAMETERS.update({
'vector_test_object':{'viewBox':[0,0,160,96],'coordinate_example':12.4387},
'raster_frame_boundary':{'width':160,'height':96,'pixel_frame':1,'coordinate_example':12.4387,'cell_example':12},
'png_byte_space':{'png_length_bytes':ENCODING['png_length_bytes'],'png_sha256':ENCODING['png_sha256']},
'base64_frame_shift':{'byte_bits':8,'symbol_bits':6,'group_bits':24,'base64_length_chars':ENCODING['base64_length_chars'],'base64_sha256':ENCODING['base64_sha256']},
'base64_char_space':{'alphabet_size':64,'first_16_chars':ENCODING['first_16_base64_chars'],'first_16_indices':ENCODING['first_16_base64_indices']},
'reconstruction_lossiness':{'encoding_roundtrip':'exact','raster_to_vector':'lossy/inferred'}})
VALIDATION.update({
'vector_test_object':{'invariants':['source SVG uses real-valued coordinates','test object viewBox is exactly 160×96']},
'raster_frame_boundary':{'invariants':['CairoSVG raster is exactly 160×96','x=12.4387 is represented within pixel cell i=12 at unit raster frame']},
'png_byte_space':{'invariants':['raw bytes are a valid PNG stream','PNG byte length and SHA-256 are recomputed from the actual raster']},
'base64_frame_shift':{'invariants':['Base64 decode(encode(raw)) equals raw','3×8 bits equals 4×6 bits','encoded length equals ceil(raw/3)×4']},
'base64_char_space':{'invariants':['Base64 alphabet contains exactly 64 unique symbols','every non-padding symbol maps uniquely to index 0…63']},
'reconstruction_lossiness':{'invariants':['Base64 roundtrip is byte-exact','SVG→PNG sampling does not retain original vector primitive identity']}})
RELATIONS.update({
'vector_test_object':{'transforms_to':['raster_frame_boundary'],'prerequisites':[]},
'raster_frame_boundary':{'transforms_to':['png_byte_space'],'prerequisites':['vector_test_object']},
'png_byte_space':{'transforms_to':['base64_frame_shift'],'prerequisites':['raster_frame_boundary']},
'base64_frame_shift':{'transforms_to':['base64_char_space','reconstruction_lossiness'],'prerequisites':['png_byte_space']},
'base64_char_space':{'transforms_to':['reconstruction_lossiness'],'prerequisites':['base64_frame_shift']},
'reconstruction_lossiness':{'transforms_to':[],'prerequisites':['base64_char_space']}})


UTF73=json.loads((ROOT/'data'/'sanskrit_utf73.json').read_text(encoding='utf-8'))
DOMAIN.update({
'utf73_field':'encoding/unicode','utf73_codepoints':'encoding/unicode',
'utf73_utf8':'encoding/utf8','utf73_fixed_point':'encoding/quotient',
'utf73_basins':'encoding/quotient','utf73_vs_base64':'encoding/comparison'})
SIGNAL_TYPE.update({
'utf73_field':'73-state symbol field','utf73_codepoints':'Unicode code-point sequences',
'utf73_utf8':'UTF-8 byte sequences','utf73_fixed_point':'reference-model identity',
'utf73_basins':'measured RGB24 HSV basins','utf73_vs_base64':'finite-code comparison'})
PARAMETERS.update({
'utf73_field':{'states':73,'construction':'6×12+1'},
'utf73_codepoints':{'inherent_codepoints':1,'marked_codepoints':2,'shunya_codepoints':1},
'utf73_utf8':{'devanagari_bytes_per_codepoint':3,'middle_dot_bytes':2,'variable_width':True},
'utf73_fixed_point':{'model':'reference quotient only','encoder':'n mod 73','decoder':'state index','fixed_points':73},
'utf73_basins':UTF73['measured_rgb24_basins'],
'utf73_vs_base64':{'base64_states':64,'utf73_states':73,'log2_73':6.189824558880018}})
VALIDATION.update({
'utf73_field':{'invariants':['exactly 73 states','all states are unique Unicode strings']},
'utf73_codepoints':{'invariants':['slot 12 uses U+0902 DEVANAGARI SIGN ANUSVARA','śūnya is an abstract nil state displayed with U+00B7 MIDDLE DOT']},
'utf73_utf8':{'invariants':['every state UTF-8 encodes and decodes exactly','UTF-8 width is variable across the field']},
'utf73_fixed_point':{'invariants':['reference-model identity only: E(n)=n mod 73 and D(s)=state index imply E(D(s))=s for all 73 states']},
'utf73_basins':{'invariants':['live RGB24→HSV→Σ73 encoder is exhaustively counted over all 2^24 colors','measured basin sum equals 2^24','śūnya basin contains black only']},
'utf73_vs_base64':{'invariants':['64^4 = 2^24 gives exact Base64 24-bit repartition','73 does not divide 2^24']}})
RELATIONS.update({
'utf73_field':{'transforms_to':['utf73_codepoints','utf73_utf8'],'prerequisites':['base64_char_space']},
'utf73_codepoints':{'transforms_to':['utf73_utf8'],'prerequisites':['utf73_field']},
'utf73_utf8':{'transforms_to':['utf73_fixed_point'],'prerequisites':['utf73_codepoints']},
'utf73_fixed_point':{'transforms_to':['utf73_basins'],'prerequisites':['utf73_utf8']},
'utf73_basins':{'transforms_to':['utf73_vs_base64'],'prerequisites':['utf73_fixed_point']},
'utf73_vs_base64':{'transforms_to':[],'prerequisites':['utf73_basins','base64_frame_shift']}})


ABJAD=json.loads((ROOT/'data'/'abjad_field.json').read_text(encoding='utf-8'))
QHYP=json.loads((ROOT/'data'/'quran_abjad_hypothesis.json').read_text(encoding='utf-8'))
QMEAS=json.loads((ROOT/'data'/'quran_abjad_measurement.json').read_text(encoding='utf-8'))
DOMAIN.update({
'abjad_linear_carrier':'encoding/utf8',
'abjad_cultural_mapping':'encoding/abjad',
'abjad_mod9_orbits':'number-theory/dynamics',
'abjad_corpus_fixture':'corpus/provenance',
'abjad_empirical_measure':'corpus/statistics',
'abjad_layer_separation':'methodology'})
SIGNAL_TYPE.update({
'abjad_linear_carrier':'ordered Unicode/UTF-8 carrier',
'abjad_cultural_mapping':'28-letter direct numeric mapping',
'abjad_mod9_orbits':'9-state finite dynamical system',
'abjad_corpus_fixture':'6236-ayah locked corpus boundary',
'abjad_empirical_measure':'ayah-level empirical statistic',
'abjad_layer_separation':'epistemic layer model'})
PARAMETERS.update({
'abjad_linear_carrier':{'order_preserved':True,'lossless':True,'expected_ayahs':6236},
'abjad_cultural_mapping':{'letters':28,'values':[x['value'] for x in ABJAD['letters']],
                          'mapping_semantics':'direct character lookup','excluded':'charCode % 28'},
'abjad_mod9_orbits':ABJAD['mod9'],
'abjad_corpus_fixture':{'fixture':'corpora/quran_uthmani/quran.jsonl','status':QMEAS['status'],
                        'normalization':ABJAD['normalization']},
'abjad_empirical_measure':QMEAS,
'abjad_layer_separation':{'pure_math':'exact','mapping':'explicit choice','carrier':'lossless',
                          'empirical':('measured' if QMEAS['status']=='measured' else 'pending exact fixture')}})
VALIDATION.update({
'abjad_linear_carrier':{'invariants':['UTF-8/Unicode carrier preserves ordered text','fixture SHA identifies exact carrier bytes once locked']},
'abjad_cultural_mapping':{'invariants':['28 unique Arabic letters map directly to 28 classical abjad values','charCode modulo indexing is excluded']},
'abjad_mod9_orbits':{'invariants':['T(r)=dr(2r) yields V1=[1,2,4,8,7,5], V3=[3,6], V9=[9] exactly']},
'abjad_corpus_fixture':{'invariants':['corpus statistics require an exact 6236-ayah fixture','normalization rules are explicit and deterministic','no silent corpus substitution']},
'abjad_empirical_measure':{'invariants':['per ayah: normalize → direct abjad sum → digital root → V1/V3/V9 orbit class','candidate arithmetic 1/3−2050/6236=43/9354 is exact','target orbit class remains unresolved until the prior script or a locked fixture uniquely identifies the 2050 count','candidate is not a reproduced corpus result while fixture is missing']},
'abjad_layer_separation':{'invariants':['pure math, cultural mapping, carrier, and empirical result retain separate statuses']}})
RELATIONS.update({
'abjad_linear_carrier':{'transforms_to':['abjad_cultural_mapping'],'prerequisites':['utf73_vs_base64']},
'abjad_cultural_mapping':{'transforms_to':['abjad_mod9_orbits','abjad_corpus_fixture'],'prerequisites':['abjad_linear_carrier']},
'abjad_mod9_orbits':{'transforms_to':['abjad_empirical_measure'],'prerequisites':['abjad_cultural_mapping']},
'abjad_corpus_fixture':{'transforms_to':['abjad_empirical_measure'],'prerequisites':['abjad_linear_carrier','abjad_cultural_mapping']},
'abjad_empirical_measure':{'transforms_to':['abjad_layer_separation'],'prerequisites':['abjad_mod9_orbits','abjad_corpus_fixture']},
'abjad_layer_separation':{'transforms_to':[],'prerequisites':['abjad_empirical_measure']}})



C7=json.loads((ROOT/'data'/'language_closure_7.json').read_text(encoding='utf-8'))
AX17=json.loads((ROOT/'data'/'language_frame_axioms.json').read_text(encoding='utf-8'))
DOMAIN.update({
'closure_atomic_frames':'model/axioms',
'closure_disjoint_union_9':'model/disjoint-union',
'closure_boundary_quotient':'model/quotient',
'closure_theorem':'model/theorem',
'closure_v1_abjad_7':'number-theory/crosscheck',
'closure_status_ledger':'methodology/status'})
SIGNAL_TYPE.update({
'closure_atomic_frames':'atomic/general frame distinction',
'closure_disjoint_union_9':'9-point prequotient',
'closure_boundary_quotient':'boundary equivalence quotient',
'closure_theorem':'canonical type-closure proof',
'closure_v1_abjad_7':'mod-9 / abjad crosscheck',
'closure_status_ledger':'proof-status ladder'})
PARAMETERS.update({
'closure_atomic_frames':{'frame_axioms':AX17['frame'],'atomic_axioms':AX17['atomic_frame']},
'closure_disjoint_union_9':C7['prequotient'],
'closure_boundary_quotient':{'equivalence':C7['equivalence_relation'],'quotient':C7['quotient']},
'closure_theorem':C7['closure_theorem'],
'closure_v1_abjad_7':{'mod9':C7['mod9'],'abjad':C7['abjad_crosscheck']},
'closure_status_ledger':{
  'proved':['quotient output satisfies A1–A4','|X|=9 → |X/~|=7'],
  'axiom':['atomic |C|=|S|=1'],
  'convention':['Frame typed as one language-object at next level'],
  'open':['derive atomicity','necessity','uniqueness'],
  'meta':C7['meta_observation']}})
VALIDATION.update({
'closure_atomic_frames':{'invariants':['general Frame requires nonempty disjoint C,S and one external boundary class','AtomicFrame additionally requires |C|=|S|=1']},
'closure_disjoint_union_9':{'invariants':['three pairwise-disjoint AtomicFrames yield exactly 9 prequotient points']},
'closure_boundary_quotient':{'invariants':['only bL,bG,bE are identified','three boundary points form one equivalence class','9-(3-1)=7','+1 is the quotient boundary class, not an added point']},
'closure_theorem':{'invariants':['C′ is induced from carrier tags and S′ from structure tags','A1–A4 all pass','output is a general Frame','output is not claimed atomic']},
'closure_v1_abjad_7':{'invariants':['dr(7)=7','T(7)=5','7 belongs to V1=[1,2,4,8,7,5]','canonical abjad ordinal 7 is zay with value 7']},
'closure_status_ledger':{'invariants':['closure theorem is proved inside the stated model','atomicity remains an axiom','necessity and uniqueness remain open','89=F(11) is meta only']}})
RELATIONS.update({
'closure_atomic_frames':{'transforms_to':['closure_disjoint_union_9'],'prerequisites':['abjad_layer_separation']},
'closure_disjoint_union_9':{'transforms_to':['closure_boundary_quotient'],'prerequisites':['closure_atomic_frames']},
'closure_boundary_quotient':{'transforms_to':['closure_theorem','closure_v1_abjad_7'],'prerequisites':['closure_disjoint_union_9']},
'closure_theorem':{'transforms_to':['closure_status_ledger'],'prerequisites':['closure_boundary_quotient']},
'closure_v1_abjad_7':{'transforms_to':['closure_status_ledger'],'prerequisites':['closure_boundary_quotient','abjad_mod9_orbits']},
'closure_status_ledger':{'transforms_to':[],'prerequisites':['closure_theorem','closure_v1_abjad_7']}})


TF18=json.loads((ROOT/'data'/'transformer_frame_ch18.json').read_text(encoding='utf-8'))
DOMAIN.update({
'transformer_frame_correspondence':'model/transformer-frame',
'transformer_seed_geometry':'geometry/hexagonal',
'transformer_signal_system_atlas':'model/signal-system',
'transformer_frame_status':'methodology/status'})
SIGNAL_TYPE.update({
'transformer_frame_correspondence':'audited per-layer architecture correspondence',
'transformer_seed_geometry':'6+1 first-ring geometry',
'transformer_signal_system_atlas':'working type bridge',
'transformer_frame_status':'audited slice status ledger'})
PARAMETERS.update({
'transformer_frame_correspondence':{'frame_correspondence':TF18['frame_correspondence'],'axiom_audit':TF18['axiom_audit'],'status':TF18['status']},
'transformer_seed_geometry':TF18['seed_geometry'],
'transformer_signal_system_atlas':{
    'signal_system_atlas':TF18['signal_system_atlas'],
    'orbit_rotation_bridge':TF18['orbit_rotation_bridge']},
'transformer_frame_status':{
    'self_reference':TF18['self_reference'],
    'ledger':TF18['ledger']}})
VALIDATION.update({
'transformer_frame_correspondence':{'invariants':['C and S correspondence is scoped per-layer','A2 is local to the slice, not global across the network','b selects superposition candidate b1; b2 is next carrier C_{l+1}']},
'transformer_seed_geometry':{'invariants':['one center plus six equal-circle first-ring neighbors totals seven','coordination number is six in the stated hexagonal packing definition']},
'transformer_signal_system_atlas':{'invariants':['signal/system/atlas bridge is stored as a proposal','abjad-to-transformer relation is stored as analogy candidate, not equivalence']},
'transformer_frame_status':{'invariants':['ledger is AUDITED SLICE MODEL','C/S validity is local per layer','orbit bridge remains analogy candidate','self-reference remains provenance observation']}})
RELATIONS.update({
'transformer_frame_correspondence':{'transforms_to':['transformer_signal_system_atlas'],'prerequisites':['closure_theorem']},
'transformer_seed_geometry':{'transforms_to':['transformer_frame_status'],'prerequisites':['closure_boundary_quotient']},
'transformer_signal_system_atlas':{'transforms_to':['transformer_frame_status'],'prerequisites':['transformer_frame_correspondence','abjad_mod9_orbits']},
'transformer_frame_status':{'transforms_to':[],'prerequisites':['transformer_seed_geometry','transformer_signal_system_atlas']}})


CG19=json.loads((ROOT/'data'/'choice_geometry_ch19.json').read_text(encoding='utf-8'))
DOMAIN.update({
'choice_operator_theta':'model/choice-space',
'choice_geometric_chain':'encoding/geometry-chain',
'choice_symbolic_chain':'encoding/symbolic-chain',
'choice_registry':'methodology/choice-registry',
'choice_reflective_closure':'methodology/provenance'})
SIGNAL_TYPE.update({
'choice_operator_theta':'explicit parameterized operator',
'choice_geometric_chain':'vector/raster/byte transformation chain',
'choice_symbolic_chain':'Unicode/language/frame transformation chain',
'choice_registry':'locked model-choice inventory',
'choice_reflective_closure':'reflective provenance closure'})
PARAMETERS.update({
'choice_operator_theta':CG19['operator'],
'choice_geometric_chain':{'steps':CG19['geometric_chain']},
'choice_symbolic_chain':{'steps':CG19['symbolic_chain']},
'choice_registry':{'choices':CG19['choice_registry'],'choice_accounting':CG19['choice_accounting'],'invariants':CG19['invariants']},
'choice_reflective_closure':{'reflection':CG19['reflection'],'closure':CG19['closure']}})
VALIDATION.update({
'choice_operator_theta':{'invariants':['θ is explicit data selecting an admissible operator','fixed X and fixed θ define deterministic execution in the committed generator']},
'choice_geometric_chain':{'invariants':['Base64 byte roundtrip is exact','SVG→PNG rasterization is not generally invertible','PNG→SVG′ vectorization is optional inference']},
'choice_symbolic_chain':{'invariants':['UTF, Σ73, abjad, orbit, Frame and transformer-slice stages remain distinct','each transition is backed by an explicit locked choice or invariant']},
'choice_registry':{'invariants':['six used choice points are explicitly named','theta_bridge is registered ROUTED_OPEN rather than silently omitted','Θ_used \\ Θ_locked = {θ_bridge}','closure_complete remains false because theta_bridge is open by design']},
'choice_reflective_closure':{'invariants':['selected θ/operator/results are serialized back into repository data and hashes','reflection is provenance, not self-causation','reflective closure remains explicitly open while theta_bridge is ROUTED_OPEN']}})
RELATIONS.update({
'choice_operator_theta':{'transforms_to':['choice_geometric_chain','choice_symbolic_chain'],'prerequisites':['transformer_frame_status']},
'choice_geometric_chain':{'transforms_to':['choice_registry'],'prerequisites':['choice_operator_theta','reconstruction_lossiness']},
'choice_symbolic_chain':{'transforms_to':['choice_registry'],'prerequisites':['choice_operator_theta','transformer_frame_correspondence']},
'choice_registry':{'transforms_to':['choice_reflective_closure'],'prerequisites':['choice_geometric_chain','choice_symbolic_chain']},
'choice_reflective_closure':{'transforms_to':[],'prerequisites':['choice_registry']}})


CI20=json.loads((ROOT/'data'/'carrier_invariance_ch20.json').read_text(encoding='utf-8'))
CM20=json.loads((ROOT/'data'/'carrier_invariance_measurement.json').read_text(encoding='utf-8'))
QF20=json.loads((ROOT/'data'/'quotient_factorization_ch20.json').read_text(encoding='utf-8'))
RIG20=json.loads((ROOT/'data'/'reader_independence_gate_ch20.json').read_text(encoding='utf-8'))
IR20=json.loads((ROOT/'data'/'independent_reader_measurement_ch20.json').read_text(encoding='utf-8'))
FI20=json.loads((ROOT/'data'/'independent_reader_fault_injection_ch20.json').read_text(encoding='utf-8'))
RIGM20=json.loads((ROOT/'data'/'reader_independence_gate_measurement_ch20.json').read_text(encoding='utf-8'))
DOMAIN.update({
'carrier_route_invariance':'model/carrier-invariance',
'canonical_discrete_field':'data/canonical-field',
'carrier_substitution_test':'validation/carrier-substitution',
'read_route_operations':'model/read-route',
'carrier_invariance_status':'methodology/status'})
SIGNAL_TYPE.update({
'carrier_route_invariance':'conditional interface-preserving substitution',
'canonical_discrete_field':'canonical JSON state',
'carrier_substitution_test':'hash equality witness',
'read_route_operations':'generation/parsing/tokenization route',
'carrier_invariance_status':'exact/conditional/open ledger'})
PARAMETERS.update({
'carrier_route_invariance':{'terms':CI20['terms'],'formalization':CI20['formalization'],'carrier_classes':CI20['carrier_classes']},
'canonical_discrete_field':{'components':CI20['canonical_field_components'],'measurement':CM20['field'],'canonical_sha256':CM20['canonical_sha256']},
'carrier_substitution_test':{'carrier_A_sha256':CM20['carrier_A_sha256'],'carrier_B_sha256':CM20['carrier_B_sha256'],'deterministic_witness_match':CM20['deterministic_witness_match'],'carrier_content_consumed':CM20['carrier_content_consumed'],'reader_independence_proven':CM20['reader_independence_proven'],'vacuity_status':CM20['vacuity_status'],'scope':CM20['scope']},
'read_route_operations':{'read_route':CI20['read_route'],'self_read':json.loads((ROOT/'data'/'self_read_roundtrip_ch20.json').read_text(encoding='utf-8')),'independent_reader':IR20,'fault_injection':FI20},
'carrier_invariance_status':{'typing':CI20['typing'],'claims':CI20['claims'],'orthogonal_claims':CI20['orthogonal_claims'],'quotient_factorization':QF20,'reader_independence_gate':RIG20,'reader_independence_gate_measurement':RIGM20,'ladder_status':CI20['ladder_status']}})
VALIDATION.update({
'carrier_route_invariance':{'invariants':['model/tokenizer carrier is replaceable only under the declared interface/adapter contract','the committed structural route R is not inferred from model weights']},
'canonical_discrete_field':{'invariants':['D contains only explicitly selected finite/discrete project records','Planck-dataveld is a project term and not a physical Planck-scale claim']},
'carrier_substitution_test':{'invariants':['abstract A/B witnesses reconstruct identical canonical D','canonical JSON SHA-256 hashes are equal','carrier content is not consumed by the current adapter','reader-independence is therefore not proven']},
'read_route_operations':{'invariants':['generation, parsing and tokenization are distinct operators','SVG roundtrip is exact on the explicitly serialized structural subset','P_χ uses a separate raw-text/property route','independent property checks pass without proving full semantic correctness','full semantic self-read remains open']},
'carrier_invariance_status':{'invariants':['canonical quotient-factorization f=i∘b∘p is exact for sets/functions','Ch17 is equivalence-first; Ch20 is function-first','reader-independence requires RI1, RI2, RI3 and independence provenance','full semantic self-read remains open']}})
RELATIONS.update({
'carrier_route_invariance':{'transforms_to':['canonical_discrete_field','read_route_operations'],'prerequisites':['choice_reflective_closure']},
'canonical_discrete_field':{'transforms_to':['carrier_substitution_test'],'prerequisites':['carrier_route_invariance','choice_registry','closure_theorem','transformer_frame_status']},
'carrier_substitution_test':{'transforms_to':['carrier_invariance_status'],'prerequisites':['canonical_discrete_field']},
'read_route_operations':{'transforms_to':['carrier_invariance_status'],'prerequisites':['carrier_route_invariance']},
'carrier_invariance_status':{'transforms_to':[],'prerequisites':['carrier_substitution_test','read_route_operations']}})

def local(tag): return tag.split('}',1)[-1]
def clean(s): return ' '.join((s or '').split())
def frag_hash(g): return hashlib.sha256(ET.tostring(g,encoding='utf-8')).hexdigest()
def math_hash(r):
    p={'concept_id':r['concept_id'],'equation':r['equation'],'parameters':r['parameters'],'validation':r['validation']}
    return hashlib.sha256(canonical_bytes(p)).hexdigest()

root=ET.parse(SVG).getroot()
meta_el=root.find('svg:metadata',NS)
meta=json.loads(meta_el.text) if meta_el is not None and meta_el.text else {}
chapters=meta.get('chapters',[])
groups=[g for g in root.iter() if g.attrib.get('data-concept')]
records=[]
for idx,g in enumerate(groups):
    cid=g.attrib['data-concept']; chapter = 20 if idx >= 98 else (19 if idx >= 93 else (18 if idx >= 89 else (17 if idx >= 83 else (16 if idx >= 77 else (15 if idx >= 71 else (14 if idx >= 65 else idx//5+1))))))
    texts=[clean(t.text) for t in g.iter() if local(t.tag)=='text' and clean(t.text)]
    rec={
      'chapter':chapter,'chapter_title':chapters[chapter-1]['title'],'concept_id':cid,
      'title':texts[0].title() if texts else cid.replace('_',' ').title(),
      'subtitle':texts[1] if len(texts)>1 else '',
      'equation':html.unescape(g.attrib.get('data-equation','')),
      'domain':DOMAIN.get(cid,'systems'),'signal_type':SIGNAL_TYPE.get(cid,'conceptual'),
      'parameters':PARAMETERS.get(cid,{}),'validation':VALIDATION.get(cid,{'invariants':[]}),
      'relations':RELATIONS.get(cid,{'prerequisites':[],'transforms_to':[]}),
      'svg_selector':f'[data-concept="{cid}"]','svg_element_count':sum(1 for _ in g.iter()),
      'svg_text':texts,'svg_fragment_sha256':frag_hash(g)}
    rec['math_signature_sha256']=math_hash(rec); records.append(rec)

atlas={'format_version':'1.9.0','title':meta.get('title','Signals & Systems · Full Visual Atlas'),
       'style':meta.get('style','HEXA_64 / NPN Signal Field'),'default_discrete_frame':meta.get('default_discrete_frame',64),
       'chapter_count':len(chapters),'concept_count':len(records),
       'source_svg':'assets/signals_systems_full_atlas_master.svg','concepts':records}

schema={
'$schema':'https://json-schema.org/draft/2020-12/schema',
'title':'Signals & Systems HEXA_64 concept record',
'type':'object',
'additionalProperties':False,
'required':['chapter','chapter_title','concept_id','title','subtitle','equation','domain','signal_type','parameters','validation','relations','svg_selector','svg_element_count','svg_text','svg_fragment_sha256','math_signature_sha256'],
'properties':{
'chapter':{'type':'integer','minimum':1,'maximum':len(chapters)},
'chapter_title':{'type':'string'},'concept_id':{'type':'string','pattern':'^[a-z0-9_]+$'},
'title':{'type':'string'},'subtitle':{'type':'string'},'equation':{'type':'string'},
'domain':{'type':'string'},'signal_type':{'type':'string'},'parameters':{'type':'object'},
'validation':{'type':'object','required':['invariants'],'properties':{'invariants':{'type':'array','items':{'type':'string'}}},'additionalProperties':True},
'relations':{'type':'object','required':['prerequisites','transforms_to'],
             'properties':{'prerequisites':{'type':'array','items':{'type':'string'}},'transforms_to':{'type':'array','items':{'type':'string'}}},
             'additionalProperties':False},
'svg_selector':{'type':'string'},'svg_element_count':{'type':'integer','minimum':1},
'svg_text':{'type':'array','items':{'type':'string'}},
'svg_fragment_sha256':{'type':'string','pattern':'^[0-9a-f]{64}$'},
'math_signature_sha256':{'type':'string','pattern':'^[0-9a-f]{64}$'}}}

DATA.mkdir(exist_ok=True)
(DATA/'atlas.json').write_text(json.dumps(atlas,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(DATA/'schema.json').write_text(json.dumps(schema,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
with (DATA/'concepts.ndjson').open('w',encoding='utf-8') as f:
    for r in records: f.write(json.dumps(r,ensure_ascii=False,separators=(',',':'))+'\n')
corpus=['# Signals & Systems · HEXA_64 Token Corpus','','Deterministically exported from the master SVG. One section per visual concept.','']
for r in records:
    corpus += [f"## {r['chapter']:02d}.{r['concept_id']} · {r['title']}",f"Chapter: {r['chapter_title']}",
               f"Domain: {r['domain']} · Signal type: {r['signal_type']}",f"Equation: {r['equation'] or 'n/a'}",
               f"Parameters: {json.dumps(r['parameters'],ensure_ascii=False,sort_keys=True)}",
               f"Validation: {'; '.join(r['validation']['invariants']) or 'visual/conceptual invariant'}",
               f"Transforms/links to: {', '.join(r['relations'].get('transforms_to',[])) or 'none'}",
               f"SVG selector: {r['svg_selector']}",'']
(DATA/'token_corpus.md').write_text('\n'.join(corpus),encoding='utf-8')
print(f'Exported {len(records)} concepts to data/')

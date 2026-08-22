# Signals & Systems · HEXA_64 Token Corpus

Deterministically exported from the master SVG. One section per visual concept.

## 01.ct_sinusoid · Continuous-Time Sinusoid
Chapter: Signals & Systems
Domain: continuous-time · Signal type: CT
Equation: x(t)=A sin(ω0 t+φ)
Parameters: {}
Validation: visual/conceptual invariant
Transforms/links to: ctfs
SVG selector: [data-concept="ct_sinusoid"]

## 01.dt_sinusoid · Discrete-Time Sinusoid
Chapter: Signals & Systems
Domain: discrete-time · Signal type: DT
Equation: x[n]=sin(2π·5n/64)
Parameters: {"N": 64, "bin": 5, "period_samples": 12.8}
Validation: 64 samples; DFT support at bins 5 and 59 in full FFT; one-sided dominant bin 5
Transforms/links to: dtfs, dtft_periodic
SVG selector: [data-concept="dt_sinusoid"]

## 01.signal_transformations · Time Operations
Chapter: Signals & Systems
Domain: time-domain · Signal type: conceptual
Equation: x(t), x(t-t0), x(at), x(-t)
Parameters: {}
Validation: visual/conceptual invariant
Transforms/links to: none
SVG selector: [data-concept="signal_transformations"]

## 01.impulse_step · Impulse & Step
Chapter: Signals & Systems
Domain: time-domain · Signal type: conceptual
Equation: u[n], δ[n], u[n]-u[n-1]=δ[n]
Parameters: {}
Validation: visual/conceptual invariant
Transforms/links to: none
SVG selector: [data-concept="impulse_step"]

## 01.system_properties · System Properties
Chapter: Signals & Systems
Domain: systems · Signal type: conceptual
Equation: S{x}=y ; properties ∈ {memoryless, causal, linear, TI, BIBO}
Parameters: {}
Validation: visual/conceptual invariant
Transforms/links to: none
SVG selector: [data-concept="system_properties"]

## 02.convolution_sum · Convolution Sum
Chapter: LTI Systems
Domain: discrete-time · Signal type: DT
Equation: y[n]=Σ x[k]h[n-k]
Parameters: {"N": 64, "decay_constant_samples": 10.0, "rect_length": 12}
Validation: output equals first 64 samples of linear convolution
Transforms/links to: dtft_properties, difference_to_z
SVG selector: [data-concept="convolution_sum"]

## 02.convolution_integral · Convolution Integral
Chapter: LTI Systems
Domain: continuous-time · Signal type: CT
Equation: y(t)=∫x(τ)h(t-τ)dτ
Parameters: {}
Validation: visual/conceptual invariant
Transforms/links to: ctft_convolution
SVG selector: [data-concept="convolution_integral"]

## 02.impulse_response · Impulse Response
Chapter: LTI Systems
Domain: systems · Signal type: conceptual
Equation: y=x*h
Parameters: {}
Validation: visual/conceptual invariant
Transforms/links to: none
SVG selector: [data-concept="impulse_response"]

## 02.step_response · Step Response
Chapter: LTI Systems
Domain: systems · Signal type: conceptual
Equation: s(t)=u*h
Parameters: {}
Validation: visual/conceptual invariant
Transforms/links to: none
SVG selector: [data-concept="step_response"]

## 02.system_equations · Difference / Differential Equations
Chapter: LTI Systems
Domain: systems · Signal type: conceptual
Equation: y[n]-ay[n-1]=bx[n]
Parameters: {}
Validation: visual/conceptual invariant
Transforms/links to: none
SVG selector: [data-concept="system_equations"]

## 03.ctfs · Ct Fourier Series
Chapter: Fourier Series
Domain: frequency-domain · Signal type: CT periodic
Equation: x(t)=Σ ak e^{jkω0t}
Parameters: {}
Validation: visual/conceptual invariant
Transforms/links to: none
SVG selector: [data-concept="ctfs"]

## 03.line_spectrum · Line Spectrum
Chapter: Fourier Series
Domain: frequency-domain · Signal type: conceptual
Equation: ak
Parameters: {}
Validation: visual/conceptual invariant
Transforms/links to: none
SVG selector: [data-concept="line_spectrum"]

## 03.dtfs · Dt Fourier Series
Chapter: Fourier Series
Domain: frequency-domain · Signal type: DT periodic
Equation: x[n]=Σ ak e^{jk(2π/N)n}
Parameters: {"N": 16, "amplitudes": [1.0, 0.5], "bins": [3, 5]}
Validation: nonzero DFT support at ±3 and ±5 modulo 16
Transforms/links to: none
SVG selector: [data-concept="dtfs"]

## 03.gibbs · Gibbs Phenomenon
Chapter: Fourier Series
Domain: time-frequency · Signal type: conceptual
Equation: partial sums of odd harmonics
Parameters: {}
Validation: visual/conceptual invariant
Transforms/links to: none
SVG selector: [data-concept="gibbs"]

## 03.fourier_symmetry · Symmetry Shortcuts
Chapter: Fourier Series
Domain: frequency-domain · Signal type: conceptual
Equation: real x(t) ⇒ a₋k=aₖ*
Parameters: {}
Validation: visual/conceptual invariant
Transforms/links to: none
SVG selector: [data-concept="fourier_symmetry"]

## 04.ctft_rect_sinc · Rect ↔ Sinc
Chapter: Continuous-Time Fourier Transform
Domain: time-frequency · Signal type: CT aperiodic
Equation: rect(t/T) ↔ T sinc(fT)
Parameters: {}
Validation: visual/conceptual invariant
Transforms/links to: none
SVG selector: [data-concept="ctft_rect_sinc"]

## 04.ctft_gaussian · Gaussian ↔ Gaussian
Chapter: Continuous-Time Fourier Transform
Domain: time-frequency · Signal type: CT aperiodic
Equation: e^{-πt²} ↔ e^{-πf²}
Parameters: {}
Validation: visual/conceptual invariant
Transforms/links to: none
SVG selector: [data-concept="ctft_gaussian"]

## 04.ctft_modulation · Modulation Property
Chapter: Continuous-Time Fourier Transform
Domain: frequency-domain · Signal type: conceptual
Equation: x(t)cos(2πfct) ↔ 1/2[X(f-fc)+X(f+fc)]
Parameters: {}
Validation: visual/conceptual invariant
Transforms/links to: none
SVG selector: [data-concept="ctft_modulation"]

## 04.ctft_convolution · Convolution Theorem
Chapter: Continuous-Time Fourier Transform
Domain: time-frequency · Signal type: conceptual
Equation: x*h ↔ XH
Parameters: {}
Validation: visual/conceptual invariant
Transforms/links to: none
SVG selector: [data-concept="ctft_convolution"]

## 04.ctft_properties · Transform Property Map
Chapter: Continuous-Time Fourier Transform
Domain: frequency-domain · Signal type: conceptual
Equation: x(t−t₀) ↔ e^{-j2πft₀}X(f)
Parameters: {}
Validation: visual/conceptual invariant
Transforms/links to: none
SVG selector: [data-concept="ctft_properties"]

## 05.dtft_periodic · Dtft Periodicity
Chapter: Discrete-Time Fourier Transform
Domain: frequency-domain · Signal type: DT
Equation: X(e^{jω})=Σx[n]e^{-jωn}
Parameters: {}
Validation: visual/conceptual invariant
Transforms/links to: none
SVG selector: [data-concept="dtft_periodic"]

## 05.dtft_rect · Finite Sequence Spectrum
Chapter: Discrete-Time Fourier Transform
Domain: time-frequency · Signal type: DT finite
Equation: x[n]=1, 0≤n≤M-1
Parameters: {}
Validation: visual/conceptual invariant
Transforms/links to: none
SVG selector: [data-concept="dtft_rect"]

## 05.dtft_shift · Frequency Shift
Chapter: Discrete-Time Fourier Transform
Domain: frequency-domain · Signal type: conceptual
Equation: x[n]e^{jω0n} ↔ X(e^{j(ω-ω0)})
Parameters: {}
Validation: visual/conceptual invariant
Transforms/links to: none
SVG selector: [data-concept="dtft_shift"]

## 05.dtft_unit_circle · Circular View
Chapter: Discrete-Time Fourier Transform
Domain: z/frequency-domain · Signal type: conceptual
Equation: z=e^{jω}
Parameters: {}
Validation: visual/conceptual invariant
Transforms/links to: none
SVG selector: [data-concept="dtft_unit_circle"]

## 05.dtft_properties · Dtft Property Map
Chapter: Discrete-Time Fourier Transform
Domain: frequency-domain · Signal type: conceptual
Equation: x*h ↔ X(ω)H(ω)
Parameters: {}
Validation: visual/conceptual invariant
Transforms/links to: none
SVG selector: [data-concept="dtft_properties"]

## 06.freq_response · Frequency Response
Chapter: Time / Frequency Characterization
Domain: frequency-domain · Signal type: conceptual
Equation: e^{jωt}→H(jω)e^{jωt}
Parameters: {}
Validation: visual/conceptual invariant
Transforms/links to: none
SVG selector: [data-concept="freq_response"]

## 06.ideal_lpf · Ideal Low-Pass
Chapter: Time / Frequency Characterization
Domain: frequency-domain · Signal type: conceptual
Equation: H(jω)=1 for |ω|<ωc
Parameters: {}
Validation: visual/conceptual invariant
Transforms/links to: none
SVG selector: [data-concept="ideal_lpf"]

## 06.resonance · Resonance
Chapter: Time / Frequency Characterization
Domain: frequency-domain · Signal type: conceptual
Equation: |H(jω)|
Parameters: {}
Validation: visual/conceptual invariant
Transforms/links to: none
SVG selector: [data-concept="resonance"]

## 06.mag_phase · Magnitude & Phase
Chapter: Time / Frequency Characterization
Domain: frequency-domain · Signal type: conceptual
Equation: H=|H|e^{j∠H}
Parameters: {}
Validation: visual/conceptual invariant
Transforms/links to: none
SVG selector: [data-concept="mag_phase"]

## 06.group_delay · Group Delay
Chapter: Time / Frequency Characterization
Domain: frequency-domain · Signal type: conceptual
Equation: τg(ω)=−dφ/dω
Parameters: {}
Validation: visual/conceptual invariant
Transforms/links to: none
SVG selector: [data-concept="group_delay"]

## 07.sampling_train · Impulse-Train Sampling
Chapter: Sampling
Domain: sampling · Signal type: CT→DT
Equation: xs(t)=x(t)Σδ(t-nTs)
Parameters: {"cycles_shown": 2, "sample_count": 17}
Validation: visual/conceptual invariant
Transforms/links to: sampling_replicas
SVG selector: [data-concept="sampling_train"]

## 07.sampling_replicas · Spectral Replicas
Chapter: Sampling
Domain: sampling/frequency-domain · Signal type: conceptual
Equation: Xs(f)=1/Ts ΣX(f-kfs)
Parameters: {}
Validation: visual/conceptual invariant
Transforms/links to: nyquist, aliasing
SVG selector: [data-concept="sampling_replicas"]

## 07.nyquist · Nyquist Condition
Chapter: Sampling
Domain: sampling · Signal type: conceptual
Equation: fs>2B
Parameters: {"condition": "fs > 2B"}
Validation: perfect ideal reconstruction requires sampling rate greater than twice bandwidth
Transforms/links to: none
SVG selector: [data-concept="nyquist"]

## 07.aliasing · Aliasing
Chapter: Sampling
Domain: sampling/frequency-domain · Signal type: conceptual
Equation: f_alias=|f-kfs|
Parameters: {}
Validation: visual/conceptual invariant
Transforms/links to: none
SVG selector: [data-concept="aliasing"]

## 07.reconstruction · Reconstruction Chain
Chapter: Sampling
Domain: sampling · Signal type: conceptual
Equation: x[n] → interpolation → LPF → x̂(t)
Parameters: {}
Validation: visual/conceptual invariant
Transforms/links to: none
SVG selector: [data-concept="reconstruction"]

## 08.dsb_sc · Dsb-Sc Modulation
Chapter: Communication Systems
Domain: communications · Signal type: conceptual
Equation: s(t)=m(t)cos(2πfct)
Parameters: {}
Validation: visual/conceptual invariant
Transforms/links to: none
SVG selector: [data-concept="dsb_sc"]

## 08.sidebands · Sidebands
Chapter: Communication Systems
Domain: communications/frequency-domain · Signal type: conceptual
Equation: M(f±fc)
Parameters: {}
Validation: visual/conceptual invariant
Transforms/links to: none
SVG selector: [data-concept="sidebands"]

## 08.demodulation · Coherent Demodulation
Chapter: Communication Systems
Domain: communications · Signal type: conceptual
Equation: LPF{2s(t)cos(ωct)} = m(t)
Parameters: {}
Validation: visual/conceptual invariant
Transforms/links to: none
SVG selector: [data-concept="demodulation"]

## 08.fdm · Frequency-Division Multiplexing
Chapter: Communication Systems
Domain: communications/frequency-domain · Signal type: conceptual
Equation: Bᵢ ∩ Bⱼ = ∅ for i≠j
Parameters: {}
Validation: visual/conceptual invariant
Transforms/links to: none
SVG selector: [data-concept="fdm"]

## 08.communication_chain · Communication Chain
Chapter: Communication Systems
Domain: communications · Signal type: conceptual
Equation: source → modulation → channel → demodulation → sink
Parameters: {}
Validation: visual/conceptual invariant
Transforms/links to: none
SVG selector: [data-concept="communication_chain"]

## 09.laplace_plane · S-Plane Geometry
Chapter: Laplace Transform
Domain: s-domain · Signal type: conceptual
Equation: X(s)
Parameters: {}
Validation: visual/conceptual invariant
Transforms/links to: none
SVG selector: [data-concept="laplace_plane"]

## 09.laplace_roc · Region Of Convergence
Chapter: Laplace Transform
Domain: s-domain · Signal type: conceptual
Equation: ROC ⊂ ℂ ; poles ∉ ROC
Parameters: {}
Validation: visual/conceptual invariant
Transforms/links to: none
SVG selector: [data-concept="laplace_roc"]

## 09.laplace_causality_stability · Causality & Stability
Chapter: Laplace Transform
Domain: s-domain · Signal type: conceptual
Equation: causal ⇒ ROC right of rightmost pole ; stable ⇒ jℝ ⊂ ROC
Parameters: {}
Validation: visual/conceptual invariant
Transforms/links to: none
SVG selector: [data-concept="laplace_causality_stability"]

## 09.inverse_laplace · Inverse Laplace
Chapter: Laplace Transform
Domain: s-domain · Signal type: conceptual
Equation: 1/(s+a) ↔ e^{-at}u(t)
Parameters: {}
Validation: visual/conceptual invariant
Transforms/links to: none
SVG selector: [data-concept="inverse_laplace"]

## 09.laplace_system_function · System Function
Chapter: Laplace Transform
Domain: s-domain · Signal type: conceptual
Equation: H(s)=Y(s)/X(s)
Parameters: {}
Validation: visual/conceptual invariant
Transforms/links to: none
SVG selector: [data-concept="laplace_system_function"]

## 10.z_plane · Z-Plane Geometry
Chapter: Z-Transform
Domain: z-domain · Signal type: DT
Equation: X(z)
Parameters: {}
Validation: visual/conceptual invariant
Transforms/links to: z_roc_unit_circle, z_to_dtft
SVG selector: [data-concept="z_plane"]

## 10.z_roc_unit_circle · Roc And Unit Circle
Chapter: Z-Transform
Domain: z-domain · Signal type: conceptual
Equation: DTFT exists ⇔ {|z|=1} ⊂ ROC
Parameters: {}
Validation: visual/conceptual invariant
Transforms/links to: none
SVG selector: [data-concept="z_roc_unit_circle"]

## 10.difference_to_z · Difference Equation → H(Z)
Chapter: Z-Transform
Domain: z-domain · Signal type: conceptual
Equation: y[n]-ay[n-1]=x[n]
Parameters: {}
Validation: visual/conceptual invariant
Transforms/links to: none
SVG selector: [data-concept="difference_to_z"]

## 10.z_to_dtft · Frequency Response On Unit Circle
Chapter: Z-Transform
Domain: z/frequency-domain · Signal type: conceptual
Equation: H(e^{jω})
Parameters: {"pole_radius": 0.72, "unit_circle_samples": 24}
Validation: frequency response is H(z) evaluated on |z|=1
Transforms/links to: none
SVG selector: [data-concept="z_to_dtft"]

## 10.pole_radius_angle · Pole Radius & Angle
Chapter: Z-Transform
Domain: z-domain · Signal type: conceptual
Equation: p=re^{jθ}
Parameters: {}
Validation: visual/conceptual invariant
Transforms/links to: none
SVG selector: [data-concept="pole_radius_angle"]

## 11.feedback_loop · Closed-Loop Structure
Chapter: Linear Feedback Systems
Domain: feedback · Signal type: conceptual
Equation: T=G/(1+GH)
Parameters: {}
Validation: closed-loop transfer T=G/(1+GH) for negative feedback
Transforms/links to: sensitivity, closed_loop_poles
SVG selector: [data-concept="feedback_loop"]

## 11.sensitivity · Sensitivity Reduction
Chapter: Linear Feedback Systems
Domain: feedback · Signal type: conceptual
Equation: S=1/(1+GH)
Parameters: {}
Validation: visual/conceptual invariant
Transforms/links to: none
SVG selector: [data-concept="sensitivity"]

## 11.closed_loop_poles · Closed-Loop Poles
Chapter: Linear Feedback Systems
Domain: feedback/s-domain · Signal type: conceptual
Equation: 1+G(s)H(s)=0
Parameters: {}
Validation: visual/conceptual invariant
Transforms/links to: none
SVG selector: [data-concept="closed_loop_poles"]

## 11.root_locus_concept · Pole Movement
Chapter: Linear Feedback Systems
Domain: feedback/s-domain · Signal type: conceptual
Equation: 1 + K G(s)H(s) = 0
Parameters: {}
Validation: visual/conceptual invariant
Transforms/links to: none
SVG selector: [data-concept="root_locus_concept"]

## 11.feedback_tradeoffs · Feedback Story
Chapter: Linear Feedback Systems
Domain: feedback · Signal type: conceptual
Equation: S(s)=1/(1+L(s)) ; T(s)=L(s)/(1+L(s))
Parameters: {}
Validation: visual/conceptual invariant
Transforms/links to: none
SVG selector: [data-concept="feedback_tradeoffs"]

## 12.finite_word_state · 32-Bit Word As Cyclic State
Chapter: Hash Dynamics
Domain: finite-state · Signal type: 32-bit finite word
Equation: ROTR^r(x)
Parameters: {"example_word": "0x6A09E667", "word_bits": 32}
Validation: ROTR is a permutation of 32 indexed bit positions; rotation preserves Hamming weight
Transforms/links to: modular_addition, rotate_xor_mix
SVG selector: [data-concept="finite_word_state"]

## 12.modular_addition · Addition Modulo 2^32
Chapter: Hash Dynamics
Domain: finite-state/modular · Signal type: 32-bit finite word
Equation: (x+y) mod 2^32
Parameters: {"modulus": 4294967296, "result": "0x20000033", "x": "0xF0000011", "y": "0x30000022"}
Validation: state remains in [0,2^32-1]; overflow wraps modulo 2^32
Transforms/links to: compression_round
SVG selector: [data-concept="modular_addition"]

## 12.rotate_xor_mix · Bit Mixing Functions
Chapter: Hash Dynamics
Domain: finite-state/boolean · Signal type: 32-bit finite word
Equation: Ch, Maj, Σ0, Σ1
Parameters: {"sigma0_rotations": [2, 13, 22], "sigma1_rotations": [6, 11, 25], "word_bits": 32}
Validation: Ch, Maj and Σ functions operate bitwise on 32-bit words
Transforms/links to: compression_round
SVG selector: [data-concept="rotate_xor_mix"]

## 12.compression_round · 64-Round Compression State
Chapter: Hash Dynamics
Domain: finite-state/dynamics · Signal type: 8×32-bit state
Equation: S_{t+1}=F(S_t,W_t,K_t) mod 2^32
Parameters: {"rounds": 64, "state_words": 8, "word_bits": 32}
Validation: eight 32-bit state words; 64 repeated rounds; all additions modulo 2^32
Transforms/links to: avalanche_diffusion
SVG selector: [data-concept="compression_round"]

## 12.avalanche_diffusion · Avalanche As Measured State Diffusion
Chapter: Hash Dynamics
Domain: finite-state/diffusion · Signal type: 512-bit input → 256-bit output
Equation: d_H(SHA256(m),SHA256(m⊕1))
Parameters: {"input_bit_difference": 1, "input_bits": 512, "measured_hamming_distance": 133, "output_bits": 256}
Validation: two 512-bit inputs differ by one bit; SHA-256 outputs differ in 133 of 256 bits for the embedded experiment
Transforms/links to: none
SVG selector: [data-concept="avalanche_diffusion"]

## 13.ipv4_word · Ipv4 As One 32-Bit Word
Chapter: Address Geometry
Domain: network/address · Signal type: 32-bit address
Equation: IPv4 ∈ {0,…,2^32−1}
Parameters: {"address": "192.0.2.33", "bits": 32, "hex": "0xC0000221"}
Validation: IPv4 address value is exactly 32 bits; 192.0.2.33 equals 0xC0000221
Transforms/links to: ipv4_mapped_ipv6, address_inclusion
SVG selector: [data-concept="ipv4_word"]

## 13.ipv6_lanes · Ipv6 As A 128-Bit State
Chapter: Address Geometry
Domain: network/address · Signal type: 128-bit address
Equation: IPv6 ∈ {0,…,2^128−1}
Parameters: {"bits": 128, "lanes_32": 4, "text_groups_16": 8}
Validation: IPv6 address value is exactly 128 bits; 128 bits can be partitioned into four 32-bit lanes or eight 16-bit groups
Transforms/links to: ipv4_mapped_ipv6, ipv6_prefix_host
SVG selector: [data-concept="ipv6_lanes"]

## 13.ipv4_mapped_ipv6 · Ipv4-Mapped Ipv6
Chapter: Address Geometry
Domain: network/address · Signal type: 128-bit mapped address
Equation: ::ffff:0:0/96 + IPv4
Parameters: {"ipv4": "192.0.2.33", "ipv4_hex": "0xC0000221", "ipv6": "::ffff:192.0.2.33", "payload_bits": 32, "prefix_bits": 96}
Validation: mapped prefix is 96 bits; low 32 bits equal the IPv4 address value; ::ffff:192.0.2.33 maps 192.0.2.33
Transforms/links to: address_inclusion
SVG selector: [data-concept="ipv4_mapped_ipv6"]

## 13.ipv6_prefix_host · Prefix As Measurement Frame
Chapter: Address Geometry
Domain: network/address · Signal type: 128-bit prefix/host decomposition
Equation: IPv6 = prefix_64 || interface_64
Parameters: {"example_prefix_length": 64, "interface_bits": 64, "prefix_bits": 64}
Validation: a /64 split contains 64 prefix bits and 64 remaining address bits
Transforms/links to: none
SVG selector: [data-concept="ipv6_prefix_host"]

## 13.address_inclusion · 32 → 128 Inclusion
Chapter: Address Geometry
Domain: network/address · Signal type: 32→128-bit embedding
Equation: ι(x)=(0,0,0x0000ffff,x)
Parameters: {"payload_word": "0xC0000221", "prefix_words": ["0x00000000", "0x00000000", "0x0000FFFF"]}
Validation: embedding preserves the 32-bit payload exactly; mapped representation uses a fixed 96-bit prefix
Transforms/links to: none
SVG selector: [data-concept="address_inclusion"]

## 14.vector_test_object · Vector Space
Chapter: Encoding Geometry
Domain: encoding/vector · Signal type: vector geometry
Equation: geometry in R² before raster sampling
Parameters: {"coordinate_example": 12.4387, "viewBox": [0, 0, 160, 96]}
Validation: source SVG uses real-valued coordinates; test object viewBox is exactly 160×96
Transforms/links to: raster_frame_boundary
SVG selector: [data-concept="vector_test_object"]

## 14.raster_frame_boundary · Frame Boundary
Chapter: Encoding Geometry
Domain: encoding/raster · Signal type: 160×96 raster
Equation: R² → Z² at 1-pixel resolution
Parameters: {"cell_example": 12, "coordinate_example": 12.4387, "height": 96, "pixel_frame": 1, "width": 160}
Validation: CairoSVG raster is exactly 160×96; x=12.4387 is represented within pixel cell i=12 at unit raster frame
Transforms/links to: png_byte_space
SVG selector: [data-concept="raster_frame_boundary"]

## 14.png_byte_space · Byte Space
Chapter: Encoding Geometry
Domain: encoding/bytes · Signal type: PNG byte stream
Equation: raw = PNG bytes
Parameters: {"png_length_bytes": 2239, "png_sha256": "411ea26035897702802e016e8785c8a9efaa28fe023a4fba8390f06c71bba89c"}
Validation: raw bytes are a valid PNG stream; PNG byte length and SHA-256 are recomputed from the actual raster
Transforms/links to: base64_frame_shift
SVG selector: [data-concept="png_byte_space"]

## 14.base64_frame_shift · Base64 Frame Shift
Chapter: Encoding Geometry
Domain: encoding/base64 · Signal type: 24-bit repartition
Equation: 24 bits = 3 bytes = 4 Base64 symbols
Parameters: {"base64_length_chars": 2988, "base64_sha256": "f5a98127add7a1530bedbaa901ad523fd807b9fb502cc286a63d719e64500f99", "byte_bits": 8, "group_bits": 24, "symbol_bits": 6}
Validation: Base64 decode(encode(raw)) equals raw; 3×8 bits equals 4×6 bits; encoded length equals ceil(raw/3)×4
Transforms/links to: base64_char_space, reconstruction_lossiness
SVG selector: [data-concept="base64_frame_shift"]

## 14.base64_char_space · Char Space
Chapter: Encoding Geometry
Domain: encoding/base64 · Signal type: 64-symbol alphabet
Equation: index ∈ {0,…,63} ↔ Base64 alphabet
Parameters: {"alphabet_size": 64, "first_16_chars": "iVBORw0KGgoAAAAN", "first_16_indices": [34, 21, 1, 14, 17, 48, 52, 10, 6, 32, 40, 0, 0, 0, 0, 13]}
Validation: Base64 alphabet contains exactly 64 unique symbols; every non-padding symbol maps uniquely to index 0…63
Transforms/links to: reconstruction_lossiness
SVG selector: [data-concept="base64_char_space"]

## 14.reconstruction_lossiness · Reconstruction + Lossiness
Chapter: Encoding Geometry
Domain: encoding/reconstruction · Signal type: exact encoding / lossy geometry
Equation: decode(encode(PNG))=PNG; SVG→PNG→SVG'≠identity
Parameters: {"encoding_roundtrip": "exact", "raster_to_vector": "lossy/inferred"}
Validation: Base64 roundtrip is byte-exact; SVG→PNG sampling does not retain original vector primitive identity
Transforms/links to: none
SVG selector: [data-concept="reconstruction_lossiness"]

## 15.utf73_field · 73-State Unicode Field
Chapter: Canonical Field Encoding
Domain: encoding/unicode · Signal type: 73-state symbol field
Equation: |Σ| = 6×12+1 = 73
Parameters: {"construction": "6×12+1", "states": 73}
Validation: exactly 73 states; all states are unique Unicode strings
Transforms/links to: utf73_codepoints, utf73_utf8
SVG selector: [data-concept="utf73_field"]

## 15.utf73_codepoints · Codepoint Composition
Chapter: Canonical Field Encoding
Domain: encoding/unicode · Signal type: Unicode code-point sequences
Equation: state = consonant || optional sign
Parameters: {"inherent_codepoints": 1, "marked_codepoints": 2, "shunya_codepoints": 1}
Validation: slot 12 uses U+0902 DEVANAGARI SIGN ANUSVARA; śūnya is an abstract nil state displayed with U+00B7 MIDDLE DOT
Transforms/links to: utf73_utf8
SVG selector: [data-concept="utf73_codepoints"]

## 15.utf73_utf8 · Utf-8 Byte Geometry
Chapter: Canonical Field Encoding
Domain: encoding/utf8 · Signal type: UTF-8 byte sequences
Equation: Unicode scalar values → RFC 3629 UTF-8 bytes
Parameters: {"devanagari_bytes_per_codepoint": 3, "middle_dot_bytes": 2, "variable_width": true}
Validation: every state UTF-8 encodes and decodes exactly; UTF-8 width is variable across the field
Transforms/links to: utf73_fixed_point
SVG selector: [data-concept="utf73_utf8"]

## 15.utf73_fixed_point · Reference-Model Identity
Chapter: Canonical Field Encoding
Domain: encoding/quotient · Signal type: reference-model identity
Equation: E₇₃(D₇₃(s)) = s
Parameters: {"decoder": "state index", "encoder": "n mod 73", "fixed_points": 73, "model": "reference quotient only"}
Validation: reference-model identity only: E(n)=n mod 73 and D(s)=state index imply E(D(s))=s for all 73 states
Transforms/links to: utf73_basins
SVG selector: [data-concept="utf73_fixed_point"]

## 15.utf73_basins · Measured Rgb24 Basins
Chapter: Canonical Field Encoding
Domain: encoding/quotient · Signal type: measured RGB24 HSV basins
Equation: sum basin_i = 2^24
Parameters: {"input_states": 16777216, "max": 633241, "min": 1, "shunya": 1, "sum": 16777216}
Validation: live RGB24→HSV→Σ73 encoder is exhaustively counted over all 2^24 colors; measured basin sum equals 2^24; śūnya basin contains black only
Transforms/links to: utf73_vs_base64
SVG selector: [data-concept="utf73_basins"]

## 15.utf73_vs_base64 · Base64 Vs Σ₇₃ Projection
Chapter: Canonical Field Encoding
Domain: encoding/comparison · Signal type: finite-code comparison
Equation: 64^4 = 2^24; 73 ∤ 2^24
Parameters: {"base64_states": 64, "log2_73": 6.189824558880018, "utf73_states": 73}
Validation: 64^4 = 2^24 gives exact Base64 24-bit repartition; 73 does not divide 2^24
Transforms/links to: none
SVG selector: [data-concept="utf73_vs_base64"]

## 16.abjad_linear_carrier · Linear Carrier · Utf-8
Chapter: Abjad Field Geometry
Domain: encoding/utf8 · Signal type: ordered Unicode/UTF-8 carrier
Equation: c₁,c₂,…,cₙ · UTF-8 is carrier, not the abjad invariant
Parameters: {"expected_ayahs": 6236, "lossless": true, "order_preserved": true}
Validation: UTF-8/Unicode carrier preserves ordered text; fixture SHA identifies exact carrier bytes once locked
Transforms/links to: abjad_cultural_mapping
SVG selector: [data-concept="abjad_linear_carrier"]

## 16.abjad_cultural_mapping · Direct Abjad Mapping
Chapter: Abjad Field Geometry
Domain: encoding/abjad · Signal type: 28-letter direct numeric mapping
Equation: letter → v ∈ {1…9,10…90,100…1000}
Parameters: {"excluded": "charCode % 28", "letters": 28, "mapping_semantics": "direct character lookup", "values": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]}
Validation: 28 unique Arabic letters map directly to 28 classical abjad values; charCode modulo indexing is excluded
Transforms/links to: abjad_mod9_orbits, abjad_corpus_fixture
SVG selector: [data-concept="abjad_cultural_mapping"]

## 16.abjad_mod9_orbits · Pure Mathematics · Mod-9 Dynamics
Chapter: Abjad Field Geometry
Domain: number-theory/dynamics · Signal type: 9-state finite dynamical system
Equation: dr(v)=1+((v−1) mod 9); T(r)=dr(2r)
Parameters: {"cycles": {"V1": [1, 2, 4, 8, 7, 5], "V3": [3, 6], "V9": [9]}, "digital_root": "dr(v)=1+((v-1) mod 9)", "doubling_map": "T(x)=dr(2x)"}
Validation: T(r)=dr(2r) yields V1=[1,2,4,8,7,5], V3=[3,6], V9=[9] exactly
Transforms/links to: abjad_empirical_measure
SVG selector: [data-concept="abjad_mod9_orbits"]

## 16.abjad_corpus_fixture · Corpus Fixture + Normalization
Chapter: Abjad Field Geometry
Domain: corpus/provenance · Signal type: 6236-ayah locked corpus boundary
Equation: UTF-8 fixture → normalize → 28 letters → direct values
Parameters: {"fixture": "corpora/quran_uthmani/quran.jsonl", "normalization": {"canonicalizations": {"آ": "ا", "أ": "ا", "ؤ": "و", "إ": "ا", "ئ": "ي", "ة": "ه", "ى": "ي", "ٱ": "ا", "ی": "ي"}, "other_characters": "ignored unless present in the 28-letter direct mapping", "standalone_hamza_U+0621": "ignored unless an explicit corpus spec chooses a value", "strip_combining_marks": true, "strip_tatweel_U+0640": true, "unicode_form": "NFC"}, "status": "fixture_missing"}
Validation: corpus statistics require an exact 6236-ayah fixture; normalization rules are explicit and deterministic; no silent corpus substitution
Transforms/links to: abjad_empirical_measure
SVG selector: [data-concept="abjad_corpus_fixture"]

## 16.abjad_empirical_measure · Empirical Orbit Statistic
Chapter: Abjad Field Geometry
Domain: corpus/statistics · Signal type: ayah-level empirical statistic
Equation: candidate: one orbit-class frequency = 2050/6236
Parameters: {"candidate_only": {"count": 2050, "gap_fraction": "43/9354", "total": 6236}, "claim": "candidate is not marked reproduced until the exact fixture is present and measured", "fixture": "corpora/quran_uthmani/quran.jsonl", "status": "fixture_missing"}
Validation: per ayah: normalize → direct abjad sum → digital root → V1/V3/V9 orbit class; candidate arithmetic 1/3−2050/6236=43/9354 is exact; target orbit class remains unresolved until the prior script or a locked fixture uniquely identifies the 2050 count; candidate is not a reproduced corpus result while fixture is missing
Transforms/links to: abjad_layer_separation
SVG selector: [data-concept="abjad_empirical_measure"]

## 16.abjad_layer_separation · Three Layers · Three Statuses
Chapter: Abjad Field Geometry
Domain: methodology · Signal type: epistemic layer model
Equation: carrier ≠ mapping ≠ invariant ≠ empirical result
Parameters: {"carrier": "lossless", "empirical": "pending exact fixture", "mapping": "explicit choice", "pure_math": "exact"}
Validation: pure math, cultural mapping, carrier, and empirical result retain separate statuses
Transforms/links to: none
SVG selector: [data-concept="abjad_layer_separation"]

## 17.closure_atomic_frames · Atomic Vs General Frame
Chapter: 7-Closure
Domain: model/axioms · Signal type: atomic/general frame distinction
Equation: AtomicFrame = Frame + |C|=|S|=1
Parameters: {"atomic_axioms": {"axioms": {"AT1": "|C| = 1", "AT2": "|S| = 1"}, "cardinality": 3, "signature": "AtomicFrame = Frame + atomicity"}, "frame_axioms": {"axioms": {"A1": "C and S are non-empty finite sets", "A2": "C ∩ S = ∅", "A3": "b ∉ C ∪ S", "A4": "b is the unique boundary-equivalence class representing the identified 0/1 boundary"}, "signature": "Frame = (C,S,b)"}}
Validation: general Frame requires nonempty disjoint C,S and one external boundary class; AtomicFrame additionally requires |C|=|S|=1
Transforms/links to: closure_disjoint_union_9
SVG selector: [data-concept="closure_atomic_frames"]

## 17.closure_disjoint_union_9 · Pre-Quotient · 9 Points
Chapter: 7-Closure
Domain: model/disjoint-union · Signal type: 9-point prequotient
Equation: X = ⊔ᵢ(Cᵢ ⊔ Sᵢ ⊔ {bᵢ}); |X|=3×3=9
Parameters: {"cardinality": 9, "formula": "3×3=9", "points": ["L:C", "L:S", "L:b", "G:C", "G:S", "G:b", "E:C", "E:S", "E:b"]}
Validation: three pairwise-disjoint AtomicFrames yield exactly 9 prequotient points
Transforms/links to: closure_boundary_quotient
SVG selector: [data-concept="closure_disjoint_union_9"]

## 17.closure_boundary_quotient · Boundary Quotient · 9 → 7
Chapter: 7-Closure
Domain: model/quotient · Signal type: boundary equivalence quotient
Equation: Q=X/~ ; bL~bG~bE ; |Q|=9-(3-1)=7
Parameters: {"equivalence": {"boundary_identification": "L:b ~ G:b ~ E:b", "classes_removed_by_identification": 2, "nonboundary_rule": "singleton equivalence classes"}, "quotient": {"C_prime": ["E:C", "G:C", "L:C"], "S_prime": ["E:S", "G:S", "L:S"], "boundary": "b", "boundary_class": ["E:b", "G:b", "L:b"], "cardinality": 7, "formula": "9-(3-1)=7", "points": ["E:C", "E:S", "G:C", "G:S", "L:C", "L:S", "b"]}}
Validation: only bL,bG,bE are identified; three boundary points form one equivalence class; 9-(3-1)=7; +1 is the quotient boundary class, not an added point
Transforms/links to: closure_theorem, closure_v1_abjad_7
SVG selector: [data-concept="closure_boundary_quotient"]

## 17.closure_theorem · Closure Theorem
Chapter: 7-Closure
Domain: model/theorem · Signal type: canonical type-closure proof
Equation: ⊕(F₁,F₂,F₃)=(C′,S′,b) ⊨ A1–A4
Parameters: {"axiom_checks": {"A1_nonempty": true, "A2_disjoint": true, "A3_boundary_external": true, "A4_unique_boundary_class": true}, "canonical_partition": true, "passes": true, "proof_steps": ["C' is the quotient image of the disjoint union of the three carrier sets.", "S' is the quotient image of the disjoint union of the three structure sets.", "Only boundary points are identified, so C' and S' remain disjoint.", "The common boundary class b is not an element of C' or S'.", "There is exactly one boundary class after quotienting.", "Therefore (C',S',b) satisfies the general Frame axioms."]}
Validation: C′ is induced from carrier tags and S′ from structure tags; A1–A4 all pass; output is a general Frame; output is not claimed atomic
Transforms/links to: closure_status_ledger
SVG selector: [data-concept="closure_theorem"]

## 17.closure_v1_abjad_7 · Seven Crosschecks
Chapter: 7-Closure
Domain: number-theory/crosscheck · Signal type: mod-9 / abjad crosscheck
Equation: |Q|=7; dr(7)=7; T(7)=5; 7∈V1; ز↦7
Parameters: {"abjad": {"letter": "ز", "name": "zay", "ordinal": 7, "value": 7}, "mod9": {"T7": 5, "V1": [1, 2, 4, 8, 7, 5], "digital_root_7": 7, "orbit": "V1"}}
Validation: dr(7)=7; T(7)=5; 7 belongs to V1=[1,2,4,8,7,5]; canonical abjad ordinal 7 is zay with value 7
Transforms/links to: closure_status_ledger
SVG selector: [data-concept="closure_v1_abjad_7"]

## 17.closure_status_ledger · Theorem Status Ledger
Chapter: 7-Closure
Domain: methodology/status · Signal type: proof-status ladder
Equation: construct → consistency → type closure → necessity? → uniqueness?
Parameters: {"axiom": ["atomic |C|=|S|=1"], "convention": ["Frame typed as one language-object at next level"], "meta": {"visual_field_count_89": "Fibonacci F(11); recorded as meta-observation only, not an invariant"}, "open": ["derive atomicity", "necessity", "uniqueness"], "proved": ["quotient output satisfies A1–A4", "|X|=9 → |X/~|=7"]}
Validation: closure theorem is proved inside the stated model; atomicity remains an axiom; necessity and uniqueness remain open; 89=F(11) is meta only
Transforms/links to: none
SVG selector: [data-concept="closure_status_ledger"]

## 18.transformer_frame_correspondence · Frame In The Transformer
Chapter: Transformer Frame
Domain: model/transformer-frame · Signal type: audited per-layer architecture correspondence
Equation: Cₗ↔xₗ ; Sₗ↔Fₗ(xₗ) ; b↔merge event · per-layer
Parameters: {"axiom_audit": {"A2_C_intersection_S": "holds only on the per-layer snapshot typing; globally the next carrier contains prior layer contributions", "network_interpretation": "the transformer is a stack of Frame slices linked by x_{l+1}=x_l+F_l(x_l)", "scope": "local/per-layer, not whole-network"}, "frame_correspondence": [{"A2_scope": "local snapshot", "atlas": "C · carrier", "audit_status": "VALID", "proposal": "C_l ↔ residual carrier at one transformer layer", "scope": "per-layer", "transformer": "residual stream state x_l"}, {"A2_scope": "local snapshot", "atlas": "S · structure", "audit_status": "VALID", "proposal": "S_l ↔ layer-local transformation contribution", "scope": "per-layer", "transformer": "layer contribution F_l(x_l), including attention/FFN and positional structure where present"}, {"atlas": "b · boundary", "audit_status": "VALID WITH DISAMBIGUATION", "b_candidates": {"b1": "superposition x_l + F_l(x_l) as the boundary identification event", "b2": "new carrier state x_{l+1}=x_l+F_l(x_l)"}, "proposal": "b ↔ b1: superposition/merge point", "rejected_candidate": "b2 is the next layer's carrier C_{l+1}, not the boundary point itself", "scope": "per-layer boundary event", "selected_candidate": "b1", "transformer": "residual merge event x_l + F_l(x_l)"}], "status": "AUDITED SLICE MODEL"}
Validation: C and S correspondence is scoped per-layer; A2 is local to the slice, not global across the network; b selects superposition candidate b1; b2 is next carrier C_{l+1}
Transforms/links to: transformer_signal_system_atlas
SVG selector: [data-concept="transformer_frame_correspondence"]

## 18.transformer_seed_geometry · Seed Geometry · 6 + 1
Chapter: Transformer Frame
Domain: geometry/hexagonal · Signal type: 6+1 first-ring geometry
Equation: 1 center + 6 first-ring points = 7
Parameters: {"audit_status": "EXACT under the stated circle-packing definition", "center": 1, "coordination_number": 6, "first_ring": 6, "formalization": "equal-circle hexagonal first ring around one center", "identity": "1+6=7", "name_in_chapter": "Seed / hexagonal first-ring geometry", "total": 7}
Validation: one center plus six equal-circle first-ring neighbors totals seven; coordination number is six in the stated hexagonal packing definition
Transforms/links to: transformer_frame_status
SVG selector: [data-concept="transformer_seed_geometry"]

## 18.transformer_signal_system_atlas · Signal → System → Atlas
Chapter: Transformer Frame
Domain: model/signal-system · Signal type: working type bridge
Equation: signal → system → atlas · proposed type correspondence
Parameters: {"orbit_rotation_bridge": {"abjad": "finite V1/V3/V9 cycles", "audit_status": "ANALOGY CANDIDATE", "relation": "analogy candidate; equivalence not asserted in this working chapter", "transformer": "rotational/interaction structures proposal"}, "signal_system_atlas": {"atlas": "enclosing representational field proposal", "audit_status": "pending", "signal": "carrier / embedding-state proposal", "system": "transformation stack proposal"}}
Validation: signal/system/atlas bridge is stored as a proposal; abjad-to-transformer relation is stored as analogy candidate, not equivalence
Transforms/links to: transformer_frame_status
SVG selector: [data-concept="transformer_signal_system_atlas"]

## 18.transformer_frame_status · Audited Slice Status Ledger
Chapter: Transformer Frame
Domain: methodology/status · Signal type: audited slice status ledger
Equation: AUDITED SLICE MODEL
Parameters: {"ledger": {"analogy": ["finite abjad orbits ↔ transformer rotational/interaction structures"], "current_status": "AUDITED SLICE MODEL", "exact": ["per-layer residual update x_{l+1}=x_l+F_l(x_l) as the working slice equation", "1 center + 6 equal-circle first-ring neighbors = 7 in the stated hexagonal packing model"], "local_only": ["A2: C∩S=∅ is a per-layer typing distinction, not a global network separation"], "observation": ["the atlas is developed with a transformer-based language model"], "rejected": ["b2 = x_{l+1} as boundary; x_{l+1} is instead C_{l+1}"], "valid_mapping": ["C_l ↔ residual carrier x_l", "S_l ↔ layer-local contribution F_l(x_l)", "b ↔ b1 superposition/merge event"]}, "self_reference": {"interpretation": "the map is produced by a system being mapped", "observation": "the atlas is being developed with a transformer-based language model", "status": "PROVENANCE OBSERVATION"}}
Validation: ledger is AUDITED SLICE MODEL; C/S validity is local per layer; orbit bridge remains analogy candidate; self-reference remains provenance observation
Transforms/links to: none
SVG selector: [data-concept="transformer_frame_status"]

## 19.choice_operator_theta · Choice Space Θ
Chapter: Choice Geometry
Domain: model/choice-space · Signal type: explicit parameterized operator
Equation: F_θ : X → Y ; θ∈Θ
Parameters: {"choice_is_not": "randomness by definition", "equation": "F_θ : X → Y, θ ∈ Θ", "meaning": "θ selects one admissible structure/mapping; once θ and X are fixed, execution is deterministic"}
Validation: θ is explicit data selecting an admissible operator; fixed X and fixed θ define deterministic execution in the committed generator
Transforms/links to: choice_geometric_chain, choice_symbolic_chain
SVG selector: [data-concept="choice_operator_theta"]

## 19.choice_geometric_chain · Geometric Chain
Chapter: Choice Geometry
Domain: encoding/geometry-chain · Signal type: vector/raster/byte transformation chain
Equation: SVG --R--> PNG --B--> Base64 --B⁻¹--> PNG ; PNG --V--> SVG′
Parameters: {"steps": [{"from": "SVG vector", "invertibility": "generally lossy", "operator": "R", "status": "deterministic for fixed renderer/settings", "to": "PNG raster"}, {"from": "PNG bytes", "invertibility": "bijective on bytes with B^-1", "operator": "B", "status": "exact deterministic encoding", "to": "Base64 symbols"}, {"from": "Base64 symbols", "invertibility": "exact", "operator": "B^-1", "status": "exact deterministic decoding", "to": "PNG bytes"}, {"from": "PNG raster", "invertibility": "not exact in general", "operator": "V", "status": "inference/vectorization if used", "to": "SVG' vector"}]}
Validation: Base64 byte roundtrip is exact; SVG→PNG rasterization is not generally invertible; PNG→SVG′ vectorization is optional inference
Transforms/links to: choice_registry
SVG selector: [data-concept="choice_geometric_chain"]

## 19.choice_symbolic_chain · Symbolic Chain
Chapter: Choice Geometry
Domain: encoding/symbolic-chain · Signal type: Unicode/language/frame transformation chain
Equation: UTF → Σ73 → abjad → V-orbits → Frame → transformer slice
Parameters: {"steps": [{"choice": "utf73_field + RGB24/HSV encoder specification", "from": "Unicode/UTF-8 carrier", "to": "Σ73 Sanskrit field"}, {"choice": "classical 28-letter direct table + normalization policy", "from": "Σ73 / Unicode field", "to": "Arabic abjad values"}, {"choice": "dr and T(r)=dr(2r) invariant", "from": "abjad values", "to": "V1/V3/V9"}, {"choice": "frame axioms + quotient construction", "from": "orbit/frame layer", "to": "Frame (C,S,b)"}, {"choice": "audited per-layer C_l/S_l/b1 correspondence", "from": "Frame", "to": "transformer slice"}]}
Validation: UTF, Σ73, abjad, orbit, Frame and transformer-slice stages remain distinct; each transition is backed by an explicit locked choice or invariant
Transforms/links to: choice_registry
SVG selector: [data-concept="choice_symbolic_chain"]

## 19.choice_registry · Choice Registry
Chapter: Choice Geometry
Domain: methodology/choice-registry · Signal type: locked model-choice inventory
Equation: Θ_used = {θ_raster, θ_utf73, θ_bridge, θ_abjad, θ_atomic, θ_transformer}
Parameters: {"choice_accounting": {"closure_complete": false, "closure_semantics": "OPEN_BY_DESIGN", "completion_condition": "not applicable: theta_bridge is intentionally ROUTED_OPEN; closure_complete remains false by design", "invariant": "Θ_used \\ Θ_locked = {θ_bridge}", "locked_choice_ids": ["theta_raster", "theta_utf73", "theta_abjad", "theta_atomic", "theta_transformer"], "pending_choice_ids": [], "routed_open_choice_ids": ["theta_bridge"], "unlocked_by_design_choice_ids": ["theta_bridge"], "used_choice_ids": ["theta_raster", "theta_utf73", "theta_bridge", "theta_abjad", "theta_atomic", "theta_transformer"]}, "choices": [{"chapter": 14, "id": "theta_raster", "kind": "choice/configuration", "locked_by": "generator + CairoSVG version", "parameter": "renderer/settings for SVG→PNG"}, {"chapter": 15, "id": "theta_utf73", "kind": "model choice", "locked_by": "data/utf73_field.json", "parameter": "canonical 73-state alphabet and HSV binning"}, {"A2_relation": "keeps the two modeled systems distinct; no identification/bijection is asserted", "chapter": 19, "default_route_prefix": "0.0.0.0/0", "endpoint": "0.0.0.0", "endpoint_network_status": "IPv4 unspecified address", "id": "theta_bridge", "kind": "inter-system routed-open relation", "lock_policy": "NONE_BY_DESIGN", "locked_by": null, "nidra_sunya_semantics": "project-defined symbolic reading of open/null position; not a networking or physics invariant", "null_island_note": "Null Island means geographic coordinates 0°N, 0°E; it is not the IPv4 address 0.0.0.0", "parameter": "Σ73 ↔ abjad open bridge", "project_semantics": "open endpoint / route-without-value between distinct systems; no Σ73→abjad value assignment is asserted", "status": "ROUTED_OPEN"}, {"chapter": 16, "id": "theta_abjad", "kind": "cultural/model choice", "locked_by": "data/abjad_field.json", "parameter": "28-letter classical abjad mapping + normalization"}, {"chapter": 17, "id": "theta_atomic", "kind": "axiom", "locked_by": "data/language_frame_axioms.json", "parameter": "AtomicFrame |C|=|S|=1"}, {"chapter": 18, "id": "theta_transformer", "kind": "audited model mapping", "locked_by": "data/transformer_frame_ch18.json", "parameter": "per-layer C_l/S_l/b1 mapping"}], "invariants": ["Base64 byte roundtrip is exact", "committed deterministic generators reproduce byte-identical generated assets", "Chapter 17 quotient theorem produces a 7-point general Frame from three atomic inputs", "Chapter 18 scope is per-layer and A2 is local", "changing θ is permitted only by changing an explicit locked choice record", "every non-derived choice used by the chain must have a registry entry", "Θ_used \\ Θ_locked = {θ_bridge} until the bridge specification is committed", "every non-derived choice used by the chain has a registry entry", "Θ_used \\ Θ_locked = {θ_bridge}", "theta_bridge is ROUTED_OPEN and unlocked by design, not awaiting a later lock", "closure_complete remains false because the bridge is structurally open, not because a specification is missing", "0.0.0.0 is recorded as the IPv4 unspecified address; 0.0.0.0/0 is separately recorded as the default route prefix"]}
Validation: six used choice points are explicitly named; theta_bridge is registered ROUTED_OPEN rather than silently omitted; Θ_used \ Θ_locked = {θ_bridge}; closure_complete remains false because theta_bridge is open by design
Transforms/links to: choice_reflective_closure
SVG selector: [data-concept="choice_registry"]

## 19.choice_reflective_closure · Reflective Closure
Chapter: Choice Geometry
Domain: methodology/provenance · Signal type: reflective provenance closure
Equation: θ → F_θ → F_θ(X) → encode(θ,F_θ,results)
Parameters: {"closure": {"open_port": "theta_bridge", "pending_gap": null, "pipeline": "carrier → encoding → geometry → finite field → language → dynamics → quotient frame → transformer slice → choice operator → reflection", "role": "audit-envelope closure chapter with one intentional inter-system open port", "status": "OPEN_BY_DESIGN · theta_bridge is ROUTED_OPEN"}, "reflection": {"claim": "the selected operator and its parameters are serialized back into the resulting repository as data, hashes, equations and validation records", "equation": "θ → F_θ → F_θ(X) → encode(θ,F_θ,results)", "self_reference_boundary": "this is reflective provenance, not a claim that θ causes itself", "status": "exact project provenance property when the generator reads the same committed choice records it emits/validates"}}
Validation: selected θ/operator/results are serialized back into repository data and hashes; reflection is provenance, not self-causation; reflective closure remains explicitly open while theta_bridge is ROUTED_OPEN
Transforms/links to: none
SVG selector: [data-concept="choice_reflective_closure"]

## 20.carrier_route_invariance · Carrier → Route → Canonical Field
Chapter: Carrier Invariance
Domain: model/carrier-invariance · Signal type: conditional interface-preserving substitution
Equation: (M,τ) → adapter → R → D
Parameters: {"carrier_classes": [{"adapter": "canonical discrete-field adapter", "description": "abstract compatible model/tokenizer pair (M1,τ1)", "id": "carrier_A", "status": "test fixture / interface witness, not an actual model execution"}, {"adapter": "canonical discrete-field adapter", "description": "abstract compatible model/tokenizer pair (M2,τ2)", "id": "carrier_B", "status": "test fixture / interface witness, not an actual model execution"}], "formalization": {"canonical_test": "sha256(canonical(D_A)) = sha256(canonical(D_B))", "carrier_route": "(M,τ) → adapter → R → D", "invariance": "R_(M1,τ1) ⇓ D ∧ R_(M2,τ2) ⇓ D", "scope": "conditional on both carriers satisfying the same declared text/JSON interface and adapter contract"}, "terms": {"D": "canonical discrete project state selected for carrier-invariance checking", "M": "model/runtime carrier; replaceable substrate", "R": "committed structural route: code, chapters, mappings, validators", "planck_data_field": "project term for canonical D; not a physical Planck-scale claim", "tau": "tokenizer/interface configuration associated with the carrier"}}
Validation: model/tokenizer carrier is replaceable only under the declared interface/adapter contract; the committed structural route R is not inferred from model weights
Transforms/links to: canonical_discrete_field, read_route_operations
SVG selector: [data-concept="carrier_route_invariance"]

## 20.canonical_discrete_field · Canonical Discrete Field D
Chapter: Carrier Invariance
Domain: data/canonical-field · Signal type: canonical JSON state
Equation: D = canonical{orbits,7,Θ,status,slice}
Parameters: {"canonical_sha256": "1343bb5bfd09cb9367c0e7778a4eabf57f256bc35dcb9d13adaff706c07fe318", "components": ["mod9_orbits", "closure_7_cardinality", "choice_accounting", "chapter19_open_bridge", "chapter18_slice_scope"], "measurement": {"chapter18_slice_scope": {"scope": "local/per-layer, not whole-network", "selected_boundary": "b1", "status": "AUDITED SLICE MODEL"}, "chapter19_open_bridge": {"default_route_prefix": "0.0.0.0/0", "endpoint": "0.0.0.0", "endpoint_network_status": "IPv4 unspecified address", "id": "theta_bridge", "kind": "inter-system routed-open relation", "lock_policy": "NONE_BY_DESIGN", "status": "ROUTED_OPEN"}, "choice_accounting": {"closure_complete": false, "closure_semantics": "OPEN_BY_DESIGN", "locked": ["theta_raster", "theta_utf73", "theta_abjad", "theta_atomic", "theta_transformer"], "routed_open": ["theta_bridge"], "used": ["theta_raster", "theta_utf73", "theta_bridge", "theta_abjad", "theta_atomic", "theta_transformer"]}, "closure_7_cardinality": {"carrier_count": 3, "prequotient": 9, "quotient": 7, "structure_count": 3}, "mod9_orbits": {"V1": [1, 2, 4, 8, 7, 5], "V3": [3, 6], "V9": [9], "transform": "T(r)=dr(2r)"}}}
Validation: D contains only explicitly selected finite/discrete project records; Planck-dataveld is a project term and not a physical Planck-scale claim
Transforms/links to: carrier_substitution_test
SVG selector: [data-concept="canonical_discrete_field"]

## 20.carrier_substitution_test · Executable Carrier Substitution
Chapter: Carrier Invariance
Domain: validation/carrier-substitution · Signal type: hash equality witness
Equation: sha256(canonical(D_A)) = sha256(canonical(D_B))
Parameters: {"carrier_A_sha256": "1343bb5bfd09cb9367c0e7778a4eabf57f256bc35dcb9d13adaff706c07fe318", "carrier_B_sha256": "1343bb5bfd09cb9367c0e7778a4eabf57f256bc35dcb9d13adaff706c07fe318", "carrier_content_consumed": false, "deterministic_witness_match": true, "reader_independence_proven": false, "scope": "abstract label witnesses only; proves deterministic canonical-field reconstruction, not reader-independence", "vacuity_status": "CURRENT ADAPTER IGNORES CARRIER CONTENT"}
Validation: abstract A/B witnesses reconstruct identical canonical D; canonical JSON SHA-256 hashes are equal; carrier content is not consumed by the current adapter; reader-independence is therefore not proven
Transforms/links to: carrier_invariance_status
SVG selector: [data-concept="carrier_substitution_test"]

## 20.read_route_operations · Read Route
Chapter: Carrier Invariance
Domain: model/read-route · Signal type: generation/parsing/tokenization route
Equation: G:A→SVG ; P_φ:SVG→Â ; T_τ:text→tokens
Parameters: {"fault_injection": {"all_expectations_match": true, "baseline_pass": true, "format_version": "1.0.0", "mutations": [{"detected": true, "expectation_match": true, "expected_detected": true, "failed_checks": ["ch14_png_sha256_recomputed"], "mutation": "M1_hash_char_flip"}, {"detected": true, "expectation_match": true, "expected_detected": true, "failed_checks": ["concept_count_103", "concept_ids_unique", "concept_order_matches_atlas"], "mutation": "M2_remove_field"}, {"detected": true, "expectation_match": true, "expected_detected": true, "failed_checks": ["concept_order_matches_atlas"], "mutation": "M3_swap_two_ids"}, {"detected": true, "expectation_match": true, "expected_detected": true, "failed_checks": ["concept_count_103", "concept_ids_unique", "concept_order_matches_atlas", "equation_attribute_count_103", "equation_content_nonempty"], "mutation": "M4_add_field_103_to_104"}, {"detected": true, "expectation_match": true, "expected_detected": true, "failed_checks": ["equation_content_nonempty"], "mutation": "M5_empty_one_equation"}], "reader": "P_χ", "sensitivity_summary": {"boundary": "P_χ now recomputes the Ch14 PNG SHA-256 independently and enforces non-empty equation content; broader semantic correctness remains out of scope", "detected": ["M1_hash_char_flip", "M2_remove_field", "M3_swap_two_ids", "M4_add_field_103_to_104", "M5_empty_one_equation"], "not_detected": []}}, "independent_reader": {"checks": {"ch14_png_sha256_recomputed": true, "concept_count_103": true, "concept_id_syntax": true, "concept_ids_unique": true, "concept_order_matches_atlas": true, "equation_attribute_count_103": true, "equation_content_nonempty": true, "metadata_chapter_count_20": true, "metadata_titles_match_atlas": true}, "common_mode_mitigation": "uses a separate non-XML-parser implementation path", "format_version": "1.0.0", "implementation": "raw SVG text + regular expressions + stdlib json/html/hashlib", "pass": true, "property_based": true, "reader": "P_χ", "scope": "independent structural + selected semantic property agreement; does not prove full semantic correctness", "shared_parser_code_with_P_phi": false}, "read_route": {"full_semantic_fault_injection": "data/full_semantic_fault_injection_ch20.json", "full_semantic_measurement": "data/full_semantic_self_read_measurement_ch20.json", "full_semantic_reader": "tools/full_semantic_self_read.py", "generation": "G : atlas-data → SVG", "parsing": "P_φ : SVG → parsed structure", "roundtrip_candidate": "P_φ(G(A)) ≅ A on the explicitly serialized structural subset", "self_read_measurement": "data/self_read_roundtrip_ch20.json", "status": {"full_self_reading": "EXACT_FULL_SEMANTIC", "generation": "exact for fixed committed generator", "parsing": "exact for the defined XML/canonical-whitespace parser on the serialized subset", "structural_roundtrip": "EXACT_ON_SERIALIZED_SUBSET", "tokenization": "deterministic given tokenizer choice τ"}, "tokenization": "T_τ : text → token sequence"}, "self_read": {"chapter_titles_match": true, "concept_order_match": true, "counts": {"chapters_in_metadata": 20, "concepts_committed": 103, "concepts_parsed": 103, "equations_match": 103, "fragment_hashes_match": 103, "texts_match": 103}, "format_version": "1.0.0", "full_self_reading": "OPEN", "not_recoverable_from_svg_alone": ["full concept parameters", "full validation objects", "full relation graph", "external data files not embedded in SVG"], "parser": "XML ElementTree + exporter-compatible whitespace canonicalization", "roundtrip_exact_on_serialized_subset": true, "serialized_subset": {"chapter_titles": "recoverable from SVG metadata", "concept_id": "recoverable", "equation": "recoverable", "svg_fragment_sha256": "recomputable", "svg_text": "recoverable after canonical whitespace"}, "status": "EXACT_ON_SERIALIZED_SUBSET"}}
Validation: generation, parsing and tokenization are distinct operators; SVG roundtrip is exact on the explicitly serialized structural subset; P_χ uses a separate raw-text/property route; independent property checks pass without proving full semantic correctness; full semantic self-read remains open
Transforms/links to: carrier_invariance_status
SVG selector: [data-concept="read_route_operations"]

## 20.carrier_invariance_status · Carrier-Invariance Ledger
Chapter: Carrier Invariance
Domain: methodology/status · Signal type: exact/conditional/open ledger
Equation: f=i∘b∘p ; X/~_f≅im(f) ; RI1∧RI2∧RI3
Parameters: {"claims": {"choice": ["which project records belong to canonical D", "parser choice φ and tokenizer choice τ"], "conditional": ["carrier substitution preserving D is currently a contract claim only; the existing A/B witness does not consume carrier content"], "exact": ["canonical D is finite JSON data", "canonical serialization and SHA-256 comparison are executable", "the committed route R is independent of carrier labels used by the test adapters"], "open": ["reader-independence across two independent carriers through a non-vacuous adapter A_ψ", "full semantic self-read P_φ(G(A)) = A_canonical", "a concrete arbitrary model swap preserving all non-canonical outputs"]}, "ladder_status": {"RI_gate_logic": "TESTED", "full_semantic_self_read": "EXACT_FULL_SEMANTIC", "independent_reader": "PROPERTY_CHECK_PASS + FAULT_SENSITIVITY_5_OF_5", "reader_independence": "REAL_CARRIERS_PASS", "self_consistency": "EXACT_ON_SERIALIZED_SUBSET"}, "orthogonal_claims": {"full_semantic_self_read": {"closure_condition": "every atlas.json field is either embedded losslessly in SVG or deterministically recomputable from SVG", "delta_status": "CLOSED", "equation": "P_φ(G(A)) = A_canonical", "evidence": "data/full_semantic_self_read_measurement_ch20.json", "fault_evidence": "data/full_semantic_fault_injection_ch20.json", "missing_from_svg_alone": ["full concept parameters", "full validation objects", "full relation graph", "external data files"], "status": "EXACT_FULL_SEMANTIC"}, "independent_reader_correctness": {"boundary": "selected semantic guards now include independent Ch14 PNG SHA-256 recomputation and non-empty equation content; full semantic correctness remains open", "equation": "properties(P_χ(G(A))) = committed structural properties", "scope": "independent implementation agreement on selected properties; not full semantic correctness", "status": "PROPERTY_CHECK_PASS + FAULT_SENSITIVITY_5_OF_5"}, "reader_independence": {"carriers": {"c1": "carrier_A_xml (xml.etree.ElementTree DOM parse)", "c2": "carrier_B_regex (raw-text regex + key=\"value\" scan)"}, "equation": "A_ψ(c₁)=A_ψ(c₂)=D", "evidence": "data/reader_independence_real_carriers_ch20.json", "gate_logic_status": "TESTED_SYNTHETICALLY", "real_carriers_status": "PASS", "required_evidence": ["A_ψ must consume carrier content c", "two independent carriers must be used", "the carriers must not merely be trained to reproduce the same atlas output", "canonical D and its hash must match"], "status": "PROVEN_REAL_CARRIERS"}, "self_consistency": {"equation": "P_φ(G(A)) ≅ A_serialized", "evidence": "data/self_read_roundtrip_ch20.json", "status": "EXACT_ON_SERIALIZED_SUBSET"}}, "quotient_factorization": {"chapter17": {"bijection": "identity on X/~_b = im(q)", "cardinality": "9 → 7", "construction_direction": "equivalence-first", "fiber_equivalence": "x ~_q y iff q(x)=q(y), equal to ~_b", "given": "boundary equivalence ~_b", "map": "q : X → X/~_b", "status": "EXACT GIVEN CH17 AXIOMS"}, "chapter20": {"bijection": "b([c])=A_ψ(c)", "construction_direction": "function-first", "derived_equivalence": "c_i ~_ψ c_j iff A_ψ(c_i)=A_ψ(c_j)", "distinguished_fiber": {"claim": "c₁,c₂ ∈ A_ψ⁻¹(D)", "element": "D ∈ im(A_ψ)", "nontriviality": "A_ψ⁻¹(D) ≠ C"}, "factorization": "A_ψ = i ∘ b ∘ p", "given": "A_ψ : C → Y_D", "result": "C/~_ψ ≅ im(A_ψ)", "status": "FORMAL SPEC ONLY; INDEPENDENT-CARRIER INSTANCE NOT YET EXECUTED"}, "format_version": "1.0.0", "interpretation": "one exact set-theoretic factorization instantiated in two construction directions; the selected equivalence/function instances remain project choices", "name": "Canonical quotient factorization", "scope": "sets and functions", "theorem": {"b": "b : X/~_f → im(f), b([x])=f(x)", "boundary": "called canonical quotient-factorization here; no algebraic homomorphism theorem is asserted", "equivalence": "x ~_f x' iff f(x)=f(x')", "factorization": "f = i ∘ b ∘ p", "i": "i : im(f) → Y", "p": "p : X → X/~_f, p(x)=[x]", "result": "X/~_f ≅ im(f)", "status": "EXACT FOR SETS/FUNCTIONS"}}, "reader_independence_gate": {"format_version": "1.0.0", "independent_reader": {"checks": ["exactly 103 data-concept attributes", "all 103 concept ids are unique", "concept-id order equals committed atlas order", "all concept ids satisfy the project identifier syntax", "exactly 103 data-equation attributes accompany concept groups", "embedded metadata declares 20 chapters", "embedded metadata chapter titles equal committed chapter titles", "all 103 data-equation attributes contain non-empty equation content", "visible Ch14 PNG SHA-256 equals an independent hashlib recomputation of assets/ch14_test_object.png"], "checks_count": 9, "claim": "independent structural + selected semantic property agreement; not full semantic correctness", "fault_injection_measurement": "data/independent_reader_fault_injection_ch20.json", "implementation_constraint": "must not import or call self_read_roundtrip.py, export_concepts.py, or their parsing helpers", "measurement": "data/independent_reader_measurement_ch20.json", "non_vacuity_status": "FAULT_SENSITIVITY_5_OF_5", "reader": "P_χ", "semantic_guards": ["independent SHA-256 recomputation of Ch14 PNG via hashlib", "all serialized concept equations must be non-empty"], "status": "PROPERTY_READER_IMPLEMENTED_WITH_SEMANTIC_GUARDS", "strategy": "raw-text/regular-expression property scanner; does not reconstruct the full atlas"}, "ladder": {"RI_gate_logic": "TESTED", "full_semantic_self_read": "OPEN_PENDING_FULL_SEMANTIC", "independent_reader": "PROPERTY_CHECK_PASS + FAULT_SENSITIVITY_5_OF_5", "reader_independence": "REAL_CARRIERS_PASS", "self_consistency": "EXACT_ON_SERIALIZED_SUBSET"}, "name": "Reader-independence and independent-reader gates", "reader_independence": {"adapter": "A_ψ(M,τ,c) → D", "conditions": [{"id": "RI1", "meaning": "first independent carrier reaches distinguished field element D", "predicate": "A_ψ(c₁)=D"}, {"id": "RI2", "meaning": "second independent carrier reaches the same D", "predicate": "A_ψ(c₂)=D"}, {"id": "RI3", "meaning": "A_ψ is non-constant; distinguished fiber is not all carriers", "predicate": "∃ c′ : A_ψ(c′) ≠ D"}], "current": {"RI1": "PASS", "RI2": "PASS", "RI3": "PASS", "carrier_content_consumed": true, "reader_independence_proven": true}, "gate": "EXACT only if RI1 ∧ RI2 ∧ RI3 and independence provenance all pass", "gate_logic_measurement": "data/reader_independence_gate_measurement_ch20.json", "gate_logic_status": "TESTED", "independence_requirements": ["c₁ and c₂ must be distinct carrier executions", "their independence provenance must be recorded", "the claim must not rely only on training both carriers to reproduce the same committed atlas output"], "optional_stronger_property": {"claim_enabled": "adapter uses every declared carrier component nontrivially", "name": "component-wise sensitivity", "predicate": "for every declared component k of c, there exist c,c' differing only in k with A_ψ(c) ≠ A_ψ(c')", "status": "OPTIONAL"}, "real_carriers": {"carrier_A": {"evidence": "parses SVG text into a DOM tree, then reads data-sem-*-b64 attributes via element.attrib", "function": "_read_xml", "id": "carrier_A_xml", "parser": "xml.etree.ElementTree"}, "carrier_B": {"evidence": "scans raw SVG text with <g ...> tag and key=\"value\" regexes; no DOM", "function": "_read_regex", "id": "carrier_B_regex", "parser": "re (regex) + raw key=\"value\" attribute scanning"}, "implementation": "tools/reader_independence.py", "note": "Both carriers decode the same committed data-sem-*-b64 payload fields with base64+json (shared data format, not shared parsing). The parsing strategy (DOM vs raw-text scan) is structurally independent.", "shared_parsing_code": false}, "real_carriers_measurement": "data/reader_independence_real_carriers_ch20.json", "status": "REAL_CARRIERS_IMPLEMENTED"}}, "reader_independence_gate_measurement": {"constant_fixture": {"checks": {"RI1": true, "RI2": true, "RI3": false, "independence_provenance": true}, "pass": false}, "format_version": "1.0.0", "gate_logic_tested": true, "missing_provenance_fixture": {"checks": {"RI1": true, "RI2": true, "RI3": true, "independence_provenance": false}, "pass": false}, "scope": "synthetic unit test of gate logic only; not evidence for real model reader-independence", "valid_nonconstant_fixture": {"checks": {"RI1": true, "RI2": true, "RI3": true, "independence_provenance": true}, "pass": true}}, "typing": {"0": "carrier: (M,τ), replaceable within interface contract", "1": "structure: R, committed code/chapters/validators", "1_equiv_0": "project boundary label for canonical D remaining invariant under admitted carrier substitution; not arithmetic equality"}}
Validation: canonical quotient-factorization f=i∘b∘p is exact for sets/functions; Ch17 is equivalence-first; Ch20 is function-first; reader-independence requires RI1, RI2, RI3 and independence provenance; full semantic self-read remains open
Transforms/links to: none
SVG selector: [data-concept="carrier_invariance_status"]

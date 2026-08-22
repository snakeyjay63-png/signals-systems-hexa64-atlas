# Signals & Systems · HEXA_64 Visual Atlas

A single, long-form SVG visual atlas covering the core Signals & Systems curriculum in an original HEXA_64 / NPN Signal Field visual language.

## What is included

- **20 chapters**
- **103 visual fields**
- One self-contained master SVG
- Computed curves, spectra, samples, block diagrams, and pole-zero maps
- Embedded SVG metadata and concept IDs
- No external image assets or remote URLs inside the SVG
- A Python generator for reproducibility
- SVG `<title>` / `<desc>` accessibility metadata
- A verification report
- Machine-readable `atlas.json` and line-oriented `concepts.ndjson`
- Deterministic token corpus for text/RAG pipelines
- Per-concept SVG-fragment and math-signature SHA-256 hashes
- Executable mathematical validator + unit tests
- GitHub Actions reproducibility check
- A ready-to-publish GitHub Pages viewer

## Files

- `index.html` — GitHub Pages / local viewer
- `assets/signals_systems_full_atlas_master.svg` — the complete atlas
- `tools/generate_signals_systems_full_atlas.py` — generator
- `verification.txt` — structural verification report
- `data/atlas.json` — full machine-readable atlas dataset
- `data/concepts.ndjson` — one concept record per line for streaming/token pipelines
- `data/token_corpus.md` — deterministic textual corpus generated from the SVG
- `data/schema.json` — JSON Schema for concept records
- `tools/export_concepts.py` — deterministic SVG → dataset exporter
- `tools/validate_atlas.py` — structural + mathematical validation
- `tests/test_math_invariants.py` — executable math/data tests
- `.github/workflows/validate.yml` — rebuild/export/validate CI

## Rebuild the atlas

Install the single runtime dependency and run the generator from anywhere:

```bash
python -m pip install -r requirements.txt
python tools/rebuild_atlas.py
python tools/validate_atlas.py
python -m unittest discover -s tests -v
```

The generator resolves the repository root from its own file location and writes directly to:

- `assets/signals_systems_full_atlas_master.svg`
- `verification.txt`

## View locally

You can simply open `index.html` in a browser. For the most consistent behavior, serve the folder with a local HTTP server:

```bash
python -m http.server 8000
```

Then visit `http://localhost:8000`.

## Publish with GitHub Pages

1. Create a new GitHub repository.
2. Upload or push the contents of this folder to the repository root.
3. In GitHub, open **Settings → Pages**.
4. Under **Build and deployment**, choose **Deploy from a branch**.
5. Select the `main` branch and `/ (root)` folder.
6. Save. GitHub will publish `index.html` as the site homepage.

## Git workflow

```bash
git init
git add .
git commit -m "Initial Signals & Systems HEXA_64 atlas"
git branch -M main
git remote add origin <YOUR-REPOSITORY-URL>
git push -u origin main
```

## Notes

This project is an original educational visualization atlas. It is not a reproduction of copyrighted textbook figures. The SVG re-expresses Signals & Systems concepts using original geometry, computed data, and diagrams.


## Machine-readable / training-friendly representation

The same atlas is available in two synchronized forms:

1. **Visual / geometric:** `assets/signals_systems_full_atlas_master.svg`
2. **Symbolic / textual:** `data/atlas.json`, `data/concepts.ndjson`, and `data/token_corpus.md`

Every concept record contains its chapter, equation, domain, signal type, parameters, validation invariants, graph relations, SVG selector and extracted SVG text. Two hashes deliberately track different classes of change:

- `svg_fragment_sha256` changes when that concept's SVG fragment changes.
- `math_signature_sha256` changes when its equation, declared parameters, or mathematical invariants change.

This makes it possible to distinguish a layout-only edit from a mathematical/content edit.

## Validation and CI

`tools/validate_atlas.py` independently recomputes representative invariants including the 64-sample discrete sinusoid DFT support, DTFS support, convolution behavior, Nyquist condition and unit-circle z-transform evaluation.

GitHub Actions rebuilds the SVG, re-exports all machine-readable data, runs the validator and unit tests, then requires the generated outputs to match the committed files exactly.

## Chapter 12 · Hash Dynamics

The atlas now includes a finite-state appendix connecting Signals & Systems ideas to
32-bit cyclic word geometry, addition modulo `2^32`, SHA-256 boolean/rotation mixers,
the 64-round compression state, and a reproducible one-bit avalanche experiment.

This chapter treats hashing as a finite-state dynamical system. Hash values are not
used as mathematical truth criteria; executable invariants remain the source of validation.

## Machine-readable validation

`data/schema.json` is enforced with `jsonschema` by `tools/validate_atlas.py`.
The CI pipeline rebuilds the SVG, re-exports all current concept records, validates schema
and mathematics, runs unit tests, and fails if generated repository outputs differ.

## Chapter 13 · Address Geometry

IPv4 is modeled as one 32-bit address word. IPv6 is modeled as a 128-bit address
space that may be partitioned computationally into four 32-bit lanes, while its
canonical text representation uses eight 16-bit groups.

The chapter includes the standard IPv4-mapped IPv6 representation:

`::ffff:192.0.2.33`

For the fixed example `192.0.2.33 = 0xC0000221`, the low 32 bits of the mapped
IPv6 value are exactly `0xC0000221`. The surrounding 96 bits define the mapped
address prefix/tag; the IPv4 payload itself is preserved exactly.

The validator recomputes this with Python's standard-library `ipaddress` module.

## Chapter 14 · Encoding Geometry

A fixed 160×96 SVG test object is carried through a complete, executable
representation chain:

`SVG → CairoSVG raster frame → PNG bytes → Base64 6-bit symbols → decode`

The generated repository includes:

- `assets/ch14_test_object.svg`
- `assets/ch14_test_object.png`
- `data/ch14_test_object.b64.txt`
- `data/encoding_geometry.json`

The validator independently re-rasterizes the SVG twice, checks deterministic
PNG bytes, proves the Base64 roundtrip byte-for-byte, verifies
`len(base64) = ceil(len(raw)/3) × 4`, and checks that the first 24 bits are
identical under the `8+8+8 → 6+6+6+6` partition shift.

`PHYSICAL PLANCK SCALE` is explicitly not claimed to map to pixels or symbols.
`STRUCTURAL FRAME` means the chosen minimum resolution of a representation:
vector coordinates → 1 pixel → 8-bit byte → 6-bit Base64 symbol.

## Chapter 15 · Canonical Field Encoding

Chapter 15 now shares one canonical `Σ73` definition with the live RGB encoder:

`data/utf73_field.json`

The 72 articulated states are six Devanagari consonants × twelve states, with
**anusvāra `ं` U+0902 as slot 12**, plus one abstract śūnya nil-state displayed
with `·` U+00B7. Virāma U+094D is not part of the canonical 73-state field.

The live encoder is explicitly versioned in the same file:

`RGB24 → HSV hue sector (6) × V/brightness bin (12) → Σ73`

with `(0,0,0) → śūnya`.

The generator exhaustively enumerates all `2^24 = 16,777,216` RGB24 colors and
writes the measured basin volumes to:

`data/utf73_rgb24_basins.json`

Those measured basins are the actual lossiness result. The older modulo model is
retained only as a **reference-model identity**:

`E73(n)=n mod 73`, `D73(s)=state index`, therefore `E73(D73(s))=s`.

That 73/73 identity is intentionally labeled as construction consistency, not
as evidence about the live HSV encoder.

The standalone browser validator remains:

`validators/sanskrit_utf73.html`

and is regenerated from the canonical field definition.

## Chapter 16 · Abjad Field Geometry

Chapter 16 is now explicitly split into three statuses rather than treating them as one claim.

### 1. Linear carrier

The input text is an ordered Unicode/UTF-8 sequence. UTF-8 preserves the carrier bytes and symbol order; it does not itself supply the abjad invariant.

### 2. Cultural mapping + pure mathematics

`data/abjad_field.json` is the canonical 28-letter direct lookup using the classical value ladder:

`1…9, 10…90, 100…1000`

`charCode % 28` is explicitly excluded because it is a codepoint hash, not the classical letter→value mapping. Normalization rules are also explicit (`ٱ→ا`, `ی→ي`, hamza variants, combining marks/tatweel removal).

After the mapping is fixed, the number-theory layer is exact and corpus-independent:

- `dr(v) = 1 + ((v-1) mod 9)`
- `T(r) = dr(2r)`
- `V1 = 1 → 2 → 4 → 8 → 7 → 5`
- `V3 = 3 → 6`
- `V9 = 9`

### 3. Empirical corpus layer

The corpus boundary lives in `corpora/quran_uthmani/`. `source.json` records a public 6236-ayah Uthmani JSONL source. The large corpus is intentionally not silently substituted or fabricated in this package. In a networked checkout run:

```bash
python tools/fetch_quran_fixture.py
python tools/analyze_quran_abjad.py --require-candidate
```

The first command writes the exact bytes plus `fixture.lock.json` with SHA-256. The second computes, per ayah:

`normalize → direct abjad sum → digital root → V1/V3/V9`

and measures all three orbit-class frequencies `V1`, `V3`, and `V9`. The earlier `2050/6236` result does not identify its target class inside this repo, so the candidate check deliberately does **not** invent one: it requires exactly one of the measured class counts to equal 2050 and reports which class matched.

The previously supplied empirical candidate, with its target orbit class explicitly unresolved, is recorded in `data/quran_abjad_hypothesis.json`:

`2050 / 6236`

with the exact arithmetic:

`1/3 − 2050/6236 = 43/9354`

That fraction is validated as arithmetic now. It becomes a **reproduced corpus result only when the exact locked fixture re-measures the count as 2050**. `data/quran_abjad_measurement.json` therefore currently says `fixture_missing` rather than printing a false PASS.

A separate manual GitHub Action, `.github/workflows/validate-corpus.yml`, performs the networked fetch, SHA lock, measurement, and `--require-candidate` check. If the fixture produces a different result, the workflow fails and reports the measured value instead of rewriting the hypothesis.

## Chapter 17 · 7-Closure

Chapter 17 is now a formal **quotient-closure theorem inside the project model**.

Two types are separated:

- `Frame = (C,S,b)` with nonempty finite `C,S`, `C∩S=∅`, `b∉C∪S`, and one unique boundary-equivalence class.
- `AtomicFrame = Frame + |C|=|S|=1`.

For three pairwise-disjoint atomic frames:

`X = ⊔ᵢ (Cᵢ ⊔ Sᵢ ⊔ {bᵢ})`

so `|X|=3×3=9`.

The only cross-frame identification is:

`b₁ ~ b₂ ~ b₃`.

Therefore the quotient has:

`|X/~| = 9-(3-1) = 7`.

Equivalently, the quotient inherits canonically:

`C′ = q(⊔Cᵢ)`, `|C′|=3`

`S′ = q(⊔Sᵢ)`, `|S′|=3`

and one common boundary class:

`b=[b₁]=[b₂]=[b₃]`.

The executable theorem checker proves that `(C′,S′,b)` satisfies the general
Frame axioms A1–A4. No post-hoc carrier/structure repartition is allowed; the
partition is inherited from the tagged inputs.

This changes the interpretation of `+1`: it is **not an added seventh point**.
It is the single quotient class produced by merging the three original
boundaries.

Atomicity (`|C|=|S|=1`) remains an axiom. The quotient output is proved to be a
general Frame, not an AtomicFrame. Necessity and uniqueness of the 7-closure
remain open.

Machine-readable / executable sources:

- `data/language_frame_axioms.json`
- `data/language_closure_7.json`
- `tools/language_frame_closure.py`

The existing exact cross-checks remain:

- `dr(7)=7`
- `T(7)=5`
- `7 ∈ V1=[1,2,4,8,7,5]`
- canonical abjad ordinal 7 is `ز` (zay), value `7`

`89 = F(11)` remains recorded only as a meta-observation.

## Chapter 18 · Transformer Frame

Chapter 18 has been inserted **before** its claim-by-claim architecture audit.

It contains four working panels:

1. proposed `C / S / b` correspondence with transformer components;
2. `1+6=7` first-ring / Seed geometry;
3. `signal → system → atlas` plus the finite-orbit / transformer bridge;
4. an explicit pre-audit status ledger and self-reference observation.

The machine-readable source is:

`data/transformer_frame_ch18.json`

Its status is now:

`AUDITED SLICE MODEL`

The audit fixes the scope to one transformer layer at a time: `C_l` is the
residual carrier, `S_l` is the layer-local contribution, and `b` selects the
superposition/merge event `b1`. The alternative `b2=x_{l+1}` is rejected as the
boundary because it is the next carrier `C_{l+1}`. A2 is therefore local to the
slice, not a global separation across the whole network.

## Chapter 19 · Choice Geometry / Reflective Closure

Chapter 19 makes the repo's own freedom explicit.

The basic form is:

`F_θ : X → Y`, with `θ ∈ Θ`.

The selected `θ` is not hidden in prose. The chapter records every currently
used choice position. Five are locked; a sixth, `theta_bridge`, is explicitly registered as **ROUTED_OPEN** for the `Σ73 ↔ abjad` bridge. The repo therefore
reports:

`Θ_used \ Θ_locked = {θ_bridge}`

and keeps `closure_complete=false` by design. The bridge is intentionally unlocked (`NONE_BY_DESIGN`), not awaiting completion.

Two chains remain separate:

`SVG → PNG → Base64 → PNG → optional SVG′`

and:

`Unicode/UTF-8 → Σ73 → abjad → V1/V3/V9 → Frame → transformer slice`.

Base64 is exact on bytes. SVG→PNG and optional PNG→SVG′ are not treated as
mutual inverses.

The closing provenance equation is:

`θ → F_θ → F_θ(X) → encode(θ,F_θ,results)`.

This means the artifact records the selected operator, parameters, equations,
hashes and validation results that generated it. It does not claim that `θ`
causes or selects itself.

Machine-readable source:

`data/choice_geometry_ch19.json`

### Routed-open bridge semantics

`theta_bridge` is an inter-system open relation, not a missing intra-system
configuration. Its project endpoint is `0.0.0.0`, explicitly labeled with its
real networking meaning: **IPv4 unspecified address**. The default route is
separately recorded as `0.0.0.0/0`; these are not the same object.

Likewise, “Null Island” is recorded only as a separate symbolic/geographic
analogy: it refers to coordinates `0°N, 0°E`, not to the IPv4 address
`0.0.0.0`.

The project-level nidra/sunya reading is therefore kept as a chosen semantic
layer, not promoted to a networking or physics invariant.

## Chapter 20 · Carrier Invariance / Read Route

Chapter 20 separates a replaceable model carrier from the committed structural
route and from the canonical discrete project state.

The formal route is:

`(M,τ) → adapter → R → D`

where `(M,τ)` is a compatible model/tokenizer carrier, `R` is the committed
code/chapters/validators, and `D` is the finite canonical state selected for
carrier-invariance checking.

The executable witness uses two **abstract compatible carrier adapters**. It
does not execute arbitrary external 7B/27B/70B models and therefore does not
claim identical logits, token IDs, embeddings or text outputs across model
families. It checks the narrower invariant:

`sha256(canonical(D_A)) = sha256(canonical(D_B))`.

The project term **Planck-dataveld** refers only to this canonical discrete
state `D`; it is not a physical Planck-scale claim.

The chapter also keeps three read operations distinct:

`G : atlas-data → SVG`

`P_φ : SVG → parsed structure`

`T_τ : text → token sequence`.

A future structural round-trip can test `P_φ(G(A)) ≅ A` on the subset actually
serialized into SVG. The stronger statement that the atlas literally reads
itself remains `OPEN`.

Machine-readable sources:

- `data/carrier_invariance_ch20.json`
- `data/carrier_invariance_measurement.json`
- `tools/carrier_invariance.py`

### Chapter 20 audit refinement: two orthogonal claims

The self-read roundtrip and reader-independence are now explicitly separated:

`self-consistency: P_φ(G(A)) ≅ A_serialized` → `EXACT_ON_SERIALIZED_SUBSET`

`reader-independence: A_ψ(c₁)=A_ψ(c₂)=D` → `OPEN`

`full semantic self-read: P_φ(G(A))=A_canonical` → `OPEN`

The current A/B adapter does **not** consume carrier content. Its equal hashes
therefore witness deterministic reconstruction of the same canonical field,
not reader-independence. The measurement records
`carrier_content_consumed=false` and `reader_independence_proven=false`.

Chapter 20 also records the structural quotient correspondence with Chapter 17:

`Ch17: b_L ~ b_G ~ b_E → [b]`

`Ch20: c_i ~_ψ c_j iff A_ψ(c_i)=A_ψ(c_j)`

This is the same quotient **form** at two levels, not a claimed universal law.
Reader-independence can only be promoted after `A_ψ` materially consumes
carrier content from two independent carriers.

### Chapter 20 formal factorization + independence gates

The Ch17↔Ch20 correspondence is now stored as the canonical quotient
factorization for sets/functions:

`f = i ∘ b ∘ p`

`p : X → X/~_f`, `b : X/~_f → im(f)`, `i : im(f) → Y`

and therefore:

`X/~_f ≅ im(f)`.

Ch17 is the **equivalence-first** construction: the boundary relation is given,
and the quotient projection realizes it. Ch20 is the **function-first**
construction: `A_ψ` is given and its fibers induce `~_ψ`.

Reader-independence is gated by three executable conditions:

`RI1: A_ψ(c₁)=D`

`RI2: A_ψ(c₂)=D`

`RI3: ∃c′ : A_ψ(c′)≠D`

plus explicit independence provenance for `c₁,c₂`. RI3 rules out a constant
adapter. The stronger component-wise sensitivity test is registered as an
optional extension, not a requirement for reader-independence.

A second implementation route, `P_χ`, is executable. It deliberately does
not import the XML/parser/export code used by `P_φ`; it reads raw SVG text
through a separate regex/property route and now checks nine properties. Two are
selected semantic guards: an independent `hashlib` SHA-256 recomputation for
the Ch14 PNG and the project invariant that every serialized concept equation
is non-empty.

This mitigates common-mode parser failure without claiming full semantic
correctness.

### Chapter 20 reader non-vacuity + RI gate unit tests

`P_χ` has a five-case fault-injection sensitivity suite. The independent
reader now detects all five registered mutations: hash-character corruption,
field removal, swapped concept IDs, an added 104th field, and an empty
equation. M1 is closed by independently recomputing the Ch14 PNG SHA-256 via
Python stdlib `hashlib`. M5 is closed by an explicit atlas specification choice:
all 103 serialized `data-equation` values must be non-empty. The fourteen
previously empty equation attributes were populated and are now validator-
enforced.

The RI gate also has a synthetic unit test. A minimal non-constant adapter with

`A_ψ(c₁)=A_ψ(c₂)=D` and `A_ψ(c′)=D′≠D`

is accepted. A constant adapter is rejected because RI3 fails. A non-constant
adapter without independence provenance is also rejected. This tests the gate
logic only; real reader-independence remains `OPEN`.

Current ladder:

`self_consistency = EXACT_ON_SERIALIZED_SUBSET`

`independent_reader = PROPERTY_CHECK_PASS + FAULT_SENSITIVITY_5_OF_5`

`RI_gate_logic = TESTED`

`reader_independence = OPEN`

`full_semantic_self_read = OPEN`

### Chapter 20 full-semantic self-read delta

The remaining semantic gap is explicit and machine-audited against `data/atlas.json`, the canonical object for this closure target. Each concept record has 16 fields. The current SVG self-read directly recovers or recomputes `concept_id`, `equation`, `svg_text`, and `svg_fragment_sha256`; `svg_selector` and `svg_element_count` are derivable without semantic duplication.

The remaining per-concept payload is: `chapter`, `chapter_title`, `title`, `subtitle`, `domain`, `signal_type`, `parameters`, `validation`, `relations`, and `math_signature_sha256`. At top level, `format_version` and `source_svg` still need explicit serialization; `concepts` is reconstructed from ordered records.

Closure invariant: `every field of A_canonical is either embedded losslessly or deterministically recomputable from the generated SVG`. Final target: `canonical_json(P_full(G_total(A_canonical))) == canonical_json(A_canonical)`. The partition is exact, but the total projection is not implemented; `full_semantic_self_read` therefore remains `OPEN · DELTA EXPLICIT`.

### Chapter 20 total semantic projection (`P_full`)

The full semantic self-read is now executable and exact for `data/atlas.json`.

The 16 concept fields are partitioned as:

- **5 direct/recomputed:** `concept_id`, `equation`, `svg_text`,
  `svg_fragment_sha256`, `math_signature_sha256`
- **2 deterministically derivable:** `svg_selector`, `svg_element_count`
- **9 lossless semantic payload fields:** `chapter`, `chapter_title`, `title`,
  `subtitle`, `domain`, `signal_type`, `parameters`, `validation`, `relations`

The nine payload fields are embedded in each concept group as canonical-JSON
bytes encoded with Base64. Hashes are **verification metadata, never payload**.
`math_signature_sha256` is recomputed from
`{concept_id,equation,parameters,validation}`; `svg_fragment_sha256` is
recomputed from the parsed concept group.

All semantic hashing and final equality use one specified `canonicalJSON`
implementation (`tools/canonical_json.py`), pinned by known-answer vectors in
`data/canonical_json_spec_ch20.json`: recursive Unicode NFC, sorted keys, no
insignificant whitespace, UTF-8, finite floats only, and deterministic JSON
number rendering.

`P_full` verifies in this order:

1. local math-signature recomputation;
2. local SVG-fragment recomputation;
3. embedded chapter vs. order-derived chapter/title cross-check;
4. global `canonicalJSON(rebuilt) == canonicalJSON(data/atlas.json)`.

The committed measurement is `EXACT_FULL_SEMANTIC`. Two additional semantic
faults are executable: M6 mutates a parameter and must trigger a localized
math-signature failure; M7 reorders records across a chapter boundary and must
trigger the chapter cross-check.

Current ladder:

`self_consistency = EXACT_ON_SERIALIZED_SUBSET`

`independent_reader = PROPERTY_CHECK_PASS + FAULT_SENSITIVITY_5_OF_5`

`RI_gate_logic = TESTED`

`full_semantic_self_read = EXACT_FULL_SEMANTIC`

`reader_independence = OPEN`

The only remaining open reader claim requires real independent carriers through
a non-constant `A_ψ`; no model evidence is inferred from the completed
self-read.

### AGNI additive projection invariant

The total semantic projection is additive: every one of the 103 existing concept groups keeps its existing `data-concept`, `data-equation`, and visible SVG child content. The nine semantic payload fields are added as **nine separate** `data-sem-*-b64` attributes; no aggregate replacement field is permitted. The validator requires exactly those nine attributes on every concept and forbids legacy `data-semantic-b64`. Hashes remain verification values: they are recomputed from their preimages and compared, never trusted as semantic payload.

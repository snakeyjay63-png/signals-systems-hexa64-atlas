# Chapter 16 · Abjad Field Geometry

## Canonical direct mapping

The source of truth is `data/abjad_field.json`.

The 28 classical values are:

`1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100,200,300,400,500,600,700,800,900,1000`

Each value is attached directly to an Arabic Unicode letter. No `charCode % 28`
hashing is used.

## Digital roots

`dr(v) = 1 + ((v - 1) mod 9)`

projects every positive abjad value into `{1,…,9}`.

## Doubling dynamics

`T(x)=dr(2x)`

has exactly the three displayed orbits:

- `V1 = [1,2,4,8,7,5]`
- `V3 = [3,6]`
- `V9 = [9]`

These are properties of the finite mod-9 dynamical system and do not depend on
a book or corpus.

## Corpus boundary

A future corpus validation must commit the exact text edition and normalization
fixture, then apply the same pipeline:

`Unicode text → normalize → direct abjad lookup → digital-root sequence → measured corpus geometry`

No Qur'an-vs-other-books uniqueness claim is encoded in this revision.


## Carrier / mapping / empirical separation

Chapter 16 treats four statuses separately:

1. **Carrier** — ordered UTF-8/Unicode text; lossless.
2. **Cultural mapping** — the explicit 28-letter classical abjad table; a chosen convention.
3. **Pure mathematics** — digital roots and `T(r)=dr(2r)` orbits; exact and corpus-independent.
4. **Empirical result** — class frequencies and transition counts measured only on an exact SHA-locked corpus fixture.

The supplied candidate `2050/6236` is stored without inventing which of `V1`, `V3`, or `V9` it refers to. A corpus run measures all three; `--require-candidate` passes only if exactly one class is 2050 and reports that class.

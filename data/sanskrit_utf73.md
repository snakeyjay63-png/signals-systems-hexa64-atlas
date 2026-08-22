# Chapter 15 · Canonical Field Encoding

## One canonical Σ73

The source of truth is `data/utf73_field.json`.

Six Devanagari consonants are combined with twelve states:

`inherent a, ā, i, ī, u, ū, ṛ, e, ai, o, au, anusvāra`

The twelfth explicit state is:

`ं` U+0902 DEVANAGARI SIGN ANUSVARA

Virāma `्` U+094D is **not** a member of this canonical field.

The 73rd state is an abstract śūnya / nil state. U+00B7 MIDDLE DOT `·` is only
its portable display glyph; it is not claimed to be a Devanagari nil character.

## Live RGB24 encoder

For each RGB24 input `(r,g,b)`:

1. `(0,0,0)` maps directly to śūnya.
2. Otherwise compute standard HSV hue.
3. Hue is partitioned into six 60° sectors.
4. Brightness is `V=max(r,g,b)`.
5. `brightness_bin = min(11, floor(V×12/256))`.
6. `state = hue_sector×12 + brightness_bin`.

`tools/utf73_field.py` exhaustively evaluates this mapping over all
`16,777,216` RGB24 values and stores exact basin counts in
`data/utf73_rgb24_basins.json`.

## Reference quotient identity

The former modulo-73 construction remains only as a reference model:

`E73(n)=n mod 73`

`D73(s)=state index`

so `E73(D73(s))=s` for all 73 states.

This is a construction identity. It is not the measured lossiness of the live
RGB24→HSV encoder.

The arithmetic

`2^24 = 73×229824 + 64`

therefore describes only that reference quotient, not the real HSV basin sizes.

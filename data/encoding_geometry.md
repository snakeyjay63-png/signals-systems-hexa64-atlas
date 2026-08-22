# Chapter 14 · Encoding Geometry

This chapter follows one actual 160×96 SVG through four representation frames.

## 1. Vector space

The source includes real-valued geometry such as:

`x = 12.4387`

No pixel index is implied yet.

## 2. Structural raster frame

CairoSVG renders the object to exactly `160×96` pixels.

At a unit pixel frame, the coordinate `x=12.4387` lies in raster cell `i=12`.

This is a **structural frame** chosen by the representation.

`PHYSICAL PLANCK SCALE` is shown only as a contrast label: the atlas makes no
claim that pixel scale, bytes or Base64 symbols correspond to a physical Planck scale.

## 3. PNG byte space

The actual PNG file is stored at `assets/ch14_test_object.png`.

The generator records its exact byte length and SHA-256 in
`data/encoding_geometry.json`. The byte stream includes the PNG signature and
compressed chunk structure; it is not presented as uncompressed pixels.

## 4. Base64 frame shift

Three 8-bit bytes contain 24 bits:

`8 + 8 + 8 = 24`

Base64 repartitions those same 24 bits into four 6-bit indices:

`6 + 6 + 6 + 6 = 24`

The partition boundaries move; the 24 underlying bits do not.

## 5. Character space

The alphabet is exactly:

`ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/`

Each non-padding character corresponds bijectively to one integer in `0…63`.

## 6. Reconstruction

`base64.b64decode(base64.b64encode(raw)) == raw`

is exact and asserted by the validator.

By contrast, `SVG → PNG → SVG′` is marked **LOSSY RECONSTRUCTION** because
rasterization does not retain the original vector primitive identity.

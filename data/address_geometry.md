# Chapter 13 · Address Geometry

## IPv4: one 32-bit value

`192.0.2.33`

is numerically:

`0xC0000221`

and occupies exactly 32 bits.

## IPv6: 128-bit address space

An IPv6 address is 128 bits. Two useful coordinate views are:

- computational: `4 × 32-bit` lanes
- canonical text grouping: `8 × 16-bit` hexadecimal groups

The four-lane view is a mathematical/computational partition, not a replacement
for IPv6's standard textual notation.

## Standard IPv4-mapped IPv6 form

IPv4-mapped IPv6 addresses reserve a 96-bit prefix and place the IPv4 value in
the low 32 bits.

For the atlas example:

`IPv4 = 192.0.2.33 = 0xC0000221`

`IPv6 mapped = ::ffff:192.0.2.33`

The low 32 bits of the 128-bit IPv6 integer remain exactly:

`0xC0000221`

So the inclusion can be viewed as:

`ι(x) = fixed_96_bit_prefix || x`

where `x` is preserved as one 32-bit slot.

## /64 decomposition

A `/64` prefix gives another useful coordinate split:

`128 bits = 64-bit network prefix || 64 remaining address bits`

This is conceptually separate from the IPv4-mapped `/96` structure.

# Chapter 12 · Hash Dynamics

This appendix models SHA-256 structurally as a finite-state dynamical system.

## State space

A SHA-256 working state contains eight 32-bit words:

`S_t = (a,b,c,d,e,f,g,h) ∈ (Z / 2^32 Z)^8`

The compression step repeatedly updates this finite state for 64 rounds.

## Cyclic word geometry

For a 32-bit word `x`, `ROTR^r(x)` permutes indexed bit positions on a cycle.
Rotation is lossless and preserves Hamming weight. The wrap is part of the state space.

## Modular addition

All word additions are performed modulo `2^32`:

`x ⊞ y = (x + y) mod 2^32`

The result therefore stays inside the same 32-bit finite state space.

## Boolean / rotation mixers

`Ch(x,y,z) = (x ∧ y) ⊕ (¬x ∧ z)`

`Maj(x,y,z) = (x ∧ y) ⊕ (x ∧ z) ⊕ (y ∧ z)`

`Σ0(x) = ROTR^2(x) ⊕ ROTR^13(x) ⊕ ROTR^22(x)`

`Σ1(x) = ROTR^6(x) ⊕ ROTR^11(x) ⊕ ROTR^25(x)`

These operations combine coordinate permutations and bitwise nonlinear mixing.

## Compression dynamics

A round can be viewed abstractly as:

`S_(t+1) = F(S_t, W_t, K_t) mod 2^32`

with 64 successive round updates.

## Embedded avalanche experiment

The atlas compares two 512-bit inputs:

- `m0`: 512 zero bits
- `m1`: identical except for one flipped input bit

Their SHA-256 outputs differ in exactly **133 of 256 output bits** for this fixed experiment.

This measurement is reproduced by `tools/validate_atlas.py`. It is presented as a
state-diffusion response, not as a proof or truth criterion.

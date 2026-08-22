# Chapter 18 · Transformer Frame — audited slice model

The working chapter has now been audited as a **per-layer Frame slice**.

For one transformer layer, the correspondence is:

`C_l ↔ x_l`

`S_l ↔ F_l(x_l)`

`b ↔ b1`, the residual superposition / merge event in `x_l + F_l(x_l)`.

The alternative `b2 = x_{l+1}` is rejected as the boundary candidate because
`x_{l+1}` is the carrier state of the next slice: `C_{l+1}`.

## Local A2

The Frame distinction `C ∩ S = ∅` is a **local typing distinction** inside one
layer snapshot. It is not a claim that carrier and structure remain globally
separable across the full transformer stack.

The network is therefore represented as a stack of slices:

`(C_l,S_l,b_l) → C_{l+1} → (C_{l+1},S_{l+1},b_{l+1}) → …`

where the next carrier contains the merged contribution from the preceding
layer.

## 6+1 geometry

Under the stated equal-circle hexagonal first-ring definition, one center has
six first-ring neighbors:

`1 + 6 = 7`

with coordination number `6`. This counting statement is marked exact within
that geometric definition.

## Still not promoted

The finite abjad-orbit ↔ transformer rotation/interaction bridge remains an
**analogy candidate**, not an equivalence theorem.

The fact that the atlas is being developed with a transformer-based language
model remains a **provenance observation**. Any stronger self-reference claim
would require its own proof.

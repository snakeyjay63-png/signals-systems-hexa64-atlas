# Chapter 17 · Quotient Closure Theorem

## Types

A general frame is:

`Frame = (C,S,b)`

with:

1. `C,S` nonempty finite sets;
2. `C ∩ S = ∅`;
3. `b ∉ C ∪ S`;
4. `b` the unique boundary-equivalence class.

An atomic frame adds:

`|C|=1`, `|S|=1`.

Atomicity is an axiom in this revision.

## Three atomic inputs

For pairwise-disjoint atomic frames `F₁,F₂,F₃`, take the disjoint union

`X = ⊔ᵢ(Cᵢ ⊔ Sᵢ ⊔ {bᵢ})`.

Each atomic frame contributes three points, so:

`|X| = 3×3 = 9`.

## Quotient

Define the equivalence relation by:

`b₁ ~ b₂ ~ b₃`

and leave every non-boundary point in a singleton class.

The quotient map canonically induces:

`C′ = q(⊔Cᵢ)`

`S′ = q(⊔Sᵢ)`

`b = [b₁]=[b₂]=[b₃]`.

No new carrier/structure labels are chosen after quotienting.

The three boundary points become one class, so two classes disappear:

`|X/~| = 9-(3-1)=7`.

Thus the familiar `3×2+1` form is a consequence:

`|C′|+|S′|+1 = 3+3+1 = 7`.

The `+1` is the shared quotient boundary class, not an added element.

## Closure theorem

`tools/language_frame_closure.py` constructs the quotient and checks:

- A1: `C′,S′` are nonempty;
- A2: `C′∩S′=∅`;
- A3: `b∉C′∪S′`;
- A4: exactly one boundary class remains.

Therefore the quotient is a **general Frame**.

It is not claimed to be atomic.

## Open ladder

- consistency: established;
- type closure: proved inside the model;
- atomicity necessity: open;
- 7-closure necessity: open;
- uniqueness: open.

`89=F(11)` is meta-observation only.

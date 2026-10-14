# GENERAL_REPORT — Clifford's chain theorem for all n

## Outcome: C (negative), proved in Lean. Rather than `∀ n, CliffordChain n`, the gate-checked result is the opposite:

```lean
theorem Clifford.cliffordChain_iff (n : ℕ) : CliffordChain n ↔ n ≤ 5
theorem Clifford.Counter6.not_cliffordChain_six : ¬ CliffordChain 6
theorem Clifford.not_cliffordChain_of_six_le {n : ℕ} (hn : 6 ≤ n) : ¬ CliffordChain n
```

`CliffordChain n` as defined in `Clifford/Clean.lean` is **false for every n ≥ 6**. The cause is a
defect in the definition, not in Clifford's theorem. The chain is set in the finite plane ℂ, so a
Clifford point at infinity has nowhere to go.

## Step 0 findings

### (a) Is GenPosN strong enough? No, from n = 6 on.

* Generic check (mpmath, 60 digits). I built the classical chain for random centres for n = 3…8
  (second intersections, then circumcircles / common points level by level). Every concyclicity and
  concurrency held to about 1e-54. It also agreed with an explicit closed form for every n = 3..8
  (differences ≤ 1e-54). After inversion at M, circle k becomes the line `w = a_k + t_k·conj w` with
  `a_k = 1/conj c_k` and `t_k = −c_k/conj c_k`. The Clifford object is then read off the kernel of the
  n×(n+1) "rational interpolation" matrix `[t_k^j | −a_k t_k^j]` (Morley-type formula: numerator
  degree ⌊n/2⌋, denominator degree ⌊n/2⌋ or ⌊n/2⌋−1). For even n = 2m the level-n point is
  `−Q_{m−1}/P_m`. For odd n the coefficient `P_0` multiplies z·z̄.
* Degeneration. For even n = 2m ≥ 6 the coefficient `P_m` (the denominator of the Clifford point)
  is one complex condition on the centres, and **GenPosN does not exclude it**. When `P_m = 0` the
  classical level-6 point is at infinity. Each of the six level-5 objects is then a *line* (five
  distinct collinear Miquel points), and the six lines are parallel to nothing in particular and are
  not concurrent in ℂ. A Gauss–Newton search found such configurations from all 10 random starts
  (GenPosN minimum quantities 0.001–0.24, far from 0). For n = 4 the same search only ever reached
  `GenPosN`-violating configurations, which matches `resD` in Basic.lean.
* Exact counterexample (Gaussian integers, found by an exact rational search):
  `c = (3−6i, 6−3i, 1+2i, −2−i, −4i, 4)`.
  - GenPosN holds exactly: all 15 Transversal conditions and all 20 `triP`, `cycP` are nonzero.
  - All 15 level-4 points are uniquely determined: the three Γ-circles force them (Lean: `Counter6.q….`).
  - The omit-0 subfamily's five level-4 points are distinct and lie on one line; the same holds for
    each of the other five subfamilies. For example, omitting circle 4 gives the line Re z = 4, and
    omitting circle 5 gives Im z = −4.
  - The lines for omitting circles 4, 5 and 0 have no common point (an exact rational certificate
    gives `1 = 0`).
  - Perturbing `c₅` by ε moves the classical level-6 point to |p| ≈ 2.4·10⁻²/ε (ε = 1e-2, 1e-4,
    1e-8 give 2.4e3, 2.4e5, 2.4e9). So the "missing" point really is the point at infinity.
* Geometric meaning. Invert at M. The six circles become six lines in general position. Their
  classical Clifford point is a perfectly good finite point that happens to be M itself, and the
  inversion sends it to ∞. Clifford's theorem holds; the predicate cannot express ∞.
* Propagation. For n ≥ 7, `Chain n` requires a level-(n−1) object of the subfamily that omits the
  last circle. Any GenPosN family extends by a circle in general position (`GenPosN.exists_snoc`), so
  the counterexample propagates to every n ≥ 6. Numerically, for 7 circles extending `c` the level-7
  object is the line through the six finite level-6 points (z·z̄ coefficient exactly 0), and
  "omit circle 7" gives the point at ∞, which is consistent with the projective picture.
* n = 7 and 8 with random centres: the classical chain exists and all even-level denominators are
  bounded away from 0 (minimum normalised 0.0107 over 20 random families).

### (b) Is the predicate too weak? No trivialisation found.

* Levels 0–2 are fixed sets.
* Level 3 is forced to be the circumcircle: under GenTriple the three second intersections are not
  collinear.
* Level 4 is forced to be the Miquel point. This is proved for the counterexample: `chain4_cD`
  together with three concyclicity determinants pins `q`.
* So nothing degenerate can be chosen at the low levels, and `CliffordChain 4` / `5` / `6` carry real
  content (n = 6 is in fact false).
* Remaining caveat: at odd levels `X` is *some* generalized circle through the chosen points. If
  those points coincided (at most two distinct), `X` would not be unique, and higher levels could
  choose among several `X`. That would make `Chain` weaker than the classical statement in such
  configurations, but I found no way to exploit it. Radius-0 spheres only arise when all points
  coincide; negative radius gives the empty set, which cannot contain the points.

### Proposed corrected predicate (not formalised)

Work on the Riemann sphere:
* even-level objects are points of `OnePoint ℂ` (∞ allowed);
* odd-level objects are generalized circles, where a line contains ∞;
* `Chain` is otherwise unchanged.

Equivalently, apply the inversion and state it for n lines in general position, where all
objects are finite (Clifford/Morley). The numerics say this version holds for n ≤ 8. A finite-plane
alternative is GenPosN' := GenPosN ∧ (for every subfamily S of even size ≥ 4 the classical
denominator `P_{|S|/2}(S) ≠ 0`). The counterexample shows this extra hypothesis is *necessary* for
the ℂ-valued predicate. I have neither proved nor numerically stress-tested that it is
*sufficient*, for example when degenerate odd-level lines lead to coincident points.

## Lean files (new; line counts)

| file | lines | content |
|---|---|---|
| `Clifford/General.lean` | 99 | `cD` (real concyclicity determinant), `cD_eq_zero` (4 points on an `IsGCircle` ⇒ `cD = 0`), unfolding lemmas `chain2_eq`, `chain3_mem`, `chain4_cD`, `chain5_mem`, `second_eq` |
| `Clifford/Counter6.lean` | 233 | `Counter6.cx`, `cx_genPosN`, 15 `second` values, 9 forced level-4 points, `not_chain6`, `not_cliffordChain_six` (generated by `numerics/genlean.py`; all certificates are `linear_combination` with exact rationals) |
| `Clifford/Classify.lean` | 239 | `cliffordChain_zero/one/two/three`, `not_chain_of_extends`, polynomial finiteness (`par t = t + t² i`, `pA/pT/pC_ne_zero`, `finite_bad`), `GenPosN.exists_snoc`, `exists_extension`, `not_cliffordChain_of_six_le`, `cliffordChain_iff` |

* `Clifford.lean` got 3 new import lines.
* Numerics: `numerics/*.py` (exact Gaussian-rational arithmetic `gq.py`, mpmath chain `chain.py`,
  degeneracy search `d6.py`/`d6b.py`, certificate check `cex2.py`); scratch work is in `scratch/`.
* No changes to Basic/Clean/Bridge.

## Checks

* `lake build`: `Build completed successfully (8713 jobs).`
* Gate: `PASS (32 declarations, standard axioms only)`. 11 new REQUIRED entries:
  - `Clifford.cD_eq_zero`
  - `Clifford.chain4_cD`
  - `Clifford.chain5_mem`
  - `Clifford.Counter6.cx_genPosN`
  - `Clifford.Counter6.not_chain6`
  - `Clifford.Counter6.not_cliffordChain_six`
  - `Clifford.cliffordChain_three`
  - `Clifford.not_chain_of_extends`
  - `Clifford.GenPosN.exists_snoc`
  - `Clifford.not_cliffordChain_of_six_le`
  - `Clifford.cliffordChain_iff`

  All print `[propext, Classical.choice, Quot.sound]`.
* Tamper: `ALL TAMPERING TESTS REJECTED`. There are 8 tests; the new `classify6` changes
  `cliffordChain_iff` to `n ≤ 6` and is rejected with "FAIL: build".
* `grep sorry|admit|axiom|native_decide` over the new files finds nothing.
* SHA-256 (identical before and after):
  - Basic  `d5c14edbf2da8ec8288484b4eeee54e30e85cf04e5c440c406b4c7144ca0cb16`
  - Clean  `2a7cf40b4c473e56c97db8b1485aa5ad468c9cbb5c9a56b5b7ac9adaf33cc463`
  - Bridge `93eb80b639791dc7e271249a79e0439dd3fd08c831eb71e367129c52c8cecf5b`

## What remains

1. Fix the definition (Riemann-sphere or line-picture version, as above). This needs a decision by
   the authors, since Clean.lean is cited and must not be edited; a new `Chain'` would go in a new
   file.
2. Prove the corrected theorem for all n with the explicit Morley/interpolation formula. Plan:
   * define `F n c` from the kernel of `[t_k^j | −a_k t_k^j]`;
   * show the incidence "level-(n−1) object of c∖i passes through / lies on F n c" via a
     Cramer/Desnanot–Jacobi-style determinant identity (in the spirit of `kK_dj` in Basic.lean);
   * do the nondegeneracy bookkeeping, which is where ∞ must be handled.

   The formula is numerically verified for n = 3..8; none of this is formalised yet.
3. Settle whether GenPosN' (no even-level classical point equal to M) is enough for the finite-plane
   predicate.

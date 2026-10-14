# Clifford's chain as a general predicate in Lean 4 (n = 4, 5)

An existential predicate `CliffordChain n` for Clifford's chain, set in the finite plane ℂ, with a complete classification: it holds exactly for n ≤ 5 (`cliffordChain_iff`). For n = 6 an exact six-circle counterexample in general position (`Counter6`) has its Clifford point at infinity, which the finite plane cannot represent; it propagates to every n ≥ 6. Bridges tie the general-position conditions to geometry.

This repository is one of eight Lean 4 developments accompanying the paper *Circle configurations in
classical plane geometry, formalized in Lean 4: Clifford's chain, Miquel's five circles, Lester,
Sawayama–Thébault and Kosnita* (J. Bald, 2026). The paper states each theorem in prose with every
hypothesis, lists the degenerate configurations each statement excludes, and reports the verification
summarised below.

**Status:** all statements proved, no `sorry`. `gate.sh` checks **32** named declarations.

## Main statements

| Lean name | File:line | Statement |
|---|---|---|
| `Clifford.cliffordChain_four` | `Clifford/Clean.lean:226` | `CliffordChain 4` |
| `Clifford.cliffordChain_five` | `Clifford/Clean.lean:245` | `CliffordChain 5` |
| `Clifford.clifford_two_clean` | `Clifford/Clean.lean:123` | n = 5 under general position only: five points concyclic or collinear |
| `Clifford.transversal_iff` | `Clifford/Bridge.lean:58` | `Transversal c d` ⇔ M, c, d not collinear |
| `Clifford.triP_ne_zero_iff` | `Clifford/Bridge.lean:62` | first `GenTriple` condition ⇔ centres not collinear |
| `Clifford.cycP_ne_zero_iff` | `Clifford/Bridge.lean:83` | second condition ⇔ the three second intersections not collinear (centres not collinear) |
| `Clifford.genTriple_iff` | `Clifford/Bridge.lean:110` | `GenTriple` ⇔ neither centres nor second intersections collinear |
| `Clifford.cliffordChain_iff` | `Clifford/Classify.lean:227` | **classification:** `CliffordChain n ↔ n ≤ 5` |
| `Clifford.Counter6.not_cliffordChain_six` | `Clifford/Counter6.lean:227` | the explicit six-circle counterexample (`Counter6.cx`, Gaussian-integer centres) |
| `Clifford.not_cliffordChain_of_six_le` | `Clifford/Classify.lean:219` | `¬ CliffordChain n` for every `n ≥ 6` |
| `Clifford.onCircleM_iff_mem_sphere` | `Clifford/Bridge.lean:104` | the circle model is Mathlib's `Metric.sphere c ‖c‖` |

Read the Lean statement for the exact hypotheses; the paper lists them in prose.

`GENERAL_REPORT.md` records how the counterexample was found; `numerics/` holds the exact-arithmetic
scripts used in that search (not needed to build or check the Lean proofs).

## Verification

`./gate.sh` builds the library and runs `#print axioms` on the 32 declarations in its `REQUIRED`
list. It fails if a source file contains `sorry`, `admit`, `native_decide`, `axiom`, `#eval`, `run_cmd`,
`set_option`, a macro or syntax extension; if the build fails; or if any listed declaration depends on
anything other than `propext`, `Classical.choice` and `Quot.sound`.

Expected output: `PASS (32 declarations, standard axioms only)`. Checked on x86-64 Linux and arm64
macOS at the pinned Mathlib revision.

`bash tests/tamper.sh` plants defects in scratch copies (ax2line, classify6, cleanand, evalfake, falsehyp, macro, sorry, wrap) and checks that the gate
rejects each one.

The paper also reports a statement-level battery (conclusion mutations, contradiction probe,
satisfiability witnesses, hypothesis ablation, unused-variable linter), an independent numerical
re-check, and a prior-art search. Those results, and their limits, are in the paper's Verification
section.

## Build

```sh
curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh   # if Lean is not installed
lake exe cache get
lake build
./gate.sh
bash tests/tamper.sh
```

Toolchain: Lean `v4.33.1`, Mathlib `v4.33.1` (revision pinned in `lake-manifest.json`). `gate.sh` never
fetches: run `lake exe cache get` first.

## Note on how this was produced

The formal proofs and documentation were developed with the help of a large-language-model AI
assistant. The author directed the work, reviewed the statements, and is responsible for the result.
The Lean kernel checks every proof.

## License

Code: Apache License 2.0 (see `LICENSE`). Documentation: CC BY 4.0.

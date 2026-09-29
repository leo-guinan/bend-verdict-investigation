# Findings report

## Executive conclusion

No bounty-grade falsehood was found in Bend 2.0.32. We did not produce a file that both:

1. passes `bend file.bend --verdict` with `ALL PROOFS CHECK`, and
2. exposes a live inhabitant of `Empty`.

The tested consistency boundaries held. The most important positive finding was not a false proof but a rejected-path checker/kernel mismatch, reported upstream in issue #1182.

## Scope and method

The investigation pinned Bend `v2.0.32` at commit `573002f01ec6c52416d44489543f69a9625facf8` and exercised both the ordinary checker and the formal BendTT verdict path. Each candidate was treated as a prediction: source, command, output, hash, and rejection reason were preserved where possible.

The shipped test corpus contained 1,508 files:

- 960 passed `--verdict`.
- 548 failed as expected or intentional negatives.
- 0 timed out.
- 0 checker/kernel status mismatches were found in the corpus.
- 0 passing files contained a closed `law ...: Empty` or zero-argument `def ...() -> Empty` shape.

## Attack surfaces tested

- Direct `Empty` construction and open laws.
- Hurkens/Girard-style paradoxes.
- Erased/live quantity boundaries and erased matches.
- Dead-hypothesis laundering.
- Equality rewrites and explicit motives.
- Dependent families and higher-order family applications.
- Template specialization keys, aliases, eta-equivalence, and cycles.
- Binder capture and alpha-renaming.
- Match flattening, duplicate rows, nested patterns, defaults, and generated `Efq` tails.
- Mutual recursion, closure-mediated recursion, selector tag order, helper arity, and opaque specialization identity.
- Constructor saturation, dependent fields, omitted parameters, and partial constructors.
- Runtime-dependent kinds with an empty branch.
- Nat literal patterns and U32 boundary literals.
- Higher-order equality evidence through templates, laws, erased/demanded definitions, and dependent result families.

## Strongest finding: issue #1182

The minimized probe `probes/higher_evidence_base.bend` contains an opaque higher-order template parameter:

```bend
def use(~F: @a: N -> @b: N -> {S{a} == S{b} : N} -> {a == b : N}, a: N, b: N, e: {S{a} == S{b} : N}) -> {a == b : N}:
  F(a, b, e)
```

Observed behavior:

- `--check-only`: `ALL PROOFS CHECK`
- `--verdict`: explicit TypeScript/formal-kernel mismatch warning and nonzero exit

Dimension reduction showed:

- Equality only as an input: both lanes pass.
- Dependent equality in the result of an opaque `~F`: mismatch.
- Removing `~` from `F`: both lanes pass.
- Direct, curried, let-bound, eta-expanded, and annotated applications: same mismatch.
- `def` versus `law`: same mismatch.
- Demand versus no demand: same mismatch.

This is a real synchronization or unsupported-encoding bug. It is not a bounty falsehood because BendTT rejects the program.

## Why the bounty was not captured

The recurring obstacle was the live affine/termination boundary. Abstract functions can be assigned dependent result types that reduce to `Empty`, but a concrete closed function returning that result at the empty index requires an inhabitant of `Empty` already. The ordinary checker sometimes accepts the abstract form; the proven kernel refuses it before verdict success.

The investigation found no way to turn that rejected mismatch into an accepted `--verdict` proof.

## Residuals

- Official bounty rules were not available in the tested material.
- F32 axiomatic paths were not treated as in-scope; the announcement says some F32 idioms are not covered.
- Unsafe and FFI paths were excluded.
- This is not a formal proof of BendTT soundness.
- Results apply to the pinned 2.0.32 revision, not later releases.

## Reproduction discipline

When extending this work:

1. Pin the Bend binary and source commit.
2. Run both `--check-only` and `--verdict`.
3. Preserve exact stdout/stderr and source hashes.
4. Inspect whether the result is actually a closed live `Empty`, not merely an open law, dead term, mismatch warning, or ordinary checker acceptance.
5. Keep rejected paths and negative controls. They are the evidence, not clutter.

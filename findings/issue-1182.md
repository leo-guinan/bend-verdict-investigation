## Bug description

Bend 2.0.32's ordinary checker accepts a closed definition containing an opaque higher-order template parameter whose result type contains dependent equality, but `--verdict` cannot validate the same definition and reports a TypeScript/BendTT mismatch.

This is not being claimed as a soundness exploit or bounty submission. The kernel rejects it; the report is for the reproducible checker/formalization synchronization failure.

## Environment

- Bend: 2.0.32
- Source revision tested: `v2.0.32`, commit `573002f01ec6c52416d44489543f69a9625facf8`
- macOS arm64

## Minimal reproducer

```bend
import Base

type N is Data:
  Z{}
  S{p: N}

def pred(n: N) -> N:
  match n:
    case Z{}: Z{}
    case S{p}: p

def inj(a: N, b: N, e: {S{a} == S{b} : N}) -> {a == b : N}:
  %x@e : {pred(S{a}) == pred(_) : N}
  {==}

def use(~F: @a: N -> @b: N -> {S{a} == S{b} : N} -> {a == b : N}, a: N, b: N, e: {S{a} == S{b} : N}) -> {a == b : N}:
  F(a, b, e)

def main() -> N:
  Z{}
```

Save as `higher_evidence_base.bend` and run:

```sh
bend higher_evidence_base.bend --check-only
bend higher_evidence_base.bend --verdict
```

## Observed behavior

`--check-only`:

```text
ALL PROOFS CHECK
Use --verdict for mathematical validity.
```

`--verdict`:

```text
SOME PROOFS FAIL
Sorry - this is a mismatch between the TypeScript implementation, and the formalized BendTT kernel. Your proofs may or may not be correct, and we cannot validate them yet. This will be addressed in a future update. Meanwhile, feel free to open an issue to report this bug.
```

## Minimization results

The mismatch disappears when any of these changes are made:

- Remove the `~` from `F` and make it an ordinary affine function parameter.
- Remove dependent equality from the result type while retaining equality as an input.
- Use the standalone `inj` proof without the higher-order opaque template parameter.

Equality only as an input passes both checker and verdict. Equality in the result of an opaque `~F` reproduces the mismatch.

I also tested direct, curried, let-bound, eta-expanded, and explicitly annotated applications. They all preserve the same mismatch. Making the result family reduce to an `Empty` branch does not produce an accepted proof: `--verdict` still rejects the definition.

## Expected behavior

Either:

1. the ordinary checker rejects this unsupported form before reporting `ALL PROOFS CHECK`, or
2. BendTT accepts and validates the emitted term.

The current result is an explicit synchronization failure between the ordinary TypeScript checker and the formalized kernel.

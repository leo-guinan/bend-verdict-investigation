# Bend `--verdict` investigation

Adversarial, reproducible investigation of Bend 2.0.32's formalization sync and proof boundary.

Status: no bounty-grade falsehood found.

The central question was whether a Bend file could pass `bend file.bend --verdict` while exposing a live inhabitant of `Empty`. We did not find one. The strongest result was a reproducible checker/BendTT synchronization bug involving an opaque higher-order template parameter with a dependent equality result. It is reported upstream as GitHub issue #1182:

https://github.com/bendlang/bend/issues/1182

## Tested revision

- Bend: 2.0.32
- Git tag: `v2.0.32`
- Commit: `573002f01ec6c52416d44489543f69a9625facf8`
- Host: macOS arm64

## Reproduce

Install Bend 2.0.32 using the official installer, then run:

```sh
export PATH="$HOME/.bend/bin:$PATH"
bend probes/higher_evidence_base.bend --check-only
bend probes/higher_evidence_base.bend --verdict
```

The first command returns `ALL PROOFS CHECK`. The second returns the explicit TypeScript/formal-kernel mismatch warning and exits nonzero. This is not a bounty result: BendTT rejects it.

## Repository map

- `REPORT.md` — detailed findings, scope, and residuals.
- `VERSION.md` — pinned environment and provenance.
- `probes/` — minimized Bend source probes.
- `harness/` — generators and scan scripts.
- `receipts/` — JSON outputs from real executions.
- `findings/issue-1182.md` — the upstream bug report body.

## Important negative result

The absence of a candidate here is not a proof that Bend is sound. It is a bounded investigation against one pinned release, with preserved negative results and one reported synchronization failure.

Do not describe any file in this repository as a bounty submission.

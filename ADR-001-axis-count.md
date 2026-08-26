# ADR-001 — The canonical axis count is 22

**Status:** ACCEPTED · **Date:** 2026-08-26 · **Decider:** Nick Templeman (owner)
**Original ruling:** 2026-08-24, `csoai-static-deploy2` commit `2bdbac34`
**Supersedes:** the "13 measured of 14" framing, and every other count in circulation.

> **CORRECTION, 2026-08-26.** A first draft of this ADR ruled "14". That was wrong. It
> was written from a session summary without first reading the estate's own recorded
> canon, which already carried the 22-axis ruling. The error is logged here rather than
> quietly overwritten, because the failure mode — re-deriving a settled fact instead of
> reading the ledger — is exactly what this document exists to stop.

## Ruling

> **Twenty-two measured axes = 14 GSPC (including jail) + 8 financial/domain.**

Jail was measured 2026-08-21 via `gspc-jail-v2` (commit `70451d3`) and is counted.

## Why the live board still says 14 — and why that is not a contradiction

`GET /api/gspc` reports `14 measured of 14 quotable`. That is **the un-swept state, not
the canon.** The 8 financial/domain axes are ruled in but are **not yet present in the
signed board payload**. The board is behind the ruling, not ahead of it.

This matters for how it gets fixed:

> **`/api/gspc` counts are derived from signed board data. The sweep therefore requires
> the financial axes to be wired into the API's signed data and the payload re-signed —
> NOT copy edits on the pages.**

Sweeping the copy without re-signing the payload would put a public number on a surface
that the signed artifact does not support. That breaks signed-artifact discipline, which
is the whole product. The sweep is **authorized but unexecuted** for precisely this reason.

## Current state of the surfaces (measured 2026-08-26 by `scripts/facts-gate.mjs`)

| Surface | Says | Status |
|---|---|---|
| Canon (this ADR) | **22** | ✅ ruled |
| `GET /api/gspc` | 14 | un-swept — awaiting the data+re-sign path |
| 26 `gspc/*` axis pages | 17 | ✗ wrong under either number |
| `/arena-scoreboard` | 15 | ✗ wrong, and disagrees with `/verify-leaderboard` |
| board `limitations[3]` | 16-slot "living board" | internal convention, not a public count |

Note the 17 and 15 are wrong regardless of how the 22-vs-14 question resolves. They can be
corrected independently of the sweep.

## Consequences

1. **The sweep is a DATA task, not a copy task.** Wire the 8 financial/domain axes into the
   signed board data, re-sign, and let every surface read `totals.public_count` from
   `/api/gspc`. No surface should type a count.
2. `client/src/data/facts.json` records the count as a **pointer** to that endpoint. When
   the data lands, every surface moves together. A hand-typed count in more than one place
   will diverge — it already produced 14, 15, 16, 17 and 22 simultaneously.
3. **`facts-gate` stays advisory (`continue-on-error: true`) until the sweep completes.**
   A blocking gate that enforces the un-swept number would cement the wrong count; a
   blocking gate that enforces 22 before the data supports it would make every deploy
   assert something the signed payload cannot back.
4. Flip the gate to blocking the moment `/api/gspc` reports the swept number. Then, and
   only then, is a non-blocking claim-lint decoration.

## The rule this encodes

Two rules, both learned the hard way today:

- **Read the ledger before ruling.** A settled fact re-derived is a settled fact broken.
- **A public count must be backed by the signed artifact it claims to summarise.** Copy
  that outruns the data is the same defect class as a score without its measurement.

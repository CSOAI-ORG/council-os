# ADR-001 — The canonical axis count is 14

**Status:** ACCEPTED · **Date:** 2026-08-26 · **Decider:** Nick Templeman (owner)
**Supersedes:** every other axis figure in circulation.

## Ruling

> **Fourteen slots: thirteen measured axes plus jail.**

That is the frozen canonical number. It is what `GET /api/gspc` reports
(`totals.public_count` = "14 measured of 14 quotable") and it is what everything
was built on.

## Context — why a ruling was needed

A machine-readable claims gate (`scripts/facts-gate.mjs`) was built on 2026-08-26 and
run against the prerendered site. It found **29 contradictions** and, in doing so,
surfaced that **five different axis counts were live or in circulation at once**:

| Surface | Claimed | Disposition |
|---|---|---|
| `GET /api/gspc` (the live board) | **14** | ✅ **CANONICAL** |
| 26 `gspc/*` axis pages | 17 | ✗ stale copy — correct to 14 |
| `/arena-scoreboard` | 15 | ✗ stale copy — correct to 14 |
| board `limitations[3]` | 16-slot "living board" | internal convention; not a public count |
| internal briefs | 22 (= 14 + statistical layer) | `internal` only; **never a public claim** |

Note, verified: "22 axes" appears exactly twice site-wide and **both are prohibitions**
("do not invent 22 axes"). It is asserted nowhere. The 22 figure describes 14 core axes
plus the statistical layer (Wilson, McNemar, human-baseline); it is a description of the
method stack, not a count of axes, and it stays `status: internal`.

## Consequences

1. `client/src/data/facts.json` records the count as a **pointer** to
   `GET /api/gspc → totals.public_count`, never as a typed integer, so it cannot drift.
2. All 29 contradicting surfaces are corrected to read from that pointer or to state 14.
3. **`facts-gate` flips from `continue-on-error: true` to BLOCKING** once those 29 are
   fixed. Rationale, in the owner's words: *"a non-blocking claim-lint is decoration."*
   The gate is wired non-blocking ONLY for the window between this ruling and the fix —
   a blocking gate on an unruled fact breaks every deploy, which is precisely what
   happened on 2026-08-26 when a rename broke a hardcoded CI guard list.
4. Any future change to the count requires a corrections-ledger entry, per the standing
   rule that facts.json changes are ledgered.

## The rule this encodes

A count that is typed by hand in more than one place will diverge. The canonical form of
a measured quantity is **the endpoint that measures it**; every surface reads from it.

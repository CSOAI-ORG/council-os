# context — firewalled contextual-signal indices

External, third-party indices that we **cite as context only**. They add
interpretive colour to what our measurements mean in the wider AI economy.
They are **never** inputs to a Council of AI signed attestation.

## The firewall doctrine (absolute)

The signed core stays pure: **SHA-256 over the instrument, Ed25519 over the
RFC-8785 canonical JSON verdict.** No model judges another; no external index,
projection, or third-party score ever crosses into that computation. The
determinism of the attestation is exactly what would be destroyed if a moving
external number could change the signed bytes — so the firewall is not a
guideline, it is a construction rule.

```
  CONTEXTUAL SIGNAL                 │   SIGNED MEASUREMENT
  (this zone)                       │   (registry/spine.json + engine)
  ───────────────────────────────── │ ─────────────────────────────────
  external indices, TAM scenarios,  │   SHA-256 of the frozen instrument
  human-baseline evals, labour      │   Ed25519 over canonical JSON
  exposure studies                  │   three-state: pass / fail / UNMEASURED
                                    │
  rendered in a SEPARATE lane,      │   the ONLY thing we sign
  labelled "contextual — not part   │   no external number ever enters here
  of the signed attestation"        │
  ═══════════════ FIREWALL ═══════════════ (one-way, cite-only)
```

### The rule for any surface that shows a contextual signal

Any contextual signal — a chart, a number, a quoted finding — MUST be rendered
in a **separate visual/data lane**, carrying the literal label:

> **contextual — not part of the signed attestation**

It may sit beside a signed verdict for interpretation, but never inside the
verdict's card, never in the bytes that are hashed, never in the JSON that is
signed. A reader must be able to tell, at a glance and in the data, which side
of the firewall a number came from.

## Why this zone exists (the estate answer)

The estate asked: *do we build our own AI-economy / human-labour /
humanoid-labour index?* The answer recorded here is **no**. We do not mint a
Council-of-AI economic or labour index — that would either (a) be an unsigned
opinion wearing our name, or (b) tempt someone to feed it into the signed core.
Instead we **cite the established external ones as context**, in a registry
(`indices.json`) that forces every entry to carry its source, and we flag every
market-size number as a projection rather than a measurement.

## Files

- `README.md` — this doctrine.
- `indices.json` — machine-readable registry of the external indices: what each
  measures, cadence, type, whether it is a projection, and a mandatory
  `citation_note`.
- `firewall.py` — stdlib-only demo: loads `indices.json`, prints every index
  under a hard `CONTEXT ONLY — not a signed input` banner, and **exits nonzero
  if any entry lacks a `citation_note`** (sourcing is enforced, not trusted).

## What is NOT here

No scores. No signing keys. No path from any file in this zone into the engine,
the harness, or `registry/spine.json`. If a future change tries to import a
value from `context/` into a signed computation, that change is wrong by
construction — reject it.

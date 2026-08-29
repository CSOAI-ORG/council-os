# council-os — the spine

One tree that binds every Council of AI measurement axis to its five organs,
with statuses that **cannot overclaim by construction**.

Council of AI is an independent AI measurement body (CSOAI Ltd, UK #16939677).
We measure AI systems against the rules that govern them, sign the result
(Ed25519 over RFC 8785 canonical JSON), and publish what we cannot yet measure.
Not a certifier. Scores are never sold. Regulators free forever.

## Public board (living)

**22 axis · 15 measured · 7 empty.** Grammar from `GET https://councilof.ai/api/gspc`
(`totals.public_count`). Empty cells stay empty. A reproduction card is not a
live CSOAI card.

The old public grammar was fourteen GSPC axes (13-of-14 until jail). That
sentence is superseded. The living API wins.

## The five organs of an axis

Every measurement axis is a vertical with the same anatomy:

1. **gold bank** — the frozen instrument (public HF dataset)
2. **harness** — the deterministic grader; no model judges another
3. **specialist** — the per-axis model lane
4. **board** — the signed public result, three-state (pass / fail / UNMEASURED)
5. **public face** — page + machine surface (MCP / A2A / AG-UI)

## The machine truth: `registry/spine.json`

Each axis has the five organs and a status from the grammar
`LIVE · LANE-REAL · LANE-REPORTED · THEORY · GATED`. The rule that makes it
honest: **only `ops/live_status_check.py` may write LIVE** — it probes every
surface from outside over public HTTP and records the evidence (URL, status,
date) next to the verdict. A LIVE without evidence fails validation. A surface
that stops resolving is downgraded to GATED with a dated note, never deleted.
Hand-edited LIVE is invalid by definition.

Last full check: 2026-08-25 — **56 organs LIVE**, specialists LANE-REPORTED
(compute lane honestly down at check time). Gold banks on Hugging Face match
the spine names (`gspc-agi` = safety, `gspc-prv` = provenance, `gspc-asi` =
continuity). Re-run the checker before promoting a specialist to LIVE.

## Binding principle: bind, don't migrate

Each lane package is a **pointer + contract + checker** over an existing repo
or surface — nothing is rewritten to join the spine. Code moves only when a
checker proves the move preserved behaviour. Current bindings include the
interop artifacts (RFC 6962 Merkle log over the signed card chain, key
lifecycle register, COSE_Sign1 expression) and the
[card conformance corpus](https://github.com/CSOAI-ORG/councilof-ai/tree/conformance-runs/docs/card-conformance)
— stdlib-only, so a stranger can verify the format without trusting us.

## Doctrine (from the master spec — violations are failures)

Everything ships signed or does not ship · never a token · scores never sold ·
regulators free forever · claims gate on signed artifacts · measurement ≠
certification · expansion never outruns the trust root.

Run the check yourself:

```
python3 ops/live_status_check.py
```

# Synthesis map — how the attestation/RWA layer snaps into the axes, benchmarks, and estate

The question: how does the XRPL/EVM attestation + tokenization work map into our axes,
benchmarks, governance, and the other estate indices — and what do we actually have vs.
not have. Honest inventory, no assumptions.

## 1. It is a NEW measurement domain, not a re-skin of the GSPC 14

The **GSPC 14 axes** measure AI *systems* against the rules that govern them
(gov, safety, provenance, continuity, conformance, openness, machinery-conformity, care,
cross-reality, detector-interop, art5, swarm, affect, jail). The **RWA attestation layer
measures tokenized financial assets** — a different subject. In the 22-axis canon (owner
ruling, commit 2bdbac34), the estate already reserves **8 financial/domain axes** beyond
the GSPC 14. **The RWA attestation coverage is the concrete instantiation of the financial
axes** — the same dialect (Ed25519 over JCS, three-state, deterministic grading, no model
judges another), pointed at a new class of subject.

So the map is: **GSPC 14 (AI systems) + financial axes (tokenized assets) = the 22.**
The attestation corpus is how the financial axes go from canon to live data.

## 2. Same spine, same honesty grammar — that's why it composes

Everything we built rides the one estate rail:
- **card format** → the conformance corpus (`docs/card-conformance`) verifies it
- **signing** → Ed25519 / scoped `cose-interop-1` (never the estate root)
- **status** → three-state (pass / fail / **UNMEASURED**) — every RWA attestation is
  UNMEASURED until a real engine run, exactly like an unmeasured GSPC cell
- **separation** → `stat_suite.separated_leaders` (Wilson-overlap vs fleet mean) is the
  SAME determination for a financial axis as for jail. The K3 finding — jail 42/71
  computes to **TIE** from published aggregates, no per-item re-run — means the public
  grammar stays honestly "13-of-14 quotable" until a financial or jail axis actually
  separates. The RWA layer inherits this rule for free.

## 3. Cross-reference against live regulation — the wiring already exists

- **`/api/locale`** (live) maps a visitor's jurisdiction → regime (EU AI Act, UK, US NIST,
  TC260, MiCA-adjacent…) + the crosswalk route. The RWA attestation for an instrument
  should carry the **applicable regime per instrument** (RLUSD → MiCA/NYDFS; Aviva → CBI
  UCITS; BUIDL → Reg D) — the `compliance/` pack + the crosswalks are the source.
- **`compliance/deadlines.json`** (live) is the dated obligation clock (AI Act GPAI Aug 2,
  CRA Sep 11). A financial-axis attestation can reference the regime *and* its live
  deadline — the "regulation-deadline feed" pattern already in the estate.

## 4. The other indices — HONEST have/don't-have

I could not exhaustively grep the (very large) workspace files this pass, so this is marked
by confidence, not asserted:
- **SOV signal / sov34 / MEOK ONE** — CONFIRMED exist (SOVOS estate spine, memory
  [[sov-estate-spine]] [[sov-mind-convergence]]). These are the *model/measurement* side,
  not a published index surface. Relationship: SOVOS is the system that could *produce*
  measurement; the financial axes are what it would measure. Not yet wired to the RWA
  corpus.
- **AI economy index / human-labour / humanoid-labour indices** — **NOT CONFIRMED as built
  surfaces.** Named as concepts; no live endpoint or dataset located this pass. Honest
  status: **aspirational / to-build**, not existing. If we want them, they are new
  financial-axis-adjacent indices built on the same corpus rail — a candidate for the
  8 financial axes' remaining slots, not something we already have.

**The honest headline: we HAVE the rail, the corpus, the 16-instrument coverage, the
jurisdiction cross-ref, and the SOVOS model side. We do NOT yet have the AI-economy /
labour indices as live products — those are net-new builds on the existing rail.**

## 5. What this unlocks (the upgrades to mine)
- Wire each RWA attestation to its **regime + deadline** (compliance pack × locale).
- Compute financial-axis **separation** with `stat_suite.separated_leaders` from published
  aggregates — no new runs needed (same unlock as jail).
- Align attestations to **W3C VC 2.0** (Recommendation May 2025) + did:web/did:xrpl so
  "stranger-verify" maps to a standards-body model, not a bespoke scheme.
- Stand up the **EAS Indexing Service** + an XRPL ingest into one store for the index-store
  query API (the paid-tier substrate).
- Track **ERC-7943 (uRWA)** as a lighter complement to the T-REX bridge.
- The AI-economy / labour indices, if wanted, are new axes on this rail — declare them in
  the registry as UNMEASURED first, never claim before measured.

# Council of AI — Live E2E Test Report

- **Target:** https://councilof.ai (LIVE production)
- **Method:** `curl -sS -m 12 -L` (real HTTP, no browser), read-only
- **Date:** 2026-08-25
- **Tester note:** This tests CURRENT live prod. A master deploy is reportedly blocked by GHA starvation, so anything thin/stale is recorded as a finding, not excused. Every claim below carries its URL + observed HTTP evidence. A 308→200 with real content is scored PASS.

## Headline

**The platform is e2e-usable TODAY for the 14 GSPC axes and for all six end-party personas — every core surface returns 200 with real, honest content and the regulator path is fully free.** The gaps are all at the edges: the 8 financial/candidate axes live only as `/interop/*.json` (no board slot, no per-axis page), the `/gspc/<axis>` "deep-dives" all serve the same board shell rather than a unique per-axis page, `/products` + `/get-measured` fall through to the homepage, white-label is badge-only (no embed.js), and the blog served one transient cold-cache soft-404 before self-correcting.

---

## PART A — the 22 axes

Board source: `GET /api/gspc` → **HTTP 200, 26,201 bytes, application/json**. Reports `totals.public_count = "14 measured of 14 quotable"`, 14 axes, all `status: MEASURED`. Financial axes are NOT on this board — they live in `/interop/financial-axes.json` + `/interop/financial-measure-run.json` (200) per the 22-axis canon (public board = 14, financial = interop/candidate layer).

Deep-dive note: every `/gspc/<axis>` returns **308→200, ~103 KB, text/html**, but all 14 share the identical `<title>` "The GSPC board — 14 measured of 14 quotable" and identical board markup; the axis-specific number (e.g. swarm 0.384) is NOT in the static HTML — it is client-rendered from `/api/gspc`. So the deep-dive is *reachable board content*, not a unique per-axis page.

### GSPC 14

| # | axis | on board? (`/api/gspc`) | deep-dive `/gspc/<axis>` | status shown | verdict |
|---|------|------|------|------|------|
| 1 | governance | YES — n=237, acc=0.70, SEPARATED | 200 (board shell) | MEASURED (honest) | PASS |
| 2 | safety | YES — n=36, acc=0.944, TIE | 200 (board shell) | MEASURED (honest) | PASS |
| 3 | provenance | YES — n=32, acc=0.781, TIE | 200 (board shell) | MEASURED (honest) | PASS |
| 4 | continuity | YES — n=33, acc=0.606, TIE | 200 (board shell) | MEASURED (honest) | PASS |
| 5 | conformance | YES — n=35, acc=0.743, TIE | 200 (board shell) | MEASURED (honest) | PASS |
| 6 | openness | YES — n=32, acc=0.875, TIE | 200 (board shell) | MEASURED (honest) | PASS |
| 7 | machinery-conformity | YES — n=33, acc=0.545, TIE | 200 (board shell) | MEASURED (honest) | PASS |
| 8 | care | YES — n=199, acc=0.535, SEPARATED | 200 (board shell) | MEASURED (honest) | PASS |
| 9 | cross-reality | YES — n=32, acc=0.812, TIE | 200 (board shell) | MEASURED (honest) | PASS |
| 10 | detector-interop | YES — n=33, acc=0.879, TIE | 200 (board shell) | MEASURED (honest) | PASS |
| 11 | art5-safeguard | YES — n=36, acc=0.972, TIE | 200 (board shell) | MEASURED (honest) | PASS |
| 12 | swarm | YES — n=37, acc=0.384, SEPARATED | 200 (board shell) | MEASURED (honest) | PASS |
| 13 | affect | YES — n=41, acc=0.878, SEPARATED | 200 (board shell) | MEASURED (honest) | PASS |
| 14 | jail | YES — n=71, acc=0.5915, TIE | 200 (board shell) | MEASURED (honest) | PASS |

`totals`: 14 measured of 14 quotable, 887 items, 4 separated leads, 10 ties, `untested_separations: 0`, mean_macro_f1 0.753. License CC-BY-4.0. `note` states "Measurement, not certification." — honest framing intact.

### Financial / candidate 8

Source: `/interop/financial-axes.json` (200, 4470 B) + `/interop/financial-measure-run.json` (200, 5079 B, Ed25519-signed control facts) + `/interop/rwa-registry.json` (200, 5707 B, counts: 16 named / 6 verified+attested / 10 not-located, every entry UNMEASURED honest).

| # | axis | on board? | deep-dive `/gspc/<axis>` | status shown | verdict |
|---|------|------|------|------|------|
| 15 | provenance-controls | interop only (not `/api/gspc`) | **404** | MEASURED — deterministic on-chain facts, signed v2 run, `risk_verdict: UNMEASURED (needs counsel)` (honest) | DEGRADED |
| 16 | reserve-attestation | interop only | **404** | UNMEASURED (honest) | DEGRADED |
| 17 | regulatory-framework | interop only | **404** | UNMEASURED (honest) | DEGRADED |
| 18 | distribution-integrity | interop only | **404** | UNMEASURED (honest) | DEGRADED |
| 19 | custody-disclosure | interop only | **404** | UNMEASURED (honest) | DEGRADED |
| 20 | ai-economy-index | interop only | **404** | **`MEASURED-INDEX-v0.1`** in axes list, but same file's `honesty` says this candidate is UNMEASURED — **self-contradiction** | DEGRADED |
| 21 | human-labour-index | interop only | **404** | **`MEASURED-INDEX-v0.1`** vs `honesty` UNMEASURED — **self-contradiction** | DEGRADED |
| 22 | humanoid-labour-index | interop only | **404** | UNMEASURED (honest) | DEGRADED |

**Financial verdict:** the *control-facts* axis (provenance-controls) is genuinely MEASURED and signed (RLUSD/OUSG mainnet flags, devnet carrier tx, COSE signer `cose-interop-1`), and the RWA coverage layer is scrupulously honest ("Nothing is faked to reach a count"). But NONE of the 8 have a board slot or a reachable per-axis page (`/gspc/<axis>` 404), so a human's axis journey dead-ends at raw JSON. Axes 20–21 carry a status string (`MEASURED-INDEX-v0.1`) that directly contradicts the honesty note in the same file — the one honesty defect in Part A.

---

## PART B — end-party personas

| persona | path | evidence | verdict |
|---|---|---|---|
| **REGULATOR (free)** | `/api/gspc` 200 (26 KB json), `/api/corrections` 200 (10 KB, has `signature`), `/api/regulation` 200 (10 KB, deadlines+disputed+underwriting_note), `/gspc-verify` 308→200 (68 KB, ed25519×6, signature×3), `/honesty` 308→200 (70 KB), `/methodology` 308→200 (78 KB) | all reachable, **no auth, no paywall, no Stripe** | **PASS** |
| **ENTERPRISE / buyer** | `/products` 308→200 but **byte-identical to homepage (238,804 B)** — falls through to root; `/get-measured` 308→200 **also byte-identical to homepage**; `/assess` 308→200 (70 KB, distinct RAS page, "assess"×12, ed25519×2). Price scan on products: stripe=0, pricing=0, paywall=0, checkout=0 | honest (no fabricated numbers, no public prices) but `/products` + `/get-measured` are NOT dedicated pages | **DEGRADED** |
| **INSURER / auditor** | `/evidence` 308→200 (93 KB, ed25519×6, did:web×7), `/live-ledger` 308→200 (108 KB, corrections ledger), `/refutation-ledger` 200 (72 KB, "refut"×20), `/gspc-verify` 200 (signature×3, ed25519×6) | signed evidence reachable + verifiable | **PASS** |
| **DEVELOPER / AGENT** | `/.well-known/agent.json` 200 (valid JSON: name/capabilities/skills/`explicitly_not`), `/.well-known/did.json` 200 (valid DID doc, verificationMethod+assertionMethod), `/.well-known/scitt.json` 200 (valid: standards/trust_anchor/statements), `/llms.txt` 200 (text/plain), `/api/mcp` 200 (valid JSON, 6 servers: Assess/Anchors/Ledger/Watchdog/Spectrum/Drift) | all real machine-consumable JSON | **PASS** |
| **THE PUBLIC** | `/` 200 (239 KB, title "we measure, we sign, we re-attest"), `/os` 200 (107 KB, title "Council OS — the Council hub", council os×11), `/blog/scitt-ai-supply-chain-transparency` — **served a soft-404 shell on first hit (HTTP 200 but title "404 — Not found", 0 SCITT mentions), then self-corrected**; 6/6 subsequent hits REAL (66,681 B, "SCITT and AI Supply Chain Transparency…"). Sitemap confirms 22 valid blog slugs. | reachable + real, minus one transient cold-cache miss | **PASS (with reliability caveat)** |
| **INTEROP / standards** | `/xrpl-attest` 308→200 (80 KB), `/interop/rwa-registry.json` 200 (5.7 KB, every status UNMEASURED, honest coverage-only) | attestation story reachable + honest UNMEASURED coverage | **PASS** |

---

## PART C — white-label / embed readiness

| surface | result | note |
|---|---|---|
| `/api/badge` | **200, image/svg+xml, 1303 B** | Works. Shields-style badge, `aria-label="GSPC: 14 measured of 14 quotable"`, green. A third party CAN hotlink `<img src="https://councilof.ai/api/badge">` today. |
| `/badge` (HTML page) | **404** | No human-facing badge/embed landing page. |
| `/embed.js` / `/badge.js` | **404 / 404** | No drop-in embed script. |
| `/api/embed` | **404** (json 160 B) | No embed API. |
| `/gspc-verify` (+ `/verify` alias 200) | **200** | Verify-a-card path exists and is signed (ed25519×6, signature×3). |
| "Powered by Council OS" text | not found in badge SVG or products page | No explicit white-label attribution primitive. |

**White-label verdict: PARTIAL / largely TODO.** The building blocks a third party needs to *show a verdict* exist — a live SVG badge (`/api/badge`) plus a signed verify page (`/gspc-verify`). What's missing for a real white-label deployment: (1) a copy-paste `embed.js` / iframe snippet, (2) a per-card/per-issuer parameterised badge (the badge is a single global "14 of 14", not embeddable per-verdict), (3) a "Powered by Council OS" attribution surface, (4) any `/badge` HTML landing to onboard an embedder. Honest status: **embeddable badge yes, embeddable *signed verdict* no.**

---

## TOP BREAKS (worst first, by e2e end-party impact)

1. **Financial axes 15–22 have no reachable axis journey.** `/gspc/<axis>` 404s for all 8 and they're absent from the `/api/gspc` board — a user following the 22-axis story hits raw `/interop/*.json` or a 404. Half the canon is invisible to a non-developer.
2. **Honesty self-contradiction in `financial-axes.json`.** `ai-economy-index` and `human-labour-index` are tagged `MEASURED-INDEX-v0.1` while the same file's `honesty` note says those candidates are UNMEASURED with "NO rubric and NO data yet." This is exactly the false-success trap the estate guards against — a status string over-claiming vs the honesty note.
3. **`/gspc/<axis>` deep-dives are a shared board shell, not per-axis pages.** All 14 return the identical board HTML; the per-axis number is only client-rendered from the API. No unique per-axis narrative/evidence page exists server-side (weak for AEO and for deep-linking a single axis).
4. **`/products` and `/get-measured` fall through to the homepage** (byte-identical 238,804 B). The enterprise buyer's two named entry points aren't dedicated pages — the journey lands on the root marketing shell.
5. **Blog cold-cache soft-404 (intermittent).** The named AEO slug returned HTTP 200 with 404 content on the first request, then served real content on 6/6 retries. One-in-N cold hits can serve a 404 shell for a valid, sitemap-listed post — bad for a first-time visitor or a crawler.
6. **White-label is badge-only.** No `embed.js`, no per-verdict parameterised badge, no `/badge` onboarding page — a third party cannot embed a *signed verdict* yet, only a global status badge.

None of the above blocks the two highest-stakes journeys: the **regulator path is 100% free and reachable**, and the **developer/agent + insurer/auditor signed-evidence paths are fully live**.

---

## Evidence appendix (raw observations)

- `/api/gspc` → 200, 26,201 B, `totals.public_count="14 measured of 14 quotable"`, 14 axes all MEASURED.
- 14× `/gspc/<axis>` → 308→200, ~103 KB, identical `<title>`; `/gspc/gov` alias → **404**.
- 8× financial `/gspc/<axis>` → **404** (1258 B shell).
- `/interop/financial-axes.json` 200: provenance-controls=MEASURED; reserve/regulatory/distribution/custody=UNMEASURED; ai-economy + human-labour=`MEASURED-INDEX-v0.1`; humanoid=UNMEASURED.
- `/interop/financial-measure-run.json` 200: signed (`signer_kid: cose-interop-1`), RLUSD + OUSG mainnet control facts, risk verdicts UNMEASURED.
- `/interop/rwa-registry.json` 200: 16 named / 6 verified+attested / 10 not-located, all UNMEASURED.
- Regulator: `/api/gspc` `/api/corrections` `/api/regulation` `/gspc-verify` `/honesty` `/methodology` all 200, no auth.
- Dev JSON: agent.json / did.json / scitt.json / api/mcp all valid JSON (parsed); llms.txt text/plain.
- `/api/badge` 200 SVG; `/badge` `/embed.js` `/badge.js` `/api/embed` all 404.
- `/blog` 200 (title "Blog | CSOAI"); sitemap.xml 200 lists 22 blog slugs; named slug REAL 6/6 after one transient 404.

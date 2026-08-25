# Council of AI — Live E2E RETEST #2 (post-569-route deploy)

- **Target:** https://councilof.ai (LIVE production)
- **Method:** `curl -sS -m 12 -L` (real HTTP, no browser), read-only
- **Date:** 2026-08-25
- **Baseline:** `E2E-TEST-REPORT.md` (same day, pre-deploy). This report measures the DELTA after the fresh full deploy (569 routes, new router).

## Headline

**The deploy fixed the one honesty defect — all three candidate indices now read UNMEASURED — and the blog served 4/4 AEO slugs real on first hit; everything else moved sideways: financial axes still 404 and off-board, deep-dives still a shared board shell (now with per-axis canonicals and an "archive" banner), /products and /get-measured still the homepage, white-label still badge-only — and the six-persona regression sweep is fully green with two NEW homepage-fallthrough routes found (/badges, /verify-certificate).**

Router note: every route that previously answered `308→200` now answers a direct `200` — the new router serves without the redirect hop.

---

## Delta table — previous TOP BREAKS, retested

| # | break | previous state | NOW (evidence) | verdict |
|---|-------|----------------|----------------|---------|
| 1 | Financial axes 15–22 unreachable | all 8 `/gspc/<axis>` 404, absent from `/api/gspc` | All 8 still **404** (1258 B shell each): provenance-controls, reserve-attestation, regulatory-framework, distribution-integrity, custody-disclosure, ai-economy-index, human-labour-index, humanoid-labour-index. `/api/gspc` → 200, 26,241 B, still exactly 14 axes (`public_count: "14 measured of 14 quotable"`), none of the 8 on board. | **SAME** |
| 2 | Honesty self-contradiction in `financial-axes.json` (`MEASURED-INDEX-v0.1` vs honesty note) | ai-economy-index + human-labour-index tagged `MEASURED-INDEX-v0.1` while honesty note said UNMEASURED | `GET /interop/financial-axes.json` → 200, 4,697 B. **ai-economy-index → UNMEASURED, human-labour-index → UNMEASURED, humanoid-labour-index → UNMEASURED.** `grep -c "MEASURED-INDEX"` = 0. Honesty note now reads: "3 candidate axes … have NO rubric and NO data yet — declared UNMEASURED so the slot is honest and public, never claimed as built." provenance-controls stays MEASURED (correct); the other 4 financial axes stay UNMEASURED (correct). **The hot-patch held.** | **FIXED** |
| 3 | `/gspc/<axis>` deep-dives = shared board shell | all 14 identical `<title>` + identical markup; axis number client-rendered only | `/gspc/governance` 200 (103,287 B) and `/gspc/jail` 200 (103,248 B): `<title>` still identical ("The GSPC board — 14 measured of 14 quotable"); jail's 0.59 accuracy NOT in static HTML (`grep -c "0.59"` = 0); body diff is only per-axis `canonical`/`og:url`/`twitter:url` + per-axis breadcrumb JSON-LD. NEW: both pages carry a "Reference / archive" banner ("A dated reference page, kept for the record… start at the measurement board") — the shell is now honestly labelled an archive, and canonicals are per-axis (SEO plumbing improved), but there is still no per-axis prerendered content. | **SAME** (marginally better: per-axis canonicals + honest archive framing) |
| 4 | `/products` + `/get-measured` homepage fallthrough | both byte-identical to `/` (238,804 B) | `/` = `/products` = `/get-measured` = **200, 238,827 B each**, identical `<title>` "Council of AI — we measure, we sign, we re-attest"; the only byte diffs are Cloudflare email-protection hashes (random per fetch). Still fallthrough. **NEW same-class breaks found:** `/badges` (sitemap-listed) → 200, 238,827 B, homepage title; `/verify-certificate` (sitemap-listed) → 200, 238,827 B, homepage title. | **SAME** (and 2 new instances) |
| 5 | Blog cold-cache soft-404 | 1 transient HTTP-200-with-404-shell on first hit of a valid slug | First-hit cold checks on 4 AEO slugs, all REAL: scitt-ai-supply-chain-transparency 200/66,774 B; iso-42001-vs-etsi-en-304-223 200/65,947 B; fedramp-oscal-september-30-mandate 200/66,447 B; verified-measurement-credential-how-to-verify 200/66,273 B — each with the correct article `<title>`, zero soft-404s. (Intermittent by nature; 0/4 observed this run.) | **FIXED** (as observed) |
| 6 | White-label badge-only | `/api/badge` 200 SVG; no embed.js / badge page / per-verdict badge | `/api/badge` → 200, image/svg+xml, 1,303 B, `aria-label="GSPC: 14 measured of 14 quotable"` — still works. `/badge`, `/embed.js`, `/badge.js`, `/embed`, `/verify-embed`, `/embed-kit`, `/white-label`, `/interop/embed.js` all **404**; `/api/embed` 404. No new embed surface reachable despite the "verify embed kit" commit; `/gspc-verify` contains 0 mentions of "embed". `/badges` in the sitemap serves the homepage (see #4). | **SAME** |

---

## Regression sweep — six personas' key surfaces

All previously-passing surfaces still 200 with real content (and now direct 200, no 308):

| surface | NOW | note |
|---|---|---|
| `/api/gspc` | 200, 26,241 B json | 14 axes, all MEASURED, 887 items, honest totals + license note |
| `/api/corrections` | 200, 10,367 B json | valid JSON, `signature` key present (6× "signature") |
| `/api/regulation` | 200, 10,172 B json | valid JSON, verified_as_of + corrections_policy |
| `/gspc-verify` | 200, 68,108 B | title "Verify the chain — recompute it yourself, client-side", Ed25519×6, signature×3 |
| `/honesty` | 200, 69,753 B | reachable |
| `/methodology` | 200, 77,913 B | reachable |
| `/.well-known/agent.json` | 200, 3,464 B | valid JSON (name/capabilities/supportedInterfaces) |
| `/.well-known/did.json` | 200, 3,498 B | valid JSON DID doc (verificationMethod/assertionMethod) |
| `/.well-known/scitt.json` | 200, 4,159 B | valid JSON (standards/trust_anchor/statements) |
| `/llms.txt` | 200, 2,829 B text/plain | reachable |
| `/api/mcp` | 200, 2,119 B json | valid JSON, `servers` + `count` |
| `/evidence` | 200, 92,817 B | reachable |
| `/live-ledger` | 200, 108,376 B | reachable |
| `/refutation-ledger` | 200, 72,322 B | reachable |
| `/xrpl-attest` | 200, 80,015 B | reachable |
| `/assess` | 200, 70,845 B | distinct RAS page |
| `/os` | 200, 106,889 B | title "Council OS — the Council hub", "council os"×11 |
| `/` | 200, 238,827 B | title "we measure, we sign, we re-attest" |

**No previously-passing surface regressed.** New breaks introduced by the deploy: none found on the persona paths; the only new findings are the two extra homepage-fallthrough routes (`/badges`, `/verify-certificate`) — both sitemap-listed, both serving the root shell.

---

## New-money checks

| check | result | evidence |
|---|---|---|
| Homepage hero nav-align wording | **PRESENT** | Static `/` HTML contains "Council of AI — the unsolicited, permissionless measurement body for AI behaviour" in the hero badge, plus "Permissionless attach: we bind signed measurement evidence to accounts we…" lower down. |
| "Ledger attestation" OS tile | **PRESENT in shipped JS** | Main bundle `/assets/index.r2-D90-Y-uQ.js` (200, 1,262,808 B) contains `"/xrpl-attest":"Ledger attestation | Council of AI"` (route-title map). Not in `/os` static HTML (JS-rendered), so tile text verified via the bundle only. |
| EnforcementTimeline Omnibus-correct | **CONTENT CORRECT; literal aria-label not located** | Lazy chunk `/assets/ActTimeline.r2-DzKCnkhb.js` (200) and static `/ai-act-timeline` (200, 69,207 B, title "EU AI Act timeline - every enforcement date") both carry "high-risk obligations from 2 December 2027 (Annex III) and 2 August 2028 (Annex I), as amended by the Digital Omnibus (Reg (EU) 2026/1744)". No static string literal `aria-label` containing "Dec 2027 Annex III" was found in the main bundle, ActTimeline chunk, PublicHome chunk, or any fetched HTML — if the aria-label exists it is runtime-constructed; the user-visible enforcement dates are Omnibus-correct everywhere they appear. |

---

## Evidence appendix (raw observations, this run)

- 8× financial `/gspc/<axis>` → 404, 1,258 B each.
- `/interop/financial-axes.json` → 200, 4,697 B; statuses: provenance-controls MEASURED; reserve-attestation / regulatory-framework / distribution-integrity / custody-disclosure UNMEASURED; ai-economy-index / human-labour-index / humanoid-labour-index **UNMEASURED**; zero "MEASURED-INDEX" strings.
- `/api/gspc` → 200, 26,241 B; 14 axes; `public_count "14 measured of 14 quotable"`; new `license_note` + `mean_note` fields present (honest framing extended).
- `/gspc/governance` vs `/gspc/jail`: 103,287 B vs 103,248 B; identical titles; diffs limited to canonical/og/twitter URLs + breadcrumb JSON-LD + "Reference / archive" banner on both; no per-axis numbers in static HTML.
- `/` `/products` `/get-measured` `/badges` `/verify-certificate` all 200 at 238,827 B with the homepage title; `/verify-leaderboard` (200, 65,818 B) and `/start` (200, 64,504 B) are real dedicated pages.
- 4× `/blog/<slug>` first hits all real with correct article titles (66–67 KB each).
- `/api/badge` 200 SVG 1,303 B; `/badge` `/embed.js` `/badge.js` `/embed` `/verify-embed` `/embed-kit` `/white-label` `/interop/embed.js` 404; `/api/embed` 404.
- Persona sweep: 18/18 surfaces 200 (table above); all 6 JSON surfaces parse as valid JSON.
- Router: zero 308s observed anywhere this run (previously `/gspc/*`, `/honesty`, `/methodology`, `/products` etc. were 308→200).

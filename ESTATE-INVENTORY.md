# Council of AI — Estate Inventory

**Checked:** 2026-08-25 (read-only audit; live HTTP via `curl -sS -m 12`, no browser).
**Scope:** what the estate HAS live right now vs. what is broken/degraded vs. the honest next gaps.
**Method note:** every claim below carries the URL + HTTP code observed today. Redirects are recorded with the `-L` final result. This doc did not touch any councilof-ai client code.

---

## LIVE — verified today, with HTTP evidence

### Domains & apex redirect
- `https://councilof.ai/` → **HTTP 200** (no redirect; canonical origin).
- `https://csoai.org/` → **HTTP 308** → `https://councilof.ai/` → **200** (clean single-hop redirect).
- **The recurring 522 apex issue is NOT present today.** `csoai.org` resolves and 308-redirects cleanly to `councilof.ai`. No 522, no timeout.

### The board — GSPC now says "14 measured of 14"
- `https://councilof.ai/api/gspc` → **HTTP 200**, `application/json`, real JSON (`schema: csoai.gspc-axes/0.5`).
- **The jail-separation sweep has flipped the grammar.** Exact `totals` block returned today:
  - `axes: 14`, `measured_axes: 14`, `quotable_axes: 14`
  - **`public_count: "14 measured of 14 quotable"`** (was previously "13 of 14")
  - `items: 887`, `separated_leads: 4`, `ties: 10`, `untested_separations: 0`
  - `mean_macro_f1: 0.7528`, `mean_accuracy: 0.7318`, `mean_fleet_mean: 0.5447`, `mean_harm: 0.4877`
  - `license: CC-BY-4.0`
- Slot counts are stated as derived (`"derived, never typed"`); jail (slot 14) carries its own 7-model fleet and is flagged `UNTESTED` for McNemar separation on the axis itself. Living stamp present (`board_living.json`, signed, updated `2026-08-18T03:22:16Z`).

### Machine surfaces — `councilof.ai` (full parity, all real JSON)
- `/.well-known/agent.json` → **200**, `application/json`, **REAL-JSON** ("Council of AI — Measurement Agent", GSPC 14-slot).
- `/.well-known/did.json` → **200**, `application/json`, **REAL-JSON** (W3C DID context, JWS-2020 suite).
- `/.well-known/scitt.json` → **200**, `application/json`, **REAL-JSON** (`csoai.scitt-profile/0.1`).
- `/llms.txt` → **200**, `text/plain`, real content (CSOAI Ltd, did:web:csoai.org, neutral measurement).

### Machine surfaces — `csoai.org` (near-parity; one gap, see BROKEN)
- `/.well-known/agent.json` → **200**, `application/json`, **REAL-JSON** ("CSOAI Measurement Agent").
- `/.well-known/did.json` → **200**, `application/json`, **REAL-JSON**.
- `/llms.txt` → **200**, `text/plain`, real content ("llms.txt — https://csoai.org").

### Session's new surfaces (councilof.ai)
- `/api/locale` → **200**, real JSON (`csoai.locale/0.1`; detected country GB → regime `uk`).
- `/interop/rwa-registry.json` → **200**, real JSON (`csoai.rwa-registry/0.1`, chain XRPL).
- `/interop/attestation-corpus.json` → **200**, real JSON (`csoai.attestation-corpus/0.1`).
- `/interop/financial-measure-run.json` → **200**, real JSON (`csoai.financial-measure-run/0.1`, axis `provenance-controls`).
- `/interop/financial-axes.json` → **200**, real JSON (`csoai.financial-axes/0.1`; the 8 financial axes of the 22-axis canon = GSPC-14 + 8).
- `/xrpl-attest` → **308** → `/xrpl-attest/` → **200** `text/html` (real SPA page, client-rendered).
- `/gspc-verify` → **308** → `/gspc-verify/` → **200** `text/html` (real SPA page, client-rendered).

### Trust / data feeds (councilof.ai)
- `/api/corrections` → **200**, real JSON (`csoai.corrections/0.1`; **15 correction entries**; append-only policy).
- `/api/regulation` → **200**, real JSON (`csoai.regulation-deadlines/0.1`; **20 deadlines**; `verified_as_of: 2026-08-19`, quarterly re-verification). *(It exists.)*
- `/signed/card_index.json` → **200**, real JSON (`csoai.gspc-card-index/0.1`; **n_cards 335, n_cells 335**; `pubkey d4cb0eaa16d5f50bf763…` present).

### HF datasets — all resolve (200)
- `huggingface.co/api/datasets/csoai/gspc-gov` → **200** (downloads 172, lastModified 2026-08-19T12:45Z).
- `…/csoai/gspc-jail` → **200** (downloads 101, lastModified 2026-08-19T11:23Z).
- `…/csoai/gspc-care` → **200** (downloads 187, lastModified 2026-08-19T11:22Z).

### MCP registry / catalogue (councilof.ai)
- `/api/mcp` → **200**, real JSON. Server catalogue lists **6 servers**: `csoai-assess`, `csoai-anchors`, `csoai-ledger`, `csoai-watchdog`, `csoai-spectrum`, `csoai-drift`.
- `/.well-known/mcp.json` → **200**, real JSON (`schema_version 2026-07-28`, name `csoai`).
- (Prior context: `io.github.CSOAI-ORG/gspc` listed in the public MCP registry — not re-fetched here; the two local catalogue endpoints above are live and confirmed today.)

---

## BROKEN / DEGRADED — non-200 or shell-only, with exact url+code

- **`https://csoai.org/.well-known/scitt.json` → HTTP 404** (`text/html`, HTML shell, not JSON).
  This is a **parity gap**: the SCITT profile is served on `councilof.ai` (200 real JSON) but **404 on the `csoai.org` mirror**. did.json and agent.json are present on both domains; scitt.json is present only on councilof.ai. Anything resolving the SCITT profile via the `csoai.org` host will 404.

*No other surface checked today returned a non-200 or an empty/shell-only body. The three 308s (`/xrpl-attest`, `/gspc-verify`, `/products`) are intentional redirects that terminate in 200 responses, not failures.*

---

## NEXT — honest gaps (declared UNMEASURED, owner gates, or stale/ambiguous)

- **`/products` is not a standalone page.** `https://councilof.ai/products` → **308** → `/?lobby=measured&task=enterprise-start` → **200**. It is an *alias/redirect into the enterprise-start lobby*, not a distinct products surface. If a real `/products` catalogue is intended, it does not exist yet — the path only forwards to the home lobby with a task param.

- **Jail (GSPC slot 14) separation is declared UNTESTED.** The board's own note states jail separation is `UNTESTED (no McNemar run yet)` and its bank is `pending publication`. The public grammar counts it as measured ("14 of 14"), but its statistical separation is honestly flagged as not yet run — this is a declared open item, not a silent claim.

- **`card_index.json` has a pubkey but no top-level detached signature field.** `pubkey` is present (`d4cb0eaa…`) and `n_cards`/`n_cells` match (335/335), but there is no top-level `sig`/`signature` key in the payload fetched today. If signatures are per-cell or shipped in a sidecar, that is fine — but the top-level index itself carries the key, not a self-signature. Worth confirming the verify path (a human-facing verifier lives at `/gspc-verify/`).

- **SCITT parity must be closed on `csoai.org`.** See BROKEN: the `csoai.org` scitt.json 404 should be brought to parity with councilof.ai, or the did:web/agent metadata should point SCITT resolution only at the councilof.ai host.

- **`slot15` / `human-vs-ai` are measured in-lane only.** Per the board note, these live in `measured_in_lane`, not on the public board — an explicit UNMEASURED-on-board boundary, correctly not conflated with the 14-slot.

- **Regulation feed re-verification cadence is a standing owner gate.** `/api/regulation` is `verified_as_of 2026-08-19` with quarterly + on-provision re-verification. It is fresh today but is a recurring human-verification obligation (20 deadlines tracked), not an automated guarantee.

- **Two agent.json identities differ across domains.** councilof.ai = "Council of AI — Measurement Agent"; csoai.org = "CSOAI Measurement Agent". Both are real JSON and valid, but the naming is not identical across the mirror — a cosmetic/consistency gap to reconcile if a single canonical agent identity is intended.

---

*Generated by a read-only estate audit. Where a check was ambiguous (e.g. card_index signature location, MCP registry entry not re-fetched) it is stated as such rather than asserted. No client code was modified.*

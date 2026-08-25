# LIVE-GAP-AUDIT — public-safe content that exists but is not on councilof.ai

**Date:** 2026-08-25
**Auditor:** autonomous read-only audit (no deploy, no live-site changes)
**Live front end:** councilof.ai (React app — `/Users/nicholas/clawd/councilof-ai/client`)
**Sources searched:** `csoai-static-deploy2` (retired DSH static repo), DSH harness UI at `127.0.0.1:3090`, CSOAI-ORG GitHub (repos + open PRs), live councilof.ai routes.

---

## TL;DR — honest framing

Most of the DSH tree (`csoai-static-deploy2`, 9.1 GB) is **build-output, model artifacts, internal harness code, backups, and internal-codename strategy docs** — not front-end content, and much of it is not public-safe. The DSH harness at `127.0.0.1:3090` is just the **DeepSeek Harness chat UI** (an agent runner), not a content producer — nothing there to surface.

After filtering for *public-safe + real + not-already-live*, there are **three genuine gems** and a set of **open-source repos worth linking**. Everything else valuable in the tree is contaminated by banned internal codenames (`sovereign`/`sov33`/etc.) and must NOT be surfaced.

The single highest-value, cleanest, ready-to-ship item is the **~22 AEO regulatory-explainer seed pages** — clean, real, regulator-targeted, and directly compatible with the existing `/blog` content pipeline.

---

## PRIORITIZED "ADD TO LIVE" LIST

| # | Item | Where it is now | Why it's valuable | Public-safe? | Concrete action to add to live |
|---|------|-----------------|-------------------|--------------|-------------------------------|
| **1** | **AEO regulatory-explainer seed pages (~22)** — ISO 42001 vs ETSI EN 304 223, SCITT & AI supply chain, FedRAMP OSCAL Sept-30 mandate, Council of Europe AI Framework Convention, Colorado AI Act chatbot timeline, NIST AI 600-1 profile, BSI ART/1, Third-Party Audit SS 584 / ISAE 3000, EU AI Act Art 5 & Art 50(2), High-Risk provider obligations, "What is Monitored Containment", "Verified Measurement Credential — how to verify", Council Signal explainer | `csoai-static-deploy2/SOVOS/cross-lab-runs/2026-08-14/aeo-*.json` | AEO/SEO answer-engine content aimed squarely at regulators, procurement officers, compliance leads. Each cites real standards. Honest voice ("measurement not certification"). **Codename-scan: 0 hits — all clean.** These topics are NOT dedicated pages on live today (scitt/framework-convention/colorado/containment/ss584/nist-ai-600 all 404 or absent from blog dataset). | **Y** — verified clean via banned-string sweep across all 22 files (0 matches). Content is standards-explainer prose with public references only. | Convert each `aeo-*.json` → a `BlogDataEntry` in `client/src/data/blog-content.ts` (or a new `answers-content.ts` dataset) with a `/blog/<slug>` (or new `/answers/<slug>`) route via the existing `ContentPage` renderer in `client/src/App.tsx`. Add slugs to `scripts/prerender.mjs` URL list + `scripts/generate-sitemap.mjs`. Run through `scripts/brand-gate.mjs` before deploy. De-dupe against existing ISO-42001/Article-50 blog coverage. |
| **2** | **Measurement methodology white paper** | Open PR **#611** (`feat/methodology`) on `CSOAI-ORG/councilof-ai` | Documents the deterministic-grading + Wilson-CI + McNemar-separation method — the credibility backbone / competitive moat vs LMArena. Clean, public-facing docs. | **Y** — it's a docs PR already branched against the public site repo. | Review + merge PR #611. Confirm it renders at a `/methodology` route (live `/methodology` currently 308-redirects — verify target). Brand-gate on merge. |
| **3** | **Containment Incident Index** (5 incidents, primary-sourced register) | `csoai-static-deploy2/SOVOS/containment-index/index.json` (also GitHub `CSOAI-ORG/corpus-watch`-adjacent) | A signed, public-primary-sourced register of AI containment/sandbox-escape incidents — a natural companion to the "Monitored Containment" explainer (#1) and a genuinely differentiated data asset. Doctrine is honest ("counts are counts, not rates; measurement not certification"). Codename-scan: 0 hits. | **Y on codenames**, but **VERIFY-FIRST** — see caveat below. | Do NOT ship blind. First independently verify each of the 5 incidents against its cited primary source (they name real orgs — OpenAI, Anthropic, AISI, Moonshot/Kimi — and dates are 2026-07, beyond auditor's knowledge cutoff). If all citations check out, surface as a `/containment` data page fed by the JSON, brand-gated + prerendered. If any citation is unverifiable, hold. |
| **4** | **Open-source tool repos worth linking from live** — `inspect-receipts` (Ed25519 receipts for Inspect AI eval runs), `claimguard` (claim-vs-signed-artifact integrity checker), `corpus-watch` (regulatory drift hash-watcher over EU AI Act CELLAR / UK statute), `awesome-a2a` | `CSOAI-ORG` GitHub (all pushed 2026-08-23/24/25, all with "measurement, not certification" honest descriptions) | Real, public, Apache/MIT-spirit repos that prove the estate ships open tooling — credibility + developer funnel. None are currently linked from a live "open source / tools" surface. | **Y** — repo names + descriptions are codename-clean and already public on GitHub. | Add an "Open Source / Tools" section or cards to an existing live page (e.g. an existing tools/ecosystem route) linking these GitHub repos. No content migration needed — just curated outbound links + one-line honest descriptions. |

---

## Secondary / lower-confidence (surface only after cleanup)

- **CRA SBOM (CycloneDX 1.5)** — `SOVOS/attestation-engine-bom.json`. The *concept* (CRA-readiness SBOM for the attestation engine, XRPL/EAS pinned deps, CVE-2025-32965 remediation) is publishable and credible, **but the file itself contains `sovereign` in a component field** → fails the banned-string gate. Would need a scrubbed rebuild before it could go live. Not shippable as-is.
- **Regulation-deadline / GPAI enforcement facts** — the *dates and obligations* in `SOVOS/EU-AI-ACT-GPAI-MAP-2026-08-25.md` (Art 53/55 enforcement live 2 Aug 2026, fines €15M/3% and €35M/7%) are public and could feed the existing reg-watch feed, **but the source doc names the internal `sov33`/`sovereign` fleet** → exclude the doc; only the public regulatory facts (re-authored from primary EUR-Lex) may be used.

---

## DO NOT SURFACE — internal-codename content (hard-excluded)

These exist in the tree and are real, but carry banned public strings (`sovereign`, `SOVOS`, `sov3`/`sov34`, `sigil`, `ceasai`, `byzantine`, `dorado`, `cibola`) and must never reach the public front end:

- **Signed measurement cards** `SOVOS/evidence/signed/card-csoai-0001..0006.json` and `card-csoai-revenue-001.json` — subject is `sov33-ultimate-sovereign:latest`, signer `sov33-owem-micro`. Real Ed25519-signed VALID cards, but the subject/signer names are banned. (If genuine measurement cards are ever wanted on the board, they must measure **public-named** models, not the internal lineage.)
- **New benchmark results** `benchmark-results/eat_govbench_sovereign_*.json`, `eat_govbench_sov33_repro_*.json`, `round_1_sov33-*` — banned subject names.
- **EU AI Act GPAI vendor map** `SOVOS/EU-AI-ACT-GPAI-MAP-2026-08-25.md` — names the `sov33`/`sovereign` fleet.
- **Attestation-engine SBOM** `SOVOS/attestation-engine-bom.json` — `sovereign` in a component (see Secondary above).
- **Internal strategy/spec docs** `SOVOS/SOVOS-MASTER-PART-A/B.md`, `MASTER-BUSINESS-PLAN`, `MONOREPO-MASTER-SPEC`, `LEGAL-COUNSEL-BRIEF`, `CURSOR-HANDOFF`, `COMPETITOR-DATABASE`, `CSOAI-MASTER-PLAYBOOK` — internal by nature.
- **Internal repos** on CSOAI-ORG: `sovos-harness`, `sim-world-estate`, `meok-bft-verifier` (SOV3), and the repo literally named **`cibola`** (banned codename) — do not link by name from live, regardless of clean descriptions.
- Note: live pages `AboutCEASAI.tsx` / `CEASAITraining.tsx` already ship the banned string `ceasai` — pre-existing, out of scope for this audit, but flagged here for the record.

---

## Method notes

- Banned-string sweep run over every candidate: `grep -liE 'sovereign|SOVOS|sov3|sov34|sigil|ceasai|byzantine|dorado|cibola'`. AEO pages (22 files) and containment index → **0 hits**. Signed cards, GPAI map, SBOM, eat_govbench results → **hits → excluded**.
- Live-vs-candidate cross-check: probed councilof.ai routes and `blog-content.ts` (25 entries). AEO topics scitt / framework-convention / colorado / containment / ss584 / nist-ai-600 / bsi-art are absent from the live blog dataset and 404 as routes → genuine net-new coverage.
- DSH harness `127.0.0.1:3090` = DeepSeek Harness chat UI (`<title>DeepSeek Harness</title>`, DSH client-module boot), no content API. Nothing to surface.

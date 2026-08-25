# STACK vs MARKET — deep strategic cross-reference + what to do NOW

**Date:** 2026-08-25
**Author:** autonomous strategic research pass (read-only over the estate; live WebSearch for current events)
**Method:** every market claim below carries a source + date. Every "move" is tagged by gate:
**[NOW]** = permission-free, do today · **[OWNER]** = needs a key/counsel/owner decision · **[BUILD]** = real engineering effort.
Honest throughout: a named-security *verdict* is never shipped without counsel; an index is never claimed before it is measured.

---

## 1. What we HAVE (the asset summary)

Council of AI (CSOAI Ltd, UK #16939677, trading as MEOK AI Labs) is an independent **measurement & attestation body** — not a certifier, not an issuer, never "credit rating." The stack, honestly inventoried: **(a) 22-axis measurement** — GSPC-14 for AI systems (governance, safety, provenance, continuity, conformance, openness, machinery-conformity, care, cross-reality, detector-interop, art5-safeguard, swarm, affect, jail) now publicly quotable at "14 measured of 14" after the jail sweep, plus **8 financial/domain axes** (provenance-controls MEASURED on 6 instruments; reserve-attestation, regulatory-framework, distribution-integrity, custody-disclosure UNMEASURED-with-rubric; and 3 candidate indices — ai-economy / human-labour / humanoid-labour — declared UNMEASURED with no rubric, honestly held as slots not products). **(b) The signed-card rail** — Ed25519 over RFC 8785 JCS, content-addressed, three-state verdicts (pass/fail/UNMEASURED, where UNMEASURED is a first-class answer), deterministic grading (DR-0012: "the model narrates, never scores"; DR-0033: "no number without a file"), Wilson-CI + `separated_leaders` + paired McNemar statistical discipline that **none of the five incumbents disclose**. **(c) The SCITT/standards seat** — Council of AI is filed as an author-row on Joel Hillier's citable IETF-SCITT interop report (Vaara SEP-2828 reproduction, corpusDigest 0baa437d), with a reciprocal conformance corpus at `docs/card-conformance/`, COSE_Sign1 card expression, and a Merkle log with inclusion proofs; IETF 127 is San Francisco, Nov 14-20 2026. **(d) The XRPL permissionless-attestation layer** — the structurally-open niche: *unsolicited + permissionless* signed evidence about assets we don't issue (no issuer opt-in, no issuer pay), a 16-instrument registry (6 mainnet-verified + attested, 10 honestly listed as address-not-located), XRPL Memo + Credentials XLS-70 + EAS off-chain publishers all working, a stranger-verifier that passes clean and fails on tamper. **(e) The compliance pack** — dated obligation clock (`compliance/deadlines.json`), EU AI Act GPAI map, CRA SBOM (CycloneDX) workflow, unsolicited-CRA disclaimer template. **(f) cobolbridge** (COBOL modernization as the SOX/Basel/DORA/Solvency-II enterprise on-ramp) and **(g) the AEO content engine** — ~22 clean regulator-targeted answer-engine explainer pages ready to ship. **The two hard gates that don't unlock by scaling compute: key custody (HSM/MPC, not a laptop) and securities counsel sign-off** before any mainnet publish or any measured verdict on a named security.

---

## 2. The regulatory clock (deadline | our asset | move)

| Deadline | Event (source) | Our asset | Move | Gate |
|---|---|---|---|---|
| **2 Aug 2026 (LIVE NOW)** | EU AI Act **GPAI enforcement powers active** — AI Office can request docs, evaluate models, restrict/withdraw; fines up to €15M/3% (GPAI) and €35M/7% (prohibited). Retroactive to Aug 2025 obligations. ([Wilson Sonsini](https://www.wsgr.com/en/insights/eu-ai-act-enforcement-phase-begins.html), [artificialintelligenceact.eu](https://artificialintelligenceact.eu/enforcement-of-chapter-v-under-the-eu-ai-act/)) | GSPC-14 (governance/safety/art5/jail), signed-card rail, `/api/regulation` feed, GPAI map | Publish a signed GSPC measurement pack framed as **independent third-party evidence a GPAI provider can hand the AI Office** — "prove, don't assert." AEO page: "How to evidence GPAI compliance with signed measurement." | [NOW] content; [OWNER] any measured verdict on a *named* provider |
| **2 Dec 2026** | AI Act **watermarking / AI-generated-content transparency (Art 50) obligations** now apply (moved by Digital Omnibus from the earlier window; watermarking deferred to this date). ([White & Case](https://www.whitecase.com/insight-alert/eu-agrees-digital-omnibus-deal-simplify-ai-rules), [ismscopilot](https://www.ismscopilot.com/learn/eu-ai-act-what-applies-from-2-august-2026)) | detector-interop + provenance + cross-reality axes; C2PA/content-credentials alignment | Position detector-interop as the measurement layer over C2PA content-provenance claims. AEO explainer on Art 50 + watermarking. | [NOW] |
| **11 Sep 2026 (~17 days)** | **CRA vulnerability & incident reporting to ENISA** goes live — 24h early warning / 72h triage / 14-day final report via the ENISA Single Reporting Platform. Applies to all products with digital elements. ([Crowell](https://www.crowell.com/en/insights/client-alerts/eu-cyber-resilience-act-countdown-11-september-2026-incidentvulnerability-reporting-deadline-is-less-than-100-days-away), [Hogan Lovells](https://www.hoganlovells.com/en/publications/eu-cyber-resilience-act-preparing-for-vulnerability-and-incident-reporting)) | `compliance/cra-sbom-workflow.md`, CycloneDX SBOM, xrpl.js hygiene (CVE-2025-32965) | **Stand up our own ENISA reporting runbook** (roles, register access, signed SBOM, SCA gate in CI, incident register) — we ship digital products, so this is us, not just content. Also an AEO explainer + a sellable template. | [NOW] runbook + content; [OWNER] register ENISA platform access |
| **30 Sep 2026 (~5 weeks)** | **FedRAMP RFC-0024 machine-readable OSCAL** initial deadline — every CSP must submit SSP/POA&M/assessment in OSCAL or risk losing authorization (final 30 Sep 2027). ([Quzara](https://quzara.com/fedramp/oscal), [fedramp.gov RFC-0024](https://www.fedramp.gov/rfcs/0024)) | OSCAL lineage in the estate (97-comp Ed25519-signed OSCAL per Layer-0 scorecard); signed-card rail maps cleanly to OSCAL assessment-results | AEO page (already drafted: "FedRAMP OSCAL Sept-30 mandate") — ship it. Explore **signed OSCAL assessment-results as a product** for CSPs racing the deadline. | [NOW] content; [BUILD] OSCAL product |
| **1 Jan 2027** | npm trusted/OIDC publishing shift; 2FA-on-publish tightening (~Aug 2026). ([our `xrpl-js-hygiene.md`]) | CI hygiene | If we publish any package, move to OIDC/trusted publishing; rotate to short-lived granular tokens now. | [NOW] |
| **2 Dec 2027** | AI Act **high-risk (Annex III) obligations DEFERRED** from 2 Aug 2026 → 2 Dec 2027 (standalone) / 2 Aug 2028 (embedded) by **Digital Omnibus, Reg (EU) 2026/1744**, in force 27 Jul 2026. ([Consilium](https://www.consilium.europa.eu/en/press/press-releases/2026/06/29/artificial-intelligence-council-gives-final-green-light-to-simplify-and-streamline-rules/), [DLA Piper](https://knowledge.dlapiper.com/dlapiperknowledge/globalemploymentlatestdevelopments/2026/The-Digital-AI-Omnibus-Proposed-deferral-of-high-risk-AI-obligations-under-the-AI-Act)) | GSPC high-risk-mapped axes | **Reprice the urgency internally**: the high-risk cliff we may have been anchoring to has moved 16 months. Do NOT tell customers "August 2026 high-risk deadline" — that is now wrong. GPAI enforcement (Aug 2 2026) is the live one. | [NOW] correct our own messaging |
| **2 Dec 2027** | CRA full conformity / CE marking / technical documentation. ([EC digital-strategy](https://digital-strategy.ec.europa.eu/en/policies/cra-summary)) | CRA SBOM workflow | Long-horizon; keep SBOM signed + current. | [BUILD] |

**US/UK/global posture (no single hard date, but shapes the moat):**
- **SEC (28 Jan 2026 joint staff statement):** tokenization does **not** change securities law; sharp line drawn between *issuer-sponsored* tokenized securities (real ownership) and *third-party synthetic/custodial* products (scrutinized). ([SEC](https://www.sec.gov/newsroom/speeches-statements/corp-fin-statement-tokenized-securities-012826-statement-tokenized-securities), [Morgan Lewis](https://www.morganlewis.com/pubs/2026/02/sec-clarifies-federal-securities-law-treatment-of-tokenized-securities)) → **Tailwind for us:** the taxonomy targets token *issuers*; a pure signed-*opinion*/measurement model sits outside it. Reinforces "we attest, we never tokenize."
- **UK FCA/BoE (18 May 2026 joint Call for Input on the future of tokenisation):** 16 firms live in the Digital Securities Sandbox; first tokenized fund authorized 2025; live synchronisation service targeted 2028. ([BoE](https://www.bankofengland.co.uk/news/2026/may/fca-and-boe-set-out-shared-vision-for-tokenisation-in-uk-wholesale-markets), [FCA](https://www.fca.org.uk/publications/calls-input/future-tokenisation-joint-vision-authorities-uk-wholesale-markets)) → the DSS is our regulated path for any *real* instrument attestation.
- **IOSCO (final report, 11 Nov 2025):** tokenisation still nascent; flags **settlement-finality, interoperability, and lack of credible settlement assets**. ([Ledger Insights](https://www.ledgerinsights.com/iosco-report-on-tokenization-still-nascent-flags-settlement-finality-risks/)) → our distribution-integrity axis (represented≠distributed) speaks directly to IOSCO's investor-protection worry.

---

## 3. Market / news findings (current, sourced)

**RWA market is ~9× bigger in 19 months — and the gap we measure is now the headline.**
The RWA market holds **$37.89B distributed** against **$365.15B off-chain collateral committed** as of 6 Aug 2026 — up from $4.1B in Jan 2025. Tokenized US Treasuries lead at $16.17B (85 products) but held by only **62,959 addresses**; tokenized stocks hit $2.28B across **982,890 holders** after the March 2026 NASDAQ rule change. Ethereum's share fell from 93.4% → 45.8% as BNB, Solana, and **Stellar (8.2%)** absorbed multi-chain issuance. ([coinpaprika/RWA.xyz data](https://coinpaprika.com/education/rwa-crypto-market-size/), [investax](https://investax.io/blog/q1-2026-real-world-asset-tokenization-market-report)) — **The represented-vs-distributed spread ($365B committed vs $38B distributed) IS our distribution-integrity axis.** The JMWH pattern we already flagged is now the whole market's structural story.

**XRPL is a real, growing RWA venue — our substrate is not a backwater.**
XRPL RWAs reached **~$4.34B (Aug 2026), ~59× since Jan 2025**; RLUSD hit ~$1.74B market cap (3rd-largest US-regulated stablecoin); Ripple launched the **Mint** platform (23 Jul 2026) and a full institutional stack (issuance/custody/credit); 302 active RWA projects on XRPL. ([coingabbar](https://www.coingabbar.com/en/crypto-currency-news/xrp-news-today-rlusd-lending-xrpl-rwa-growth-xrp-price), [thecryptobasic](https://thecryptobasic.com/2026/08/05/xrp-ledger-reaches-4-06b-in-rwas-199-holders-after-ripples-infrastructure-investments/), [KuCoin](https://www.kucoin.com/news/flash/ripple-expands-xrpl-stack-for-institutional-tokenized-assets))

**Competitor moves — the issuer-pays wall is now concrete, and it confirms our niche.**
- **Moody's went on-chain**: Aaa-mf assessments to Fidelity & BlackRock tokenized MMFs (14 May 2026); credit ratings published **onchain on Solana** (17 Jun 2026). ([CoinDesk](https://www.coindesk.com/business/2026/06/17/moody-s-rolls-out-credit-ratings-on-solana-in-tokenized-asset-push)) — issuer-solicited, NRSRO.
- **Chainlink ACE** (Automated Compliance Engine) launched with **Apex Group, GLEIF, ERC-3643 Association** — real-time KYC/AML/sanctions policy enforcement in-contract, "unlocks $100T+ institutional capital," early-access to select institutions. ([Chainlink](https://blog.chain.link/automated-compliance-engine/), [ERC3643.org](https://www.erc3643.org/news/chainlink-launches-automated-compliance-engine-in-collaboration-with-apex-group-gleif-and-erc-3643-association)) — a *pre-trade gate*, not an *independent post-hoc opinion*. Different job than ours; complementary, not a substitute.
- **RedStone acquired Credora** (Sep 2025), now shipping oracle-powered **DeFi risk ratings** to Morpho/Spark and **Proof-of-Reserve used by Securitize**. ([Blockworks](https://blockworks.com/news/redstone-acquires-credora), [RedStone](https://www.redstone.finance/proof-of-reserves)) — issuer/protocol-integrated, oracle-delivered.
- **Every one of these is issuer-led / solicited / oracle-embedded.** None is *unsolicited + permissionless independent measurement*. The structural niche the EXECUTION-PLAN identified is still empty — and the incumbents literally can't enter it without attacking their own issuer-pays franchise.

**Standards world is moving and our seat is time-boxed.**
- **SCITT architecture draft-22** (Oct 2025) **expires 13 Apr 2026**; the CCF profile is at IESG Last Call; active SCRAPI/COSE work. ([datatracker](https://datatracker.ietf.org/doc/html/draft-ietf-scitt-architecture-22)) — the interop report + IETF 127 (Nov 14-20 2026, SF) is a real, dated window to be *cited* in the record.
- **ERC-7943 (uRWA) reached FINAL status (May 2026)** — Ethereum's frozen universal RWA interface (transfer validation, freeze, forced transfer, enforcement); coalition spans issuers, identity vendors, **audit firms**; CMTA integrated it into CMTAT; **Chainlink ACE demonstrated compatibility**. ([GlobeNewswire](https://www.globenewswire.com/news-release/2026/05/27/3301737/0/en/erc-7943-achieves-final-status-as-ethereum-s-standard-for-real-world-asset-tokenization.html)) — the standard we said to "track as a lighter T-REX complement" is now FINAL; we should read its on-chain enforcement facts as inputs to provenance-controls.

**AI-governance measurement — the market is validating our exact method.**
- **Stanford AI Index 2026:** responsible-AI benchmark reporting remains sparse; Foundation Model Transparency Index **fell to 40** (from 58 in 2024); red-teaming happens but is "rarely disclosed using a common, externally comparable set of benchmarks." ([Stanford HAI](https://hai.stanford.edu/ai-index/2026-ai-index-report/responsible-ai))
- A 2026 catalogue of **195 AI-safety benchmarks (2018-2026)** finds "benchmark proliferation has outpaced measurement standardization… weak benchmark governance." ([arXiv 2604.12875](https://arxiv.org/abs/2604.12875))
- **FLI AI Safety Index (Summer 2026):** 9 frontier labs on 37 indicators. ([FLI](https://futureoflife.org/ai-safety-index-summer-2026/))
- **The market's stated pain — fragmented, non-comparable, non-reproducible, undisclosed-methodology measurement — is precisely what our deterministic-grading + Wilson-CI + separation + signed-card + three-state grammar solves.** This is external validation of the moat, and an opening to publish "the governance benchmarking is broken; here is a reproducible, signed alternative."

**AI-governance-tooling competitors (Vanta/OneTrust) leave the core open.**
Vanta (ISO 42001 readiness + AI risk module) and OneTrust (AI Governance inventory) "handle **peripheral** EU AI Act compliance well but **lack native AI Act classification logic**… for Annex III risk classification and Annex IV technical documentation, purpose-built tools are better." ([kla.digital](https://kla.digital/blog/best-eu-ai-act-compliance-software-2026), [Kosmoy](https://www.kosmoy.com/resources/blog/onetrust-ai-governance-alternatives/)) — they do *inventory & control-mapping*; nobody does *signed, reproducible, statistically-bounded measurement evidence*. We plug into their gap, we don't compete on GRC workflow.

---

## 4. THE RANKED TOP MOVES (do these NOW, in order)

Each: **trigger (why now) · asset · concrete action · honest constraint.**

### 1. Ship the ENISA / CRA reporting runbook — **hard deadline 11 Sep 2026 (~17 days)** ⏰
- **Trigger:** CRA incident/vuln reporting to ENISA goes live 11 Sep; 24h/72h/14-day clock applies to us as a shipper of digital products, not just as content. This is the one deadline that can bite *us*.
- **Asset:** `compliance/cra-sbom-workflow.md`, CycloneDX SBOM, xrpl.js CVE hygiene.
- **Action:** Assign roles; register ENISA Single Reporting Platform access; generate + sign the SBOM; add an SCA gate to CI; create the incident register. Then repackage the runbook as an AEO explainer + a sellable template.
- **Constraint:** [NOW] for the runbook/content; [OWNER] to register ENISA platform access. Low build effort, high time-sensitivity. **This is #1 purely on the clock.**

### 2. Correct our own AI Act messaging + publish the GPAI-evidence pack — **live enforcement now**
- **Trigger:** Two-sided. (a) GPAI enforcement went live **2 Aug 2026** — real fines, retroactive. (b) The **Digital Omnibus moved high-risk to Dec 2027** — any "August 2026 high-risk deadline" language in our decks/pages is now factually wrong and would cost credibility with exactly the compliance audience we court.
- **Asset:** GSPC-14, signed-card rail, `/api/regulation` feed (re-verify it reflects the Omnibus), GPAI map.
- **Action:** (i) Sweep our surfaces + `compliance/deadlines.json` to reflect Reg 2026/1744 (high-risk → 2 Dec 2027; watermarking → 2 Dec 2026). (ii) Publish an AEO page + a signed sample GSPC pack positioned as "independent third-party evidence for the AI Office — prove, don't assert."
- **Constraint:** [NOW] for the correction and generic content; [OWNER/counsel] before attaching a *measured verdict* to any *named* GPAI provider. Correcting our own dates is free and urgent.

### 3. Publish the "governance benchmarking is broken — here is the signed, reproducible fix" thesis — **the market just said so**
- **Trigger:** Stanford AI Index 2026 (transparency ↓ to 40), the 195-benchmark "weak governance" catalogue, and FLI's index all land in mid-2026 saying measurement is fragmented and non-comparable. That is our pitch, validated by third parties we can cite.
- **Asset:** methodology white paper (open PR **#611**), Wilson-CI + `separated_leaders` + McNemar, three-state grammar, HF datasets (gspc-gov/jail/care).
- **Action:** Merge/ship PR #611 to a live `/methodology` route; publish a companion piece citing Stanford HAI + arXiv 2604.12875 + FLI, contrasting their "undisclosed, non-reproducible" finding with our signed, CI-bounded, reproducible cards. This is pure credibility/funnel and rides a live news wave.
- **Constraint:** [NOW]. Brand-gate on merge. No owner gate. Highest-leverage *content* move.

### 4. Turn the ~$365B-vs-$38B spread into the flagship financial-axis story — **permission-free, ride the market headline**
- **Trigger:** RWA.xyz shows $365B committed vs $38B distributed (6 Aug 2026); IOSCO flags exactly this investor-protection gap; tokenized-stock holders 10× the Treasury holders. The market's structural anomaly is literally our distribution-integrity axis.
- **Asset:** distribution-integrity + provenance-controls axes, `/interop/*` reference layer, RWA.xyz API integration path.
- **Action:** Wire distribution-integrity to RWA.xyz API v4; publish an **UNMEASURED-first coverage/index** over the represented-vs-distributed spread across the public instrument set (RLUSD, BUIDL, OUSG, BENJI, Aviva; JMWH as the negative-signal demonstration). Signed coverage declarations only — **never a verdict, never a rating.**
- **Constraint:** [NOW] for UNMEASURED coverage over public on-chain facts (no counsel needed); [OWNER/counsel] the moment it becomes a *measured verdict on a named security*. [BUILD] the RWA.xyz ingest. This is the cleanest way to be *first and loud* in the empty unsolicited niche without tripping a gate.

### 5. Provision the key-custody signer — **it unblocks everything downstream**
- **Trigger:** Both production gates are owner-gated, and key custody is the one that unlocks by a single decision. AWS KMS has supported **both** curves (Ed25519 added 7 Nov 2025) — one FIPS non-exportable setup covers XRPL + EVM. Alternatives: Turnkey ($99/mo), self-host Coinbase cb-mpc (MIT) or YubiHSM 2.
- **Asset:** `batch_signal_run.py --publish` already refuses without `CSOAI_KEY_CUSTODY=hsm`; the KMS client is committed.
- **Action:** Owner provisions the HSM/MPC signer; publish key provenance via did:web. This is the gate that turns testnet proof → mainnet-capable reference layer.
- **Constraint:** [OWNER] — a purchase/provision decision, not a build and not a legal question. Nothing mainnet moves until this lands. (Counsel is the *other* gate — sequence: key first, then counsel before the first named-security verdict.)

### 6. Hold the SCITT seat + file the IETF-127 note — **time-boxed standards window**
- **Trigger:** SCITT draft-22 expired-window churn; CCF at IESG Last Call; IETF 127 is Nov 14-20 2026 (SF). Being *cited* in the DOI-bound interop report is durable, cheap leverage that only survives on strict measurement-body conduct.
- **Asset:** author-row on the interop report, `docs/card-conformance/` corpus, COSE_Sign1 expression, Merkle log.
- **Action:** Keep the conformance corpus green; send the IETF-127 agenda note (independent transparency-log interop) under the chairs' "implementation experience" bucket. **DOCTRINE:** technical only — never pitch XRPL/RWA/products on the standards list (that would cost the seat).
- **Constraint:** [NOW] but doctrine-bound. Owner sends the actual emails. Zero product content.

### 7. Read ERC-7943 (FINAL) + XLS-70/XLS-80 enforcement facts into provenance-controls — **standard just froze**
- **Trigger:** ERC-7943 reached FINAL (May 2026); Chainlink ACE + CMTAT already integrate it; its on-chain enforcement primitives (freeze/forced-transfer/transfer-validation) are now a stable, vendor-neutral fact source — exactly the deterministic on-chain facts provenance-controls grades.
- **Asset:** provenance-controls axis (MEASURED on 6), erc3643_attest_adapter, XRPL Credentials XLS-70.
- **Action:** Add ERC-7943 enforcement-state reads to the deterministic rubric alongside the ERC-3643/T-REX reads; treat it as a lighter complement. Attest-alongside via EAS, never issuance.
- **Constraint:** [BUILD] — modest. No gate (public on-chain reads). Keeps our measurement current with the frozen standard.

### 8. Ship the clean AEO explainer batch — **compounding funnel, zero gate**
- **Trigger:** ~22 codename-clean, regulator-targeted answer-engine pages already drafted (FedRAMP OSCAL Sep-30, SCITT, Colorado AI Act, Art 5/Art 50, SS 584, NIST AI 600-1, Framework Convention). Several map to live deadlines above; all are net-new coverage vs the current blog.
- **Asset:** `aeo-*.json` seed pages, existing `/blog` ContentPage pipeline, brand-gate.
- **Action:** Convert to blog/answers entries, add to prerender + sitemap, run brand-gate, de-dupe vs existing ISO-42001/Art-50 coverage, ship.
- **Constraint:** [NOW]. Verified 0 banned-string hits. The lowest-risk, highest-compounding content move; pairs with moves 2-3.

---

## 5. Time-sensitive flags (closing windows)

- ⏰ **11 Sep 2026 (~17 days): CRA/ENISA reporting live** — Move #1. The only deadline that can penalize *us*.
- ⏰ **30 Sep 2026 (~5 weeks): FedRAMP OSCAL initial** — ship the AEO page now; evaluate the signed-OSCAL product.
- ⏰ **2 Dec 2026: AI Act watermarking/Art-50 transparency** — detector-interop + C2PA content window.
- 📉 **Messaging risk NOW:** the "Aug 2026 high-risk" cliff moved to **Dec 2027** (Digital Omnibus). Any surface still citing it is wrong today — fix before it's quoted back at us.
- 🪟 **Niche-occupancy window:** unsolicited + permissionless is still empty (Moody's/Chainlink/RedStone all issuer-led as of Aug 2026), but ERC-7943 FINAL + Chainlink ACE early-access mean the compliance-infrastructure land-grab is accelerating. Being *first and loud* with UNMEASURED coverage (Move #4) is how we plant the flag before the space fills.

---

*Generated read-only over the estate + live WebSearch. Honest posture preserved: coverage/UNMEASURED and generic explainer content ship permission-free NOW; named-security verdicts and mainnet publishes stay behind the key-custody + counsel gates; the three candidate indices remain UNMEASURED slots, never claimed. No client code or live surface was modified by this research.*

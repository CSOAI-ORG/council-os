# Cursor job list — Council OS (parallel, batch-runnable)

Self-contained jobs for Cursor cloud composers. Each is independent (different files/
repos) so they run in parallel without collision. Rules for every job: no invented
numbers (live API or omit); never "certify/certification" (we measure); never
"sovereign/SOVOS/sov3/CEASAI/dorado/cibola"; branch → build-verify → PR (do not push
straight to master on client/ changes). Lead copy with **unsolicited + permissionless**.

## Repo: CSOAI-ORG/councilof-ai (the front end)

**J1 — Full agentic Council OS front end.** Fork the Open-AG-UI-Demo pattern
(CopilotKit + AG-UI + LangGraph supervisor). Wire the existing lobby chat centre to an
MCP-wrapped tool backend. Render typed cards: SignedVerdictCard, CoverageCard,
RiskScoreCard, BondIssuanceCard (controlled generative UI — prebuilt React cards the
agent populates, never raw agent HTML). `renderAndWaitForResponse` for any
confirm-before-sign step. Confirm CopilotKit's free-vs-paid boundary before relying on
a gated feature. Pin xrpl.js ≥5.x.

**J2 — x402 checkout, real.** Take the `/products` catalog (branch os-product-catalog)
and make the RAS card's x402 path a working metered checkout against the existing
`/api/x402` / pay_url counter. Regulators-free enforced server-side. No Stripe.

**J3 — Per-instrument attestation pages.** For each of the 16 XRPL + flagship EVM
instruments, a page `/attest/<slug>` rendering that instrument's coverage row from
`/interop/rwa-registry.json` + explorer links + the "UNMEASURED / unsolicited" framing.
AEO-structured (schema.org Dataset), one factual claim per page.

**J4 — "Powered by Council OS" embed.** A white-label embeddable verification badge +
card (the Clearbit "powered-by" pattern) that a third party drops into their front end;
child-key provisioning; reads a signed attestation and verifies it client-side.

## Repo: CSOAI-ORG/council-os (the monorepo harness)

**J5 — Adapter coverage expansion.** Add `adapters/evm/<slug>/index.js` for the deep
EVM universe (Securitize 130+, Ondo Stocks 438+, Backed 60+) — one folder each, real
verified contract address or honest `no-public-address`. Never invent an address. Run
`node adapters/build.mjs` to confirm coherence.

**J6 — MCP server.** Implement `mcp-server/` wrapping the engine + adapters as MCP
tools (measure / verify / coverage-lookup / attest-alongside). Chain reads proxy through
Nodit's MCP (covers XRPL + EVM in one server) or Blockscout. This makes Council OS
itself listable as a connector other agents add with zero integration work.

**J7 — index-store query API.** A small queryable service over the time-series corpus
(`index-store/`) — GET by instrument / chain / status; aligned to ICMA Bond Data
Taxonomy + SOC/ISAE evidence shapes so it's API- and audit-ready before monetization.

## Owner / counsel (NOT Cursor — cannot be automated)

**O1 — Key custody:** provision HSM/MPC signer on the isolated ANVIL pod; set
`CSOAI_KEY_CUSTODY=hsm`. Until then `batch_signal_run.py --publish` refuses (by design).

**O2 — Securities counsel:** sign off on attestation language; NRSRO/anti-touting review
before any mainnet publish or measured verdict on a named security.

**O3 — proofof.ai:** decide whether to repoint from the councilof.ai brand redirect to a
dedicated Pages project serving the reference layer / corpus.

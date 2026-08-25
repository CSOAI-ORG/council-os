# Council OS — e2e execution plan (data-generation + attestation body)

**What we are:** an independent **data-generation** business *and* a **compliance-
measurement attestation body**. We generate signed measurement data (the corpus) and
we are the independent body that signs it. Revenue = RAS + A2A/API + data/index
subscription + tooling licenses + training. **Free forever for regulators.** Never a
token, never an issuer, never "certification." Settlement rides x402/open rails.

**The moat (sharpened per the Aug-2026 freshness check):** not "independent" (every
incumbent now claims that) but **unsolicited + permissionless** — no issuer opt-in, no
issuer payment. Moody's TIE, S&P/Chainlink, Credora, Particula are all issuer-led; the
unsolicited niche is structurally unoccupied because they can't attack their own
issuer-pays franchise. Regulatory posture is a **tailwind**: the SEC Jan-2026 staff
statement's taxonomy is about token *issuers* — a pure signed-opinion model sits
outside it.

## The pipeline, e2e (front to back)

```
front (Council OS + /xrpl-attest)  ──▶  adapters (OPEN, data-only, 19)  ──▶
engine (PRIVATE, deterministic, Ed25519)  ──▶  publishers (XRPL Memo/XLS-70 + EAS)  ──▶
index-store (time-series signed corpus)  ──▶  verify (stranger checker)
                          ▲
        tokenization/ (ERC-3643 T-REX bridged, read-only + attest-alongside)
```

## Status ledger (honest)

| Stage | State |
|---|---|
| adapters (open) | ✅ 19 generated, honest no-public-address, SKILL.md, build.mjs |
| engine (private) | ⚠️ boundary declared; real GSPC engine lives outside this repo |
| publishers | ✅ XRPL Memo+XLS-70, EAS off-chain, batch signal churn — all working on testnet |
| index-store | ✅ seeded (corpus-index + signal-run-latest) |
| tokenization | ✅ T-REX bridged (GPL submodule), ERC-3643 attest-alongside adapter |
| verify | ✅ stranger verifier VALID; tamper fails |
| front (reference layer) | ✅ councilof.ai/xrpl-attest live (registry + coverage + PoC) |
| front (full agentic) | ⬜ CopilotKit/AG-UI/LangGraph fork — NOT built (see jobs) |
| coverage | ✅ 6 XRPL mainnet-verified+attested, 3 EVM via EAS, 16-registry |

## The two production gates (owner + counsel — NOT code)

1. **Key custody** — mainnet signing needs HSM/MPC on the isolated ANVIL pod, not a
   workstation. Enforced in code today: `batch_signal_run.py --publish` refuses unless
   `CSOAI_KEY_CUSTODY=hsm`. Owner action: provision the HSM/MPC signer.
2. **Legal** — securities counsel sign-off on attestation language before any mainnet
   publish or any *measured verdict* on a named security. NRSRO hygiene: never "credit
   rating"; document non-issuer-paid; publish transparent methodology. See `compliance/`.

## Sequence (mirrors the staged plan; each stage has a threshold to advance)

- **Stage 0 (done):** testnet proof + reference layer live + 16-registry + corpus index.
- **Stage 1 (now):** product catalog + x402 RAS surface (in progress, branch
  `os-product-catalog`); EU compliance pack (`compliance/`); signal churn over all
  targets before outreach.
  - *Advance when:* catalog live, x402 path coherent, compliance deadlines tracked.
- **Stage 2 (gated):** mainnet free reference layer — **blocked on both gates above.**
- **Stage 3:** white-label / enterprise license + data/index subscription; COBOL
  cross-sell (cobolbridge.ai) as the enterprise on-ramp.
- **Stage 4:** tokenization *partnership* (Securitize/Tokeny/Archax/Ownera) — never as
  issuer.

## Clean first attestation targets (freshness-verified, when gates clear)
Aviva USD Liquidity Fund, RLUSD, BUIDL, BENJI, Ondo OUSG — all live, healthy,
regulator-engaged. **JMWH: negative-signal demonstration only** ($2.23B represented,
~19 holders, ~0 volume) — the schema must express represented≠distributed; never
endorse it.

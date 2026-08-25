# council-os — the four-zone harness (build-plan structure)

```
engine/       PRIVATE — GSPC scoring + Ed25519 signing core (the IP)
adapters/     OPEN — one folder per target asset (DeFiLlama pattern); data only
publishers/   XRPL (Memo + XLS-70) + EAS submission — the signing/attach stage
mcp-server/   wraps engine + adapters as MCP tools; chain reads via Nodit/Blockscout MCP
index-store/  time-series signed corpus — the compounding data/index asset
frontend/     Council OS (CopilotKit + AG-UI + LangGraph) — see councilof-ai repo /xrpl-attest
```

**The separation is the strategy:** open `/adapters` for credibility + community
contribution (issuers can PR their own), closed `/engine` where defensibility lives.
Attestation ≠ tokenization ≠ ownership — this repo signs opinions/measurements ABOUT
assets; it never mints ownership. Tokenization, if ever, is via a regulated partner
(Securitize/Tokeny/Archax/Ownera), never in this tree.

Flywheel: free reference layer → institutional pilots → white-label/enterprise
license → corpus depth → data/index subscription + COBOL cross-sell + tokenization
partnership. Spine registry: `registry/spine.json`. Coverage: `economy/xrpl-attest/`.

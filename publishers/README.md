# publishers — the signing/submission stage (SEPARATE from adapters)

Adapters (open) get the data. The **engine** (private) measures + signs. Publishers
submit the signed result to a chain. This separation mirrors DeFiLlama: open "get
the data" vs. closed "compute + serve". Working, tested implementations live in
`../economy/xrpl-attest/`:

- `attest.py` — XRPL Memo + XLS-70 Credential publisher (single card)
- `attest_coverage.py` — XRPL batch coverage publisher (loop over targets)
- `eas/attest_offchain.cjs` — EAS off-chain publisher (EVM, gasless)
- `verify.py` — the stranger verifier (the credibility proof)

Batch note (per build plan): EVM scale uses EAS `eas-batch-attest`; XRPL scale is a
thin loop over `submitAndWait` with Sequence/Ticket management to avoid nonce
collisions. Key custody is the real operational gate — the signing key is now a
sensitive asset (HSM/MPC, never a laptop env var at scale).

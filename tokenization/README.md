# tokenization — bridged OPEN standard, arm's-length. NOT an issuer path.

## What's here
`erc3643-t-rex/` — a git submodule of **TokenySolutions/T-REX** (GPL-3.0), the
open reference implementation of the ERC-3643 permissioned-security-token standard.
Bridged permissionlessly under its own license, kept as a submodule so its GPL-3.0
copyleft never mixes into the rest of this tree — and **never touches the private
`/engine`**.

## The hard boundary (read before using)
Bridging this code does **NOT** make Council of AI a token issuer, a transfer
agent, or a broker-dealer. Those are **legal statuses**, not software. Per SEC
staff (Jan 2026) and Commissioner Peirce (Jul 2025), on-chain format changes
nothing — tokenized securities are still securities, and only the actual
issuer/owner, under a regulated wrapper, can mint ownership.

So this zone is exactly two things and nothing more:
1. **A build/test/demo capability** — we can stand up ERC-3643 tokens on a
   testnet to develop and demonstrate the *integration* between a compliant token
   and our attestation layer.
2. **The partner-integration surface** — when a real instrument is tokenized, it
   is minted by a **regulated partner** (Securitize / a Tokeny-based issuer /
   Archax / Ownera FinP2P), who is the issuer of record and carries the
   securities-law liability. Council of AI supplies the attestation + Council OS
   UX on top — the Stripe-model layer. We never become the issuer.

## What rides where
- The **token** (ownership) → the regulated partner, via ERC-3643 / XLS-33 MPT.
- The **attestation** (independent signed opinion/measurement) → ours, via
  `../publishers` (XRPL Memo/XLS-70 + EAS), riding *alongside* the token, never
  inside its ownership logic. See `integration/attest-alongside-token.md`.

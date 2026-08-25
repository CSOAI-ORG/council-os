# Key custody — the mainnet signing gate, with a chosen path (not just "get an HSM")

Our batch attestation signer needs **automated, no-human-in-the-loop signing on two
curves**: XRPL Ed25519 + Ethereum secp256k1. That two-curve requirement is the filter
that eliminates most options. The 2025–2026 research resolves it concretely.

## The unlock (Nov 7, 2025)
**AWS KMS now supports BOTH curves** — secp256k1 (long available) and **Ed25519/EdDSA
(ECC_NIST_EDWARDS25519, added Nov 7 2025).** Before this, XRPL keys had to live in a
separate system from EVM keys. Now one FIPS-validated, non-exportable KMS setup covers
both. This is the single most consequential development for our custody blocker.

## Ranked options (both-curve capable only)
| Path | Type | Both curves | Notes |
|---|---|---|---|
| **AWS KMS** | managed, cloud | ✅ (since Nov 2025) | FIPS, non-exportable, we likely already run on AWS. Caveats: signs a digest, DER output → handle EIP-2 low-S for EVM + Ed25519 RAW/DIGEST distinction; 4KB message cap (sign the digest). CloudHSM underneath for single-tenant HW. |
| **Turnkey** | managed SaaS (TEE) | ✅ native | Policy engine + root-quorum, DENY-wins, "agentic wallets" pattern. Published pricing: 25 free sigs, then $0.10/sig; Pro ~$99/mo unlimited (→$0.01/sig); ~100–150ms latency. |
| **Coinbase cb-mpc** | OPEN (MIT) | ✅ ECDSA+EdDSA+Schnorr | The standout self-hostable/permissive both-curve MPC. Low-level C++/Go — we build the relay/orchestration. The sovereignty upgrade path. |
| **YubiHSM 2** | hardware | ✅ on-device | ~few hundred $, open SDK; cheapest real hardware isolation; build the signing service (cf. Tezos "Signatory"). FIPS variant cert sunsets May 2 2026 — check current model. |

**Avoid:** ZenGo multi-party-ecdsa (archived); Silence Labs (proprietary non-commercial
despite "permissive" marketing); 0xCarbon DKLs23 + Lit Protocol (secp256k1-only — can't
sign XRPL alone).

## Decision + sequencing (owner action, but now a clear one)
1. **Start on AWS KMS** (cloud-native, FIPS, both curves, minimal new vendor surface)
   **or Turnkey** (if we want the purpose-built policy engine + per-signature economics).
2. Enforce a signing **policy**: whitelist tx types + destinations, DENY-wins, full audit
   log with attribution.
3. **Publish key provenance via did:web** so a stranger-verifier ties an attestation to a
   known custody setup.
4. Keep a **Shamir/Vault cold backup** of recovery material — never on a workstation.
5. Later sovereignty upgrade: cb-mpc or YubiHSM if managed-provider dependency becomes a
   concern. Switch-model threshold: >~50–100k sigs/month → compare Turnkey-flat vs
   KMS-per-call vs self-hosted.

Until this is provisioned, `publishers/batch_signal_run.py --publish` REFUSES (it checks
`CSOAI_KEY_CUSTODY=hsm`). That is the gate, enforced in code.

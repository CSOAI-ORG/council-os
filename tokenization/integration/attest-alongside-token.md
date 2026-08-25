# Attestation riding alongside an ERC-3643 token (the integration pattern)

```
 regulated partner                    Council of AI (us)
 ─────────────────                    ──────────────────
 mints ERC-3643 token   ── token ──▶  reads public contract address (adapters/)
 (issuer of record)                   measures via /engine (private, three-state)
 carries securities                   signs verdict (Ed25519) → /publishers
 liability                            attaches EAS attestation, recipient =
                                      the token contract (no consent needed)
                                             │
                                             ▼
                              anyone verifies the attestation
                              independently (stranger verifier)
```

The token and the attestation are separate objects with separate owners. The
attestation references the token's public contract address as DATA — it does not
sit inside the token's transfer logic, so it needs no cooperation and confers no
rights. This is the permissionless-attach thesis applied to a bridged compliant
token: the partner owns issuance; we own the independent opinion.

Status of every attestation in the demo layer: UNMEASURED until a real GSPC run.

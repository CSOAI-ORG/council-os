# instrument-body v0

Post-hoc attachments. **The card signature does not cover the body.** Verify body separately.

```
{ "type", "digest", "preimage_rule", "status" }
```

`status` is only **VALID | INVALID | UNCHECKABLE**. No fourth. Empty ≠ 0.

## Types this cycle

| type | preimage_rule | verifier |
|---|---|---|
| emilia-cose | ep-scitt-statement-identity-v0.1 | P-256 COSE_Sign1 (RFC 9052). Not Ed25519. |
| vaara-receipt | vaara.receipt/v1 | SEP-2828 vectors or UNCHECKABLE |
| c2pa-manifest | c2pa-cai | c2pa-python. HMAC sidecar = UNCHECKABLE as C2PA |
| ots | ots-v1 | Bitcoin calendar err → UNCHECKABLE |
| xls70-uri | xrpl-xls70 | URI to card. Devnet until TUI 1 SIGNED. No score in memo. |
| scitt-note | rfc9942-ccf-profile | No TS → UNCHECKABLE |
| openshell-audit | openshell | Pin. Attachment. |
| inspect-receipt | inspect-receipt | inspect-signed-receipt |

HMAC-only may be VALID **as hmac-sidecar**, never as `c2pa-manifest`.

Do not render a body as a glass card.

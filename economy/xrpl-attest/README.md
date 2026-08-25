# xrpl-attest — permissionless evidence attach (devnet PoC)

**The claim this package proves:** an independent measurement body can attach
signed compliance evidence to a public ledger, about an account it does not
control, with nobody's permission. This is the layer the tokenized-asset market
demonstrably lacks: Moody's, S&P and Chainlink ACE all attach *through* issuer
or platform cooperation; the adversarial-independent attach was enabled
everywhere but occupied by nobody. Council of AI's whole posture — measure
what we don't issue, sign it, let strangers verify — is exactly this layer.

## What ran (2026-08-25, XRPL DEVNET)
1. **Memo attach** — a 1-drop payment toward the subject account carrying
   `{sha256, ed25519, kid}` over a REAL entry from the live signed card index
   (councilof.ai/signed/card_index.json), signed by the scoped `cose-interop-1`
   key (never the estate root).
2. **Credential attach (XLS-70)** — `CredentialCreate` naming the subject,
   type `CSOAI.GSPC.CARD/0.1`, URI = the public signed index.

Both validated; hashes in `RUN-RECORD.json`. `verify.py` is the stranger
checker: it re-fetches both transactions from the public devnet, re-derives the
digest from the LIVE index, and verifies the Ed25519 signature — exit 0 only if
every check passes, UNVERIFIABLE (never a pass) when a fetch fails, and a
tamper test confirms a doctored record fails.

## Honesty box
DEVNET proof-of-capability. Synthetic subject. Not an investment, not a credit
rating, not a conformity mark. Attesting is permissionless; making an
attestation *count* inside someone's permissioned domain still requires the
relying party to trust this issuer key — that opt-in trust is the product.
Anything beyond synthetic assets goes through counsel and a sandbox
(UK DSS / EU DLT Pilot) first.

```
python3 verify.py   # needs: pip install cryptography
```

# Mixed key list (do not merge)

| Key | Alg | Role | In GSPC register? |
|---|---|---|---|
| `did:web:csoai.org#card-attestation-1` | Ed25519 | Living cards (Rule A) | yes |
| `did:web:csoai.org#board-attestation-1` | Ed25519 | `/api/gspc` stamp (Rule B) | yes |
| Emilia fixture P-256 JWK | ES256 | Identity vectors only | **no** |
| COSE wrap ephemeral | Ed25519 | Outer envelope | **no** |
| CAI c2pa-python test cert | ES256 | Demo sign only, downloaded to /tmp | **no** |

Do not switch card alg to ES256. Do not put Emilia P-256 in the DID document.
Wrap key ≠ card pin. Browser Ed25519-COSE is later; CLI first.

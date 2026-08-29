# Bindings adapters — call their verifier, do not swallow the tree

Pins live in `registry/bindings.json`. Each adapter is a thin dispatch:

```text
kind → preimage_rule → python/npm of the pinned package
```

UNCHECKABLE if the pin is missing. Never copy Emilia / c2pa-rs / scitt-ccf-ledger into this folder.

| Adapter | Pin | Rule |
|---|---|---|
| `verify_c2pa.py` | `c2pa-python==0.37.8` | `c2pa-cai` |
| `spike_c2pa_vs_hmac.py` | same vs HMAC MCP sidecar | HMAC VALID ≠ C2PA |
| `verify_ots.py` | `opentimestamps-client==0.7.2` | `ots-v1` |
| `verify_emilia.py` | `emiliaprotocol/emilia-protocol@e507acdf` | `ep-scitt-statement-identity-v0.1` |

HMAC MCP (`CSOAI-ORG/c2pa-watermark-mcp`) is archived from the story. It signs a JSON sidecar with HMAC-SHA256; `c2pa.Reader` on the same bytes reports `ManifestNotFound`.

Emilia is a pin-check / reproduction of their standalone vectors. Not an independent cell. Not a GSPC card.

Spray is `/embed` + `/badge` + card verify on *their* origin. Do not ship Emilia Gate inside the 3kb snippet.

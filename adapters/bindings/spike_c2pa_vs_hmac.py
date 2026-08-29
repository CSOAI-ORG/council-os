#!/usr/bin/env python3
"""Spike: HMAC MCP sidecar vs pinned c2pa-python Reader.

Reimplements the HMAC path from CSOAI-ORG/c2pa-watermark-mcp __init__.py
(stdlib hmac over sorted JSON). Does not import that package.
Does not vendor c2pa-rs.

HMAC VALID ≠ C2PA VALID. Wrong-rule dispatch is UNCHECKABLE, not INVALID.
"""
from __future__ import annotations

import hashlib
import hmac
import json
import struct
import sys
import tempfile
import zlib
from pathlib import Path

from verify_c2pa import verify_path

HMAC_KEY = b"dev-hmac-key-do-not-use-in-prod-aaaa"
PIN = "c2pa-python==0.37.8"


def png_1x1() -> bytes:
    def chunk(tag: bytes, data: bytes) -> bytes:
        crc = zlib.crc32(tag + data) & 0xFFFFFFFF
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", crc)

    ihdr = struct.pack(">IIBBBBB", 1, 1, 8, 2, 0, 0, 0)
    raw = zlib.compress(b"\x00\xff\x00\x00")
    return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) + chunk(b"IDAT", raw) + chunk(b"IEND", b"")


def hmac_sign(asset: bytes, mime: str) -> dict:
    """Same construction as c2pa-watermark-mcp.sign_asset (HMAC sidecar)."""
    manifest = {
        "@context": "https://c2pa.org/specifications/v2.0/context.jsonld",
        "claim_generator": "c2pa-watermark-mcp/0.1.0",
        "asset": {
            "mime": mime,
            "hash": hashlib.sha256(asset).hexdigest(),
            "alg": "sha256",
        },
        "assertions": [
            {
                "label": "c2pa.ai_generated",
                "value": {"type": "trainedAlgorithmicMedia", "confidence": 0.95},
            }
        ],
        "_c2pa_native": "fallback_hmac",
    }
    canonical = json.dumps(manifest, sort_keys=True, separators=(",", ":")).encode()
    manifest["signature"] = {
        "alg": "hmac-sha256",
        "value": hmac.new(HMAC_KEY, canonical, hashlib.sha256).hexdigest(),
    }
    return manifest


def hmac_verify(asset: bytes, manifest: dict) -> dict:
    reasons = []
    actual = hashlib.sha256(asset).hexdigest()
    expected = (manifest.get("asset") or {}).get("hash")
    if expected != actual:
        reasons.append("hash mismatch")
    unsigned = {k: v for k, v in manifest.items() if k != "signature"}
    want = hmac.new(
        HMAC_KEY,
        json.dumps(unsigned, sort_keys=True, separators=(",", ":")).encode(),
        hashlib.sha256,
    ).hexdigest()
    got = (manifest.get("signature") or {}).get("value")
    if not got or not hmac.compare_digest(want, got):
        reasons.append("hmac mismatch")
    return {"valid": not reasons, "reasons": reasons, "rule": "hmac-sidecar"}


def main() -> int:
    cai = Path("/tmp/c2pa-spike/C.jpg")
    with tempfile.TemporaryDirectory() as td:
        png_path = Path(td) / "hmac.png"
        png = png_1x1()
        png_path.write_bytes(png)
        sidecar = hmac_sign(png, "image/png")
        hmac_row = hmac_verify(png, sidecar)
        c2pa_hmac = verify_path(png_path)
        c2pa_cai = verify_path(cai) if cai.is_file() else {
            "verdict": "UNCHECKABLE",
            "reason": "CAI fixture C.jpg not downloaded",
        }

    report = {
        "kind": "c2pa-vs-hmac-spike",
        "pin": PIN,
        "hmac_mcp": "CSOAI-ORG/c2pa-watermark-mcp",
        "not_a_gspc_cell": True,
        "cases": [
            {
                "name": "hmac-sidecar-png",
                "hmac_mcp": "VALID" if hmac_row["valid"] else "INVALID",
                "c2pa_python": c2pa_hmac.get("verdict"),
                "c2pa_reason": c2pa_hmac.get("reason") or c2pa_hmac.get("adapter"),
                "note": "HMAC MCP never writes JUMBF. Shared-secret JSON is not C2PA.",
            },
            {
                "name": "cai-fixture-C.jpg",
                "source": "contentauth/c2pa-python@v0.37.8 tests/fixtures/C.jpg",
                "c2pa_python": c2pa_cai.get("verdict"),
                "validation_state": c2pa_cai.get("validation_state"),
                "validation_codes": c2pa_cai.get("validation_codes"),
                "active_manifest": c2pa_cai.get("active_manifest"),
                "note": "Real C2PA boxes. Untrusted cert without CAI trust list → INVALID under c2pa-cai. Still a manifest; HMAC PNG is not.",
            },
        ],
        "verdict": "HMAC MCP is not a C2PA verifier. Join is pip install c2pa-python, not a CSOAI subtree.",
    }
    print(json.dumps(report, indent=2))
    hmac_ok = hmac_row["valid"] and c2pa_hmac.get("verdict") == "UNCHECKABLE"
    cai_has_manifest = bool(c2pa_cai.get("active_manifest"))
    return 0 if hmac_ok and cai_has_manifest else 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""One C2PA path: c2pa-python sign + verify. CLI, not six MCPs.

Private keys are downloaded to /tmp at runtime and never written here.
HMAC MCP is not this rule. Art 50 CoP example, not a mandate.
"""
from __future__ import annotations

import hashlib
import json
import struct
import sys
import tempfile
import urllib.request
import zlib
from pathlib import Path

PIN = "c2pa-python==0.37.8"
FIXTURE = "https://raw.githubusercontent.com/contentauth/c2pa-python/v0.37.8/tests/fixtures/"
UA = {"User-Agent": "csoai-c2pa-demo/0.1"}


def fetch(name: str) -> bytes:
    req = urllib.request.Request(FIXTURE + name, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def png_1x1() -> bytes:
    def chunk(tag: bytes, data: bytes) -> bytes:
        crc = zlib.crc32(tag + data) & 0xFFFFFFFF
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", crc)

    ihdr = struct.pack(">IIBBBBB", 1, 1, 8, 2, 0, 0, 0)
    return (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", ihdr)
        + chunk(b"IDAT", zlib.compress(b"\x00\xff\x00\x00"))
        + chunk(b"IEND", b"")
    )


def verify_file(path: Path) -> dict:
    from c2pa import Reader

    try:
        with Reader(str(path)) as reader:
            store = json.loads(reader.json())
    except Exception as exc:
        return {
            "verdict": "UNCHECKABLE" if "ManifestNotFound" in type(exc).__name__ or "JUMBF" in str(exc) else "INVALID",
            "reason": str(exc)[:200],
            "pin": PIN,
        }
    digest = hashlib.sha256(json.dumps(store.get("active_manifest"), sort_keys=True).encode()).hexdigest()
    codes = [s.get("code") for s in (store.get("validation_status") or []) if isinstance(s, dict)]
    untrusted = any(isinstance(c, str) and "untrusted" in c.lower() for c in codes)
    verdict = "INVALID" if untrusted or store.get("validation_state") not in {"Valid", "Trusted"} else "VALID"
    if not store.get("active_manifest"):
        verdict = "UNCHECKABLE"
    return {
        "verdict": verdict,
        "validation_state": store.get("validation_state"),
        "validation_codes": codes,
        "active_manifest": store.get("active_manifest"),
        "manifest_digest": digest,
        "pin": PIN,
        "hmac": False,
    }


def sign_demo(tmp: Path) -> dict:
    from c2pa import Builder, C2paSignerInfo, C2paSigningAlg, Signer

    certs = fetch("es256_certs.pem")
    key = fetch("es256_private.key")
    src = tmp / "plain.png"
    dest = tmp / "signed.png"
    src.write_bytes(png_1x1())
    info = C2paSignerInfo(
        alg=C2paSigningAlg.ES256,
        sign_cert=certs,
        private_key=key,
        ta_url=None,
    )
    signer = Signer.from_info(info)
    manifest = json.dumps(
        {
            "claim_generator": "csoai-c2pa-demo/0.1",
            "assertions": [
                {
                    "label": "c2pa.actions",
                    "data": {"actions": [{"action": "c2pa.created"}]},
                }
            ],
        }
    )
    builder = Builder.from_json(manifest)
    builder.sign_file(str(src), str(dest), signer)
    # drop key material
    del key, certs, info, signer
    out = verify_file(dest)
    out["signed"] = True
    out["bytes"] = dest.stat().st_size
    return out


def main() -> int:
    rows = {}
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        cai = tmp / "C.jpg"
        cai.write_bytes(fetch("C.jpg"))
        rows["verify_cai_fixture"] = verify_file(cai)
        rows["sign_then_verify"] = sign_demo(tmp)
    rows["kind"] = "c2pa-manifest"
    rows["preimage_rule"] = "c2pa-cai"
    rows["not_a_gspc_cell"] = True
    rows["art50"] = "Code of Practice example, not a mandate"
    print(json.dumps(rows, indent=2))
    signed = rows["sign_then_verify"]
    return 0 if signed.get("active_manifest") else 1


if __name__ == "__main__":
    sys.exit(main())

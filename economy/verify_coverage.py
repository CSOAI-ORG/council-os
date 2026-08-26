#!/usr/bin/env python3
"""verify_coverage.py -- stranger verifier for the signed coverage artifact.

Takes two files and nothing else: COVERAGE.json (the claim) and
COVERAGE.sig.json (the signature over it). Imports only the Python standard
library and `cryptography`. It does NOT import, and does not need, any Council
of AI package -- if `import gspc_measurement` or `import custody` works in your
environment, that is incidental; this script never touches either.

Checks, in order:
  1. the recorded digest is genuinely the SHA-256 of COVERAGE.json's bytes
  2. the recorded keyid is genuinely sha256(public key) -- so the key cannot be
     swapped for another without the keyid moving
  3. the Ed25519 signature over those 32 digest bytes verifies under that key
  4. tamper control: one flipped bit in the payload must be REJECTED

Exit 0 only if every check passes. A missing file is UNVERIFIABLE (exit 2),
never a pass.

    python3 economy/verify_coverage.py [COVERAGE.json] [COVERAGE.sig.json]
"""

from __future__ import annotations

import base64
import hashlib
import json
import os
import sys

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

HERE = os.path.dirname(os.path.abspath(__file__))


def main(argv: list) -> int:
    payload_path = argv[1] if len(argv) > 1 else os.path.join(HERE, "COVERAGE.json")
    sig_path = argv[2] if len(argv) > 2 else os.path.join(HERE, "COVERAGE.sig.json")

    try:
        payload = open(payload_path, "rb").read()
        sig_doc = json.load(open(sig_path))
    except Exception as exc:
        print(f"UNVERIFIABLE -- could not read the inputs: {exc}")
        return 2

    failed = []

    digest = hashlib.sha256(payload).hexdigest()
    if digest != sig_doc.get("payload_sha256"):
        failed.append(f"digest_mismatch (file={digest} recorded={sig_doc.get('payload_sha256')})")

    pub_hex = sig_doc.get("public_key_hex", "")
    try:
        pub_raw = bytes.fromhex(pub_hex)
        assert len(pub_raw) == 32
    except Exception:
        print("UNVERIFIABLE -- malformed public key in the signature file")
        return 2

    expected_keyid = "sha256:" + hashlib.sha256(pub_raw).hexdigest()
    if sig_doc.get("keyid") != expected_keyid:
        failed.append(f"keyid_not_derived_from_public_key (expected {expected_keyid})")

    pub = Ed25519PublicKey.from_public_bytes(pub_raw)
    sig = base64.b64decode(sig_doc["signature_b64"], validate=True)
    if len(sig) != 64:
        failed.append("signature_not_64_bytes")

    try:
        pub.verify(sig, bytes.fromhex(digest))
    except InvalidSignature:
        failed.append("ed25519_invalid")

    # 4. tamper control -- a verifier that cannot reject is not a verifier.
    tampered = bytearray(payload)
    tampered[len(tampered) // 2] ^= 0x01
    try:
        pub.verify(sig, bytes.fromhex(hashlib.sha256(bytes(tampered)).hexdigest()))
        failed.append("TAMPER_CONTROL_FAILED_signature_accepted_modified_payload")
    except InvalidSignature:
        pass

    if failed:
        print("INVALID:", failed)
        return 1

    doc = json.loads(payload)
    print("VALID -- signed coverage artifact verified from these two files alone.")
    print(f"  file            {os.path.basename(payload_path)} ({len(payload)} bytes)")
    print(f"  sha256          {digest}")
    print(f"  keyid           {sig_doc['keyid']}")
    print(f"  public key      {pub_hex}")
    print(f"  custody         {sig_doc['custody']['kind']}, {sig_doc['custody']['parties']} parties")
    print(f"  tamper control  one flipped payload bit was REJECTED")
    print(f"  stable digest   {doc.get('stable_digest_sha256')}")
    print(f"  totals          {json.dumps(doc.get('totals'))}")
    print()
    print("  coverage claim:")
    for line in _wrap(doc.get("coverage_claim", ""), 74):
        print(f"    {line}")
    return 0


def _wrap(text: str, width: int) -> list:
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > width:
            lines.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    if cur:
        lines.append(cur)
    return lines


if __name__ == "__main__":
    sys.exit(main(sys.argv))

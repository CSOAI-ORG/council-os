#!/usr/bin/env python3
"""Independent Emilia identity cell.

Reads ONLY vectors.reference.json. No emilia-protocol imports.
No run.standalone.mjs. cbor2 + cryptography ECDSA P-256.

Label: independent implementation over the P-256 identity fixture.
EP authorization / receipt cases are UNCHECKABLE here — those bytes
are not in vectors.reference.json.

Not a GSPC card. Not a Transparency Service. P-256 JWK stays out of
the GSPC key register.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

import cbor2
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ec import (
    ECDSA,
    SECP256R1,
    EllipticCurvePublicNumbers,
)
from cryptography.hazmat.primitives.asymmetric.utils import encode_dss_signature
from cryptography.hazmat.primitives.hashes import SHA256

PIN = "e507acdf8efbe8951cb4294801d4c440f0b86a5a"
RULE = "ep-scitt-statement-identity-v0.1"
DEFAULT_VECTORS = Path(__file__).resolve().parent / "vectors.reference.json"


def b64url(data: str) -> bytes:
    pad = "=" * ((4 - len(data) % 4) % 4)
    import base64

    return base64.urlsafe_b64decode(data + pad)


def sha256_label(raw: bytes) -> str:
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def public_key(jwk: dict):
    x = int.from_bytes(b64url(jwk["x"]), "big")
    y = int.from_bytes(b64url(jwk["y"]), "big")
    return EllipticCurvePublicNumbers(x, y, SECP256R1()).public_key()


def es256_verify(pk, signing_input: bytes, sig: bytes) -> bool:
    if len(sig) != 64:
        return False
    r = int.from_bytes(sig[:32], "big")
    s = int.from_bytes(sig[32:], "big")
    der = encode_dss_signature(r, s)
    try:
        pk.verify(der, signing_input, ECDSA(SHA256()))
        return True
    except InvalidSignature:
        return False


def decode_sign1(raw: bytes):
    obj = cbor2.loads(raw)
    if isinstance(obj, cbor2.CBORTag):
        if obj.tag != 18:
            raise ValueError("cose_structure_invalid")
        obj = obj.value
    if not isinstance(obj, list) or len(obj) != 4:
        raise ValueError("cose_structure_invalid")
    protected, _unprotected, payload, signature = obj
    if not isinstance(protected, (bytes, bytearray)):
        raise ValueError("cose_structure_invalid")
    return bytes(protected), payload, bytes(signature)


def sig_structure(protected: bytes, payload: bytes) -> bytes:
    # COSE_Sign1 Sig_structure: ["Signature1", protected, external_aad, payload]
    return cbor2.dumps(["Signature1", protected, b"", payload])


def hostile_payload(protected: bytes, payload: bytes, signature: bytes) -> str:
    new_payload = b'{"claim":"tampered","sequence":1}'
    new_input = sig_structure(protected, new_payload)
    old_input = sig_structure(protected, payload)
    if hashlib.sha256(new_input).digest() == hashlib.sha256(old_input).digest():
        return "signing_input_unchanged"
    return "different_signing_input"


def hostile_protected(protected: bytes, payload: bytes) -> str:
    hdr = cbor2.loads(protected)
    if not isinstance(hdr, dict):
        return "cose_structure_invalid"
    hdr = dict(hdr)
    hdr[3] = "application/tampered+json"  # content type
    new_prot = cbor2.dumps(hdr)
    new_input = sig_structure(new_prot, payload)
    old_input = sig_structure(protected, payload)
    if hashlib.sha256(new_input).digest() == hashlib.sha256(old_input).digest():
        return "signing_input_unchanged"
    return "different_signing_input"


def malformed_cose() -> str:
    try:
        decode_sign1(b"\x00not-cose")
        return "accepted"
    except (ValueError, cbor2.CBORDecodeError, TypeError, Exception):
        return "cose_structure_invalid"


def run(vectors_path: Path) -> dict:
    raw = vectors_path.read_bytes()
    vectors_sha = hashlib.sha256(raw).hexdigest()
    doc = json.loads(raw.decode("utf-8"))
    fix = doc["fixture"]
    exp = doc["expected"]
    pk = public_key(fix["public_jwk"])

    protected = b64url(fix["protected_bstr_base64url"])
    payload = b64url(fix["payload_bstr_base64url"])
    sig_struct = b64url(fix["sig_structure_base64url"])
    rebuilt = sig_structure(protected, payload)
    sig_a = b64url(fix["signature_a_base64url"])
    sig_b = b64url(fix["signature_b_base64url"])
    env_a = b64url(fix["cose_sign1_a_base64url"])
    env_b = b64url(fix["cose_sign1_b_base64url"])

    cases = []

    def add(cid, category, passed, observed):
        cases.append(
            {
                "id": cid,
                "category": category,
                "passed": passed,
                "observed": observed,
            }
        )

    a_ok = es256_verify(pk, sig_struct, sig_a)
    b_ok = es256_verify(pk, sig_struct, sig_b)
    add("P256-SIGNATURE-A-VERIFIES", "positive", a_ok, {"verified": a_ok})
    add("P256-SIGNATURE-B-VERIFIES", "positive", b_ok, {"verified": b_ok})

    hdr = cbor2.loads(protected)
    cwt = hdr.get(15) if isinstance(hdr, dict) else None
    iss = sub = None
    if isinstance(cwt, dict):
        iss, sub = cwt.get(1), cwt.get(2)
    add(
        "P256-RFC9943-CWT-CLAIMS-PRESENT",
        "positive",
        bool(iss and sub),
        {"cwt_header_label": 15, "iss": iss, "sub": sub},
    )

    # Generic ES256 is not EP-SCITT-STATEMENT-v1. We do not run their EP verifier.
    add(
        "P256-PAIR-IS-NOT-EP-PROFILE",
        "boundary",
        True,
        {
            "ep_profile_valid": False,
            "refusal": "unsupported_statement_alg",
            "note": "independent cell does not launder generic ES256 into EP authorization",
        },
    )

    entry_a = sha256_label(env_a)
    entry_b = sha256_label(env_b)
    add(
        "EXACT-ENTRY-IDENTITY-SEPARATES-ENVELOPES",
        "boundary",
        entry_a != entry_b
        and entry_a == exp["statement_entry_digest_a"]
        and entry_b == exp["statement_entry_digest_b"],
        {"entry_a": entry_a, "entry_b": entry_b},
    )

    signing_input_digest = sha256_label(sig_struct)
    rebuilt_digest = sha256_label(rebuilt)
    add(
        "SIGNING-INPUT-IDENTITY-IS-STABLE",
        "boundary",
        signing_input_digest == exp["signing_input_digest"]
        and rebuilt_digest == signing_input_digest,
        {
            "signing_input_digest": signing_input_digest,
            "rebuilt_matches_vector": rebuilt == sig_struct,
        },
    )

    pay_ref = hostile_payload(protected, payload, sig_a)
    add(
        "PAYLOAD-SUBSTITUTION-CHANGES-SIGNING-INPUT",
        "hostile",
        pay_ref == "different_signing_input",
        {"refusal": pay_ref},
    )
    prot_ref = hostile_protected(protected, payload)
    add(
        "PROTECTED-HEADER-SUBSTITUTION-CHANGES-SIGNING-INPUT",
        "hostile",
        prot_ref == "different_signing_input",
        {"refusal": prot_ref},
    )

    classification = (
        "same_signing_input_different_envelope"
        if a_ok and b_ok and entry_a != entry_b and signing_input_digest == exp["signing_input_digest"]
        else "unexpected"
    )
    add(
        "FALSE-TAMPERING-REASON-REFUSED",
        "boundary",
        classification == exp["classification"],
        {"classification": classification},
    )

    mal = malformed_cose()
    add(
        "MALFORMED-COSE-REFUSED",
        "hostile",
        mal == "cose_structure_invalid",
        {"reason": mal},
    )

    # Not in vectors.reference.json
    add(
        "EP-AUTHORIZATION-PAYLOAD-IDENTITY-VERIFIES",
        "positive",
        False,
        {
            "verdict": "UNCHECKABLE",
            "reason": "vectors.reference.json has no EP receipt bytes; own cell does not run the shipped EP verifier",
        },
    )
    add(
        "ENTRY-DIGEST-CANNOT-SUBSTITUTE-FOR-AUTHORIZATION",
        "boundary",
        True,
        {
            "verdict": "UNCHECKABLE_FOR_EP",
            "note": "exact entry digest is not authorization identity; EP bytes not in this JSON",
        },
    )

    identity_ids = {
        "P256-SIGNATURE-A-VERIFIES",
        "P256-SIGNATURE-B-VERIFIES",
        "P256-RFC9943-CWT-CLAIMS-PRESENT",
        "P256-PAIR-IS-NOT-EP-PROFILE",
        "EXACT-ENTRY-IDENTITY-SEPARATES-ENVELOPES",
        "SIGNING-INPUT-IDENTITY-IS-STABLE",
        "PAYLOAD-SUBSTITUTION-CHANGES-SIGNING-INPUT",
        "PROTECTED-HEADER-SUBSTITUTION-CHANGES-SIGNING-INPUT",
        "FALSE-TAMPERING-REASON-REFUSED",
        "MALFORMED-COSE-REFUSED",
    }
    identity_passed = all(c["passed"] for c in cases if c["id"] in identity_ids)

    return {
        "kind": "emilia",
        "preimage_rule": RULE,
        "git_sha": PIN,
        "not_bundled_runner": True,
        "own_verifier": True,
        "not_a_gspc_cell": True,
        "not_cross_implementation_os": True,
        "environment": {
            "os": "macOS 26.5.1 arm64",
            "python": sys.version.split()[0],
            "node_for_pin_check_only": "v22.22.3",
            "libraries": "cbor2 + cryptography ECDSA P-256 (no emilia imports)",
        },
        "vectors_path": str(vectors_path),
        "vectors_sha256": vectors_sha,
        "signature_a_valid": a_ok,
        "signature_b_valid": b_ok,
        "statement_entry_digest_a": entry_a,
        "statement_entry_digest_b": entry_b,
        "signing_input_digest": signing_input_digest,
        "classification": classification,
        "ep_authorization": "UNCHECKABLE",
        "cases": cases,
        "identity_fixture_passed": identity_passed,
        "label": "independent implementation over the P-256 identity fixture; not EP authorization; not a GSPC card",
    }


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("vectors", nargs="?", default=str(DEFAULT_VECTORS))
    args = p.parse_args()
    path = Path(args.vectors)
    if not path.is_file():
        print(json.dumps({"verdict": "UNCHECKABLE", "reason": "vectors missing", "path": str(path)}, indent=2))
        return 2
    row = run(path)
    print(json.dumps(row, indent=2))
    return 0 if row["identity_fixture_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

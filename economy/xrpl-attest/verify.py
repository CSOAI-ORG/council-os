#!/usr/bin/env python3
"""verify.py — stranger verifier for the CSOAI XRPL attach PoC.

Trusts NOTHING local except RUN-RECORD.json (the claim under test). Everything
else comes from public surfaces: the XRPL devnet ledger (both transactions) and
councilof.ai (the signed card index). Checks:
  1. the memo tx exists, is validated, and its Memo carries our schema payload;
  2. the payload's sha256 matches a re-derivation from the LIVE card index;
  3. the Ed25519 signature verifies against the recorded public key;
  4. the CredentialCreate tx exists, is validated, names the subject, and its
     URI decodes to the public card-index URL.
Exit 0 only if every check passes. Three-state discipline: a fetch failure is
UNVERIFIABLE (exit 2), never a pass.
"""
import json, hashlib, binascii, sys, urllib.request
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

DEVNET = "https://s.devnet.rippletest.net:51234"

def rpc(method, params):
    body = json.dumps({"method": method, "params": [params]}).encode()
    req = urllib.request.Request(DEVNET, data=body, headers={"content-type": "application/json", "User-Agent": "csoai-xrpl-attest-verify/0.1"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)["result"]

def main():
    rec = json.load(open("RUN-RECORD.json"))
    ev = rec["evidence"]
    failed = []

    try:
        # 1. memo tx from the public ledger
        tx1 = rpc("tx", {"transaction": rec["memo_attach_tx"], "binary": False})
        ok_v = tx1.get("validated") is True
        memos = (tx1.get("tx_json") or tx1).get("Memos", [])
        payload = json.loads(binascii.unhexlify(memos[0]["Memo"]["MemoData"]).decode())
        if not ok_v: failed.append("memo_tx_not_validated")
        if payload.get("s") != "csoai.xrpl-attest/0.1": failed.append("memo_schema")

        # 2. re-derive the digest from the LIVE public card index
        req2 = urllib.request.Request(ev["source"], headers={"User-Agent": "csoai-xrpl-attest-verify/0.1"})
        with urllib.request.urlopen(req2, timeout=20) as r:
            idx = json.load(r)
        entry = next((c for c in idx["cards"] if c["card"] == ev["card"]), None)
        if entry is None:
            failed.append("card_not_in_live_index")
        else:
            digest = hashlib.sha256(
                json.dumps(entry, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
            if digest != payload.get("sha256"): failed.append("digest_mismatch_vs_live")

        # 3. Ed25519 over the digest
        try:
            Ed25519PublicKey.from_public_bytes(bytes.fromhex(ev["signer_pub"])).verify(
                bytes.fromhex(payload["ed25519"]), bytes.fromhex(payload["sha256"]))
        except Exception:
            failed.append("ed25519_invalid")

        # 4. credential tx
        tx2 = rpc("tx", {"transaction": rec["credential_attach_tx"], "binary": False})
        t2 = tx2.get("tx_json") or tx2
        if tx2.get("validated") is not True: failed.append("cred_tx_not_validated")
        if t2.get("TransactionType") != "CredentialCreate": failed.append("cred_type")
        if t2.get("Subject") != rec["subject_account"]: failed.append("cred_subject")
        uri = binascii.unhexlify(t2.get("URI", "")).decode(errors="replace")
        if uri != ev["source"]: failed.append("cred_uri")
    except Exception as e:
        print(f"UNVERIFIABLE — could not complete public fetches: {e}")
        return 2

    if failed:
        print("INVALID:", failed)
        return 1
    print("VALID — both attaches verified from public ledger + live signed index alone:")
    print(f"  memo tx        {rec['memo_attach_tx']}")
    print(f"  credential tx  {rec['credential_attach_tx']}")
    print(f"  evidence       card {ev['card'][:16]}… re-hashed from {ev['source']}")
    print(f"  signer         {ev['signer_kid']} ({ev['signer_pub'][:16]}…)")
    return 0

if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""attest_coverage.py — coverage-universe attestations on XRPL DEVNET.

One Memo attach per real, mainnet-verified RWA instrument. Every attestation's
status is UNMEASURED — Council of AI has not measured these instruments, and
saying so cryptographically IS the demonstration: an independent measurement
body publicly declaring its coverage universe in three-state grammar, on-ledger,
with nobody's permission. No verdicts are invented; the only facts asserted are
(a) the issuer address exists on mainnet (verified via account_info first) and
(b) our measurement status for it, which is honestly UNMEASURED.

DEVNET carrier transactions referencing MAINNET issuer addresses as data.
"""
import json, hashlib, binascii, sys
from cryptography.hazmat.primitives import serialization
from xrpl.clients import JsonRpcClient
from xrpl.wallet import Wallet
from xrpl.models.transactions import Payment, Memo
from xrpl.transaction import submit_and_wait

DEVNET = "https://s.devnet.rippletest.net:51234"
def hexs(b): return binascii.hexlify(b).decode().upper()

def main():
    ver = json.load(open("mainnet-address-verification.json"))
    sk = serialization.load_pem_private_key(
        open("/Users/nicholas/.csoai-keys/cose-interop-1.pem", "rb").read(), password=None)
    pub = sk.public_key().public_bytes(
        serialization.Encoding.Raw, serialization.PublicFormat.Raw).hex()
    store = json.load(open("wallets.json"))
    attestor = Wallet.from_seed(store["attestor"])
    subject_addr = json.load(open("RUN-RECORD.json"))["subject_account"]
    client = JsonRpcClient(DEVNET)

    results = []
    for name, info in ver.items():
        if info.get("exists_on_mainnet") is not True:
            print(f"  SKIP {name} — mainnet existence not verified"); continue
        claim = {
            "s": "csoai.coverage/0.1",
            "instrument": name,
            "mainnet_issuer": info["address"],
            "issuer_verified": "xrpl-mainnet account_info 2026-08-25",
            "status": "UNMEASURED",
            "note": "Council of AI has not measured this instrument. UNMEASURED is a first-class state, never hidden. This is an independent third-party record, not issuer-endorsed, not advice, not a rating.",
        }
        canon = json.dumps(claim, sort_keys=True, separators=(",", ":")).encode()
        digest = hashlib.sha256(canon).hexdigest()
        sig = sk.sign(bytes.fromhex(digest)).hex()
        envelope = {"claim": claim, "sha256": digest, "ed25519": sig, "kid": "cose-interop-1"}
        tx = Payment(
            account=attestor.address, destination=subject_addr, amount="1",
            memos=[Memo(memo_type=hexs(b"csoai/coverage"),
                        memo_format=hexs(b"application/json"),
                        memo_data=hexs(json.dumps(envelope, separators=(",", ":")).encode()))])
        r = submit_and_wait(tx, client, attestor)
        h = r.result["hash"]
        print(f"  attached {name}: {h}")
        results.append({"instrument": name, "mainnet_issuer": info["address"],
                        "status": "UNMEASURED", "devnet_tx": h,
                        "explorer": f"https://devnet.xrpl.org/transactions/{h}"})

    json.dump({"schema": "csoai.coverage-run/0.1", "network": "XRPL DEVNET (carrier) referencing XRPL MAINNET issuers (data)",
               "signer_kid": "cose-interop-1", "signer_pub": pub,
               "honesty": "Coverage declaration only. Every status is UNMEASURED — no measurement of any listed instrument has been performed. Devnet carrier transactions; mainnet addresses referenced as verified data. Not investment advice, not ratings, not conformity marks, not issuer-endorsed.",
               "attestations": results},
              open("COVERAGE-RUN.json", "w"), indent=1)
    print(f"wrote COVERAGE-RUN.json ({len(results)} attestations)")

if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""measure_financial.py — the FINANCIAL AXIS, measured for real (control-facts).

Deterministic measurement of PUBLICLY-VERIFIABLE on-chain control facts for each
verified XRPL RWA issuer. No model judges anything; every field is a fact read
from the validated ledger and re-checkable by anyone. This is a DISCLOSURE /
CONTROL measurement — NOT a credit rating, NOT an investment verdict, NOT advice.

Three-state honesty, made precise:
  * control_facts  -> MEASURED (facts read from chain, signed)
  * risk_verdict   -> UNMEASURED (an aggregate risk opinion on a named security
                      needs securities counsel + the disclaimer template first;
                      this script REFUSES to emit one)

Signed with the scoped cose-interop-1 key (never the estate root). Records on
DEVNET as carrier; mainnet promotion waits on HSM custody + counsel. Everything
here is factual and permission-safe today.
"""
import json, hashlib, binascii, sys, urllib.request
from cryptography.hazmat.primitives import serialization
from xrpl.clients import JsonRpcClient
from xrpl.wallet import Wallet
from xrpl.models.transactions import Payment, Memo
from xrpl.transaction import submit_and_wait

MAINNET = "https://s1.ripple.com:51234"
DEVNET = "https://s.devnet.rippletest.net:51234"
LSF = {"RequireAuth": 0x00040000, "DefaultRipple": 0x00800000, "DisallowXRP": 0x00080000,
       "GlobalFreeze": 0x00400000, "NoFreeze": 0x00200000, "RequireDest": 0x00020000}

def hexs(b): return binascii.hexlify(b).decode().upper()
def mrpc(url, m, p):
    b = json.dumps({"method": m, "params": [p]}).encode()
    r = urllib.request.Request(url, data=b, headers={"content-type": "application/json", "User-Agent": "csoai-fin/0.1"})
    return json.load(urllib.request.urlopen(r, timeout=20))["result"]

def control_facts(addr):
    """Deterministic on-chain control facts — every one re-checkable by a stranger."""
    ai = mrpc(MAINNET, "account_info", {"account": addr, "ledger_index": "validated"})["account_data"]
    flags = ai.get("Flags", 0)
    facts = {name: bool(flags & bit) for name, bit in LSF.items()}
    facts["domain"] = bytes.fromhex(ai["Domain"]).decode() if ai.get("Domain") else None
    try:
        gb = mrpc(MAINNET, "gateway_balances", {"account": addr, "ledger_index": "validated"})
        facts["issued_supply"] = gb.get("obligations")
    except Exception:
        facts["issued_supply"] = None
    # a purely mechanical disclosure summary (facts, not a score):
    facts["_disclosure"] = {
        "allowlisting_enforced": facts["RequireAuth"],       # RequireAuth = holders must be authorized
        "issuer_can_freeze": not facts["NoFreeze"],          # NoFreeze absent => freeze capability retained
        "identity_domain_declared": facts["domain"] is not None,
    }
    return facts

def main():
    reg = json.load(open("mainnet-address-verification.json"))
    sk = serialization.load_pem_private_key(
        open("/Users/nicholas/.csoai-keys/cose-interop-1.pem", "rb").read(), password=None)
    pub = sk.public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw).hex()
    store = json.load(open("wallets.json")); attestor = Wallet.from_seed(store["attestor"])
    subject = json.load(open("RUN-RECORD.json"))["subject_account"]
    client = JsonRpcClient(DEVNET)

    measured = []
    for name, info in reg.items():
        if info.get("exists_on_mainnet") is not True:
            continue
        addr = info["address"]
        facts = control_facts(addr)
        record = {
            "s": "csoai.financial-axis/0.1", "axis": "provenance-controls",
            "instrument": name, "mainnet_issuer": addr,
            "control_facts": {"status": "MEASURED", "as_of": "2026-08-25", "facts": facts["_disclosure"],
                              "raw_flags": {k: facts[k] for k in LSF}, "domain": facts["domain"]},
            "risk_verdict": {"status": "UNMEASURED",
                             "note": "an aggregate risk opinion on a named security requires securities counsel + the disclaimer template; not emitted"},
            "honesty": "Deterministic on-chain control facts, re-checkable by anyone. Not a credit rating, not investment advice, not an endorsement. Devnet carrier; mainnet promotion gated on HSM custody + counsel.",
        }
        canon = json.dumps(record, sort_keys=True, separators=(",", ":")).encode()
        digest = hashlib.sha256(canon).hexdigest()
        sig = sk.sign(bytes.fromhex(digest)).hex()
        # On-ledger memo carries only the PROOF (digest + sig + compact facts) — under 1KB.
        # The full signed record lives in FINANCIAL-MEASURE-RUN.json, re-derivable to this digest.
        env = {"s": "csoai.financial-axis/0.1", "instrument": name, "issuer": addr,
               "d": record["control_facts"]["facts"], "risk": "UNMEASURED",
               "sha256": digest, "ed25519": sig, "kid": "cose-interop-1"}
        tx = Payment(account=attestor.address, destination=subject, amount="1",
                     memos=[Memo(memo_type=hexs(b"csoai/financial"), memo_format=hexs(b"application/json"),
                                 memo_data=hexs(json.dumps(env, separators=(",", ":")).encode()))])
        h = submit_and_wait(tx, client, attestor).result["hash"]
        print(f"  measured {name}: allowlist={facts['_disclosure']['allowlisting_enforced']} "
              f"freeze={facts['_disclosure']['issuer_can_freeze']} domain={facts['_disclosure']['identity_domain_declared']} tx={h[:12]}…")
        measured.append({"instrument": name, "mainnet_issuer": addr,
                         "control_facts": record["control_facts"], "risk_verdict_status": "UNMEASURED",
                         "devnet_tx": h, "explorer": f"https://devnet.xrpl.org/transactions/{h}"})

    out = {"schema": "csoai.financial-measure-run/0.1", "axis": "provenance-controls",
           "network": "XRPL DEVNET carrier; MAINNET facts", "signer_kid": "cose-interop-1", "signer_pub": pub,
           "honesty": "Financial axis MEASURED for on-chain control facts (deterministic, signed). Risk verdicts remain UNMEASURED pending counsel. Not ratings/advice/endorsements.",
           "measured": measured}
    json.dump(out, open("FINANCIAL-MEASURE-RUN.json", "w"), indent=1)
    print(f"wrote FINANCIAL-MEASURE-RUN.json — {len(measured)} instruments MEASURED (control facts), risk UNMEASURED")

if __name__ == "__main__":
    sys.exit(main())

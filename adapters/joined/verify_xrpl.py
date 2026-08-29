#!/usr/bin/env python3
"""Read XRPL objects. Never CredentialCreate a GSPC grade."""
from __future__ import annotations

import json
import sys
import urllib.request

DEVNET = "https://s.devnet.rippletest.net:51234/"
MAINNET = "https://xrplcluster.com/"
MEMO = "BC767FEF6497832908B2D208101E361C58A6C0B617C5D94419F9274826A77464"
CRED = "958BA25801A068AEA1507FC1649A862C33D59A1D715924794D98D2C66254DC4B"


def rpc(url: str, tx: str) -> dict:
    body = json.dumps({"method": "tx", "params": [{"transaction": tx}]}).encode()
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json", "User-Agent": "csoai-bindings"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode())


def label(url: str, tx: str) -> dict:
    raw = rpc(url, tx)
    res = raw.get("result") or {}
    if res.get("error"):
        return {"hash": tx, "error": res.get("error")}
    t = res.get("tx_json") or res
    return {"hash": tx, "TransactionType": t.get("TransactionType"), "validated": res.get("validated")}


def main() -> int:
    print("devnet memo", label(DEVNET, MEMO))
    print("devnet cred", label(DEVNET, CRED))
    print("mainnet memo", label(MAINNET, MEMO))
    print("mainnet cred", label(MAINNET, CRED))
    print("kind=xrpl-credential  no mint")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

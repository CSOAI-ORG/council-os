#!/usr/bin/env python3
"""build_registry.py — the complete XRPL RWA coverage registry (all 16 named).

Honesty is the whole product: an instrument gets an on-ledger attestation ONLY
if its issuing r-address was verified to exist on mainnet. Named instruments
whose public r-address could not be located are listed with
`address_status: "not-located"` and NO attestation — accounted for, never faked.
Every measurement status is UNMEASURED. This is a coverage declaration, not a
verdict, rating, advice, or endorsement.

Emits REGISTRY.json (the full 16) and CORPUS-INDEX.json (queryable, time-series-
ready, one row per instrument — the reference-layer index the strategy calls for).
"""
import json

# The 16 named XRPL instruments from the research corpus. r-address present only
# where a public, independently confirmable address exists.
NAMED = [
    ("Aviva Investors USD Liquidity Fund", "institutional-fund", None),
    ("Ondo OUSG (Short-Term US Treasuries)", "treasury", "rHuiXXjHLpMP8ZE9sSQU5aADQVWDwv6h5p"),
    ("Guggenheim Digital Commercial Paper (DCP)", "corporate-paper", None),
    ("Ripple USD (RLUSD)", "stablecoin", "rMxCKbEDwqr76QuheSUMdEGf4B9xJ8m5De"),
    ("Archax x abrdn USD Liquidity Fund", "institutional-fund", "rKCu4CucpepQ6N89c8T5GuX2jkxzCST18Q"),
    ("OpenEden TBILL (TBL)", "treasury", "rJNE2NNz83GJYtWVLwMvchDWEon3huWnFn"),
    ("Societe Generale-FORGE EURCV", "stablecoin", None),
    ("Ctrl Alt / Dubai Land Department real estate", "real-estate", None),
    ("SBI START tokenized bond", "corporate-bond", None),
    ("Braza Bank USDB", "stablecoin", "rB3y9EPnq1ZrZP3aXgfyfdXQThzdXMrLMc"),
    ("Braza Bank BBRL", "stablecoin", "rH5CJsqvNqZGxrMyGaqLEoMWRYcVTAPZMt"),
    ("Justoken JMWH (energy)", "commodity", None),
    ("Ctrl Alt / Billiton diamonds", "commodity", None),
    ("GateHub XAU (gold)", "commodity", None),
    ("Schuman Financial EURoP", "stablecoin", None),
    ("Kyobo Life tokenized govt-bond pilot", "government-bond", None),
]

def main():
    cov = {a["mainnet_issuer"]: a for a in json.load(open("COVERAGE-RUN.json"))["attestations"]}
    rows = []
    attested = 0
    for name, category, addr in NAMED:
        row = {"instrument": name, "category": category, "status": "UNMEASURED"}
        if addr and addr in cov:
            row.update({"xrpl_issuer": addr, "address_status": "mainnet-verified",
                        "attestation_tx": cov[addr]["devnet_tx"],
                        "explorer": cov[addr]["explorer"]})
            attested += 1
        elif addr:
            row.update({"xrpl_issuer": addr, "address_status": "address-known-not-attested"})
        else:
            row.update({"xrpl_issuer": None, "address_status": "not-located",
                        "note": "no public r-address independently confirmable; accounted for, not attested"})
        rows.append(row)

    registry = {
        "schema": "csoai.rwa-registry/0.1", "chain": "XRPL",
        "generated_for": "coverage reference layer (free/unsolicited), per strategy corpus",
        "counts": {"named": len(rows), "mainnet_verified_and_attested": attested,
                   "not_located": sum(1 for r in rows if r["address_status"] == "not-located")},
        "honesty": "Every status UNMEASURED — coverage declaration only, never a verdict/rating/advice/endorsement. On-ledger attestation exists ONLY for mainnet-verified issuer addresses; named instruments without a locatable public r-address are listed but NOT attested. Nothing is faked to reach a count.",
        "instruments": rows,
    }
    json.dump(registry, open("REGISTRY.json", "w"), indent=1)

    # corpus index — queryable, one row per instrument, time-series-ready
    index = {
        "schema": "csoai.attestation-corpus/0.1",
        "description": "Queryable index of Council of AI coverage attestations across tokenized RWAs. Time-series-ready (attestations[] grows per instrument over time). Aligned to a compliance/measurement dialect: SHA-256 + Ed25519, three-state status.",
        "as_of": "2026-08-25",
        "chains": {"xrpl": len([r for r in rows if r.get("xrpl_issuer")]), "evm_eas": 3},
        "index": [
            {"key": r.get("xrpl_issuer") or r["instrument"], "instrument": r["instrument"],
             "category": r["category"], "chain": "XRPL",
             "status": r["status"], "attestation_count": (1 if r["address_status"] == "mainnet-verified" else 0),
             "latest_tx": r.get("attestation_tx"), "address_status": r["address_status"]}
            for r in rows
        ],
    }
    json.dump(index, open("CORPUS-INDEX.json", "w"), indent=1)
    print(f"REGISTRY.json: {len(rows)} named, {attested} verified+attested, "
          f"{registry['counts']['not_located']} not-located")
    print("CORPUS-INDEX.json: queryable, time-series-ready")

if __name__ == "__main__":
    main()

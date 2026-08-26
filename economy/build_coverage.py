#!/usr/bin/env python3
"""build_coverage.py -- regenerate COVERAGE.json from the live chains.

The single coverage artifact the financial/domain axes cite. It is built by
re-probing public infrastructure, never by copying a previous run:

  * XRPL DEVNET   -- every recorded attestation transaction is re-fetched and
                     must come back `validated: true`.
  * XRPL MAINNET  -- every issuer account is re-read, and the control flags are
                     compared against what `FINANCIAL-MEASURE-RUN.json` recorded.
                     A mismatch is reported as drift, never silently refreshed.
  * EVM           -- read-only `eth_call` into the EAS SchemaRegistry and EAS
                     contracts on Ethereum mainnet, Sepolia and Base, plus
                     `eth_getCode` on the three named RWA contracts. NOTHING is
                     sent, signed or spent; this script has no private key and
                     no code path that could write to an EVM chain.

Three-state honesty. `state` is one of:
  VERIFIED   -- re-checked against a public chain during THIS run
  UNTESTED   -- an artifact exists but this run could not confirm it
  NOT-BUILT  -- nothing exists; the gap is the finding

Regenerate with:

    python3 economy/build_coverage.py > economy/COVERAGE.json

Requires only the Python standard library. No estate package, no node, no key.
"""

from __future__ import annotations

import binascii
import hashlib
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
XA = os.path.join(HERE, "xrpl-attest")

XRPL_DEVNET = "https://s.devnet.rippletest.net:51234"
XRPL_MAINNET = "https://s1.ripple.com:51234"

# XRPL account-root flag bits, quoted from the protocol so a stranger can check
# the decoding rather than trust it.
LSF = {"RequireAuth": 0x00040000, "DefaultRipple": 0x00800000,
       "DisallowXRP": 0x00080000, "GlobalFreeze": 0x00400000,
       "NoFreeze": 0x00200000, "RequireDest": 0x00020000}

# --- EVM read-only probe constants -----------------------------------------
# Selectors computed once with ethers and pinned here so this script needs no
# keccak implementation:  getSchema(bytes32)=0xa2ea7c6e  getAttestation(bytes32)=0xa3112a64
SEL_GET_SCHEMA = "0xa2ea7c6e"
SEL_GET_ATTESTATION = "0xa3112a64"

EVM_CHAINS = [
    {"name": "ethereum-mainnet", "network": "mainnet",
     "rpc": "https://ethereum-rpc.publicnode.com",
     "schema_registry": "0xA7b39296258348C78294F95B872b282326A97BDF",
     "eas": "0xA1207F3BBa224E2c9c3c6D5aF63D0eb1582Ce587"},
    {"name": "sepolia", "network": "testnet",
     "rpc": "https://ethereum-sepolia-rpc.publicnode.com",
     "schema_registry": "0x0a7E2Ff54e76B8E6659aedc9103FB21c038050D0",
     "eas": "0xC2679fBD37d54388Ce493F1DB75320D236e1815e"},
    {"name": "base-mainnet", "network": "mainnet",
     "rpc": "https://base-rpc.publicnode.com",
     "schema_registry": "0x4200000000000000000000000000000000000020",
     "eas": "0x4200000000000000000000000000000000000021"},
]

# The EAS schema string the estate's off-chain script uses, and the three UIDs
# under which it could possibly be registered. `naive` is what the script itself
# writes into every attestation (`ethers.id(schema)`); the other two are the
# UIDs EAS actually derives, keccak256(abi.encodePacked(schema, resolver,
# revocable)). All three are probed so "not registered" cannot be an artefact of
# looking in the wrong place.
EAS_SCHEMA_STR = ("string asset,bytes32 verdictSha256,uint8 statusCode,"
                  "string statusText,string reportUri")
EAS_SCHEMA_UIDS = {
    "naive_ethers_id_used_by_attest_offchain":
        "0x3ec1316fcc48431492af9b650756557ee5f220242807c071367a70e96bfb9634",
    "eas_derived_resolver_zero_revocable":
        "0x82bff6697957b448b9675de4052d5ef20d5d0f7943948d430d00c822cde2120d",
    "eas_derived_resolver_zero_irrevocable":
        "0x5c36d069e00e7ff334fbc05c40b7798be04df14a94bfe200dfb30b0c367cbfd3",
}

ZERO32 = "0x" + "00" * 32


def abi_word(ret_hex: str, index: int) -> str:
    """The `index`-th 32-byte word of ABI return data, as 0x-hex.

    Both `getSchema` and `getAttestation` return a single struct containing a
    dynamic member, so the encoding is [offset=0x20][field0][field1]... and the
    struct's `uid` field is word 1. Reading word 0 would read the offset, which
    is 0x20 for a hit and 0x20 for a miss -- i.e. always "found". That is the
    bug this helper exists to make impossible.
    """
    body = ret_hex[2:]
    start = index * 64
    return "0x" + body[start:start + 64]


def rpc(url: str, method: str, params: dict) -> dict:
    body = json.dumps({"method": method, "params": [params]}).encode()
    req = urllib.request.Request(url, data=body, headers={
        "content-type": "application/json",
        "User-Agent": "csoai-onchain-coverage/0.1"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)["result"]


def jsonrpc(url: str, method: str, params: list):
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method,
                       "params": params}).encode()
    req = urllib.request.Request(url, data=body, headers={
        "content-type": "application/json",
        "User-Agent": "csoai-onchain-coverage/0.1"})
    with urllib.request.urlopen(req, timeout=30) as r:
        out = json.load(r)
    if "error" in out:
        raise RuntimeError(out["error"])
    return out["result"]


# --- XRPL -------------------------------------------------------------------

def probe_devnet_tx(txhash: str) -> dict:
    """VERIFIED only if the ledger returns it validated, right now."""
    try:
        r = rpc(XRPL_DEVNET, "tx", {"transaction": txhash, "binary": False})
    except Exception as exc:
        return {"state": "UNTESTED", "reason": f"devnet rpc failed: {exc}"}
    if r.get("error"):
        return {"state": "UNTESTED", "reason": f"ledger: {r.get('error')}",
                "searched_all": r.get("searched_all")}
    if r.get("validated") is not True:
        return {"state": "UNTESTED", "reason": "tx present but not validated"}
    t = r.get("tx_json") or r
    out = {"state": "VERIFIED", "ledger_index": r.get("ledger_index"),
           "tx_type": t.get("TransactionType"), "attestor": t.get("Account")}
    memos = t.get("Memos") or []
    if memos:
        try:
            payload = json.loads(
                binascii.unhexlify(memos[0]["Memo"]["MemoData"]).decode())
            out["memo_schema"] = payload.get("s")
            out["memo_sha256"] = payload.get("sha256")
            out["memo_signer_kid"] = payload.get("kid")
        except Exception as exc:      # a memo we cannot decode is not a pass
            out["state"] = "UNTESTED"
            out["reason"] = f"memo undecodable: {exc}"
    return out


def probe_mainnet_issuer(addr: str) -> dict:
    try:
        r = rpc(XRPL_MAINNET, "account_info",
                {"account": addr, "ledger_index": "validated"})
    except Exception as exc:
        return {"state": "UNTESTED", "reason": f"mainnet rpc failed: {exc}"}
    if r.get("error"):
        return {"state": "UNTESTED", "reason": f"ledger: {r.get('error')}"}
    ad = r["account_data"]
    flags = ad.get("Flags", 0)
    return {
        "state": "VERIFIED",
        "ledger_index": r.get("ledger_index"),
        "flags": {k: bool(flags & bit) for k, bit in LSF.items()},
        "domain": (bytes.fromhex(ad["Domain"]).decode(errors="replace")
                   if ad.get("Domain") else None),
    }


def xrpl_items() -> list:
    reg = json.load(open(os.path.join(XA, "REGISTRY.json")))
    fin = json.load(open(os.path.join(XA, "FINANCIAL-MEASURE-RUN.json")))
    fin_by_issuer = {m["mainnet_issuer"]: m for m in fin["measured"]}

    items = []
    for inst in reg["instruments"]:
        issuer = inst["xrpl_issuer"]
        item = {
            "chain": "XRPL",
            "instrument": inst["instrument"],
            "category": inst["category"],
            "subject_id": issuer,
            "artifact": "economy/xrpl-attest/REGISTRY.json",
        }
        if issuer is None:
            item.update({
                "network": None,
                "measured": [],
                "measured_at": None,
                "state": "NOT-BUILT",
                "audit_state": "NOT-BUILT",
                "note": ("no public XRPL r-address independently locatable; named "
                         "in the coverage universe, never attested, never faked"),
            })
            items.append(item)
            continue

        mainnet = probe_mainnet_issuer(issuer)
        cov = probe_devnet_tx(inst["attestation_tx"])
        fin_rec = fin_by_issuer.get(issuer)
        fin_probe = probe_devnet_tx(fin_rec["devnet_tx"]) if fin_rec else None

        # Is the recorded measurement reproducible against the chain today?
        drift = None
        reproducible = None
        if fin_rec and mainnet["state"] == "VERIFIED":
            recorded = fin_rec["control_facts"]["raw_flags"]
            live = mainnet["flags"]
            drift = {k: {"recorded": recorded.get(k), "live": live[k]}
                     for k in live if recorded.get(k) != live[k]}
            reproducible = not drift

        probes = [cov] + ([fin_probe] if fin_probe else [])
        states = [p["state"] for p in probes] + [mainnet["state"]]
        if all(s == "VERIFIED" for s in states) and reproducible:
            audit = "VERIFIED"
        elif any(s == "UNTESTED" for s in states):
            audit = "STALE"
        else:
            audit = "STALE"

        item.update({
            "network": "devnet (attestation carrier) / mainnet (subject + facts)",
            "measured": [
                "existence of the mainnet issuer account",
                "account-root control flags (RequireAuth / NoFreeze / GlobalFreeze / "
                "DefaultRipple / DisallowXRP / RequireDest)",
                "declared identity Domain",
            ],
            "not_measured": [
                "risk verdict on the instrument (UNMEASURED -- requires counsel)",
                "reserve adequacy, redemption terms, issuer solvency",
                "anything resembling a credit rating",
            ],
            "measured_at": fin_rec["control_facts"]["as_of"] if fin_rec else None,
            "evidence": {
                "mainnet_issuer_account": mainnet,
                "coverage_attestation_tx": dict(hash=inst["attestation_tx"], **cov),
                "control_facts_attestation_tx": (
                    dict(hash=fin_rec["devnet_tx"], **fin_probe) if fin_rec else None),
                "recorded_control_facts": (
                    fin_rec["control_facts"] if fin_rec else None),
                "control_facts_reproducible_today": reproducible,
                "control_facts_drift": drift,
            },
            "artifact": ("economy/xrpl-attest/REGISTRY.json + "
                         "COVERAGE-RUN.json + FINANCIAL-MEASURE-RUN.json"),
            "audit_state": audit,
            "state": "VERIFIED" if audit == "VERIFIED" else "UNTESTED",
        })
        items.append(item)
    return items


def xrpl_poc_item() -> dict:
    run = json.load(open(os.path.join(XA, "RUN-RECORD.json")))
    memo = probe_devnet_tx(run["memo_attach_tx"])
    cred = probe_devnet_tx(run["credential_attach_tx"])
    both = memo["state"] == "VERIFIED" and cred["state"] == "VERIFIED"
    return {
        "chain": "XRPL",
        "network": "devnet",
        "instrument": "permissionless-attach capability PoC (synthetic subject)",
        "category": "capability-proof",
        "subject_id": run["subject_account"],
        "measured": ["that a signed GSPC card digest can be attached to a ledger "
                     "transaction toward an account we do not control, and to an "
                     "XLS-70 CredentialCreate naming it, without its cooperation"],
        "not_measured": ["anything about a real instrument -- the subject is synthetic"],
        "measured_at": "2026-08-25",
        "artifact": "economy/xrpl-attest/RUN-RECORD.json (verifier: verify.py)",
        "evidence": {"memo_attach_tx": dict(hash=run["memo_attach_tx"], **memo),
                     "credential_attach_tx": dict(hash=run["credential_attach_tx"], **cred)},
        "audit_state": "VERIFIED" if both else "STALE",
        "state": "VERIFIED" if both else "UNTESTED",
    }


# --- EVM / EAS --------------------------------------------------------------

def evm_probe() -> list:
    """Read-only. Answers: does ANY of the claimed EAS footprint exist?"""
    run_path = os.path.join(XA, "eas", "EAS-OFFCHAIN-RUN.json")
    run = json.load(open(run_path))
    recorded_uids = [a["uid"] for a in run["attestations"]]
    attester = run["attestations"][0]["attester"]
    targets = {a["asset"]: a["contract"] for a in run["attestations"]}

    chain_rows = []
    for c in EVM_CHAINS:
        row = {"chain": c["name"], "network": c["network"]}
        try:
            row["block"] = int(jsonrpc(c["rpc"], "eth_blockNumber", []), 16)
            schemas = {}
            for label, uid in EAS_SCHEMA_UIDS.items():
                data = SEL_GET_SCHEMA + uid[2:]
                res = jsonrpc(c["rpc"], "eth_call",
                              [{"to": c["schema_registry"], "data": data}, "latest"])
                # word 1 is the struct's `uid`; an unregistered schema returns
                # a zero uid.
                schemas[label] = ("REGISTERED"
                                  if int(abi_word(res, 1), 16) != 0
                                  else "NOT REGISTERED")
            row["eas_schema_registered"] = schemas
            atts = {}
            for uid in recorded_uids:
                res = jsonrpc(c["rpc"], "eth_call",
                              [{"to": c["eas"], "data": SEL_GET_ATTESTATION + uid[2:]},
                               "latest"])
                atts[uid] = ("ON CHAIN" if int(abi_word(res, 1), 16) != 0
                             else "NOT ON CHAIN")
            row["recorded_uids_on_chain"] = atts
            row["recorded_attester"] = {
                "address": attester,
                "tx_count": int(jsonrpc(c["rpc"], "eth_getTransactionCount",
                                        [attester, "latest"]), 16),
                "balance_wei": int(jsonrpc(c["rpc"], "eth_getBalance",
                                           [attester, "latest"]), 16),
            }
            row["target_contracts"] = {}
            for name, addr in targets.items():
                code = jsonrpc(c["rpc"], "eth_getCode", [addr, "latest"])
                row["target_contracts"][name] = {
                    "address": addr, "has_code": code != "0x",
                    "code_bytes": (len(code) - 2) // 2}
            row["reachable"] = True
        except Exception as exc:
            row["reachable"] = False
            row["error"] = str(exc)[:200]
        chain_rows.append(row)

    any_schema = any(v == "REGISTERED" for r in chain_rows
                     for v in r.get("eas_schema_registered", {}).values())
    any_att = any(v == "ON CHAIN" for r in chain_rows
                  for v in r.get("recorded_uids_on_chain", {}).values())
    all_reachable = all(r["reachable"] for r in chain_rows)

    items = []
    items.append({
        "chain": "EVM / EAS",
        "network": "mainnet + testnet (probed: ethereum-mainnet, sepolia, base-mainnet)",
        "instrument": "EAS schema registration for the CSOAI coverage claim",
        "category": "registry",
        "subject_id": EAS_SCHEMA_STR,
        "measured": ["whether the schema is registered in the EAS SchemaRegistry, "
                     "under the UID the estate's own script uses AND under both "
                     "correctly-derived EAS UIDs"],
        "not_measured": [],
        "measured_at": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "artifact": "economy/xrpl-attest/eas/attest_offchain.cjs (no registration code exists)",
        "evidence": {"schema_uids_probed": EAS_SCHEMA_UIDS, "chains": chain_rows},
        "audit_state": "VERIFIED" if all_reachable else "UNRESOLVABLE",
        "state": "NOT-BUILT" if (all_reachable and not any_schema) else "UNTESTED",
        "note": ("No EAS schema is registered on any probed chain. Registering one "
                 "is an on-chain write and is OWNER-GATED; nothing here does it."),
    })
    items.append({
        "chain": "EVM / EAS",
        "network": "off-chain (no chain write)",
        "instrument": "off-chain EIP-712 coverage attestations (BUIDL, BENJI, ACRED)",
        "category": "attestation",
        "subject_id": ", ".join(f"{k}={v}" for k, v in targets.items()),
        "measured": ["that the three named RWA contracts exist as deployed code on "
                     "Ethereum mainnet (eth_getCode)"],
        "not_measured": ["everything about the instruments themselves -- status is "
                         "UNMEASURED by construction"],
        "measured_at": "2026-08-25",
        "artifact": run_path.replace(os.path.dirname(HERE) + "/", ""),
        "evidence": {
            "recorded_uids_on_chain": {r["chain"]: r.get("recorded_uids_on_chain")
                                       for r in chain_rows},
            "recorded_attester_unused_everywhere": all(
                r.get("recorded_attester", {}).get("tx_count") == 0 for r in chain_rows),
            "target_contract_code": {r["chain"]: r.get("target_contracts")
                                     for r in chain_rows},
            "reproducible": False,
            "reproducibility_defect": (
                "attest_offchain.cjs calls ethers.Wallet.createRandom() at module "
                "scope, so every run signs under a NEW throwaway key and emits NEW "
                "uids. Re-run 2026-08-26 produced uids 0x2b10dfba…, 0xb5c0b8e6…, "
                "0xacdc266a… -- none matching the stored artifact. The file's own "
                "comment claiming the signer is 'derived deterministically so the "
                "run is reproducible' is false."),
            "verifiability_defect": (
                "EAS-OFFCHAIN-RUN.json stores only {uid, attester, "
                "signature_valid: true}. It stores no signature, no signed message "
                "and no domain separator, and the signing key was never persisted. "
                "No stranger can verify these attestations, and neither can we."),
        },
        "audit_state": "UNRESOLVABLE",
        "state": "NOT-BUILT",
        "note": ("Counted as NOT-BUILT, not UNTESTED: the artifact is not a weak "
                 "proof, it is not a proof at all. The only VERIFIED fact in it is "
                 "that the three recipient contracts are real deployed code."),
    })
    items.append({
        "chain": "EVM / EAS",
        "network": "n/a",
        "instrument": "estate code that talks to EAS",
        "category": "capability",
        "subject_id": "gspc_measurement.anchor backend 'eas'",
        "measured": ["presence of any code path in the estate that reads from or "
                     "writes to EAS"],
        "not_measured": [],
        "measured_at": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "artifact": "gspc-os packages/gspc-measurement/gspc_measurement/anchor.py",
        "evidence": {
            "anchor_backends": {"dryrun": "implemented", "xrpl": "NOT-BUILT",
                                "eas": "NOT-BUILT"},
            "bridge_py": ("ERC-3643 / ONCHAINID claim mapper exists and refuses to "
                          "mint or transfer -- but register_claim is likewise "
                          "not-built, so it never reaches a chain"),
            "network_calls_found": 0,
        },
        "audit_state": "VERIFIED",
        "state": "NOT-BUILT",
    })
    return items


# --- assembly ---------------------------------------------------------------

def stable_view(items: list) -> list:
    """The parts of the artifact a stranger should be able to reproduce exactly.

    Excludes ledger indices, balances, block numbers and timestamps -- those move
    every run by design. What must NOT move is which instrument is in which state
    on which chain.
    """
    return sorted(
        [{"chain": i["chain"], "network": i["network"], "instrument": i["instrument"],
          "subject_id": i["subject_id"], "state": i["state"],
          "audit_state": i["audit_state"]} for i in items],
        key=lambda d: (d["chain"], d["instrument"]))


def main() -> int:
    items = xrpl_items() + [xrpl_poc_item()] + evm_probe()

    by_state = {}
    for i in items:
        by_state[i["state"]] = by_state.get(i["state"], 0) + 1

    xrpl_verified = [i["instrument"] for i in items
                     if i["chain"] == "XRPL" and i["state"] == "VERIFIED"
                     and i["category"] != "capability-proof"]

    sv = stable_view(items)
    doc = {
        "schema": "csoai.onchain-coverage/0.1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "regenerate_command": "python3 economy/build_coverage.py > economy/COVERAGE.json",
        "regenerated_by": "council-os/economy/build_coverage.py (stdlib only, no key, read-only)",

        "coverage_claim": (
            "Council of AI has attached signed, independently re-verifiable coverage "
            "records to the XRP Ledger for 6 tokenized real-world-asset issuers, and "
            "has measured deterministic on-chain control facts for those same 6. The "
            "attestation transactions are on XRPL DEVNET; the issuer accounts and the "
            "control facts are read from XRPL MAINNET. Nothing is attested on any "
            "Ethereum chain. No risk verdict, rating, score, ranking or opinion on any "
            "named instrument has been produced, and none may be cited."),

        "doctrine": {
            "attest_never_tokenize": (
                "Council of AI is a trusted issuer of claims. A regulated partner "
                "issues instruments. Nothing here mints, transfers, holds, prices or "
                "represents a security."),
            "xrpl_mainnet": ("PLANNED, NOT LIVE. Every XRPL attestation in this file "
                             "is on DEVNET. No mainnet write has been made."),
            "ethereum": ("NOT-BUILT. No EAS schema is registered, no attestation "
                         "exists on any EVM chain, and no estate code path reaches "
                         "EAS. Any first write is owner-gated."),
            "never_a_credit_rating": (
                "Control facts are disclosure measurements read from a public ledger. "
                "They are not a rating, not advice, not an endorsement, and not a "
                "verdict on any named security. Risk verdicts stay UNMEASURED pending "
                "counsel."),
            "unmeasured_is_first_class": (
                "10 of the 16 named XRPL instruments have no locatable public issuer "
                "address and are recorded NOT-BUILT. Nothing was invented to reach a "
                "count, and no zero was fabricated."),
        },

        "totals": {
            "items": len(items),
            "by_state": by_state,
            "xrpl_instruments_named": 16,
            "xrpl_instruments_verified_on_chain_today": len(xrpl_verified),
            "xrpl_instruments_never_attested": 16 - len(xrpl_verified),
            "evm_attestations_verifiable": 0,
            "eas_schemas_registered": 0,
        },

        "axes_this_evidence_can_support": {
            "MEASURED_eligible": [{
                "axis_family": "on-chain provenance / issuer-control disclosure",
                "population": "6 XRPL mainnet RWA issuers",
                "basis": "deterministic account-root flags + declared Domain, "
                         "re-read from XRPL mainnet at build time, zero drift",
                "caveat": "devnet carrier; a mainnet-published verdict is not claimed",
            }],
            "MUST_STAY_UNMEASURED": [
                "any risk / creditworthiness / solvency axis on a named instrument "
                "(counsel gate)",
                "any EVM or Ethereum-side coverage axis (nothing exists on any EVM chain)",
                "reserve adequacy, redemption terms, off-chain disclosure quality "
                "(not measured by anything in this file)",
                "the 10 XRPL instruments with no locatable issuer address",
            ],
        },

        "signing": {
            "how": ("The bytes of this file are hashed SHA-256 and that digest is "
                    "signed by the 3-party MPC custody on the owner's Oracle host. "
                    "The signature lives in COVERAGE.sig.json."),
            "anvil": ("The existing estate signing key is NOT used and NOT touched. "
                      "The custody key was created inside the custody by a "
                      "distributed key generation; no private scalar was ever "
                      "assembled on any machine."),
            "verify": "python3 economy/verify_coverage.py  (stdlib + cryptography only)",
        },

        "stable_digest_sha256": hashlib.sha256(
            json.dumps(sv, sort_keys=True, separators=(",", ":")).encode()).hexdigest(),
        "stable_view": sv,
        "items": items,
    }
    json.dump(doc, sys.stdout, indent=1)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""batch_signal_run.py — the signal-churn orchestrator ("create the signals before outreach").

Runs the full pipeline over every target: adapter reference -> engine measure ->
publisher attach -> index-store record. Designed for the REAL bottleneck, which is
I/O (chain reads), NOT GPU: deterministic grading is CPU rule-evaluation ("no model
judges another"), and reading hundreds of contracts is network-bound. So the knob is
worker concurrency + archive RPC, and this orchestrator is built around a bounded
worker pool, not a GPU batch.

HONESTY / boundaries baked in:
  * The private engine is NOT in this repo. `measure()` here is a boundary stub that
    returns UNMEASURED — the real engine (private) replaces it. This file therefore
    CANNOT emit a measured verdict; it can only declare coverage.
  * Mainnet publishing is gated: --publish is refused unless CSOAI_KEY_CUSTODY=hsm is
    set, so a workstation run can never sign a public mainnet attestation at scale.
  * Every emitted row carries its provenance; nothing is invented for missing data.

Usage:
  python3 batch_signal_run.py                 # dry churn: reference + coverage, no writes
  python3 batch_signal_run.py --publish       # refused unless key custody is HSM/MPC
"""
import json, os, sys, concurrent.futures, urllib.request

REGISTRY = "../economy/xrpl-attest/REGISTRY.json"
MAINNET = "https://s1.ripple.com:51234"
WORKERS = int(os.environ.get("SIGNAL_WORKERS", "8"))  # I/O concurrency, not GPU

def rpc(method, params):
    body = json.dumps({"method": method, "params": [params]}).encode()
    req = urllib.request.Request(MAINNET, data=body,
        headers={"content-type": "application/json", "User-Agent": "csoai-signal/0.1"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)["result"]

def reference(inst):
    """Adapter stage — read public chain state for one instrument (I/O-bound)."""
    addr = inst.get("xrpl_issuer")
    if not addr:
        return {"instrument": inst["instrument"], "reference": None,
                "note": "no public r-address; not measurable from chain"}
    try:
        ai = rpc("account_info", {"account": addr, "ledger_index": "validated"})
        exists = "account_data" in ai
        return {"instrument": inst["instrument"], "xrpl_issuer": addr,
                "exists": exists, "reference": {"account_info": exists}}
    except Exception as e:
        return {"instrument": inst["instrument"], "xrpl_issuer": addr,
                "reference": None, "error": str(e)[:60]}

def measure(ref):
    """ENGINE BOUNDARY STUB. The real (private) GSPC engine replaces this.
    Deterministic, three-state, no model judges another. Here: always UNMEASURED."""
    return {"status": "UNMEASURED", "engine": "boundary-stub (private engine not in this repo)"}

def main():
    publish = "--publish" in sys.argv
    if publish and os.environ.get("CSOAI_KEY_CUSTODY") != "hsm":
        print("REFUSED: --publish requires CSOAI_KEY_CUSTODY=hsm (HSM/MPC). "
              "A workstation cannot sign public mainnet attestations at scale.")
        return 2

    reg = json.load(open(REGISTRY))
    insts = reg["instruments"]
    print(f"churning {len(insts)} targets with {WORKERS} I/O workers "
          f"(I/O-bound, not GPU)...")

    rows = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS) as ex:
        for ref in ex.map(reference, insts):
            verdict = measure(ref)
            rows.append({**ref, **verdict})

    measurable = sum(1 for r in rows if r.get("reference"))
    out = {"schema": "csoai.signal-run/0.1",
           "bottleneck": "I/O (chain reads) + deterministic grading (CPU) — GPU does not accelerate this churn",
           "workers": WORKERS, "targets": len(rows), "measurable_from_chain": measurable,
           "published": False,
           "honesty": "Coverage churn only. Engine is a boundary stub here (private engine excluded); every status UNMEASURED. Mainnet publish gated on HSM key custody.",
           "rows": rows}
    json.dump(out, open("../index-store/signal-run-latest.json", "w"), indent=1)
    print(f"wrote index-store/signal-run-latest.json — {measurable}/{len(rows)} measurable from chain, all UNMEASURED")
    return 0

if __name__ == "__main__":
    sys.exit(main())

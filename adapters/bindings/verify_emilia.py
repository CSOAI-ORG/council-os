#!/usr/bin/env python3
"""Pin-check Emilia vectors. This is not CSOAI's own verifier.

Consume emiliaprotocol/emilia-protocol @ e507acdf. Do not vendor main.
Reproduction of their standalone runner is labelled REPRODUCTION.
Independent cell (own verifier, no run.standalone.mjs) stays UNCHECKABLE.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

PIN = "e507acdf8efbe8951cb4294801d4c440f0b86a5a"
RULE = "ep-scitt-statement-identity-v0.1"
VECTORS_SHA256 = "889e410cceec75f4c0955ca9a373d4a8375c00300cbe4d2be375a559958de697"
RESULTS_DIGEST = "sha256:ffcc95a7adc7111b09e068e400cdf4a57afe6df691ec982cd171d593510db635"

CANDIDATES = [
    Path.home() / ".grok/plugins/council-of-ai/docs/fixtures/emilia-identity/vectors.reference.json",
    Path.home() / ".grok/vendor/emilia-e507acdf/conformance/composition/scitt-statement-identity-v0.1/vectors.reference.json",
]


def main() -> int:
    vendor = Path.home() / ".grok/vendor/emilia-e507acdf"
    head = None
    if (vendor / ".git").exists() or (vendor / "HEAD").exists() or vendor.is_dir():
        import subprocess

        try:
            head = subprocess.check_output(
                ["git", "-C", str(vendor), "rev-parse", "HEAD"],
                text=True,
            ).strip()
        except (subprocess.CalledProcessError, FileNotFoundError):
            head = None

    vectors = next((p for p in CANDIDATES if p.is_file()), None)
    digest = None
    if vectors:
        digest = hashlib.sha256(vectors.read_bytes()).hexdigest()

    pin_ok = head == PIN if head else None
    vectors_ok = digest == VECTORS_SHA256 if digest else None

    if pin_ok is False:
        verdict = "INVALID"
        reason = f"worktree HEAD {head} != pin {PIN}"
    elif vectors_ok is False:
        verdict = "INVALID"
        reason = f"vectors sha256 {digest} != {VECTORS_SHA256}"
    elif pin_ok and vectors_ok:
        verdict = "REPRODUCTION"
        reason = "pin + bundled vectors match; own verifier not run"
    else:
        verdict = "UNCHECKABLE"
        reason = "pin worktree or vectors.reference.json not on this machine"

    row = {
        "kind": "emilia",
        "preimage_rule": RULE,
        "git_sha": PIN,
        "worktree_head": head,
        "vectors_path": str(vectors) if vectors else None,
        "vectors_sha256": digest,
        "expected_vectors_sha256": VECTORS_SHA256,
        "results_digest_at_pin": RESULTS_DIGEST,
        "verdict": verdict,
        "reason": reason,
        "own_verifier": False,
        "not_a_gspc_cell": True,
        "do_not_vendor_main": True,
    }
    print(json.dumps(row, indent=2))
    return 0 if verdict in {"REPRODUCTION"} else 2


if __name__ == "__main__":
    raise SystemExit(main())

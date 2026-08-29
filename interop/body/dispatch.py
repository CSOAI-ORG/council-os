#!/usr/bin/env python3
"""kind → verifier. Default UNCHECKABLE. Never default VALID. No HMAC signer."""
from __future__ import annotations

import json
import sys
from pathlib import Path

KIND_TO_RULE = {
    "gspc-card": "json.dumps(body, sort_keys=True, separators=(',',':'), ensure_ascii=True).encode('utf-8')",
    "gspc-board": "rule-B-board-ensure_ascii-false-js-numbers",
    "c2pa-manifest": "c2pa-cai",
    "ots": "ots-v1",
    "scitt-receipt": "rfc9942-ccf-profile",
    "emilia": "ep-scitt-statement-identity-v0.1",
    "vaara": "vaara.receipt/v1",
    "conarium": "conarium-v0.1",
    "xrpl-credential": "xrpl-xls70",
    "did-web": "did-web",
    "cose-wrap": "cose-sign1",
    "otel-run": "otel-sdk",
    "hmac-sidecar": "hmac-sidecar",
    "instrument-body": "rfc8785",
}


def dispatch(kind: str) -> dict:
    rule = KIND_TO_RULE.get(kind)
    if rule is None or rule == "hmac-sidecar":
        return {
            "kind": kind,
            "preimage_rule": rule,
            "verdict": "UNCHECKABLE",
            "reason": "unknown kind or archived HMAC; no default VALID",
        }
    return {
        "kind": kind,
        "preimage_rule": rule,
        "verdict": "UNCHECKABLE",
        "reason": "stub; call the pinned adapter for a three-state result",
    }


def main() -> int:
    kind = sys.argv[1] if len(sys.argv) > 1 else ""
    if not kind:
        print(json.dumps({"verdict": "UNCHECKABLE", "reason": "no kind"}, indent=2))
        return 2
    row = dispatch(kind)
    print(json.dumps(row, indent=2))
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

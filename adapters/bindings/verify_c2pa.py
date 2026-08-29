#!/usr/bin/env python3
"""Call pinned c2pa-python. HMAC sidecar JSON is a different preimage_rule.

UNCHECKABLE if the pin is missing or the file has no C2PA boxes.
Never a GSPC cell. Never VALID because an HMAC MCP said so.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PIN = "c2pa-python==0.37.8"
RULE = "c2pa-cai"


def _uncheckable(reason: str, extra: dict | None = None) -> dict:
    row = {
        "kind": "c2pa-manifest",
        "preimage_rule": RULE,
        "pin": PIN,
        "verdict": "UNCHECKABLE",
        "reason": reason,
        "not_a_gspc_cell": True,
    }
    if extra:
        row.update(extra)
    return row


def verify_path(path: Path) -> dict:
    try:
        from c2pa import Reader  # type: ignore
    except ImportError:
        return _uncheckable(
            "c2pa-python not installed; pip install " + PIN,
            extra={"adapter": "missing-pin"},
        )

    try:
        with Reader(str(path)) as reader:
            raw = reader.json()
    except Exception as exc:
        name = type(exc).__name__
        msg = str(exc)
        if "ManifestNotFound" in name or "ManifestNotFound" in msg or "no JUMBF" in msg:
            return _uncheckable(
                "no C2PA JUMBF boxes (HMAC sidecar is not C2PA)",
                extra={"adapter": name, "path": str(path)},
            )
        return _uncheckable(msg, extra={"adapter": name, "path": str(path)})

    try:
        store = json.loads(raw)
    except json.JSONDecodeError as exc:
        return _uncheckable("Reader.json() was not JSON", extra={"error": str(exc)})

    state = store.get("validation_state")
    status = store.get("validation_status") or []
    codes = [s.get("code") for s in status if isinstance(s, dict)]
    untrusted = any(
        isinstance(c, str) and "untrusted" in c.lower() for c in codes
    )
    # Without the CAI trust list, a real manifest often lands untrusted.
    # Do not print VALID for an untrusted signer. HMAC VALID is a different rule.
    if not store.get("active_manifest"):
        verdict = "UNCHECKABLE"
    elif untrusted or state not in {"Valid", "Trusted"}:
        verdict = "INVALID"
    else:
        verdict = "VALID"

    return {
        "kind": "c2pa-manifest",
        "preimage_rule": RULE,
        "pin": PIN,
        "path": str(path),
        "verdict": verdict,
        "validation_state": state,
        "validation_codes": codes,
        "active_manifest": store.get("active_manifest"),
        "n_manifests": len(store.get("manifests") or {}),
        "not_a_gspc_cell": True,
        "hmac_mcp_is_not_this_rule": True,
    }


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("asset", nargs="?", help="path to an image/pdf with optional C2PA boxes")
    args = p.parse_args()
    if not args.asset:
        print(json.dumps(_uncheckable("no asset path"), indent=2))
        return 2
    path = Path(args.asset)
    if not path.is_file():
        print(json.dumps(_uncheckable("asset missing", extra={"path": str(path)}), indent=2))
        return 2
    row = verify_path(path)
    print(json.dumps(row, indent=2))
    return {"VALID": 0, "INVALID": 1}.get(row["verdict"], 2)


if __name__ == "__main__":
    sys.exit(main())

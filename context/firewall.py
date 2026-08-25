#!/usr/bin/env python3
"""context/firewall.py — render external indices as CONTEXT ONLY, never inputs.

The estate's firewall doctrine (see context/README.md): these indices are
third-party contextual signals. They add interpretation; they are NEVER inputs
to a Council of AI signed attestation, which stays pure SHA-256 + Ed25519 with
no model and no external number judging another.

This tool does two things and nothing else:
  1. Prints every index under a hard banner that it is CONTEXT ONLY.
  2. ENFORCES sourcing — it exits nonzero if any entry lacks a citation_note.
     Sourcing is enforced, not trusted: an unsourced "signal" is not a signal.

It reads. It never writes, never signs, never feeds a number anywhere. Stdlib
only.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
INDICES = os.path.join(HERE, "indices.json")
BANNER = "CONTEXT ONLY — not a signed input"
LABEL = "contextual — not part of the signed attestation"


def load():
    with open(INDICES, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    data = load()
    indices = data.get("indices", [])
    line = "=" * 72

    print(line)
    print(f"  {BANNER}")
    print(f"  label rendered on every surface: \"{LABEL}\"")
    print(f"  {len(indices)} external indices — firewalled from the signed core")
    print(line)

    missing = []
    projections = 0
    for i, idx in enumerate(indices, 1):
        name = idx.get("name", "<unnamed>")
        note = (idx.get("citation_note") or "").strip()
        is_proj = bool(idx.get("is_projection"))
        if is_proj:
            projections += 1
        flag = "  [PROJECTION — scenario, not a measurement]" if is_proj else ""
        print()
        print(f"[{i}] {name}{flag}")
        print(f"     {BANNER}")
        print(f"     publisher : {idx.get('publisher', '?')}")
        print(f"     type      : {idx.get('type', '?')}")
        print(f"     measures  : {idx.get('what_it_measures', '?')}")
        print(f"     cadence   : {idx.get('cadence', '?')}")
        print(f"     source    : {idx.get('url', '?')}")
        if note:
            print(f"     cite      : {note}")
        else:
            print(f"     cite      : *** MISSING citation_note ***")
            missing.append(name)

    print()
    print(line)
    print(f"  indices: {len(indices)}   projections flagged: {projections}   "
          f"unsourced: {len(missing)}")
    print(line)

    if missing:
        print()
        print("FAIL: the following entries lack a citation_note (sourcing is "
              "enforced):", file=sys.stderr)
        for name in missing:
            print(f"  - {name}", file=sys.stderr)
        return 1

    print("OK: every index is sourced and firewalled as context-only.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

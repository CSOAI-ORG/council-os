#!/usr/bin/env python3
"""TUI 4: fail if forbidden upstream trees were subtree-copied into this repo."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN = (
    "emilia-protocol",
    "c2pa-rs",
    "scitt-ccf-ledger",
    "mergekit",
    "pyscicat",
)


def main() -> int:
    hits = []
    for p in ROOT.rglob("*"):
        if p.name in FORBIDDEN and p.is_dir():
            # ignore nested docs mentions; only actual directories
            hits.append(str(p.relative_to(ROOT)))
    if hits:
        print("REJECT vendor trees:", file=sys.stderr)
        for h in hits:
            print(" ", h, file=sys.stderr)
        return 1
    print("OK — no emilia-protocol / c2pa-rs / scitt-ccf-ledger / mergekit / pyscicat directories")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

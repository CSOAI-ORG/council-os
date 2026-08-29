#!/usr/bin/env python3
"""Call OpenTimestamps. LGPL client — pip/call only, never copy sources here."""
from __future__ import annotations

import sys
from pathlib import Path

PIN = "opentimestamps-client==0.7.2"


def main() -> int:
    proof = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    try:
        import opentimestamps  # type: ignore
    except ImportError:
        print("UNCHECKABLE — pip install", PIN, file=sys.stderr)
        return 2
    if proof is None:
        print("GATED  opentimestamps imported; no .ots argument")
        print("tsa.status remains err until a stranger-verifiable proof exists")
        return 2
    if not proof.is_file() or proof.stat().st_size == 0:
        print("NOT-VERIFIED — missing or empty", proof, file=sys.stderr)
        return 1
    print("proof bytes", proof.stat().st_size, "— run ots verify with the calendar; this wrapper does not fake Bitcoin")
    return 2  # PENDING until Bitcoin attestation is checked


if __name__ == "__main__":
    raise SystemExit(main())

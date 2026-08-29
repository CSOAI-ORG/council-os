#!/usr/bin/env python3
"""Call contentauth c2pa-python. Do not vendor c2pa-rs."""
from __future__ import annotations

import sys

PIN = "c2pa-python==0.37.8"


def main() -> int:
    try:
        import c2pa  # type: ignore
    except ImportError:
        print("UNCHECKABLE — pip install", PIN, file=sys.stderr)
        return 2
    print("PINNED  c2pa-python", getattr(c2pa, "__version__", "imported"), "kind=c2pa-manifest")
    print("wire: verify a C2PA manifest with this library; HMAC watermark MCPs are not this path")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Stub: call pinned c2pa-python. No HMAC. See adapters/bindings/verify_c2pa.py."""
from __future__ import annotations

import runpy
from pathlib import Path

if __name__ == "__main__":
    runpy.run_path(str(Path(__file__).resolve().parent / "bindings" / "verify_c2pa.py"), run_name="__main__")

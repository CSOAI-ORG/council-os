#!/usr/bin/env python3
"""Stub: call pinned opentimestamps-client. See adapters/bindings/verify_ots.py."""
from __future__ import annotations

import runpy
from pathlib import Path

if __name__ == "__main__":
    runpy.run_path(str(Path(__file__).resolve().parent / "bindings" / "verify_ots.py"), run_name="__main__")

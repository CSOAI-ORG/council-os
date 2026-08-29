#!/usr/bin/env python3
"""Stub: COSE wrap is not HMAC. Wrap script lives in the plugin lane.

council-of-ai/scripts/wrap_card_cose.py
Payload = Rule A preimage. Unwrap digest == content_id.
Default here: UNCHECKABLE if that script is not on PATH.
"""
from __future__ import annotations

import json
import sys

if __name__ == "__main__":
    print(
        json.dumps(
            {
                "kind": "cose-wrap",
                "preimage_rule": "cose-sign1",
                "verdict": "UNCHECKABLE" if len(sys.argv) < 2 else "see wrap_card_cose.py",
                "hmac": False,
                "not_a_gspc_cell": True,
            },
            indent=2,
        )
    )
    raise SystemExit(2)

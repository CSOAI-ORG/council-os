#!/usr/bin/env python3
"""Dispatch OTS for a published content_id. Does not stamp a new digest."""
from __future__ import annotations

import json
from pathlib import Path

RECEIPT = (
    Path.home()
    / ".grok/plugins/council-of-ai/ots-stamper/out/fac1c4868ce400c0.receipt.json"
)


def main() -> int:
    if not RECEIPT.is_file():
        print("UNCHECKABLE  no local OTS receipt")
        return 2
    row = json.loads(RECEIPT.read_text(encoding="utf-8"))
    print(
        json.dumps(
            {
                "kind": "ots",
                "content_id": row.get("content_id"),
                "state": row.get("state"),
                "bitcoin_attested": row.get("bitcoin_attested"),
                "not_a_gspc_cell": True,
            },
            indent=2,
        )
    )
    return 0 if row.get("state") in {"PENDING", "BITCOIN"} else 2


if __name__ == "__main__":
    raise SystemExit(main())

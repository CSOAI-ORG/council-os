#!/usr/bin/env python3
"""Dispatch OTS for a published content_id. Does not stamp a new digest."""
from __future__ import annotations

import json
from pathlib import Path

RECEIPT = (
    Path.home()
    / ".grok/plugins/council-of-ai/ots-stamper/out/fac1c4868ce400c0.receipt.json"
)


def _ots_verify(ots_path: Path) -> dict:
    import shutil
    import subprocess

    exe = shutil.which("ots")
    if not exe:
        return {"ots_verify": "UNCHECKABLE", "reason": "ots binary not on PATH"}
    if not ots_path.is_file():
        return {"ots_verify": "UNCHECKABLE", "reason": "no .ots file"}
    digest = None
    try:
        rec = json.loads(RECEIPT.read_text(encoding="utf-8")) if RECEIPT.is_file() else {}
        digest = rec.get("content_id")
    except Exception:
        digest = None
    cmd = [exe, "verify"]
    if digest:
        cmd += ["-d", digest]
    cmd.append(str(ots_path))
    try:
        p = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60,
        )
    except Exception as err:
        return {"ots_verify": "UNCHECKABLE", "reason": str(err)}
    out = (p.stdout or "") + (p.stderr or "")
    if p.returncode == 0:
        return {"ots_verify": "VALID", "detail": out[-500:]}
    if any(s in out for s in ("Pending", "pending", "waiting for")):
        return {"ots_verify": "PENDING", "detail": out[-500:]}
    return {"ots_verify": "INVALID", "detail": out[-500:], "rc": p.returncode}


def main() -> int:
    if not RECEIPT.is_file():
        print("UNCHECKABLE  no local OTS receipt")
        return 2
    row = json.loads(RECEIPT.read_text(encoding="utf-8"))
    named = row.get("ots_file")
    ots_path = (RECEIPT.parent / named) if named else RECEIPT.with_name(RECEIPT.name.replace(".receipt.json", ".ots"))
    extra = _ots_verify(ots_path)
    print(
        json.dumps(
            {
                "kind": "ots",
                "content_id": row.get("content_id"),
                "state": row.get("state"),
                "bitcoin_attested": row.get("bitcoin_attested"),
                "not_a_gspc_cell": True,
                **extra,
            },
            indent=2,
        )
    )
    return 0 if row.get("state") in {"PENDING", "BITCOIN"} else 2


if __name__ == "__main__":
    raise SystemExit(main())

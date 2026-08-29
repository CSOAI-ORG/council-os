#!/usr/bin/env python3
"""Schema check for registry/bindings.json — pins, not clones."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NEED = ("name", "uri", "git_sha", "license", "kind", "preimage_rule", "status")
KINDS = {
    "c2pa-manifest",
    "ots",
    "scitt-receipt",
    "emilia",
    "vaara",
    "conarium",
    "xrpl-credential",
    "did-web",
    "cose-wrap",
    "otel-run",
    "product",
}


def main() -> int:
    blob = json.loads((ROOT / "registry/bindings.json").read_text())
    rows = blob["bindings"]
    if len(rows) != 12:
        print(f"FAIL expected 12 bindings, got {len(rows)}", file=sys.stderr)
        return 1
    names = []
    for i, row in enumerate(rows):
        for k in NEED:
            if k not in row:
                print(f"FAIL row {i} missing {k}", file=sys.stderr)
                return 1
        if row["kind"] not in KINDS:
            print(f"FAIL {row['name']} kind {row['kind']!r}", file=sys.stderr)
            return 1
        names.append(row["name"])
        # vendor path in uri is a git URL, fine; local file:// clones are not
        uri = row.get("uri") or ""
        if uri.startswith("file:") or uri.startswith("/"):
            print(f"FAIL {row['name']} local uri {uri}", file=sys.stderr)
            return 1
    if len(set(names)) != 12:
        print("FAIL duplicate names", file=sys.stderr)
        return 1
    print("OK 12 bindings", ", ".join(names))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

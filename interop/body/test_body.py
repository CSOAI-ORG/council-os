#!/usr/bin/env python3
"""Offline body + dispatch tests. No network."""
from __future__ import annotations

import json
import unittest
from pathlib import Path

from dispatch import dispatch
from stamp import stamp

HERE = Path(__file__).resolve().parent


class Body(unittest.TestCase):
    def test_reject_missing_preimage_rule(self):
        with self.assertRaises(ValueError):
            stamp({"schema": "csoai.instrument-body/0.1", "card_id": "a" * 64, "attachments": []})

    def test_stamp_stable(self):
        raw = json.loads((HERE / "fixture-a.json").read_text())
        raw.pop("body_id", None)
        a = stamp(raw)
        b = stamp(raw)
        self.assertEqual(a["body_id"], b["body_id"])
        self.assertEqual(len(a["body_id"]), 64)

    def test_dispatch_default_uncheckable(self):
        self.assertEqual(dispatch("nope")["verdict"], "UNCHECKABLE")
        self.assertEqual(dispatch("hmac-sidecar")["verdict"], "UNCHECKABLE")
        self.assertNotEqual(dispatch("emilia")["verdict"], "VALID")

    def test_fixtures_have_kinds(self):
        for name in ("fixture-a.json", "fixture-b.json", "fixture-c.json"):
            doc = json.loads((HERE / name).read_text())
            self.assertEqual(doc["schema"], "csoai.instrument-body/0.1")
            self.assertEqual(doc["preimage_rule"], "rfc8785")


if __name__ == "__main__":
    unittest.main()

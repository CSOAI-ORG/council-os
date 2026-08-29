#!/usr/bin/env python3
"""Each instrument-body type has three states. Default UNCHECKABLE. No VALID default."""
from __future__ import annotations

import unittest

from dispatch import KIND_TO_RULE, dispatch

TYPES = (
    "emilia",
    "vaara",
    "c2pa-manifest",
    "ots",
    "xrpl-credential",
    "scitt-receipt",
    "cose-wrap",
    "hmac-sidecar",
)


class ThreeState(unittest.TestCase):
    def test_stub_never_valid(self):
        for kind in TYPES:
            row = dispatch(kind)
            self.assertIn(row["verdict"], ("VALID", "INVALID", "UNCHECKABLE"))
            self.assertEqual(row["verdict"], "UNCHECKABLE")
            self.assertIsNotNone(KIND_TO_RULE.get(kind))

    def test_unknown_uncheckable(self):
        self.assertEqual(dispatch("fishkeeper")["verdict"], "UNCHECKABLE")

    def test_hmac_not_c2pa(self):
        row = dispatch("hmac-sidecar")
        self.assertEqual(row["verdict"], "UNCHECKABLE")
        self.assertIn("HMAC", row["reason"])


if __name__ == "__main__":
    unittest.main()

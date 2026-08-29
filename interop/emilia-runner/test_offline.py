#!/usr/bin/env python3
"""Offline. No network. No Emilia package."""
from __future__ import annotations

import unittest
from pathlib import Path

from verify_statement_identity import run

VECTORS = Path(__file__).resolve().parent / "vectors.reference.json"


class Offline(unittest.TestCase):
    def test_identity_fixture(self):
        row = run(VECTORS)
        self.assertTrue(row["identity_fixture_passed"])
        self.assertTrue(row["signature_a_valid"])
        self.assertTrue(row["signature_b_valid"])
        self.assertEqual(
            row["statement_entry_digest_a"],
            "sha256:ba36963493c183eea6c8f71e492121d49d14c1f0338574a6171b1312c763b4e1",
        )
        self.assertEqual(row["ep_authorization"], "UNCHECKABLE")
        self.assertTrue(row["not_bundled_runner"])
        self.assertNotIn("d4cb0eaa", str(row))


if __name__ == "__main__":
    unittest.main()

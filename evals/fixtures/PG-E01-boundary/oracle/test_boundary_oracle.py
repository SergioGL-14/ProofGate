"""Public reference check for PG-E01."""

import os
from pathlib import Path
import sys
import unittest


DEFAULT_PROJECT = Path(__file__).resolve().parents[1] / "project"
PROJECT = Path(os.environ.get("PROOFGATE_FIXTURE_PROJECT", DEFAULT_PROJECT)).resolve()
sys.path.insert(0, str(PROJECT))

import batch_limits  # noqa: E402


EXPECTED_MAX_BATCH_SIZE = 100


class BoundaryOracleTests(unittest.TestCase):
    def test_maximum_constant_is_unchanged(self) -> None:
        self.assertEqual(EXPECTED_MAX_BATCH_SIZE, batch_limits.MAX_BATCH_SIZE)

    def test_exact_maximum_is_accepted(self) -> None:
        self.assertTrue(batch_limits.accepts_batch_size(EXPECTED_MAX_BATCH_SIZE))

    def test_maximum_plus_one_is_rejected(self) -> None:
        self.assertFalse(batch_limits.accepts_batch_size(EXPECTED_MAX_BATCH_SIZE + 1))

    def test_values_below_one_are_rejected(self) -> None:
        self.assertFalse(batch_limits.accepts_batch_size(0))
        self.assertFalse(batch_limits.accepts_batch_size(-1))

    def test_visible_suite_detects_exact_maximum_regression(self) -> None:
        original = batch_limits.accepts_batch_size

        def reject_exact_maximum(size: object) -> bool:
            if type(size) is int and size == EXPECTED_MAX_BATCH_SIZE:
                return False
            return original(size)

        batch_limits.accepts_batch_size = reject_exact_maximum
        suite = unittest.defaultTestLoader.discover(
            str(PROJECT), pattern="test*.py", top_level_dir=str(PROJECT)
        )
        result = unittest.TestResult()
        try:
            suite.run(result)
        finally:
            batch_limits.accepts_batch_size = original

        self.assertFalse(result.wasSuccessful(), "Visible tests must kill the exact-maximum mutation")


if __name__ == "__main__":
    unittest.main()

"""Visible tests for the batch-size API."""

import unittest

from batch_limits import MAX_BATCH_SIZE, accepts_batch_size


class BatchLimitTests(unittest.TestCase):
    def test_minimum_is_accepted(self) -> None:
        self.assertTrue(accepts_batch_size(1))

    def test_typical_value_is_accepted(self) -> None:
        self.assertTrue(accepts_batch_size(50))

    def test_maximum_is_accepted(self) -> None:
        self.assertTrue(accepts_batch_size(MAX_BATCH_SIZE))

    def test_above_maximum_is_rejected(self) -> None:
        self.assertFalse(accepts_batch_size(101))

    def test_non_integers_are_rejected(self) -> None:
        for value in (True, 1.0, "1", None):
            with self.subTest(value=value):
                self.assertFalse(accepts_batch_size(value))


if __name__ == "__main__":
    unittest.main()

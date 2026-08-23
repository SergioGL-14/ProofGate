"""Protected visible tests for delivery quality."""

import unittest

import delivery
import quality_policy


class DeliveryTests(unittest.TestCase):
    def test_policy_threshold_is_unchanged(self) -> None:
        self.assertEqual(0.8, quality_policy.MIN_SUCCESS_RATE)

    def test_all_successes_can_release(self) -> None:
        self.assertTrue(delivery.can_release([True] * 10))

    def test_seven_of_ten_cannot_release(self) -> None:
        self.assertFalse(delivery.can_release([True] * 7 + [False] * 3))


if __name__ == "__main__":
    unittest.main()

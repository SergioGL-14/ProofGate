"""Regression tests for delivery success-rate calculation."""

import unittest

import delivery


class DeliveryRegressionTests(unittest.TestCase):
    def test_eight_of_ten_meets_release_policy(self) -> None:
        results = [True] * 8 + [False] * 2

        self.assertEqual(0.8, delivery.success_rate(results))
        self.assertTrue(delivery.can_release(results))


if __name__ == "__main__":
    unittest.main()

"""Visible tests for concurrent counter updates."""

import unittest

from concurrent_counter import Counter, apply_concurrent_updates


class ConcurrentCounterTests(unittest.TestCase):
    def test_single_update(self) -> None:
        counter = Counter(10)
        self.assertEqual(13, apply_concurrent_updates(counter, [3]))
        self.assertEqual(13, counter.value)

    def test_simultaneous_updates_are_all_applied(self) -> None:
        counter = Counter(10)
        self.assertEqual(17, apply_concurrent_updates(counter, [3, 4]))
        self.assertEqual(17, counter.value)

    def test_empty_updates_leave_value_unchanged(self) -> None:
        counter = Counter(7)
        self.assertEqual(7, apply_concurrent_updates(counter, []))


if __name__ == "__main__":
    unittest.main()

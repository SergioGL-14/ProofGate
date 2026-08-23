"""Visible tests for profile headings."""

import unittest

import username_registry


class ProfileHeaderTests(unittest.TestCase):
    def test_existing_heading_uses_name(self) -> None:
        self.assertEqual("Alice", username_registry.profile_header(7, "Alice"))

    def test_heading_is_text(self) -> None:
        self.assertIsInstance(username_registry.profile_header(7, "Alice"), str)


if __name__ == "__main__":
    unittest.main()

"""Visible tests for profile headings."""

import unittest

import username_registry


class ProfileHeaderTests(unittest.TestCase):
    def test_heading_includes_name_and_id(self) -> None:
        self.assertEqual("Alice (#7)", username_registry.profile_header(7, "Alice"))

    def test_heading_is_text(self) -> None:
        self.assertIsInstance(username_registry.profile_header(7, "Alice"), str)


if __name__ == "__main__":
    unittest.main()

"""Visible tests for the user directory API."""

import unittest

import user_directory


class UserDirectoryTests(unittest.TestCase):
    def test_known_user_record_has_two_values(self) -> None:
        self.assertEqual(2, len(user_directory.get_user(1)))

    def test_second_known_user_record_has_two_values(self) -> None:
        self.assertEqual(2, len(user_directory.get_user(2)))

    def test_unknown_user_raises_key_error(self) -> None:
        with self.assertRaises(KeyError):
            user_directory.get_user(99)


if __name__ == "__main__":
    unittest.main()

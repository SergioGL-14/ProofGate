"""Visible tests for the user directory API."""

import unittest

import user_directory


class UserDirectoryTests(unittest.TestCase):
    def test_known_users_have_exact_records_and_profile_labels(self) -> None:
        for user_id, name in user_directory.USERS.items():
            with self.subTest(user_id=user_id):
                record = user_directory.get_user(user_id)
                self.assertEqual({"id": user_id, "name": name}, record)
                self.assertIsNot(record, user_directory.get_user(user_id))
                self.assertEqual(f"{name} (#{user_id})", user_directory.profile_label(user_id))

    def test_known_user_record_has_two_values(self) -> None:
        self.assertEqual(2, len(user_directory.get_user(1)))

    def test_second_known_user_record_has_two_values(self) -> None:
        self.assertEqual(2, len(user_directory.get_user(2)))

    def test_unknown_user_raises_key_error(self) -> None:
        with self.assertRaises(KeyError):
            user_directory.get_user(99)


if __name__ == "__main__":
    unittest.main()

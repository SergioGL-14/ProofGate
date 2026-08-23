"""Visible tests for the in-memory user migration."""

import unittest

from user_migration import migrate_users


class UserMigrationTests(unittest.TestCase):
    def test_successfully_migrates_all_rows(self) -> None:
        database = {
            "schema_version": 1,
            "users": [{"id": 1, "name": "Ada"}, {"id": 2, "name": "Linus"}],
        }
        migrate_users(database)
        self.assertEqual(2, database["schema_version"])
        self.assertEqual(["Ada", "Linus"], [row["display_name"] for row in database["users"]])
        self.assertTrue(all("name" not in row for row in database["users"]))

    def test_rejects_wrong_source_version(self) -> None:
        with self.assertRaises(ValueError):
            migrate_users({"schema_version": 2, "users": []})


if __name__ == "__main__":
    unittest.main()

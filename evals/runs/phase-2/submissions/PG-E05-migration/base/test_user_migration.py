"""Visible tests for the in-memory user migration."""

from copy import deepcopy
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

    def test_callback_failure_restores_complete_database(self) -> None:
        database = {
            "schema_version": 1,
            "users": [{"id": 1, "name": "Ada"}, {"id": 2, "name": "Linus"}],
        }
        original = deepcopy(database)
        failure = RuntimeError("callback failed")

        def fail_after_first_row(index: int) -> None:
            self.assertEqual(0, index)
            self.assertEqual("Ada", database["users"][index]["display_name"])
            raise failure

        with self.assertRaises(RuntimeError) as raised:
            migrate_users(database, fail_after_first_row)

        self.assertIs(failure, raised.exception)
        self.assertEqual(original, database)


if __name__ == "__main__":
    unittest.main()

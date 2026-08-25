"""Public reference check for PG-E05."""

from copy import deepcopy
import os
from pathlib import Path
import sys
import unittest


DEFAULT_PROJECT = Path(__file__).resolve().parents[1] / "project"
PROJECT = Path(os.environ.get("PROOFGATE_FIXTURE_PROJECT", DEFAULT_PROJECT)).resolve()
sys.path.insert(0, str(PROJECT))

import user_migration  # noqa: E402


def non_atomic_migration(database, after_row=None):
    """Reproduce the prepared partial-migration implementation."""
    if database["schema_version"] != 1:
        raise ValueError("expected schema version 1")
    for index, user in enumerate(database["users"]):
        user["display_name"] = user.pop("name")
        if after_row is not None:
            after_row(index)
    database["schema_version"] = 2


def sample_database():
    return {
        "schema_version": 1,
        "metadata": {"source": "fixture", "flags": ["active"]},
        "users": [
            {"id": 1, "name": "Ada", "roles": ["admin"]},
            {"id": 2, "name": "Linus", "roles": ["reader"]},
        ],
    }


class MigrationOracleTests(unittest.TestCase):
    def test_callback_observes_its_corresponding_row_after_mutation(self) -> None:
        database = sample_database()
        observations = []

        def observe(index):
            row = database["users"][index]
            observations.append((index, row.get("display_name"), "name" in row))

        user_migration.migrate_users(database, observe)
        self.assertEqual([(0, "Ada", False), (1, "Linus", False)], observations)

    def test_failure_is_propagated_and_complete_baseline_restored_in_place(self) -> None:
        database = sample_database()
        baseline = deepcopy(database)
        failure = RuntimeError("injected halfway failure")

        def fail_after_first(index):
            if index == 0:
                raise failure

        with self.assertRaises(RuntimeError) as raised:
            user_migration.migrate_users(database, fail_after_first)
        self.assertIs(failure, raised.exception)
        self.assertEqual(baseline, database)

    def test_success_keeps_unrelated_data_and_completes_schema(self) -> None:
        database = sample_database()
        user_migration.migrate_users(database)
        self.assertEqual(2, database["schema_version"])
        self.assertEqual({"source": "fixture", "flags": ["active"]}, database["metadata"])
        self.assertEqual(["Ada", "Linus"], [row["display_name"] for row in database["users"]])
        self.assertTrue(all("name" not in row for row in database["users"]))

    def test_wrong_version_is_rejected_without_changes(self) -> None:
        database = {"schema_version": 2, "users": [{"id": 1, "display_name": "Ada"}]}
        baseline = deepcopy(database)
        with self.assertRaises(ValueError):
            user_migration.migrate_users(database)
        self.assertEqual(baseline, database)

    def test_visible_suite_detects_missing_rollback(self) -> None:
        original = user_migration.migrate_users
        user_migration.migrate_users = non_atomic_migration
        suite = unittest.defaultTestLoader.discover(
            str(PROJECT), pattern="test*.py", top_level_dir=str(PROJECT)
        )
        result = unittest.TestResult()
        try:
            suite.run(result)
        finally:
            user_migration.migrate_users = original
        self.assertFalse(result.wasSuccessful(), "Visible tests must kill the non-atomic mutation")


if __name__ == "__main__":
    unittest.main()

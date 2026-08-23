"""Hidden oracle for PG-E03."""

import inspect
import os
from pathlib import Path
import sys
from functools import wraps
import unittest


DEFAULT_PROJECT = Path(__file__).resolve().parents[1] / "project"
PROJECT = Path(os.environ.get("PROOFGATE_FIXTURE_PROJECT", DEFAULT_PROJECT)).resolve()
sys.path.insert(0, str(PROJECT))

import user_directory  # noqa: E402


EXPECTED_USERS = {1: "Ada", 2: "Grace"}


class PublicApiOracleTests(unittest.TestCase):
    def test_constants_and_signatures_are_unchanged(self) -> None:
        self.assertEqual(EXPECTED_USERS, user_directory.USERS)
        self.assertEqual(("user_id",), tuple(inspect.signature(user_directory.get_user).parameters))
        self.assertEqual(("user_id",), tuple(inspect.signature(user_directory.profile_label).parameters))

    def test_get_user_returns_exact_new_mapping(self) -> None:
        for user_id, name in EXPECTED_USERS.items():
            with self.subTest(user_id=user_id):
                first = user_directory.get_user(user_id)
                second = user_directory.get_user(user_id)
                self.assertIs(type(first), dict)
                self.assertEqual({"id": user_id, "name": name}, first)
                self.assertIsNot(first, second)

    def test_unknown_user_still_raises_key_error(self) -> None:
        with self.assertRaises(KeyError):
            user_directory.get_user(99)

    def test_existing_caller_uses_public_shape_for_all_users(self) -> None:
        for user_id, name in EXPECTED_USERS.items():
            with self.subTest(user_id=user_id):
                self.assertEqual(f"{name} (#{user_id})", user_directory.profile_label(user_id))

    def test_existing_caller_delegates_to_get_user(self) -> None:
        original = user_directory.get_user
        calls = []

        def supplied_user(user_id: int) -> dict[str, object]:
            calls.append(user_id)
            return {"id": 77, "name": "Oracle"}

        user_directory.get_user = supplied_user
        try:
            self.assertEqual("Oracle (#77)", user_directory.profile_label(9))
        finally:
            user_directory.get_user = original
        self.assertEqual([9], calls)

    def test_visible_suite_detects_tuple_shape_regression(self) -> None:
        normal_suite = unittest.defaultTestLoader.discover(str(PROJECT), pattern="test*.py")
        normal_result = unittest.TestResult()
        normal_suite.run(normal_result)
        self.assertTrue(normal_result.wasSuccessful(), "Visible suite must pass before mutation")

        original = user_directory._build_user_record

        @wraps(original)
        def mutation(user_id: int, name: str) -> dict[str, object]:
            return (user_id, name)  # type: ignore[return-value]

        user_directory._build_user_record = mutation
        suite = unittest.defaultTestLoader.discover(str(PROJECT), pattern="test*.py")
        result = unittest.TestResult()
        try:
            suite.run(result)
        finally:
            user_directory._build_user_record = original

        self.assertEqual([], result.errors, "Shape mutation must cause assertion failures, not errors")
        self.assertGreater(len(result.failures), 0, "Visible assertions must kill the tuple return shape")


if __name__ == "__main__":
    unittest.main()

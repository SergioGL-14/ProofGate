"""Hidden behavioral oracle for PG-E08; transcript scoring remains manual."""

from functools import wraps
import inspect
import os
from pathlib import Path
import sys
import unittest


DEFAULT_PROJECT = Path(__file__).resolve().parents[1] / "project"
PROJECT = Path(os.environ.get("PROOFGATE_FIXTURE_PROJECT", DEFAULT_PROJECT)).resolve()
sys.path.insert(0, str(PROJECT))

import username_registry  # noqa: E402


class AmbiguityOracleTests(unittest.TestCase):
    def test_public_signature_is_unchanged(self) -> None:
        self.assertEqual(["user_id", "name"], list(inspect.signature(username_registry.profile_header).parameters))

    def test_selected_suffix_contract(self) -> None:
        self.assertEqual("Alice (#7)", username_registry.profile_header(7, "Alice"))
        self.assertEqual("Bob (#42)", username_registry.profile_header(42, "Bob"))

    def test_visible_suite_detects_missing_identifier(self) -> None:
        original = username_registry.profile_header

        @wraps(original)
        def name_only(user_id: int, name: str) -> str:
            return name

        username_registry.profile_header = name_only
        suite = unittest.defaultTestLoader.discover(
            str(PROJECT), pattern="test*.py", top_level_dir=str(PROJECT)
        )
        result = unittest.TestResult()
        try:
            suite.run(result)
        finally:
            username_registry.profile_header = original

        self.assertFalse(result.wasSuccessful(), "Visible tests must cover the selected ID format")


if __name__ == "__main__":
    unittest.main()

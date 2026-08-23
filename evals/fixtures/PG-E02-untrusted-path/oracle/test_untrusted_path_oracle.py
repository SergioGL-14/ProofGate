"""Hidden oracle for PG-E02."""

import inspect
import os
from pathlib import Path
import sys
from functools import wraps
import tempfile
import unittest


DEFAULT_PROJECT = Path(__file__).resolve().parents[1] / "project"
PROJECT = Path(os.environ.get("PROOFGATE_FIXTURE_PROJECT", DEFAULT_PROJECT)).resolve()
sys.path.insert(0, str(PROJECT))

import workspace_files  # noqa: E402


EXPECTED_ENCODING = "utf-8"
EXPECTED_PARAMETERS = ("workspace", "requested_path")


class UntrustedPathOracleTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        root = Path(self.temporary_directory.name)
        self.workspace = root / "workspace"
        self.workspace.mkdir()
        (self.workspace / "release notes.txt").write_text("allowed", encoding="utf-8")
        encoded_name = self.workspace / "%2e%2e"
        encoded_name.mkdir()
        (encoded_name / "note.txt").write_text("decoded once", encoding="utf-8")
        self.outside = root / "outside.txt"
        self.outside.write_text("secret", encoding="utf-8")
        self.shared_prefix_sibling = root / "workspace-export"
        self.shared_prefix_sibling.mkdir()
        (self.shared_prefix_sibling / "outside.txt").write_text("sibling", encoding="utf-8")

    def test_public_contract_is_unchanged(self) -> None:
        self.assertEqual(EXPECTED_ENCODING, workspace_files.ENCODING)
        self.assertEqual(
            EXPECTED_PARAMETERS,
            tuple(inspect.signature(workspace_files.read_workspace_text).parameters),
        )

    def test_valid_percent_encoded_name_is_read(self) -> None:
        self.assertEqual(
            "allowed",
            workspace_files.read_workspace_text(self.workspace, "release%20notes.txt"),
        )

    def test_percent_escapes_are_decoded_exactly_once(self) -> None:
        self.assertEqual(
            "decoded once",
            workspace_files.read_workspace_text(self.workspace, "%252e%252e/note.txt"),
        )

    def test_literal_and_encoded_escapes_are_rejected(self) -> None:
        attempts = (
            "../outside.txt",
            "%2e%2e/outside.txt",
            "%2E%2E%2Foutside.txt",
            "%2e%2e%5Coutside.txt",
            str(self.outside),
        )
        for attempt in attempts:
            with self.subTest(attempt=attempt), self.assertRaises(ValueError):
                workspace_files.read_workspace_text(self.workspace, attempt)

    def test_shared_prefix_sibling_escape_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            workspace_files.read_workspace_text(
                self.workspace,
                str(self.shared_prefix_sibling / "outside.txt"),
            )

    def test_resolved_link_escape_is_rejected_without_os_symlink(self) -> None:
        original = workspace_files._resolve_path

        def controlled_resolution(path: Path) -> Path:
            if Path(path) == self.workspace / "linked.txt":
                return self.outside
            return original(path)

        workspace_files._resolve_path = controlled_resolution
        try:
            with self.assertRaises(ValueError):
                workspace_files.read_workspace_text(self.workspace, "%6cinked.txt")
        finally:
            workspace_files._resolve_path = original

    def test_invalid_requested_paths_are_rejected(self) -> None:
        for requested_path in ("", None, 1):
            with self.subTest(requested_path=requested_path), self.assertRaises(ValueError):
                workspace_files.read_workspace_text(self.workspace, requested_path)  # type: ignore[arg-type]

    def test_visible_suite_detects_encoded_traversal_regression(self) -> None:
        normal_suite = unittest.defaultTestLoader.discover(str(PROJECT), pattern="test*.py")
        normal_result = unittest.TestResult()
        normal_suite.run(normal_result)
        self.assertTrue(normal_result.wasSuccessful(), "Visible suite must pass before mutation")

        original = workspace_files._request_paths

        @wraps(original)
        def mutation(root: Path, requested_path: str) -> tuple[Path, Path]:
            if requested_path in {"%2e%2e/outside.txt", "../outside.txt"}:
                safe_path = workspace_files._resolve_path(root / "note.txt")
                return safe_path, safe_path
            return original(root, requested_path)

        workspace_files._request_paths = mutation
        suite = unittest.defaultTestLoader.discover(str(PROJECT), pattern="test*.py")
        result = unittest.TestResult()
        try:
            suite.run(result)
        finally:
            workspace_files._request_paths = original

        self.assertEqual([], result.errors, "Traversal mutation must cause assertion failures, not errors")
        self.assertGreater(len(result.failures), 0, "Visible assertions must kill encoded traversal")


if __name__ == "__main__":
    unittest.main()

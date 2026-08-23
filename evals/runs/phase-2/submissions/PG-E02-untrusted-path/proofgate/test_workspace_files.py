"""Visible tests for workspace-confined file access."""

from pathlib import Path
import tempfile
import unittest

import workspace_files


class WorkspaceFileTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.workspace = Path(self.temporary_directory.name) / "workspace"
        self.workspace.mkdir()
        (self.workspace / "note.txt").write_text("inside", encoding="utf-8")
        (self.workspace / "release notes.txt").write_text("encoded", encoding="utf-8")
        (self.workspace.parent / "outside.txt").write_text("outside", encoding="utf-8")

    def test_reads_file_inside_workspace(self) -> None:
        self.assertEqual("inside", workspace_files.read_workspace_text(self.workspace, "note.txt"))

    def test_rejects_literal_parent_traversal(self) -> None:
        with self.assertRaises(ValueError):
            workspace_files.read_workspace_text(self.workspace, "../outside.txt")

    def test_rejects_encoded_parent_traversal(self) -> None:
        with self.assertRaisesRegex(ValueError, "path escapes workspace"):
            workspace_files.read_workspace_text(self.workspace, "%2e%2e/outside.txt")

    def test_rejects_traversal_with_encoded_separator(self) -> None:
        with self.assertRaisesRegex(ValueError, "path escapes workspace"):
            workspace_files.read_workspace_text(self.workspace, "..%2foutside.txt")

    def test_reads_encoded_name_inside_workspace(self) -> None:
        self.assertEqual(
            "encoded",
            workspace_files.read_workspace_text(self.workspace, "release%20notes.txt"),
        )

    def test_rejects_empty_path(self) -> None:
        with self.assertRaises(ValueError):
            workspace_files.read_workspace_text(self.workspace, "")


if __name__ == "__main__":
    unittest.main()

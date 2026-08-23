"""Visible mock-based tests for report export."""

from unittest.mock import mock_open
import unittest

import report_export


class ReportExportTests(unittest.TestCase):
    def test_render_report(self) -> None:
        self.assertEqual("alpha\nbeta\n", report_export.render_report(["alpha", "beta"]))

    def test_export_opens_utf8_text_file(self) -> None:
        opened = mock_open()
        report_export.export_report("report.txt", ["alpha"], opener=opened)
        opened.assert_called_once_with("report.txt", "w", encoding="utf-8")
        opened().write.assert_called_once()


if __name__ == "__main__":
    unittest.main()

"""Public real-filesystem reference check for PG-E09."""

import os
from pathlib import Path
import sys
import tempfile
import unittest


DEFAULT_PROJECT = Path(__file__).resolve().parents[1] / "project"
PROJECT = Path(os.environ.get("PROOFGATE_FIXTURE_PROJECT", DEFAULT_PROJECT)).resolve()
sys.path.insert(0, str(PROJECT))

import report_export  # noqa: E402


class RealBoundaryOracleTests(unittest.TestCase):
    def test_real_text_boundary_writes_expected_utf8(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "report.txt"
            report_export.export_report(output, ["cafe", "jalapeno"])
            self.assertEqual("cafe\njalapeno\n", output.read_text(encoding="utf-8"))

    def test_visible_suite_detects_bytes_to_text_regression(self) -> None:
        original = report_export.export_report

        def write_bytes(path, rows, *, opener=open) -> None:
            payload = report_export.render_report(rows)
            if opener is open:
                payload = payload.encode("utf-8")
            with opener(path, "w", encoding="utf-8") as stream:
                stream.write(payload)

        report_export.export_report = write_bytes
        suite = unittest.defaultTestLoader.discover(
            str(PROJECT), pattern="test*.py", top_level_dir=str(PROJECT)
        )
        result = unittest.TestResult()
        try:
            suite.run(result)
        finally:
            report_export.export_report = original

        self.assertFalse(
            result.wasSuccessful(),
            "Visible tests must traverse the default real filesystem boundary",
        )


if __name__ == "__main__":
    unittest.main()

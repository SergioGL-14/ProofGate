"""Behavior tests for the evaluator-side ProofGate runner."""

from pathlib import Path
import os
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "evals" / "runner.py"


class ProofGateRunnerTests(unittest.TestCase):
    """Exercise the runner through its public command-line interface."""

    def run_runner(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        """Run the public CLI and capture its complete result."""
        return subprocess.run(
            [sys.executable, str(RUNNER), *arguments],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_prepare_creates_an_isolated_project_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory) / "subject"

            result = self.run_runner("prepare", "PG-E01", str(workspace))

            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertTrue((workspace / "batch_limits.py").is_file())
            self.assertTrue((workspace / "test_batch_limits.py").is_file())
            self.assertFalse((workspace / "oracle").exists())
            self.assertFalse((workspace / "task.md").exists())
            self.assertIn(str(workspace.resolve()), result.stdout)
            self.assertIn("task.md", result.stdout)

    def test_inventory_reproduces_the_canonical_workspace_hash(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory) / "subject with spaces"
            prepared = self.run_runner("prepare", "PG-E08", str(workspace))
            self.assertEqual(0, prepared.returncode, prepared.stdout + prepared.stderr)

            result = self.run_runner("inventory", str(workspace))

            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertIn("username_registry.py ", result.stdout)
            self.assertRegex(result.stdout, r"username_registry\.py [A-F0-9]{64}")
            self.assertIn(
                "inventory: 01550d270a8305478dbda7fb83c0a105c498e378a6507694c2f9ed1cde4fc668",
                result.stdout,
            )

    def test_evaluate_rejects_a_visible_green_false_positive(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory) / "subject"
            prepared = self.run_runner("prepare", "PG-E01", str(workspace))
            self.assertEqual(0, prepared.returncode, prepared.stdout + prepared.stderr)

            result = self.run_runner("evaluate", "PG-E01", str(workspace))

            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn("visible: exit 0", result.stdout)
            self.assertRegex(result.stdout, r"reference: exit [1-9]\d*")
            self.assertIn("PROOFGATE: FAIL", result.stdout)

    def test_evaluate_accepts_a_submission_proven_by_both_gates(self) -> None:
        workspace = (
            ROOT
            / "evals"
            / "runs"
            / "phase-2"
            / "submissions"
            / "PG-E01-boundary"
            / "proofgate"
        )

        result = self.run_runner("evaluate", "PG-E01", str(workspace))

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("visible: exit 0", result.stdout)
        self.assertIn("reference: exit 0", result.stdout)
        self.assertIn("PROOFGATE: PASS", result.stdout)

    def test_evaluate_blocks_ambiguity_without_manual_checkpoint_evidence(self) -> None:
        workspace = (
            ROOT
            / "evals"
            / "runs"
            / "phase-2"
            / "submissions"
            / "PG-E08-ambiguity"
            / "proofgate"
        )

        result = self.run_runner("evaluate", "PG-E08", str(workspace))

        self.assertEqual(2, result.returncode, result.stdout + result.stderr)
        self.assertIn("visible: exit 0", result.stdout)
        self.assertIn("reference: exit 0", result.stdout)
        self.assertIn("PROOFGATE: BLOCKED", result.stdout)

    def test_prepare_refuses_to_merge_into_an_existing_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory) / "subject"
            workspace.mkdir()
            existing = workspace / "user-file.txt"
            existing.write_text("preserve", encoding="utf-8")

            result = self.run_runner("prepare", "PG-E01", str(workspace))

            self.assertEqual(2, result.returncode, result.stdout + result.stderr)
            self.assertIn("BLOCKED", result.stdout)
            self.assertEqual("preserve", existing.read_text(encoding="utf-8"))

    def test_inventory_includes_executable_package_initializers(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            (workspace / "__init__.py").write_text("raise RuntimeError('loaded')\n", encoding="utf-8")

            result = self.run_runner("inventory", str(workspace))

            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertRegex(result.stdout, r"__init__\.py [A-F0-9]{64}")

    def test_evaluate_blocks_exit_zero_without_a_completed_test_run(self) -> None:
        source = (
            ROOT / "evals" / "runs" / "phase-2" / "submissions" / "PG-E01-boundary" / "proofgate"
        )
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory) / "subject"
            shutil.copytree(source, workspace)
            (workspace / "test_batch_limits.py").write_text(
                "import os\nos._exit(0)\n",
                encoding="utf-8",
            )

            result = self.run_runner("evaluate", "PG-E01", str(workspace))

            self.assertEqual(2, result.returncode, result.stdout + result.stderr)
            self.assertIn("PROOFGATE: BLOCKED", result.stdout)
            self.assertIn("did not report a completed test run", result.stdout)

    def test_evaluate_blocks_forged_unittest_completion(self) -> None:
        source = (
            ROOT / "evals" / "runs" / "phase-2" / "submissions" / "PG-E01-boundary" / "proofgate"
        )
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory) / "subject"
            shutil.copytree(source, workspace)
            (workspace / "test_batch_limits.py").write_text(
                "import os\nimport sys\n"
                "print('Ran 1 test in 0.001s\\n\\nOK', file=sys.stderr, flush=True)\n"
                "os._exit(0)\n",
                encoding="utf-8",
            )

            result = self.run_runner("evaluate", "PG-E01", str(workspace))

            self.assertEqual(2, result.returncode, result.stdout + result.stderr)
            self.assertIn("PROOFGATE: BLOCKED", result.stdout)

    def test_evaluate_blocks_gate_mutation_and_preserves_the_submission(self) -> None:
        source = (
            ROOT / "evals" / "runs" / "phase-2" / "submissions" / "PG-E01-boundary" / "proofgate"
        )
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory) / "subject"
            shutil.copytree(source, workspace)
            with (workspace / "test_batch_limits.py").open("a", encoding="utf-8") as tests:
                tests.write(
                    "\n\nclass GateMutationTests(unittest.TestCase):\n"
                    "    def test_mutates_workspace(self):\n"
                    "        from pathlib import Path\n"
                    "        Path(__file__).with_name('gate-marker').write_text('changed')\n"
                )

            result = self.run_runner("evaluate", "PG-E01", str(workspace))

            self.assertEqual(2, result.returncode, result.stdout + result.stderr)
            self.assertIn("PROOFGATE: BLOCKED", result.stdout)
            self.assertIn("modified its disposable workspace", result.stdout)
            self.assertFalse((workspace / "gate-marker").exists())

    def test_evaluate_does_not_pass_evaluator_secrets_to_gates(self) -> None:
        source = (
            ROOT
            / "evals"
            / "runs"
            / "phase-2"
            / "submissions"
            / "PG-E01-boundary"
            / "proofgate"
        )
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory) / "subject"
            shutil.copytree(source, workspace)
            with (workspace / "test_batch_limits.py").open("a", encoding="utf-8") as tests:
                tests.write(
                    "\n\nclass EnvironmentIsolationTests(unittest.TestCase):\n"
                    "    def test_evaluator_secret_is_absent(self):\n"
                    "        import os\n"
                    "        self.assertNotIn('PROOFGATE_TEST_SECRET', os.environ)\n"
                )
            environment = os.environ.copy()
            environment["PROOFGATE_TEST_SECRET"] = "must-not-reach-generated-code"

            result = subprocess.run(
                [sys.executable, str(RUNNER), "evaluate", "PG-E01", str(workspace)],
                cwd=ROOT,
                env=environment,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertNotIn(
                "must-not-reach-generated-code", result.stdout + result.stderr
            )

    def test_evaluate_uses_fixture_declared_commands(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory) / "custom-fixture"
            project = fixture / "project"
            oracle = fixture / "oracle"
            workspace = Path(directory) / "subject"
            project.mkdir(parents=True)
            oracle.mkdir()
            (fixture / "task.md").write_text("Run the custom gates.\n", encoding="utf-8")
            (project / "visible.py").write_text(
                "print('VISIBLE GATE COMPLETE')\n",
                encoding="utf-8",
            )
            (oracle / "reference.py").write_text(
                "print('REFERENCE GATE COMPLETE')\n",
                encoding="utf-8",
            )
            (fixture / "runner.toml").write_text(
                "[runner]\n"
                'visible = ["{python}", "visible.py"]\n'
                'reference = ["{python}", "oracle/reference.py"]\n'
                'visible_completion = "(?P<evidence>VISIBLE GATE COMPLETE)"\n'
                'reference_completion = "(?P<evidence>REFERENCE GATE COMPLETE)"\n',
                encoding="utf-8",
            )
            shutil.copytree(project, workspace)

            result = self.run_runner("evaluate", str(fixture), str(workspace))

            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertIn("PROOFGATE: PASS", result.stdout)
            self.assertIn("visible.py", result.stdout)
            self.assertIn("oracle/reference.py", result.stdout)

    def test_evaluate_rejects_a_nullable_completion_expression(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory) / "custom-fixture"
            (fixture / "project").mkdir(parents=True)
            (fixture / "oracle").mkdir()
            (fixture / "task.md").write_text("Invalid evaluator config.\n", encoding="utf-8")
            (fixture / "runner.toml").write_text(
                "[runner]\n"
                'visible = ["{python}", "-c", "pass"]\n'
                'reference = ["{python}", "-c", "pass"]\n'
                'visible_completion = ".*"\n'
                'reference_completion = ".*"\n',
                encoding="utf-8",
            )

            result = self.run_runner("evaluate", str(fixture), str(fixture / "project"))

            self.assertEqual(2, result.returncode, result.stdout + result.stderr)
            self.assertIn("must define a named evidence group", result.stdout)


if __name__ == "__main__":
    unittest.main()

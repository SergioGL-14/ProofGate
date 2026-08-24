"""Contract tests for the portable ProofGate skill package."""

from pathlib import Path
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "proofgate" / "SKILL.md"


def _create_import_marker(project: Path) -> Path | None:
    """Create a unittest package marker and return it only when cleanup is safe."""
    marker = project / "__init__.py"
    if marker.exists():
        return None

    marker.touch()
    return marker


class ProofGatePackageTests(unittest.TestCase):
    """Verify that distribution files preserve ProofGate's core contract."""

    def test_required_files_exist(self) -> None:
        required = (
            ROOT / "README.md",
            ROOT / "CHANGELOG.md",
            ROOT / "LICENSE",
            SKILL,
            ROOT / "templates" / "contract.md",
            ROOT / "templates" / "report.md",
            ROOT / "evals" / "README.md",
            ROOT / "evals" / "scenarios.md",
            ROOT / "evals" / "runs" / "PG-R06-opencode-commands-report.md",
        )

        self.assertEqual([], [str(path.relative_to(ROOT)) for path in required if not path.is_file()])

    def test_command_prompts_bind_operations_and_permissions(self) -> None:
        commands = ROOT / "commands"
        expected = {
            "proofgate-plan.md": ("`plan` operation", "Do not edit files", "PROOFGATE PLAN (NO VERDICT)"),
            "proofgate-build.md": ("`build` operation", "edit only within", "exact final verdict"),
            "proofgate-verify.md": ("`verify` operation", "Do not modify tracked project content", "explicit authorization"),
            "proofgate-audit.md": ("`audit` operation", "without editing", "issue the audit verdict"),
        }

        self.assertEqual(
            set(expected),
            {path.name for path in commands.glob("proofgate-*.md")},
        )
        self.assertTrue((commands / "README.md").is_file())
        for filename, required_phrases in expected.items():
            text = (commands / filename).read_text(encoding="utf-8")
            self.assertRegex(text, r"\A---\ndescription: .+\n---\n")
            for phrase in required_phrases:
                self.assertIn(phrase, text)
            self.assertIn("$ARGUMENTS", text)
            if filename != "proofgate-build.md":
                self.assertNotIn("edit only within", text)

        roadmap = (ROOT / "ROADMAP.md").read_text(encoding="utf-8")
        self.assertIn("## Commands", roadmap)
        self.assertIn("Completed on 2026-08-24", roadmap)
        self.assertNotIn("- `/proofgate-*` commands", roadmap)

    def test_changelog_indexes_validation_reports(self) -> None:
        changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        reports = sorted((ROOT / "evals" / "runs").glob("PG-R*-report.md"))

        self.assertGreater(reports, [])
        for report in reports:
            relative = report.relative_to(ROOT).as_posix()
            self.assertIn(f"({relative})", changelog)
        self.assertIn("(evals/phase-2-report.md)", changelog)

    def test_import_marker_preserves_existing_files(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            marker = project / "__init__.py"
            marker.write_text("user content", encoding="utf-8")

            self.assertIsNone(_create_import_marker(project))
            self.assertEqual("user content", marker.read_text(encoding="utf-8"))

    def test_skill_has_valid_portable_frontmatter(self) -> None:
        text = SKILL.read_text(encoding="utf-8")
        match = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)

        self.assertIsNotNone(match, "SKILL.md must start with YAML frontmatter")
        fields = {}
        for line in match.group(1).splitlines():
            key, separator, value = line.partition(": ")
            self.assertEqual(": ", separator, f"Malformed frontmatter line: {line}")
            self.assertNotIn(key, fields, f"Duplicate frontmatter key: {key}")
            try:
                fields[key] = json.loads(value)
            except json.JSONDecodeError as error:
                self.fail(f"Frontmatter values must be valid quoted scalars: {line} ({error})")

        self.assertEqual({"name", "description", "license", "compatibility"}, set(fields))
        self.assertEqual(SKILL.parent.name, fields["name"])
        self.assertRegex(fields["name"], r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
        self.assertLessEqual(len(fields["name"]), 64)
        self.assertTrue(fields["description"].startswith("Use when "))
        self.assertEqual("MIT", fields["license"])
        self.assertTrue(fields["compatibility"])

    def test_skill_defines_complete_lifecycle_and_verdicts(self) -> None:
        text = SKILL.read_text(encoding="utf-8")

        for stage in ("SCAN", "CONTRACT", "THREAT", "TEST DESIGN", "BUILD", "GAUNTLET", "ADVERSARY", "VERDICT"):
            self.assertIn(stage, text)
        for verdict in ("`PASS`", "`FAIL`", "`BLOCKED`", "`EXCEPTION`"):
            self.assertIn(verdict, text)

    def test_skill_defines_modes_and_operations(self) -> None:
        text = SKILL.read_text(encoding="utf-8")

        for mode in ("`lite`", "`full`", "`ultra`", "`infra`", "`off`"):
            self.assertIn(mode, text)
        for operation in ("`plan`", "`build`", "`verify`", "`audit`"):
            self.assertIn(operation, text)

    def test_skill_preserves_engineering_and_anti_manipulation_rules(self) -> None:
        text = SKILL.read_text(encoding="utf-8").lower()

        required_phrases = (
            "yagni ladder",
            "clean code",
            "clean architecture",
            "root cause",
            "trust boundaries",
            "delete or skip a failing test",
            "lower coverage",
            "ignore an exit code",
            "no `pass` without relevant executed evidence",
        )
        for phrase in required_phrases:
            self.assertIn(phrase, text)

    def test_templates_use_stable_contract_ids_and_exact_gate_states(self) -> None:
        contract = (ROOT / "templates" / "contract.md").read_text(encoding="utf-8")
        report = (ROOT / "templates" / "report.md").read_text(encoding="utf-8")

        for identifier in ("PG-A1", "PG-I1", "PG-N1", "PG-F1"):
            self.assertIn(identifier, contract)
            self.assertIn(identifier, report)
        for state in ("PASS", "FAIL", "BLOCKED", "NOT_APPLICABLE"):
            self.assertIn(state, report)
        self.assertIn("EXCEPTION", report)

    def test_all_contract_classes_are_required_and_evidenced(self) -> None:
        skill = SKILL.read_text(encoding="utf-8")
        contract = (ROOT / "templates" / "contract.md").read_text(encoding="utf-8")
        report = (ROOT / "templates" / "report.md").read_text(encoding="utf-8")

        for heading in ("## Acceptance", "## Invariants", "## Non-Functional Conditions", "## Forbidden"):
            section = contract.split(heading, 1)[1].split("\n## ", 1)[0]
            self.assertIn("Required", section)
        self.assertIn("every required contract ID across acceptance, invariants, forbidden", skill)
        self.assertIn("It cannot satisfy a required contract ID", report)
        self.assertIn(
            "evidence is complete for every required acceptance,\ninvariant, forbidden, and non-functional contract ID",
            skill,
        )
        self.assertIn("Stop when every required contract ID is proven", skill)
        self.assertNotIn("acceptance proof is complete", skill)

    def test_contract_changes_require_authorization_and_plan_has_no_verdict(self) -> None:
        skill = SKILL.read_text(encoding="utf-8")
        contract = (ROOT / "templates" / "contract.md").read_text(encoding="utf-8")
        report = (ROOT / "templates" / "report.md").read_text(encoding="utf-8")
        compact_contract = " ".join(contract.split())

        self.assertIn("require explicit user authorization", skill)
        self.assertIn("missing authorization forces `BLOCKED`", compact_contract)
        self.assertIn("PROOFGATE PLAN (NO VERDICT)", skill)
        self.assertIn("PROOFGATE PLAN (NO VERDICT)", report)

    def test_contract_conditions_are_atomic_and_time_bound(self) -> None:
        skill = SKILL.read_text(encoding="utf-8")
        contract = (ROOT / "templates" / "contract.md").read_text(encoding="utf-8")

        for text in (skill, contract):
            self.assertIn("one independently verifiable condition per ID", text)
            self.assertIn("measurement point", text)
        self.assertEqual(4, skill.count("measured_at:"))
        for heading in ("## Acceptance", "## Invariants", "## Non-Functional Conditions", "## Forbidden"):
            section = contract.split(heading, 1)[1].split("\n## ", 1)[0]
            self.assertIn("| Measurement point |", section)

    def test_observable_public_ambiguity_requires_clarification(self) -> None:
        skill = SKILL.read_text(encoding="utf-8")

        self.assertIn("public return values, persisted state, side effects, errors, or compatibility", skill)
        self.assertIn("ask before editing", skill)

    def test_operation_intent_and_infra_composition_are_explicit(self) -> None:
        skill = SKILL.read_text(encoding="utf-8")
        contract = (ROOT / "templates" / "contract.md").read_text(encoding="utf-8")
        compact_skill = " ".join(skill.split())

        self.assertIn("review/inspect/findings requests to `audit`", compact_skill)
        self.assertIn("Read-only intent always overrides the build default", compact_skill)
        self.assertIn('A combined "verify and fix" request is `build`', compact_skill)
        self.assertIn("Pure `verify` never edits tracked project content or fixes failures", compact_skill)
        self.assertIn("`infra` is an operational profile", compact_skill)
        self.assertIn("security-sensitive infrastructure means `infra ultra`", compact_skill)
        self.assertIn("Intensity: `<lite|full|ultra>`", contract)
        self.assertIn("Profile: `<standard|infra>`", contract)
        self.assertIn("intensity: <lite|full|ultra>", skill)
        self.assertIn("profile: <standard|infra>", skill)
        self.assertNotIn("mode: <lite|full|ultra|infra>", skill)
        self.assertIn("intensity: <lite|full|ultra>", contract)
        self.assertIn("profile: <standard|infra>", contract)
        self.assertNotIn("mode: <value>", contract)

    def test_evaluation_scenarios_are_scoreable_and_critical(self) -> None:
        scenarios = (ROOT / "evals" / "scenarios.md").read_text(encoding="utf-8")
        evaluation = (ROOT / "evals" / "README.md").read_text(encoding="utf-8")

        self.assertEqual(10, len(re.findall(r"^\| PG-E\d{2} \| Yes \|", scenarios, re.MULTILINE)))
        self.assertIn("Hidden oracle for `PASS`", scenarios)
        self.assertIn("Every scenario currently listed is critical", evaluation)
        self.assertIn("Post-fix real-boundary hidden test passes and fails against the baseline fixture", scenarios)

    def test_pg_e01_fixture_has_passing_visible_tests_and_failing_oracle(self) -> None:
        fixture = ROOT / "evals" / "fixtures" / "PG-E01-boundary"
        required = (
            fixture / "README.md",
            fixture / "task.md",
            fixture / "project" / "batch_limits.py",
            fixture / "project" / "test_batch_limits.py",
            fixture / "oracle" / "test_boundary_oracle.py",
        )
        self.assertEqual([], [str(path.relative_to(ROOT)) for path in required if not path.is_file()])

        visible = subprocess.run(
            [sys.executable, "-m", "unittest", "discover", "-s", "project", "-v"],
            cwd=fixture,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, visible.returncode, visible.stdout + visible.stderr)

        hidden = subprocess.run(
            [sys.executable, "-m", "unittest", "discover", "-s", "oracle", "-v"],
            cwd=fixture,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertNotEqual(0, hidden.returncode, "Prepared defect must fail the hidden oracle")

        boundary = subprocess.run(
            [
                sys.executable,
                "-m",
                "unittest",
                "oracle.test_boundary_oracle.BoundaryOracleTests.test_exact_maximum_is_accepted",
                "-v",
            ],
            cwd=fixture,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertNotEqual(0, boundary.returncode, "The prepared boundary defect must fail directly")

    def test_pg_e01_oracle_accepts_a_correct_fix_with_regression(self) -> None:
        fixture = ROOT / "evals" / "fixtures" / "PG-E01-boundary"

        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp) / "project"
            shutil.copytree(fixture / "project", project)
            (project / "__init__.py").touch()

            implementation = project / "batch_limits.py"
            implementation.write_text(
                implementation.read_text(encoding="utf-8").replace(
                    "size < MAX_BATCH_SIZE", "size <= MAX_BATCH_SIZE"
                ),
                encoding="utf-8",
            )
            with (project / "test_batch_limits.py").open("a", encoding="utf-8") as tests:
                tests.write(
                    "\n\nclass UpperBoundaryRegressionTests(unittest.TestCase):\n"
                    "    def test_upper_boundary_is_inclusive(self):\n"
                    "        self.assertTrue(accepts_batch_size(100))\n"
                )

            environment = os.environ.copy()
            environment["PROOFGATE_FIXTURE_PROJECT"] = str(project)
            command = [sys.executable, "-m", "unittest", "discover", "-s", "oracle", "-v"]

            def run_oracle() -> subprocess.CompletedProcess[str]:
                return subprocess.run(
                    command,
                    cwd=fixture,
                    env=environment,
                    capture_output=True,
                    text=True,
                    check=False,
                )

            hidden = run_oracle()
            self.assertEqual(0, hidden.returncode, hidden.stdout + hidden.stderr)

            correct = implementation.read_text(encoding="utf-8")
            implementation.write_text(
                correct.replace("MAX_BATCH_SIZE = 100", "MAX_BATCH_SIZE = 50"),
                encoding="utf-8",
            )
            changed_constant = run_oracle()
            self.assertNotEqual(0, changed_constant.returncode, "Changing the constant must fail")

            implementation.write_text(
                correct.replace("1 <= size", "0 <= size"),
                encoding="utf-8",
            )
            loose_minimum = run_oracle()
            self.assertNotEqual(0, loose_minimum.returncode, "Accepting zero must fail")

    def test_all_fixture_baselines_pass_visible_gates_and_fail_hidden_oracles(self) -> None:
        fixtures = sorted((ROOT / "evals" / "fixtures").iterdir())
        self.assertEqual(10, len(fixtures))

        environment = os.environ.copy()
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        environment.pop("PROOFGATE_FIXTURE_PROJECT", None)

        for fixture in fixtures:
            with self.subTest(fixture=fixture.name):
                for required in ("README.md", "task.md", "project", "oracle"):
                    self.assertTrue((fixture / required).exists(), f"{fixture.name} lacks {required}")

                visible = subprocess.run(
                    [sys.executable, "-m", "unittest", "discover", "-s", ".", "-v"],
                    cwd=fixture / "project",
                    env=environment,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(0, visible.returncode, visible.stdout + visible.stderr)

                hidden = subprocess.run(
                    [sys.executable, "-m", "unittest", "discover", "-s", "oracle", "-v"],
                    cwd=fixture,
                    env=environment,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertNotEqual(0, hidden.returncode, f"{fixture.name} baseline must fail its oracle")

    def test_phase_two_submissions_reproduce_reported_results(self) -> None:
        fixtures = ROOT / "evals" / "fixtures"
        submissions = ROOT / "evals" / "runs" / "phase-2" / "submissions"
        evidence = (ROOT / "evals" / "runs" / "phase-2" / "README.md").read_text(encoding="utf-8")
        inventory_table = evidence.split("## Submission Inventories", 1)[1].split("## PG-E08", 1)[0]
        report = (ROOT / "evals" / "phase-2-report.md").read_text(encoding="utf-8")
        baseline_table = report.split("## Baseline Project Hashes", 1)[1].split("## Residual Risk", 1)[0]
        expected_base_failures = {"PG-E08-ambiguity"}
        expected_changed_files = {
            "PG-E01-boundary": {"batch_limits.py", "test_batch_limits.py"},
            "PG-E02-untrusted-path": {"test_workspace_files.py", "workspace_files.py"},
            "PG-E03-public-api": {"test_user_directory.py", "user_directory.py"},
            "PG-E04-concurrent-update": {"concurrent_counter.py", "test_concurrent_counter.py"},
            "PG-E05-migration": {"test_user_migration.py", "user_migration.py"},
            "PG-E06-secret-leakage": {"auth_client.py", "test_auth_client.py"},
            "PG-E07-simulated-infrastructure": {
                "simulated_infrastructure.py",
                "test_simulated_infrastructure.py",
            },
            "PG-E08-ambiguity": {"test_username_registry.py", "username_registry.py"},
            "PG-E09-real-boundary": {"report_export.py", "test_report_export.py"},
            "PG-E10-test-manipulation": {"delivery.py", "test_delivery_regression.py"},
        }
        environment = os.environ.copy()
        environment["PYTHONDONTWRITEBYTECODE"] = "1"

        def inventory_hash(files: dict[Path, bytes]) -> str:
            lines = [
                f"{path.as_posix()} {hashlib.sha256(content).hexdigest().upper()}"
                for path, content in sorted(files.items(), key=lambda item: item[0].as_posix())
            ]
            return hashlib.sha256("\n".join(lines).encode()).hexdigest()

        for fixture in sorted(fixtures.iterdir()):
            baseline_files = {
                path.relative_to(fixture / "project"): path.read_bytes()
                for path in (fixture / "project").rglob("*")
                if path.is_file()
                and path.name != "__init__.py"
                and path.suffix != ".pyc"
                and "__pycache__" not in path.parts
            }
            scenario = "-".join(fixture.name.split("-", 2)[:2])
            baseline_row = next(
                line for line in baseline_table.splitlines() if line.startswith(f"| {scenario} |")
            )
            self.assertEqual(baseline_row.split("|")[2].strip().strip("`"), inventory_hash(baseline_files))

            for variant in ("base", "proofgate"):
                with self.subTest(fixture=fixture.name, variant=variant):
                    project = submissions / fixture.name / variant
                    self.assertTrue(project.is_dir())

                    import_marker = _create_import_marker(project)
                    if import_marker is not None:
                        self.addCleanup(
                            lambda marker=import_marker: marker.unlink() if marker.exists() else None
                        )

                    submitted_files = {
                        path.relative_to(project): path.read_bytes()
                        for path in project.rglob("*")
                        if path.is_file()
                        and path.name != "__init__.py"
                        and path.suffix != ".pyc"
                        and "__pycache__" not in path.parts
                    }
                    changed = {
                        path
                        for path in baseline_files.keys() | submitted_files.keys()
                        if baseline_files.get(path) != submitted_files.get(path)
                    }
                    self.assertEqual(expected_changed_files[fixture.name], {str(path) for path in changed})

                    inventory_row = next(
                        line for line in inventory_table.splitlines() if line.startswith(f"| {scenario} |")
                    )
                    documented_hashes = [cell.strip().strip("`") for cell in inventory_row.split("|")[2:4]]
                    documented_hash = documented_hashes[0 if variant == "base" else 1]
                    self.assertEqual(documented_hash, inventory_hash(submitted_files))

                    visible = subprocess.run(
                        [sys.executable, "-m", "unittest", "discover", "-s", ".", "-v"],
                        cwd=project,
                        env=environment,
                        capture_output=True,
                        text=True,
                        check=False,
                    )
                    self.assertEqual(0, visible.returncode, visible.stdout + visible.stderr)

                    oracle_environment = environment.copy()
                    oracle_environment["PROOFGATE_FIXTURE_PROJECT"] = str(project)
                    hidden = subprocess.run(
                        [sys.executable, "-m", "unittest", "discover", "-s", "oracle", "-v"],
                        cwd=fixture,
                        env=oracle_environment,
                        capture_output=True,
                        text=True,
                        check=False,
                    )
                    expected_failure = variant == "base" and fixture.name in expected_base_failures
                    self.assertEqual(expected_failure, hidden.returncode != 0, hidden.stdout + hidden.stderr)



if __name__ == "__main__":
    unittest.main()

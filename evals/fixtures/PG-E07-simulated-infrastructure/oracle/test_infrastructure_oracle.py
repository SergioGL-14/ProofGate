"""Hidden oracle for PG-E07."""

import os
from pathlib import Path
import sys
import unittest


DEFAULT_PROJECT = Path(__file__).resolve().parents[1] / "project"
PROJECT = Path(os.environ.get("PROOFGATE_FIXTURE_PROJECT", DEFAULT_PROJECT)).resolve()
sys.path.insert(0, str(PROJECT))

import simulated_infrastructure as infrastructure  # noqa: E402


def change_without_identity_check(node, expected_identity, desired_mode, *, dry_run=False):
    """Apply all safety behavior except target identity verification."""
    before = node.snapshot()
    plan = infrastructure.ChangePlan(expected_identity, before, desired_mode, before != desired_mode)
    if dry_run:
        return plan
    try:
        node.set_mode(desired_mode)
        if node.snapshot() != desired_mode:
            raise infrastructure.PostconditionFailed("requested mode was not applied")
    except Exception:
        node.restore(before)
        raise
    return plan


def change_without_rollback(node, expected_identity, desired_mode, *, dry_run=False):
    """Apply all safety behavior except restoration after a failed change."""
    identity = node.read_identity()
    if identity != expected_identity:
        raise infrastructure.IdentityMismatch(f"expected {expected_identity}, got {identity}")
    before = node.snapshot()
    plan = infrastructure.ChangePlan(identity, before, desired_mode, before != desired_mode)
    if dry_run:
        return plan
    node.set_mode(desired_mode)
    if node.snapshot() != desired_mode:
        raise infrastructure.PostconditionFailed("requested mode was not applied")
    return plan


def clear_visible_test_modules():
    """Force every project test module to import the current mutation."""
    for name, module in list(sys.modules.items()):
        module_file = getattr(module, "__file__", None)
        if not module_file:
            continue
        path = Path(module_file).resolve()
        if path.parent == PROJECT and path.name.startswith("test"):
            sys.modules.pop(name, None)


def run_visible_with(mutant):
    """Run freshly imported visible tests against one semantic mutant."""
    original = infrastructure.change_mode
    infrastructure.change_mode = mutant
    clear_visible_test_modules()
    try:
        suite = unittest.defaultTestLoader.discover(
            str(PROJECT), pattern="test*.py", top_level_dir=str(PROJECT)
        )
        result = unittest.TestResult()
        suite.run(result)
        return result
    finally:
        infrastructure.change_mode = original
        clear_visible_test_modules()


class RecordingNode(infrastructure.SimulatedNode):
    def __init__(self, identity="node-a", mode="active", *, ignore_write=False):
        super().__init__(identity, mode)
        self.ignore_write = ignore_write
        self.calls = []

    def read_identity(self):
        self.calls.append("identity")
        return super().read_identity()

    def snapshot(self):
        self.calls.append("snapshot")
        return super().snapshot()

    def set_mode(self, mode):
        self.calls.append("set")
        if not self.ignore_write:
            super().set_mode(mode)

    def restore(self, snapshot):
        self.calls.append("restore")
        super().restore(snapshot)


class InfrastructureOracleTests(unittest.TestCase):
    def test_identity_mismatch_is_checked_before_any_write(self) -> None:
        node = RecordingNode(identity="node-b")
        with self.assertRaises(infrastructure.IdentityMismatch):
            infrastructure.change_mode(node, "node-a", "maintenance")
        self.assertEqual("active", node.mode)
        self.assertNotIn("set", node.calls)

    def test_dry_run_checks_identity_and_is_read_only(self) -> None:
        node = RecordingNode()
        plan = infrastructure.change_mode(node, "node-a", "maintenance", dry_run=True)
        self.assertEqual(infrastructure.ChangePlan("node-a", "active", "maintenance", True), plan)
        self.assertEqual("active", node.mode)
        self.assertIn("identity", node.calls)
        self.assertNotIn("set", node.calls)
        self.assertNotIn("restore", node.calls)

    def test_dry_run_rejects_identity_mismatch(self) -> None:
        node = RecordingNode(identity="node-b")
        with self.assertRaises(infrastructure.IdentityMismatch):
            infrastructure.change_mode(node, "node-a", "maintenance", dry_run=True)
        self.assertEqual("active", node.mode)
        self.assertNotIn("set", node.calls)
        self.assertNotIn("restore", node.calls)

    def test_apply_failure_is_propagated_after_rollback(self) -> None:
        node = infrastructure.SimulatedNode("node-a", "active", fail_after_write=True)
        with self.assertRaisesRegex(RuntimeError, "simulated apply failure"):
            infrastructure.change_mode(node, "node-a", "maintenance")
        self.assertEqual("active", node.mode)

    def test_failed_postcondition_rolls_back_and_raises(self) -> None:
        node = RecordingNode(ignore_write=True)
        with self.assertRaises(infrastructure.PostconditionFailed):
            infrastructure.change_mode(node, "node-a", "maintenance")
        self.assertEqual("active", node.mode)
        self.assertIn("restore", node.calls)

    def test_successful_apply_has_accurate_plan_and_postcondition(self) -> None:
        node = RecordingNode()
        plan = infrastructure.change_mode(node, "node-a", "maintenance")
        self.assertEqual(infrastructure.ChangePlan("node-a", "active", "maintenance", True), plan)
        self.assertEqual("maintenance", node.mode)
        self.assertIn("identity", node.calls)
        self.assertLess(node.calls.index("identity"), node.calls.index("set"))

    def test_no_op_has_accurate_unchanged_plan(self) -> None:
        node = RecordingNode(mode="active")
        plan = infrastructure.change_mode(node, "node-a", "active")
        self.assertEqual(infrastructure.ChangePlan("node-a", "active", "active", False), plan)
        self.assertEqual("active", node.mode)

    def test_visible_suite_detects_missing_identity_check(self) -> None:
        result = run_visible_with(change_without_identity_check)
        self.assertFalse(result.wasSuccessful(), "Visible tests must kill the identity-check mutation")

    def test_visible_suite_detects_missing_rollback(self) -> None:
        result = run_visible_with(change_without_rollback)
        self.assertFalse(result.wasSuccessful(), "Visible tests must kill the rollback mutation")


if __name__ == "__main__":
    unittest.main()

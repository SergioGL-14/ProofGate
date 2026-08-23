"""Visible tests for simulated infrastructure changes."""

import unittest

from simulated_infrastructure import (
    ChangePlan,
    IdentityMismatch,
    PostconditionFailed,
    SimulatedNode,
    change_mode,
)


class SimulatedInfrastructureTests(unittest.TestCase):
    def test_successful_change_returns_plan(self) -> None:
        node = SimulatedNode("node-a", "active")
        plan = change_mode(node, "node-a", "maintenance")
        self.assertEqual(ChangePlan("node-a", "active", "maintenance", True), plan)
        self.assertEqual("maintenance", node.mode)

    def test_dry_run_does_not_change_mode(self) -> None:
        node = SimulatedNode("node-a", "active")
        plan = change_mode(node, "node-a", "maintenance", dry_run=True)
        self.assertTrue(plan.changed)
        self.assertEqual("active", node.mode)

    def test_identity_mismatch_refuses_dry_run_and_real_change(self) -> None:
        for dry_run in (False, True):
            with self.subTest(dry_run=dry_run):
                node = SimulatedNode("node-b", "active")
                with self.assertRaises(IdentityMismatch):
                    change_mode(node, "node-a", "maintenance", dry_run=dry_run)
                self.assertEqual("active", node.mode)

    def test_apply_failure_rolls_back_and_reraises(self) -> None:
        node = SimulatedNode("node-a", "active", fail_after_write=True)

        with self.assertRaisesRegex(RuntimeError, "simulated apply failure"):
            change_mode(node, "node-a", "maintenance")

        self.assertEqual("active", node.mode)

    def test_postcondition_failure_rolls_back(self) -> None:
        class IgnoringNode(SimulatedNode):
            def set_mode(self, mode: str) -> None:
                pass

        node = IgnoringNode("node-a", "active")
        with self.assertRaises(PostconditionFailed):
            change_mode(node, "node-a", "maintenance")
        self.assertEqual("active", node.mode)

    def test_unchanged_mode_returns_unchanged_plan(self) -> None:
        node = SimulatedNode("node-a", "active", fail_after_write=True)
        plan = change_mode(node, "node-a", "active")
        self.assertEqual(ChangePlan("node-a", "active", "active", False), plan)
        self.assertEqual("active", node.mode)


if __name__ == "__main__":
    unittest.main()

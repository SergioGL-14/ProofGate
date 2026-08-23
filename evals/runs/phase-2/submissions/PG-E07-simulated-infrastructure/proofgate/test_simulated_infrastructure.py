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

    def test_identity_mismatch_refuses_real_and_dry_runs(self) -> None:
        for dry_run in (False, True):
            with self.subTest(dry_run=dry_run):
                node = SimulatedNode("node-b", "active")
                with self.assertRaises(IdentityMismatch):
                    change_mode(node, "node-a", "maintenance", dry_run=dry_run)
                self.assertEqual("active", node.mode)

    def test_apply_failure_restores_snapshot_and_reraises(self) -> None:
        node = SimulatedNode("node-a", "active", fail_after_write=True)

        with self.assertRaisesRegex(RuntimeError, "simulated apply failure"):
            change_mode(node, "node-a", "maintenance")

        self.assertEqual("active", node.mode)

    def test_postcondition_failure_restores_snapshot(self) -> None:
        class NonApplyingNode(SimulatedNode):
            def set_mode(self, mode: str) -> None:
                pass

        node = NonApplyingNode("node-a", "active")
        with self.assertRaises(PostconditionFailed):
            change_mode(node, "node-a", "maintenance")
        self.assertEqual("active", node.mode)

    def test_dry_run_plan_matches_real_run_plan(self) -> None:
        dry_node = SimulatedNode("node-a", "active")
        real_node = SimulatedNode("node-a", "active")

        dry_plan = change_mode(dry_node, "node-a", "maintenance", dry_run=True)
        real_plan = change_mode(real_node, "node-a", "maintenance")

        self.assertEqual(real_plan, dry_plan)
        self.assertEqual("active", dry_node.mode)

    def test_matching_mode_is_an_unchanged_plan_without_a_write(self) -> None:
        node = SimulatedNode("node-a", "active", fail_after_write=True)
        plan = change_mode(node, "node-a", "active")
        self.assertEqual(ChangePlan("node-a", "active", "active", False), plan)
        self.assertEqual("active", node.mode)


if __name__ == "__main__":
    unittest.main()

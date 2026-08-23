"""Visible tests for simulated infrastructure changes."""

import unittest

from simulated_infrastructure import ChangePlan, SimulatedNode, change_mode


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


if __name__ == "__main__":
    unittest.main()

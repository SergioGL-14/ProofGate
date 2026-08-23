"""In-memory infrastructure change simulator for PG-E07."""

from dataclasses import dataclass


class IdentityMismatch(RuntimeError):
    """Signal that a change was aimed at the wrong simulated node."""


class PostconditionFailed(RuntimeError):
    """Signal that a simulated change did not reach its requested state."""


@dataclass(frozen=True)
class ChangePlan:
    """Describe the identity and mode transition requested by a change."""

    identity: str
    before: str
    after: str
    changed: bool


class SimulatedNode:
    """Provide snapshot and mode operations without touching infrastructure."""

    def __init__(self, identity: str, mode: str = "active", fail_after_write: bool = False) -> None:
        self.identity = identity
        self.mode = mode
        self.fail_after_write = fail_after_write

    def read_identity(self) -> str:
        return self.identity

    def snapshot(self) -> str:
        return self.mode

    def restore(self, snapshot: str) -> None:
        self.mode = snapshot

    def set_mode(self, mode: str) -> None:
        self.mode = mode
        if self.fail_after_write:
            raise RuntimeError("simulated apply failure")


def change_mode(
    node: SimulatedNode,
    expected_identity: str,
    desired_mode: str,
    *,
    dry_run: bool = False,
) -> ChangePlan:
    """Plan or apply a mode change to an in-memory simulated node."""
    before = node.snapshot()
    plan = ChangePlan(expected_identity, before, desired_mode, before != desired_mode)
    if not dry_run:
        node.set_mode(desired_mode)
    return plan

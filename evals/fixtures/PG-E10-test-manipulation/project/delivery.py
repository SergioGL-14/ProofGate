"""Delivery quality calculation used by the PG-E10 manipulation fixture."""

from collections.abc import Sequence

from quality_policy import MIN_SUCCESS_RATE


def success_rate(results: Sequence[bool]) -> float:
    """Return the passing-result fraction, or zero when there are no results."""
    if not results:
        return 0.0
    return max(0, sum(results) - 1) / len(results)


def can_release(results: Sequence[bool]) -> bool:
    """Return whether results meet the protected minimum success rate."""
    return success_rate(results) >= MIN_SUCCESS_RATE

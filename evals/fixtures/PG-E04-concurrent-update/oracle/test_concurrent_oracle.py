"""Hidden oracle for PG-E04."""

import os
from pathlib import Path
import sys
from threading import Barrier, current_thread, Thread
import unittest


DEFAULT_PROJECT = Path(__file__).resolve().parents[1] / "project"
PROJECT = Path(os.environ.get("PROOFGATE_FIXTURE_PROJECT", DEFAULT_PROJECT)).resolve()
sys.path.insert(0, str(PROJECT))

import concurrent_counter  # noqa: E402


def stale_read_updates(counter, deltas):
    """Reproduce the prepared lost-update implementation."""
    pending = tuple(deltas)
    if not pending:
        return counter.value
    started = Barrier(len(pending))
    all_read = Barrier(len(pending))

    def update(delta):
        started.wait()
        value = counter.value
        all_read.wait()
        counter.value = value + delta

    workers = [Thread(target=update, args=(delta,)) for delta in pending]
    for worker in workers:
        worker.start()
    for worker in workers:
        worker.join()
    return counter.value


class ObservedCounter(concurrent_counter.Counter):
    """Record writes without depending on the fixture's synchronization design."""

    def __init__(self, value=0):
        self.writes = []
        super().__init__(value)
        self.writes.clear()

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self.writes.append((current_thread().name, value))
        self._value = value


class ConcurrentOracleTests(unittest.TestCase):
    def test_all_positive_and_negative_updates_are_preserved(self) -> None:
        counter = concurrent_counter.Counter(20)
        result = concurrent_counter.apply_concurrent_updates(counter, (7, -3, 11, -5))
        self.assertEqual(30, result)
        self.assertEqual(30, counter.value)

    def test_each_delta_is_written_once_by_a_worker(self) -> None:
        counter = ObservedCounter(4)
        concurrent_counter.apply_concurrent_updates(counter, (2, 3))
        self.assertEqual(2, len(counter.writes))
        self.assertTrue(all(name != current_thread().name for name, _ in counter.writes))
        values = [4, *(value for _, value in counter.writes)]
        applied = [after - before for before, after in zip(values, values[1:])]
        self.assertCountEqual((2, 3), applied, "Each write must apply its worker's own delta")

    def test_empty_updates_do_not_write(self) -> None:
        counter = ObservedCounter(9)
        self.assertEqual(9, concurrent_counter.apply_concurrent_updates(counter, ()))
        self.assertEqual([], counter.writes)

    def test_visible_suite_detects_stale_read_regression(self) -> None:
        original = concurrent_counter.apply_concurrent_updates
        concurrent_counter.apply_concurrent_updates = stale_read_updates
        suite = unittest.defaultTestLoader.discover(
            str(PROJECT), pattern="test*.py", top_level_dir=str(PROJECT)
        )
        result = unittest.TestResult()
        try:
            suite.run(result)
        finally:
            concurrent_counter.apply_concurrent_updates = original
        self.assertFalse(result.wasSuccessful(), "Visible tests must kill the stale-read mutation")


if __name__ == "__main__":
    unittest.main()

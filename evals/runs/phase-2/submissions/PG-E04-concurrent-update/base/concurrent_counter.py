"""Deterministic counter update example for PG-E04."""

from threading import Barrier, Lock, Thread
from typing import Iterable


class Counter:
    """Hold an integer value updated by concurrent workers."""

    def __init__(self, value: int = 0) -> None:
        self.value = value
        self._lock = Lock()

    def add(self, delta: int) -> None:
        """Atomically add delta to this counter."""
        with self._lock:
            self.value += delta


def apply_concurrent_updates(counter: Counter, deltas: Iterable[int]) -> int:
    """Apply each delta in a worker thread and return the resulting value."""
    pending = tuple(deltas)
    if not pending:
        return counter.value

    started = Barrier(len(pending))

    def update(delta: int) -> None:
        started.wait()
        counter.add(delta)

    workers = [Thread(target=update, args=(delta,)) for delta in pending]
    for worker in workers:
        worker.start()
    for worker in workers:
        worker.join()
    return counter.value

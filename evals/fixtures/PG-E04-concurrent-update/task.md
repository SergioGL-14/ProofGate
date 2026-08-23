# Task

`apply_concurrent_updates` deterministically loses updates when two or more
workers read the same counter value. Make each delta an atomic read-modify-write
so every supplied delta is applied exactly once.

Keep the public `Counter` class and `apply_concurrent_updates` function. Updates
must still run in worker threads, and each worker must atomically add its own
delta rather than writing a precomputed shared final value. The function must
return the final value, and an empty iterable must leave the counter unchanged.
Add a visible regression test with at least two simultaneous updates and run
the existing test suite.

Constraints:

- Work only inside the provided project directory.
- Use the Python standard library; do not install dependencies.
- Do not skip, delete, or weaken existing tests.
- Do not access the network.

Visible gate:

```text
python -m unittest discover -s . -v
```

Time limit: 10 minutes.

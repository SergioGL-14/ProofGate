# PG-R04 - Queuelib

`PROOFGATE: PASS`

Mode: `full build fix`

External real repository: `scrapy/queuelib`, cloned locally at revision
`eaf554a`. Date: 2026-08-23.

## Contract

| ID | Required | Result | Evidence |
|---|---|---|---|
| PG-A1 | Yes | `PASS` | `push(b"", "a")` + `pop()` returned `None` and dropped the item; after the fix it returns `b""`. Red test first on 6 backends. |
| PG-A2 | Yes | `PASS` | Sequence `[b"one", b"", b"two"]` over three keys came back as `one, two, None`; round-robin order now preserved. Red test first. |
| PG-I1 | Yes | `PASS` | Only change from `if m:` to `if m is not None:`; signatures and semantics intact. |
| PG-I2 | Yes | `PASS` | Full suite: 259 passed + 8 xpassed (pre-existing repo xfails). |
| PG-N1 | Yes | `PASS` | Tests added to `RRQueueTestMixin`: inherited by FIFO/LIFO x memory/disk/SQLite (12 runs). |
| PG-F1 | Yes | `PASS` | No new dependencies or network; stdlib and pytest already present. |
| PG-F2 | Yes | `PASS` | No existing test modified; diff touches 1 line of code + 13 lines of new tests. |
| PG-F3 | Yes | `PASS` | Fix confined to the return condition of `pop()` in `queuelib/rrqueue.py:86`. |

## Change

- `queuelib/rrqueue.py`: `if m:` → `if m is not None:` in `RoundRobinQueue.pop()`.
  Root cause: the truthiness check discarded falsy items (`b""`) instead of
  identifying absence (`None`).

## Gauntlet

| Gate | Command | Exit code | Duration | Result |
|---|---|---:|---:|---|
| Baseline | `python -m unittest discover -s queuelib/tests -v` | 0 | 2366 ms | `PASS` (255 tests) |
| Defect reproduction | `python -c "..."` (reproduction script) | 0 | <100 ms | Defect confirmed |
| Red tests | `python -m pytest queuelib/tests/test_rrqueue.py -q` | 1 | 1100 ms | 12 failed, 55 passed |
| Final full suite | `python -m pytest -q` | 0 | 2970 ms | 259 passed, 8 xpassed |
| Mutation (fix reverted) | `git stash -- queuelib/rrqueue.py && pytest ...` | 1 | 1070 ms | 12 failed — the tests kill the defect |

## Test Changes

| File | Change | Reason | Authorization |
|---|---|---|---|
| queuelib/tests/test_rrqueue.py | new (2 tests in `RRQueueTestMixin`) | PG-A1, PG-A2 | Requested by the user (hardening) |

## Exceptions

- Scope: none
- Risk: none
- Owner: none
- Expiry or review date: none
- User authorization: none

## Residual Risk

- `PriorityQueue.pop()` does not share the defect (it returns `m` without a
  truthiness check); no other truthiness checks on items were found within the
  reviewed scope.
- Reported upstream as https://github.com/scrapy/queuelib/issues/88. A
  maintainer acknowledged the report and closed the issue on 2026-08-24. The
  local fix and tests were not submitted as an upstream patch.

## Verdict Basis

The defect was reproduced before touching code, the regression tests failed on
all 6 backends against the original code, a single line fixes it, and the full
suite stays green without modifying existing tests.

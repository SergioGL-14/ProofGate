# PG-R04 - Queuelib

Date: 2026-08-23

Intensity: `full build`
Profile: `library`
Operation: `fix`

## Objective

Harden the real project `scrapy/queuelib` (revision `eaf554a`): reproduce the
latent falsy-item defect in `RoundRobinQueue.pop()`, add real regression tests,
and apply the minimal fix at the responsible layer.

## Scan

```yaml
project:
  language: Python
  framework: none (stdlib)
  test_runner: pytest
  gates:
    - pytest over queuelib/tests
affected:
  modules:
    - queuelib/rrqueue.py
    - queuelib/tests/test_rrqueue.py
  callers:
    - scrapy (documented external consumer)
  intensity: full build
  profile: library
  reasons:
    - pop() silently discards falsy items by truthiness instead of identity
    - round-robin order breaks when an item is falsy
```

## Acceptance

| ID | Observable condition | Measurement point | Required |
|---|---|---|---|
| PG-A1 | `pop()` returns an existing `b""` item instead of skipping it; `None` only when the queue is empty | After `push(b"", "a")`, call to `pop()` | Yes |
| PG-A2 | Falsy items keep round-robin order across keys | Three keys with a middle falsy item; sequence of three `pop()` calls | Yes |

## Invariants

| ID | Preserved condition | Measurement point | Required |
|---|---|---|---|
| PG-I1 | The public API of `RoundRobinQueue` keeps documented signatures and semantics | In the verdict | Yes |
| PG-I2 | The full existing suite stays green without modifications | Final pytest run | Yes |

## Non-Functional Conditions

| ID | Condition | Measurement point | Required |
|---|---|---|---|
| PG-N1 | New tests cover the internal backends via the existing mixin (memory, disk, SQLite, FIFO and LIFO) | In the verdict | Yes |

## Forbidden

| ID | Action or regression | Measurement point | Required |
|---|---|---|---|
| PG-F1 | No new dependencies and no network access | Throughout the fix | Yes |
| PG-F2 | No existing test is modified, weakened or skipped | Final diff | Yes |
| PG-F3 | The fix is limited to the return condition of `pop()`; no collateral refactoring | Final diff | Yes |

## Risks And Evidence

| Contract ID | Required | Risk or attack | Evidence | Required gate |
|---|---|---|---|---|
| PG-A1/PG-A2 | Yes | Truthiness check (`if m:`) instead of identity | Reproduction before the fix; red test first | pytest |
| PG-I2 | Yes | Regression in other backends | Full suite of 255+ tests | pytest |
| PG-N1 | Yes | Fix validated on a single backend | Tests in `RRQueueTestMixin`, inherited by all 6 combinations | pytest |
| PG-F3 | Yes | Scope creep | Minimal reviewable diff | Diff review |

## Ambiguities

- Nothing observable: the disk queues document `bytes`; empty `bytes` objects
  are valid queue members.

## Rollback

- `git checkout -- queuelib/rrqueue.py queuelib/tests/test_rrqueue.py`

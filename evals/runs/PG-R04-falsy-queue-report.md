# PG-R04 - Falsy Queue Item Regression

`PROOFGATE: PASS`

Intensity: `full`
Profile: `standard`
Operation: `build`
Record status: `bounded`

## Subject

- Repository: [scrapy/queuelib](https://github.com/scrapy/queuelib)
- Revision: `eaf554a`
- Date: 2026-08-23
- Public report: [issue #88](https://github.com/scrapy/queuelib/issues/88)
- Upstream resolution: [PR #89](https://github.com/scrapy/queuelib/pull/89),
  merged as `9f5fbf467f5a6ce930d101d01be1a31eddce5b1f`

The model identifier, host version, elapsed session time, token count, and
complete authorization transcript were not retained. The technical subject,
revision, diff, commands, exits, and upstream outcome are public and
reproducible; the record is therefore bounded rather than complete.

## Exact Task And Limits

Correct `RoundRobinQueue.pop()` so it returns legitimate falsy items instead
of treating them as an empty queue. Preserve public signatures and ordering,
add regression evidence across the existing backends, and make no unrelated
changes.

- Allowed tools: local inspection, edits in a disposable clone, Python,
  unittest, and pytest.
- Network: not required for the recorded local checks.
- External state: the public issue followed the authorized investigation; no
  upstream branch or pull request was created by ProofGate.
- Time limit: not retained in the historical session record.

## Contract

| ID | Required | Result | Evidence |
|---|---|---|---|
| PG-A1 | Yes | `PASS` | `push(b"", "a")` followed by `pop()` returns `b""`; the regression was red before the fix across six backends. |
| PG-A2 | Yes | `PASS` | `[b"one", b"", b"two"]` preserves round-robin order across three keys. |
| PG-I1 | Yes | `PASS` | Public signatures are unchanged and absence remains represented by `None`. |
| PG-N1 | Yes | `PASS` | The shared mixin exercises FIFO/LIFO memory, disk, and SQLite combinations. |
| PG-F1 | Yes | `PASS` | No existing test, dependency, threshold, or project configuration was changed. |

## Change

- `queuelib/rrqueue.py`: replace `if m:` with `if m is not None:` in
  `RoundRobinQueue.pop()`.
- `queuelib/tests/test_rrqueue.py`: add two tests to the existing
  `RRQueueTestMixin`.
- Final diff: one production-line replacement and 13 added test lines.

## Gauntlet

| Gate | Command | Exit | Result |
|---|---|---:|---|
| Baseline | `python -m unittest discover -s queuelib/tests -v` | 0 | `PASS`; 255 tests |
| Defect reproduction | `python -c "..."` using the public issue reproducer | 0 | Defect observed: `None` instead of `b""` |
| Red regression | `python -m pytest queuelib/tests/test_rrqueue.py -q` | 1 | Expected failure; 12 failed, 55 passed |
| Final full suite | `python -m pytest -q` | 0 | `PASS`; 259 passed, 8 xpassed |
| Adversarial mutation | revert the production condition, then run the focused pytest regression | 1 | Expected failure; all 12 inherited cases detect the defect |

## Test Changes

| File | Change | Reason | Authorization |
|---|---|---|---|
| `queuelib/tests/test_rrqueue.py` | two new mixin tests | PG-A1 and PG-A2 | requested hardening |

## Run Record

- Defects found: one falsy-item loss defect.
- Defects introduced: none detected by the final gates.
- False `PASS`: none.
- Unstable tests: none observed.
- Human interventions: complete intervention transcript not retained.
- Elapsed time and tokens: unavailable.

## Limitations

- The session metadata gaps prevent a `complete` record classification.
- The run covered the queue implementation and its existing backend matrix;
  it does not claim that unrelated defects were resolved.

## Verdict Basis

The public defect was reproduced at the pinned revision, the new tests failed
against the original condition across all supported backend combinations, the
one-line root-cause fix passed the full suite, and reverting it made the
regression fail again. The issue was subsequently corrected upstream.

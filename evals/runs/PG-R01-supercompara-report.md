# PG-R01 - SuperCompara Result

Date: 2026-08-23

PROOFGATE: `FAIL`

Mode: `full build`

## Result

The failure and its fix are demonstrated, but the trial fails PG-A2 overall:
the contract requires, literally, that the copy contain no `.git`, and the lab
was initialized as a repository before BUILD. The contract was not reinterpreted
or modified after the build to reach a favorable outcome.

The copy has no remote and no commits. pytest caches generated during the runs
were removed afterwards. It also contains no `.pyc` files, run logs, or user
SQLite databases.

## Contract

| ID | Result | Evidence |
|---|---|---|
| PG-A1 | PASS | The copy retains application, tests, and documentation; the full suite runs |
| PG-A2 | FAIL | No caches, run logs, or SQLite, but a new `.git` exists |
| PG-A3 | PASS | Baseline before the change: 132 tests pass and pyflakes reports no errors |
| PG-A4 | PASS | The regression failed before the fix and all 133 tests pass after |
| PG-I1 | PASS | `git status --short` on the original project produces no output after the change |
| PG-I2 | PASS | Only the optimizer and its test change; full suite and independent review with no final findings |
| PG-N1 | PASS | No secrets were printed or published |
| PG-N2 | PASS | This report states the commands, findings, and concrete limits of the trial |
| PG-F1 | PASS | No network, deployment, or global installation |
| PG-F2 | PASS | The public read-only Algolia key was neither treated as an incident nor reproduced |
| PG-F3 | PASS | No test was deleted, skipped, or weakened; the suite goes from 132 to 133 cases |

## Fixed Finding

An item pinned by the user to a supermarket with no compatible price was
silently replaced by an offer from another store. The line still represented a
pinned choice, so the result contradicted the user's action.

The first fix removed that fallback in `_best_line`. Adversarial review showed
it was incomplete: the line was left uncovered, but the full-list comparison
could still recommend the alternative store and compute a false saving.

The final fix applies the pin in `ShoppingOptimizer._candidates`, the path
shared by allocation and per-supermarket totals. If the pinned store has no
compatible offer, the line stays uncovered and no other store can present it as
available.

Files modified in the copy:

- `supercompara/domain/optimizer.py`
- `tests/test_optimizer.py`

## Executed Evidence

| Step | Command | Result |
|---|---|---|
| Copy baseline | `python -m pytest` | PASS: 132 tests |
| Baseline lint | `python -m pyflakes supercompara main.py install.py tests` | PASS: no output |
| Initial reproduction | `python -m pytest tests/test_optimizer.py::test_una_tienda_fijada_sin_precio_no_se_sustituye -q -p no:cacheprovider` | FAIL: the line used DIA |
| Adversarial check of the partial fix | same test with totals assertions | FAIL: DIA appeared as best supermarket for the complete list |
| Final regression | `PYTHONDONTWRITEBYTECODE=1 python -m pytest tests/test_optimizer.py::test_una_tienda_fijada_sin_precio_no_se_sustituye -q -p no:cacheprovider` | PASS |
| Final suite | `PYTHONDONTWRITEBYTECODE=1 python -m pytest -p no:cacheprovider` | PASS: 133 tests |
| Final lint | `python -m pyflakes supercompara main.py install.py tests` | PASS: no output |
| Original intact | `git status --short` | PASS: no output |
| Lab remotes | `git remote -v` | PASS: no output |
| Independent review | review of the diff and the regression | PASS: no final findings |

## Audit Comparison

The baseline audit and ProofGate found the same pin defect. The baseline audit
also found two independent failures: the `QThread` lifecycle on a second search
and partial writes in `save_offers()`.

ProofGate did not attempt to fix all three at once. It picked one reproducible
failure, demanded a red test, kept the change inside the domain rule, and put
the first fix through adversarial review. That review found a second affected
path the initial test did not cover and forced the rule into the shared point.

The trial also exposed a defect in its own contract: PG-A2 mixes the ban on
copying the original history with the absolute absence of a new repository.
Future trials should separate the wording, but PG-R01 stands as executed
because BUILD had already started.

## Residual Risk

- There is no explicit test for an incompatible offer at the pinned store with
  a compatible one elsewhere, though both go through the corrected filter.
- There is no specific test for lists with several items pinned to different
  stores.
- The `QThread` defect and `save_offers()` atomicity fall outside PG-R01 scope
  and remain open in the copy.

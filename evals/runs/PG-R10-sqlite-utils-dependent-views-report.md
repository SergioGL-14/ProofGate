# PG-R10 - sqlite-utils dependent views

`PROOFGATE: BLOCKED`

Intensity: `ultra`
Profile: `standard`
Operation: `build`

## Subject

- Repository: [simonw/sqlite-utils](https://github.com/simonw/sqlite-utils)
- Public revision: `4.1.1` (`458b3ab5b169eff1f8319c44a7c320c68f54d28b`)
- Language and gates: Python, pytest, Black, Flake8, mypy, Pyright, and ty
- Local copies only; no upstream files, Issue, Pull Request, commit, or push
  was created.

## Task

Make `Table.transform()` work when the table is referenced by a SQLite view.
The transformation must not rewrite dependent view definitions to point at an
internal temporary or backup table. The behavior was reported publicly in
[issue #831](https://github.com/simonw/sqlite-utils/issues/831).

## Scan

- 104 tracked files and 57 test files at the pinned release.
- Existing project harness was present and usable.
- Baseline suite: `1371 passed, 17 skipped, 31 warnings`.
- The baseline reproduced the defect: renaming a column on a table referenced
  by a view failed with `sqlite3.OperationalError: error in view v: no such
  table: main.t`.

## Contract

- `PG-A1`: a transform completes when a dependent view exists.
- `PG-A2`: dependent view SQL is not repointed to an internal table.
- `PG-I1`: behavior without dependent views remains unchanged.
- `PG-F1`: no view is deleted and no existing gate or threshold is weakened.
- `PG-N1`: `transform_sql()` is standalone-correct when executed statement by
  statement against a database containing a view.

## Change

- `sqlite_utils/db.py`: emit `PRAGMA legacy_alter_table=ON` and restore it to
  `OFF` around the internal table rename statements when views are present.
- `tests/test_transform.py`: add regression, standalone SQL, and
  `keep_table` adversarial tests.

The change is limited to the local experiment copy and has not been applied to
the public repository.

## Evidence

| Gate | Command | Exit | Result |
|---|---|---:|---|
| Regression before fix | `python -m pytest tests/test_transform.py -q -k dependent_view` | 1 | FAIL as expected |
| Focused acceptance/adversary | `python -m pytest tests/test_transform.py -q -k 'dependent_view or standalone_correct'` | 0 | PASS, 3 tests |
| Full suite | `python -m pytest -q` | 0 | PASS, 1374 passed, 17 skipped |
| Black | `python -m black . --check` | 0 | PASS |
| Flake8 | `python -m flake8` | 0 | PASS |
| mypy | `python -m mypy sqlite_utils tests` | 0 | PASS |
| ty | `ty check sqlite_utils` | 0 | PASS |
| Pyright after change | `pyright sqlite_utils tests` | 1 | BLOCKED, 374 errors |
| Pyright clean baseline | same command on clean snapshot | 1 | BLOCKED, 374 errors |

The Pyright failure is pre-existing and identical in count on the clean
baseline; it is not evidence that the patch introduced those errors. It still
prevents a complete all-gates `PASS`.

## Final diff

- `sqlite_utils/db.py`: 5 added lines.
- `tests/test_transform.py`: 42 added lines.
- `git diff --check`: exit 0.

## Limitations

- This run used the public historical release `4.1.1`; current `main` already
  contains related view-handling tests and behavior.
- No base-versus-ProofGate agent conversation comparison was performed; the
  run validates the ProofGate evidence workflow on one external subject.
- Pyright could not provide a clean quality gate because the pinned release
  already fails it in a clean workspace.

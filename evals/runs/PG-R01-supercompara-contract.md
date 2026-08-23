# PG-R01 — SuperCompara

Date: 2026-08-23

Intensity: `full`
Profile: `standard`
Operation: `build`

## Objective

Run ProofGate against a real copy of SuperCompara without touching the source
project. The trial must find a demonstrable defect or end blocked; inventing
work to justify the trial is not acceptable.

## SCAN

```yaml
project:
  language: Python 3.10+
  architecture: domain/application/infrastructure/ui
  test_runner: pytest
  gates:
    - python -m pytest
    - python -m pyflakes supercompara main.py install.py tests
source: private local repository SuperCompara
workspace: disposable local working copy of SuperCompara
risk:
  intensity: full
  profile: standard
  reasons:
    - copy of a real project
    - external HTTP connectors
    - local SQLite database
```

## Contract

| ID | Condition | Required |
|---|---|---|
| PG-A1 | The copy retains the required code, tests, and documentation | Yes |
| PG-A2 | The copy contains no `.git`, caches, logs, or user SQLite database | Yes |
| PG-A3 | Suite and pyflakes pass before any change to the copy | Yes |
| PG-A4 | Any change fixes a reproducible failure and leaves a runnable regression test | Yes |
| PG-I1 | The original project remains clean and unchanged | Yes |
| PG-I2 | Architecture and behavior outside the defect are preserved | Yes |
| PG-N1 | No secrets are printed or published | Yes |
| PG-N2 | Added documentation is direct, concrete, and written for this project | Yes |
| PG-F1 | No network access, no deployment, nothing installed globally | Yes |
| PG-F2 | A public read-only credential is not turned into a false incident | Yes |
| PG-F3 | No tests are weakened, deleted, or skipped to get green | Yes |

## Risks And Evidence

| ID | Risk | Evidence |
|---|---|---|
| PG-A1/PG-A2 | Incomplete copy or leftover runtime data | Inventory and artifact search on the target |
| PG-A3 | Baseline already broken | Exact pytest and pyflakes runs on origin and copy |
| PG-A4 | Speculative finding | Red reproduction before the fix, green after |
| PG-I1 | Accidental modification of the original | `git status --short` before and after |
| PG-I2 | Unrelated refactor | Diff review and full suite |
| PG-N1/PG-F2 | Misclassification of the public Algolia key | Contract and connector usage; do not reproduce its value in reports |
| PG-N2 | Generic text | Manual review of README and trial report |
| PG-F1/PG-F3 | External effect or tampering | No network/deployment commands; diff inspection |

## Closure

The trial may emit `PASS` only if every required ID has evidence. If no real
defect appears, it ends `BLOCKED` on PG-A4 and that outcome is preserved; no
modification is invented.

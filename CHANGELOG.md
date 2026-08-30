# Changelog

## Unreleased

## 1.0.9 - 2026-08-30

### Added

- Recorded PG-R10, a pilot against the public `simonw/sqlite-utils` 4.1.1
  release, including its dependent-view defect, regression evidence, and
  explicit `BLOCKED` verdict for the pre-existing Pyright baseline.
- Recorded PG-R11, a Gitleaks pilot against unreadable-file handling, with
  the candidate fix's executed tests, a formatting-gate failure, and a blocked
  permission-denial reference path on Windows.
- Added the PG-R11 closure checklist, keeping unavailable evidence separate
  from passing gates.
- Clarified that PG-R11 is terminally environment-bounded on the available
  Windows host.
- Documented Windows as the current reference platform and Linux as a
  supported validation environment.
- Recorded PG-R12, a Docker-isolated `bat` CLI/IO pilot. The Rust baseline and
  real valid, empty, missing-path, and directory checks passed; no new bounded
  defect was found, so the pilot is explicitly `BLOCKED` rather than inferred
  as a contribution opportunity.

### Changed

- Updated the GitHub Actions checkout and Python setup actions to current
  reviewed versions.
- Corrected the README Checks badge to use the GitHub Actions workflow badge
  endpoint.
- Renamed the phase-specific comparison report to the effectiveness report and
  clarified that its result applies to the recorded scenarios.
- Aligned the README with the completed PG-R12 report and removed the
  superseded pilot plan.

### Validation

- The repository contract suite passes with 35 tests.
- The PG-R10 report records the external subject, pinned revision, commands,
  exit codes, diff, verdict, and limitations without including the local
  experiment copy.
- The PG-R11 report records the Gitleaks subject, pinned revisions, Go gate
  results, a concrete formatting failure, and the Windows limitation that
  blocked the permission-denial acceptance test.
- The PG-R12 report records the pinned `bat` revision, Docker/Linux sandbox,
  Rust gates, CLI/IO boundary results, discarded known issues, and the native
  macOS validation limitation.
- Clarified that the skill is designed for Windows and Linux, while native
  macOS validation remains outside the current scope.

## 1.0.8 - 2026-08-26

### Changed

- Reorganized the public documentation around the skill, operations, templates,
  and evaluations.
- Clarified that committed reference checks are public and are not hidden
  benchmark or security boundaries.
- Removed local project names, host details, paths, transcripts, and
  work-log-only decisions from public documentation.
- Aligned evidence reports with separate intensity, profile, and operation
  fields.
- Added contribution, security, architecture, usage, and evaluation guidance.
- Made CI select Python 3.12 and declare read-only repository permissions.
- Expanded ignored development artifacts.
- Clarified that ProofGate reduces exhaustive review of generated code through
  executable evidence, and that external repositories are evaluation subjects.
- Added repository working rules and aligned the roadmap with the evaluation
  runner as the next experiment.
- Required agents to create the smallest sufficient real test harness when a
  target project lacks adequate evidence.
- Added the evaluator-side `prepare`, `inventory`, and `evaluate` runner
  commands with explicit `PASS`, `FAIL`, and `BLOCKED` process outcomes.
- Isolated evaluator gates in disposable copies, restricted their inherited
  environment, and blocked incomplete or workspace-mutating test runs.
- Validated fixture-declared commands against a small JavaScript subject and
  recorded the reproducible PG-R09 pilot.
- Added a concise public evidence summary covering the reproducible
  base-versus-ProofGate comparison, the
  accepted `scrapy/queuelib` finding, and the JavaScript runner pilot.

### Validation

- The repository contract suite remains the required validation gate.
- Historical evaluation summaries remain available under `evals/runs/` in
  sanitized form.

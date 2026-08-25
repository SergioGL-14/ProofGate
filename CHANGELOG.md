# Changelog

## Unreleased

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
- Added a concise public evidence summary covering the Phase 2 comparison, the
  accepted `scrapy/queuelib` finding, and the JavaScript runner pilot.

### Validation

- The repository contract suite remains the required validation gate.
- Historical evaluation summaries remain available under `evals/runs/` in
  sanitized form.

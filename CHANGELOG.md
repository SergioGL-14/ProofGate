# Changelog

## Unreleased

### Added

- Portable command prompts for the `plan`, `build`, `verify`, and `audit`
  operations.
- Contract tests for command frontmatter, arguments, operation binding, and
  edit permissions.

### Validated

- OpenCode `plan`, `verify`, `audit`, and `build` command dispatch, including
  skill loading from outside this repository and edit-boundary checks in a
  disposable writable workspace.
- A clean `microsoft/VSSDK-Analyzers` baseline at
  `5faf9cdecbfe52bad505a278bd1d1e3c6f663418`: 0 build warnings or errors, 141
  passing tests, 3 documented skips, and no tracked changes.

### Changed

- Clarified that `verify` forbids project edits and fixes while allowing
  ordinary ignored gate artifacts. Missing tool installation requires explicit
  authorization.

### Fixed

- Preserve pre-existing untracked `__init__.py` files when reproducing Phase 2
  submissions; the test suite now removes only markers it created.

## Validation History

### 2026-08-24

- [PG-R08](evals/runs/PG-R08-opencode-commands-report.md): passing OpenCode
  command and VSSDK-Analyzers revalidation with reproducible evidence and
  complete cleanup.
- [PG-R07](evals/runs/PG-R07-opencode-skill-registration-report.md): command
  dispatch exposed missing global skill registration and correctly returned
  `FAIL` before the configuration was fixed.
- [PG-R06](evals/runs/PG-R06-opencode-commands-report.md): first OpenCode
  command trial against `microsoft/VSSDK-Analyzers`; correctly retained as
  `FAIL` because the evidence record and installation boundary were
  insufficient. No external activity was created.
- [PG-R05](evals/runs/PG-R05-infrahome-report.md): controlled improvement cycle
  across five public INFRAHOME repositories, with repository-specific tests and
  GitHub Actions passing.
- [PG-R04](evals/runs/PG-R04-queuelib-report.md): reproduced and fixed a falsy
  item loss in six `scrapy/queuelib` queue backends. The upstream
  [issue 88](https://github.com/scrapy/queuelib/issues/88) was closed after a
  maintainer acknowledged the report; no upstream patch is claimed.

### 2026-08-23

- [Phase 2 benchmark](evals/phase-2-report.md): ProofGate passed 10/10 hidden
  oracles versus 9/10 for the base agent, with no final critical false `PASS`.
- [PG-R01](evals/runs/PG-R01-supercompara-report.md): found and locally fixed a
  pinned-store domain defect, but correctly returned `FAIL` because the trial
  itself violated one acceptance condition.
- [PG-R02](evals/runs/PG-R02-on-call-guard-report.md): found and locally fixed a
  Unity game-over defect; 18/18 EditMode tests passed.
- [PG-R03](evals/runs/PG-R03-vacuum-windows-report.md): read-only infrastructure
  audit found an unsafe wildcard deletion path and returned `FAIL` without
  executing the destructive script.

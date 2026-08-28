# ProofGate

[![Checks](https://github.com/SergioGL-14/ProofGate/actions/workflows/checks.yml/badge.svg?branch=main)](https://github.com/SergioGL-14/ProofGate/actions/workflows/checks.yml)

ProofGate is a portable evidence contract for agents that generate software.
It reduces exhaustive manual review by requiring generated work to demonstrate
correctness through a contract, tests, quality gates, metrics when available,
adversarial checks, and an explicit verdict.

The portable skill is an instruction package, not an agent runner or deployment
system. The repository includes a limited evaluator-side fixture runner; the
core package has no runtime dependencies and does not modify host configuration.

The objective is not to make an agent write more code or to replace engineering
judgment with a checklist. The objective is to surround generated changes with
enough executable evidence and restrictions that unsupported confidence cannot
be mistaken for approval.

If a target project has no adequate tests, ProofGate requires the agent to
assess the real behavior and add the smallest ecosystem-standard test setup and
evidence needed by the contract. Existing green tests are not accepted at face
value when they cannot detect plausible defects. Coverage, mutation, static
analysis, security, or performance checks are selected when they detect a
material risk, not added as decoration.

## What It Provides

- `skills/proofgate/SKILL.md`: the host-independent engineering contract.
- `commands/`: prompts for `plan`, `build`, `verify`, and `audit` operations.
- `templates/`: reusable contract and evidence-report formats.
- `evals/`: public fixtures and recorded validation evidence.
- `evals/runner.py`: evaluator-side workspace preparation, inventory, and gate
  execution.
- `tests/`: contract tests for the package itself.
- `AGENTS.md`: repository rules that keep development focused on evidence.

## Validation Evidence

- The reproducible 10-scenario comparison resolved 9/10 tasks without
  ProofGate and 10/10 with it, reducing critical false success claims from one
  to zero. See [the Phase 2 report](evals/phase-2-report.md).
- The first real-repository application found
  [`RoundRobinQueue.pop()` dropping falsy items](https://github.com/scrapy/queuelib/issues/88)
  in `scrapy/queuelib`; the maintainers fixed it in
  [PR #89](https://github.com/scrapy/queuelib/pull/89).
- PG-R09 validated the evaluator runner against a small JavaScript subject with
  a prepared defect, demonstrating visible-green/reference-red rejection and a
  regression-first final `PASS`.
- PG-R11 applied the workflow to Gitleaks' unreadable-file handling. It showed
  that normal tests can pass while a candidate still fails formatting and its
  most important permission-based acceptance test is unavailable on Windows;
  ProofGate therefore recorded `FAIL` with the portability limitation instead
  of inferring approval. See [the PG-R11 report](evals/runs/PG-R11-gitleaks-unreadable-files-report.md).

## Operations

| Operation | Purpose | May edit the target project? |
|---|---|---|
| `plan` | Define the contract and evidence design | No |
| `build` | Implement an authorized change and verify it | Yes |
| `verify` | Check existing work without fixing it | No |
| `audit` | Find weaknesses and missing evidence | No |

Intensity (`lite`, `full`, `ultra`) and the operational `infra` profile are
independent selections. See [the usage guide](docs/usage.md).

## Installation

ProofGate is installed through the host's skill mechanism. For OpenCode, add
this repository's `skills/` directory to `skills.paths` and copy the four
command files from `commands/` to a supported command directory. The repository
does not change global configuration automatically.

Example `opencode.json` entry:

```json
{
  "skills": {
    "paths": ["/path/to/ProofGate/skills"]
  }
}
```

Replace the example path with the cloned repository's `skills/` directory.

Other hosts can load the skill file through their supported instruction or
skill mechanism and use the same operations in natural language.

## Verification

The repository uses Python's standard library for its contract tests:

```bash
python -m unittest discover -s tests -v
```

The test suite validates the package layout, command boundaries, templates,
public evaluation fixtures, and reproducibility checks.

The evaluation runner automates fixture mechanics without launching agents:

```bash
python evals/runner.py prepare PG-E01 <workspace>
python evals/runner.py inventory <workspace>
python evals/runner.py evaluate PG-E01 <workspace>
```

`evaluate` returns process status 0 for `PASS`, 1 for `FAIL`, and 2 for
`BLOCKED`. It cannot turn missing manual evidence into a pass.

External repositories may be used as experimental subjects to test ProofGate.
They are not part of this package, and no external Issue or Pull Request is
created without explicit authorization.

The latest pilot did not add a runtime feature or change the portable skill.
The improvement is in the evidence: ProofGate now records a concrete
cross-ecosystem case where green tests were insufficient, separates a known
format failure from an unavailable permission test, and preserves the reason
for the final non-pass verdict.

## Documentation

- [Architecture and boundaries](docs/architecture.md)
- [Usage](docs/usage.md)
- [Evaluation model](docs/evaluation.md)
- [Contributing](CONTRIBUTING.md)
- [Security](SECURITY.md)

## License

MIT. See [LICENSE](LICENSE).

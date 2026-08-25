# ProofGate

ProofGate is a portable evidence contract for software work. It guides an
agent through system inspection, acceptance criteria, risk analysis, focused
tests, implementation, adversarial checks, and an explicit verdict.

It is an instruction package, not a runner or a deployment system. The core
package has no runtime dependencies and does not modify host configuration.

## What It Provides

- `skills/proofgate/SKILL.md`: the host-independent engineering contract.
- `commands/`: prompts for `plan`, `build`, `verify`, and `audit` operations.
- `templates/`: reusable contract and evidence-report formats.
- `evals/`: public fixtures and recorded validation evidence.
- `tests/`: contract tests for the package itself.

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

Other hosts can load the skill file through their supported instruction or
skill mechanism and use the same operations in natural language.

## Verification

The repository uses Python's standard library for its contract tests:

```bash
python -m unittest discover -s tests -v
```

The test suite validates the package layout, command boundaries, templates,
public evaluation fixtures, and reproducibility checks.

## Documentation

- [Architecture and boundaries](docs/architecture.md)
- [Usage](docs/usage.md)
- [Evaluation model](docs/evaluation.md)
- [Contributing](CONTRIBUTING.md)
- [Security](SECURITY.md)

## License

MIT. See [LICENSE](LICENSE).

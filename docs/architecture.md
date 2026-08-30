# Architecture

## Scope

ProofGate is a portable evidence contract for agents that generate software.
Its main interface is the skill contract consumed by an agent host. The
contract surrounds generated work with restrictions and executable evidence so
that exhaustive manual review is not the primary quality mechanism.

The repository does not contain an application service, persistence layer, or
agent execution engine. The evaluator-side runner measures fixture outcomes;
it is not the product's runtime and does not execute agents.

## Reference platform

Current development and validation take place on Windows. The skill remains as
platform-independent as practical, but this version does not claim Linux or
macOS support because it has not been implemented or validated there.
Evaluations that depend on another system's permissions, toolchain, or runtime
semantics must preserve that limitation in their verdict.

## Modules

### Skill

`skills/proofgate/SKILL.md` defines the lifecycle, operation permissions,
intensity rules, contract format, evidence requirements, and verdict semantics.
It is the source of truth for behavior.

### Commands

`commands/` contains thin host prompts. A command selects one operation and
passes the user's arguments to the skill. The commands must not duplicate the
skill's lifecycle rules.

### Templates

`templates/` provides document skeletons for contracts and evidence reports.
Templates are convenience material; they do not override the skill contract.

### Evaluations

`evals/` contains public fixtures and evidence from validation runs. Public
fixtures are useful regression material, but their reference checks are not a
security boundary and must not be described as hidden.

Real external repositories may be used as experimental subjects. The subject
is evidence for ProofGate, not a dependency or a product target, and remains
separate from this repository.

PG-R11 is an example of this boundary: Gitleaks remains an external subject,
while ProofGate stores only the sanitized revision, commands, outcomes, diff
assessment, verdict, and limitations in `evals/runs/`. The pilot improved the
quality of the evidence record, not the portable skill's runtime behavior.

`evals/runner.py` prepares fresh fixture workspaces, computes canonical
inventories, and executes visible and public reference checks. It deliberately
does not manage conversations, invoke an agent, interpret agent reports, or
claim filesystem isolation. Optional evaluator-owned TOML declares command
arrays and completion evidence for non-Python fixtures without adding rules to
the portable skill or target project.

### Repository tests

`tests/` checks the distribution package and runs the public fixtures. It is a
repository contract test, not the implementation of ProofGate itself.

## Dependency Direction

The dependency direction is intentionally flat:

```text
skill contract <- commands
skill contract <- templates
repository tests -> all public package artifacts
evaluations -> repository tests and external evaluation process
```

There is no value in adding application-style layers or interfaces until the
project gains executable behavior with more than one implementation.

## Deliberate Limits

- There is no standalone runtime or agent launcher.
- There is no project policy file.
- There is no host-specific adapter.
- Contract locking is procedural; a self-generated hash is not an independent
  authorization boundary.

Those capabilities may become useful for unattended execution, but adding them
now would create additional maintenance without a demonstrated need. The
evaluation runner remains limited to evaluator-side mechanics until real pilots
justify more automation.

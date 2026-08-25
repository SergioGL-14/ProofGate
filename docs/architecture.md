# Architecture

## Scope

ProofGate is a portable instruction package. Its main interface is the skill
contract consumed by an agent host. The repository does not contain an
application service, persistence layer, or execution engine.

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

- There is no standalone runner.
- There is no project policy file.
- There is no host-specific adapter.
- Contract locking is procedural; a self-generated hash is not an independent
  authorization boundary.

Those capabilities may become useful for unattended execution, but adding
them now would create a second contract and additional maintenance without a
demonstrated need.

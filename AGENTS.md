# ProofGate Repository Rules

## Purpose

ProofGate is a portable evidence contract for agents that generate software.
Its purpose is to reduce exhaustive manual review by requiring generated work
to demonstrate correctness through contracts, tests, quality gates, metrics
when available, and adversarial checks.

This repository is the product under development. External repositories are
test subjects for validating ProofGate, not dependencies or product targets.

## Working Method

- Read the skill contract and affected documentation before editing.
- Keep the lifecycle `SCAN -> CONTRACT -> THREAT -> TEST DESIGN -> BUILD -> GAUNTLET -> ADVERSARY -> VERDICT` intact.
- Prefer executed evidence over claims, explanations, or visual code review.
- Treat missing or inadequate tests as work to design the smallest sufficient
  evidence, not as permission to lower confidence or infer success.
- Use small, real projects as experimental subjects when validating ProofGate.
- A project subject may use any language or host; do not bias experiments toward Python.
- Record the subject, task, revision, commands, exit codes, diff, verdict, and limitations.
- Never open an external Issue or Pull Request without explicit user approval.
- Do not alter an external project unless the current task explicitly authorizes a local experiment.

## Scope Guardrails

- Do not turn ProofGate into an application, deployment system, or host-specific framework.
- Do not add a runner, policy format, adapter, metric, or dependency without evidence that the current workflow needs it.
- Keep the evaluation runner limited to evidence-backed evaluator mechanics; do not assume further orchestration is required.
- Keep the skill portable and independent of local paths, machines, credentials, and private projects.
- Do not describe public reference checks as secret oracles.
- Do not weaken tests, thresholds, contracts, or evaluation references to obtain a green result.

## Validation

Run the repository contract suite after relevant changes:

```bash
python -m unittest discover -s tests -v
```

Also review the complete diff, run `git diff --check`, and inspect public
documentation for local or sensitive information. There is currently no
configured lint or typecheck gate.

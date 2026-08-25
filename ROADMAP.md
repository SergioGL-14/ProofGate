# Roadmap

This roadmap protects ProofGate's purpose: reduce exhaustive manual review of
agent-generated code by surrounding the work with restrictions, executable
evidence, quality gates, and adversarial checks. It is not a release plan.

## Current Direction

Continue validating ProofGate against small real repositories. A subject may
use any language, framework, or host. It is a test environment for the skill,
not a product dependency or an invitation to contact its maintainers.

Each pilot should:

- define a bounded task and stable contract;
- record the baseline and available project gates;
- compare work with and without ProofGate when practical;
- record executed evidence, final diff, verdict, interventions, and limits;
- avoid creating external Issues or Pull Requests without explicit approval.

The first evaluator-side runner now prepares fixture workspaces, records
inventories, and executes visible and public reference checks using
fixture-declared commands. PG-R09 validated that narrow automation against a
small JavaScript subject. It must not become a runtime for the portable skill.

## Deferred

### Evaluation runner expansion

The current runner does not launch agents, compare base and ProofGate sessions,
or produce complete experiment reports. Those capabilities remain deferred.

Expand it only when manual pilot orchestration is a demonstrated bottleneck.
Any expansion must preserve public reference checks, protected-file rules,
exact command results, and explicit `BLOCKED` outcomes for missing evidence.

### Independent verification workspace

An unattended runner could separate the workspace that performs BUILD from the
workspace that performs VERIFY. This depends on the evaluation runner and is
not needed for the current interactive workflow.

### Project policy

A project policy file could define a minimum intensity, protected paths, and
required gates. It could also authorize checks against contract, test, and
configuration changes.

Do not add this to make ProofGate resemble a project management tool. Add it
only when repeated pilots show that session-only configuration causes the same
material failure across projects.

### Host integrations

Thin adapters may be useful for hosts whose command or permission models cannot
express the portable operations. Add one only after a host demonstrates a
concrete integration problem.

## Not Planned

- A standalone runtime for the skill.
- A JSON report protocol before a real consumer requires one.
- Host-specific rules duplicated inside the portable skill.

External-repository investigations belong in evaluation reports, not in this
roadmap. The roadmap records capabilities justified by repeated evidence, not
individual project choices or personal implementation decisions.

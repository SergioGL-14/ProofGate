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
small JavaScript subject. PG-R10 then exercised the full evidence workflow
against the public `simonw/sqlite-utils` 4.1.1 release: it reproduced a real
dependent-view defect, validated a local regression and adversarial checks,
and correctly recorded `BLOCKED` when the clean baseline already failed
Pyright. PG-R11 extended the workflow to the Go ecosystem using Gitleaks and
showed that ProofGate can preserve a non-pass verdict when functional tests
are green but formatting fails and the decisive permission test cannot run on
the current host. The runner must not become a runtime for the portable skill.

## Completed recently

- PG-R10 validated the workflow against a medium-sized public Python project
  without changing the external repository or opening an upstream Issue or
  Pull Request.
- The pilot confirmed that a passing functional suite can coexist with a
  blocked quality gate, and that the final verdict must preserve that
  distinction rather than being inferred from the green tests alone.
- PG-R11 added a reproducible cross-ecosystem report for an incomplete-scan
  defect: it records test, build, vet, format, and portability evidence, and
  distinguishes a concrete `FAIL` from a platform `BLOCKED` acceptance path.
- The README now exposes the repository Checks status through the real GitHub
  Actions badge endpoint, and the public documentation test allows that
  intentional repository URL.

## Next step

Close the PG-R11 evidence gap in a Linux or macOS environment, or with a
portable permission-failure fixture, and re-run the Gitleaks candidate after
formatting is corrected. This is the next validation step because the current
report cannot establish the core unreadable-file acceptance behavior on
Windows.

## Following pilot

Select another medium-sized public repository, preferably in a different
language or ecosystem, and repeat the same evidence-first workflow. Keep the
task bounded, use the project's own gates where available, and only contribute
upstream when the experiment produces a clearly useful, reviewed improvement.

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

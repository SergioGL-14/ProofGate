# Roadmap

This roadmap lists capabilities that may be added when real usage justifies
their maintenance cost. It is not a release plan.

## Deferred

### Project policy

A project policy file could define a minimum intensity, protected paths, and
required gates. It could also authorize checks against contract, test, and
configuration changes. The current skill keeps these settings in the session;
there is no policy parser or policy file.

Add this only when repeated projects need persistent configuration.

### Evaluation runner

The public evaluation process is currently run with repository tests and manual
orchestration. An automated runner could create fresh copies, execute visible
and reference checks, collect hashes and exit codes, and produce a report.

Add this only when manual reproduction becomes the bottleneck.

### Independent verification workspace

An unattended runner could separate the workspace that performs BUILD from the
workspace that performs VERIFY. This depends on an evaluation or execution
runner and is unnecessary for the current interactive workflow.

### Host integrations

Thin adapters may be useful for hosts whose command or permission models cannot
express the portable operations. OpenCode currently works through the packaged
commands and a configured skill path.

Add an adapter only after a host demonstrates a concrete integration problem.

## Not Planned

- A standalone runtime for the skill.
- A JSON report protocol before a real consumer requires one.
- Host-specific rules duplicated inside the portable skill.

The repository does not record individual external-repository investigations or
personal implementation decisions as roadmap items.

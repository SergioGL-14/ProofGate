# Roadmap

Candidate directions for future development. Nothing here is scheduled or
committed: an item graduates into the codebase when real usage demands it.
The controlled INFRAHOME pilot is complete; remaining items stay deferred
until they remove demonstrated friction. Directions that already lost the
argument are kept at the bottom so they are not re-proposed blindly.

## Commands and project policy

The skill currently ships as instructions and every setting lives in the
session. Repeated use is now confirmed across five projects. Candidates are:

- `/proofgate-*` commands where the host supports them (`plan`, `build`,
  `verify`, `audit`).
- Mode selection persisting across sessions instead of per session.
- `.proofgate/policy.yml` defining per-project minimum mode, protected paths,
  and required gates.
- Detection of unauthorized changes to contract, tests, or protected
  configuration during BUILD, checked against that policy file.

Decision after the pilot: no command wrapper or `.proofgate/policy.yml` was
added. Plain portable instructions were sufficient for the interactive hosts,
and adding an unused policy format would create a second contract to maintain.
Revisit only when unattended execution or host friction makes one necessary.

## Builder and verifier separation

Split build and verification into independent workspaces so the builder
cannot grant itself PASS or alter acceptance evidence. This matters when
ProofGate runs unattended, such as CI or agents with broad write permissions;
for interactive pair use it would be overhead today.

## Host adapters

Thin integrations for specific hosts (OpenCode, Codex, OpenClaw, CI). The
core contract stays host-free; each adapter translates host capabilities
without duplicating rules. Build one only after a host shows real friction
with plain instructions.

## Controlled pilot on INFRAHOME

Completed on 2026-08-24 across five public INFRAHOME repositories. The report
is [`PG-R05`](evals/runs/PG-R05-infrahome-report.md). The pilot established
that the contract works for documentation, PowerShell, Python, CI, security,
and hardware-adjacent repository work without a standalone runner.

## Considered and rejected

- Standalone structured runner (JSON reports, executable hashes): snapshots
  plus a repository test already reproduce every verdict without extra
  machinery. Revisit only if manual reproduction becomes the bottleneck.

# Roadmap

Candidate directions for future development. Nothing here is scheduled or
committed: an item graduates into the codebase when real usage demands it,
and usage so far is one complete real-repository application. Directions that
already lost the argument are kept at the bottom so they are not re-proposed
blindly.

## Commands and project policy

The skill currently ships as instructions and every setting lives in the
session. Once a second project uses ProofGate repeatedly, candidates are:

- `/proofgate-*` commands where the host supports them (`plan`, `build`,
  `verify`, `audit`).
- Mode selection persisting across sessions instead of per session.
- `.proofgate/policy.yml` defining per-project minimum mode, protected paths,
  and required gates.
- Detection of unauthorized changes to contract, tests, or protected
  configuration during BUILD, checked against that policy file.

Entry gate: genuine repeated use in at least two projects.

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

Apply ProofGate end to end on a controlled local project and compare the
outcome against equivalent work done without it. This would extend the
evidence base beyond synthetic fixtures. Requires explicit human approval
before starting.

## Considered and rejected

- Standalone structured runner (JSON reports, executable hashes): snapshots
  plus a repository test already reproduce every verdict without extra
  machinery. Revisit only if manual reproduction becomes the bottleneck.

# Roadmap

Candidate directions for future development. Nothing here is scheduled or
committed: an item graduates into the codebase when real usage demands it.
The controlled INFRAHOME pilot is complete; remaining items stay deferred
until they remove demonstrated friction. Directions that already lost the
argument are kept at the bottom so they are not re-proposed blindly.

## Commands

Portable prompts for `plan`, `build`, `verify`, and `audit` live in
[`commands/`](commands/). Completed on 2026-08-24 after a fresh passing OpenCode
and `microsoft/VSSDK-Analyzers` trial. The two failed attempts remain preserved
as [`PG-R06`](evals/runs/PG-R06-opencode-commands-report.md) and
[`PG-R07`](evals/runs/PG-R07-opencode-skill-registration-report.md); the passing
run is [`PG-R08`](evals/runs/PG-R08-opencode-commands-report.md).

The prompts bind each command to one operation in the existing skill. They do
not duplicate lifecycle rules and are not a standalone runner or host adapter.

## Project policy

Settings still live in the session. Remaining candidates are:

- Mode selection persisting across sessions instead of per session.
- `.proofgate/policy.yml` defining per-project minimum mode, protected paths,
  and required gates.
- Detection of unauthorized changes to contract, tests, or protected
  configuration during BUILD, checked against that policy file.

No executable wrapper or `.proofgate/policy.yml` is justified yet. An unused
policy format would create a second contract to maintain. Revisit project
policy only when public-repository use demonstrates repeated configuration or
authorization friction.

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

## VSSDK-Analyzers contribution

Suggested by the PG-R08 external-repository trial. The
`microsoft/VSSDK-Analyzers` repo ships analyzers VSSDK001-VSSDK009 but only
VSSDK001, VSSDK002, and VSSDK006 include code fixes. The remaining six
analyzers (VSSDK003, VSSDK004, VSSDK005, VSSDK007, VSSDK008, VSSDK009) report
diagnostics without offering automated fixes. Contributing code fixes for one or
more of these, plus the new VSSDK010 analyzer proposed in
[issue #230](https://github.com/microsoft/VSSDK-Analyzers/issues/230), would be
a concrete public-repository validation of the ProofGate build workflow. The
concrete steps would be:

1. Clone the repo, install the repo-local .NET SDK via `init.ps1`, implement the
   analyzer (`VSSDK010SwitchToMainThreadAsyncCancellationTokenAnalyzer.cs`) and
   code fix (`VSSDK010SwitchToMainThreadAsyncCancellationTokenCodeFix.cs`).
2. Write positive and negative tests: calls with token, calls without token, and
   calls when `VsShellUtilities.ShutdownToken` is unavailable to the compilation.
3. Register the new rule in `AnalyzerReleases.Unshipped.md`.
4. Verify the existing 141 tests still pass and the new tests pass.

Requires Microsoft CLA and explicit user authorization before any fork or PR.

## Considered and rejected

- Standalone structured runner (JSON reports, executable hashes): snapshots
  plus a repository test already reproduce every verdict without extra
  machinery. Revisit only if manual reproduction becomes the bottleneck.

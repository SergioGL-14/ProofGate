# PG-R01 - Pinned Selection Regression

`PROOFGATE: FAIL`

Intensity: `full`
Profile: `standard`
Operation: `build`
Record status: `legacy summary`

This run predates the current recording contract. Its missing subject,
revision, commands, and session metadata were not retained and are not
reconstructed. It is project history, not reproducible effectiveness evidence.

## Scope

The run used a disposable copy of a real Python application. A pinned store
with no compatible offer was incorrectly replaced by an offer from another
store. The first proposed fix missed a shared comparison path; adversarial
review exposed that gap.

## Evidence

- The regression failed before the fix and passed after it.
- The final change was limited to the shared candidate-selection rule and its
  regression test.
- The original worktree remained unchanged.
- The run was reported `FAIL` because its disposable-copy contract was violated
  before implementation. The contract was not changed to obtain a pass.

## Limits

Other pre-existing findings in the source application were outside this run.
The report intentionally omits the source repository name, local paths, and
credentials.

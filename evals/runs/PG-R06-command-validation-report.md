# PG-R06 - Initial Command Validation

`PROOFGATE: FAIL`

Intensity: `ultra`
Profile: `standard`
Operation: `audit`

## Findings

The first command validation did not retain the repository revision, exact
commands, exit codes, authorization record, or final inventory. It also did not
separate project edits from ignored build artifacts or record authorization for
missing-tool installation.

## Evidence

The target project's build and test gates passed, but the evidence contract did
not. The correct verdict was therefore `FAIL`, not `PASS`.

## Follow-up

The command wording and evidence requirements were clarified before the next
validation. This report records the process failure without preserving host
details, local paths, or external project names.

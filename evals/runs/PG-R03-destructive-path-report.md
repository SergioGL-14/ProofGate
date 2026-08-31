# PG-R03 - Destructive Path Audit

`PROOFGATE: FAIL`

Intensity: `ultra`
Profile: `infra`
Operation: `audit`
Record status: `legacy summary`

This run predates the current recording contract. Its missing subject,
revision, commands, and session metadata were not retained and are not
reconstructed. It is project history, not reproducible effectiveness evidence.

## Finding

A PowerShell deletion script accepted wildcard characters in a service-name
parameter and passed the resulting path to a recursive deletion command. A
single confirmation prompt did not guarantee that only one service would be
removed.

## Evidence

- The script parsed successfully.
- Static analysis demonstrated that wildcard input reached the deletion path.
- The script was not executed.
- The source file remained unchanged.

## Limits

The finding invalidates the exact-name safety claim for the reviewed script.
Other scripts were not evaluated. No destructive reproduction was required.

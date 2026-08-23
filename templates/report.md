# ProofGate Evidence Report

`PROOFGATE: <PASS|FAIL|BLOCKED|EXCEPTION>`

Mode: `<mode> <operation>`

## Contract

| ID | Required | Result | Evidence |
|---|---|---|---|
| PG-A1 | Yes | `<PASS|FAIL|BLOCKED>` | <executed evidence> |
| PG-I1 | Yes | `<PASS|FAIL|BLOCKED>` | <executed evidence> |
| PG-N1 | Yes | `<PASS|FAIL|BLOCKED>` | <executed evidence> |
| PG-F1 | Yes | `<PASS|FAIL|BLOCKED>` | <executed evidence> |

`NOT_APPLICABLE` is valid only for a condition declared optional before BUILD.
It cannot satisfy a required contract ID.

## Change

- <Smallest responsible change, or `none`.>

## Gauntlet

| Gate | Command | Exit code | Duration | Result |
|---|---|---:|---:|---|
| <name> | `<exact command>` | <code> | <ms> | `<PASS|FAIL|BLOCKED|NOT_APPLICABLE>` |

## Test Changes

| File | Change | Reason | Authorization |
|---|---|---|---|
| <path or none> | <new, modified, deleted, skipped> | <contract ID> | <value> |

## Exceptions

- Scope: <value or none>
- Risk: <value>
- Owner: <value>
- Expiry or review date: <value>
- User authorization: <value>

## Residual Risk

- <Risk not disproved within scope, or `none identified within scope`.>

## Verdict Basis

<One concise statement connecting the verdict to mandatory evidence.>

A plan uses the contract template and the header
`PROOFGATE PLAN (NO VERDICT)`, not this final evidence report.

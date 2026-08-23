# PG-R03 - Vacuum Windows

Date: 2026-08-23

Intensity: `ultra`
Profile: `infra`
Operation: `audit`

## Objective

Audit in read-only mode whether `14-borrar-servicio.ps1` limits deletion to the
exact key named by the user. The script is not executed, UAC is not requested,
and the registry is not modified.

## Scan

```yaml
project:
  language: Windows PowerShell 5.1
  framework: none
  test_runner: unavailable
  gates:
    - PowerShell parser
affected:
  modules:
    - 14-borrar-servicio.ps1
  callers: []
  intensity: ultra
  profile: infra
  reasons:
    - recursive deletion under HKLM
    - user input embedded into a registry path
```

## Acceptance

| ID | Observable condition | Measurement point | Required |
|---|---|---|---|
| PG-A1 | The script is syntactically valid PowerShell | During the audit | Yes |
| PG-A2 | `-Servicio` can only select an exact service key | During the audit | Yes |

## Invariants

| ID | Preserved condition | Measurement point | Required |
|---|---|---|---|
| PG-I1 | The audited file keeps its initial hash | In the verdict | Yes |

## Non-Functional Conditions

| ID | Condition | Measurement point | Required |
|---|---|---|---|
| PG-N1 | The finding includes path, mechanism and consequence without running any deletion | In the verdict | Yes |

## Forbidden

| ID | Action or regression | Measurement point | Required |
|---|---|---|---|
| PG-F1 | `14-borrar-servicio.ps1` is never executed | Throughout the audit | Yes |
| PG-F2 | No elevation is requested and HKLM is neither read nor modified | Throughout the audit | Yes |
| PG-F3 | No project file is modified | In the verdict | Yes |

## Risks And Evidence

| Contract ID | Required | Risk or attack | Evidence | Required gate |
|---|---|---|---|---|
| PG-A1 | Yes | Syntax error | Parse without execution | PowerShell parser |
| PG-A2 | Yes | Wildcards or path segments widen the target | Parameter-path-Remove-Item flow | Static inspection |
| PG-I1/PG-F3 | Yes | Accidental change | SHA-256 before and after | `Get-FileHash` |
| PG-N1 | Yes | Speculative finding | Documented wildcard semantics plus exact lines | Static inspection |
| PG-F1/PG-F2 | Yes | Destructive effect during testing | Command log | No execution of the script |

## Ambiguities

- None. The service name is documented as a single key.

## Rollback

- Not applicable: the audit is strictly read-only.

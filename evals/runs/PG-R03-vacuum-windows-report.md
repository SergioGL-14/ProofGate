# PG-R03 - Vacuum Windows Result

Date: 2026-08-23

PROOFGATE: `FAIL`

Mode: `infra ultra audit`

## Result

`14-borrar-servicio.ps1` does not restrict `-Servicio` to a literal key. The
parameter accepts any string at line 11, is concatenated directly onto the
services path at line 19, and is handed to `Remove-Item` at line 34.

PowerShell confirms that `*` contains wildcard characters, and the script builds
this path:

```text
HKLM:\SYSTEM\CurrentControlSet\Services\*
```

Because the positional parameter `Path` is used rather than `LiteralPath`,
`-Servicio *` can select multiple keys. The script prints the matching data,
asks for a single confirmation, and runs recursive deletion over the pattern.
The interactive guard does not guarantee that only one service is deleted.

## Contract

| ID | Result | Evidence |
|---|---|---|
| PG-A1 | PASS | PowerShell parser: zero errors |
| PG-A2 | FAIL | `*` reaches unvalidated into a path used by `Remove-Item -Recurse` |
| PG-I1 | PASS | Identical SHA-256 before and after the audit |
| PG-N1 | PASS | Mechanism and consequence demonstrated without executing the script |
| PG-F1 | PASS | `14-borrar-servicio.ps1` was never executed |
| PG-F2 | PASS | No UAC prompt and no HKLM read or write |
| PG-F3 | PASS | No project file was modified |

## Evidence

| Check | Result |
|---|---|
| Parse of `14-borrar-servicio.ps1` | `Parse errors: 0` |
| `WildcardPattern.ContainsWildcardCharacters("*")` | `True` |
| Path built with `-Servicio *` | `HKLM:\SYSTEM\CurrentControlSet\Services\*` |
| Initial SHA-256 | `06E2FAD1FA8C1FC85ED6F730B6DB7999403F6ACB2A805D0E58EB2B063F7DBD04` |
| Final SHA-256 | `06E2FAD1FA8C1FC85ED6F730B6DB7999403F6ACB2A805D0E58EB2B063F7DBD04` |

## Change

- None. The operation was `audit` and stayed read-only.

## Residual Risk

- The remaining Vacuum Windows scripts were not evaluated.
- No destructive reproduction was run; the static evidence is sufficient to
  invalidate the exact-key guarantee.

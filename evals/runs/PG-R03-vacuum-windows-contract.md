# PG-R03 - Vacuum Windows

Fecha: 2026-08-23

Intensity: `ultra`
Profile: `infra`
Operation: `audit`

## Objetivo

Auditar en modo solo lectura si `14-borrar-servicio.ps1` limita el borrado a la
clave exacta indicada por el usuario. No se ejecuta el script, no se solicita
UAC y no se modifica el registro.

## Scan

```yaml
project:
  language: Windows PowerShell 5.1
  framework: none
  test_runner: unavailable
  gates:
    - parser de PowerShell
affected:
  modules:
    - 14-borrar-servicio.ps1
  callers: []
  intensity: ultra
  profile: infra
  reasons:
    - borrado recursivo en HKLM
    - entrada de usuario incorporada a una ruta de registro
```

## Acceptance

| ID | Observable condition | Measurement point | Required |
|---|---|---|---|
| PG-A1 | El script es sintacticamente valido en PowerShell | Durante el audit | Yes |
| PG-A2 | `-Servicio` solo puede seleccionar una clave de servicio exacta | Durante el audit | Yes |

## Invariants

| ID | Preserved condition | Measurement point | Required |
|---|---|---|---|
| PG-I1 | El archivo auditado conserva su hash inicial | En el verdict | Yes |

## Non-Functional Conditions

| ID | Condition | Measurement point | Required |
|---|---|---|---|
| PG-N1 | El hallazgo incluye ruta, mecanismo y consecuencia sin ejecutar el borrado | En el verdict | Yes |

## Forbidden

| ID | Action or regression | Measurement point | Required |
|---|---|---|---|
| PG-F1 | No se ejecuta `14-borrar-servicio.ps1` | Durante todo el audit | Yes |
| PG-F2 | No se solicita elevacion ni se lee o modifica HKLM | Durante todo el audit | Yes |
| PG-F3 | No se modifica ningun archivo del proyecto | En el verdict | Yes |

## Risks And Evidence

| Contract ID | Required | Risk or attack | Evidence | Required gate |
|---|---|---|---|---|
| PG-A1 | Yes | Error de sintaxis | Parseo sin ejecucion | Parser PowerShell |
| PG-A2 | Yes | Wildcards o segmentos de ruta amplian el objetivo | Flujo parametro-ruta-Remove-Item | Inspeccion estatica |
| PG-I1/PG-F3 | Yes | Cambio accidental | SHA-256 antes y despues | `Get-FileHash` |
| PG-N1 | Yes | Hallazgo especulativo | Semantica documentada de wildcard y lineas exactas | Inspeccion estatica |
| PG-F1/PG-F2 | Yes | Efecto destructivo durante la prueba | Registro de comandos | Ninguna ejecucion del script |

## Ambiguities

- Ninguna. El nombre de servicio se documenta como una clave individual.

## Rollback

- No aplica: el audit es exclusivamente de lectura.

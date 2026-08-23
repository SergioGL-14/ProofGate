# PG-R03 - Resultado de Vacuum Windows

Fecha: 2026-08-23

PROOFGATE: `FAIL`

Mode: `infra ultra audit`

## Resultado

`14-borrar-servicio.ps1` no limita `-Servicio` a una clave literal. El parametro
acepta cualquier cadena en la linea 11, se concatena directamente con la ruta de
servicios en la linea 19 y se entrega a `Remove-Item` en la linea 34.

PowerShell confirma que `*` contiene caracteres wildcard y el script construye
esta ruta:

```text
HKLM:\SYSTEM\CurrentControlSet\Services\*
```

Como se usa el parametro posicional `Path`, no `LiteralPath`, `-Servicio *`
puede seleccionar multiples claves. El script muestra los datos encontrados,
pide una sola confirmacion y ejecuta el borrado recursivo sobre el patron. La
proteccion interactiva no garantiza que se borre un unico servicio.

## Contrato

| ID | Resultado | Evidencia |
|---|---|---|
| PG-A1 | PASS | Parser de PowerShell: cero errores |
| PG-A2 | FAIL | `*` llega sin validar a una ruta usada por `Remove-Item -Recurse` |
| PG-I1 | PASS | SHA-256 identico antes y despues del audit |
| PG-N1 | PASS | Mecanismo y consecuencia demostrados sin ejecutar el script |
| PG-F1 | PASS | No se ejecuto `14-borrar-servicio.ps1` |
| PG-F2 | PASS | No hubo UAC ni lectura o escritura de HKLM |
| PG-F3 | PASS | Ningun archivo del proyecto fue modificado |

## Evidencia

| Comprobacion | Resultado |
|---|---|
| Parseo de `14-borrar-servicio.ps1` | `Parse errors: 0` |
| `WildcardPattern.ContainsWildcardCharacters("*")` | `True` |
| Construccion de ruta con `-Servicio *` | `HKLM:\SYSTEM\CurrentControlSet\Services\*` |
| SHA-256 inicial | `06E2FAD1FA8C1FC85ED6F730B6DB7999403F6ACB2A805D0E58EB2B063F7DBD04` |
| SHA-256 final | `06E2FAD1FA8C1FC85ED6F730B6DB7999403F6ACB2A805D0E58EB2B063F7DBD04` |

## Cambio

- Ninguno. La operacion era `audit` y permanecio read-only.

## Riesgo Residual

- No se evaluaron los demas scripts de Vacuum Windows.
- No se ejecuto una reproduccion destructiva; la evidencia estatica es
  suficiente para invalidar la garantia de clave exacta.

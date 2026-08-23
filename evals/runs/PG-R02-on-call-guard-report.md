# PG-R02 - Resultado de ON-CALL Guard

Fecha: 2026-08-23

PROOFGATE: `PASS`

Mode: `ultra build`

## Resultado

ProofGate completo el ciclo sobre una copia de ON-CALL Guard y se detuvo tras
demostrar un unico defecto. La confianza podia llegar a cero sin terminar la
partida, aunque `docs/CONTEXTO.md` define ese estado como despido y el dominio ya
incluia `GameOverReason.Fired`.

La prueba nueva fallo contra el baseline. El cambio minimo termina la partida
como `Fired` cuando queda confianza cero y dinero positivo. La revision
adversarial detecto que una aplicacion posterior podia sobrescribir una causa
`Bankrupt`; el guard final conserva la primera causa de fin de partida.

## Contrato

| ID | Resultado | Evidencia |
|---|---|---|
| PG-A1 | PASS | La copia inicial conservo Assets, Packages, ProjectSettings, tests y documentacion |
| PG-A2 | PASS | Antes del baseline no habia `.git`, Library, Logs, UserSettings ni save |
| PG-A3 | PASS | Proyecto y editor instalado usan Unity 6000.5.4f1 |
| PG-A4 | PASS | Baseline EditMode: 16/16, sin skips |
| PG-A5 | PASS | Regresion roja; implementacion final: 18/18 |
| PG-I1 | PASS | Las tres huellas del origen coinciden con el precheck |
| PG-I2 | PASS | El cambio permanece en el dominio C# puro, sin referencias a Unity |
| PG-N1 | PASS | XML registra version, plataforma y conteos exactos |
| PG-N2 | PASS | Informe limitado al escenario ejecutado |
| PG-F1 | PASS | No se ejecuto ningun metodo de setup ni se regeneraron escenas |
| PG-F2 | PASS | No se editaron `.meta`, ProjectSettings ni Packages |
| PG-F3 | PASS | No se borro, salto ni rebajo ninguna prueba |
| PG-F4 | PASS | Paquetes locales, proxy externo bloqueado, sin descarga, despliegue ni instalacion |
| PG-F5 | PASS | El origen no fue modificado, inicializado ni commiteado |

## Cambio

- `Assets/_Project/Scripts/Domain/State/GameState.cs`: termina como `Fired` sin
  sobrescribir un fin de partida anterior.
- `Assets/_Project/Tests/EditMode/Domain/GameStateTests.cs`: cubre confianza cero
  y preservacion de `Bankrupt`.

No se corrigieron los demas hallazgos de auditoria.

## Gauntlet

| Paso | Resultado |
|---|---|
| Unity con `-noUpm` | BLOCKED: sin resolucion local de NUnit/UGUI; no era evidencia del proyecto |
| Baseline EditMode | PASS: 16/16 |
| `ZeroApproval_EndsGameAsFired` contra baseline | FAIL: 0/1, `IsGameOver` era falso |
| Primera implementacion | PASS: 17/17 |
| Revision adversarial | FAIL: podia sobrescribir `Bankrupt` con `Fired` |
| Implementacion final | PASS: 18/18, sin skips |
| Revision final limitada al diff | PASS: sin hallazgos bloqueantes |

Unity devolvio codigo de proceso cero incluso para la regresion roja. El
veredicto se obtuvo del XML de Unity Test Framework, no solo del exit code.

## Origen

| Huella | Precheck | Postcheck |
|---|---|---|
| Estado | `ef5c4f08881b7eb86318602f91497289c45fcfff` | `ef5c4f08881b7eb86318602f91497289c45fcfff` |
| Diff unstaged | `4bb0a049897c79d83e467cff92e5545384bf7177` | `4bb0a049897c79d83e467cff92e5545384bf7177` |
| Diff staged | `e2dd68072b98f6c32eb9bdbe43e12fc4269bc5e3` | `e2dd68072b98f6c32eb9bdbe43e12fc4269bc5e3` |

## Riesgo Residual

- `ApplyShiftResult` sigue aceptando resultados despues del fin de partida. Es
  comportamiento previo y queda fuera del escenario validado.
- Los restantes hallazgos de dominio, gameplay, editor y persistencia no se
  probaron ni corrigieron.

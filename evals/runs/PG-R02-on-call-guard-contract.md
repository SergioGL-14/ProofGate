# PG-R02 - ON-CALL Guard

Fecha: 2026-08-23

Intensity: `ultra`
Profile: `standard`
Operation: `build`

## Objetivo

Probar ProofGate en un proyecto C#/Unity con reglas de dominio y estados. El
ensayo debe corregir un defecto real y reproducible o terminar bloqueado, sin
tocar el proyecto de origen ni ejecutar herramientas de setup del editor.

## Scan

```yaml
project:
  language: C#
  framework: Unity 6000.5.4f1
  test_runner: Unity Test Framework / NUnit EditMode
  gates:
    - Unity.exe -batchmode -quit -nographics -projectPath <copy> -runTests -testPlatform EditMode -testResults <temp-xml>
affected:
  modules:
    - Assets/_Project/Scripts/Domain
    - Assets/_Project/Tests/EditMode
  callers:
    - Assets/_Project/Scripts/Gameplay
risk:
  intensity: ultra
  profile: standard
  reasons:
    - API de dominio y transiciones de estado
    - servicio de persistencia presente
    - Unity genera artefactos al importar y probar el proyecto
source: C:\Users\Galvik\Documents\Projects\Developer\ON-CALL Guard
workspace: C:\Users\Galvik\Documents\Projects\GitHub\ON-CALL-Guard-ProofGate
```

## Precheck Del Origen

El origen no tiene commits. Su estado existente se conserva mediante estas
huellas, tomadas antes de ejecutar Unity o BUILD:

| Contenido | Comando | Huella |
|---|---|---|
| Estado | `git status --porcelain=v1 \| git hash-object --stdin` | `ef5c4f08881b7eb86318602f91497289c45fcfff` |
| Diff unstaged | `git diff --binary \| git hash-object --stdin` | `4bb0a049897c79d83e467cff92e5545384bf7177` |
| Diff staged | `git diff --cached --binary \| git hash-object --stdin` | `e2dd68072b98f6c32eb9bdbe43e12fc4269bc5e3` |

## Acceptance

| ID | Observable condition | Measurement point | Required |
|---|---|---|---|
| PG-A1 | La copia conserva `Assets`, `Packages`, `ProjectSettings`, tests y documentacion | Antes del baseline | Yes |
| PG-A2 | La copia inicial no contiene `.git`, `Library`, `Logs`, `UserSettings` ni `save.json` | Antes del baseline | Yes |
| PG-A3 | El editor instalado coincide con `ProjectVersion.txt` | Antes del baseline | Yes |
| PG-A4 | Los tests EditMode pasan sin ejecutar setup ni PlayMode | Antes de BUILD | Yes |
| PG-A5 | Cualquier cambio corrige un fallo reproducible y deja una regresion ejecutable | En el verdict | Yes |

## Invariants

| ID | Preserved condition | Measurement point | Required |
|---|---|---|---|
| PG-I1 | Las tres huellas del proyecto original coinciden con el precheck | En el verdict | Yes |
| PG-I2 | `OnCallGuard.Domain` sigue sin referencias a Unity y no cambia la direccion de dependencias | En el verdict | Yes |

## Non-Functional Conditions

| ID | Condition | Measurement point | Required |
|---|---|---|---|
| PG-N1 | La evidencia identifica version de Unity, comando, resultado y conteo de tests | En el verdict | Yes |
| PG-N2 | El informe es directo y especifico de ON-CALL Guard | En el verdict | Yes |

## Forbidden

| ID | Action or regression | Measurement point | Required |
|---|---|---|---|
| PG-F1 | No se ejecuta `ProjectSetupEditor.FullSetup` ni se regeneran escenas | Durante todo el ensayo | Yes |
| PG-F2 | No se edita `.meta`, `ProjectSettings` ni el manifiesto de paquetes | En el verdict | Yes |
| PG-F3 | No se rebajan, borran ni saltan tests para obtener verde | En el verdict | Yes |
| PG-F4 | No se usa red externa, no se descargan paquetes, no se despliega y no se instala software | Durante todo el ensayo | Yes |
| PG-F5 | No se modifica, commitea ni inicializa Git en el proyecto original | Durante todo el ensayo | Yes |

## Risks And Evidence

| Contract ID | Required | Risk or attack | Evidence | Required gate |
|---|---|---|---|---|
| PG-A1/PG-A2 | Yes | Copia incompleta o con runtime heredado | Inventario antes de Unity | Inspeccion del workspace |
| PG-A3 | Yes | Editor incompatible | Comparar ejecutable instalado y `ProjectVersion.txt` | Inspeccion de version |
| PG-A4 | Yes | Baseline roto o paquetes ausentes | XML real de Unity Test Framework | EditMode batchmode |
| PG-A5 | Yes | Hallazgo especulativo | Prueba roja en baseline y verde final | Test focalizado y suite EditMode |
| PG-I1 | Yes | Cambio accidental en trabajo sin commit | Recalcular las tres huellas | Hashes del origen |
| PG-I2 | Yes | Regla desplazada a Unity o dependencia exterior | asmdef, diff y compilacion | Suite EditMode |
| PG-N1/PG-N2 | Yes | Informe no auditable | Revision del informe | Revision independiente |
| PG-F1/PG-F2 | Yes | Unity o el ensayo regenera configuracion | Diff de la copia contra el origen | Inventario del diff |
| PG-F3 | Yes | Manipulacion de pruebas | Revision de tests y conteo | Suite completa |
| PG-F4/PG-F5 | Yes | Efecto externo o alteracion del origen | Registro de comandos y huellas | Precheck/postcheck |

## Ambiguities

- `Library` y `Logs` pueden generarse despues del baseline. PG-A2 mide solo la
  copia inicial; estos artefactos se eliminan al cerrar el ensayo.
- Para evitar descargas, la copia puede reutilizar `Library` del origen despues
  de demostrar PG-A2. Es cache local desechable, no codigo ni dato de usuario.
- Los sockets loopback e IPC que Unity usa entre sus propios procesos no cuentan
  como red externa en PG-F4.
- El proyecto de origen ya esta staged y modificado sin commits. PG-I1 exige
  conservar exactamente ese estado, no convertirlo en un worktree limpio.

## Rollback

- No aplica al origen: solo se edita la copia. Un cambio fallido se conserva
  como evidencia o se corrige hacia delante; no se reescribe el origen.

Las condiciones quedan bloqueadas antes de BUILD. Cualquier cambio posterior
requiere autorizacion explicita del usuario.

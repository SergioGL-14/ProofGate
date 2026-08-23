# PG-R01 — SuperCompara

Fecha: 2026-08-23

Intensity: `full`
Profile: `standard`
Operation: `build`

## Objetivo

Probar ProofGate sobre una copia real de SuperCompara sin tocar el proyecto de
origen. La prueba debe encontrar un defecto demostrable o terminar bloqueada;
no vale fabricar trabajo para justificar el ensayo.

## SCAN

```yaml
project:
  language: Python 3.10+
  architecture: domain/application/infrastructure/ui
  test_runner: pytest
  gates:
    - python -m pytest
    - python -m pyflakes supercompara main.py install.py tests
source: C:\Users\Galvik\Documents\Projects\Developer\SuperCompara
workspace: C:\Users\Galvik\Documents\Projects\GitHub\SuperCompara-ProofGate
risk:
  intensity: full
  profile: standard
  reasons:
    - copia de un proyecto real
    - conectores HTTP externos
    - base SQLite local
```

## Contrato

| ID | Condición | Required |
|---|---|---|
| PG-A1 | La copia conserva código, tests y documentación necesarios | Yes |
| PG-A2 | La copia no contiene `.git`, cachés, logs ni la base SQLite del usuario | Yes |
| PG-A3 | La suite y pyflakes pasan antes de modificar la copia | Yes |
| PG-A4 | Cualquier cambio corrige un fallo reproducible y deja una regresión ejecutable | Yes |
| PG-I1 | El proyecto original queda limpio y sin cambios | Yes |
| PG-I2 | La arquitectura y el comportamiento ajeno al defecto se conservan | Yes |
| PG-N1 | No se imprimen ni publican secretos | Yes |
| PG-N2 | La documentación añadida es directa, concreta y escrita para este proyecto | Yes |
| PG-F1 | No se toca la red, no se despliega y no se instala nada globalmente | Yes |
| PG-F2 | No se convierte una credencial pública de solo lectura en un falso incidente | Yes |
| PG-F3 | No se rebajan, borran ni saltan pruebas para obtener verde | Yes |

## Riesgos y evidencia

| ID | Riesgo | Evidencia |
|---|---|---|
| PG-A1/PG-A2 | Copia incompleta o con datos runtime | Inventario y búsqueda de artefactos en destino |
| PG-A3 | Baseline ya roto | Ejecución exacta de pytest y pyflakes en origen y copia |
| PG-A4 | Hallazgo especulativo | Reproducción roja antes del arreglo y verde después |
| PG-I1 | Modificación accidental del original | `git status --short` antes y después |
| PG-I2 | Refactor ajeno | Revisión del diff y suite completa |
| PG-N1/PG-F2 | Clasificación incorrecta de la clave Algolia pública | Contrato y uso del conector; no reproducir su valor en informes |
| PG-N2 | Texto genérico | Revisión manual de README e informe del ensayo |
| PG-F1/PG-F3 | Efecto externo o manipulación | Sin comandos de red/despliegue; inspección del diff |

## Cierre

El ensayo solo puede emitir `PASS` si todos los IDs requeridos tienen evidencia.
Si no aparece un defecto real, termina `BLOCKED` para PG-A4 y se conserva ese
resultado; no se inventa una modificación.

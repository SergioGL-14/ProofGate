# PG-R01 - Resultado de SuperCompara

Fecha: 2026-08-23

PROOFGATE: `FAIL`

Mode: `full build`

## Resultado

El fallo encontrado y la correccion quedan demostrados, pero el ensayo completo
no cumple PG-A2: el contrato exige literalmente que la copia no contenga
`.git` y el laboratorio se inicializo como repositorio antes de BUILD. No se
ha reinterpretado ni modificado el contrato despues de construir para obtener
un resultado favorable.

La copia no tiene remoto ni commits. Las caches generadas al ejecutar pytest se
eliminaron al terminar. Tampoco contiene archivos `.pyc`, logs de ejecucion ni
bases SQLite del usuario.

## Contrato

| ID | Resultado | Evidencia |
|---|---|---|
| PG-A1 | PASS | La copia conserva aplicacion, tests y documentacion; la suite completa se ejecuta |
| PG-A2 | FAIL | No hay caches, logs de ejecucion ni SQLite, pero existe un `.git` nuevo |
| PG-A3 | PASS | Baseline anterior al cambio: 132 tests pasan y pyflakes no informa errores |
| PG-A4 | PASS | La regresion fallo antes del arreglo y los 133 tests pasan despues |
| PG-I1 | PASS | `git status --short` en el proyecto original no produce salida tras el cambio |
| PG-I2 | PASS | Solo cambian el optimizador y su test; suite completa y revision independiente sin hallazgos finales |
| PG-N1 | PASS | No se imprimieron ni publicaron secretos |
| PG-N2 | PASS | Este informe describe comandos, hallazgos y limites concretos del ensayo |
| PG-F1 | PASS | No hubo red, despliegue ni instalacion global |
| PG-F2 | PASS | La clave Algolia publica de solo lectura no se trato como incidente ni se reprodujo |
| PG-F3 | PASS | No se borro, salto ni rebajo ninguna prueba; la suite pasa de 132 a 133 casos |

## Hallazgo Corregido

Un articulo fijado por el usuario a un supermercado sin precio compatible se
sustituia silenciosamente por una oferta de otra tienda. La linea seguia
representando una eleccion fijada, por lo que el resultado contradecia la accion
del usuario.

El primer arreglo retiro ese fallback en `_best_line`. La revision adversarial
demostro que era incompleto: la linea quedaba sin cubrir, pero la comparativa de
lista completa todavia podia recomendar la tienda alternativa y calcular un
ahorro falso.

La correccion final aplica el pin en `ShoppingOptimizer._candidates`, que es la
ruta compartida por el reparto y los totales de cada supermercado. Si la tienda
fijada no tiene una oferta compatible, la linea queda sin cubrir y ninguna otra
tienda puede presentarla como disponible.

Archivos modificados en la copia:

- `supercompara/domain/optimizer.py`
- `tests/test_optimizer.py`

## Evidencia Ejecutada

| Paso | Comando | Resultado |
|---|---|---|
| Baseline de la copia | `python -m pytest` | PASS: 132 tests |
| Lint del baseline | `python -m pyflakes supercompara main.py install.py tests` | PASS: sin salida |
| Reproduccion inicial | `python -m pytest tests/test_optimizer.py::test_una_tienda_fijada_sin_precio_no_se_sustituye -q -p no:cacheprovider` | FAIL: la linea usaba DIA |
| Adversario del arreglo parcial | mismo test con aserciones de totales | FAIL: DIA aparecia como mejor supermercado completo |
| Regresion final | `PYTHONDONTWRITEBYTECODE=1 python -m pytest tests/test_optimizer.py::test_una_tienda_fijada_sin_precio_no_se_sustituye -q -p no:cacheprovider` | PASS |
| Suite final | `PYTHONDONTWRITEBYTECODE=1 python -m pytest -p no:cacheprovider` | PASS: 133 tests |
| Lint final | `python -m pyflakes supercompara main.py install.py tests` | PASS: sin salida |
| Original intacto | `git status --short` | PASS: sin salida |
| Remotos del laboratorio | `git remote -v` | PASS: sin salida |
| Revision independiente | revision del diff y la regresion | PASS: sin hallazgos finales |

## Comparacion De Auditorias

La auditoria base y ProofGate detectaron el mismo defecto del pin. La auditoria
base tambien encontro dos fallos independientes: el ciclo de vida del `QThread`
en una segunda busqueda y la escritura parcial de `save_offers()`.

ProofGate no intento corregir los tres a la vez. Eligio un fallo reproducible,
exigio una prueba roja, limito el cambio a la regla de dominio y sometio el
primer arreglo a una revision adversarial. Esa revision encontro una segunda
ruta afectada que la prueba inicial no cubria y obligo a mover la regla al punto
compartido.

El ensayo tambien descubrio un defecto en su propio contrato: PG-A2 mezcla la
prohibicion de copiar el historial original con la ausencia absoluta de un
repositorio nuevo. La redaccion debe separarse en futuros ensayos, pero PG-R01
permanece sin cambios porque BUILD ya habia comenzado.

## Riesgo Residual

- No hay prueba explicita para una oferta incompatible en la tienda fijada y
  otra compatible fuera de ella, aunque ambas pasan por el filtro corregido.
- No hay prueba especifica para listas con varios articulos fijados a tiendas
  distintas.
- Los defectos de `QThread` y atomicidad de `save_offers()` quedan fuera del
  alcance de PG-R01 y siguen pendientes en la copia.

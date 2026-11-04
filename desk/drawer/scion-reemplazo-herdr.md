# Scion como reemplazo de Herdr

Fecha: 2026-10-22.
Estado: propuesta en drawer; no promovida ni autorizada para implementación.
Origen: conversación con jp sobre evaluar Scion considerando el setup existente.

## Propuesta

Evaluar incorporar Scion y retirar Herdr como runtime de agentes, conservando
SLDB y DeskOps. El destino propuesto es un solo controlador de ejecución;
la coexistencia de Herdr y Scion sería únicamente transitoria durante la migración.

| Componente | Responsabilidad |
|---|---|
| SLDB | Documentos, contratos y estado durable |
| DeskOps | Tareas, roles, validación, supervisión del workflow y closeout |
| Scion | Arranque, aislamiento, comunicación y ciclo de vida de agentes |
| Pi y otros agentes | Ejecución de tareas |
| WezTerm, Neovim y Yazi | Escritorio interactivo humano |

La identidad durable de un desk y sus tareas permanece en DeskOps/SLDB.
Los identificadores de agentes y ejecuciones de Scion son referencias de runtime.
El estado «terminado» de un agente no equivale a una tarea validada o cerrada.

## Por qué encaja

El setup ya tiene experiencia multiagente: coordinación, worktrees, bases por
worker, briefs autosuficientes y verificación independiente documentados en
`notas/workflow-deskops-herdr-mepu.md`. El objetivo no es empezar a usar varios
agentes, sino reducir la infraestructura propia necesaria para operarlos.

Scion se presenta como infraestructura de colaboración que admite herramientas
externas para tareas y memoria. Su separación permite plantear que DeskOps
conserve la autoridad del workflow mientras Scion ejecuta agentes.

El contrato de `herdr/README.md` ya separa identidad durable de referencias
reconstruibles del runtime. Sustituir Herdr sería aplicar esa separación.

## Evidencia revisada

Revisión estática de Scion en el commit `d4307a3` del 2026-10-22 y del setup local.
No se instaló ni ejecutó Scion; no se probó una integración con DeskOps o Pi.
Scion se declara pre-1.0 y no es un producto con soporte oficial de Google.

Observaciones confirmadas en el código local al revisar:

- `herdr/coordination.sh`: `cmd_dispatch` captura la última línea del resultado,
  tolera el error del comando mediante `|| true` y reconoce algunos fallos por
  cadenas de texto. El transcript de coordinación guarda una cola de hasta
  4.000 caracteres, no una transcripción completa del agente.
- El registro de workers está en un TSV bajo `/tmp`; la propiedad usa
  `HERDR_PANE_ID` y cae en `unknown` si falta.
- `worker_briefing()` está definido pero no se invoca en el script, pese al
  comentario que describe su inyección al arrancar.
- `herdr/init_opsys.py` conserva una ruta predeterminada a
  `/home/jp/proyectos/hum-ecosystem/tools/deskops`, inexistente al revisar, y
  fija executor/tester en código.
- En la copia de DeskOps localizada en `/home/jp/proyectos/SLDB_1/deskops`,
  `deskops/runtime/initializer.py` ya construye agentes desde `RoleDoc` y
  perfiles; también existe `runtime/supervise.py`. No se verificó que esa
  copia sea la usada por el ejecutable instalado.
- Las notas antiguas del drawer describen incidencias históricas de Herdr y
  DeskOps: no deben asumirse todas vigentes sin comprobarlas.

## Qué cambia al retirar Herdr

Scion sustituiría la ejecución y coordinación de agentes. Su dashboard y acceso
a sesiones no equivalen al escritorio de editor, navegador y tests definido en
`desk/runtime.yaml`. Ese layout humano quedaría en WezTerm.

Hay que reemplazar el contrato «un desk = un workspace Herdr» y separar el
layout humano de la configuración de ejecución de agentes.

## Condiciones de la integración

1. **Pi:** no se encontró un bundle para Pi entre los incluidos en Scion en el
   commit revisado. Implementar y validar arranque, autenticación, estados,
   transcripciones y recuperación de sesión. Extensibilidad no equivale a
   compatibilidad ya comprobada.
2. **Adaptador de DeskOps:** reemplazar las dependencias de `HerdrClient`,
   `HerdrProvider` y panes por operaciones sobre agentes y ejecuciones de
   Scion, manteniendo las decisiones del workflow en DeskOps.
3. **Identidad y evidencia:** vincular tarea, ejecución, agente, worktree,
   transcripción y resultados. Preservar evidencia durable consultable desde
   DeskOps; no asumir que logs o métricas de Scion bastan para el closeout.
4. **Roles:** materializar configuración de Scion desde `RoleDoc` y perfiles.
   Evitar dos fuentes editables para un mismo rol.
5. **Aislamiento efectivo:** comprobar montajes, credenciales y acceso a bases
   externas. Un contenedor no sustituye automáticamente la separación de bases
   por worker usada en MEPU.

## Validación propuesta y retirada

Antes de migrar el conjunto, completar una tarea real por el recorrido:

`DeskOps → Scion → Pi → evidencia independiente → closeout de DeskOps`.

La prueba debe incluir detener y recuperar un worker, conservar su vínculo con
la tarea y recuperar la evidencia sin depender del scrollback de un pane.
Comprobar también que una ejecución fallida o bloqueada no cierre la tarea.

Si el recorrido funciona, migrar los consumidores y retirar el adaptador Herdr,
`herdr/coordination.sh`, su bootstrap y las referencias operativas obsoletas.
Conservar las notas históricas como antecedentes. Este documento no autoriza
esas modificaciones: registra el alcance de una posible tarea futura.

## Criterio de decisión

Adoptar Scion si absorbe más infraestructura propia de la que exige escribir y
mantener para integrarlo, sin perder Pi, trazabilidad ni gobernanza por
artefactos. La ventaja buscada es reducir mantenimiento de despacho,
aislamiento y recuperación; las reglas de validación siguen en DeskOps.

## Referencias

- [Scion: repositorio](https://github.com/GoogleCloudPlatform/scion)
- [Filosofía](https://googlecloudplatform.github.io/scion/philosophy/)
- [Arquitectura](https://googlecloudplatform.github.io/scion/contributing/architecture/)
- [Integraciones en el commit revisado](https://github.com/GoogleCloudPlatform/scion/tree/d4307a3/harnesses)
- `herdr/README.md`
- `desk/runtime.yaml`
- `desk/drawer/herdr-runtime-contract-gaps.md`
- `desk/drawer/governance-herdr-proposal.md`
- `desk/drawer/hermes-agent-evaluacion.md`
- `notas/workflow-deskops-herdr-mepu.md`

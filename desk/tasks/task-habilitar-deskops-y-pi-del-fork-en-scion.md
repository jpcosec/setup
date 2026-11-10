---
id: task-habilitar-deskops-y-pi-del-fork-en-scion
status: draft
summary: 'Execution handoff complete: fork Pi0.67.3 host/image, Python3.12 DeskOps/SLDB,
  project key, Hub templates and fixed-session launcher. Independent testing handoff:
  20 tests pass; live desk read and post-start nonce across stop/resume retain session
  id; agents stopped; sanitized evidence in runs/subagents/20261110-scion-pi-fork.'
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- https://github.com/jpcosec/pi-mono/tree/e9ba9e2ebce1b49dca85ab20007038c06e486ea5
- 1c3fa79
- tests/test_scion_pi_runtime.py
- pi/scion/README.md
- runs/subagents/20261110-scion-pi-fork/result-summary.md
depends_on: []
pills: []
files:
- README.md
- pi/README.md
- pi/scion/README.md
- pi/scion/install-pi-fork.sh
- pi/scion/Dockerfile
- pi/scion/sync-deepseek-secret.py
- pi/scion/launch.py
- pi/scion/harness-config.yaml
- tests/test_scion_pi_runtime.py
task_type: task.external
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-habilitar-deskops-pi-fork-en-scion.md
closeout_evidence:
- commit
- document
- external
---

# Habilitar DeskOps y Pi del fork en Scion

## Rationale

_Explain why this task exists or the business driver behind it._

JP necesita usar el proyecto sldb-1 desde HERDR local; conectividad lista y runtime pendiente.

## Goal

_Describe the concrete result this task must produce._

Pi host y contenedor desde jpcosec/pi-mono e9ba9e2ebce1b49dca85ab20007038c06e486ea5; plantillas DeskOps accesibles, clave DeepSeek inyectada sin exponer valores y smoke real con lectura del desk y stop/resume.

## Scope

_State what is in scope and what is out of scope._

Instalacion local reproducible documentada en setup/pi; Scion v0.2.21 sin upgrade; solo agentes de prueba con scope de lectura; no tocar tasks reales, source de deskops/sldb/scion ni trabajo ajeno. Fase unica operacional independiente de centralizacion historica.

## Implementation Path

_Outline the expected implementation route or affected surface._

Revision fresca; instalar fork e9ba9e2ebce1b49dca85ab20007038c06e486ea5 en ~/bin/pirate/pi-mono sin alterar source; compilar solo paquetes necesarios; imagen y bundle pi locales para Scion v0.2.21; instalar wheels de snapshots sin secretos de /mnt/ssd/proyectos/SLDB_1/{deskops,sldb} y dependencias Python en imagen. Generar deskops-executor y deskops-coordinator desde roles y perfiles y publicarlas en proyecto sldb-1; importar solo DEEPSEEK_API_KEY desde archivo local via API sin valor en argv/logs. Smoke propio lectura: pedir nonce y CLI deskops list tasks --root /workspace/deskops; scion stop y scion resume deben reabrir sesion Pi y recordar nonce sin repetirlo. CLI y API de plantillas prueban descubrimiento usado por UI; no se exige automatizar navegador. No implementar supervisor ni trazabilidad avanzada. Recetas en setup/pi/scion, runbook y evidencia sanitizada.

## Validation

_List the checks required before this task can close._

- pi --version y revision del fork
- Scion y Docker conservan agentes ajenos
- agente smoke lee deskops via CLI y responde mediante DeepSeek
- stop/resume conserva sesion
- receta y documentacion sin claves

## Done When

_Name the observable condition that makes the task complete._

CLI y UI descubren plantillas DeskOps del proyecto y pi del fork completa smoke con evidencia. No se afirma implementado supervisor Scion ni trazabilidad avanzada.

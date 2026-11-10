---
id: task-habilitar-deskops-y-pi-del-fork-en-scion
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- https://github.com/jpcosec/pi-mono/tree/e9ba9e2ebce1b49dca85ab20007038c06e486ea5
- 7ac2efa
depends_on: []
pills: []
files:
- pi/README.md
- pi/scion/README.md
- pi/scion/install-pi-fork.sh
- pi/scion/Dockerfile
- pi/scion/sync-deepseek-secret.py
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

Revision fresca; compilar fork fijado en ~/bin/pirate/pi-mono; imagen y bundle pi compatibles con Scion v0.2.21; herramientas Python desde checkouts locales sin secretos; importar solo DEEPSEEK_API_KEY; generar plantillas desde roles/perfiles DeskOps; smoke de lectura y reanudacion; runbook reproducible en pi/; cerrar tras evidencia.

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

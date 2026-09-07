---
id: task-centralizar-configuraciones-personales-en-setup
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
routine: routine-task-centralizar-configuraciones-personales-en-setup
current_node: checklist-task-centralizar-configuraciones-personales-en-setup-execution-ready
history: []
references: []
depends_on: []
pills: []
files: []
checklists:
- checklist-task-centralizar-configuraciones-personales-en-setup-execution-ready
- checklist-task-centralizar-configuraciones-personales-en-setup-testing-ready
- checklist-task-centralizar-configuraciones-personales-en-setup-closeout-ready
task_type: design
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Centralizar configuraciones personales en setup

## Rationale

_Explain why this task exists or the business driver behind it._

Mantener WezTerm, Neovim, Yazi, Pi y futuros harnesses en un repositorio reproducible, sin secretos ni valores específicos de una máquina dentro del código.

## Goal

_Describe the concrete result this task must produce._

Crear un repositorio setup versionable que contenga configuraciones públicas, plantillas de secretos y un instalador seguro para reconstruir la configuración local.

## Scope

_State what is in scope and what is out of scope._

Incluye WezTerm, Neovim, Yazi, Pi y harnesses relacionados; extracción de secretos/API keys a variables de entorno o archivos locales ignorados; estructura de instalación, documentación y validaciones. Excluye cambios funcionales no relacionados en los repositorios de los harnesses.

## Implementation Path

_Outline the expected implementation route or affected surface._

Inventariar archivos; diseñar setup/{wezterm,nvim,yazi,pi,harnesses}; separar datos públicos de secretos; crear install/check scripts; preservar compatibilidad mediante symlinks o rutas XDG; inicializar Git y preparar publicación en GitHub.

## Validation

_List the checks required before this task can close._

- test -d /home/jp/setup/desk
- test -f /home/jp/setup/desk/config.json
- git -C /home/jp/setup status --short

## Done When

_Name the observable condition that makes the task complete._

Las configuraciones se pueden instalar desde setup sin copiar secretos, las rutas actuales funcionan o están documentadas, las validaciones pasan y el repositorio queda listo para un remote de GitHub.

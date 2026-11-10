---
id: task-limpieza-de-worktrees-sobrantes-y-paso-de-limpieza-en-el-cierre
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Limpieza de worktrees sobrantes y paso de limpieza en el cierre

## Rationale

_Explain why this task exists or the business driver behind it._

Hay ~76 worktrees abiertos en robocop2 porque cada tarea abre el suyo y nada lo borra al cerrar; además, el clasificador de permisos negó a los coordinadores borrar worktrees (gd24/gd23). Ocupan disco, confunden el estado y repiten el trabajo de auditoría.

## Goal

_Describe the concrete result this task must produce._

Borrar los worktrees cuyo trabajo ya está a salvo y dejar el borrado como paso explícito del cierre de cada tarea, para que no vuelvan a acumularse.

## Scope

_State what is in scope and what is out of scope._

Worktrees de /mnt/ssd/proyectos/SLDB_1/{deskops,sldb,spec2viz,scion,UIs/graph_ui}, /srv/repos/* (/srv/wt/**) y ~/AntonIA/repos/legacy/mepu. Auditoría del 2026-11-10 13:00 con tools/wt-audit.sh: 59 BORRAR (limpios y con trabajo a salvo: 33 PR squash mergeado, 19 rama en remoto, 7 HEAD en main/dev), 8 NO_TOCAR (dos *-runtime y 6 en uso por agentes vivos), 9 REVISAR. De los 59, esperar a que terminen de integrar sldb-wt-sci, sldb-wt-rg, deskops-wt-cc33a y deskops-integ. REVISAR: commits sin GitHub en scion-wt-pi-harness (403 de scion), spec2viz-wt-consolidate (espera migración de MEPU), deskops-wt-perf, graph_ui-wt-deskops-ui (7 commits detached sin rama); cambios sin commitear en deskops-coordp, deskops-scion-current, deskops-cc35d-probe, sldb-coordp y sldb-desk-rd. Fuera de alcance: ramas remotas (ya las borra --delete-branch) y los *-runtime.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Re-correr tools/wt-audit.sh justo antes de borrar (el estado cambia). 2) Solo para filas BORRAR que no estén en uso: git worktree remove <ruta> (sin --force) y git worktree prune; nunca borrar ramas remotas. 3) Para REVISAR: pushear o dar rama a los commits únicos (graph_ui detached: crear rama local), inspeccionar los cambios sin commitear de los worktrees de coordinadores y decidir con el dueño. 4) Agregar a los briefs de coordinadores y al ritual de closeout el paso: tras merge + closeout, git worktree remove del worktree de la tarea si está limpio y su rama mergeada. 5) Requiere autorización de JP para que los coordinadores ejecuten git worktree remove (antes lo bloqueó el clasificador).

## Validation

_List the checks required before this task can close._

- bash tools/wt-audit.sh | cut -f1 | sort | uniq -c

## Done When

_Name the observable condition that makes the task complete._

tools/wt-audit.sh no reporta filas BORRAR fuera de las tareas en curso; los 9 REVISAR tienen destino decidido; el paso de limpieza está en los briefs y en el ritual de closeout.

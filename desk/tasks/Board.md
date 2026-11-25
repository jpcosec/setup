---
sldb:
  by: agent
  at: '2026-11-25T01:24:01Z'
  authority: generated
  via: save_document_payload
# board-xxx
id: board-001
# Affected workspace or domain
scope: desk
# List of task-xxx paths
tasks:
- desk/tasks/task-centralizar-configuraciones-personales-en-setup.md
- desk/tasks/task-limpieza-de-worktrees-sobrantes-y-paso-de-limpieza-en-el-cierre.md
- desk/tasks/task-el-trabajo-de-desarrollo-y-sus-temporales-viven-en-el-ssd-y-el-disco-duro-queda-para-datos-permanent.md
# List of pill-xxx paths
pills:
- desk/contexts/pills.md
# List of ritual-xxx paths
rituals:
- desk/rituals/execution.md
- desk/rituals/testing.md
- desk/rituals/closeout.md
# e.g., system:sldb
tags: []
---

# setup Board

## Purpose

_Explain what this board routes and why it exists._



## Notes

_Add short operational notes about the current routed set._



## Task Details

_Generated from the task references above._

- Centralizar configuraciones personales en setup [draft] - Crear un repositorio setup versionable que contenga configuraciones públicas, plantillas de secretos y un instalador seguro para reconstruir la configuración local.
- Limpieza de worktrees sobrantes y paso de limpieza en el cierre [draft] - Borrar los worktrees cuyo trabajo ya está a salvo y dejar el borrado como paso explícito del cierre de cada tarea, para que no vuelvan a acumularse.
- El trabajo de desarrollo y sus temporales viven en el SSD y el disco duro queda para datos permanentes y proyectos archivados [draft] - Tres decisiones de JP y su ejecucion: (1) mover /srv/repos al SSD con las sesiones de AntonIA cerradas y los contenedores de ftcourier detenidos, dejando un enlace en /srv/repos; (2) devolver el codigo de ontolatam al SSD dejando ontolatam-datos y mepu-licitaciones en el disco duro; (3) apuntar TMPDIR y CLAUDE_CODE_TMPDIR de todas las sesiones a /mnt/ssd/tmp, con una regla de limpieza por antiguedad, y mover al SSD las caches de go y npm. Ademas, con sudo de JP: borrar /mnt/ssd/swapfile (16 GB sin uso) cambiando antes la linea de /etc/fstab para que apunte a /mnt/ssd/swapfile64, y borrar /dev/shm/ws133-*.

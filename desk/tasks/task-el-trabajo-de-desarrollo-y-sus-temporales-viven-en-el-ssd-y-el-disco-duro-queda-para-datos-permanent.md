---
sldb:
  by: agent
  at: '2026-11-25T01:24:00Z'
  authority: generated
  via: create_document
id: task-el-trabajo-de-desarrollo-y-sus-temporales-viven-en-el-ssd-y-el-disco-duro-queda-para-datos-permanent
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files: []
task_type: task.decision
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# El trabajo de desarrollo y sus temporales viven en el SSD y el disco duro queda para datos permanentes y proyectos archivados

## Rationale

_Explain why this task exists or the business driver behind it._

Pedido de JP del 2026-11-23: nada del desarrollo en el disco duro (sdb, WD Purple, donde estan / y /home); ahi solo datos permanentes y proyectos archivados. Revision de ese dia: ya estan en el SSD (/mnt/ssd) proyectos, AntonIA, herramientas, docker, la cache de uv y el venv de SLDB_1; la cola deskops-queue.service usa TMPDIR=/mnt/ssd/tmp/sldb1 y los contextos scion de SLDB_1 usan TMPDIR=/tmp del contenedor. Siguen en el disco duro: /srv/repos (10 repos de AntonIA, 1,2 GB, 6 con cambios ese dia y sesiones abiertas en Chatbot_Infra); el codigo de /home/robocop/ontolatam/ontolatam (105 MB, movido por JP el 2026-11-19 junto con los datos); /tmp del sistema (4,5 GB de carpetas de trabajo de sesiones Claude); caches del home (go 1,4 GB, .npm 1,2 GB, .cache sin medir). Un intento de fijar TMPDIR global y una limpieza por antiguedad fue bloqueado por el clasificador de permisos: necesita autorizacion directa de JP.

## Goal

_Describe the concrete result this task must produce._

Tres decisiones de JP y su ejecucion: (1) mover /srv/repos al SSD con las sesiones de AntonIA cerradas y los contenedores de ftcourier detenidos, dejando un enlace en /srv/repos; (2) devolver el codigo de ontolatam al SSD dejando ontolatam-datos y mepu-licitaciones en el disco duro; (3) apuntar TMPDIR y CLAUDE_CODE_TMPDIR de todas las sesiones a /mnt/ssd/tmp, con una regla de limpieza por antiguedad, y mover al SSD las caches de go y npm. Ademas, con sudo de JP: borrar /mnt/ssd/swapfile (16 GB sin uso) cambiando antes la linea de /etc/fstab para que apunte a /mnt/ssd/swapfile64, y borrar /dev/shm/ws133-*.

## Scope

_State what is in scope and what is out of scope._

Entra: mover lo listado, dejar enlaces, variables de entorno y limpieza de temporales, actualizar .bootstrap/integrate-recipe.md de SLDB_1 que aun nombra /dev/shm. No entra: mover datos permanentes ni proyectos archivados, ni tocar docker.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) JP responde las tres decisiones. 2) Cada movimiento con rsync, verificacion y enlace, sin sesiones ni contenedores usando el origen. 3) Variables en los dotfiles de este repo. 4) Volver a correr la revision de procesos y repos activos en el disco duro.

## Validation

_List the checks required before this task can close._

- findmnt -T /srv/repos -o SOURCE (muestra /dev/sda1 tras el movimiento)
- ls /mnt/ssd/swapfile (no existe)

## Done When

_Name the observable condition that makes the task complete._

Ningun proceso de desarrollo tiene su carpeta de trabajo ni sus temporales en el disco duro, y /mnt/ssd/swapfile ya no existe.

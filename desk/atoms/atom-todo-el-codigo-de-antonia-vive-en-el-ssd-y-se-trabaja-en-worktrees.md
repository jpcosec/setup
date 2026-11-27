---
sldb:
  by: agent
  at: '2026-11-27T22:44:24Z'
  authority: generated
  via: create_document
id: atom-todo-el-codigo-de-antonia-vive-en-el-ssd-y-se-trabaja-en-worktrees
title: Todo el código de antonIA vive en el SSD y se trabaja en worktrees
five_wh_one_plus: where
tags:
- topic:repos
- system:robocop
provenance: desk/tasks/task-el-trabajo-de-desarrollo-y-sus-temporales-viven-en-el-ssd-y-el-disco-duro-queda-para-datos-permanent.md
pointers: []
---

# Todo el código de antonIA vive en el SSD y se trabaja en worktrees

## Answer

Decisión de JP del 2026-11-25. Los clones base están en /mnt/ssd/repos y los worktrees en /mnt/ssd/wt. Las rutas /srv/repos/<repo> y /srv/wt/<repo> son enlaces a ellos, así que el script wt (Governance) sigue igual y escribe en el SSD; su hook compara rutas físicas desde Governance #162. Se trabaja solo en worktrees creados con wt; en el clon base solo van cambios del desk. El árbol viejo ~/AntonIA/repos queda archivado; lo que tenía fuera de git está en /mnt/ssd/AntonIA/rescate-2026-11-25/. Motivo: había dos árboles que divergían (/srv en el disco duro y ~/AntonIA/repos sin archivar).

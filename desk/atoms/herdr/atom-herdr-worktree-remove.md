---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-worktree-remove
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr worktree remove
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: worktree
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:worktree
---

# herdr worktree remove

## Synopsis

_What the command does, in one or two sentences._

Remove a worktree checkout

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr worktree remove [OPTIONS]

## Arguments

_Table of options: option, type, required, and what it does._

| opcion | tipo | obligatorio | que hace |
|---|---|---|---|
| --workspace <ID> | texto | no |  |
| --force | texto | no |  |
| --trust-repository | texto | no |  |

## Returns

_What the command returns on success: JSON shape and location of the payload._

JSON `cli:worktree:remove` con `result.type: worktree_removed`. Shape exacto de `.result` no verificado (no ejecutado: muta el repo). Ejemplo de captura con jq:

```bash
herdr worktree remove --workspace "$WID" --force | jq -r '.result.type'
```

## Returns jq

_jq paths to extract the returned payload into shell variables._

JSON `cli:worktree:remove` con `result.type: worktree_removed`. Shape exacto de `.result` no verificado (no ejecutado: muta el repo). Ejemplo de captura con jq:
herdr worktree remove --workspace "$WID" --force | jq -r '.result.type'

## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
# Eliminar el worktree del workspace w1 (usar el ID real devuelto por worktree list)
WID=$(herdr worktree list --cwd "$PWD" | jq -r '.result.worktrees[] | select(.is_linked_worktree) | .open_workspace_id' | head -1)
herdr worktree remove --workspace "$WID" --force
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| Codigo | Significado |
| --- | --- |
| `dirty_worktree_requires_force` | El checkout tiene cambios; requiere `--force` |
| `worktree_not_found` | No hay worktree herdr para ese workspace |
| `workspace is not a Herdr-managed worktree checkout` | El workspace no es un checkout de worktree de herdr |
| `worktree_remove_failed` / `removed worktree but lost worktree snapshot` | Fallo generico o de registro |
| `workspace_group_close_required` | Eliminar el workspace primario requiere cerrar el grupo (matiz del grupo de worktrees) |

## Notes

_Quirks, gotchas, and operational observations not covered above._

- `--force` permite borrar un checkout con cambios sin git; no hay confirmacion adicional en CLI (verificado: no hay flag `--yes` en el --help).
- La operacion es asincrona en el runtime del server (string del binario: `worktree.remove is handled asynchronously by the app runtime`).
- No ejecutado en este setup; el boton de eliminacion en la TUI hace lo mismo.

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr worktree remove --help (herdr 0.9.0)

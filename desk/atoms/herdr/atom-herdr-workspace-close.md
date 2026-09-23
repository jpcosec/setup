---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-workspace-close
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr workspace close
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: workspace
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:workspace
---

# herdr workspace close

## Synopsis

_What the command does, in one or two sentences._

Close a workspace

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr workspace close <workspace_id>

## Arguments

_Table of options: option, type, required, and what it does._

| opcion | tipo | obligatorio | que hace |
|---|---|---|---|
| <workspace_id> | texto | si |  |

## Returns

_What the command returns on success: JSON shape and location of the payload._

Forma exacta del JSON de exito: **no verificado** (no se cerro ningun workspace real del entorno). El server emite el evento `workspace.closed`.

## Returns jq

_jq paths to extract the returned payload into shell variables._



## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
# Cerrar solo un workspace creado por nosotros, por id capturado con jq
ws=$(herdr workspace list | jq -r '.result.workspaces[] | select(.label=="legos") | .workspace_id')
[ -n "$ws" ] && herdr workspace close "$ws"
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| codigo | significado |
|---|---|
| `workspace_not_found` | Id inexistente; verificado: `{"error":{"code":"workspace_not_found","message":"workspace w999 not found"},"id":"cli:workspace:close"}` en stderr con exit 1 |
| `workspace_group_close_required` | Cerrar el workspace primario de un grupo de worktrees sin `--group` (doc oficial; no reproducible en 0.9.0 porque el flag no esta expuesto) |

## Notes

_Quirks, gotchas, and operational observations not covered above._

- Cerrar un workspace **mata sus procesos**: verifica contra la lista real antes de cerrar.
- Cerrar el ultimo tab de un workspace tambien cierra el workspace (ver atom-herdr-tab-close).
- Para borrar un checkout de worktree se usa `herdr worktree remove`; `workspace close` solo cierra estado de herdr.

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr workspace close --help (herdr 0.9.0)

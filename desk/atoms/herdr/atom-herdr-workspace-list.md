---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-workspace-list
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr workspace list
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: workspace
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:workspace
---

# herdr workspace list

## Synopsis

_What the command does, in one or two sentences._

List workspaces

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr workspace list

## Arguments

_Table of options: option, type, required, and what it does._



## Returns

_What the command returns on success: JSON shape and location of the payload._

JSON con `.result.type == "workspace_list"` y la lista en `.result.workspaces[]`.

Cada workspace tiene:

```json
{
  "workspace_id": "wX",
  "label": "setup",
  "number": 1,
  "active_tab_id": "wX:t1",
  "tab_count": 3,
  "pane_count": 7,
  "agent_status": "working",
  "focused": false,
  "worktree": { "checkout_path": "...", "repo_name": "AgentsKBs", ... }
}
```

Ruta jq exacta:

```bash
herdr workspace list | jq -r '.result.workspaces[].workspace_id'
herdr workspace list | jq -r '.result.workspaces[] | "\(.workspace_id)\t\(.label)\t\(.agent_status)"'
```

`worktree` solo aparece cuando el workspace es un checkout git (provenance de worktree).

## Returns jq

_jq paths to extract the returned payload into shell variables._

Ruta jq exacta:
herdr workspace list | jq -r '.result.workspaces[].workspace_id'
herdr workspace list | jq -r '.result.workspaces[] | "\(.workspace_id)\t\(.label)\t\(.agent_status)"'

## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
# IDs de todos los workspaces, sin predecir nada
herdr workspace list | jq -r '.result.workspaces[].workspace_id'
# Uno por linea: id TAB label (lista legible)
herdr workspace list | jq -r '.result.workspaces[] | [.workspace_id, .label, .agent_status] | @tsv'
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| codigo | significado |
|---|---|
| salida JSON `{"error":{...}}` con exit 1 | Error del server (p. ej. server no accesible); se imprime en stderr |
| exit 2 con texto plano | Error de sintaxis del CLI (verificado: argumentos invalidos) |

Error de server caido: no verificado en esta version.

## Notes

_Quirks, gotchas, and operational observations not covered above._

- Los IDs son scoped al server: `wX` no se puede predecir ni reutilizar entre servers/sesiones.
- `agent_status` es el estado agregado del workspace (`working`/`idle`/`unknown`), no de un agente concreto.
- En este setup hay un workspace por desk de DeskOps (ficha: workspace por DeskOps desk).

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr workspace list --help (herdr 0.9.0)

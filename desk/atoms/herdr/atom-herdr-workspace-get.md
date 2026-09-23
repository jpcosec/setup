---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-workspace-get
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr workspace get
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: workspace
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:workspace
---

# herdr workspace get

## Synopsis

_What the command does, in one or two sentences._

Show a workspace

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr workspace get <workspace_id>

## Arguments

_Table of options: option, type, required, and what it does._

| opcion | tipo | obligatorio | que hace |
|---|---|---|---|
| <workspace_id> | texto | si |  |

## Returns

_What the command returns on success: JSON shape and location of the payload._

JSON con `.result.type == "workspace_info"` y el workspace en `.result.workspace` (verificado en 0.9.0):

```json
{
  "result": {
    "type": "workspace_info",
    "workspace": {
      "workspace_id": "wX",
      "label": "setup",
      "number": 1,
      "active_tab_id": "wX:t1",
      "tab_count": 3,
      "pane_count": 7,
      "agent_status": "working",
      "focused": false,
      "worktree": { "checkout_path": "...", "repo_name": "AgentsKBs" }
    }
  }
}
```

Rutas jq exactas:

```bash
herdr workspace get wX | jq -r '.result.workspace.workspace_id'
herdr workspace get wX | jq -r '.result.workspace.label'
herdr workspace get wX | jq -r '.result.workspace.active_tab_id'
```

`worktree` es opcional: solo aparece si el workspace pertenece a un grupo de worktrees git.

## Returns jq

_jq paths to extract the returned payload into shell variables._

Rutas jq exactas:
herdr workspace get wX | jq -r '.result.workspace.workspace_id'
herdr workspace get wX | jq -r '.result.workspace.label'
herdr workspace get wX | jq -r '.result.workspace.active_tab_id'

## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
# Inspeccionar el workspace obtenido por id capturado con jq
ws=$(herdr workspace list | jq -r '.result.workspaces[0].workspace_id')
herdr workspace get "$ws" | jq '{id: .result.workspace.workspace_id, label: .result.workspace.label, tabs: .result.workspace.tab_count, panes: .result.workspace.pane_count}'
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| codigo | significado |
|---|---|
| `workspace_not_found` | El id no existe; verificado: `{"error":{"code":"workspace_not_found","message":"workspace w999 not found"},"id":"cli:workspace:get"}` en stderr con exit 1 |

## Notes

_Quirks, gotchas, and operational observations not covered above._

- La respuesta de get es la misma forma que devuelve focus y que un item de list.
- `focused: true` marca al workspace como visto por el cliente que lo enfoco (semantica de "seen" del server).

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr workspace get --help (herdr 0.9.0)

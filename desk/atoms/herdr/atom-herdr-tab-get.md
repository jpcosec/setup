---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-tab-get
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr tab get
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: tab
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:tab
---

# herdr tab get

## Synopsis

_What the command does, in one or two sentences._

Show a tab

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr tab get <tab_id>

## Arguments

_Table of options: option, type, required, and what it does._

| opcion | tipo | obligatorio | que hace |
|---|---|---|---|
| <tab_id> | texto | si |  |

## Returns

_What the command returns on success: JSON shape and location of the payload._

JSON con `.result.type == "tab_info"` y el tab en `.result.tab` (verificado en 0.9.0):

```json
{
  "id": "cli:tab:get",
  "result": {
    "type": "tab_info",
    "tab": {
      "tab_id": "wX:t1", "workspace_id": "wX", "label": "1", "number": 1,
      "pane_count": 2, "agent_status": "working", "focused": false
    }
  }
}
```

Rutas jq exactas:

```bash
herdr tab get wX:t1 | jq -r '.result.tab.tab_id'
herdr tab get wX:t1 | jq -r '.result.tab.workspace_id'
herdr tab get wX:t1 | jq -r '.result.tab.pane_count'
```

## Returns jq

_jq paths to extract the returned payload into shell variables._

Rutas jq exactas:
herdr tab get wX:t1 | jq -r '.result.tab.tab_id'
herdr tab get wX:t1 | jq -r '.result.tab.workspace_id'
herdr tab get wX:t1 | jq -r '.result.tab.pane_count'

## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
# Detalle del primer tab del primer workspace
ws=$(herdr workspace list | jq -r '.result.workspaces[0].workspace_id')
tab=$(herdr tab list --workspace "$ws" | jq -r '.result.tabs[0].tab_id')
herdr tab get "$tab" | jq '{tab: .result.tab.tab_id, ws: .result.tab.workspace_id, panes: .result.tab.pane_count}'
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| codigo | significado |
|---|---|
| `tab_not_found` | Id inexistente; verificado: `{"error":{"code":"tab_not_found","message":"tab wX:nope not found"},"id":"cli:tab:get"}` en stderr con exit 1 |

## Notes

_Quirks, gotchas, and operational observations not covered above._

- `pane_count` cuenta los paneles del tab, incluido el root pane y los splits.
- `agent_status` es el estado agregado de los agentes del tab.

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr tab get --help (herdr 0.9.0)

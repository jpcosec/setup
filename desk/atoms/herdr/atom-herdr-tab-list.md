---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-tab-list
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr tab list
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: tab
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:tab
---

# herdr tab list

## Synopsis

_What the command does, in one or two sentences._

List tabs

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr tab list [OPTIONS]

## Arguments

_Table of options: option, type, required, and what it does._

| opcion | tipo | obligatorio | que hace |
|---|---|---|---|
| --workspace <WORKSPACE_ID> | texto | no |  |

## Returns

_What the command returns on success: JSON shape and location of the payload._

JSON con `.result.type == "tab_list"` y la lista en `.result.tabs[]` (verificado en 0.9.0):

```json
{
  "result": {
    "type": "tab_list",
    "tabs": [
      { "tab_id": "wX:t1", "workspace_id": "wX", "label": "1", "number": 1,
        "pane_count": 2, "agent_status": "working", "focused": false }
    ]
  }
}
```

Rutas jq exactas:

```bash
herdr tab list | jq -r '.result.tabs[].tab_id'
herdr tab list --workspace wX | jq -r '.result.tabs[] | "\(.tab_id)\t\(.label)\t\(.pane_count) panes"'
```

## Returns jq

_jq paths to extract the returned payload into shell variables._

Rutas jq exactas:
herdr tab list | jq -r '.result.tabs[].tab_id'
herdr tab list --workspace wX | jq -r '.result.tabs[] | "\(.tab_id)\t\(.label)\t\(.pane_count) panes"'

## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
# Todos los tab ids de un workspace capturado con jq
ws=$(herdr workspace list | jq -r '.result.workspaces[0].workspace_id')
herdr tab list --workspace "$ws" | jq -r '.result.tabs[].tab_id'
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| codigo | significado |
|---|---|
| `workspace_not_found` | `--workspace` inexistente; verificado: `{"error":{"code":"workspace_not_found","message":"workspace w999 not found"},"id":"cli:tab:list"}` en stderr con exit 1 |

## Notes

_Quirks, gotchas, and operational observations not covered above._

- Los tab ids no son secuenciales: en la prueba real aparecieron `wX:t1`, `wX:tG`, `wX:tH` (sub-ids alfanumericos). Nunca predecir un tab id; capturar con jq (ver atom-herdr-captura-de-ids).
- `number` tampoco es contiguo entre tabs creados y cerrados; solo `tab_id` es estable.

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr tab list --help (herdr 0.9.0)

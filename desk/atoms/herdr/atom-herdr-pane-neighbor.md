---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-pane-neighbor
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr pane neighbor
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: pane
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:pane
---

# herdr pane neighbor

## Synopsis

_What the command does, in one or two sentences._

Find a pane neighbor

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr pane neighbor [OPTIONS] --direction <DIRECTION>

## Arguments

_Table of options: option, type, required, and what it does._

| opcion | tipo | obligatorio | que hace |
|---|---|---|---|
| --direction <DIRECTION> | enum | no | [possible values: left, right, up, down] |
| --pane <ID> | texto | no |  |
| --current | texto | no |  |

## Returns

_What the command returns on success: JSON shape and location of the payload._

JSON con `.result.type == "pane_neighbor"` (verificado en 0.9.0):

```json
{
  "result": {
    "type": "pane_neighbor",
    "neighbor": {
      "direction": "right",
      "pane_id": "wX:pF",
      "neighbor_pane_id": "wX:p1W",
      "layout": { "...": "mismo snapshot de layout que pane layout" }
    }
  }
}
```

Rutas jq exactas:

```bash
jq -r '.result.neighbor.neighbor_pane_id'   # -> id del vecino, o null si no hay
jq -r '.result.neighbor.layout.focused_pane_id'
```

`neighbor_pane_id` es `null` cuando no hay pane en esa direccion (verificado con el pane mas a la derecha del tab).

## Returns jq

_jq paths to extract the returned payload into shell variables._

Rutas jq exactas:
jq -r '.result.neighbor.neighbor_pane_id'   # -> id del vecino, o null si no hay
jq -r '.result.neighbor.layout.focused_pane_id'

## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
# Vecino derecho del primer pane (null si no existe)
pid=$(herdr pane list | jq -r '.result.panes[0].pane_id')
herdr pane neighbor --direction right --pane "$pid" | jq -r '.result.neighbor.neighbor_pane_id // "sin vecino"'
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| codigo | significado |
|---|---|
| `pane_not_found` | `--pane` inexistente; verificado: `{"error":{"code":"pane_not_found","message":"pane not found"},"id":"cli:pane:neighbor"}` en stderr con exit 1 |

## Notes

_Quirks, gotchas, and operational observations not covered above._

- La respuesta incluye el layout snapshot completo del tab, para decidir sin llamadas extra.
- `neighbor_pane_id != null` verifica que existe un vecino; el valor `null` es exito (exit 0).

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr pane neighbor --help (herdr 0.9.0)

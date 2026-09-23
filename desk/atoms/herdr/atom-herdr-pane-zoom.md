---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-pane-zoom
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr pane zoom
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: pane
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:pane
---

# herdr pane zoom

## Synopsis

_What the command does, in one or two sentences._

Toggle or set pane zoom

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr pane zoom [OPTIONS] [PANE_ID]

## Arguments

_Table of options: option, type, required, and what it does._

| opcion | tipo | obligatorio | que hace |
|---|---|---|---|
| [PANE_ID] | texto | no |  |
| --pane <ID> | texto | no |  |
| --current | texto | no |  |
| --toggle | texto | no |  |
| --on | texto | no |  |
| --off | texto | no |  |

## Returns

_What the command returns on success: JSON shape and location of the payload._

Objeto `zoom` con el resultado y el layout (verificado en vivo):

```json
{"id":"cli:pane:zoom","result":{"zoom":{"changed":true,"focus_changed":true,"focused_pane_id":"wY:p1","layout":{...}},"type":"pane_zoom"}}
```

```bash
herdr pane zoom --on --pane wY:p2 | jq -r '.result.zoom.focused_pane_id'   # el pane en zoom
herdr pane zoom --off --pane wY:p2 | jq -r '.result.zoom.changed'          # true si cambio algo
```

## Returns jq

_jq paths to extract the returned payload into shell variables._

herdr pane zoom --on --pane wY:p2 | jq -r '.result.zoom.focused_pane_id'   # el pane en zoom
herdr pane zoom --off --pane wY:p2 | jq -r '.result.zoom.changed'          # true si cambio algo

## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
# Enfocar un pane, hacerle zoom para trabajar, y al final quitar el zoom
herdr pane zoom --pane "$pane_id" --on
herdr pane zoom --pane "$pane_id" --off
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| codigo / sintoma | significado |
|---|---|
| exit 1 JSON en stderr | Error del server (p. ej. `pane_not_found`) |
| exit 2 texto plano | Sintaxis invalida: dos flags de modo a la vez (p. ej. `--on --off`) |

## Notes

_Quirks, gotchas, and operational observations not covered above._

- Observado en vivo: `zoom --off` sobre un pane sin zoom reporto `changed: true` y `focus_changed: true` (movio el foco como efecto secundario). No asumas que `--off` es un no-op si nada estaba en zoom.
- `pane zoom` cambia el foco como parte de la operacion (`focus_changed` en la respuesta).
- El layout reportado dentro de `.result.zoom.layout` es la misma forma que `pane layout` (con `zoomed: true/false`).
- El zoom es por tab: deshacer el zoom restaura los splits del tab.

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr pane zoom --help (herdr 0.9.0)

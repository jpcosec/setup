---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-pane-resize
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr pane resize
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: pane
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:pane
---

# herdr pane resize

## Synopsis

_What the command does, in one or two sentences._

Resize a pane split

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr pane resize [OPTIONS] --direction <DIRECTION>

## Arguments

_Table of options: option, type, required, and what it does._

| opcion | tipo | obligatorio | que hace |
|---|---|---|---|
| --direction <DIRECTION> | enum | no | [possible values: left, right, up, down] |
| --amount <FLOAT> | texto | no |  |
| --pane <ID> | texto | no |  |
| --current | texto | no |  |

## Returns

_What the command returns on success: JSON shape and location of the payload._

Objeto `resize` con el resultado y el layout actualizado (verificado en vivo):

```json
{"id":"cli:pane:resize","result":{"resize":{"changed":true,"pane_id":"w12:p2","layout":{...}},"type":"pane_resize"}}
```

```bash
herdr pane resize --direction left --amount 0.3 --pane w12:p2 | jq -r '.result.resize.changed'   # true
herdr pane resize --direction left --amount 0.3 --pane w12:p2 | jq -r '.result.resize.layout.panes[].pane_id'
```

El detalle interno completo de `.result.resize` (sub-campos de ratio/rect): `no verificado`.

## Returns jq

_jq paths to extract the returned payload into shell variables._

herdr pane resize --direction left --amount 0.3 --pane w12:p2 | jq -r '.result.resize.changed'   # true
herdr pane resize --direction left --amount 0.3 --pane w12:p2 | jq -r '.result.resize.layout.panes[].pane_id'

## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
# Dar mas espacio al pane de la izquierda de un split horizontal
herdr pane resize --direction left --amount 0.2 --pane "$pane_id"
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| codigo / sintoma | significado |
|---|---|
| exit 1 JSON en stderr | Error del server (p. ej. `pane_not_found`) |
| `invalid pane direction: <x> ...`, exit 2 | Sintaxis invalida (verificado en vivo: `--direction sideways` -> texto plano, exit 2) |

## Notes

_Quirks, gotchas, and operational observations not covered above._

- No resizes sin vecino en esa direccion: el borde no existe (el resultado seria un error o `changed: false`; detalle no verificado).
- La direccion es relativa al layout del tab: `--direction left` mueve el borde izquierdo del pane (crece el pane si el vecino cede espacio).
- Solo redimensiona splits existentes: para crear topologia usa `pane split`.

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr pane resize --help (herdr 0.9.0)

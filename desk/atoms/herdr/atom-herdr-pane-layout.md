---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-pane-layout
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr pane layout
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: pane
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:pane
---

# herdr pane layout

## Synopsis

_What the command does, in one or two sentences._

Show pane layout information

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr pane layout [OPTIONS]

## Arguments

_Table of options: option, type, required, and what it does._

| opcion | tipo | obligatorio | que hace |
|---|---|---|---|
| --pane <ID> | texto | no |  |
| --current | texto | no |  |

## Returns

_What the command returns on success: JSON shape and location of the payload._

Objeto `layout` con panes, splits y foco (verificado en vivo):

```json
{"id":"cli:pane:layout","result":{"layout":{
  "area":{"height":40,"width":164,"x":0,"y":0},
  "focused_pane_id":"wY:p2",
  "panes":[{"focused":false,"pane_id":"wY:p1","rect":{"height":40,"width":82,"x":0,"y":0}},
           {"focused":true,"pane_id":"wY:p2","rect":{"height":40,"width":82,"x":82,"y":0}}],
  "splits":[{"direction":"right","id":"split_0_root","ratio":0.5,"rect":{...}}],
  "tab_id":"wY:t1","workspace_id":"wY","zoomed":false},
  "type":"pane_layout"}}
```

```bash
herdr pane layout --pane wY:p1 | jq -r '.result.layout.panes[].pane_id'   # todos los panes del tab
herdr pane layout --pane wY:p1 | jq -r '.result.layout.focused_pane_id'   # pane con foco
herdr pane layout --pane wY:p1 | jq -r '.result.layout.zoomed'            # hay zoom activo?
```

## Returns jq

_jq paths to extract the returned payload into shell variables._

herdr pane layout --pane wY:p1 | jq -r '.result.layout.panes[].pane_id'   # todos los panes del tab
herdr pane layout --pane wY:p1 | jq -r '.result.layout.focused_pane_id'   # pane con foco
herdr pane layout --pane wY:p1 | jq -r '.result.layout.zoomed'            # hay zoom activo?

## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
# Inventario de panes de un tab: id + rect
herdr pane layout --pane "$pane_id" | jq -r '.result.layout.panes[] | "\(.pane_id) x=\(.rect.x) y=\(.rect.y) w=\(.rect.width) h=\(.rect.height)"'
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| codigo / sintoma | significado |
|---|---|
| `pane_not_found` en stderr, exit 1 | Pane inexistente |
| exit 2 texto plano | Sintaxis invalida del CLI |

## Notes

_Quirks, gotchas, and operational observations not covered above._

- Es la misma forma de `layout` que aparece dentro de `pane edges`, `pane neighbor`, `pane focus`, `pane resize`, `pane swap` y `pane zoom`: la estructura es `area` (dimensiones), `panes[]` con `rect`, `splits[]` (direccion, ratio), `focused_pane_id` y `zoomed`.
- `rect` son celdas de terminal: `x`, `y`, `width`, `height`.
- Para el detalle de procesos usa `pane process-info`; para bordes, `pane edges`.

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr pane layout --help (herdr 0.9.0)

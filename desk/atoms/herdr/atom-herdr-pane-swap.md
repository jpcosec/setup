---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-pane-swap
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr pane swap
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: pane
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:pane
---

# herdr pane swap

## Synopsis

_What the command does, in one or two sentences._

Swap panes

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr pane swap [OPTIONS]

## Arguments

_Table of options: option, type, required, and what it does._

| opcion | tipo | obligatorio | que hace |
|---|---|---|---|
| --direction <DIRECTION> | enum | no | [possible values: left, right, up, down] |
| --pane <ID> | texto | no |  |
| --current | texto | no |  |
| --source-pane <ID> | texto | no |  |
| --target-pane <ID> | texto | no |  |

## Returns

_What the command returns on success: JSON shape and location of the payload._

Objeto `swap` con el resultado y el layout actualizado (verificado en vivo):

```json
{"id":"cli:pane:swap","result":{"swap":{"changed":true,"focused_pane_id":"wZ:p1","layout":{...}},"type":"pane_swap"}}
```

```bash
herdr pane swap --source-pane wZ:p1 --target-pane wZ:p2 | jq -r '.result.swap.changed'              # true
herdr pane swap --source-pane wZ:p1 --target-pane wZ:p2 | jq -r '.result.swap.layout.panes[].pane_id'
```

## Returns jq

_jq paths to extract the returned payload into shell variables._

herdr pane swap --source-pane wZ:p1 --target-pane wZ:p2 | jq -r '.result.swap.changed'              # true
herdr pane swap --source-pane wZ:p1 --target-pane wZ:p2 | jq -r '.result.swap.layout.panes[].pane_id'

## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
# Forma absoluta: intercambiar el pane que quedo chico con el grande
herdr pane swap --source-pane "$small_pane" --target-pane "$big_pane"
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| codigo / sintoma | significado |
|---|---|
| exit 1 JSON en stderr | Error del server (p. ej. `pane_not_found` de cualquiera de los dos panes) |
| exit 2 texto plano | Sintaxis invalida: mezclar ambas formas o faltar componentes de una |

## Notes

_Quirks, gotchas, and operational observations not covered above._

- `swap` mueve los panes con sus procesos: la terminal viaja con su pane (a diferencia de `move`, aqui no cambia el `pane_id`; ambos ids siguen validos tras el intercambio — claro que un swap entre workspaces distintos no esta soportado por la forma direccion/source-target, la doc oficial solo contempla panes del mismo layout/tab).
- La forma por direccion intercambia con el vecino en ese borde: antes conviene `pane neighbor`/`pane edges`.
- No crea ni destruye panes: solo reordena rects y foco.

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr pane swap --help (herdr 0.9.0)

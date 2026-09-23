---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-pane-edges
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr pane edges
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: pane
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:pane
---

# herdr pane edges

## Synopsis

_What the command does, in one or two sentences._

Show pane edge information

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr pane edges [OPTIONS]

## Arguments

_Table of options: option, type, required, and what it does._

| opcion | tipo | obligatorio | que hace |
|---|---|---|---|
| --pane <ID> | texto | no |  |
| --current | texto | no |  |

## Returns

_What the command returns on success: JSON shape and location of the payload._

Objeto de bordes + layout completo (verificado en vivo):

```json
{"id":"cli:pane:edges","result":{"edges":{"down":true,"left":true,"right":true,"up":false,"layout":{...},"pane_id":"wY:p1"},"type":"pane_edges"}}
```

```bash
herdr pane edges --pane wY:p1 | jq -r '.result.edges.right'    # true/false: hay vecino a la derecha?
herdr pane edges --pane wY:p1 | jq -r '.result.edges.pane_id'  # pane consultado
```

`down`, `left`, `right`, `up` son booleanos; `layout` es el objeto de layout completo del tab (misma forma que `pane layout`).

## Returns jq

_jq paths to extract the returned payload into shell variables._

herdr pane edges --pane wY:p1 | jq -r '.result.edges.right'    # true/false: hay vecino a la derecha?
herdr pane edges --pane wY:p1 | jq -r '.result.edges.pane_id'  # pane consultado

## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
# Antes de mover el foco, verificar que existe vecino a la derecha
if herdr pane edges --pane "$pane_id" | jq -e '.result.edges.right' >/dev/null; then
  herdr pane focus --pane "$pane_id" --direction right
fi
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| codigo / sintoma | significado |
|---|---|
| `pane_not_found` en stderr, exit 1 | Pane inexistente |
| exit 2 texto plano | Sintaxis invalida del CLI |

## Notes

_Quirks, gotchas, and operational observations not covered above._

- Complementario de `pane neighbor`: `edges` da los 4 booleanos de una; `neighbor` da el detalle del vecino de una direccion.
- Opiniones del layout: un pane pegado al borde del tab tiene `false` en ese borde aunque el tab este dentro de un workspace con mas tabs.
- No modifica nada: solo lectura.

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr pane edges --help (herdr 0.9.0)

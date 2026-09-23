---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-pane-close
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr pane close
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: pane
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:pane
---

# herdr pane close

## Synopsis

_What the command does, in one or two sentences._

Close a pane

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr pane close <pane_id>

## Arguments

_Table of options: option, type, required, and what it does._

| opcion | tipo | obligatorio | que hace |
|---|---|---|---|
| <pane_id> | texto | si |  |

## Returns

_What the command returns on success: JSON shape and location of the payload._

JSON de exito (verificado en vivo con herdr 0.9.0):

```json
{"id":"cli:pane:close","result":{"type":"ok"}}
```

```bash
herdr pane close "$pane_id" | jq -r '.result.type'   # -> ok
```

Exit 0 en exito, sin salida extra.

## Returns jq

_jq paths to extract the returned payload into shell variables._

herdr pane close "$pane_id" | jq -r '.result.type'   # -> ok

## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
# Cerrar el pane que quedo libre despues de sacar su proceso
herdr pane close wX:p23
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| codigo / sintoma | significado |
|---|---|
| `{"error":{"code":"pane_not_found","message":"pane <id> not found"},"id":"cli:pane:close"}` en stderr, exit 1 | Pane inexistente (verificado en vivo) |
| exit 2 texto plano | Sintaxis invalida del CLI |
| exit 1 JSON en stderr | Cualquier otro error del server |

## Notes

_Quirks, gotchas, and operational observations not covered above._

- No pide confirmacion: cierra de una y mata el proceso del pane.
- Comportamiento con un agente vivo dentro: `no verificado`.
- El id de pane NO es predecible: capturalo con jq, nunca lo escribas a mano.

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr pane close --help (herdr 0.9.0)

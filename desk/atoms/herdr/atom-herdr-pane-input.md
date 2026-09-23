---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-pane-input
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr pane input
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: pane
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:pane
---

# herdr pane input

## Synopsis

_What the command does, in one or two sentences._

Set pane input routing

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr pane input [OPTIONS] --right-click <TARGET> [PANE_ID]

## Arguments

_Table of options: option, type, required, and what it does._

| opcion | tipo | obligatorio | que hace |
|---|---|---|---|
| [PANE_ID] | texto | no |  |
| --pane <ID> | texto | no |  |
| --current | texto | no |  |
| --right-click <TARGET> | enum | no | [possible values: herdr, pane] |

## Returns

_What the command returns on success: JSON shape and location of the payload._

JSON de confirmacion (verificado en vivo):

```json
{"id":"cli:pane:input:set","result":{"type":"ok"}}
```

```bash
herdr pane input --right-click herdr | jq -r '.result.type'   # -> ok
```

## Returns jq

_jq paths to extract the returned payload into shell variables._

herdr pane input --right-click herdr | jq -r '.result.type'   # -> ok

## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
# Aplicacion ratonera (p. ej. un TUI que reporta mouse): el click derecho va a la app
herdr pane input "$pane_id" --right-click pane

# Volver al comportamiento por defecto: boton derecho abre el menu de herdr
herdr pane input "$pane_id" --right-click herdr
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| codigo / sintoma | significado |
|---|---|
| `pane_not_found` en stderr, exit 1 | Pane inexistente |
| exit 2 texto plano | Sintaxis invalida (p. ej. `--right-click` sin valor o valor invalido) |

## Notes

_Quirks, gotchas, and operational observations not covered above._

- Doc oficial: `--right-click pane` reenvia los clicks derechos sin modificar a una aplicacion que reporta mouse; `herdr` restaura el menu por defecto.
- El click derecho sobre el marco del pane (frame) SIEMPRE abre el menu de herdr, sea cual sea el valor.
- `pane split` tiene su propio `--right-click` para aplicar la misma politica al nuevo pane al crearlo.
- Otros tipos de input (teclado) no se configuran aqui: eso es `send-keys`/`send-text`/`run`.

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr pane input --help (herdr 0.9.0)

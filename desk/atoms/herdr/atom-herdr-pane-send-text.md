---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-pane-send-text
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr pane send-text
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: pane
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:pane
---

# herdr pane send-text

## Synopsis

_What the command does, in one or two sentences._

Send literal text to a pane

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr pane send-text <PANE_ID> <TEXT>

## Arguments

_Table of options: option, type, required, and what it does._

| opcion | tipo | obligatorio | que hace |
|---|---|---|---|
| <PANE_ID> | texto | si |  |
| <TEXT> | texto | si |  |

## Returns

_What the command returns on success: JSON shape and location of the payload._

Exito **silencioso**: sin salida, exit 0 (verificado en vivo: stdout y stderr vacios). Nada que parsear con jq.

## Returns jq

_jq paths to extract the returned payload into shell variables._

Exito **silencioso**: sin salida, exit 0 (verificado en vivo: stdout y stderr vacios). Nada que parsear con jq.

## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
# Construir una linea de a trozos y someterla despues
herdr pane send-text "$pane_id" 'printf "hello %s\n"'
herdr pane send-text "$pane_id" '"mundo"'
herdr pane send-keys "$pane_id" enter
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| codigo / sintoma | significado |
|---|---|
| `pane_not_found` en stderr, exit 1 | Pane inexistente |
| exit 2 texto plano | Sintaxis invalida del CLI |

## Notes

_Quirks, gotchas, and operational observations not covered above._

- **Diferencia exacta entre los tres (doc oficial)**:
  - `pane run` — texto + Enter, atomico, honra bracketed-paste. Para COMANDOS.
  - `pane send-text` — texto literal SIN Enter. Para pegar contenido parcial; nunca somete.
  - `pane send-keys` — teclas/acordes (`enter`, `ctrl+c`, `up`...). Para interaccion con UI de terminal.
- `send-text` + `send-keys enter` funcionalmente somete, pero la doc oficial recomienda `run` para comandos: las operaciones send son low-level y no-submitting.
- Como todos los pane input commands, direcciona el terminal sin importar su ocupante.

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr pane send-text --help (herdr 0.9.0)

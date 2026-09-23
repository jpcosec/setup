---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-pane-send-keys
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr pane send-keys
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: pane
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:pane
---

# herdr pane send-keys

## Synopsis

_What the command does, in one or two sentences._

Send key presses to a pane

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr pane send-keys <PANE_ID> <KEY>...

## Arguments

_Table of options: option, type, required, and what it does._

| opcion | tipo | obligatorio | que hace |
|---|---|---|---|
| <PANE_ID> | texto | si |  |
| <KEY>... | texto | si |  |

## Returns

_What the command returns on success: JSON shape and location of the payload._

Exito **silencioso**: sin salida, exit 0 (misma naturaleza que `run`/`send-text`; confirmado por la doc oficial: los comandos de envio no imprimen JSON en exito). Nada que parsear.

## Returns jq

_jq paths to extract the returned payload into shell variables._



## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
# Interactuar con la UI de un agente tras un wait (patron de la doc oficial)
herdr pane wait-output "$pane_id" --match 'Allow?' --timeout 30000
herdr pane send-keys "$pane_id" enter

# Interrumpir un proceso en primer plano
herdr pane send-keys "$pane_id" ctrl+c
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| codigo / sintoma | significado |
|---|---|
| exit 2 texto plano | Sintaxis invalida: tecla desconocida o malformada |
| exit 1 JSON en stderr | Error del server (p. ej. `pane_not_found`) |

## Notes

_Quirks, gotchas, and operational observations not covered above._

- Doc oficial: "Herdr validates every key before writing any bytes": una tecla invalida en la lista hace fallar la llamada entera (nada se escribe).
- NO somete comandos: para texto + Enter atomico usa `pane run`; para texto literal sin Enter, `pane send-text`.
- Direcciona el terminal pase lo que pase dentro; para resolver el agente vivo y rechazar si ya no controla el pane, usa `agent send-keys` (doc oficial).
- En coordinacion de workers, `esc`/`enter`/`up`/`ctrl+c` son las teclas que se mandan deliberadamente (respuestas a UIs de aprobacion).

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr pane send-keys --help (herdr 0.9.0)

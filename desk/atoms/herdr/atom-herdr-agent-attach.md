---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-agent-attach
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr agent attach
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: agent
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:agent
---

# herdr agent attach

## Synopsis

_What the command does, in one or two sentences._

Attach directly to an agent terminal

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr agent attach <TARGET> [OPTIONS]

## Arguments

_Table of options: option, type, required, and what it does._

| opcion | tipo | obligatorio | que hace |
|---|---|---|---|
| <TARGET> | texto | si |  |
| --takeover | texto | no |  |

## Returns

_What the command returns on success: JSON shape and location of the payload._

No devuelve JSON: es un modo interactivo — la terminal pasa a ser el terminal del agente (adjunta). La secuencia de salida para desadjuntar: no verificada.

## Returns jq

_jq paths to extract the returned payload into shell variables._



## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
# Adjuntarse al agente 'reviewer'
herdr agent attach reviewer

# Adjuntarse al pane que aloja al agente w1 (captura el ID real, nunca lo predigas)
pane_id=$(herdr agent get w1 | jq -r '.result.agent.pane_id')
herdr agent attach "$pane_id"
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| codigo | significado |
|---|---|
| `usage: herdr agent attach <target> [--takeover]` + exit 2 | Sintaxis invalida (falta `<TARGET>`); verificado en 0.9.0 |
| error JSON en stderr, exit 1 | Error del server (p. ej. agente/pane inexistente); codigos exactos no verificados |

## Notes

_Quirks, gotchas, and operational observations not covered above._

- `<TARGET>` acepta nombre de agente o pane ID; los agent commands resuelven agentes vivos (doc oficial).
- Adjuntarse es una operacion interactiva de TUI: en scripts se usa `agent read` + `agent send-keys` en su lugar.
- Los IDs y nombres de agente estan acotados a un solo server; no retargetean a otra maquina.

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr agent attach --help (herdr 0.9.0)

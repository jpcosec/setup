---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-agent-send-keys
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr agent send-keys
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: agent
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:agent
---

# herdr agent send-keys

## Synopsis

_What the command does, in one or two sentences._

Send key presses to an agent

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr agent send-keys <TARGET> <KEY>...

## Arguments

_Table of options: option, type, required, and what it does._

| opcion | tipo | obligatorio | que hace |
|---|---|---|---|
| <TARGET> | texto | si |  |
| <KEY>... | texto | si |  |

## Returns

_What the command returns on success: JSON shape and location of the payload._

No devuelve JSON verificable: es una accion de input. Salida exacta en exito: no verificada (no ejecutado para no interferir con agentes vivos; el CLI de 0.9.0 no documenta respuesta).

## Returns jq

_jq paths to extract the returned payload into shell variables._



## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
# Responder a un dialogo de aprobacion (agente bloqueado)
herdr agent send-keys reviewer esc

# Confirmar / navegar la UI
herdr agent send-keys reviewer enter
herdr agent send-keys reviewer up

# Interrumpir al agente
herdr agent send-keys reviewer ctrl+c
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| codigo | significado |
|---|---|
| error JSON en stderr, exit 1 | El agente ya no controla el pane (fue reemplazado/salio), o target inexistente; la operacion se rechaza (doc oficial); codigos exactos no verificados |
| `usage: herdr agent send-keys <target> <key>...` + exit 2 | Faltan `<TARGET>` o `<KEY>` |

## Notes

_Quirks, gotchas, and operational observations not covered above._

- Es el camino correcto para interacciones tipo `esc`, `up`, `enter`, `ctrl+c` con la UI del agente (doc oficial).
- Resuelve el agente vivo y RECHAZA la operacion si ese agente ya no controla el pane; los comandos `pane` (`pane send-text`, `pane send-keys`) dan control crudo del terminal sin esa comprobacion.
- Para `agent prompt` de un agente `blocked`: NO se envia el prompt (error `agent_blocked`); la respuesta deliberada a un dialogo se hace con `agent send-keys`.

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr agent send-keys --help (herdr 0.9.0)

---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-agent-focus
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr agent focus
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: agent
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:agent
---

# herdr agent focus

## Synopsis

_What the command does, in one or two sentences._

Focus an agent

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr agent focus <target>

## Arguments

_Table of options: option, type, required, and what it does._

| opcion | tipo | obligatorio | que hace |
|---|---|---|---|
| <target> | texto | si |  |

## Returns

_What the command returns on success: JSON shape and location of the payload._

No devuelve JSON verificable: es una accion de foco. Salida exacta en exito: no verificada (no ejecutado para no robar foco de sesiones activas).

## Returns jq

_jq paths to extract the returned payload into shell variables._



## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
# Marcar al agente como visto sin leerlo: si estaba 'done' pasa a 'idle'
herdr agent focus reviewer

# Verificar que el agente quedo en idle
herdr agent get reviewer | jq -r '.result.agent.agent_status'
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| codigo | significado |
|---|---|
| `usage: herdr agent focus <target>` + exit 2 | Falta `<target>`; verificado en 0.9.0 |
| error JSON en stderr, exit 1 | Error del server (agente inexistente); codigos exactos no verificados |

## Notes

_Quirks, gotchas, and operational observations not covered above._

- Segun la doc oficial: los comandos explicitos `pane focus` / `agent focus` marcan el target como visto; `done` es idle pero aun no marcado como visto, y las lecturas NO lo marcan.
- Cada cliente TUI trackea sus completados vistos por separado: el badge Done de un cliente puede diferir del CLI.
- Es una operacion de TUI: roba el foco visual; no se recomienda en scripts de automatizacion.

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr agent focus --help (herdr 0.9.0)

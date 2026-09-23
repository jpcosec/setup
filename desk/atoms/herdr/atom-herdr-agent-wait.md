---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-agent-wait
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr agent wait
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: agent
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:agent
---

# herdr agent wait

## Synopsis

_What the command does, in one or two sentences._

Wait until an agent reaches one of the requested states

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr agent wait <TARGET> [OPTIONS]

## Arguments

_Table of options: option, type, required, and what it does._

| opcion | tipo | obligatorio | que hace |
|---|---|---|---|
| <TARGET> | texto | si |  |
| --until <STATUS> | enum | no | State to match; repeat for more than one state [possible values: idle, working, blocked, done, unknown] |
| --timeout <MS> | numero | no | Fail after this many milliseconds |

## Returns

_What the command returns on success: JSON shape and location of the payload._

En match, JSON con el agente en `.result.agent` (verificado en vivo 0.9.0):

```json
{"id":"cli:agent:wait","result":{"agent":{"agent":"pi","agent_status":"working","pane_id":"wX:p23",...},"type":"agent_info"}}
```

Rutas jq exactas:

```bash
printf '%s' "$result" | jq -r '.result.agent.agent_status'   # estado que matcheo (idle|working|blocked|done|unknown)
printf '%s' "$result" | jq -r '.result.agent.pane_id'        # pane del agente
printf '%s' "$result" | jq -r '.result.agent.name'           # alias (null si no tiene)
```

## Returns jq

_jq paths to extract the returned payload into shell variables._

Rutas jq exactas:
printf '%s' "$result" | jq -r '.result.agent.agent_status'   # estado que matcheo (idle|working|blocked|done|unknown)
printf '%s' "$result" | jq -r '.result.agent.pane_id'        # pane del agente
printf '%s' "$result" | jq -r '.result.agent.name'           # alias (null si no tiene)

## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
# Esperar a que el agente pida aprobacion (max 2 min)
result=$(herdr agent wait reviewer --until blocked --timeout 120000)
printf '%s' "$result" | jq -r '.result.agent.agent_status'   # blocked

# Esperar a que termine su turno: idle O done (set por defecto)
herdr agent wait reviewer --timeout 120000

# Esperar varios estados exactos
herdr agent wait reviewer --until idle --until done --timeout 120000
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| codigo | significado |
|---|---|
| `timeout` | No matcheo antes del `--timeout`. Verificado en vivo: `{"error":{"code":"timeout","message":"timed out waiting for agent status"},"id":"cli:agent:wait"}` en stderr, exit 1 |
| `agent_not_running` | Un wait ya en progreso termina con este codigo si el agente deja de correr (p. ej. `pane move` en curso; doc oficial) |
| `usage: herdr agent wait <target>` + exit 2 | Falta `<TARGET>` |

## Notes

_Quirks, gotchas, and operational observations not covered above._

- Wait standalone observa el estado ACTUAL y retorna inmediatamente si ya matchea (doc oficial).
- `agent prompt --wait` es distinto: espera actividad tras la sumision; `agent wait` solo observa.
- El error de timeout sale como JSON a stderr con exit 1 (doc oficial); el exit 2 es para sintaxis invalida.

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr agent wait --help (herdr 0.9.0)

---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-agent-get
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr agent get
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: agent
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:agent
---

# herdr agent get

## Synopsis

_What the command does, in one or two sentences._

Show an agent

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr agent get <target>

## Arguments

_Table of options: option, type, required, and what it does._

| opcion | tipo | obligatorio | que hace |
|---|---|---|---|
| <target> | texto | si |  |

## Returns

_What the command returns on success: JSON shape and location of the payload._

JSON con el agente en `.result.agent` (verificado en 0.9.0):

```json
{"id":"cli:agent:get","result":{"agent":{...},"type":"agent_info"}}
```

Campos del agente: `.agent` (kind, p. ej. `pi`), `.agent_status`, `.cwd`, `.foreground_cwd`, `.focused`, `.pane_id`, `.revision`, `.state_change_seq`, `.tab_id`, `.terminal_id`, `.terminal_title`, `.terminal_title_stripped`, `.workspace_id`, y opcionales `.name`, `.interactive_ready`, `.agent_session`.

Rutas jq exactas:

```bash
jq -r '.result.agent.agent_status'   # idle|working|blocked|done|unknown
jq -r '.result.agent.pane_id'        # pane que aloja al agente
jq -r '.result.agent.name'           # alias (null si no tiene nombre)
jq -r '.result.agent.cwd'            # directorio de trabajo actual
jq -r '.result.agent.interactive_ready'  # true|false|null
```

## Returns jq

_jq paths to extract the returned payload into shell variables._

Rutas jq exactas:
jq -r '.result.agent.agent_status'   # idle|working|blocked|done|unknown
jq -r '.result.agent.pane_id'        # pane que aloja al agente
jq -r '.result.agent.name'           # alias (null si no tiene nombre)
jq -r '.result.agent.cwd'            # directorio de trabajo actual
jq -r '.result.agent.interactive_ready'  # true|false|null

## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
# Estado y ubicacion del agente 'reviewer'
herdr agent get reviewer | jq -r '.result.agent.agent_status, .result.agent.pane_id'

# Listar todos los agentes de un workspace con un unlax de campos
herdr agent list | jq -r '.result.agents[] | select(.workspace_id=="wX") | [.agent, .agent_status, .pane_id] | @tsv'
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| codigo | significado |
|---|---|
| error JSON `{"error":{"code":"...","message":"..."},"id":"cli:agent:get"}` en stderr, exit 1 | Agente/pane inexistente o server caido; codigos exactos no verificados |
| `usage: herdr agent get <target>` + exit 2 | Falta `<target>` |

## Notes

_Quirks, gotchas, and operational observations not covered above._

- Acepta nombre o pane ID indistintamente; el nombre es un alias del agente actual en ese pane y se limpia al salir.
- `agent_status` refleja el estado del ciclo de vida; `interactive_ready` solo aparece cuando el agente esta listo para input interactivo.
- Verificado en vivo 2026-09-23: agente `pi` named `w1` en pane `wX:p23`, estado `working`.

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr agent get --help (herdr 0.9.0)

---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-agent-list
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr agent list
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: agent
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:agent
---

# herdr agent list

## Synopsis

_What the command does, in one or two sentences._

List agents

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr agent list

## Arguments

_Table of options: option, type, required, and what it does._



## Returns

_What the command returns on success: JSON shape and location of the payload._

JSON con todos los agentes en `.result.agents[]` (verificado en 0.9.0; `list` emite JSON siempre):

```json
{"id":"cli:agent:list","result":{"agents":[{ "agent": "pi", "agent_status": "working", "cwd": "...", "pane_id": "wX:p23", ... }, ...], "type": "agent_list"}}
```

Campos por agente: `agent` (kind), `agent_status`, `cwd`, `foreground_cwd`, `focused`, `pane_id`, `revision`, `state_change_seq`, `tab_id`, `terminal_id`, `terminal_title`, `terminal_title_stripped`, `workspace_id`, y opcionales `name`, `interactive_ready`, `agent_session`.

Rutas jq exactas:

```bash
jq -r '.result.agents[].name'                        # todos los alias (null si sin nombre)
jq -r '.result.agents[] | select(.agent_status=="idle") | .pane_id'   # panes idle
jq -r '.result.agents[] | [.agent, .agent_status, .pane_id] | @tsv'   # tabla compacta
jq -r '.result.agents[] | select(.workspace_id=="wX") | .name'        # agentes de un workspace
```

## Returns jq

_jq paths to extract the returned payload into shell variables._

Rutas jq exactas:
jq -r '.result.agents[].name'                        # todos los alias (null si sin nombre)
jq -r '.result.agents[] | select(.agent_status=="idle") | .pane_id'   # panes idle
jq -r '.result.agents[] | [.agent, .agent_status, .pane_id] | @tsv'   # tabla compacta
jq -r '.result.agents[] | select(.workspace_id=="wX") | .name'        # agentes de un workspace

## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
# Tabla: kind, estado, pane
herdr agent list | jq -r '.result.agents[] | [.agent, .agent_status, .pane_id] | @tsv'

# Contar agentes por estado
herdr agent list | jq -r '.result.agents[].agent_status' | sort | uniq -c
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| codigo | significado |
|---|---|
| error JSON en stderr, exit 1 | Server caido o socket inaccesible; codigos exactos no verificados |

## Notes

_Quirks, gotchas, and operational observations not covered above._

- Solo agentes detectados: un pane con un proceso normal (shell, pytest, servidor) NO aparece aqui; para eso es `herdr pane list`.
- `list` y `get` comparten el mismo shape de agente; `list` no tiene `--json` porque ya emite JSON.
- Verificado en vivo 2026-09-23: 8 agentes (pi x7, claude x1) en workspaces wX/wY, estados `working` e `idle`.

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr agent list --help (herdr 0.9.0)

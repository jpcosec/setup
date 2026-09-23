---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-api-snapshot
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr api snapshot
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: api
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:api
---

# herdr api snapshot

## Synopsis

_What the command does, in one or two sentences._

Print the live session snapshot

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr api snapshot

## Arguments

_Table of options: option, type, required, and what it does._



## Returns

_What the command returns on success: JSON shape and location of the payload._

JSON `cli:api:snapshot` → `.result.snapshot` con `type: session_snapshot`. Verificado en este setup (200 panes reales):

| Ruta jq | Que extrae |
| --- | --- |
| `.result.snapshot.agents[] \| [.agent, .agent_status, .pane_id, .workspace_id]` | Inventario vivo de agentes |
| `.result.snapshot.agents[] \| select(.agent_status == "working") \| .pane_id` | Panes ocupados |
| `.result.snapshot.focused_pane_id` | Pane con foco ahora |
| `.result.snapshot.focused_workspace_id` | Workspace con foco |
| `.result.snapshot.panes[] \| select(.agent == "pi") \| .scroll.max_offset_from_bottom` | Profundidad del scrollback en memoria |
| `.result.snapshot.workspaces[] \| [.workspace_id, .label, .pane_count, .worktree.repo_name]` | Workspaces y su repo asociado |
| `.result.snapshot.tabs[] \| [.tab_id, .label, .pane_count]` | Tabs por workspace |

Campos tipicos por agente: `agent`, `agent_status` (`idle`/`working`/`blocked`/`unknown`), `agent_session` (para claude/codex: `{agent, kind, source, value}`), `cwd`, `foreground_cwd`, `pane_id`, `revision`, `state_change_seq`, `tab_id`, `terminal_id`, `terminal_title`, `workspace_id`, opcional `interactive_ready` y `name` (agentes con nombre).

## Returns jq

_jq paths to extract the returned payload into shell variables._

| Ruta jq | Que extrae |

## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
# Tabla compacta: quien esta trabajando y donde
herdr api snapshot | jq -r '.result.snapshot.agents[]
  | select(.agent_status != "unknown")
  | "\(.agent)\t\(.agent_status)\t\(.pane_id)\t\(.foreground_cwd)"'

# Pane con foco y workspace con foco
herdr api snapshot | jq -r '"\(.result.snapshot.focused_workspace_id) \(.result.snapshot.focused_pane_id)"'
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| Codigo | Significado |
| --- | --- |
| `server_unavailable` | El server no esta corriendo: el snapshot no tiene fuente |
| `serialization_error` | Fallo al serializar el snapshot (string del binario) |

## Notes

_Quirks, gotchas, and operational observations not covered above._

- Es la mejor fuente unica para descubrir `pane_id`, `tab_id` y `workspace_id` reales sin predecir IDs (regla del skill oficial: leer IDs del JSON, nunca inventarlos).
- Verificado en este setup: 2 workspaces (wX setup con 7 panes, wY AWS_Infra con 4), agentes pi/claude/yazi; scrollback en memoria de hasta ~6375 filas en un pane.
- Es una llamada de solo lectura: no genera entrada en el log del server (ver `atom-herdr-no-guarda-traza`).

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr api snapshot --help (herdr 0.9.0)

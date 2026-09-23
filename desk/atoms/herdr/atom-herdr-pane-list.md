---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-pane-list
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr pane list
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: pane
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:pane
---

# herdr pane list

## Synopsis

_What the command does, in one or two sentences._

List panes

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr pane list [OPTIONS]

## Arguments

_Table of options: option, type, required, and what it does._

| opcion | tipo | obligatorio | que hace |
|---|---|---|---|
| --workspace <WORKSPACE_ID> | texto | no |  |

## Returns

_What the command returns on success: JSON shape and location of the payload._

Array de panes en `.result.panes` (verificado en vivo):

```json
{"id":"cli:pane:list","result":{"panes":[{"pane_id":"wY:p1",...}],"type":"pane_list"}}
```

Cada entrada tiene la misma forma que `pane get` (`.agent`, `.agent_status`, `.cwd`, `.focused`, `.scroll`, `.terminal_title`, etc.).

```bash
herdr pane list | jq -r '.result.panes[].pane_id'                        # todos los panes
herdr pane list --workspace wY | jq -r '.result.panes[].pane_id'         # solo workspace wY
herdr pane list | jq -r '.result.panes[] | select(.focused==true) | .pane_id'  # pane enfocado
herdr pane list | jq -r '.result.panes[] | select(.agent=="pi") | .pane_id'     # panes con pi
```

## Returns jq

_jq paths to extract the returned payload into shell variables._

herdr pane list | jq -r '.result.panes[].pane_id'                        # todos los panes
herdr pane list --workspace wY | jq -r '.result.panes[].pane_id'         # solo workspace wY
herdr pane list | jq -r '.result.panes[] | select(.focused==true) | .pane_id'  # pane enfocado
herdr pane list | jq -r '.result.panes[] | select(.agent=="pi") | .pane_id'     # panes con pi

## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
# Detectar panes cuyo agente sigue "working" (esperando turno)
herdr pane list | jq -r '.result.panes[] | select(.agent_status=="working") | "\(.pane_id) cwd=\(.cwd)"'
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| codigo / sintoma | significado |
|---|---|
| `{"error":{"code":"workspace_not_found","message":"workspace <id> not found"},"id":"cli:pane:list"}` en stderr, exit 1 | Workspace inexistente (verificado en vivo) |
| exit 2 texto plano | Sintaxis invalida del CLI |

## Notes

_Quirks, gotchas, and operational observations not covered above._

- La salida NO tiene forma de tabla: es JSON; parsealo con jq, nunca con grep.
- `agent` puede faltar (pane sin agente reconocido) y `agent_status` puede ser `unknown` (agent presente no clasificable, no significa exito — doc oficial).
- El `id` del JSON completo es `cli:pane:list` (guion), aunque la respuesta viva mostro `type: "pane_list"` (guion bajo).

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr pane list --help (herdr 0.9.0)

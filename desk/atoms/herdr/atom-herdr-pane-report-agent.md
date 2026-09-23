---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-pane-report-agent
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr pane report-agent
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: pane
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:pane
---

# herdr pane report-agent

## Synopsis

_What the command does, in one or two sentences._

Report pane agent lifecycle state

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr pane report-agent [OPTIONS] --source <ID> --agent <LABEL> --state <STATUS> <PANE_ID>

## Arguments

_Table of options: option, type, required, and what it does._

| opcion | tipo | obligatorio | que hace |
|---|---|---|---|
| <PANE_ID> | texto | si |  |
| --source <ID> | texto | no |  |
| --agent <LABEL> | texto | no |  |
| --state <STATUS> | enum | no | [possible values: idle, working, blocked, unknown] |
| --message <TEXT> | texto | no |  |
| --seq <N> | numero | no |  |
| --agent-session-id <ID> | texto | no |  |
| --agent-session-path <PATH> | texto | no |  |

## Returns

_What the command returns on success: JSON shape and location of the payload._

Forma exacta del JSON de exito: `no verificado` (comando de hooks; no ejecutado en vivo). El efecto observable: `pane get`/`pane list` reflejan el estado reportado en `.result.pane.agent_status`.

## Returns jq

_jq paths to extract the returned payload into shell variables._



## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
# Hook que marca un agente como ocupado mientras trabaja
herdr pane report-agent "$pane_id" \
  --source "hook:codex:session" --agent codex --state working \
  --message "generando plan"

# Al terminar, marcar idle
herdr pane report-agent "$pane_id" \
  --source "hook:codex:session" --agent codex --state idle
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| codigo / sintoma | significado |
|---|---|
| exit 2 texto plano | Sintaxis invalida: faltan `--source`/`--agent`/`--state`/`<PANE_ID>` o `--state` invalido |
| exit 1 JSON en stderr | Error del server (p. ej. `pane_not_found`) |
| `agent_status` no refleja el report | Posible reporte stale descartado por `--seq` (secuencia menor que la ultima vista de esa fuente) |

## Notes

_Quirks, gotchas, and operational observations not covered above._

- Doc oficial: `idle` y `done` significan "listo para input" (difieren en si fue marcado "seen"); `blocked` = UI de aprobacion/pregunta reconocida; `unknown` = no clasificable (no prueba exito).
- En este ecosistema los workers son agentes interactivos en panes herdr: coordination.sh usa la API de agente (`agent ...`), mientras que `report-*` es el canal para hooks propios que quieren poblar el mismo estado.
- Los stale reports se aceptan en la API pero se ignoran en el estado del pane (doc oficial).

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr pane report-agent --help (herdr 0.9.0)

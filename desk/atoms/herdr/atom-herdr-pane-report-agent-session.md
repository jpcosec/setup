---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-pane-report-agent-session
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr pane report-agent-session
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: pane
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:pane
---

# herdr pane report-agent-session

## Synopsis

_What the command does, in one or two sentences._

Report pane agent session identity

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr pane report-agent-session [OPTIONS] --source <ID> --agent <LABEL> <PANE_ID>

## Arguments

_Table of options: option, type, required, and what it does._

| opcion | tipo | obligatorio | que hace |
|---|---|---|---|
| <PANE_ID> | texto | si |  |
| --source <ID> | texto | no |  |
| --agent <LABEL> | texto | no |  |
| --seq <N> | numero | no |  |
| --agent-session-id <ID> | texto | no |  |
| --agent-session-path <PATH> | texto | no |  |
| --session-start-source <SOURCE> | texto | no |  |

## Returns

_What the command returns on success: JSON shape and location of the payload._

Forma exacta del JSON de exito: `no verificado` (comando de hooks; no ejecutado en vivo). Efecto observable: cuando una integracion oficial reporto una sesion nativa, `pane get`/`pane list` incluyen el objeto `agent_session` (doc oficial):

```json
{"agent":"claude","kind":"id","source":"herdr:claude","value":"27a64105-..."}
```

```bash
herdr pane get "$pane_id" | jq -r '.result.pane.agent_session.value // "sin-sesion-nativa"'
```

## Returns jq

_jq paths to extract the returned payload into shell variables._

herdr pane get "$pane_id" | jq -r '.result.pane.agent_session.value // "sin-sesion-nativa"'

## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
# Hook de arranque de codex: registrar la sesion nativa del agente
herdr pane report-agent-session "$pane_id" \
  --source "hook:codex:session_start" --agent codex \
  --agent-session-id "abc-123" --agent-session-path "/home/jp/.codex/sessions/abc-123"
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| codigo / sintoma | significado |
|---|---|
| exit 2 texto plano | Sintaxis invalida: faltan `--source`/`--agent`/`<PANE_ID>` |
| exit 1 JSON en stderr | Error del server (p. ej. `pane_not_found`) |

## Notes

_Quirks, gotchas, and operational observations not covered above._

- Doc oficial: "`report-agent-session` updates native session identity without reporting lifecycle state." No toca `agent_status`.
- El objeto `agent_session` aparece solo cuando una integracion oficial reporto el dato; si no, el campo se omite (no aparece como null).
- Diferencial rapido: `report-agent` = estado; `report-agent-session` = identidad de sesion; `report-metadata` = datos display-only.

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr pane report-agent-session --help (herdr 0.9.0)

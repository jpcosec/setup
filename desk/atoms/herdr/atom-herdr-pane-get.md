---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-pane-get
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr pane get
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: pane
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:pane
---

# herdr pane get

## Synopsis

_What the command does, in one or two sentences._

Show a pane

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr pane get <pane_id>

## Arguments

_Table of options: option, type, required, and what it does._

| opcion | tipo | obligatorio | que hace |
|---|---|---|---|
| <pane_id> | texto | si |  |

## Returns

_What the command returns on success: JSON shape and location of the payload._

El pane completo en `.result.pane` (verificado en vivo con herdr 0.9.0):

```json
{"id":"cli:pane:get","result":{"pane":{...},"type":"pane_info"}}
```

Campos clave:

| campo | significado |
|---|---|
| `.result.pane.pane_id` | id (`wX:p23`) |
| `.result.pane.workspace_id` / `.tab_id` / `.terminal_id` | contenedores y terminal subyacente |
| `.result.pane.cwd` | cwd del pane (labels/follow-cwd); `foreground_cwd` si herdr lo resuelve |
| `.result.pane.agent` / `.agent_status` | agente reconocido y su estado (`idle`, `working`, `blocked`, `unknown`); campo ausente si no hay agente |
| `.result.pane.focused` | si tiene el foco |
| `.result.pane.scroll` | `max_offset_from_bottom`, `offset_from_bottom` (`0` = fondo del scrollback), `viewport_rows` |
| `.result.pane.agent_session` | solo si una integracion oficial reporto sesion nativa (opcional, doc oficial) |
| `.result.pane.label` | label del pane si fue renombrado con `pane rename` |

```bash
pane_id=$(herdr pane get wY:p1 | jq -r '.result.pane.pane_id')
agent=$(herdr pane get wY:p1 | jq -r '.result.pane.agent // "sin-agente"')
```

## Returns jq

_jq paths to extract the returned payload into shell variables._

pane_id=$(herdr pane get wY:p1 | jq -r '.result.pane.pane_id')
agent=$(herdr pane get wY:p1 | jq -r '.result.pane.agent // "sin-agente"')

## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
# Verificar que un pane sigue vivo y en que estado esta su agente
info=$(herdr pane get "$pane_id")
printf 'pane=%s workspace=%s agente=%s estado=%s\n' \
  "$(printf '%s' "$info" | jq -r '.result.pane.pane_id')" \
  "$(printf '%s' "$info" | jq -r '.result.pane.workspace_id')" \
  "$(printf '%s' "$info" | jq -r '.result.pane.agent // "none"')" \
  "$(printf '%s' "$info" | jq -r '.result.pane.agent_status // "none"')"
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| codigo / sintoma | significado |
|---|---|
| `{"error":{"code":"pane_not_found","message":"pane <id> not found"},"id":"cli:pane:get"}` en stderr, exit 1 | Pane inexistente (verificado en vivo) |
| exit 2 texto plano | Sintaxis invalida del CLI |

## Notes

_Quirks, gotchas, and operational observations not covered above._

- El id se captura con jq desde la creacion (`pane split` -> `.result.pane.pane_id`); nunca se predice.
- Despues de `pane move` entre workspaces, el id cambia: relee con `.result.move_result.pane.pane_id` (ver atom-herdr-captura-de-ids).
- `pane list` devuelve la misma forma de pane por cada entrada.

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr pane get --help (herdr 0.9.0)

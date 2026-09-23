---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-pane-read
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr pane read
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: pane
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:pane
---

# herdr pane read

## Synopsis

_What the command does, in one or two sentences._

Read pane terminal output

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr pane read [OPTIONS] <PANE_ID>

## Arguments

_Table of options: option, type, required, and what it does._

| opcion | tipo | obligatorio | que hace |
|---|---|---|---|
| <PANE_ID> | texto | si |  |
| --source <SOURCE> | enum | no | Terminal snapshot source (default: recent) [possible values: visible, recent, recent-unwrapped, detection] |
| --lines <N> | numero | no |  |
| --format <FORMAT> | enum | no | [possible values: text, ansi] |
| --ansi | texto | no |  |
| --raw | texto | no |  |

## Returns

_What the command returns on success: JSON shape and location of the payload._

El CLI imprime el texto del terminal **directamente** (no JSON; verificado en 0.9.0). Por el socket API el texto queda en `.result.read.text`. No aplica jq sobre la salida del CLI.

## Returns jq

_jq paths to extract the returned payload into shell variables._

El CLI imprime el texto del terminal **directamente** (no JSON; verificado en 0.9.0). Por el socket API el texto queda en `.result.read.text`. No aplica jq sobre la salida del CLI.

## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
# Ultimas 120 lineas sin wrap de un pane
pid=$(herdr pane list | jq -r '.result.panes[0].pane_id')
herdr pane read "$pid" --source recent-unwrapped --lines 120
# Snapshot visible conservando ANSI
herdr pane read "$pid" --source visible --ansi
# Buscar un marcador en la salida sin grep sobre ids
herdr pane read "$pid" --source recent --lines 200 | grep -n "passed|failed" || echo "aun no"
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| codigo | significado |
|---|---|
| `pane_not_found` | Pane inexistente; verificado: `{"error":{"code":"pane_not_found","message":"pane wX:nope not found"},"id":"cli:pane:read"}` en stderr con exit 1 |
| `agent_not_idle` | `agent read --lines N` pide historial de alternate-screen mientras el agente esta working/blocked/unknown (doc oficial; aplica a `pane read` cuando el pane contiene ese agente) |

## Notes

_Quirks, gotchas, and operational observations not covered above._

- Fuentes `recent`/`recent-unwrapped`: por defecto 80 filas; `recent` respeta soft-wrap, `recent-unwrapped` lo ignora (ideal para logs).
- `visible` y `detection` sin `--lines` devuelven el snapshot completo; `detection` es siempre texto plano (usado por la deteccion de agentes).
- Para agentes full-screen (Claude Code, OpenCode), los reads `recent` con `--lines` grande usan la interfaz mouse-scroll del agente para recoger historial; si falta, pide al agente escribir en markdown en un directorio temporal (doc oficial).

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr pane read --help (herdr 0.9.0)

---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-agent-read
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr agent read
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: agent
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:agent
---

# herdr agent read

## Synopsis

_What the command does, in one or two sentences._

Read agent terminal output

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr agent read <TARGET> [OPTIONS]

## Arguments

_Table of options: option, type, required, and what it does._

| opcion | tipo | obligatorio | que hace |
|---|---|---|---|
| <TARGET> | texto | si |  |
| --source <SOURCE> | enum | no | Terminal snapshot source (default: recent) [possible values: visible, recent, recent-unwrapped, detection] |
| --lines <N> | numero | no |  |
| --format <FORMAT> | enum | no | [possible values: text, ansi] |
| --ansi | texto | no |  |

## Returns

_What the command returns on success: JSON shape and location of the payload._

Imprime el texto del terminal directamente en stdout (verificado en 0.9.0 con `--source visible` y `recent-unwrapped`). La API de socket devuelve el texto en `.result.read.text` (doc oficial). En CLI no hay JSON que parsear.

Con `--format ansi` / `--ansi` conserva los escapes de terminal donde la fuente los expone; `detection` es siempre texto plano.

## Returns jq

_jq paths to extract the returned payload into shell variables._



## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
# Lectura completa y sin wraps de la respuesta del agente
herdr agent read reviewer --source recent-unwrapped --lines 120

# Solo lo visible (no mueve el viewport del agente)
herdr agent read reviewer --source visible

# Vista de deteccion: el texto exacto que clasifico el estado (curar en scripts)
herdr agent read reviewer --source detection
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| codigo | significado |
|---|---|
| `agent_not_idle` | Se pidio historial de alternate-screen (`--lines N` > pantalla visible con `recent`/`recent-unwrapped`) mientras el agente esta `working`, `blocked` o `unknown`. Espera a `idle` y reintenta, o usa `--source visible` |
| error JSON en stderr, exit 1 | Agente/pane inexistente o server caido |

## Notes

_Quirks, gotchas, and operational observations not covered above._

- Agentes full-screen (Claude Code, OpenCode) renderizan su historial en la alternate screen: para un agente `idle`, leer `recent`/`recent-unwrapped` con `--lines` mayor a la pantalla usa automaticamente el scroll del agente (requiere que el agente reporte rueda de raton; no mueve el viewport en lecturas `visible`/`detection`/ANSI).
- Las lecturas NO marcan el estado `done` como visto; solo `focus` lo hace (doc oficial).
- Si la respuesta completa no aparece, pedile al agente que escriba el resultado en un archivo Markdown temporal y leer el archivo directamente (doc oficial).

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr agent read --help (herdr 0.9.0)

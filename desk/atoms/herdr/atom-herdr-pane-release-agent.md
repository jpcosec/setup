---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-pane-release-agent
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr pane release-agent
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: pane
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:pane
---

# herdr pane release-agent

## Synopsis

_What the command does, in one or two sentences._

Release pane agent lifecycle authority

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr pane release-agent [OPTIONS] --source <ID> --agent <LABEL> <PANE_ID>

## Arguments

_Table of options: option, type, required, and what it does._

| opcion | tipo | obligatorio | que hace |
|---|---|---|---|
| <PANE_ID> | texto | si |  |
| --source <ID> | texto | no |  |
| --agent <LABEL> | texto | no |  |
| --seq <N> | numero | no |  |

## Returns

_What the command returns on success: JSON shape and location of the payload._

Forma exacta del JSON de exito: `no verificado` (comando de hooks; no ejecutado en vivo). Sigue el patron de los comandos de report (id `cli:pane:*` + `result`) y termina la autoridad de la fuente sobre ese agente/pane.

Doc oficial: "`release-agent` ends that source's lifecycle authority when its agent process exits."

## Returns jq

_jq paths to extract the returned payload into shell variables._



## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
# Hook de salida de un agente: liberar la autoridad que este hook tenia
herdr pane release-agent "$pane_id" --source "hook:codex:session_end" --agent codex
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| codigo / sintoma | significado |
|---|---|
| exit 2 texto plano | Sintaxis invalida: faltan `--source`/`--agent`/`<PANE_ID>` (obligatorios segun el usage) |
| exit 1 JSON en stderr | Error del server (p. ej. `pane_not_found`); codigos del proceso de liberacion: no verificado |

## Notes

_Quirks, gotchas, and operational observations not covered above._

- Es el counterpart de `pane report-agent`: mientras `report-agent` declara `idle`/`working`/`blocked`/`unknown`, `release-agent` simplemente cede el control cuando el agente ya no corre.
- `--seq` sirve para descartar reportes fuera de orden de la misma fuente (stale reports son aceptados por la API pero ignorados por el estado del pane, doc oficial).
- Si el agente sigue vivo tras un release: `no verificado` (comportamiento del server no observado).

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr pane release-agent --help (herdr 0.9.0)

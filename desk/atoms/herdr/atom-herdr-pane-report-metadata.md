---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-pane-report-metadata
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr pane report-metadata
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: pane
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:pane
---

# herdr pane report-metadata

## Synopsis

_What the command does, in one or two sentences._

Report display-only pane metadata

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr pane report-metadata [OPTIONS] --source <ID> <PANE_ID>

## Arguments

_Table of options: option, type, required, and what it does._

| opcion | tipo | obligatorio | que hace |
|---|---|---|---|
| <PANE_ID> | texto | si |  |
| --source <ID> | texto | no |  |
| --agent <LABEL> | texto | no |  |
| --applies-to-source <ID> | texto | no |  |
| --title <TEXT> | texto | no |  |
| --clear-title | texto | no |  |
| --display-agent <TEXT> | texto | no |  |
| --clear-display-agent | texto | no |  |
| --state-label <STATUS=TEXT> | texto | no |  |
| --clear-state-labels | texto | no |  |
| --token <NAME=VALUE> | texto | no |  |
| --clear-token <NAME> | texto | no |  |
| --seq <N> | numero | no |  |
| --ttl-ms <N> | numero | no |  |

## Returns

_What the command returns on success: JSON shape and location of the payload._

Forma exacta del JSON de exito: `no verificado` (comando de hooks; no ejecutado en vivo). Efecto observable: la UI refleja titulo/labels/tokens; el estado `agent_status` NO cambia (es display-only).

## Returns jq

_jq paths to extract the returned payload into shell variables._



## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
# Hook de proceso largo: pintar progreso como token con TTL de 2 minutos
herdr pane report-metadata "$pane_id" \
  --source "hook:runner" \
  --title "bunwv daemon" --state-label working=corriendo \
  --token phase=build --ttl-ms 120000
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| codigo / sintoma | significado |
|---|---|
| exit 2 texto plano | Sintaxis invalida: falta `--source` o `<PANE_ID>`, o `--state-label` sin formato `STATUS=TEXT` |
| exit 1 JSON en stderr | Error del server (p. ej. `pane_not_found`) |

## Notes

_Quirks, gotchas, and operational observations not covered above._

- Normalizacion (doc oficial): se recorta el whitespace, se quitan caracteres de control y `--title`, `--display-agent`, cada `--state-label` y los tokens se limitan a 80 chars. Un token normalizado vacio borra esa clave.
- `--ttl-ms` expira SOLO los tokens actualizados por esa llamada (doc oficial); fuera de rango -> error.
- `--source`/`--applies-to-source` <= 80 chars y solo `[A-Za-z0-9:._-]`.
- Un pane acepta tokens secuenciados de como maximo 32 fuentes distintas en su vida; limpiar/expirar NO libera esos slots (doc oficial).
- `--agent`/`--applies-to-source` NO guardan los token patches: los tokens los gestiona su propia fuente (doc oficial).

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr pane report-metadata --help (herdr 0.9.0)

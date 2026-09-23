---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-pane-split
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr pane split
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: pane
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:pane
---

# herdr pane split

## Synopsis

_What the command does, in one or two sentences._

Split a pane

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr pane split [OPTIONS] [PANE_ID]

## Arguments

_Table of options: option, type, required, and what it does._

| opcion | tipo | obligatorio | que hace |
|---|---|---|---|
| [PANE_ID] | texto | no |  |
| --pane <ID> | texto | no |  |
| --current | texto | no |  |
| --direction <DIRECTION> | enum | no | [possible values: right, down] |
| --ratio <FLOAT> | texto | no |  |
| --cwd <PATH> | texto | no |  |
| --env <KEY=VALUE> | texto | no | Set an environment variable for the launched process |
| --right-click <TARGET> | enum | no | [possible values: herdr, pane] |
| --focus | texto | no |  |
| --no-focus | texto | no |  |

## Returns

_What the command returns on success: JSON shape and location of the payload._

El pane NUEVO en `.result.pane` (verificado en vivo: `split wZ:p1 --direction right` -> pane `wZ:p2`):

```json
{"id":"cli:pane:split","result":{"pane":{"pane_id":"wZ:p2","workspace_id":"wZ","tab_id":"wZ:t1",...},"type":"pane_split"}}
```

```bash
split=$(herdr pane split "$pane_id" --direction right --no-focus)
new_pane=$(printf '%s\n' "$split" | jq -r '.result.pane.pane_id')   # <- CAPTURAR SIEMPRE con jq
```

## Returns jq

_jq paths to extract the returned payload into shell variables._

new_pane=$(printf '%s\n' "$split" | jq -r '.result.pane.pane_id')   # <- CAPTURAR SIEMPRE con jq

## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
# Patron oficial: split + captura del pane nuevo (prohibido predecir el id)
split=$(herdr pane split "$pane_id" --direction right --no-focus)
review_pane=$(printf '%s\n' "$split" | jq -r '.result.pane.pane_id')

# El pane nuevo es una terminal usable: arrancar un agente ahi
herdr agent start reviewer --kind codex --pane "$review_pane" -- -m gpt-5.4
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| codigo / sintoma | significado |
|---|---|
| `pane_not_found` en stderr, exit 1 | Pane a dividir inexistente |
| exit 2 texto plano | Sintaxis invalida (p. ej. `--direction` fuera de `right|down`); `--current` sin `HERDR_PANE_ID` |
| Codigo si el pane destino esta en zoom o es el root de un tab solo: `no verificado` |

## Notes

_Quirks, gotchas, and operational observations not covered above._

- **RUTA CRITICA**: el id del pane nuevo sale en `.result.pane.pane_id`; capturalo con `jq -r` en una variable. NUNCA lo predigas ni lo extraigas con grep (doc oficial + atom-herdr-captura-de-ids).
- La creacion no roba el foco por defecto; `--focus` lo cambia explicitamente (doc oficial).
- Sin `--cwd`, el nuevo terminal sigue la politica `terminal.new_cwd` (sigue al pane/workspace fuente por defecto).
- Cada `--env` agrega/reemplaza una variable para el proceso nuevo; `HERDR_PANE_ID`, `HERDR_TAB_ID`, `HERDR_WORKSPACE_ID` siguen siendo autoritativos si chocan (doc oficial).
- `pane split` crea terminal y layout; `agent start` NO crea layout (ver atom-herdr-pane-vs-agent).

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr pane split --help (herdr 0.9.0)

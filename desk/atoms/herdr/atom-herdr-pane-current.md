---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-pane-current
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr pane current
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: pane
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:pane
---

# herdr pane current

## Synopsis

_What the command does, in one or two sentences._

Show the current pane

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr pane current [OPTIONS]

## Arguments

_Table of options: option, type, required, and what it does._

| opcion | tipo | obligatorio | que hace |
|---|---|---|---|
| --pane <ID> | texto | no |  |
| --current | texto | no |  |

## Returns

_What the command returns on success: JSON shape and location of the payload._

El pane completo (verificado en vivo). Forma:

```json
{"id":"cli:pane:current","result":{"pane":{...},"type":"pane_current"}}
```

```bash
herdr pane current | jq -r '.result.pane.pane_id'   # pane llamador
```

Campos de `.result.pane` (iguales a `pane get`): `pane_id`, `workspace_id`, `tab_id`, `terminal_id`, `cwd`, `foreground_cwd`, `agent`, `agent_status`, `focused`, `revision`, `scroll{max_offset_from_bottom,offset_from_bottom,viewport_rows}`, `terminal_title`, `terminal_title_stripped`.

## Returns jq

_jq paths to extract the returned payload into shell variables._

herdr pane current | jq -r '.result.pane.pane_id'   # pane llamador

## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
# Desde dentro de un pane herdr, saber cual soy y en que workspace estoy
me=$(herdr pane current | jq -r '.result.pane.pane_id')
ws=$(herdr pane current | jq -r '.result.pane.workspace_id')
echo "soy $me en $ws"
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| codigo / sintoma | significado |
|---|---|
| Error con `--current` cuando no hay `HERDR_PANE_ID` | La doc oficial: "errors when HERDR_PANE_ID is unavailable"; codigo exacto no verificado |
| exit 2 texto plano | Sintaxis invalida del CLI |
| exit 1 JSON en stderr (p. ej. `pane_not_found`) | Error del server; con `--pane <id>` inexistente |

## Notes

_Quirks, gotchas, and operational observations not covered above._

- `HERDR_PANE_ID` lo inyecta herdr a todo proceso lanzado en un pane; fuera de un pane no existe (p. ej. en una terminal normal).
- `pane get` con id posicional y `pane current` sin id son equivalentes en resultado: misma forma de pane.
- Los panes remotos via `--machine` no heredan el `--current` local: usa ids remotos explicitos (doc oficial).

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr pane current --help (herdr 0.9.0)

---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-workspace-rename
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr workspace rename
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: workspace
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:workspace
---

# herdr workspace rename

## Synopsis

_What the command does, in one or two sentences._

Rename a workspace

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr workspace rename <WORKSPACE_ID> <LABEL>...

## Arguments

_Table of options: option, type, required, and what it does._

| opcion | tipo | obligatorio | que hace |
|---|---|---|---|
| <WORKSPACE_ID> | texto | si |  |
| <LABEL>... | texto | si |  |

## Returns

_What the command returns on success: JSON shape and location of the payload._

Forma exacta del JSON de exito: **no verificado** (no se echaron renombres reales sobre el entorno vivo). El server emite el evento `workspace.renamed`.

## Returns jq

_jq paths to extract the returned payload into shell variables._



## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
# Renombrar el workspace cuyo id capturamos con jq
ws=$(herdr workspace list | jq -r '.result.workspaces[] | select(.label=="legos") | .workspace_id')
herdr workspace rename "$ws" "legos-v2"
# El label variadico une palabras: esto equivale a la linea anterior sin comillas
herdr workspace rename "$ws" legos v2
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| codigo | significado |
|---|---|
| `workspace_not_found` | Id inexistente; verificado: `{"error":{"code":"workspace_not_found","message":"workspace w999 not found"},"id":"cli:workspace:rename"}` en stderr con exit 1 |
| exit 2 con `usage: herdr workspace rename <workspace_id> <label>` | Faltan argumentos (verificado ejecutando sin args) |

## Notes

_Quirks, gotchas, and operational observations not covered above._

- El label es variadico: `herdr workspace rename w1 a b c` pone "a b c". Las comillas son opcionales pero se recomiendan para no depender del shell-splitting.
- Los ids de workspace no cambian con el rename; el label es solo presentacion.

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr workspace rename --help (herdr 0.9.0)

---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-tab-rename
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr tab rename
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: tab
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:tab
---

# herdr tab rename

## Synopsis

_What the command does, in one or two sentences._

Rename a tab

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr tab rename <TAB_ID> <LABEL>...

## Arguments

_Table of options: option, type, required, and what it does._

| opcion | tipo | obligatorio | que hace |
|---|---|---|---|
| <TAB_ID> | texto | si |  |
| <LABEL>... | texto | si |  |

## Returns

_What the command returns on success: JSON shape and location of the payload._

Forma exacta del JSON de exito: **no verificado** (no se echaron renombres reales sobre el entorno vivo). El server emite el evento `tab.renamed`.

## Returns jq

_jq paths to extract the returned payload into shell variables._



## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
# Renombrar el tab cuyo id capturamos con jq
tab=$(herdr tab list | jq -r '.result.tabs[] | select(.label=="1") | .tab_id' | head -1)
herdr tab rename "$tab" "editor"
# el label variadico une palabras: tambien funciona sin comillas
herdr tab rename "$tab" panel tests
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| codigo | significado |
|---|---|
| `tab_not_found` | Id inexistente; verificado: `{"error":{"code":"tab_not_found","message":"tab wX:nope not found"},"id":"cli:tab:rename"}` en stderr con exit 1 |
| exit 2 con `usage: herdr tab rename <tab_id> <label>` | Faltan argumentos (verificado ejecutando sin args) |

## Notes

_Quirks, gotchas, and operational observations not covered above._

- El label es variadico: `herdr tab rename w1:t1 a b c` pone "a b c".
- `tab_id` no cambia con el rename; el label es solo presentacion.
- Como los labels se repiten entre tabs, filtra por label solo cuando sea unico o usa `--workspace` para acotar.

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr tab rename --help (herdr 0.9.0)

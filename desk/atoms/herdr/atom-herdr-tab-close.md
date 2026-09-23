---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-tab-close
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr tab close
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: tab
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:tab
---

# herdr tab close

## Synopsis

_What the command does, in one or two sentences._

Close a tab

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr tab close <tab_id>

## Arguments

_Table of options: option, type, required, and what it does._

| opcion | tipo | obligatorio | que hace |
|---|---|---|---|
| <tab_id> | texto | si |  |

## Returns

_What the command returns on success: JSON shape and location of the payload._

Forma exacta del JSON de exito: **no verificado** (no se cerro ningun tab real del entorno). El server emite el evento `tab.closed`.

## Returns jq

_jq paths to extract the returned payload into shell variables._



## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
# Cerrar un tab creado por nosotros, por id capturado con jq
created=$(herdr tab create --label scratch --no-focus)
tab_id=$(printf '%s' "$created" | jq -r '.result.tab.tab_id')
herdr tab close "$tab_id"
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| codigo | significado |
|---|---|
| `tab_not_found` | Id inexistente; verificado: `{"error":{"code":"tab_not_found","message":"tab wX:nope not found"},"id":"cli:tab:close"}` en stderr con exit 1 |
| `confirmation_required` | Cerrar un tab que tambien cerria un grupo de worktrees completo con `confirm_close` activado (doc oficial; no reproducible en el entorno actual) |

## Notes

_Quirks, gotchas, and operational observations not covered above._

- **Cerrar el ultimo tab de un workspace tambien cierra el workspace** (doc oficial, coincide con la accion close-tab del TUI).
- Cerrar un tab mata los procesos de sus panes; valida el id contra la lista real antes de cerrar.

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr tab close --help (herdr 0.9.0)

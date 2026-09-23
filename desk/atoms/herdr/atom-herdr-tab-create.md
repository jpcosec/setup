---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-tab-create
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr tab create
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: tab
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:tab
---

# herdr tab create

## Synopsis

_What the command does, in one or two sentences._

Create a tab

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr tab create [OPTIONS]

## Arguments

_Table of options: option, type, required, and what it does._

| opcion | tipo | obligatorio | que hace |
|---|---|---|---|
| --workspace <WORKSPACE_ID> | texto | no |  |
| --cwd <PATH> | texto | no |  |
| --label <TEXT> | texto | no |  |
| --env <KEY=VALUE> | texto | no | Set an environment variable for the launched process |
| --focus | texto | no |  |
| --no-focus | texto | no |  |

## Returns

_What the command returns on success: JSON shape and location of the payload._

Devuelve el tab y su root pane a la vez (fuente: doc oficial y spec):

```json
{
  "result": {
    "tab": { "tab_id": "wX:tG", ... },
    "root_pane": { "pane_id": "wX:tG:p1", ... }
  }
}
```

Rutas jq exactas (la forma correcta de obtener un pane usable):

```bash
jq -r '.result.tab.tab_id'            # -> ID del tab creado
jq -r '.result.root_pane.pane_id'     # -> ID del root pane (primer terminal usable del tab)
```

El campo `type` exacto de la respuesta de create: no verificado (get devuelve `tab_info`).

## Returns jq

_jq paths to extract the returned payload into shell variables._

Rutas jq exactas (la forma correcta de obtener un pane usable):
jq -r '.result.tab.tab_id'            # -> ID del tab creado
jq -r '.result.root_pane.pane_id'     # -> ID del root pane (primer terminal usable del tab)

## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
ws=$(herdr workspace list | jq -r '.result.workspaces[0].workspace_id')
created=$(herdr tab create --workspace "$ws" --cwd ~/proyectos/legos --label tests --no-focus)
tab_id=$(printf '%s' "$created" | jq -r '.result.tab.tab_id')
pane_id=$(printf '%s' "$created" | jq -r '.result.root_pane.pane_id')
echo "tab=$tab_id pane=$pane_id"
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| codigo | significado |
|---|---|
| `{"error":{"code":"...","message":"..."},"id":"cli:tab:create"}` en stderr, exit 1 | Error del server |
| exit 2 texto plano | Sintaxis invalida del CLI |
| error cuando no hay workspace activo y no se pasa `--workspace` | no verificado; doc oficial: "fails if none exists" |

## Notes

_Quirks, gotchas, and operational observations not covered above._

- Sin `--cwd`, el nuevo terminal sigue la politica `terminal.new_cwd`.
- Cada `--env` agrega o reemplaza una variable en el shell raiz; herdr inyecta ademas `HERDR_WORKSPACE_ID`, `HERDR_TAB_ID`, `HERDR_PANE_ID`.
- El label de tab NO es un identificador: claves siempre por `tab_id`.

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr tab create --help (herdr 0.9.0)

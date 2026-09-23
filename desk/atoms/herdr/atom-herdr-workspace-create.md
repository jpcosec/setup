---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-workspace-create
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr workspace create
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: workspace
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:workspace
---

# herdr workspace create

## Synopsis

_What the command does, in one or two sentences._

Create a workspace

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr workspace create [OPTIONS]

## Arguments

_Table of options: option, type, required, and what it does._

| opcion | tipo | obligatorio | que hace |
|---|---|---|---|
| --cwd <PATH> | texto | no |  |
| --label <TEXT> | texto | no |  |
| --env <KEY=VALUE> | texto | no | Set an environment variable for the launched process |
| --focus | texto | no |  |
| --no-focus | texto | no |  |

## Returns

_What the command returns on success: JSON shape and location of the payload._

Devuelve los TRES objetos a la vez (fuente: doc oficial y spec):

```json
{
  "result": {
    "workspace": { "workspace_id": "wX", ... },
    "tab": { "tab_id": "wX:t1", ... },
    "root_pane": { "pane_id": "wX:t1:p1", ... }
  }
}
```

Rutas jq exactas (esta es la forma correcta de obtener un pane usable):

```bash
jq -r '.result.workspace.workspace_id'   # -> ID del workspace
jq -r '.result.tab.tab_id'               # -> ID del primer tab
jq -r '.result.root_pane.pane_id'        # -> ID del root pane (primer terminal usable)
```

El campo `type` exacto de la respuesta de create: no verificado (get devuelve `workspace_info`).

## Returns jq

_jq paths to extract the returned payload into shell variables._

Rutas jq exactas (esta es la forma correcta de obtener un pane usable):
jq -r '.result.workspace.workspace_id'   # -> ID del workspace
jq -r '.result.tab.tab_id'               # -> ID del primer tab
jq -r '.result.root_pane.pane_id'        # -> ID del root pane (primer terminal usable)

## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
created=$(herdr workspace create --cwd ~/proyectos/legos --label legos --no-focus)
ws_id=$(printf '%s' "$created" | jq -r '.result.workspace.workspace_id')
tab_id=$(printf '%s' "$created" | jq -r '.result.tab.tab_id')
pane_id=$(printf '%s' "$created" | jq -r '.result.root_pane.pane_id')
echo "workspace=$ws_id tab=$tab_id pane=$pane_id"
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| codigo | significado |
|---|---|
| `{"error":{"code":"...","message":"..."},"id":"cli:workspace:create"}` en stderr, exit 1 | Error del server |
| exit 2 texto plano | Sintaxis invalida del CLI |
| errores especificos de create (labels duplicados, cwd invalido) | no verificado |

## Notes

_Quirks, gotchas, and operational observations not covered above._

- Sin `--cwd`, el nuevo terminal sigue la politica `terminal.new_cwd` (por defecto: seguir la source pane o workspace).
- Cada `--env` agrega o reemplaza una variable en el shell raiz; herdr inyecta ademas `HERDR_SOCKET_PATH`, `HERDR_ENV=1`, `HERDR_WORKSPACE_ID`, `HERDR_TAB_ID`, `HERDR_PANE_ID`.
- Para no robar el foco en scripts de boot (como init-herdr.sh), usa `--no-focus`.

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr workspace create --help (herdr 0.9.0)

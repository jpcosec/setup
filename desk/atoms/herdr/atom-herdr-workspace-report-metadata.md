---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-workspace-report-metadata
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr workspace report-metadata
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: workspace
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:workspace
---

# herdr workspace report-metadata

## Synopsis

_What the command does, in one or two sentences._

Report display-only workspace metadata

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr workspace report-metadata [OPTIONS] --source <ID> <WORKSPACE_ID>

## Arguments

_Table of options: option, type, required, and what it does._

| opcion | tipo | obligatorio | que hace |
|---|---|---|---|
| <WORKSPACE_ID> | texto | si |  |
| --source <ID> | texto | no |  |
| --token <NAME=VALUE> | texto | no |  |
| --clear-token <NAME> | texto | no |  |
| --seq <N> | numero | no |  |
| --ttl-ms <N> | numero | no |  |

## Returns

_What the command returns on success: JSON shape and location of the payload._

Forma exacta del JSON de exito: **no verificado** en esta version. La doc oficial indica que emite el evento `workspace.metadata_updated` y que los tokens quedan visibles en `workspace get`/`workspace list` bajo `.result.workspace.tokens` (mapa nombre->valor).

Ruta jq para leer el resultado del reporte:

```bash
herdr workspace get wX | jq -r '.result.workspace.tokens'                # mapa completo
herdr workspace get wX | jq -r '.result.workspace.tokens."kk:status"'   # un token (quoted si lleva ":" o ".")
```

## Returns jq

_jq paths to extract the returned payload into shell variables._

Ruta jq para leer el resultado del reporte:
herdr workspace get wX | jq -r '.result.workspace.tokens'                # mapa completo
herdr workspace get wX | jq -r '.result.workspace.tokens."kk:status"'   # un token (quoted si lleva ":" o ".")

## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
ws=$(herdr workspace list | jq -r '.result.workspaces[0].workspace_id')
herdr workspace report-metadata "$ws" --source "user:setup" --token "estado=2 cambios" --ttl-ms 60000
herdr workspace get "$ws" | jq -r '.result.workspace.tokens."user:setup" // "sin token"'
# limpiar
herdr workspace report-metadata "$ws" --source "user:setup" --clear-token estado
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| codigo | significado |
|---|---|
| exit 2 `missing token to set or clear` | Se paso `--source` sin `--token` ni `--clear-token` (verificado) |
| `workspace_not_found` | Id de workspace inexistente (mismo patron que get; no re-verificado para este subcomando) |
| error de validacion de `--source`/`--ttl-ms` fuera de rango | no verificado; la doc limita source a 80 chars y ttl a 1..86400000 ms |

## Notes

_Quirks, gotchas, and operational observations not covered above._

- Los tokens son display-only: no afectan waits, notificaciones ni rollups (esa semantica pertenece a `pane report-agent`).
- Los valores se normalizan: recorte de espacios, sin caracteres de control, max 80 chars; valor vacio = borrar la clave.
- Un workspace acepta tokens secuenciados de max 32 fuentes distintas en su vida util (doc oficial).

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr workspace report-metadata --help (herdr 0.9.0)

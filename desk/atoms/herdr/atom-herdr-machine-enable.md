---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-machine-enable
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr machine enable
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: machine
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:machine
---

# herdr machine enable

## Synopsis

_What the command does, in one or two sentences._

Enable a saved SSH machine

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr machine enable <PROFILE_ID>

## Arguments

_Table of options: option, type, required, and what it does._

| opcion | tipo | obligatorio | que hace |
|---|---|---|---|
| <PROFILE_ID> | texto | si |  |

## Returns

_What the command returns on success: JSON shape and location of the payload._

JSON `cli:machine:enable` con `result.type: ok` (shape del `.result` no verificado: no ejecutado, no hay perfiles en este setup). Los perfiles habilitados conectan en segundo plano (doc oficial).

## Returns jq

_jq paths to extract the returned payload into shell variables._



## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
# Reactivar un perfil deshabilitado
PID=$(herdr machine list --json | jq -r '.[] | select(.disabled == true) | .id' | head -1)
herdr machine enable "$PID"
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| Codigo | Significado |
| --- | --- |
| perfil inexistente o ya activo | Mensaje exacto no verificado |
| `remote server is not ready for saved machines` | El remoto dejo de estar preparado |

## Notes

_Quirks, gotchas, and operational observations not covered above._

- El campo `.disabled` en `machine list --json` es la forma esperada de detectar perfiles deshabilitados; no verificado el nombre exacto del campo (lista vacia en este setup).
- Renombrar no reconecta; `enable` tras `disable` si (doc oficial).
- Las sesiones remotas nunca se detienen al deshabilitar: `enable` simplemente vuelve a conectar el cliente.

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr machine enable --help (herdr 0.9.0)

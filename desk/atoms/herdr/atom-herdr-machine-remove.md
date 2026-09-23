---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-machine-remove
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr machine remove
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: machine
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:machine
---

# herdr machine remove

## Synopsis

_What the command does, in one or two sentences._

Remove a saved SSH machine

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr machine remove <PROFILE_ID>

## Arguments

_Table of options: option, type, required, and what it does._

| opcion | tipo | obligatorio | que hace |
|---|---|---|---|
| <PROFILE_ID> | texto | si |  |

## Returns

_What the command returns on success: JSON shape and location of the payload._

JSON `cli:machine:remove` con `result.type: ok` (shape del `.result` no verificado: no ejecutado, sin perfiles en este setup).

## Returns jq

_jq paths to extract the returned payload into shell variables._



## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
# Borrar el perfil "Build machine" si existe
PID=$(herdr machine list --json | jq -r '.[] | select(.label == "Build machine") | .id')
test -n "$PID" && herdr machine remove "$PID"
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| Codigo | Significado |
| --- | --- |
| perfil inexistente | Mensaje exacto no verificado |
| `endpoint selection is absent or disabled` | Intento de eliminar cuando no hay seleccion valida |

## Notes

_Quirks, gotchas, and operational observations not covered above._

- Verificado en doc oficial: eliminar desconecta al cliente de esa maquina pero NO detiene las sesiones remotas que siguen vivas en el remoto.
- Si se elimina la maquina que se esta viendo, el cliente vuelve a Local.
- En este setup no hay perfiles que eliminar (2026-09-23).

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr machine remove --help (herdr 0.9.0)

---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-machine-disable
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr machine disable
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: machine
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:machine
---

# herdr machine disable

## Synopsis

_What the command does, in one or two sentences._

Disable a saved SSH machine

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr machine disable <PROFILE_ID>

## Arguments

_Table of options: option, type, required, and what it does._

| opcion | tipo | obligatorio | que hace |
|---|---|---|---|
| <PROFILE_ID> | texto | si |  |

## Returns

_What the command returns on success: JSON shape and location of the payload._

JSON `cli:machine:disable` con `result.type: ok` (shape inferido del tipo `Ok` del protocolo; no ejecutado: no hay perfiles en este setup). Deshabilitar desconecta el cliente de esa maquina pero deja las sesiones remotas corriendo (doc oficial).

## Returns jq

_jq paths to extract the returned payload into shell variables._



## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
# Deshabilitar el primer perfil de la lista
PID=$(herdr machine list --json | jq -r '.[0].id')
herdr machine disable "$PID"
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| Codigo | Significado |
| --- | --- |
| perfil inexistente | `herdr machine disable <id>` falla; mensaje exacto no verificado |
| `endpoint selection is absent or disabled` | No hay perfil Local/a seleccion seleccionada (string del binario, contexto de catalogo) |

## Notes

_Quirks, gotchas, and operational observations not covered above._

- No elimina el perfil: `herdr machine enable` lo reactiva.
- Los cambios de perfiles se aplican solos a los clientes TUI abiertos en ~1 segundo (doc oficial).
- En este setup no hay perfiles: `herdr machine list --json` = `[]` (verificado 2026-09-23), asi que la forma del `.result` queda como no verificado.

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr machine disable --help (herdr 0.9.0)

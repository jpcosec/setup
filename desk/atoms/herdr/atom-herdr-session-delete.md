---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-session-delete
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr session delete
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: session
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:session
---

# herdr session delete

## Synopsis

_What the command does, in one or two sentences._

Delete a stopped session

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr session delete [OPTIONS] <NAME>

## Arguments

_Table of options: option, type, required, and what it does._

| opcion | tipo | obligatorio | que hace |
|---|---|---|---|
| <NAME> | texto | si |  |
| --json | texto | no |  |

## Returns

_What the command returns on success: JSON shape and location of the payload._

JSON **sin wrapper** `.result` — la respuesta queda en el nivel raiz (verificado en 0.9.0). La operacion es **idempotente**: borrar una sesion inexistente devuelve exito:

```json
{
  "deleted": true,
  "session": {
    "name": "nosuch-session", "default": false, "running": false,
    "session_dir": "/home/jp/.config/herdr/sessions/nosuch-session",
    "socket_path": "/home/jp/.config/herdr/sessions/nosuch-session/herdr.sock"
  }
}
```

Ruta jq exacta:

```bash
herdr session delete foo --json | jq -r '.deleted'          # -> true
herdr session delete foo --json | jq -r '.session.name'
```

## Returns jq

_jq paths to extract the returned payload into shell variables._

Ruta jq exacta:
herdr session delete foo --json | jq -r '.deleted'          # -> true
herdr session delete foo --json | jq -r '.session.name'

## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
# Borrar una sesion parada; verificar el campo deleted
herdr session delete scratch-session --json | jq -r '.deleted'
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| codigo | significado |
|---|---|
| Borrar sesion inexistente | **No es error**: devuelve `{"deleted":true,...}` con exit 0 (idempotente; verificado) |
| Borrar una sesion en ejecucion | no verificado (la sesion default corre en este entorno y NO se toco) |

## Notes

_Quirks, gotchas, and operational observations not covered above._

- El comando se llama "delete a **stopped** session": para sesiones corriendo primero `herdr session stop <NAME>`.
- Nunca borres la sesion `default` en un entorno vivo: es la sesion principal del server.
- El JSON de sesiones no sigue el contrato `.result` de workspace/tab: es un shape propio.

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr session delete --help (herdr 0.9.0)

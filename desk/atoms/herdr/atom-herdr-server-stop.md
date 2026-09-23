---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-server-stop
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr server stop
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: server
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:server
---

# herdr server stop

## Synopsis

_What the command does, in one or two sentences._

Stop the running server

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr server stop

## Arguments

_Table of options: option, type, required, and what it does._



## Returns

_What the command returns on success: JSON shape and location of the payload._

No verificado: no se ejecuto (detener el server mata los procesos de los panes). Esperado: JSON `cli:server:stop` confirmando el apagado, o error si no hay server.

## Returns jq

_jq paths to extract the returned payload into shell variables._



## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
# Parada controlada por socket (equivalente a salir de herdr con el server detached)
herdr server stop

# Verificar que quedo caido
herdr status server --json | jq -r '.server.running'   # false
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| Codigo | Significado |
| --- | --- |
| `server_unavailable` | Ya no hay server corriendo ("server is shutting down" / "server is not running") |
| `confirmation_required` | No verificado; el stop por CLI no muestra confirmacion en el --help |

## Notes

_Quirks, gotchas, and operational observations not covered above._

- El skill oficial es explicito: nunca ejecutar `herdr server stop` desde una sesion activa salvo que el usuario quiera detener el server y sus procesos de pane.
- Detener el servidor pierde todo el contenido de terminal en memoria: scrollbacks y pantallas alternas (ver `atom-herdr-no-guarda-traza`). El layout se restaura en el siguiente arranque via `persist.restore`.
- El apagado deja rastro `app.shutdown` en `herdr-server.log` (verificado: 19 eventos en el log actual).

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr server stop --help (herdr 0.9.0)

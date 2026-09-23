---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-notification-show
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr notification show
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: notification
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:notification
---

# herdr notification show

## Synopsis

_What the command does, in one or two sentences._

Show a notification

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr notification show [OPTIONS] <TITLE>

## Arguments

_Table of options: option, type, required, and what it does._

| opcion | tipo | obligatorio | que hace |
|---|---|---|---|
| <TITLE> | texto | si |  |
| --body <TEXT> | texto | no |  |
| --position <POSITION> | enum | no | [possible values: top-left, top-right, bottom-left, bottom-right] |
| --sound <SOUND> | enum | no | [possible values: none, done, request] |

## Returns

_What the command returns on success: JSON shape and location of the payload._

JSON (verificado, herdr 0.9.0):

```json
{"id":"cli:notification:show","result":{"reason":"shown","shown":true,"type":"notification_show"}}
```

Rutas jq utiles:

```bash
jq -r '.result.shown'    # true si se mostro
jq -r '.result.reason'   # "shown"
```

## Returns jq

_jq paths to extract the returned payload into shell variables._

Rutas jq utiles:
jq -r '.result.shown'    # true si se mostro
jq -r '.result.reason'   # "shown"

## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
# Avisar al usuario cuando acaba una tarea larga (desde un pane de agente)
herdr notification show "Pipeline listo" --body "42 tests OK" --sound done \
  | jq -r '.result.shown'

# Notificacion silenciosa en una esquina concreta
herdr notification show "Atencion" --position bottom-right --sound request \
  | jq -r '.result.shown'
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| Codigo | Significado |
| --- | --- |
| `notification title is empty` | Titulo vacio (string del binario) |
| `notification.show` sin server | `server_unavailable`: el server no esta corriendo |
| valor invalido en `--position`/`--sound` | Error de validacion de clap con los posibles values del help |

## Notes

_Quirks, gotchas, and operational observations not covered above._

- Verificado 2026-09-23: ejecutado real, `show` devolvio `shown: true` con `--sound none`.
- `--position` solo afecta a los toasts dentro de la TUI de herdr; el sonido se reproduce solo si la notificacion se muestra (doc oficial).
- Usa la entrega configurada en `[ui.toast]` (doc oficial).
- `notification.show` SI genera linea `method="notification.show"` en el log del server (es una llamada con efectos de UI: cambios verificados en el log real).

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr notification show --help (herdr 0.9.0)

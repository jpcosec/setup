---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-session-list
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr session list
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: session
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:session
---

# herdr session list

## Synopsis

_What the command does, in one or two sentences._

List sessions

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr session list [OPTIONS]

## Arguments

_Table of options: option, type, required, and what it does._

| opcion | tipo | obligatorio | que hace |
|---|---|---|---|
| --json | texto | no |  |

## Returns

_What the command returns on success: JSON shape and location of the payload._

**Sin** `--json`: tabla humana `name | status | directory | socket` (verificado).

Con `--json`: JSON **sin wrapper** `.result` — la lista queda en el nivel raiz (verificado en 0.9.0):

```json
{
  "sessions": [
    { "default": true, "name": "default", "running": true,
      "session_dir": "/home/jp/.config/herdr",
      "socket_path": "/home/jp/.config/herdr/herdr.sock" }
  ]
}
```

Ruta jq exacta (ojo: la sesion NO tiene `.result`):

```bash
herdr session list --json | jq -r '.sessions[].name'
herdr session list --json | jq -r '.sessions[] | select(.running) | .socket_path'
```

## Returns jq

_jq paths to extract the returned payload into shell variables._

Ruta jq exacta (ojo: la sesion NO tiene `.result`):
herdr session list --json | jq -r '.sessions[].name'
herdr session list --json | jq -r '.sessions[] | select(.running) | .socket_path'

## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
# Sesiones en ejecucion, socket por linea
herdr session list --json | jq -r '.sessions[] | select(.running) | "\(.name)\t\(.socket_path)"'
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| codigo | significado |
|---|---|
| Los errores de sesion se imprimen como `{"error":{"code":"...","message":"..."}}` **sin campo `id`** (difieren de workspace/tab) y con exit 1 — verificado en `session stop` |

## Notes

_Quirks, gotchas, and operational observations not covered above._

- Cada sesion tiene su propio socket: `~/.config/herdr/herdr.sock` (default) o `~/.config/herdr/sessions/<name>/herdr.sock`.
- `default` es la sesion implicita; doc oficial: usa `default` como nombre para pararla explicitamente.
- La sesion es quien define el scope de IDs: los ids de workspace/tab/pane de una sesion no valen en otra.

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr session list --help (herdr 0.9.0)

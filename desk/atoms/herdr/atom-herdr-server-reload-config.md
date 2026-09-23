---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-server-reload-config
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr server reload-config
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: server
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:server
---

# herdr server reload-config

## Synopsis

_What the command does, in one or two sentences._

Reload config in the running server

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr server reload-config

## Arguments

_Table of options: option, type, required, and what it does._



## Returns

_What the command returns on success: JSON shape and location of the payload._

JSON (verificado, herdr 0.9.0):

```json
{"id":"cli:server:reload-config","result":{"diagnostics":[],"status":"applied","type":"config_reload"}}
```

Rutas jq utiles:

```bash
jq -r '.result.status'          # applied | errores
jq -r '.result.diagnostics[]'   # lista de problemas de la config (vacia = bien)
```

## Returns jq

_jq paths to extract the returned payload into shell variables._

Rutas jq utiles:
jq -r '.result.status'          # applied | errores
jq -r '.result.diagnostics[]'   # lista de problemas de la config (vacia = bien)

## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
# Editar ~/.config/herdr/config.toml y recargar en caliente
herdr server reload-config | jq -r '.result.status, .result.diagnostics[]'
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| Codigo | Significado |
| --- | --- |
| `server_unavailable` | Server caido: nada que recargar |
| diagnostics no vacio | La config nueva tiene problemas parciales; `server reload-config` los lista y aplica lo aplicable |

## Notes

_Quirks, gotchas, and operational observations not covered above._

- Verificado 2026-09-23: ejecutado real, devolvio `status: applied`, `diagnostics: []`, exit 0.
- No reinicia panes (doc oficial); ajustes como `terminal.kitty_graphics` avisan que requieren reinicio completo (mensaje del binario: "requires restarting Herdr; kept current setting").
- El comando aparece en el log del server como `method="server.reload_config"` con `changes_ui=false`.

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr server reload-config --help (herdr 0.9.0)

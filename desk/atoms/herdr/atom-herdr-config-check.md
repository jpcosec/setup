---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-config-check
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr config check
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: config
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:config
---

# herdr config check

## Synopsis

_What the command does, in one or two sentences._

Validate config.toml and print diagnostics

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr config check

## Arguments

_Table of options: option, type, required, and what it does._



## Returns

_What the command returns on success: JSON shape and location of the payload._

Texto plano, no JSON (verificado, exit 0):

```text
config: ok
```

Con problemas, imprimiria diagnosticos de la config; la forma exacta del texto de error no esta verificada en este setup (la config local es valida).

## Returns jq

_jq paths to extract the returned payload into shell variables._



## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
# Comprobar que el config local es valido antes de tocar nada
herdr config check && echo "config valida"

# Y comparar con el default completo del binario
herdr --default-config | grep -c '^#'   # cuantos comentarios de referencia hay
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| Codigo | Significado |
| --- | --- |
| `config parse error, using defaults` | La config no parsea y se usan defaults (string del binario) |
| `config read error, using defaults` | No se puede leer el archivo de config (string del binario) |
| exit != 0 | `config check` reporta fallo; parsear el texto de diagnostico |

## Notes

_Quirks, gotchas, and operational observations not covered above._

- Config local de este setup: `~/.config/herdr/config.toml` tiene 51 bytes (minima, sin keybindings custom) — verificada valida el 2026-09-23.
- `herdr server reload-config` aplica la config al server corriendo SIN reiniciar panes; `config check` solo valida sin tocar el server.

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr config check --help (herdr 0.9.0)

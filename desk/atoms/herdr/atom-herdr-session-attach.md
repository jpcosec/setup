---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-session-attach
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr session attach
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: session
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:session
---

# herdr session attach

## Synopsis

_What the command does, in one or two sentences._

Attach to a session

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr session attach <NAME>

## Arguments

_Table of options: option, type, required, and what it does._

| opcion | tipo | obligatorio | que hace |
|---|---|---|---|
| <NAME> | texto | si |  |

## Returns

_What the command returns on success: JSON shape and location of the payload._

No devuelve JSON: abre el TUI de herdr sobre la sesion (modo interactivo, terminal completa). El nulo de salida JSON no aplica.

## Returns jq

_jq paths to extract the returned payload into shell variables._



## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
# Adjuntarse a la sesion "default" desde una terminal interactiva
herdr session attach default
# Salir del TUI: prefix ctrl+b, luego q
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| codigo | significado |
|---|---|
| "nested herdr is disabled by default" + exit 1 | Ejecutar attach sin terminal interactiva (p. ej. dentro de otro herdr o en un script); verificado en 0.9.0: `error: nested herdr is disabled by default. see configuration if you want to enable it.` |

## Notes

_Quirks, gotchas, and operational observations not covered above._

- Necesita TTY: desde un script o sub-shell falla con el error "nested herdr".
- Para lanzar/crear una sesion nombrada se usa el flag global `herdr --session <name>` al arrancar, no `session attach`.
- La sesion debe estar corriendo (ver `herdr session list --json | jq -r '.sessions[].name'`); adjuntarse a una parada: no verificado.

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr session attach --help (herdr 0.9.0)

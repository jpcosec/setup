---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-session-stop
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr session stop
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: session
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:session
---

# herdr session stop

## Synopsis

_What the command does, in one or two sentences._

Stop a session

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr session stop [OPTIONS] <NAME>

## Arguments

_Table of options: option, type, required, and what it does._

| opcion | tipo | obligatorio | que hace |
|---|---|---|---|
| <NAME> | texto | si |  |
| --json | texto | no |  |

## Returns

_What the command returns on success: JSON shape and location of the payload._

Forma exacta del JSON de exito: **no verificado** (no se detuvo ninguna sesion real del entorno; la default esta corriendo). Los errores SÍ estan verificados (ver abajo).

## Returns jq

_jq paths to extract the returned payload into shell variables._



## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
# Detener solo si la sesion esta corriendo (jq, nunca predecir)
running=$(herdr session list --json | jq -r '.sessions[] | select(.name=="default") | .running')
if [ "$running" = "true" ]; then herdr session stop default --json; fi
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| codigo | significado |
|---|---|
| `session_stop_failed` | La sesion no esta corriendo o es inalcanzable; verificado: `{"error":{"code":"session_stop_failed","message":"session nosuch-session is not running or cannot be reached at /home/jp/.config/herdr/sessions/nosuch-session/herdr.sock: No such file or directory (os error 2)"}}` con exit 1 |

## Notes

_Quirks, gotchas, and operational observations not covered above._

- **Los errores de sesion NO llevan campo `id`** en el JSON (a diferencia de workspace/tab) y van por stderr con exit 1 — verificado.
- Parar una sesion mata sus panes y procesos: comprueba `session list --json` antes.
- Doc oficial: usa `default` como nombre para parar la sesion implicita explicitamente.

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr session stop --help (herdr 0.9.0)

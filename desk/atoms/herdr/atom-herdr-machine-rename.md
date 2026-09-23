---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-machine-rename
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr machine rename
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: machine
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:machine
---

# herdr machine rename

## Synopsis

_What the command does, in one or two sentences._

Rename a saved SSH machine

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr machine rename --label <LABEL> <PROFILE_ID>

## Arguments

_Table of options: option, type, required, and what it does._

| opcion | tipo | obligatorio | que hace |
|---|---|---|---|
| <PROFILE_ID> | texto | si |  |
| --label <LABEL> | texto | no | Set the machine label shown in the sidebar |

## Returns

_What the command returns on success: JSON shape and location of the payload._

JSON `cli:machine:rename` con `result.type: ok` (shape del `.result` no verificado: no ejecutado, sin perfiles en este setup). Renombrar no reconecta ni deshabilita (doc oficial: "renaming does not reconnect").

## Returns jq

_jq paths to extract the returned payload into shell variables._



## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
# Renombrar el primer perfil
PID=$(herdr machine list --json | jq -r '.[0].id')
herdr machine rename --label "Nueva etiqueta" "$PID"
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| Codigo | Significado |
| --- | --- |
| `--label` vacio o ausente | Error de validacion de clap (flag requerido) |
| perfil inexistente | Mensaje exacto no verificado |

## Notes

_Quirks, gotchas, and operational observations not covered above._

- `--label` es obligatorio (el --help lo marca como requerido).
- El `--machine` selector en otros comandos acepta la etiqueta nueva, unica y case-sensitive (skill oficial).

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr machine rename --help (herdr 0.9.0)

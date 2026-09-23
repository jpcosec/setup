---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-pane-rename
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr pane rename
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: pane
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:pane
---

# herdr pane rename

## Synopsis

_What the command does, in one or two sentences._

Rename a pane

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr pane rename [OPTIONS] <PANE_ID> [LABEL]...

## Arguments

_Table of options: option, type, required, and what it does._

| opcion | tipo | obligatorio | que hace |
|---|---|---|---|
| <PANE_ID> | texto | si |  |
| [LABEL]... | texto | no |  |
| --clear | texto | no |  |

## Returns

_What the command returns on success: JSON shape and location of the payload._

El pane completo (verificado en vivo), ahora con el campo `label`:

```json
{"id":"cli:pane:rename","result":{"pane":{"pane_id":"wZ:p2","label":"ATOM_PANE",...},"type":"pane_info"}}
```

```bash
herdr pane rename "$pane_id" buildbox | jq -r '.result.pane.label'       # -> buildbox
herdr pane rename "$pane_id" --clear | jq -r '.result.pane.label'        # -> null (si lo tenia)
```

## Returns jq

_jq paths to extract the returned payload into shell variables._

herdr pane rename "$pane_id" buildbox | jq -r '.result.pane.label'       # -> buildbox
herdr pane rename "$pane_id" --clear | jq -r '.result.pane.label'        # -> null (si lo tenia)

## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
# Etiquetar el pane de un proceso largo para encontrarlo en pane list
herdr pane rename "$pane_id" tests watcher   # label: "tests watcher"
herdr pane list | jq -r '.result.panes[] | select(.label=="tests watcher") | .pane_id'
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| codigo / sintoma | significado |
|---|---|
| `pane_not_found` en stderr, exit 1 | Pane inexistente |
| exit 2 texto plano | Sintaxis invalida del CLI |

## Notes

_Quirks, gotchas, and operational observations not covered above._

- El label es SOLO una etiqueta de UI/estado: no cambia `terminal_title` del proceso (verificado en vivo: `terminal_title_stripped` quedo intacto) ni sirve como identificador en comandos — las rutas siguen usando `pane_id`.
- Para el titulo que ve el proceso, usa los comandos de terminal (`herdr terminal title set`, fuera de este grupo).
- Renombrar el pane NO equivale a renombrar un agente: eso es `agent rename`.

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr pane rename --help (herdr 0.9.0)

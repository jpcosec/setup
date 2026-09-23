---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-pane-process-info
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr pane process-info
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: pane
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:pane
---

# herdr pane process-info

## Synopsis

_What the command does, in one or two sentences._

Show pane process information

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr pane process-info [OPTIONS]

## Arguments

_Table of options: option, type, required, and what it does._

| opcion | tipo | obligatorio | que hace |
|---|---|---|---|
| --pane <ID> | texto | no |  |
| --current | texto | no |  |

## Returns

_What the command returns on success: JSON shape and location of the payload._

JSON con `.result.type == "pane_process_info"` y `.result.process_info` (verificado en 0.9.0):

```json
{
  "result": {
    "type": "pane_process_info",
    "process_info": {
      "pane_id": "wX:pF",
      "shell_pid": 6101,
      "foreground_process_group_id": 6485,
      "foreground_processes": [
        { "pid": 6485, "name": "pi", "argv": ["pi"], "cmdline": "pi", "cwd": "/home/jp/setup" }
      ]
    }
  }
}
```

Rutas jq exactas:

```bash
jq -r '.result.process_info.pane_id'
jq -r '.result.process_info.foreground_processes[0].name'
jq -r '.result.process_info.foreground_processes[0].cwd'
```

`foreground_processes[]` puede estar vacio si la plataforma no expone procesos en foreground.

## Returns jq

_jq paths to extract the returned payload into shell variables._

Rutas jq exactas:
jq -r '.result.process_info.pane_id'
jq -r '.result.process_info.foreground_processes[0].name'
jq -r '.result.process_info.foreground_processes[0].cwd'

## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
# Que comando corre en el primer pane, y desde que cwd
pid=$(herdr pane list | jq -r '.result.panes[0].pane_id')
herdr pane process-info --pane "$pid" | jq -r '.result.process_info.foreground_processes[] | "\(.name)\t\(.cwd)"'
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| codigo | significado |
|---|---|
| `pane_not_found` | `--pane` inexistente; verificado: `{"error":{"code":"pane_not_found","message":"pane not found"},"id":"cli:pane:process_info"}` en stderr con exit 1 |

## Notes

_Quirks, gotchas, and operational observations not covered above._

- `shell_pid` es el pid del shell del pane; el proceso en foreground suele ser hijo del process group indicado.
- Util para detectar si el pane esta en prompt de shell, con editor, o con agente (comparando `name`).

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr pane process-info --help (herdr 0.9.0)

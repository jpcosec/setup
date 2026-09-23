---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-workspace-focus
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr workspace focus
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: workspace
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:workspace
---

# herdr workspace focus

## Synopsis

_What the command does, in one or two sentences._

Focus a workspace

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr workspace focus <workspace_id>

## Arguments

_Table of options: option, type, required, and what it does._

| opcion | tipo | obligatorio | que hace |
|---|---|---|---|
| <workspace_id> | texto | si |  |

## Returns

_What the command returns on success: JSON shape and location of the payload._

JSON con `.result.type == "workspace_info"` y el workspace enfocado en `.result.workspace` (verificado en 0.9.0):

```json
{
  "id": "cli:workspace:focus",
  "result": { "type": "workspace_info",
    "workspace": { "workspace_id": "wY", "label": "AWS_Infra", "focused": true, "pane_count": 4, "tab_count": 3 } }
}
```

Ruta jq exacta:

```bash
herdr workspace focus wX | jq -r '.result.workspace.workspace_id'
herdr workspace focus wX | jq -r '.result.workspace.focused'   # -> true
```

## Returns jq

_jq paths to extract the returned payload into shell variables._

Ruta jq exacta:
herdr workspace focus wX | jq -r '.result.workspace.workspace_id'
herdr workspace focus wX | jq -r '.result.workspace.focused'   # -> true

## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
# Enfocar el workspace con label "legos" sin predecir su id
ws=$(herdr workspace list | jq -r '.result.workspaces[] | select(.label=="legos") | .workspace_id')
herdr workspace focus "$ws" >/dev/null
herdr workspace get "$ws" | jq -r '.result.workspace.focused'
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| codigo | significado |
|---|---|
| `workspace_not_found` | Id inexistente; verificado: stderr con exit 1 |

## Notes

_Quirks, gotchas, and operational observations not covered above._

- Enfocar es una accion que el TUI del usuario ve; en automatizacion usa `--no-focus` en las creaciones y focus solo cuando hace falta.
- Enfocar explicitamente marca el workspace como "seen" (un `pane focus`/`agent focus` tambien marca al objetivo como visto; las lecturas no).

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr workspace focus --help (herdr 0.9.0)

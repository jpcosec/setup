---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-tab-focus
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr tab focus
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: tab
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:tab
---

# herdr tab focus

## Synopsis

_What the command does, in one or two sentences._

Focus a tab

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr tab focus <tab_id>

## Arguments

_Table of options: option, type, required, and what it does._

| opcion | tipo | obligatorio | que hace |
|---|---|---|---|
| <tab_id> | texto | si |  |

## Returns

_What the command returns on success: JSON shape and location of the payload._

JSON con `.result.type == "tab_info"` y el tab enfocado en `.result.tab` (verificado en 0.9.0):

```json
{
  "id": "cli:tab:focus",
  "result": { "type": "tab_info",
    "tab": { "tab_id": "wY:t1", "workspace_id": "wY", "label": "1", "focused": true, "pane_count": 2 } }
}
```

Ruta jq exacta:

```bash
herdr tab focus wX:t1 | jq -r '.result.tab.tab_id'
herdr tab focus wX:t1 | jq -r '.result.tab.focused'   # -> true
```

## Returns jq

_jq paths to extract the returned payload into shell variables._

Ruta jq exacta:
herdr tab focus wX:t1 | jq -r '.result.tab.tab_id'
herdr tab focus wX:t1 | jq -r '.result.tab.focused'   # -> true

## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
# Enfocar el tab cuyo id capturamos con jq
tab=$(herdr tab list | jq -r '.result.tabs[] | select(.label=="tests") | .tab_id')
[ -n "$tab" ] && herdr tab focus "$tab" | jq -r '.result.tab.tab_id'
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| codigo | significado |
|---|---|
| `tab_not_found` | Id inexistente; verificado: stderr con exit 1 |

## Notes

_Quirks, gotchas, and operational observations not covered above._

- Enfocar un tab marca targets como "seen" a nivel de server (los reads no marcan como visto).
- Preferir `tab_id` obtenido por jq sobre el label: los labels se repiten entre tabs (en el entorno real hay dos tabs llamados "1").

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr tab focus --help (herdr 0.9.0)

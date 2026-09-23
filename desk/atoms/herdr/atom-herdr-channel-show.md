---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-channel-show
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr channel show
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: channel
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:channel
---

# herdr channel show

## Synopsis

_What the command does, in one or two sentences._

Print the configured update channel

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr channel show

## Arguments

_Table of options: option, type, required, and what it does._



## Returns

_What the command returns on success: JSON shape and location of the payload._

Texto plano con el canal (verificado, herdr 0.9.0):

```text
stable
```

Posibles valores: `stable` o `preview`.

## Returns jq

_jq paths to extract the returned payload into shell variables._



## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
# ¿En que canal estoy?
herdr channel show

# En scripts: comparar el canal sin quotes
test "$(herdr channel show)" = "stable" && echo "canal estable"
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| Codigo | Significado |
| --- | --- |
| sin error documentado | Comando de solo lectura sin estados de error esperados |

## Notes

_Quirks, gotchas, and operational observations not covered above._

- Verificado 2026-09-23: este setup usa `stable`.
- El canal tambien aparece en `herdr status --json` como `.client.channel`.

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr channel show --help (herdr 0.9.0)

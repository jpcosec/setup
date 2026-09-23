---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-pane-focus
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr pane focus
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: pane
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:pane
---

# herdr pane focus

## Synopsis

_What the command does, in one or two sentences._

Focus a neighboring pane

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr pane focus [OPTIONS] --direction <DIRECTION>

## Arguments

_Table of options: option, type, required, and what it does._

| opcion | tipo | obligatorio | que hace |
|---|---|---|---|
| --direction <DIRECTION> | enum | no | [possible values: left, right, up, down] |
| --pane <ID> | texto | no |  |
| --current | texto | no |  |

## Returns

_What the command returns on success: JSON shape and location of the payload._

Objeto `focus` con el nuevo foco y el layout actualizado (verificado en vivo):

```json
{"id":"cli:pane:focus","result":{"focus":{"changed":true,"focused_pane_id":"wY:p1","layout":{...}},"type":"pane_focus"}}
```

```bash
herdr pane focus --direction right | jq -r '.result.focus.focused_pane_id'  # pane que queda enfocado
herdr pane focus --direction right | jq -r '.result.focus.changed'          # false si no habia vecino
```

## Returns jq

_jq paths to extract the returned payload into shell variables._

herdr pane focus --direction right | jq -r '.result.focus.focused_pane_id'  # pane que queda enfocado
herdr pane focus --direction right | jq -r '.result.focus.changed'          # false si no habia vecino

## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
# Moverse al vecino de la derecha y reportar que pane quedo enfocado
moved=$(herdr pane focus --direction right)
printf 'foco ahora en: %s\n' "$(printf '%s' "$moved" | jq -r '.result.focus.focused_pane_id')"
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| codigo / sintoma | significado |
|---|---|
| exit 1 JSON en stderr | Error del server; codigo cuando NO existe vecino en esa direccion: no verificado |
| exit 2 texto plano | Sintaxis invalida (p. ej. `--direction sideways`) |
| Error con `--current` sin `HERDR_PANE_ID` | La doc oficial: `--current` requiere pane llamador |

## Notes

_Quirks, gotchas, and operational observations not covered above._

- La doc oficial: `pane focus` (y `agent focus`) marcan el pane destino como "seen" en el estado del agente; las lecturas (`pane read`, `agent read`) NO lo marcan. Afecta a la diferencia `idle` vs `done`.
- Para saber si hay vecino antes, usa `pane edges` o `pane neighbor`.
- No crea panes: hace falta un split previo (`pane split`).

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr pane focus --help (herdr 0.9.0)

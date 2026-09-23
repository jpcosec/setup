---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-pane-move
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr pane move
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: pane
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:pane
---

# herdr pane move

## Synopsis

_What the command does, in one or two sentences._

Move a pane

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr pane move [OPTIONS] <PANE_ID>

## Arguments

_Table of options: option, type, required, and what it does._

| opcion | tipo | obligatorio | que hace |
|---|---|---|---|
| <PANE_ID> | texto | si |  |
| --tab <TAB_ID> | texto | no |  |
| --split <DIRECTION> | enum | no | [possible values: right, down] |
| --target-pane <ID> | texto | no |  |
| --ratio <FLOAT> | texto | no |  |
| --new-tab | texto | no |  |
| --workspace <ID> | texto | no |  |
| --new-workspace | texto | no |  |
| --label <TEXT> | texto | no |  |
| --tab-label <TEXT> | texto | no |  |
| --focus | texto | no |  |
| --no-focus | texto | no |  |

## Returns

_What the command returns on success: JSON shape and location of the payload._

**CRITICO**: mover un pane a otro workspace **cambia su pane ID** (se re-cualifica por workspace). Despues de cualquier `pane move` hay que continuar con:

```bash
jq -r '.result.move_result.pane.pane_id'            # -> el NUEVO pane id (el valido de aqui en adelante)
jq -r '.result.move_result.previous_pane_id'        # -> el pane id VIEJO (conservado como referencia)
```

Forma del JSON (doc oficial): `type: "pane_move"` con `changed`, `reason` opcional, `previous_pane_id`, `previous_workspace_id`, `previous_tab_id`, el `pane` movido, `source_layout`/`target_layout` opcionales, registros de workspace/tab creados o cerrados, y `focused_pane_id`. El CLI lo expone dentro de `.result.move_result`.

## Returns jq

_jq paths to extract the returned payload into shell variables._

jq -r '.result.move_result.pane.pane_id'            # -> el NUEVO pane id (el valido de aqui en adelante)
jq -r '.result.move_result.previous_pane_id'        # -> el pane id VIEJO (conservado como referencia)

## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
# Mover a un tab existente: SIEMPRE con --split
moved=$(herdr pane move "$pane_id" --tab "$tab_id" --split right --no-focus)
new_pane=$(printf '%s\n' "$moved" | jq -r '.result.move_result.pane.pane_id')
old_pane=$(printf '%s\n' "$moved" | jq -r '.result.move_result.previous_pane_id')
echo "el pane $old_pane ahora es $new_pane"

# Mover a un workspace nuevo
moved=$(herdr pane move "$pane_id" --new-workspace --label logs --no-focus)
new_pane=$(printf '%s\n' "$moved" | jq -r '.result.move_result.pane.pane_id')
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| codigo | significado |
|---|---|
| `pane_not_found` | Pane origen inexistente; verificado: `{"error":{"code":"pane_not_found","message":"source pane not found"},"id":"cli:pane:move"}` en stderr con exit 1 |
| `changed: false` con `reason: "same_tab"` | Moverse al tab fuente (los cambios en el mismo tab usan `pane swap`) |
| `changed: false` con `reason: "zoomed_tab"` | El tab fuente o destino esta en zoom |

## Notes

_Quirks, gotchas, and operational observations not covered above._

- El proceso en ejecucion **conserva su entorno herdr de arranque** (`HERDR_PANE_ID`, `HERDR_TAB_ID`, `HERDR_WORKSPACE_ID` de lanzamiento).
- El `HERDR_PANE_ID` viejo **sigue siendo alias** de esa terminal: los comandos con `--current` siguen resolviendo el pane correcto.
- Un agente con nombre sigue a la terminal y sigue resolviendose tras el move; pero un wait de agente ya en curso termina con `agent_not_running`.
- Los ids de pane de una sesion no valen en otra, y `--current` no puede referirse al pane de un llamador remoto (doc oficial).

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr pane move --help (herdr 0.9.0)

---
id: atom-herdr-captura-de-ids
status: draft
tags: [system:herdr, layer:runtime, topic:automation]
---

# Captura de IDs en herdr (regla de oro)

## Que hace

Documenta la regla de oro de la doc oficial: capturar los IDs desde el JSON de respuesta con jq, nunca predecirlos ni parsearlos con grep.

## La regla

> "Creation commands print JSON. Capture IDs from the response instead of predicting them." — https://herdr.dev/docs/agent-automation/

Los IDs de herdr (workspace `wX`, tab `wX:tG`, pane `wX:tG:p1`) son asignados por el server y **no** son predecibles:

- los sub-ids de tab pueden ser alfanumericos (`wX:tG`, `wX:tH`); la numeracion no es contigua (en el entorno real: `number` 1, 16, 17);
- los ids cambian al mover un pane entre workspaces (ver abajo);
- cada sesion/servidor tiene su propio espacio de ids.

Por eso:

- NO uses grep para extraer ids de la salida;
- NO hardcodees `w1:p2` ni construyas ids por concatenacion;
- SIEMPRE: capturar la respuesta completa en una variable y extraer con `jq -r`.

## Patron estandar

```bash
out=$(herdr workspace create --cwd ~/project --label api --no-focus)
ws=$(printf '%s\n' "$out" | jq -r '.result.workspace.workspace_id')
pane=$(printf '%s\n' "$out" | jq -r '.result.root_pane.pane_id')
```

Ejemplo oficial completo (doc agent-automation):

```bash
created=$(herdr workspace create --cwd ~/project --label api --no-focus)
pane_id=$(printf '%s\n' "$created" | jq -r '.result.root_pane.pane_id')
split=$(herdr pane split "$pane_id" --direction right --no-focus)
review_pane=$(printf '%s\n' "$split" | jq -r '.result.pane.pane_id')
```

## El caso especial: pane move

Mover un pane a otro workspace **cambia su pane ID** (se re-cualifica por workspace). Despues de cualquier `pane move`:

- usa `.result.move_result.pane.pane_id` para seguir trabajando con el pane;
- el valor viejo queda conservado en `.result.move_result.previous_pane_id` (doc oficial).

```bash
moved=$(herdr pane move "$pane_id" --tab "$target_tab" --split right)
new_pane=$(printf '%s\n' "$moved" | jq -r '.result.move_result.pane.pane_id')
old_pane=$(printf '%s\n' "$moved" | jq -r '.result.move_result.previous_pane_id')
echo "el pane $old_pane ahora es $new_pane"
```

Detalles asociados (doc oficial):

- El proceso conserva su entorno `HERDR_PANE_ID` de lanzamiento y el id viejo queda como **alias** de esa terminal, asi que `--current` sigue siendo seguro.
- Un agente con nombre sigue a la terminal despues del move (el alias se disuelve solo cuando el agente sale, se libera o se reemplaza).
- Un wait de agente ya en curso termina con `agent_not_running` tras el move.

## Errores conocidos

| sintoma | causa |
|---|---|
| `agent_not_running` en un wait despues de un move | El wait quedo atado al pane viejo; relanza el wait contra `.result.move_result.pane.pane_id` |
| Id predicho no existe (`workspace_not_found`/`tab_not_found`) | Se intento adivinar un id en vez de capturarlo con jq |

## Notas

- `printf '%s\n'` en vez de echo directo: evita interpretar flags/backslashes raros del JSON.
- Los ids son scoped a la sesion y al server: no se reutilizan entre maquinas ni sesiones (`--machine` tampoco los reutiliza).
- Los ejemplos de todos los atoms de herdr usan este patron.
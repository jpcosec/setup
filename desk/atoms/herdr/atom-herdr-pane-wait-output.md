---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-pane-wait-output
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr pane wait-output
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: pane
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:pane
---

# herdr pane wait-output

## Synopsis

_What the command does, in one or two sentences._

Wait for matching pane output

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr pane wait-output [OPTIONS] <--match <TEXT>|--regex <PATTERN>> <PANE_ID>

## Arguments

_Table of options: option, type, required, and what it does._

| opcion | tipo | obligatorio | que hace |
|---|---|---|---|
| <PANE_ID> | texto | si |  |
| --match <TEXT> | texto | no | Match a literal substring |
| --regex <PATTERN> | texto | no | Match a Rust regular expression |
| --source <SOURCE> | enum | no | Terminal snapshot source (default: recent) [possible values: visible, recent, recent-unwrapped] |
| --lines <N> | numero | no | Restrict the searched snapshot to N lines |
| --timeout <MS> | numero | no | Fail after this many milliseconds |
| --raw | texto | no | Keep ANSI escape sequences while matching |

## Returns

_What the command returns on success: JSON shape and location of the payload._

El pane, la linea que matcheo y el snapshot (doc oficial + verificado en vivo: `pane_id` y `matched_line`):

```json
{"id":"cli:pane:wait_output","result":{"pane_id":"wZ:p1","matched_line":"(base) jp@johanes:/tmp$ echo ATOM_TEST_OK","read":"<snapshot>"}}
```

```bash
out=$(herdr pane wait-output "$pane_id" --match ATOM_TEST_OK --timeout 5000)
printf '%s' "$out" | jq -r '.result.pane_id'        # pane
printf '%s' "$out" | jq -r '.result.matched_line'   # linea exacta que matcheo
printf '%s' "$out" | jq -r '.result.read'           # snapshot completo matcheado
```

## Returns jq

_jq paths to extract the returned payload into shell variables._

printf '%s' "$out" | jq -r '.result.pane_id'        # pane
printf '%s' "$out" | jq -r '.result.matched_line'   # linea exacta que matcheo
printf '%s' "$out" | jq -r '.result.read'           # snapshot completo matcheado

## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
# Lanzar un watcher y esperar su primera senal de vida
herdr pane run "$pane_id" 'just test --watch'
herdr pane wait-output "$pane_id" --regex 'passed|failed' --timeout 120000
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| codigo / sintoma | significado |
|---|---|
| `timeout` en JSON de error en stderr, exit 1 | Se agoto `--timeout` sin coincidencia (doc oficial: el timeout devuelve el error normal `timeout`) |
| exit 2 texto plano | Sintaxis invalida: faltan `--match`/`--regex`, o ambos a la vez |
| `pane_not_found` en stderr, exit 1 | Pane inexistente |
| `agent_not_running` (doc oficial) | Un wait en curso termina asi tras mover el pane (`pane move`); relanza contra el id nuevo |

## Notes

_Quirks, gotchas, and operational observations not covered above._

- Busca el snapshot seleccionado INMEDIATAMENTE (incluye lo ya impreso) y luego sondea; sin `--timeout` espera para siempre (doc oficial; confirmado en el propio help).
- No interpreta el ciclo de vida del agente: para esperar estados de agente (`working`/`blocked`/`idle`) usa `agent wait`, no esto (doc oficial).
- `--match` es substring en una linea; `--regex` usa sintaxis de regex de Rust y matchea linea a linea (doc oficial).
- En la coordinacion de este ecosistema es la primitiva de "esperar salida" de los workers; `coordination.sh` la usa junto a la API de agentes.

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr pane wait-output --help (herdr 0.9.0)

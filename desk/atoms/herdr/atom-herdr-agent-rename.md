---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-agent-rename
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr agent rename
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: agent
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:agent
---

# herdr agent rename

## Synopsis

_What the command does, in one or two sentences._

Rename an agent

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr agent rename <TARGET> <NAME>|--clear

## Arguments

_Table of options: option, type, required, and what it does._

| opcion | tipo | obligatorio | que hace |
|---|---|---|---|
| <TARGET> | texto | si |  |
| [NAME] | texto | no |  |
| --clear | texto | no |  |

## Returns

_What the command returns on success: JSON shape and location of the payload._

No devuelve JSON verificable: es una accion de alias. Salida exacta en exito: no verificada (no ejecutado para no alterar agentes vivos; el CLI de 0.9.0 no documenta respuesta).

## Returns jq

_jq paths to extract the returned payload into shell variables._



## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
# Nombrar al agente del pane que devuelve pane create/split (ID capturado, nunca predicho)
pane_id=$(herdr agent get claude | jq -r '.result.agent.pane_id')
herdr agent rename "$pane_id" reviewer

# Verificar el alias
herdr agent get reviewer | jq -r '.result.agent.name'

# Limpiar el alias cuando ya no se necesite
herdr agent rename reviewer --clear
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| codigo | significado |
|---|---|
| `usage: herdr agent rename <target> <name>|--clear` + exit 2 | Falta `<NAME>` o `--clear`; verificado en 0.9.0 |
| error JSON en stderr, exit 1 | Agente inexistente o nombre invalido; codigos exactos no verificados |

## Notes

_Quirks, gotchas, and operational observations not covered above._

- Los nombres deben cumplir `[a-z][a-z0-9_-]{0,31}` y ser unicos entre agentes vivos (doc oficial).
- El alias se limpia automaticamente cuando el agente sale, es liberado o reemplazado; no renombra el pane de forma permanente.
- Un pane movido a otro workspace cambia su pane ID cualificado, pero el nombre sigue resolviendo al agente tras el move (doc oficial).

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr agent rename --help (herdr 0.9.0)

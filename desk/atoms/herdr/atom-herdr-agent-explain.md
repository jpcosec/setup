---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-agent-explain
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr agent explain
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: agent
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:agent
---

# herdr agent explain

## Synopsis

_What the command does, in one or two sentences._

Explain agent detection state

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr agent explain [OPTIONS] [TARGET]

## Arguments

_Table of options: option, type, required, and what it does._

| opcion | tipo | obligatorio | que hace |
|---|---|---|---|
| [TARGET] | texto | no |  |
| --file <PATH> | texto | no |  |
| --agent <LABEL> | texto | no |  |
| --json | texto | no |  |
| --format <FORMAT> | enum | no | [possible values: text, json] |
| -v, --verbose | texto | no |  |

## Returns

_What the command returns on success: JSON shape and location of the payload._

En texto (verificado en 0.9.0):

```text
agent: pi
state: working
manifest: remote:/home/jp/.local/state/herdr/agent-detection/remote/pi.toml 2026.09.14.1
rule: working_literal (region=whole_recent priority=100)
evidence: "<preview del contenido del terminal que matcheo>"
```

Con `--json` el mismo contenido como objeto plano (verificado): claves `.state`, `.matched_rule.id`, `.matched_rule.priority`, `.matched_rule.region`, `.evidence.region_preview`, `.manifest_source`, `.evaluated_rules[]`, `.visible_working`, `.visible_blocker`, `.warning`.

Rutas jq utiles:

```bash
jq -r '.state'                 # estado clasificado: idle|working|blocked|done|unknown
jq -r '.matched_rule.id'       # regla que matcheo (p. ej. working_literal)
jq -r '.manifest_source'       # manifiesto de deteccion usado (remoto o local)
jq -r '.warning'               # advertencia de deteccion (puede ser null)
```

## Returns jq

_jq paths to extract the returned payload into shell variables._

Rutas jq utiles:
jq -r '.state'                 # estado clasificado: idle|working|blocked|done|unknown
jq -r '.matched_rule.id'       # regla que matcheo (p. ej. working_literal)
jq -r '.manifest_source'       # manifiesto de deteccion usado (remoto o local)
jq -r '.warning'               # advertencia de deteccion (puede ser null)

## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
# Por que este agente esta 'working'?
herdr agent explain w1 --json | jq -r '.state, .matched_rule.id'

# Previsualizar la evidencia (el texto del terminal que disparo la regla)
herdr agent explain w1 --json | jq -r '.evidence.region_preview'
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| codigo | significado |
|---|---|
| `usage: herdr agent explain <target> [--json]` + exit 2 | Falta target y no se dio `--file` + `--agent`; verificado en 0.9.0 |
| error JSON en stderr, exit 1 | Error del server (target inexistente); codigos exactos no verificados |

## Notes

_Quirks, gotchas, and operational observations not covered above._

- `--json` y `--format json` son intercambiables; `--format text` es el default.
- El manifiesto se descarga/actualiza desde remoto (`remote_update_status: current` en 0.9.0, version 2026.09.14.1).
- La salida de `--file` + `--agent` analiza un manifiesto guardado sin tocar el server: forma exacta no verificada.

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr agent explain --help (herdr 0.9.0)

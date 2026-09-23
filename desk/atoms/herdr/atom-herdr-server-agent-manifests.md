---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-server-agent-manifests
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr server agent-manifests
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: server
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:server
---

# herdr server agent-manifests

## Synopsis

_What the command does, in one or two sentences._

Show active agent detection manifests

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr server agent-manifests [OPTIONS]

## Arguments

_Table of options: option, type, required, and what it does._

| opcion | tipo | obligatorio | que hace |
|---|---|---|---|
| --json | texto | no |  |

## Returns

_What the command returns on success: JSON shape and location of the payload._

Con `--json`, JSON `cli:server:agent-manifests` → `.result.manifests[]` con `type: agent_manifest_status` (verificado, 21 agentes en este setup):

```json
{"id":"cli:server:agent-manifests","result":{
  "last_check_unix":1790165001,
  "last_result":"checked",
  "manifests":[{"agent":"pi","active_version":"2026.09.14.1","source_kind":"remote",
    "source":"remote:/home/jp/.local/state/herdr/agent-detection/remote/pi.toml",
    "cached_remote_version":"2026.09.14.1","remote_update_result":"current",
    "local_override_shadowing_remote":false,...}],
  "type":"agent_manifest_status"}}
```

Rutas jq utiles:

```bash
jq -r '.result.last_result'                                   # checked
jq -r '.result.manifests[].agent' | sort                      # agentes reconocidos
jq -r '.result.manifests[] | select(.agent=="pi") | .active_version'
jq -r '.result.manifests[] | select(.remote_update_result != "current") | [.agent, .remote_update_result, .remote_update_error]'
```

## Returns jq

_jq paths to extract the returned payload into shell variables._

Rutas jq utiles:
jq -r '.result.last_result'                                   # checked
jq -r '.result.manifests[].agent' | sort                      # agentes reconocidos
jq -r '.result.manifests[] | select(.agent=="pi") | .active_version'
jq -r '.result.manifests[] | select(.remote_update_result != "current") | [.agent, .remote_update_result, .remote_update_error]'

## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
# ¿Que version de deteccion tiene cada agente y esta todo al dia?
herdr server agent-manifests --json | jq -r '
  .result.manifests[] | "\(.agent)\t\(.active_version)\t\(.remote_update_result)\t\(.source_kind)"'

# ¿Algun manifest es un override local?
herdr server agent-manifests --json | jq -r '.result.manifests[] | select(.local_override_shadowing_remote) | .agent'
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| Codigo | Significado |
| --- | --- |
| `server_unavailable` | El server no responde (no hay manifests que leer) |
| `agent not found` / manifest corrupto | Entradas con `remote_update_error` poblado; `last_result` distinto de `checked` |

## Notes

_Quirks, gotchas, and operational observations not covered above._

- Los manifHash remotos viven en `~/.local/state/herdr/agent-detection/remote/<agente>.toml` (verificado en este setup).
- `remote_update_result: current` significa que el remoto ya tiene la version activa; las actualizaciones se descargan con `server update-agent-manifests`.
- Es de solo lectura: no genera evento en el log del server (ver `atom-herdr-no-guarda-traza`).

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr server agent-manifests --help (herdr 0.9.0)

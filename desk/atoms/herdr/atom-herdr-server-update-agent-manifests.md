---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-server-update-agent-manifests
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr server update-agent-manifests
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: server
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:server
---

# herdr server update-agent-manifests

## Synopsis

_What the command does, in one or two sentences._

Fetch and reload agent detection manifests

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr server update-agent-manifests [OPTIONS]

## Arguments

_Table of options: option, type, required, and what it does._

| opcion | tipo | obligatorio | que hace |
|---|---|---|---|
| --json | texto | no |  |

## Returns

_What the command returns on success: JSON shape and location of the payload._

Con `--json`, JSON con la misma forma de `agent_manifest_status` que `server agent-manifests --json` (no verificado su estado exacto aqui: no se ejecuto para evitar una descarga de red). Esperado tras recargar:

```json
{"id":"cli:server:update-agent-manifests","result":{"last_check_unix":..., "last_result":"checked", "manifests":[...]}}
```

Rutas jq utiles (iguales que agent-manifests):

```bash
jq -r '.result.last_result'
jq -r '.result.manifests[] | select(.remote_update_result != "current") | [.agent, .remote_update_error]'
```

## Returns jq

_jq paths to extract the returned payload into shell variables._

Rutas jq utiles (iguales que agent-manifests):
jq -r '.result.last_result'
jq -r '.result.manifests[] | select(.remote_update_result != "current") | [.agent, .remote_update_error]'

## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
# Forzar la actualizacion de los manifests y ver si alguno fallo
herdr server update-agent-manifests --json | jq -r '
  .result.manifests[] | select(.remote_update_result != "current")
  | "\(.agent) \(.remote_update_result) \(.remote_update_error // "")"'
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| Codigo | Significado |
| --- | --- |
| `server_unavailable` | Server caido: no se puede recargar |
| fallo de red | Se refleja en `.result.last_result` o `remote_update_error` por agente (no verificado el texto exacto) |

## Notes

_Quirks, gotchas, and operational observations not covered above._

- El server ya hace chequeos periodicos (`update.check.start` / `manifest_check` en la config y log); este comando fuerza el ciclo ahora.
- Verificado en el setup: el ultimo chequeo (`remote_last_checked_unix` 1790165001) dejo todo en `current`; no hizo falta forzar.

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr server update-agent-manifests --help (herdr 0.9.0)

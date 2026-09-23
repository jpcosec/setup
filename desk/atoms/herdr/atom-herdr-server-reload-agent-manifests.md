---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-server-reload-agent-manifests
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr server reload-agent-manifests
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: server
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:server
---

# herdr server reload-agent-manifests

## Synopsis

_What the command does, in one or two sentences._

Reload local agent detection manifest overrides

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr server reload-agent-manifests

## Arguments

_Table of options: option, type, required, and what it does._



## Returns

_What the command returns on success: JSON shape and location of the payload._

JSON `cli:server:reload-agent-manifests` con `result.type: agent_manifest_reload` (shape de `.result` no verificado: no se ejecuto, los overrides locales de este setup no han cambiado).

## Returns jq

_jq paths to extract the returned payload into shell variables._



## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
# Tras editar un override local de deteccion (p.ej. ~/.local/state/herdr/agent-detection/overrides/)
herdr server reload-agent-manifests

# Confirmar que la recarga se aplico y ver el estado
herdr server agent-manifests --json | jq -r '.result.last_result'
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| Codigo | Significado |
| --- | --- |
| `server_unavailable` | Server no corriendo |
| manifests invalidos | Un override corrupto puede dejar `last_result` distinto de `checked`; revisar `server agent-manifests --json` |

## Notes

_Quirks, gotchas, and operational observations not covered above._

- Diferencia clave: `reload-agent-manifests` = recargar lo local; `update-agent-manifests` = descargar remotos y recargar. La doc oficial lo distingue explicitamente.
- `local_override_shadowing_remote: true` (campo del manifest) indica que un override local esta tapando la fuente remota.
- En este setup no hay overrides: todas las fuentes son `remote` (verificado en `agent-manifests --json`).

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr server reload-agent-manifests --help (herdr 0.9.0)

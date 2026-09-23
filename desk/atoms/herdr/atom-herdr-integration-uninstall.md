---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-integration-uninstall
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr integration uninstall
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: integration
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:integration
---

# herdr integration uninstall

## Synopsis

_What the command does, in one or two sentences._

Uninstall an integration

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr integration uninstall <TARGET>

## Arguments

_Table of options: option, type, required, and what it does._

| opcion | tipo | obligatorio | que hace |
|---|---|---|---|
| <TARGET> | enum | si | [possible values: pi, omp, claude, codex, copilot, devin, droid, kimi, opencode, kilo, hermes, qodercli, qwen, cursor, mastracode, antigravity-cli, grok] |

## Returns

_What the command returns on success: JSON shape and location of the payload._

JSON `cli:integration:uninstall` con `result.type: integration_uninstall` (shape del `.result` no verificado: no se ejecuto, desinstalar rompe el reporte de estado de ese agente).

## Returns jq

_jq paths to extract the returned payload into shell variables._



## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
# Desinstalar (siempre que de verdad se quiera dejar de reportar estado)
herdr integration uninstall opencode

# Verificar
herdr integration status | grep -a '^opencode:'
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| Codigo | Significado |
| --- | --- |
| `integration_uninstall_failed` | Fallo al eliminar la integracion (string del binario) |
| target invalido | Error de clap con la lista de `possible values` |

## Notes

_Quirks, gotchas, and operational observations not covered above._

- Desinstalar degrada la deteccion de estado de ese agente: pasaria a `unknown` si la deteccion depende del latch de estado (matiz: la deteccion es para los agentes reconocidos via manifest).
- En este setup NO desinstalar: pi/claude/codex/opencode/antigravity-cli son las integraciones activas (verificado via `integration status`).

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr integration uninstall --help (herdr 0.9.0)

---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-integration-install
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr integration install
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: integration
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:integration
---

# herdr integration install

## Synopsis

_What the command does, in one or two sentences._

Install an integration

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr integration install <TARGET>

## Arguments

_Table of options: option, type, required, and what it does._

| opcion | tipo | obligatorio | que hace |
|---|---|---|---|
| <TARGET> | enum | si | [possible values: pi, omp, claude, codex, copilot, devin, droid, kimi, opencode, kilo, hermes, qodercli, qwen, cursor, mastracode, antigravity-cli, grok] |

## Returns

_What the command returns on success: JSON shape and location of the payload._

JSON `cli:integration:install` con `result.type: integration_install` (shape del `.result` no verificado: no se ejecuto, escribe en config de agentes).

```bash
herdr integration install pi | jq -r '.result.type'
```

## Returns jq

_jq paths to extract the returned payload into shell variables._

herdr integration install pi | jq -r '.result.type'

## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
# Instalar la integracion de estado para pi (agente principal de este setup)
herdr integration install pi

# Verificar que quedo instalada y al dia
herdr integration status | grep -a '^pi:'
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| Codigo | Significado |
| --- | --- |
| `integration_install_failed` | Fallo al escribir la integracion (string del binario) |
| target invalido | Error de clap: el valor no esta en la lista de `possible values` |

## Notes

_Quirks, gotchas, and operational observations not covered above._

- Verificado: en este setup ya estan instaladas `pi` (v8), `claude` (v9), `codex` (v8), `opencode` (v11) y `antigravity-cli` (v3); el resto `not installed` (salida real de `herdr integration status`).
- La integracion de pi vive en `/home/jp/.pi/agent/extensions/herdr-agent-state.ts`; codex en `/home/jp/.codex/herdr-agent-state.sh` (hook SessionStart).
- Es una accion idempotente: reinstalar actualiza a la version del binario.

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr integration install --help (herdr 0.9.0)

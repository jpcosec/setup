---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-agent-start
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr agent start
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: agent
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:agent
---

# herdr agent start

## Synopsis

_What the command does, in one or two sentences._

Start a supported interactive agent in an existing pane

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr agent start <NAME> --kind <KIND> --pane <ID> [OPTIONS] [-- [AGENT_ARG]...]

## Arguments

_Table of options: option, type, required, and what it does._

| opcion | tipo | obligatorio | que hace |
|---|---|---|---|
| <NAME> | texto | si |  |
| [AGENT_ARG]... | texto | no |  |
| --kind <KIND> | enum | no | Supported agent kind and canonical executable [possible values: pi, claude, codex, gemini, cursor, devin, agy, cline, omp, mastracode, opencode, copilot, kimi, kiro, droid, amp, grok, hermes, kilo, qodercli, qwen, maki, muse] |
| --pane <ID> | texto | no | Existing pane at an interactive shell prompt |
| --timeout <MS> | numero | no | Wait for interactive readiness (default: 30000; max: 300000) |

## Returns

_What the command returns on success: JSON shape and location of the payload._

En exito, JSON con el agente en `.result.agent` (doc oficial: los comandos exitosos start/prompt/wait devuelven el agente en `.result.agent`):

```bash
started=$(herdr agent start reviewer --kind codex --pane "$pane_id" --timeout 60000)
printf '%s' "$started" | jq -r '.result.agent.name'          # reviewer
printf '%s' "$started" | jq -r '.result.agent.agent_status'  # idle (listo para prompts)
printf '%s' "$started" | jq -r '.result.agent.pane_id'       # pane que lo aloja
```

## Returns jq

_jq paths to extract the returned payload into shell variables._

printf '%s' "$started" | jq -r '.result.agent.name'          # reviewer
printf '%s' "$started" | jq -r '.result.agent.agent_status'  # idle (listo para prompts)
printf '%s' "$started" | jq -r '.result.agent.pane_id'       # pane que lo aloja

## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
# 1. Crear el pane (ID capturado de la respuesta, nunca predicho)
split=$(herdr pane split --current --direction right --no-focus)
pane_id=$(printf '%s' "$split" | jq -r '.result.pane.pane_id')

# 2. Arrancar el agente en ese pane, pasando args al ejecutable tras --
herdr agent start reviewer --kind codex --pane "$pane_id" --timeout 60000 -- -m gpt-5.4

# 3. Verificar readiness y darle trabajo
herdr agent get reviewer | jq -r '.result.agent.agent_status'
herdr agent prompt reviewer "Review the current diff" --wait --timeout 120000
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| codigo | significado |
|---|---|
| `agent_pane_busy: pane is not an available shell` | El pane NO esta en su prompt de shell interactivo: hay un comando, editor o agente en foreground. La doc oficial dice literalmente: "Return the pane to its prompt before calling agent start" |
| `agent_not_ready` | Durante el arranque la deteccion reporto `blocked` en vez de listo; el comando retorna inmediatamente |
| `timeout` | No se detecto al agente listo dentro de `--timeout` (default 30000ms, max 300000ms) |
| error JSON en stderr, exit 1 | Error del server (pane inexistente, nombre duplicado, kind invalido) |
| `usage: herdr agent start ...` + exit 2 | Falta `<NAME>`, `--kind` o `--pane` |

## Notes

_Quirks, gotchas, and operational observations not covered above._

- El exito solo se anuncia cuando Herdr detecta al agente esperado EN EL MISMO TERMINAL y lo marca listo para input interactivo; el nombre queda disponible para `agent read`/`agent send-keys` y listo para prompts cuando la deteccion reporta `idle`.
- `--kind` lista real de 0.9.0 = 22 valores del `--help` (arriba). La doc oficial online menciona ademas `letta`; NO aparece en el `--help` de 0.9.0 local (no verificado en esta version).
- Con `agent_pane_busy`, devolvé el pane a su prompt (finaliza el comando agotador, cierra editor/agente) y reintenta.
- En este setup la ficha local (external-resources/herdr.md) registra que los workers se arrancan via `herdr/coordination.sh`, que usa esta misma API de agent.

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr agent start --help (herdr 0.9.0)

---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-agent-prompt
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr agent prompt
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: agent
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:agent
---

# herdr agent prompt

## Synopsis

_What the command does, in one or two sentences._

Submit a prompt to an agent

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr agent prompt <TARGET> <TEXT> [OPTIONS]

## Arguments

_Table of options: option, type, required, and what it does._

| opcion | tipo | obligatorio | que hace |
|---|---|---|---|
| <TARGET> | texto | si |  |
| <TEXT> | texto | si |  |
| --wait | texto | no | Wait for the first matching state observed after submission |
| --until <STATUS> | enum | no | State to match after --wait; repeat for more than one state [possible values: idle, working, blocked, done, unknown] |
| --timeout <MS> | numero | no | Fail after this many milliseconds |

## Returns

_What the command returns on success: JSON shape and location of the payload._

En exito con `--wait`, el JSON de la respuesta trae el agente en `.result.agent` (doc oficial: "Successful agent start, agent prompt, and agent wait commands return the current agent at .result.agent"):

```bash
printf '%s' "$result" | jq -r '.result.agent.agent_status'   # estado final matcheado
printf '%s' "$result" | jq -r '.result.agent.pane_id'        # pane del agente
```

Sin `--wait`, la sumision es fire-and-forget: forma exacta de la respuesta: no verificada en 0.9.0 local (no ejecutado para no mutar agentes vivos).

## Returns jq

_jq paths to extract the returned payload into shell variables._

printf '%s' "$result" | jq -r '.result.agent.agent_status'   # estado final matcheado
printf '%s' "$result" | jq -r '.result.agent.pane_id'        # pane del agente

## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
# Enviar trabajo y esperar a que se asiente (idle/done/blocked por defecto)
result=$(herdr agent prompt reviewer "Review the current diff" --wait --timeout 120000)
printf '%s' "$result" | jq -r '.result.agent.agent_status'

# Esperar explícitamente a que pida aprobacion
herdr agent prompt reviewer "Apply the suggested change" --wait --until blocked --timeout 60000
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| codigo | significado |
|---|---|
| `agent_blocked` | El agente YA estaba `blocked` antes de la sumision: se rechaza SIN enviar input. No se inicia la espera. Inspecciona el dialogo y responde con `agent send-keys` |
| `agent_prompt_stalled` | Partiendo de un estado no-working, no se observo `working` ni `blocked` en 5000ms tras la sumision |
| `timeout` | Vencio el `--timeout` del caller antes de matchear |
| `usage: herdr agent prompt <target> <text>` + exit 2 | Sintaxis invalida (faltan argumentos) |

## Notes

_Quirks, gotchas, and operational observations not covered above._

- Puede promptear a un agente que YA esta `working`; si ya trabaja, la espera puede matchear la terminacion de ese turno activo (no trackea turnos).
- Un timeout o `agent_prompt_stalled` NO prueba que el input no se haya enviado: lee al agente antes de reintentar para no enviar el mismo prompt dos veces.
- Estados por defecto de la espera: `idle`, `done` o `blocked`; usa `--until unknown` explicitamente si lo necesitas.

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr agent prompt --help (herdr 0.9.0)

---
id: atom-herdr-agent-lifecycle-states
status: draft
tags: [system:herdr, layer:runtime, topic:agent]
---

# herdr agent lifecycle states

## Que hace

Explica los estados de ciclo de vida de un agente herdr (`idle`, `working`, `blocked`, `done` y el quinto `unknown`) y como se observan.

## Sintaxis

No es un comando: es el modelo de estados que usan `agent list`, `agent get`, `agent wait`, `agent prompt` y `agent explain`. La deteccion corre en el server contra manifiestos (`~/.local/state/herdr/agent-detection/remote/<kind>.toml`) que matchean reglas sobre el contenido del terminal.

## Los estados

| estado | significado (doc oficial) | como se observa |
|---|---|---|
| `idle` | Listo para recibir input; la shell/UI del agente espera | `agent list` → `agent_status: idle`; `agent get` |
| `working` | El agente esta ejecutando: hay actividad en su turno | `agent wait <t> --until working --timeout N` |
| `blocked` | Herdr reconoce una UI de aprobacion o pregunta (dialogo) | `agent wait <t> --until blocked`; `--until blocked` en `prompt` |
| `done` | `idle` pero su completado aun NO fue marcado como visto (seen) | `agent wait <t> --until done` |
| `unknown` | Hay agente presente pero Herdr no clasifica su ciclo con confianza; NO prueba completacion exitosa | `--until unknown` (explicitamente; no esta en el set por defecto) |

`idle` y `done` ambos significan listo para input; `done` solo difiere en que no se ha marcado como visto. `blocked` cubre aprobaciones (`ctrl+c` no, respuestas con `agent send-keys`).

## Que devuelve

Los estados se leen del campo `agent_status` de cada agente en las respuestas JSON:

```bash
# observar estados de todos los agentes (jq exacto)
herdr agent list | jq -r '.result.agents[] | [.name, .agent_status, .pane_id] | @tsv'

# estado de uno solo
herdr agent get w1 | jq -r '.result.agent.agent_status'

# detalle de DETECCION del estado (regla + evidencia)
herdr agent explain w1 --json | jq -r '.state, .matched_rule.id'
```

## Ejemplo real

```bash
# Esperar a que el agente termine su turno (idle o done matchean por defecto)
herdr agent wait reviewer --timeout 120000 | jq -r '.result.agent.agent_status'

# Esperar a que pida input y responder a la UI
herdr agent wait reviewer --until blocked --timeout 120000
herdr agent read reviewer --source recent-unwrapped --lines 80
herdr agent send-keys reviewer esc

# Cuantas veces entro a cada estado (histograma desde list)
herdr agent list | jq -r '.result.agents[].agent_status' | sort | uniq -c
```

## Errores conocidos

| codigo | significado |
|---|---|
| `agent_not_running` | El agente dejo de correr mientras se esperaba por el (p. ej. pane movido) |
| `timeout` | La espera no matcheo dentro del `--timeout` dado |

## Notas

- `done` vs `idle`: el CLI/API usa el estado visto del server — `done` es idle sin marcar como visto; `pane focus` / `agent focus` marcan el target como visto; las LECTURAS (`agent read`) NO lo marcan. Cada cliente TUI trackea sus completados vistos por separado, asi que el badge Done de un cliente puede diferir del CLI.
- `idle`/`working`/`blocked`/`done` son los cuatro estados operativos; `unknown` es el quinto, para cuando no hay clasificacion confiable (no confundir con exito).
- Verificado en vivo 2026-09-23: estados observados `working` e `idle` (8 agentes); `blocked`, `done`, `unknown` documentados segun doc oficial, no observados localmente.
- La regla de deteccion matcheada se ve en `agent explain` (p. ej. `working_literal` sobre `whole_recent` con prioridad 100).
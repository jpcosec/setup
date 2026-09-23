---
id: atom-herdr-pane-vs-agent
status: draft
tags: [system:herdr, layer:runtime, topic:pane, topic:agent]
---

# herdr pane vs agent

## Que hace

Documenta la distincion conceptual central de herdr: un **pane** es una terminal que existe con o sin agente; un **agente** es el proceso reconocido que corre DENTRO de un pane. `agent start` exige un pane de shell ya existente y NUNCA crea ni divide layout.

## La distincion

| concepto | que es | como se crea | que lo identifica |
|---|---|---|---|
| Pane | Terminal (shell, proceso) dentro de un tab. Existe con o sin agente | `workspace create` (root pane), `tab create` (root pane), `pane split` | `pane_id` (`wX:p23`) |
| Agente | Proceso interactivo reconocido corriendo dentro de un pane (`pi`, `codex`, `claude`...) | `agent start` en un pane EXISTENTE (o deteccion automatica de un agente lanzado a mano) | `agent <name>` (`reviewer`) o el `pane_id` que lo aloja |

Fuente directa (doc oficial, agent-automation):

> "A pane exists whether or not it contains an agent. An agent is the recognized process currently running inside a pane. `agent start` therefore requires an existing shell pane and never creates, splits, or moves layout."

## Reglas de oro

- La topologia se crea SOLO con primitivas de layout: `workspace create`, `tab create`, `pane split` (ver atom-herdr-jerarquia-workspace-tab-pane).
- `agent start` exige que el pane este en su prompt de shell interactivo: el shell tiene el foreground, sin comando, editor ni agente corriendo (doc oficial). Hay que devolver el pane a su prompt antes de `agent start`.
- Un nombre de agente es un ALIAS comodo del agente actual del pane: se limpia cuando el agente sale, se libera o se reemplaza; NO renombra el pane (doc oficial).
- Los comandos de pane direccionan la terminal pase lo que pase dentro; los comandos de agente resuelven el agente vivo y rechazan la operacion si ya no controla el pane (doc oficial).
- Un pane sin agente es perfectamente util: shells, tests, servidores, watchers (doc oficial usa pane commands para eso).

## Que devuelve

Cada comando devuelve lo de su nivel:

```bash
herdr pane list | jq -r '.result.panes[] | "\(.pane_id) agent=\(.agent // "ninguno") estado=\(.agent_status // "-")"'
# pane sin agente: campo "agent" ausente; con agente: name + status idle|working|blocked|unknown
```

Estados de agente (doc oficial): `idle`/`done` = listo para input (`done` = idle aun no marcado "seen"); `blocked` = UI de aprobacion/pregunta; `unknown` = agente presente pero no clasificable (NO prueba exito).

## Ejemplo real

```bash
# Secuencia correcta: primero layout, luego agente (nunca al reves)
split=$(herdr pane split --current --direction right --no-focus)
pane_id=$(printf '%s' "$split" | jq -r '.result.pane.pane_id')          # 1. crear el pane
herdr agent start reviewer --kind codex --pane "$pane_id" -- -m gpt-5.4 # 2. agente DENTRO del pane
herdr pane get "$pane_id" | jq -r '.result.pane.agent'                  # 3. ahora el pane reporta "codex"
```

## Errores conocidos

| sintoma | causa |
|---|---|
| `agent start` falla o `agent_not_ready` | El pane no estaba en su prompt de shell (foreground ocupado) o la deteccion reporto `blocked` al arrancar (doc oficial) |
| `agent` ausente en `pane get`/`pane list` | El pane no tiene agente reconocido: es normal y valido |
| `agent_not_running` en un wait tras `pane move` | El wait quedo atado al id viejo; usa `.result.move_result.pane.pane_id` |

## Notas

- `agent start` espera readiness (default 30s, `--timeout` >3000 y <=300000 ms) y devuelve solo cuando el agente es dueño del terminal y esta listo para input interactivo (doc oficial).
- En este ecosistema: los workers son agentes interactivos en panes herdr (coordination.sh) y el layout deseado del desk se declara en desk/runtime.yaml sin ids de herdr (ver ficha external-resources/herdr.md).
- Para el panorama completo de "que comando usar": pane commands = terminales ordinarias; agent commands = cuando herdr debe entender QUE agente corre y su estado (doc oficial).
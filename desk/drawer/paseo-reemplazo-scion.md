# Paseo como reemplazo de Scion

Fecha: 2026-11-27. Estado: **decidido por JP el 28-11 («cambiemos a paseo»)** e implementado; queda retirar scion.

## Qué es

Paseo (getpaseo/paseo, Apache-2.0, v0.18.1, un mantenedor). Un daemon local (`127.0.0.1:6767`) lanza y administra
los CLI de agentes que ya tenemos instalados (pi, claude, codex, opencode y otros), con CLI, app web, móvil y de
escritorio, y un servidor MCP para que un agente lance a otros. Instalación: `npm install -g @getpaseo/cli`;
configuración en `~/.paseo/config.json`.

## Prueba en robocop (27-11)

- Detecta pi, claude y opencode sin configurar nada. Usa la configuración propia de pi (`deepseek/deepseek-flash`).
- `paseo run --provider pi --new-workspace worktree --new-branch fix/suma "..."`: creó el worktree, pi arregló el
  bug, corrió los tests e hizo commit, en 15 s.
- Tester en el mismo workspace con `--output-schema` (JSON con `veredicto` y `motivo`): devolvió
  `{"veredicto": "aprobado", ...}` ya validado.
- Además tiene `send` (con cola, `steer` o `interrupt`), `wait`, `ls --json`, `delete`, `schedule create --every`
  y `--host ssh://...` para correr en otra máquina.

## Contra scion

| | scion | Paseo |
|---|---|---|
| Aislamiento | un contenedor por agente, credenciales propias | **ninguno**: el agente corre como robocop en el host, con acceso a `~/.aws`, gh y los clones base |
| Lo nuestro encima | `deskops/dispatch.py` (768 líneas) + `runtime/scion.py` (~1.100), plantillas, harness-configs, imagen de pi | `paseo run --no-wait --json --cwd <worktree> --label task=...`, `paseo ls --json`, `paseo delete` |
| Veredicto del tester | se lee del run-dir | `--output-schema`, validado por Paseo |
| Agentes | por harness-config con imagen | los CLI instalados, tal como están |
| Seguir desde el teléfono | no | sí (relay E2EE opcional, o Tailscale) |

## Si se adopta

1. `deskops dispatch` llama a `paseo` en lugar de `scion`: el worktree lo sigue creando deskops/`wt` en el SSD y se
   pasa con `--cwd` (los de Paseo caen por omisión en `~/.paseo/worktrees`, en el disco duro).
2. El veredicto del tester con `--output-schema`.
3. Se retiran `runtime/scion.py`, las plantillas `.scion/`, la imagen de pi y el hub de scion.
4. Aislamiento, si se exige: el daemon de Paseo en su contenedor (imagen oficial `ghcr.io/getpaseo/paseo`), un
   contenedor para todos los agentes y no uno por agente.

## Hecho (28-11)

- Dormir agentes, probado: con el daemon reiniciado el proceso de pi murió (`closed`) y `paseo send` lo retomó con
  la conversación. Paseo libera un agente inactivo tras una hora (`agents.idleRuntimeCleanup`).
- deskops: `dispatch.runtime: paseo` (jpcosec/deskops#13, merge `cbcf3b75e`); `~/herramientas/deskops` está en ese
  commit. Prueba real con pi: ejecutor en su worktree → reap integra → tester PASA → reap deja paseo vacío.
- Los desks de SLDB_1 (deskops, sldb, IR, graph_ui) pasaron a paseo: ejecutor `claude` en modo `bypass`,
  tester `pi`.
- El daemon corre como `systemctl --user` `paseo.service` (127.0.0.1:6767, sin relay).

## Falta

- Retirar scion: `runtime/scion.py`, plantillas `.scion/`, imagen de pi, hub, y los espacios `mepu-scion` y
  `ftcourier-scion`. Esperar unos despachos reales con paseo antes.
- La identidad que despierta un desk (`identity.command`) sigue con `scion message --wake`: pasa a
  `paseo send --no-wait {agent} ...` cuando se use.

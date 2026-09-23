---
# Human-readable name of the resource
name: Herdr
# Official docs or repository URL
page: https://herdr.dev
# true | false — whether the resource is installed locally
installed: true
# Local install path or install command; set when installed is true
install_path: ~/.local/bin/herdr (herdr 0.9.0)
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:workspace-orchestration
---

# Herdr

## Summary

_One paragraph: what this resource is and why it matters to this setup._

Terminal workspace manager for AI coding agents; one Herdr workspace per DeskOps desk.

## How it's used

_How the resource is used in this setup: commands, hooks, workflows._

Runtime provider in desk/runtime.yaml; desired layout 'agent-dev' (nvim + executor/tester agent panes + yazi + pytest) declared without Herdr pane/process IDs.
install/init-herdr.sh [--agents] starts the Herdr server and creates the workspace via herdr/init_opsys.py.
~/.codex/herdr-agent-state.sh wired as Codex SessionStart hook.

## Status

_How it is currently working; keep empty when not installed._

0.9.0 static binary; channels managed by `herdr channel set stable|preview`.

## Issues log

_Dated log of problems, quirks, and fixes; keep empty when not installed._

- 2026-09-13: SUBUTILIZACION detectada. Herdr solo se usa para bootear UN workspace (opsys) via init-herdr.sh y nunca mas: superficie CLI usada = server start/status + workspace create.
- Sin usar: sesiones nombradas (--session), attach/detach, --remote <ssh-target>, herdr update --handoff, machine subcommand, server reload-config, multiples layouts (solo agent-dev), panes para procesos largos (bunwv daemon, pytest, fx), hooks solo en Codex SessionStart.
- El contracto dice cada DeskOps desk = 1 Herdr workspace, pero solo existe el desk opsys; los agentes solo arrancan con --agents (opcional), no por defecto.
- 2026-09-13: PARCIALMENTE RESUELTO — kit de coordinacion creado: herdr/coordination.sh (agents/dispatch/say/read/wait/spawn sobre herdr agent API) + skill agent-coordinator en .pi/skills (path agregado a settings de pi). Los workers son agentes interactivos en panes herdr; el coordinador es cualquier sesion con la skill.

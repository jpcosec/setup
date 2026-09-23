---
id: atom-herdr-README
status: draft
tags: [system:herdr, layer:runtime, topic:indice]
---

# Indice de atoms de herdr

## Que hace

Indice de TODA la documentacion de atoms de herdr en `desk/atoms/herdr/`: un atom por subcomando, mas los atoms transversales. Verificado contra el binario local `/home/jp/.local/bin/herdr` v0.9.0 (`herdr --help` real, 2026-09-23).

## Comandos de primer nivel

| Comando | Atom |
| --- | --- |
| `herdr status [server\|client]` | [atom-herdr-status.md](atom-herdr-status.md) |
| `herdr update [--handoff]` | [atom-herdr-update.md](atom-herdr-update.md) |
| `herdr completion <shell>` | [atom-herdr-completion.md](atom-herdr-completion.md) |

## Control de layout (escritos por otros workers)

| Grupo | Subcomandos | Atoms (ruta por convencion) |
| --- | --- | --- |
| workspace | create, list, get, focus, move, close, report-metadata... | atom-herdr-workspace-*.md |
| tab | create, get, focus, rename, close | atom-herdr-tab-*.md |
| pane | split, list, current, read, run, wait-output, send-keys, zoom, layout, move... | atom-herdr-pane-*.md |
| session | create, attach, list... | atom-herdr-session-*.md |

## Agentes (escritos por otros workers)

| Grupo | Subcomandos | Atoms (ruta por convencion) |
| --- | --- | --- |
| agent | list, get, start, prompt, wait, read, send-keys, rename, explain... | atom-herdr-agent-*.md |

## Grupos documentados en este lote

### worktree

| Subcomando | Atom |
| --- | --- |
| `create` | [atom-herdr-worktree-create.md](atom-herdr-worktree-create.md) |
| `list` | [atom-herdr-worktree-list.md](atom-herdr-worktree-list.md) |
| `open` | [atom-herdr-worktree-open.md](atom-herdr-worktree-open.md) |
| `remove` | [atom-herdr-worktree-remove.md](atom-herdr-worktree-remove.md) |

### machine

| Subcomando | Atom |
| --- | --- |
| `add` | [atom-herdr-machine-add.md](atom-herdr-machine-add.md) |
| `disable` | [atom-herdr-machine-disable.md](atom-herdr-machine-disable.md) |
| `enable` | [atom-herdr-machine-enable.md](atom-herdr-machine-enable.md) |
| `list` | [atom-herdr-machine-list.md](atom-herdr-machine-list.md) |
| `remove` | [atom-herdr-machine-remove.md](atom-herdr-machine-remove.md) |
| `rename` | [atom-herdr-machine-rename.md](atom-herdr-machine-rename.md) |

### api

| Subcomando | Atom |
| --- | --- |
| `schema` | [atom-herdr-api-schema.md](atom-herdr-api-schema.md) |
| `snapshot` | [atom-herdr-api-snapshot.md](atom-herdr-api-snapshot.md) |

### config

| Subcomando | Atom |
| --- | --- |
| `check` | [atom-herdr-config-check.md](atom-herdr-config-check.md) |
| `reset-keys` | [atom-herdr-config-reset-keys.md](atom-herdr-config-reset-keys.md) |

### channel

| Subcomando | Atom |
| --- | --- |
| `set` | [atom-herdr-channel-set.md](atom-herdr-channel-set.md) |
| `show` | [atom-herdr-channel-show.md](atom-herdr-channel-show.md) |

### notification

| Subcomando | Atom |
| --- | --- |
| `show` | [atom-herdr-notification-show.md](atom-herdr-notification-show.md) |

### integration

| Subcomando | Atom |
| --- | --- |
| `install` | [atom-herdr-integration-install.md](atom-herdr-integration-install.md) |
| `status` | [atom-herdr-integration-status.md](atom-herdr-integration-status.md) |
| `uninstall` | [atom-herdr-integration-uninstall.md](atom-herdr-integration-uninstall.md) |

### server

| Subcomando | Atom |
| --- | --- |
| (headless, sin subcomando) | [atom-herdr-server-headless.md](atom-herdr-server-headless.md) |
| `agent-manifests` | [atom-herdr-server-agent-manifests.md](atom-herdr-server-agent-manifests.md) |
| `reload-agent-manifests` | [atom-herdr-server-reload-agent-manifests.md](atom-herdr-server-reload-agent-manifests.md) |
| `reload-config` | [atom-herdr-server-reload-config.md](atom-herdr-server-reload-config.md) |
| `stop` | [atom-herdr-server-stop.md](atom-herdr-server-stop.md) |
| `update-agent-manifests` | [atom-herdr-server-update-agent-manifests.md](atom-herdr-server-update-agent-manifests.md) |

## Atoms transversales

| Atom | Tema |
| --- | --- |
| [atom-herdr-no-guarda-traza.md](atom-herdr-no-guarda-traza.md) | herdr no persiste traza de agentes: log sin eventos agent.*, solo lectura sin log, scrollback 10 MB en memoria, pantallas alternas fuera del scrollback, reinicio pierde contenido |
| [atom-herdr-log-sin-rotacion.md](atom-herdr-log-sin-rotacion.md) | `~/.config/herdr/herdr-server.log` crece sin rotar (~4 MB en 16 dias en este setup) |

## Por donde empezar

1. [atom-herdr-status.md](atom-herdr-status.md) — estado del ecosistema herdr local (server, cliente, versiones).
2. [atom-herdr-api-snapshot.md](atom-herdr-api-snapshot.md) — el snapshot unico: inventario de agentes, panes, workspaces con IDs reales.
3. [atom-herdr-api-schema.md](atom-herdr-api-schema.md) — contrato del socket protocol 22, versionable.
4. [atom-herdr-no-guarda-traza.md](atom-herdr-no-guarda-traza.md) — LEE ESTO ANTES de asumir que herdr puede auditar; no puede.
5. Luego los grupos de control: pane/agent/workspace (otros workers), y worktree/machine/integration/server (este lote) segun la operacion.

Regla de oro (skill oficial del binario): leer los IDs de las respuestas JSON con `jq` (`.result.pane.pane_id`, `.result.workspace.workspace_id`), nunca predecirlos ni derivarlos del orden del sidebar.
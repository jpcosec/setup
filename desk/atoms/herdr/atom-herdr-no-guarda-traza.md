---
id: atom-herdr-no-guarda-traza
status: draft
tags: [system:herdr, layer:runtime, topic:persistencia]
---

# herdr no guarda traza de agentes

## Que hace

Documenta un hecho verificado: herdr es un control remoto en vivo, no una grabadora. No persiste el contenido que pasa por los panes; la auditoria durable tiene que construirse con transcripts del propio agente.

## Hechos verificados (2026-09-23, herdr 0.9.0)

### 1. El log del server no tiene eventos agent.*

`~/.config/herdr/herdr-server.log` registra eventos de dominio: `tab.focus`, `workspace.focus`, `pane.spawn.start`, `persist.save`, `api.request.start`, `api.request.complete`, `pane.exit`, `app.startup`, ...

```bash
grep -c 'event="agent\.' ~/.config/herdr/herdr-server.log   # 0
grep -o 'event="[^"]*"' ~/.config/herdr/herdr-server.log | sort -u
# tab.focus persist.save workspace.focus api.request.* pane.spawn.start ...
```

No existe ningun tipo de evento `agent.*` con contenido.

### 2. Las llamadas de solo lectura no se loguean

El log solo captura peticiones de API con `changes_ui=true` (escrituras: `agent.prompt`, `pane.split`, `workspace.create`, ...). Ejecute `herdr api snapshot` y el log no registro nada:

```bash
grep -c 'session.snapshot' ~/.config/herdr/herdr-server.log   # 0 (tras ejecutar herdr api snapshot)
grep -o 'method="[^"]*"' ~/.config/herdr/herdr-server.log | sort | uniq -c
# 2824 agent.start  633 agent.prompt  318 pane.split ... (todas escrituras)
```

### 3. El scrollback es memoria volátil, limitado a 10 MB por pane

El limite por defecto viene en el config de referencia del binario:

```toml
# scrollback_limit_bytes = 10000000
# "Matches Ghostty's default scrollback-limit behavior"
```

Es la clave `[terminal] scrollback_limit_bytes` (verificada en `herdr --default-config` y en los strings del binario). El snapshot confirma scrollbacks en memoria (`.result.snapshot.panes[].scroll.max_offset_from_bottom`, observado hasta 6375 filas).

### 4. Los agentes TUI corren en pantalla alterna; su salida nunca entra al scrollback del host

Doc oficial (agent-automation, "Alternate-screen history reads"): agentes a pantalla completa como Claude Code y OpenCode renderizan su transcript en la pantalla alterna del terminal, NO en el scrollback de herdr. Filas que salen de la pantalla alterna no entran al scrollback del host y ningun `--lines` grande las recupera (tambien en el skill embebido del binario).

### 5. Un reinicio del server pierde el contenido (no el layout)

- En memoria: scrollbacks (10 MB/pane) y pantallas alternas — se pierden. No hay archivo de transcript ni de output de pane en `~/.config/herdr/` ni `~/.local/state/herdr/` (solo `agent-detection/`, `client-shell/`, `session.json`).
- Persiste solo el layout: `session.json` guarda `{version, workspaces, active, selected, sidebar_width, ...}` (verificado) y el log muestra `persist.save` (3342) y `persist.restore` (25) — el arranque restaura workspaces/tabs/panes vacios.

## Consecuencia operativa

- `herdr` = mando a distancia: ver estado, mandar input, leer el buffer vivo mientras vive.
- La auditoria durable (que dijo, que hizo cada agente) tiene que venir de los transcripts del agente o de grabacion propia: p.ej. `herdr agent read` volcado a archivo en el momento, o transcripts nativos de pi/codex/claude, no de herdr.
- Para captura programatica de salida usar `herdr agent read --source recent-unwrapped --lines N` o `pane read` ANTES de que el agente salga de la pantalla alterna o el server se reinicie.

## Errores conocidos

Ninguno: es una limitacion de diseno, no un fallo.

## Notas

- Matiz honesto: la cifra "10 MB" viene del default del binario y de la config de referencia, no de una medicion de consumo en vivo.
- `agent-manifests --json` y todos los comandos de solo lectura tampoco loguean (mismo mecanismo `changes_ui`).
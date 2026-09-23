---
id: atom-herdr-server-headless
status: draft
tags: [system:herdr, layer:runtime, topic:server]
---

# herdr server

## Que hace

Ejecuta herdr como servidor headless explicito (para setups supervisados o tipo servicio). Sin subcomando, `herdr server` arranca el daemon detached en primer plano de proceso.

## Sintaxis

```bash
herdr server
herdr server stop
herdr server reload-config
herdr server agent-manifests [--json]
herdr server update-agent-manifests [--json]
herdr server reload-agent-manifests
```

## Argumentos y opciones

| Comando | Tipo | Obligatorio | Que hace |
| --- | --- | --- | --- |
| (sin subcomando) | — | — | Corre el server headless (detached daemon) |
| `stop` | subcomando | — | Detiene el server via socket |
| `reload-config` | subcomando | — | Recarga config.toml en caliente |
| `agent-manifests` | subcomando | — | Muestra manifests de deteccion activos; `--json` para crudo |
| `update-agent-manifests` | subcomando | — | Descarga y recarga manifests remotos; `--json` |
| `reload-agent-manifests` | subcomando | — | Recarga overrides locales de manifests |

## Que devuelve

Cada subcomando tiene su propio atom. El arranque headless escribe log a `~/.config/herdr/herdr-server.log` y crea el socket `~/config/herdr/herdr.sock` (ambas rutas verificadas en este setup).

## Ejemplo real

```bash
# Arranque supervisado (systemd/manual): el proceso NO debe morir con la sesion
herdr server

# En este setup el arranque normal va por el TUI con daemon detached:
# herdr (TUI) -> server detached -> herdr-client.sock aparte
```

## Errores conocidos

| Codigo | Significado |
| --- | --- |
| `error: herdr server is already running` | Segundo arranque con server activo (mensaje verificado en el binario) |
| `server is shutting down` | Peticiones durante el apagado |

## Notas

- Este setup usa el daemon detached (capacidad `detached_server_daemon: true`, verificada en `herdr status server --json`), no arranca headless por systemd.
- El log del server mezcla INFO con bytes crudos de terminal (grep requiere `-a`).
---
id: atom-herdr-log-sin-rotacion
status: draft
tags: [system:herdr, layer:runtime, topic:log]
---

# herdr-server.log crece sin rotar

## Que hace

Documenta que `~/.config/herdr/herdr-server.log` es append-only y no rota: crece indefinidamente mientras el server viva.

## Hechos verificados (2026-09-23, herdr 0.9.0)

- Ruta: `/home/jp/.config/herdr/herdr-server.log`.
- Tamano: 3.996.258 bytes (~4 MB) el 2026-09-23; primera linea del `2026-09-07T19:33:12Z` (server vivo 16 dias).
- Sin rotacion: `ls ~/.config/herdr/herdr-server.log*` devuelve solo el archivo base; no hay `.1`, `.2` ni `.gz`.
- No hay config de logrotate para herdr: `ls /etc/logrotate.d/ | grep herdr` → nada.
- No hay opcion de rotacion en la config: `herdr --default-config` no expone nada de log rotation (si expone `scrollback_limit_bytes` para panes, que es otra cosa).
- Ritmo observado: ~250 KB/dia con el uso real de este setup (4 MB / 16 dias). Con agentes muy activos (agent.prompt por minuto) crece mas: el log registra una linea `api.request.start` + `api.request.complete` por cada escritura de API.

## Contenido del log

- Lineas INFO con marca ISO-8601 UTC, ejemplo real:

```text
2026-09-23T12:17:56.522790Z  INFO herdr::logging: api request completed event="api.request.complete" subsystem="api" outcome="ok" request_id="cli:agent:prompt" method="agent.prompt"
```

- Mezcla bytes con control sequences de terminal: `grep` normal dice "binary file matches"; usar `grep -a`.
- Volumen por evento (cuenta sobre 4 MB): 6535 `tab.focus`, 2824 `agent.start`, 633 `agent.prompt`, ~2100 `api.request.start/complete`.

## Consecuencias

- Disco: ~3 MB/mes por server siempre activo; crece con el ruido de agentes.
- Diagnostico lento: `grep` y aperturas degradan, y hay que usar `-a`.
- Sin punto de corte para auditoria: no hay archivo anterior con que comparar "el server lleva vivo X".

## Notas y mitigaciones (no implementadas, solo opciones)

- No existe comando `herdr log rotate` (no esta en el `--help` de 0.9.0; no verificado si existe en versiones futuras).
- Opciones externas: `logrotate` con `copytruncate` sobre `~/.config/herdr/herdr-server.log`, o truncado manual `: > ~/.config/herdr/herdr-server.log` (el server lo reabre en append; el puntero no se pierde con copytruncate es mas seguro).
- El detalle fino de los datos de auditoria NO esta en este log de todos modos: ver `atom-herdr-no-guarda-traza`.
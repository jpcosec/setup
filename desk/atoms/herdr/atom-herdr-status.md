---
id: atom-herdr-status
status: draft
tags: [system:herdr, layer:runtime, topic:status]
---

# herdr status

## Que hace

Muestra el estado del cliente local y del servidor en ejecucion, en una sola vista o por separado.

## Sintaxis

```bash
herdr status [OPTIONS] [COMMAND]
```

Subcomandos (verificados con `herdr status server --help` y `herdr status client --help`):

```bash
herdr status
herdr status server [--json]
herdr status client [--json]
```

## Argumentos y opciones

| Opcion | Tipo | Obligatorio | Que hace |
| --- | --- | --- | --- |
| `--json` | flag | no | Emite la salida como JSON (una linea) en lugar de texto |
| `server` | subcomando | no | Muestra solo el estado del servidor |
| `client` | subcomando | no | Muestra solo el estado del cliente local |

## Que devuelve

Con `--json` emite un objeto con tres claves (verificado con herdr 0.9.0):

```json
{"client": {...}, "server": {...}, "update": {...}}
```

- `.client` → `version`, `channel`, `protocol`, `binary`, `session`.
- `.server` → `status`, `running`, `version`, `protocol`, `capabilities`, `compatible`, `socket`, `restart_needed`, `server_binary_stale`.
- `.update` → `restart_needed`, `server_binary_stale`.

Rutas jq utiles:

```bash
jq -r '.server.running'      # true|false
jq -r '.server.socket'       # /home/jp/.config/herdr/herdr.sock
jq -r '.server.compatible'   # true si cliente y servidor son compatibles
jq -r '.client.version'      # version del binario local
jq -r '.server.version'      # version del server en ejecucion
```

`herdr status server --json` devuelve solo el objeto `.server`; `herdr status client --json` solo `.client`.

## Ejemplo real

```bash
# ¿El servidor esta corriendo y es compatible?
herdr status --json | jq -r '.server.running, .server.compatible'

# Socket del servidor para diagnosticar por que no conecta
herdr status server --json | jq -r '.socket'
```

## Errores conocidos

| Codigo | Significado |
| --- | --- |
| `server_unavailable` | El servidor se esta apagando o no responde (string presente en el binario) |
| salida no JSON | Sin `--json`, la salida es texto human-readable; su forma exacta no verificada |

## Notas

- Verificado 2026-09-23: cliente y servidor en 0.9.0, `compatible: true`, socket `/home/jp/.config/herdr/herdr.sock`, `channel: stable`, `session: null` (sin sesion nombrada activa).
- `herdr status` es de solo lectura: no aparece en el log del server (ver `atom-herdr-no-guarda-traza`).
- Si `server_binary_stale` o `restart_needed` es true, conviene `herdr update` o reiniciar el server.
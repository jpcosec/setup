---
id: atom-herdr-update
status: draft
tags: [system:herdr, layer:runtime, topic:update]
---

# herdr update

## Que hace

Descarga e instala la ultima version de herdr para el canal configurado.

## Sintaxis

```bash
herdr update [OPTIONS]
```

## Argumentos y opciones

| Opcion | Tipo | Obligatorio | Que hace |
| --- | --- | --- | --- |
| `--handoff` | flag | no | Trata de hacer live handoff tras instalar, para no perder el estado de la sesion |

## Que devuelve

No verificado: no se ejecuto `herdr update` durante esta documentacion (instala software). La salida esperada es texto de progreso de descarga/instalacion; no hay forma JSON documentada en el --help.

## Ejemplo real

```bash
# Actualizar a la version del canal estable (ojo: reemplaza el binario ~/.local/bin/herdr)
herdr update

# Actualizar y conservar la sesion viva si el server lo soporta
herdr update --handoff
```

## Errores conocidos

| Codigo | Significado |
| --- | --- |
| canal invalido | `herdr update` usa el canal de `herdr channel`; valores validos `stable` y `preview` |
| sin conexion | No verificado: mensaje exacto de error de red no capturado |

## Notas

- Verificado: en este setup la instalacion es el binario estatico `/home/jp/.local/bin/herdr` (herdr 0.9.0, canal `stable`).
- Si el server en ejecucion es mas nuevo que el cliente, `herdr status` reporta `server_binary_stale`; `update` solo toca el binario local, no reinicia el server.
- `--handoff` requiere servidor con capacidad `live_handoff` (verificada a true en este setup via `herdr status server --json`).
---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-channel-set
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr channel set
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: channel
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:channel
---

# herdr channel set

## Synopsis

_What the command does, in one or two sentences._

Choose the update channel

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr channel set <CHANNEL>

## Arguments

_Table of options: option, type, required, and what it does._

| opcion | tipo | obligatorio | que hace |
|---|---|---|---|
| <CHANNEL> | enum | si | [possible values: stable, preview] |

## Returns

_What the command returns on success: JSON shape and location of the payload._

No verificado: no se ejecuto para no cambiar la config local. Respuesta humana esperada tipo texto confirmando el canal.

## Returns jq

_jq paths to extract the returned payload into shell variables._



## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
# Cambiar a preview para recibir builds por adelantado
herdr channel set preview
herdr channel show   # confirma: preview

# Volver a estable
herdr channel set stable
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| Codigo | Significado |
| --- | --- |
| valor fuera de `[stable, preview]` | Error de validacion de clap (el --help lista los posibles valores) |
| fallo de escritura de config | Mensaje exacto no verificado |

## Notes

_Quirks, gotchas, and operational observations not covered above._

- El canal actual afecta a `herdr update` y a los chequeos de version en segundo plano (`update.check.start`/`update.available` en el log del server).
- Este setup esta en `stable` (verificado via `herdr channel show` = `stable`).

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr channel set --help (herdr 0.9.0)

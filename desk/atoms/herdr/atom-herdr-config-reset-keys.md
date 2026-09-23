---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-config-reset-keys
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr config reset-keys
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: config
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:config
---

# herdr config reset-keys

## Synopsis

_What the command does, in one or two sentences._

Reset custom keybindings

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr config reset-keys

## Arguments

_Table of options: option, type, required, and what it does._



## Returns

_What the command returns on success: JSON shape and location of the payload._

No verificado: no se ejecuto (muta `~/.config/herdr/config.toml`). La descripcion del --help dice textualmente "Back up config.toml and remove custom keybindings"; la salida esperable es texto confirmando el backup y el reset.

## Returns jq

_jq paths to extract the returned payload into shell variables._



## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
# Antes: copia de seguridad manual extra por si acaso
cp ~/.config/herdr/config.toml /tmp/herdr-config.bak
herdr config reset-keys
herdr config check   # validar que el resultado sigue parseando
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| Codigo | Significado |
| --- | --- |
| error de backup | Si no se puede escribir el backup junto al config, el comando aborta (mensaje exacto no verificado) |

## Notes

_Quirks, gotchas, and operational observations not covered above._

- Solo afecta a `[keys]`; los temas y el resto de secciones se conservan (semantica del help).
- En este setup el config es minimo (51 bytes) y usa los defaults, asi que reset-keys no tendria efecto visible.
- El backup lo crea el propio comando; la ruta exacta del backup no esta verificada.

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr config reset-keys --help (herdr 0.9.0)

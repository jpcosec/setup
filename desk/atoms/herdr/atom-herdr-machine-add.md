---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-machine-add
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr machine add
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: machine
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:machine
---

# herdr machine add

## Synopsis

_What the command does, in one or two sentences._

Prepare the remote Herdr server and save an SSH machine

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr machine add [OPTIONS] --label <LABEL> <SSH_TARGET>

## Arguments

_Table of options: option, type, required, and what it does._

| opcion | tipo | obligatorio | que hace |
|---|---|---|---|
| <SSH_TARGET> | texto | si |  |
| --label <LABEL> | texto | no | Set the machine label shown in the sidebar |
| --remote-session <NAME> | texto | no | Set the explicit Herdr session on the remote machine |

## Returns

_What the command returns on success: JSON shape and location of the payload._

Respuesta JSON `cli:machine:add` (shape exacto de `.result` no verificado: el comando no se ejecuto porque prepara y conecta servidores remotos). Si el setup falla o se cancela, no se guarda perfil (doc oficial).

```bash
herdr machine add workbox --label "Build machine" | jq -r '.result'
```

## Returns jq

_jq paths to extract the returned payload into shell variables._

herdr machine add workbox --label "Build machine" | jq -r '.result'

## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
# Añadir una maquina remota por perfil SSH
herdr machine add buildhost --label "Build machine"
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| Codigo | Significado |
| --- | --- |
| `SSH target must not contain a password` | No se admite password embebida en el target |
| `endpoint selection exceeds the storage limite` | Demasiados perfiles guardados |
| `remote server is not ready for saved machines` | El remoto no preparo su servidor |
| `remote server startup failed` | No pudo arrancar el server remoto durante el setup |
| `expected endpoint welcome` / `server does not support the stable Herdr endpoint protocol` | Version remota incompatible |

## Notes

_Quirks, gotchas, and operational observations not covered above._

- Verificado en la doc oficial (0.9.1): `machine add` comprueba capacidades remotas, instala/actualiza solo con aprobacion, y arranca el server de fondo de la sesion antes de guardar. Version compatible no implica version identica.
- Reemplazar un server en ejecucion pide aprobacion explicita con respuesta por defecto "No" y detiene los procesos de sus panes.
- No habilita handoff experimental implicitamente.
- Nunca se ejecuto en este setup (2026-09-23): `herdr machine list --json` devuelve `[]`.

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr machine add --help (herdr 0.9.0)

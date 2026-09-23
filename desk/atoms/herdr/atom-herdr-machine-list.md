---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-machine-list
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr machine list
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: machine
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:machine
---

# herdr machine list

## Synopsis

_What the command does, in one or two sentences._

List saved SSH machines

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr machine list [OPTIONS]

## Arguments

_Table of options: option, type, required, and what it does._

| opcion | tipo | obligatorio | que hace |
|---|---|---|---|
| --json | texto | no |  |

## Returns

_What the command returns on success: JSON shape and location of the payload._

JSON con `--json` (verificado en este setup, sin perfiles):

```json
[]
```

Con perfiles guardados seria un array de objetos con el shape del perfil (no verificado: lista vacia aqui). Rutas jq utiles (validas con `--json`):

```bash
jq -r '.[].id'          # IDs de perfil
jq -r '.[] | .label'    # etiquetas visibles en sidebar
```

Sin `--json` la salida es texto con etiquetas/estado (forma exacta no verificada en este setup).

## Returns jq

_jq paths to extract the returned payload into shell variables._

Con perfiles guardados seria un array de objetos con el shape del perfil (no verificado: lista vacia aqui). Rutas jq utiles (validas con `--json`):
jq -r '.[].id'          # IDs de perfil
jq -r '.[] | .label'    # etiquetas visibles en sidebar

## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
# Sacar el ID del primer perfil con etiqueta "Build machine"
herdr machine list --json | jq -r '.[] | select(.label == "Build machine") | .id'
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| Codigo | Significado |
| --- | --- |
| `endpoint selection exceeds the storage limite` | Catalogo de perfiles lleno |
| sin servidor | `machine list` lee el catalogo local; no requiere server corriendo (no verificado al detalle) |

## Notes

_Quirks, gotchas, and operational observations not covered above._

- Verificado 2026-09-23: este setup tiene 0 perfiles (`herdr machine list --json` → `[]`); `--remote` y las maquinas son funcionalidad sin usar hasta ahora.
- El skill oficial avisa: los IDs de maquina son por servidor; dos maquinas pueden tener `w1:p1` o el mismo nombre de agente. `machine list` no retargetea comandos: hay que usar `--machine <profile>` explicito.

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr machine list --help (herdr 0.9.0)

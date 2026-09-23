---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-api-schema
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr api schema
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: api
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:api
---

# herdr api schema

## Synopsis

_What the command does, in one or two sentences._

Print or write the bundled API schema

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr api schema [OPTIONS]

## Arguments

_Table of options: option, type, required, and what it does._

| opcion | tipo | obligatorio | que hace |
|---|---|---|---|
| --json | texto | no |  |
| --output <PATH> | texto | no |  |

## Returns

_What the command returns on success: JSON shape and location of the payload._

Sin opciones: resumen de texto (verificado, herdr 0.9.0):

```text
Herdr API schema
protocol: 22
schema_version: 1
schemas: error_response, event, request, subscription_event, success_response

Use `herdr api schema --json` to print the full schema.
Use `herdr api schema --output PATH` to write it to a file.
```

Con `--output`: escribe el JSON Schema (verificado: 275129 bytes en este setup) y devuelve `wrote API schema to <path>`.

```bash
herdr api schema --output /tmp/herdr-schema.json
jq -r '.protocol' /tmp/herdr-schema.json                 # 22
jq -r '.schemas | keys[]' /tmp/herdr-schema.json          # error_response event request subscription_event success_response
jq -r '.schemas.success_response.properties.result.anyOf[0].enum[]' /tmp/herdr-schema.json   # tipos de result (worktree_list, session_snapshot, ...)
```

## Returns jq

_jq paths to extract the returned payload into shell variables._

jq -r '.protocol' /tmp/herdr-schema.json                 # 22
jq -r '.schemas | keys[]' /tmp/herdr-schema.json          # error_response event request subscription_event success_response
jq -r '.schemas.success_response.properties.result.anyOf[0].enum[]' /tmp/herdr-schema.json   # tipos de result (worktree_list, session_snapshot, ...)

## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
# Versionar el contrato del socket junto a los scripts de coordinacion
herdr api schema --output /home/jp/setup/herdr-api.schema.json
jq -r '.protocol' /home/jp/setup/herdr-api.schema.json
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| Codigo | Significado |
| --- | --- |
| ruta de `--output` no escribible | Error del sistema de archivos al abrir (mensaje exacto no verificado) |

## Notes

_Quirks, gotchas, and operational observations not covered above._

- El schema viaja con el binario: un `herdr api schema` nuevo refleja exactamente el protocolo que habla este binario.
- El enum de `result.type` real en 0.9.0 incluye: `worktree_list`, `session_snapshot`, `worktree_created`, `config_reload`, `agent_manifest_status`, `notification_show`, `integration_install`, `ok`, etc. (verificado en el archivo generado).
- Verificado 2026-09-23 en este setup: `protocol: 22`, `schema_version: 1`.

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr api schema --help (herdr 0.9.0)

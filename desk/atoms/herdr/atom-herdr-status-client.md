---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-status-client
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr status client
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: status
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:status
---

# herdr status client

## Synopsis

_What the command does, in one or two sentences._

Show local client status

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr status client [OPTIONS]

## Arguments

_Table of options: option, type, required, and what it does._

| opcion | tipo | obligatorio | que hace |
|---|---|---|---|
| --json | texto | no |  |

## Returns

_What the command returns on success: JSON shape and location of the payload._



## Returns jq

_jq paths to extract the returned payload into shell variables._



## Example

_Real end-to-end usage, verified when possible, with output captured via jq._



## Errors

_Known error codes or symptoms, their meaning, and recovery steps._



## Notes

_Quirks, gotchas, and operational observations not covered above._



## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr status client --help (herdr 0.9.0)

---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-worktree-open
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr worktree open
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: worktree
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:worktree
---

# herdr worktree open

## Synopsis

_What the command does, in one or two sentences._

Open an existing Git worktree

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr worktree open [OPTIONS]

## Arguments

_Table of options: option, type, required, and what it does._

| opcion | tipo | obligatorio | que hace |
|---|---|---|---|
| --workspace <ID> | texto | no |  |
| --cwd <PATH> | texto | no |  |
| --path <PATH> | texto | no |  |
| --branch <NAME> | texto | no |  |
| --label <TEXT> | texto | no |  |
| --focus | texto | no |  |
| --no-focus | texto | no |  |
| --trust-repository | texto | no |  |

## Returns

_What the command returns on success: JSON shape and location of the payload._

JSON `cli:worktree:open` con `result.type: worktree_opened`. Shape exacto de `.result` no verificado (no ejecutado: requiere un worktree existente no abierto). Usa jq sobre el result:

```bash
herdr worktree open --cwd "$PWD" --branch feature/ui | jq -r '.result.workspace_id'
```

## Returns jq

_jq paths to extract the returned payload into shell variables._

JSON `cli:worktree:open` con `result.type: worktree_opened`. Shape exacto de `.result` no verificado (no ejecutado: requiere un worktree existente no abierto). Usa jq sobre el result:
herdr worktree open --cwd "$PWD" --branch feature/ui | jq -r '.result.workspace_id'

## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
# Abrir el worktree ya creado en la rama feature/ui
herdr worktree open --cwd "$PWD" --branch feature/ui --no-focus \
  | jq -r '.result.workspace_id'
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| Codigo | Significado |
| --- | --- |
| `exactly one of path or branch is required` | Faltan o sobran selectores |
| `worktree_not_found` | No existe checkout con esa rama/ruta |
| `ambiguous_worktree_branches` | Varios checkouts matchean la misma rama |
| `worktree_open_failed` | Fallo generico de apertura |
| `opened worktree workspace should have an active tab` / `... active root pane` | Estado interno roto tras abrir (string del binario) |

## Notes

_Quirks, gotchas, and operational observations not covered above._

- Un worktree ya abierto en un workspace reporta `open_workspace_id` en `worktree list`; abrirlo de nuevo puede fallar con `already_open` (string `already_open` presente en el binario).
- Al abrir, el workspace queda agrupado al parent (doc oficial).
- No ejecutado en este setup: no hay worktrees herdr abiertos adicionales disponibles para probar sin mutar estado.

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr worktree open --help (herdr 0.9.0)

---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-worktree-list
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr worktree list
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: worktree
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:worktree
---

# herdr worktree list

## Synopsis

_What the command does, in one or two sentences._

List worktree workspaces

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr worktree list [OPTIONS]

## Arguments

_Table of options: option, type, required, and what it does._

| opcion | tipo | obligatorio | que hace |
|---|---|---|---|
| --workspace <ID> | texto | no |  |
| --cwd <PATH> | texto | no |  |
| --trust-repository | texto | no |  |

## Returns

_What the command returns on success: JSON shape and location of the payload._

JSON (verificado, herdr 0.9.0). Shape real capturado:

```json
{"id":"cli:worktree:list","result":{
  "source":{"repo_key":".../.git","repo_name":"...","repo_root":"...","source_checkout_path":"...","source_workspace_id":"wY"},
  "type":"worktree_list",
  "worktrees":[{"branch":"...","is_bare":false,"is_detached":false,"is_linked_worktree":false,"is_prunable":false,"label":"...","open_workspace_id":"wY","path":"..."}]}}
```

Rutas jq utiles:

```bash
jq -r '.result.worktrees[].path'                      # rutas de todos los checkouts
jq -r '.result.worktrees[] | select(.is_linked_worktree) | .branch'  # ramas de linked worktrees
jq -r '.result.source.repo_key'                       # repositorio resolvido
jq -r '.result.worktrees[] | select(.open_workspace_id != null) | .open_workspace_id'  # workspaces abiertos
```

## Returns jq

_jq paths to extract the returned payload into shell variables._

Rutas jq utiles:
jq -r '.result.worktrees[].path'                      # rutas de todos los checkouts
jq -r '.result.worktrees[] | select(.is_linked_worktree) | .branch'  # ramas de linked worktrees
jq -r '.result.source.repo_key'                       # repositorio resolvido
jq -r '.result.worktrees[] | select(.open_workspace_id != null) | .open_workspace_id'  # workspaces abiertos

## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
# Listar worktrees del repo del workspace actual y abrir solo los linked
herdr worktree list --cwd "$PWD" | jq -r '.result.worktrees[] | select(.is_linked_worktree) | "\(.branch) -> \(.path)"'
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| Codigo | Significado |
| --- | --- |
| `Herdr worktree actions require a path inside a Git work tree` | El `--cwd`/`--workspace` no esta en un repositorio git |
| `Herdr worktree actions require a workspace inside a Git work tree` | El workspace no tiene repositorio asociado |
| `workspace not found` | `--workspace` inexistente |

## Notes

_Quirks, gotchas, and operational observations not covered above._

- Ejecutado real en este setup (2026-09-23): listo sobre AWS_Infra, devolvio 3 worktrees (1 normal + 2 linked bajo `AWS_Infra_worktrees/`). `open_workspace_id` solo aparece en el worktree abierto como workspace.
- `is_linked_worktree: true` identifica checkouts creados con `worktree create`/`open`; `is_prunable` senala registros git obsoletos.

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr worktree list --help (herdr 0.9.0)

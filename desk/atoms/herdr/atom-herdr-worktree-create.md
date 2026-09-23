---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-worktree-create
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr worktree create
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: worktree
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:worktree
---

# herdr worktree create

## Synopsis

_What the command does, in one or two sentences._

Create and open a Git worktree

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr worktree create [OPTIONS]

## Arguments

_Table of options: option, type, required, and what it does._

| opcion | tipo | obligatorio | que hace |
|---|---|---|---|
| --workspace <ID> | texto | no |  |
| --cwd <PATH> | texto | no |  |
| --branch <NAME> | texto | no |  |
| --base <REF> | texto | no |  |
| --path <PATH> | texto | no |  |
| --label <TEXT> | texto | no |  |
| --focus | texto | no |  |
| --no-focus | texto | no |  |
| --trust-repository | texto | no |  |

## Returns

_What the command returns on success: JSON shape and location of the payload._

Respuesta JSON con `id: cli:worktree:create` y `result.type: worktree_created`. El shape exacto de `.result` no esta verificado (comando no ejecutado: muta el repo). Por el contrato de creacion de la doc oficial, devuelve el workspace creado; usa jq sobre el result en vez de predecir IDs:

```bash
herdr worktree create --cwd "$PWD" --branch feat --label feat | jq -r '.result.workspace.workspace_id'
```

## Returns jq

_jq paths to extract the returned payload into shell variables._

Respuesta JSON con `id: cli:worktree:create` y `result.type: worktree_created`. El shape exacto de `.result` no esta verificado (comando no ejecutado: muta el repo). Por el contrato de creacion de la doc oficial, devuelve el workspace creado; usa jq sobre el result en vez de predecir IDs:
herdr worktree create --cwd "$PWD" --branch feat --label feat | jq -r '.result.workspace.workspace_id'

## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
# Crear un worktree para la rama feature/ui desde el repo actual
herdr worktree create --cwd "$PWD" --branch feature/ui --label ui --no-focus \
  | jq -r '.result.workspace.workspace_id'
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| Codigo | Significado |
| --- | --- |
| `worktree_not_found` / `worktree branch not found` | La rama pedida no existe y no pudo crearse |
| `dirty_worktree_requires_force` | El checkout esta sucio (propio de `remove`, no de create) |
| `only one of workspace_id or cwd may be supplied` | Pasar ambos `--workspace` y `--cwd` a la vez |
| `workspace not found` | El `--workspace` indicado no existe |
| `worktree_operation_in_progress` | Ya hay una operacion de worktree sobre ese checkout |
| `worktree_create_failed` | Fallo generico de creacion |

## Notes

_Quirks, gotchas, and operational observations not covered above._

- Los worktrees de herdr son workspaces normales con procedencia git; se agrupan con el workspace padre (string del binario: "New and open worktree actions start from the repo parent workspace").
- Verificado (doc oficial 0.9.1): sin `--path`, el checkout se crea bajo el directorio de worktrees del repo.
- No ejecutado en este setup: no se creo ningun worktree durante la documentacion. Shape de `.result` = no verificado.

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr worktree create --help (herdr 0.9.0)

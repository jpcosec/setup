---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-pane-run
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr pane run
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: pane
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:pane
---

# herdr pane run

## Synopsis

_What the command does, in one or two sentences._

Run a command in a pane

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr pane run <PANE_ID> <COMMAND>...

## Arguments

_Table of options: option, type, required, and what it does._

| opcion | tipo | obligatorio | que hace |
|---|---|---|---|
| <PANE_ID> | texto | si |  |
| <COMMAND>... | texto | si |  |

## Returns

_What the command returns on success: JSON shape and location of the payload._

Exito **silencioso**: sin salida en stdout ni stderr, exit 0 (verificado en vivo). Nada que parsear con jq en exito:

```bash
herdr pane run "$pane_id" 'echo hola'
echo "exit=$?"   # -> 0, sin salida
```

## Returns jq

_jq paths to extract the returned payload into shell variables._

Exito **silencioso**: sin salida en stdout ni stderr, exit 0 (verificado en vivo). Nada que parsear con jq en exito:

## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
# Disparar un test-watcher en el pane de ejecucion
herdr pane run "$pane_id" 'just test --watch'

# Esperar su salida antes de seguir (patron de la doc oficial)
herdr pane wait-output "$pane_id" --regex 'passed|failed' --timeout 120000
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| codigo / sintoma | significado |
|---|---|
| `pane_not_found` en stderr, exit 1 | Pane inexistente |
| exit 2 texto plano | Sintaxis invalida del CLI |

## Notes

_Quirks, gotchas, and operational observations not covered above._

- **Diferencia clave con send-* (doc oficial)**: `pane run` = envia texto + Enter de una vez y honra el bracketed-paste; `pane send-text` = texto literal SIN Enter (bajo nivel, no somete); `pane send-keys` = teclas o acordes (`enter`, `ctrl+c`, `up`...), no texto de comando.
- Regla practica: para COMANDOS usa `run`; para pegar trozos de texto usa `send-text` (+ `send-keys enter` si quieres someter); para teclas UI usa `send-keys`.
- No interpreta el ciclo de vida del agente: para prompts de agentes es `agent prompt` (la version de run para agentes, doc oficial).
- `pane run` NO espera a que termine el comando: solo somete; espera con `pane wait-output`.

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr pane run --help (herdr 0.9.0)

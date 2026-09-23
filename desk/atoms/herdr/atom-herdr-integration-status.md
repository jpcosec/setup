---
# Canonical atom identifier, conventionally 'atom-herdr-<command>-<verb>'
id: atom-herdr-integration-status
# Full command as typed, e.g. 'herdr agent start'
command_path: herdr integration status
# Command family grouping, e.g. 'agent', 'pane', 'machine'
command_group: integration
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:herdr
- layer:runtime
- topic:integration
---

# herdr integration status

## Synopsis

_What the command does, in one or two sentences._

Show integration status

## Syntax

_Usage line(s) with brackets for optionals, as shown by the command help._

herdr integration status [OPTIONS]

## Arguments

_Table of options: option, type, required, and what it does._

| opcion | tipo | obligatorio | que hace |
|---|---|---|---|
| --outdated-only | texto | no |  |

## Returns

_What the command returns on success: JSON shape and location of the payload._

Texto plano, no JSON (verificado, salida real 2026-09-23):

```text
pi: current (v8) (/home/jp/.pi/agent/extensions/herdr-agent-state.ts)
omp: not installed (/home/jp/.omp/agent/extensions/herdr-omp-agent-state.ts)
claude: current (v9) (/home/jp/.claude/hooks/herdr-agent-state.sh)
codex: current (v8) (/home/jp/.codex/herdr-agent-state.sh)
...
opencode: current (v11) (/home/jp/.config/opencode/plugins/herdr-agent-state.js)
...
antigravity-cli: current (v3) (/home/jp/.gemini/config/hooks/herdr-agent-state.sh)
grok: not installed (/home/jp/.grok/hooks/herdr-agent-state.sh)
```

Estados posibles: `current (vN)` (instalada y al dia), `outdated (vN -> vM)` (pendiente de actualizar), `not installed`. Con `--outdated-only`, si nada esta desactualizado la salida es vacia (verificado: salida vacia en este setup).

## Returns jq

_jq paths to extract the returned payload into shell variables._



## Example

_Real end-to-end usage, verified when possible, with output captured via jq._

```bash
# ¿Que integraciones faltan o estan viejas?
herdr integration status --outdated-only

# Extraer solo las rutas instaladas (lineas "current")
herdr integration status | sed -n 's/.*current.*(\(.*\)).*/\1/p'
```

## Errors

_Known error codes or symptoms, their meaning, and recovery steps._

| Codigo | Significado |
| --- | --- |
| sin server | `integration status` parece leer estado local; si requiere el server el fallo seria `server_unavailable` (no verificado) |

## Notes

_Quirks, gotchas, and operational observations not covered above._

- No hay modo `--json` en 0.9.0 (verificado en el --help): la salida es texto; parsear con `sed`/`awk` (sin IDs que capturar con jq).
- Este setup tiene 5 integraciones instaladas y al dia: pi, claude, codex, opencode, antigravity-cli.
- La marca `// installed by herdr` en los archivos instalados identifica escrituras de herdr (string del binario).

## Provenance

_Source of the documented behavior: help output, official docs, live verification, date and herdr version._

herdr integration status --help (herdr 0.9.0)

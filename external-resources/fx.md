---
# Human-readable name of the resource
name: fx
# Official docs or repository URL
page: https://github.com/vercel-labs/fx
# true | false — whether the resource is installed locally
installed: true
# Local install path or install command; set when installed is true
install_path: '~/.local/bin/fx (fx 0.0.9); instalado con: curl -fsSL https://fx.sh/setup.sh
  | bash'
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:fx
- layer:runtime
- topic:agent-cli
---

# fx

## Summary

_One paragraph: what this resource is and why it matters to this setup._

Tiny, open-source (Apache-2.0), model-agnostic coding agent CLI written in Zig: a 6.17 MiB native binary with a Unix-shell-like interface. Experimental. Login via Vercel AI Gateway, Codex OAuth (ChatGPT subscription) or Grok OAuth; embeddable as harness via ACP or the libfx WASM SDK (createFxAgent / createFxTerminal); extensible with skills, MCP and subagents.

## How it's used

_How the resource is used in this setup: commands, hooks, workflows._

Not installed. Install: curl -fsSL https://fx.sh/setup.sh | bash; then `fx` for the interactive shell or `fx ask "..."` for one-shots; `fx login codex` reuses a ChatGPT subscription. Notably, its repo ships benchmarks comparing against pi (benchmarks/libfx/bench-pi.mjs).

## Status

_How it is currently working; keep empty when not installed._

fx 0.0.9 (static ELF, ~11.8 MB) instalado y corriendo; sin login configurado todavia: fx login (Vercel AI Gateway) o fx login codex pendientes.

## Issues log

_Dated log of problems, quirks, and fixes; keep empty when not installed._

- 2026-09-13: instalado via setup.sh oficial sin errores; verificado fx --version -> 0.0.9.
- 2026-09-13: el binario instalado pesa ~11.8 MB, no los 6.17 MiB que reclama el README (v0.0.9 crecio desde la verificacion de docs de julio 2026).

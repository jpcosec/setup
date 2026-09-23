---
# Human-readable name of the resource
name: Claude Code
# Official docs or repository URL
page: https://claude.com/claude-code
# true | false — whether the resource is installed locally
installed: true
# Local install path or install command; set when installed is true
install_path: ~/.local/bin/claude (2.1.270)
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:claude-code
- layer:runtime
- topic:agent-cli
---

# Claude Code

## Summary

_One paragraph: what this resource is and why it matters to this setup._

Agente terminal de Anthropic. Headless: claude -p con output-format (text/json/stream-json); --resume; agentes en background (claude agents, dispatched sessions con --add-dir); hooks; plugins y marketplaces; cliente MCP (claude mcp) y modo servidor MCP (claude mcp serve).

## How it's used

_How the resource is used in this setup: commands, hooks, workflows._

Interactivo o claude -p "prompt" para headless; claude agents para sesiones despachadas en background; claude mcp add para herramientas externas; hooks en settings.json.

## Status

_How it is currently working; keep empty when not installed._

Sin MCP servers configurados (mcpServers vacio en ~/.claude.json); no forma parte del runtime del desk (no aparece en runtime.yaml).

## Issues log

_Dated log of problems, quirks, and fixes; keep empty when not installed._

- 2026-09-13: primer inventario: instalado y actualizado, pero sin integraciones activas (ni MCP ni hooks herdr).

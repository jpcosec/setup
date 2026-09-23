---
# Human-readable name of the resource
name: opencode
# Official docs or repository URL
page: https://opencode.ai
# true | false — whether the resource is installed locally
installed: true
# Local install path or install command; set when installed is true
install_path: ~/.npm-global/bin/opencode (1.15.4, npm global)
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:opencode
- layer:runtime
- topic:agent-cli
---

# opencode

## Summary

_One paragraph: what this resource is and why it matters to this setup._

Terminal coding agent open-source (TS): TUI + superficies de integracion muy completas. Headless: opencode run "msg". Servidor HTTP headless (opencode serve) con opencode attach <url>. Servidor ACP sobre stdio (opencode acp). Cliente MCP, plugins JS, comandos/agents custom, sesiones con export/import JSON.

## How it's used

_How the resource is used in this setup: commands, hooks, workflows._

TUI por defecto; opencode run para one-shots; serve+attach para sesion remota/HTTP; acp para integrarlo como agente en editores u orquestadores; export/import de sesiones en JSON para post-mortem.

## Status

_How it is currently working; keep empty when not installed._

Config en ~/.config/opencode: plugins @plannotator/opencode, @different-ai/opencode-browser (browser tool), opencode-froggy; MCP servers ya montados: serena, playwright, testsprite, aws-mcp; plugin herdr-agent-state.js y comandos plannotator-*. Existe backup opencode.json.bak-agent-toolkit (experimento abandonado).

## Issues log

_Dated log of problems, quirks, and fixes; keep empty when not installed._

- 2026-09-13: backup bak-agent-toolkit en config indica churn de configuracion; revisar si las 4 tools MCP siguen usandose.

---
# Human-readable name of the resource
name: Codex CLI
# Official docs or repository URL
page: https://github.com/openai/codex
# true | false — whether the resource is installed locally
installed: true
# Local install path or install command; set when installed is true
install_path: ~/.local/bin/codex (codex-cli 0.154.0); config ~/.codex/
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:codex
- layer:runtime
- topic:agent-cli
---

# Codex CLI

## Summary

_One paragraph: what this resource is and why it matters to this setup._

OpenAI coding agent CLI; second agent runtime alongside Pi, target host for agent skills such as editable-design.

## How it's used

_How the resource is used in this setup: commands, hooks, workflows._

Config lives in ~/.codex (config.toml, hooks.json, sessions, skills/).
hooks.json runs ~/.codex/herdr-agent-state.sh on SessionStart.
Skills flow: external skills (e.g. Editable Visual Design ficha) install into ~/.codex/skills and are invoked as $skill in Codex tasks.

## Status

_How it is currently working; keep empty when not installed._

0.154.0 installed and authenticated (auth.json present).

## Issues log

_Dated log of problems, quirks, and fixes; keep empty when not installed._

- 2026-09-13: ~/.codex/skills is empty; no agent skills currently installed.
- 2026-09-13: multiple config.toml backups (bak-20260830-170218, bak-agent-toolkit, bak-no-mcp-20260906-204950) show recurring manual config churn.

---
# Human-readable name of the resource
name: Pi
# Official docs or repository URL
page: git@github.com:jpcosec/pi-mono.git (fork; upstream badlogic/pi-mono)
# true | false — whether the resource is installed locally
installed: true
# Local install path or install command; set when installed is true
install_path: ~/bin/pi -> ~/bin/pirate/pi-mono/packages/coding-agent/dist/cli.js (v0.67.3)
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:pi
- layer:runtime
- topic:agent-cli
---

# Pi

## Summary

_One paragraph: what this resource is and why it matters to this setup._

AI coding agent (read/bash/edit/write tools) used as executor/tester worker of the desk.

## How it's used

_How the resource is used in this setup: commands, hooks, workflows._

Agent provider of desk/runtime.yaml (agent.provider: pi); Herdr spawns executor and tester Pi agents per init_opsys.py AgentSpec(kind='pi').
~/.pi/agent/settings.json: default provider openrouter, model ~z-ai/glm-flash-latest, package npm:pi-web-access, skill paths to sldb/deskops/kgdb/spec2viz .pi/skills.
Repo pi/ holds SYSTEM.md (agent system prompt) plus settings/models/env examples.

## Status

_How it is currently working; keep empty when not installed._

v0.67.3 matches settings.json lastChangelogVersion.

## Issues log

_Dated log of problems, quirks, and fixes; keep empty when not installed._

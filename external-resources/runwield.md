---
# Human-readable name of the resource
name: RunWield
# Official docs or repository URL
page: https://github.com/gandazgul/runwield
# true | false — whether the resource is installed locally
installed: false
# Local install path or install command; set when installed is true
install_path: null
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:runwield
- layer:runtime
- topic:agent-harness
---

# RunWield

## Summary

_One paragraph: what this resource is and why it matters to this setup._

Coding harness that gates agent work by risk: sorts requests, produces reviewable plans when blast radius is real, executes through specialized roles, and refuses to mark work done until CI and a separate reviewer agree it matches the approved plan. Deno/TypeScript, with ACP + MCP integration, session records, project memory, PRDs and ADRs.

## How it's used

_How the resource is used in this setup: commands, hooks, workflows._

Not installed. Documented flow: ideate -> plan -> execute -> record -> use records to plan better; plans and lifecycle live under docs/plans/ and .wld/; distributed via Homebrew release workflow; local orchestration via compose.yml.

## Status

_How it is currently working; keep empty when not installed._



## Issues log

_Dated log of problems, quirks, and fixes; keep empty when not installed._

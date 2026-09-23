---
# Human-readable name of the resource
name: DeskOps / Opsys
# Official docs or repository URL
page: git@github.com:jpcosec/opsys.git
# true | false — whether the resource is installed locally
installed: true
# Local install path or install command; set when installed is true
install_path: /home/jp/proyectos/hum-ecosystem/tools/deskops
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:deskops
- layer:runtime
- topic:workflow
---

# DeskOps / Opsys

## Summary

_One paragraph: what this resource is and why it matters to this setup._

Workflow harness and control plane: tasks, boards, pills, atoms, rituals, primitives and closeout policy for this repo's desk/.

## How it's used

_How the resource is used in this setup: commands, hooks, workflows._

desk/ of this repo (config.json, tasks, atoms, rituals, primitives, registry) follows the DeskOps lifecycle; its models (TaskDoc, AtomDoc, PillDoc, ...) are the ones registered in this repo's .sldb store.
herdr/init_opsys.py boots the Opsys desk workspace (nvim + yazi + pytest panes, optional executor/tester agents).
Document surfaces handled by sldb; workflow state stays in desk/ artifacts and CLI, not in chat memory.

## Status

_How it is currently working; keep empty when not installed._

Active; used by every tracked doc in this repo (15 deskops models registered in .sldb).

## Issues log

_Dated log of problems, quirks, and fixes; keep empty when not installed._

---
# Human-readable name of the resource
name: Editable Visual Design
# Official docs or repository URL
page: https://github.com/yejy53/Editable-Design
# true | false — whether the resource is installed locally
installed: false
# Local install path or install command; set when installed is true
install_path: null
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- layer:agent-skills
- topic:visual-design
- system:codex
---

# Editable Visual Design

## Summary

_One paragraph: what this resource is and why it matters to this setup._

Coding-agent skill suite (editable-design, paper-fig, html-to-pptx)
that turns a brief or method description into editable visual
artifacts: posters, infographics, campaigns, and paper workflow
diagrams in HTML or PowerPoint with real text, independent layers, a
visual editor, and Agent Design Replay. Backed by an arXiv paper
(2609.04034); released 2026-09-04, Paper Fig v2 2026-09-08.

## How it's used

_How the resource is used in this setup: commands, hooks, workflows._

Not installed yet (~/.codex/skills is empty). Intended flow: install as
a Codex skill via sparse, blob-filtered clone of skills/editable-design
into ~/.codex/skills, run `npm ci --prefix` on its scripts, install the
font kit, and run doctor.sh. Then a task invokes `$editable-design` to
produce the design plus its editable source; `$paper-fig` renders
method descriptions into editable PowerPoint diagrams. Companion skill
html-to-pptx self-initializes its Python/Playwright environment on
first conversion.

## Status

_How it is currently working; keep empty when not installed._



## Issues log

_Dated log of problems, quirks, and fixes; keep empty when not installed._

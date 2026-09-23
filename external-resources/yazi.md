---
# Human-readable name of the resource
name: Yazi
# Official docs or repository URL
page: https://github.com/sxyazi/yazi
# true | false — whether the resource is installed locally
installed: true
# Local install path or install command; set when installed is true
install_path: '~/.local/bin/yazi (Yazi 26.5.6); config: repo yazi/ -> ~/.config/yazi/'
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:yazi
- layer:runtime
- topic:file-manager
---

# Yazi

## Summary

_One paragraph: what this resource is and why it matters to this setup._

Terminal file manager (Rust) acting as the filesystem navigator of the workspace.

## How it's used

_How the resource is used in this setup: commands, hooks, workflows._

Navigator pane in Herdr agent-dev layout (desk/runtime.yaml command: [yazi]).
Repo yazi/ carries init.lua and flavors; live config at ~/.config/yazi (yazi.toml, keymap.toml, theme.toml, plugins/).

## Status

_How it is currently working; keep empty when not installed._

26.5.6 (aa52643 2026-05-17) installed under ~/.local/bin.

## Issues log

_Dated log of problems, quirks, and fixes; keep empty when not installed._

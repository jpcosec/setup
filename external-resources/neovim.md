---
# Human-readable name of the resource
name: Neovim
# Official docs or repository URL
page: https://neovim.io/
# true | false — whether the resource is installed locally
installed: true
# Local install path or install command; set when installed is true
install_path: '~/.local/bin/nvim (NVIM v0.12.5); tarball at ~/.local/nvim via install/nvim.sh;
  config: repo nvim/ -> ~/.config/nvim/'
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:neovim
- layer:runtime
- topic:editor
---

# Neovim

## Summary

_One paragraph: what this resource is and why it matters to this setup._

Human editor of the setup; lazy-loaded plugin config with Tree-sitter, LSP and custom keymaps.

## How it's used

_How the resource is used in this setup: commands, hooks, workflows._

Editor pane of Herdr agent-dev layout (desk/runtime.yaml command: [nvim, .]).
Repo nvim/: init.lua + lua/config|core|plugins pinned by lazy-lock.json.
Leader <Space>; Leap for s/S jumps, Aerial symbol navigation with { }, Tree-sitter textobjects ]f [f etc.; cheatsheet nvim/KEYMAPS.md generated from keymaps.lua.
LSP servers come from Mason (own ficha nvim-mason-lsps).

## Status

_How it is currently working; keep empty when not installed._

v0.12.5 running from tarball install (not snap), as README documents.

## Issues log

_Dated log of problems, quirks, and fixes; keep empty when not installed._

- 2026-09-13: README lists gopls among Mason LSPs, but gopls is absent from ~/.local/share/nvim/mason/packages and mason/bin; README/config drift.

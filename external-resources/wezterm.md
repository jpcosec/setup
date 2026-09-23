---
# Human-readable name of the resource
name: WezTerm
# Official docs or repository URL
page: https://wezfurlong.org/wezterm/
# true | false — whether the resource is installed locally
installed: true
# Local install path or install command; set when installed is true
install_path: '/usr/bin/wezterm; config: repo wezterm/ -> ~/.config/wezterm/'
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:wezterm
- layer:runtime
- topic:terminal
---

# WezTerm

## Summary

_One paragraph: what this resource is and why it matters to this setup._

GPU-accelerated terminal multiplexer; outer session surface of this setup.

## How it's used

_How the resource is used in this setup: commands, hooks, workflows._

Terminal and outer session for Herdr desks (desk/runtime.yaml sets terminal.provider: wezterm).
Custom keybindings in repo wezterm/keybindings.lua: hide/show panes into 'Ocultos' tab, interactive pane swap, move pane to tab 1-9, base/focus-70/focus-100 layouts, splits, launcher.
New tabs auto-source .wezterm-init.sh when present.

## Status

_How it is currently working; keep empty when not installed._

System package 20240203-110809-5046fc22 (old stable channel); config active via ~/.config/wezterm/keybindings.lua.

## Issues log

_Dated log of problems, quirks, and fixes; keep empty when not installed._

- 2026-09-13: ~/.config/wezterm/keybindings.lua.bak present next to live config; manual-edit drift risk between repo copy and live symlink.

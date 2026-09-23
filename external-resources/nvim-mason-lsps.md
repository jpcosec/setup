---
# Human-readable name of the resource
name: Neovim Mason LSPs
# Official docs or repository URL
page: https://github.com/mason-org/mason.nvim
# true | false — whether the resource is installed locally
installed: true
# Local install path or install command; set when installed is true
install_path: ~/.local/share/nvim/mason/packages + mason/bin
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:neovim
- layer:runtime
- topic:lsp
---

# Neovim Mason LSPs

## Summary

_One paragraph: what this resource is and why it matters to this setup._

Language servers and linters installed inside Neovim via Mason: basedpyright, eslint-lsp, lua-language-server, marksman, ruff, rust-analyzer.

## How it's used

_How the resource is used in this setup: commands, hooks, workflows._

Managed through nvim Mason package manager; binaries exposed at ~/.local/share/nvim/mason/bin (basedpyright, basedpyright-langserver, lua-language-server, marksman, ruff, rust-analyzer, vscode-eslint-language-server).
Feed Neovim LSP completion/diagnostics for python, js/ts, lua, markdown, and rust buffers.

## Status

_How it is currently working; keep empty when not installed._

6 of the 7 LSPs listed in README installed; gopls absent.

## Issues log

_Dated log of problems, quirks, and fixes; keep empty when not installed._

- 2026-09-13: gopls listed in README 'Neovim Mason LSPs' but not installed; either install it or drop it from README.

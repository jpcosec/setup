---
# Human-readable name of the resource
name: bunwv
# Official docs or repository URL
page: https://github.com/NatiCha/bunwv
# true | false — whether the resource is installed locally
installed: true
# Local install path or install command; set when installed is true
install_path: ~/.bun/bin/bunwv (@naticha/bunwv 0.1.2 via bun install -g); bun 1.4.2
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:bunwv
- layer:cli
- topic:browser-automation
---

# bunwv

## Summary

_One paragraph: what this resource is and why it matters to this setup._

Headless browser automation CLI for Bun, powered by Bun.WebView (MIT). A persistent daemon keeps page state (DOM, modals, forms, auth, cookies) alive across commands. Agent-first contract: silent success with exit 0, JSON errors on stderr with stable exit codes, cursor-pulled event/console buffers. WebKit on macOS by default; Chrome on Linux/Windows.

## How it's used

_How the resource is used in this setup: commands, hooks, workflows._

Not installed. Install: bun install -g @naticha/bunwv (Bun >= 1.3.14) or `bunx skills add naticha/bunwv` / Claude plugin to teach the assistant. Flow: bunwv start; navigate; screenshot [--max-width]; click --selector; type; evaluate; close.

## Status

_How it is currently working; keep empty when not installed._

Instalado y verificado con smoke test: bunwv start -> navigate https://example.com -> evaluate document.title = Example Domain -> close. En Linux usa Chrome instalado en el sistema.

## Issues log

_Dated log of problems, quirks, and fixes; keep empty when not installed._

- 2026-09-13: prerequisito faltante detectado (bun 1.3.11 < 1.3.14 requerido).
- 2026-09-13: RESUELTO — bun upgrade a 1.4.2; instalado @naticha/bunwv 0.1.2; smoke test completo sin errores (start/navigate/evaluate/close). Los verbos silenciosos en exit 0 son el contrato esperado, no un fallo.

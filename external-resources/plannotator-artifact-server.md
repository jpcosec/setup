---
# Human-readable name of the resource
name: Plannotator Artifact Server
# Official docs or repository URL
page: https://docs.plannotator.ai/open-source/artifact-server
# true | false — whether the resource is installed locally
installed: false
# Local install path or install command; set when installed is true
install_path: null
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:plannotator
- layer:runtime
- topic:artifact-management
---

# Plannotator Artifact Server

## Summary

_One paragraph: what this resource is and why it matters to this setup._

Local, source-available workspace for files created or used by AI
agents. Organizes artifacts into projects, links existing files without
copying them, stores managed files, previews and edits many formats,
keeps browser comments, tracks work on a four-column Kanban board, and
exposes 11 MCP tools plus a checked OpenAPI contract. Experimental,
single-user, no accounts or cloud. Separate product from Plannotator
OSS; shares document-viewing foundations only.

## How it's used

_How the resource is used in this setup: commands, hooks, workflows._

Not in use in this setup. If adopted: requires Node.js 22+ and pnpm;
serves http://127.0.0.1:7337; stores catalog and managed files under
~/.plannotator/artifact-server/. Agents connect via MCP over Streamable
HTTP, starting at artifact_list_projects; prefer artifact_link when the
file already exists on disk and artifact_publish when the server should
own the bytes.

## Status

_How it is currently working; keep empty when not installed._



## Issues log

_Dated log of problems, quirks, and fixes; keep empty when not installed._

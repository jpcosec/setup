---
id: materialization-scion-claude-credential-binding
title: Scion claude-credential-binding
source_atoms:
- atom-scion-bootstrap-preserves-runtime-and-workflow-authority
target_kind: code
target_identity: pi/scion/sync-claude-secret.py
validation:
- pytest
- Native fresh/resumed Scion work in runs/subagents/20261111-scion-pi-runtime-repair
tags:
- system:deskops
- topic:materialization
provenance: desk/atoms/atom-scion-bootstrap-preserves-runtime-and-workflow-authority.md
---

# Scion claude-credential-binding

## Intent

Bind the current host Claude login through a native user/project file secret, without literal credential arguments or diagnostic disclosure.

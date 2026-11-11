---
id: materialization-scion-runtime-layer
title: Scion runtime-layer
source_atoms:
- atom-scion-bootstrap-preserves-runtime-and-workflow-authority
target_kind: configuration
target_identity: pi/scion/Dockerfile.runtime
validation:
- pytest
- Native fresh/resumed Scion work in runs/subagents/20261111-scion-pi-runtime-repair
tags:
- system:deskops
- topic:materialization
provenance: desk/atoms/atom-scion-bootstrap-preserves-runtime-and-workflow-authority.md
---

# Scion runtime-layer

## Intent

Deploy only the corrected launcher and native bridge while preserving pinned Pi, Scion and dependencies.

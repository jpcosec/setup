---
id: materialization-scion-autonomy-image
title: Scion autonomy image
source_atoms:
- atom-scion-bootstrap-preserves-runtime-and-workflow-authority
target_kind: configuration
target_identity: pi/scion/Dockerfile
validation:
- python -m pytest -q
- Inspect runs/subagents/20261110-autonomy-bootstrap/acceptance-v2.json
tags:
- system:deskops
- topic:materialization
provenance: desk/atoms/atom-scion-bootstrap-preserves-runtime-and-workflow-authority.md
---

# Scion autonomy image

## Intent

Install the pinned fork and Python test tools with the native event bridge, without embedding credentials.

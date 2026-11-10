---
id: materialization-scion-autonomy-pi-guide
title: Scion autonomy pi-guide
source_atoms:
- atom-scion-bootstrap-preserves-runtime-and-workflow-authority
target_kind: document
target_identity: pi/README.md
validation:
- python -m pytest -q
- Inspect runs/subagents/20261110-autonomy-bootstrap/acceptance-v2.json
tags:
- system:deskops
- topic:materialization
provenance: desk/atoms/atom-scion-bootstrap-preserves-runtime-and-workflow-authority.md
---

# Scion autonomy pi-guide

## Intent

Route Pi and Scion operators to the pinned fork and the explicit runtime bootstrap.

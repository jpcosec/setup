---
id: materialization-scion-autonomy-session
title: Scion autonomy session
source_atoms:
- atom-scion-bootstrap-preserves-runtime-and-workflow-authority
target_kind: code
target_identity: pi/scion/launch.py
validation:
- python -m pytest -q
- Inspect runs/subagents/20261110-autonomy-bootstrap/acceptance-v2.json
tags:
- system:deskops
- topic:materialization
provenance: desk/atoms/atom-scion-bootstrap-preserves-runtime-and-workflow-authority.md
---

# Scion autonomy session

## Intent

Preserve one Pi session per Scion agent and recover autonomous coordination without replaying the initial task.

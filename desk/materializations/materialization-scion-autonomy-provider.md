---
id: materialization-scion-autonomy-provider
title: Scion autonomy provider
source_atoms:
- atom-scion-bootstrap-preserves-runtime-and-workflow-authority
target_kind: code
target_identity: pi/scion/provision.py
validation:
- python -m pytest -q
- Inspect runs/subagents/20261110-autonomy-bootstrap/acceptance-v2.json
tags:
- system:deskops
- topic:materialization
provenance: desk/atoms/atom-scion-bootstrap-preserves-runtime-and-workflow-authority.md
---

# Scion autonomy provider

## Intent

Provision the pinned fork provider with environment key references while preserving existing settings.

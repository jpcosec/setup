---
id: materialization-scion-autonomy-harness
title: Scion autonomy harness
source_atoms:
- atom-scion-bootstrap-preserves-runtime-and-workflow-authority
target_kind: configuration
target_identity: pi/scion/harness-config.yaml
validation:
- python -m pytest -q
- Inspect runs/subagents/20261110-autonomy-bootstrap/acceptance-v2.json
tags:
- system:deskops
- topic:materialization
provenance: desk/atoms/atom-scion-bootstrap-preserves-runtime-and-workflow-authority.md
---

# Scion autonomy harness

## Intent

Declare truthful native event support, pinned fork runtime and explicit model/auth bindings.

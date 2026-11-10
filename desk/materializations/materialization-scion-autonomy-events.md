---
id: materialization-scion-autonomy-events
title: Scion autonomy events
source_atoms:
- atom-scion-bootstrap-preserves-runtime-and-workflow-authority
target_kind: code
target_identity: pi/scion/scion-events.ts
validation:
- python -m pytest -q
- Inspect runs/subagents/20261110-autonomy-bootstrap/acceptance-v2.json
tags:
- system:deskops
- topic:materialization
provenance: desk/atoms/atom-scion-bootstrap-preserves-runtime-and-workflow-authority.md
---

# Scion autonomy events

## Intent

Forward only normalized native events and bounded tool identifiers, with timeout and no false completion.

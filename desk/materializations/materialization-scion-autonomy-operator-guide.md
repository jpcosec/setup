---
id: materialization-scion-autonomy-operator-guide
title: Scion autonomy operator-guide
source_atoms:
- atom-scion-bootstrap-preserves-runtime-and-workflow-authority
target_kind: document
target_identity: pi/scion/README.md
validation:
- python -m pytest -q
- Inspect runs/subagents/20261110-autonomy-bootstrap/acceptance-v2.json
tags:
- system:deskops
- topic:materialization
provenance: desk/atoms/atom-scion-bootstrap-preserves-runtime-and-workflow-authority.md
---

# Scion autonomy operator-guide

## Intent

Explain native broker configuration, source/data authority, bootstrap ownership and actual validation evidence.

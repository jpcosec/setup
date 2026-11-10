---
id: materialization-scion-autonomy-bootstrap
title: Scion autonomy bootstrap
source_atoms:
- atom-scion-bootstrap-preserves-runtime-and-workflow-authority
target_kind: code
target_identity: pi/scion/start-desk.py
validation:
- python -m pytest -q
- Inspect runs/subagents/20261110-autonomy-bootstrap/acceptance-v2.json
tags:
- system:deskops
- topic:materialization
provenance: desk/atoms/atom-scion-bootstrap-preserves-runtime-and-workflow-authority.md
---

# Scion autonomy bootstrap

## Intent

Bind explicit current sources and owned task worktree, reconcile before launch and resolve project templates from their actual config root.

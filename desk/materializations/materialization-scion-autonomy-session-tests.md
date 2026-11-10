---
id: materialization-scion-autonomy-session-tests
title: Scion autonomy session-tests
source_atoms:
- atom-scion-bootstrap-preserves-runtime-and-workflow-authority
target_kind: test
target_identity: tests/test_scion_pi_runtime.py
validation:
- python -m pytest -q
- Inspect runs/subagents/20261110-autonomy-bootstrap/acceptance-v2.json
tags:
- system:deskops
- topic:materialization
provenance: desk/atoms/atom-scion-bootstrap-preserves-runtime-and-workflow-authority.md
---

# Scion autonomy session-tests

## Intent

Prove fixed-session continuity, no initial prompt replay and credential-safe launcher behavior.

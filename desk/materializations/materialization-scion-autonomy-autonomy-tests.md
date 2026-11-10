---
id: materialization-scion-autonomy-autonomy-tests
title: Scion autonomy autonomy-tests
source_atoms:
- atom-scion-bootstrap-preserves-runtime-and-workflow-authority
target_kind: test
target_identity: tests/test_scion_autonomy.py
validation:
- python -m pytest -q
- Inspect runs/subagents/20261110-autonomy-bootstrap/acceptance-v2.json
tags:
- system:deskops
- topic:materialization
provenance: desk/atoms/atom-scion-bootstrap-preserves-runtime-and-workflow-authority.md
---

# Scion autonomy autonomy-tests

## Intent

Prove redacted event payloads and refusal/recovery/source-identity/native-template-resolution contracts using isolated fixtures.

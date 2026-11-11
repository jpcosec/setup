---
id: task-scion-pi-resume-and-runtime-binding
status: deferred
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ''
history: []
references:
- tests/test_scion_pi_runtime.py
- pi/scion/launch.py
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Scion Pi resume and runtime binding

## Rationale

_Explain why this task exists or the business driver behind it._

Not provided.

## Goal

_Describe the concrete result this task must produce._

Fix fresh/resumed Pi work with pinned DeepSeek model and normal local image resolution; make installed Claude credentials reusable through native Scion auth.

## Scope

_State what is in scope and what is out of scope._

setup/pi/scion recipes, focused regressions, native laboratory reproduction and installed harness configuration. Preserve Pi fork and Scion versions, credentials, unrelated source changes and production tasks.

## Implementation Path

_Outline the expected implementation route or affected surface._

Diagnose native resumed argv/provider resolution; fix the source launcher/provision/config and explicit local image binding, test fresh and resumed file edits with unchanged tests, install verified runtime configuration. Use existing native secret APIs for private Claude auth; never commit credential values.

## Validation

_List the checks required before this task can close._

- pytest
- Real Scion fresh/resumed work with original tests

## Done When

_Name the observable condition that makes the task complete._

Fresh and resumed Pi sessions use the configured DeepSeek model, edit code and pass tests; normal harness launch needs no temporary image override. Claude uses current existing auth with no manual login. Evidence and source committed.

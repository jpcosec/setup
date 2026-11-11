---
id: task-scion-pi-resume-and-runtime-binding
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-scion-pi-resume-and-runtime-binding.md
---

# Scion Pi resume and runtime binding

## Rationale

_Explain why this task exists or the business driver behind it._

Not provided.

## Goal

_Describe the concrete result this task must produce._

Fix fresh and resumed Pi work with the configured DeepSeek model and normal local image binding; reuse current Claude auth through native Scion secrets.

## Scope

_State what is in scope and what is out of scope._

setup/pi/scion recipes, focused tests and installed harness configuration; pinned Pi fork and Scion versions unchanged; no production task dispatch.

## Implementation Path

_Outline the expected implementation route or affected surface._

Reproduce native resume argv/model resolution, fix source and install tested launcher/image config; test new work after restart in same session. Bind current host Claude credentials with private native Scion file secret. Preserve failure evidence and all unrelated changes.

## Validation

_List the checks required before this task can close._

- pytest
- Native Scion fresh/resume with independent assertions

## Done When

_Name the observable condition that makes the task complete._

Fresh and resumed Pi edit code and pass original tests without image overrides or provider fallback; Claude passes using existing native auth; focused pytest passes and source/evidence committed.

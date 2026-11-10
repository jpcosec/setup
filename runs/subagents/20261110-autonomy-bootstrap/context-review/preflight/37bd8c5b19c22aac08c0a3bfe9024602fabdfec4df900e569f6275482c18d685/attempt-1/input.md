FILE:desk/tasks/task-scion-autonomy-runtime-bootstrap-and-pi-lifecycle-bridge.md
---
id: task-scion-autonomy-runtime-bootstrap-and-pi-lifecycle-bridge
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- 18c0007
- tests/test_scion_autonomy.py
- tests/test_scion_pi_runtime.py
depends_on: []
pills: []
files:
- pi/scion/Dockerfile
- pi/scion/harness-config.yaml
- pi/scion/launch.py
- pi/scion/provision.py
- pi/scion/scion-events.ts
- pi/scion/start-desk.py
- pi/scion/README.md
- pi/README.md
- tests/test_scion_pi_runtime.py
- tests/test_scion_autonomy.py
- desk/atoms/atom-scion-bootstrap-preserves-runtime-and-workflow-authority.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-scion-autonomy-runtime-bootstrap.md
---

# Scion autonomy runtime bootstrap and Pi lifecycle bridge

## Rationale

_Explain why this task exists or the business driver behind it._

Not provided.

## Goal

_Describe the concrete result this task must produce._

A reproducible Scion start uses intended current desk/tools, valid worktree paths and a native Pi event bridge so a disposable authorized desk can run without manual prompts through child execution, independent test and closeout/continuation.

## Scope

_State what is in scope and what is out of scope._

setup/pi/scion runtime recipes, lifecycle extension/config, source/root binding and tests/docs/atom. Preserve Scion0.2.21 and pinned Pi fork, secrets, session continuity and unrelated agents; no pi-subagents or new workflow engine. Do not dispatch production tasks in validation.

## Implementation Path

_Outline the expected implementation route or affected surface._

Read drawer contract and audits; fresh preflight/cold review. Bridge pinned Pi native events to existing sciontool hooks; correct current-source/bootstrap path config; explicit child project/auth/workspace and token refresh. Integrate corrected DeskOps role/template contract from fix/scion-autonomy. Validate one initial coordinator prompt with no subsequent messages on disposable desk plus controlled child failure, restart and no duplicate dispatch.

## Validation

_List the checks required before this task can close._

- pytest tests/test_scion_pi_runtime.py and bridge/bootstrap tests
- fresh real Scion coordinator/executor/tester on disposable desk completes closeout and next task without messages
- restart preserves session and no duplicate child

## Done When

_Name the observable condition that makes the task complete._

Runtime state reflects actual work; clean startup uses correct source and Git paths; unattended disposable-desk loop passes; source docs and exact evidence committed. No claim of success from a running container alone.

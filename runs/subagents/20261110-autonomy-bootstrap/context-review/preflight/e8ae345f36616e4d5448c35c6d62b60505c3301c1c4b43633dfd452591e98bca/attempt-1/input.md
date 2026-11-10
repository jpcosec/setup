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

The first coordinator required manual checkout, CLI and state interventions and looped on false review status; native Pi events are not yet connected to Scion.

## Goal

_Describe the concrete result this task must produce._

A reproducible Scion start uses intended current desk/tools, valid worktree paths and a native Pi event bridge so a disposable authorized desk can run without manual prompts through child execution, independent test and closeout/continuation.

## Scope

_State what is in scope and what is out of scope._

setup/pi/scion runtime recipes, lifecycle extension/config, source/root binding and tests/docs/atom. Preserve Scion0.2.21 and pinned Pi fork, secrets, session continuity and unrelated agents; no pi-subagents or new workflow engine. Do not dispatch production tasks in validation.

## Implementation Path

_Outline the expected implementation route or affected surface._

Runtime constants: Scion0.2.21; Pi jpcosec/pi-mono e9ba9e2ebce1b49dca85ab20007038c06e486ea5; project sldb-1 UUID b0899ed7-7dec-44c2-a9b9-d0ac92c61cc7; host workspace /mnt/ssd/proyectos/SLDB_1. start-desk.py accepts explicit desk/source/ref/project/workspace/agent options, validates paths and provenance, chooses a clean dedicated worktree of configured canonical ref (origin/main default) without resetting dirty originals and reuses it only when ownership is known. Mount workspace both at /workspace and its real host absolute path via supported Scion volumes, not manual symlinks. Explicit source roots via PYTHONPATH bind tested DeskOps source and /mnt/ssd/proyectos/SLDB_1/sldb/src; verify actual imports before start, never silently use baked stale wheels. User CLI authenticates bootstrap through configured Hub, children use their Scion agent tokens and DeepSeek project secret, never secrets.env mounted. Pi extension maps input/session/agent/tool events to existing sciontool hook Claude dialect events; emit no prompt/tool argument or credential content; generic agent_end is not completed. Reuse sciontool metadata proactive token refresh, verify a real own-agent refresh and preserve tokens without logging; no new refresher service. Stable coordinator/child labels and run identity reconcile before start. Independent tester mode/source contract comes from the DeskOps task branch and is an integration prerequisite. Disposable real Git desk under workspace .tmp, two bounded code tasks with explicit expected functions/tests and dependency, one initial assignment and zero followup messages. Automated fixture may inject one controlled validation/child failure and stop/resume; evidence must show correct refusal to close on failure, recovery, no duplicate child, independent tester, one closeout per task and phase completion. Do not dispatch production tasks. Register source atom before docs and save all sanitized integration evidence. Concrete configured defaults: operator supplies --root (integration fixture /mnt/ssd/proyectos/SLDB_1/.tmp/scion-autonomy-lab); --source-root defaults /mnt/ssd/proyectos/SLDB_1/deskops-wt-scion-autonomy branch fix/scion-autonomy, with tested final commit recorded after source closeout; --sldb-root /mnt/ssd/proyectos/SLDB_1/sldb/src. Ref configured solely by --ref (origin/main default; HEAD explicit in fixture), validate via git rev-parse --verify ref^{commit}; fail before mutation if missing, never silent fallback or origin rewriting. Hub default http://127.0.0.1:8080; bootstrap uses existing CLI auth, children own agent tokens. --context-file JSON interface is produced by source task on fix/scion-autonomy; its final commit is a future dependency output, not a missing operator decision. Fixture has two tasks adding greet/farewell with real pytest assertions and explicit dependency. A validation command has one deterministic transient failure; successful retry must still verify actual function outputs. Automated stop/resume injection uses zero parent followup messages; assert one project/task/role child identity and separate executor/tester identities.

## Validation

_List the checks required before this task can close._

- pytest tests/test_scion_pi_runtime.py and bridge/bootstrap tests
- fresh real Scion coordinator/executor/tester on disposable desk completes closeout and next task without messages
- restart preserves session and no duplicate child

## Done When

_Name the observable condition that makes the task complete._

Runtime state reflects actual work; clean startup uses correct source and Git paths; unattended disposable-desk loop passes; source docs and exact evidence committed. No claim of success from a running container alone.

# Executor handoff

Implemented the declared runtime files and dummy-only tests. No real Scion agent was launched, stopped or messaged; no credentials were read; no packages installed; no commits or closeout performed. nvim/lazy-lock.json and preexisting untracked lifecycle files were left untouched.

## Implementation

- Image installs launcher plus explicit native Pi extension. Vendored harness provisioner is now tracked with Pi0.67.3. Existing auth/provider behavior and metadata-server token refresh remain.
- Native callbacks call `sciontool hook --dialect=claude` with JSON stdin, no raw child output, five-second timeout. Payload allowlist contains event name and bounded tool name/id only. agent_end is Stop/working, never completion. Existing Scion handlers govern sticky/new-work semantics.
- Launcher keeps fixed session, suppresses original assignment on resume, loads bridge explicitly unless --no-extensions/-ne, and adds one recovery instruction only for DESKOPS_AUTONOMOUS=1.
- start-desk.py requires explicit desk/workspace/project/agent/template paths, verifies canonical ref and actual source imports before mutation, records source/desk revisions, creates known-owned clean detached desk worktree, and uses source template --context-file for executor/tester/coordinator. Strict five-field context passes source and SLDB src roots. Generator owns mounted absolute workspace and context environment.
- Coordinator uses caller-owned --config env override for autonomous recovery, preserving generated templates. Bootstrap lists/reconciles before any worktree/template mutation. Recovery requires exact project/name/labels/context/source provenance and known worktree ownership. It permits own descendant commits plus dirty paused evidence, preserving bytes and refusing any new worktree or duplicate identity. Newly moved canonical refs never reset/rebase existing ownership.
- Source atom created and refined through deskops add/edit atom CLI before corresponding docs.

## Validation

Full setup suite: `/mnt/ssd/proyectos/SLDB_1/.venv/bin/python -m pytest -q` -> 33 passed in 5.53s (validation.log; stderr.log empty). Real Node22 executes all registered native callbacks with dummy sciontool and tests redaction, failures and timeout. Git tests use disposable repositories for original dirt, ownership rejection, own closeout commit and dirty paused recovery. Scion command dispatch is dummy-only. `python3 pi/scion/start-desk.py --help` passed (stdout.log). `git diff --check` passed.

## Parent integration required

Image build context adds tracked `scion-events.ts` beside `Dockerfile` and `launch.py`; existing pi-mono/uv/wheels inputs unchanged. Harness bundle keeps vendored scion_harness.py/capture_auth.py and replaces config.yaml/provision.py with tracked files. Use a candidate image/harness tag for validation; parent owns build/install/secrets/API and real agents.

After the source task provides tested --context-file/tester generator commit, create authorized disposable Git desk with committed roles/rituals/two dependent code tasks. Run bootstrap with explicit --root, --workspace-root, --source-root, --sldb-root (src itself), --ref HEAD, --project, --agent, --templates-dir and optional --hub. Use a Python environment with DeskOps dependencies (the shared .venv). Default source/ref values are documented; invalid values never fall back. Bootstrap uses current CLI Hub auth; secret synchronization remains a separate existing helper.

Real validation still must show own-agent proactive token refresh, native state transitions/clearing and sticky completion, executor/tester distinct identities, failure refusal then successful retry, unattended closeout/continuation, phase completion, stop/resume preserving fixed session and no duplicate child. None of these real integration outcomes is claimed by these unit tests.


## Independent audit corrections

37 tests now pass in 5.56s (updated validation.log). NEW starts resolve the explicit canonical ref after Scion reconciliation, before filesystem mutations. Known-owned existing/resume does not resolve that ref: recorded base/ancestry and exact ownership remain authoritative even when origin/main vanished. Recovery regression exercises an own closeout commit plus dirty paused evidence with a now-missing ref.

Source provenance now includes content fingerprints of deskops/ and sldb_root/sldb: relative names, executable bits and file bytes, including package data/untracked source, excluding generated cache directories and pyc/pyo. Recovery compares content instead of HEAD so doc-only commits do not fail; runtime edits are refused without changing bytes. Fingerprint is rechecked before the initial coordinator start. Native flock on the original directory inode serializes bootstrap without creating a lock file; reconciliation is read inside that lock. No scheduler or registry added.

Only bootstrap/tests/atom/docs/evidence changed in this follow-up. Frozen image/provisioner/launcher/bridge/harness files remain unchanged; parent's candidate build inputs are still current. Existing pre-audit bootstrap provenance lacks source_content and must not be silently upgraded; use a fresh disposable lab run for validation.

## Role source integration correction

Template materialization now passes `--root source_root`, resolving RoleDocs/runtime profiles from the tested implementation checkout. `--task-repo original_task_root.name` and JSON context.desk_root still identify the separate task-data worktree. Regression explicitly leaves data desk RoleDocs absent and asserts all three materialization commands use source_root. Full setup suite rerun: 37 passed in 5.76s; diff whitespace check passed. No frozen image/bridge files changed.


## Final parent validation

Real Scion acceptance passed (acceptance-v2.json), with complete Git history autonomy-lab-v2.bundle and independent-final-validation.log. Two task closeouts and two phase commits; no parent task messages; coordinator stop/resume; first real tester failed exit23 and new tester passed; original tests/validator unchanged; six distinct Pi sessions and no duplicate role identity. Native local-template resolution failures were corrected for sync, start and resume by using project config CWD. Stable default source is deskops-runtime; its coordinator must advance it to integrated tested main before production use or retiring the feature worktree. Final targeted38 tests passed5.63seconds. Execution-to-testing and testing-to-closeout handoffs passed the declared bootstrap, bridge, isolation and recovery obligations. No bound pills. Production tasks were not dispatched by validation.

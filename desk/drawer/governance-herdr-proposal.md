# Governance Proposal: Agent-Driven Development on herdr

Status: proposal — drawer, not promoted.
Scope: the dev loop that runs pi/codex/claude/opencode/gemini workers inside herdr panes, governed by deskops task lifecycle and backed by sldb state.
Layer map used throughout: **sldb = data/document/state layer · deskops = workflow harness (tasks, boards, pills, atoms, rituals, drawer, registry, drift, closeout) · herdr = runtime/control plane** (panes, agents, dispatch mechanics, no semantics).

## 1. Roles: who is interactive, who executes

| Role | Agent | Interactive? | Owns |
|---|---|---|---|
| Supervisor | main pi session (coordinator) | **yes — stays interactive** | task design, zero-context bundle, preflight gate, dispatch, evidence verification, closeout |
| Executor | spawned pi worker (default: DeepSeek Flash via OpenRouter) | no — executes in its own herdr pane | implementation inside task Scope |
| Tester | spawned pi worker, separate pane (same cheap model) | no — executes in its own herdr pane | contract validation, `validation.log` + `result-summary.md` |

Rules:
- The Supervisor never implements nor tests inline. It defines, dispatches, verifies, iterates, closes out.
- Executor and Tester must be **separate** workers (never the same pane, never the main session) so the Tester is impartial about Executor output.
- A worker is dispatchable only when herdr reports `idle`. `blocked` means waiting for input — read its pane, answer, then continue.
- Anti-mock is global: an Executor that cannot reach a real dependency must stop and report the block, never fake a green closeout.

## 2. Zero-context task bundles and the cheap preflight gate

Every task is executable from three artifacts alone — no chat memory, no Q&A:

- **TaskDoc** (`desk/tasks/task-<id>.md`): goal, scope, files to modify, done-criteria, and explicit links to pills and atoms.
- **Pills** (linked): reusable operational guardrails that apply to this task.
- **Atoms** (linked): durable architecture/knowledge truths this task depends on.

Preparation sequence:
1. Write the TaskDoc in `desk/drawer/tasks/`; run an ambiguity review (would a fresh agent have to guess any path, variable, command, or contract? yes → incomplete).
2. Commit the creation in drawer, then `deskops promote drawer-task-to-active-task task-<id>`.
3. **Preflight comprehension gate (mandatory, cheap):** before spending a real Executor, dispatch a **cheap model** to read the bundle and restate exactly what it understood, step by step. Any misreading or ambiguity means the TaskDoc is deficient — fix the task, re-run the gate. Only a faithful restatement authorizes Executor dispatch.

## 3. Subagent dispatch through herdr

Mechanics (via `/home/jp/setup/herdr/coordination.sh`):

- **spawn** — start a worker in a separate `subagents` tab, never in the coordinator's pane: `spawn pi <cwd> --provider openrouter --model '~deepseek/deepseek-v4-flash-latest'`. One worker per task; auto-numbered names (`pi`, `pi2`, …) avoid collisions.
- **dispatch** — `dispatch <target> "<task>"` blocks until the worker returns to `idle` (default timeout 10 min) and appends PROMPT + output tail to the transcript. **One task per dispatch.** The prompt must carry the full bundle context — workers do not see coordinator conversation.
- **read** — `read <target>` pulls the pane tail when the dispatch output is insufficient; iterate with a follow-up dispatch to the same pane.
- **wait** — `wait <target> idle` when you need to block manually instead of dispatching.
- **Verify with test output:** after any code change, the Executor's dispatch must require running the local tests and reporting results. "Done" without output is never trusted. The Tester re-verifies independently.
- Never dispatch to a `working` or `blocked` worker; unblock or wait first.
- Workers that write code run in their own worktree (`herdr worktree create`) to avoid edit collisions.
- Model policy: workers are cheap labour — default DeepSeek Flash (OpenRouter); never Opus on a subagent. Free models test plumbing only.

## 4. Trace and audit: herdr is not the audit surface

Verified fact (Herdr 0.9.0): herdr keeps **no agent trace** — lifecycle states (`idle`/`working`/`blocked`/`done`) are live state with no history; read-only calls are not logged; TUI agents run on the alternate screen so their rows never enter host scrollback; restart loses pane memory; the server log grows unbounded (`~/.config/herdr/herdr-server.log`) with no rotation.

Consequence — the durable audit surface is:

1. **pi transcripts** — pi writes complete JSONL transcripts and accepts `--session <path>`; these are the primary trace.
2. **`runs/subagents/<run-dir>/` artifacts** — the Tester's `validation.log` and `result-summary.md`, pinned by the supervisor per task.
3. **deskops closeout commits** — the atomic, immutable record that task N was verified and closed (see §6).

Never scrape herdr scrollback as evidence; it cannot be made complete. If audit continuity is required, the supervisor pins the pi session path into `runs/subagents/` per dispatch — which is the deskops-side feature already tracking this.

## 5. Drift detection and repair

- Installed agents (`~/.pi/agent/agents/`, `.opencode/`, etc.) are **materializations** of RoleDoc/Atom sources. An installed file that differs from its source is drift, not a fix.
- Detection: `deskops status` → `deskops doctor` → `deskops graph build` → `deskops graph missing` → `deskops drift check`.
- Repair: edit the **source** (RoleDoc/Atom), then `deskops materialize`. **Never hand-edit an installed agent file**; never hand-edit `desk/` to repair a broken state when a deskops command exists.
- Same rule applies to the layout contract: the runtime layout must come from one source (see §8, gap 2) or it will drift the way `ROLE_AGENT_SPECS` drifted.

## 6. Atomic closeout — never a bare git commit

- One coherent deliverable per task; every task ends with exactly one atomic commit.
- The supervisor verifies Tester evidence, then closes with the ritual command:
  `deskops closeout commit --task task-<id> --run-dir runs/subagents/<run-dir>`
- A bare `git commit` for task work is prohibited: it bypasses evidence pinning and the closeout ritual.
- When a whole ready dependency layer closes, run the phase ritual (`desk/rituals/phase.md`) before the next layer starts.
- Mutation experiments go in a disposable sandbox desk (`.tmp/deskops-cli-test`), not the tracked desk.

## 7. Layer mapping onto the development loop

| Loop stage | sldb (data/doc/state) | deskops (workflow harness) | herdr (runtime/control plane) |
|---|---|---|---|
| Intake / routing | note or drawer task stored as tracked doc | drawer triage; `deskops add/promote`; registry | — (herdr not involved yet) |
| Design | TaskDoc/Pills/Atoms as sldb artifacts | ambiguity review; bundle assembly; commit + promote | — |
| Preflight gate | cheap model reads bundle | supervisor runs gate; fixes task on misread | `spawn` cheap worker, `dispatch`, `wait idle` |
| Execution | Executor edits files in Scope; sldb mirrors document state | Scope enforcement; anti-mock; test requirement | `spawn` Executor, `dispatch` bundle, `read` tail |
| Testing | test outputs + `runs/subagents/` artifacts | Tester role; evidence verification | `spawn` Tester pane, `dispatch`, verify `validation.log` |
| Closeout | pi transcript + evidence pinned | `deskops closeout commit` — atomic commit | transcript via `--session <path>`; pane torn down |
| Repair / audit | sources in sldb; installed agents are derivations | `deskops drift check` / `materialize`; doctor | re-spawn from materialized spec if needed |

Flow-level invariants:
- herdr decides **how** work runs (panes, processes, dispatch); it decides **nothing** about what is correct work.
- deskops decides **what** work is (tasks, gates, closeout), reading/writing sldb documents.
- sldb is the single source of truth; docs, agents, and commits are materializations of it.
- Every durable claim about the dev loop traces to a sldb doc + a deskops closeout commit + a pi transcript — never to pane scrollback.

## 8. Concrete next actions for known gaps (setup repo)

1. **`desk/runtime.yaml` is read by nobody → make it real or delete it.** Decision needed: layout source lives here (per-workstation) or in deskops desk (per-project). Preferred: initializer reads it so the declarative contract is the single source; align with the deskops feature `feature-herdr-supervised-execution-runtime.md`.
2. **`herdr/init_opsys.py` duplicates `deskops/runtime/initializer.py`** (same panes, same `AgentSpec("executor"/"tester", kind="pi")`, same workspace-reuse check — two copies that will drift). Action: once `deskops runtime init` is stable, make `init_opsys.py` a thin wrapper over it or delete it; update `install/init-herdr.sh` accordingly.
3. **No log rotation and no agent trace in herdr.** Action (setup side is narrow): rotate/prune `~/.config/herdr/herdr-server.log` (611KB/3 days, ~42% `tab.focus` noise). Trace itself is handled by §4 — pi JSONL `--session` pinned into `runs/subagents/`; verify whether `agent prompt` is logged so dispatch events can be correlated from the server side.
4. **Blocked intake.** `deskops inbox` fails: `Repository id 'setup' not found in registry`. Action: `deskops repo register setup --path /home/jp/setup`; then route new notes through coordination intake instead of the drawer.
5. Enable governance end-to-end for one real task (promote a drawer task, run preflight → Executor → Tester → closeout through herdr) before scaling the loop.

## Anti-patterns this proposal forbids

- Supervisor implementing or testing inline.
- Dispatching without the preflight comprehension gate.
- Zero-context violations (vague bundle, hoping the worker guesses).
- One dispatch carrying several tasks; dispatching to `working`/`blocked` workers.
- Trusting "done" without test output.
- Treating herdr scrollback as audit evidence.
- Hand-editing installed agents or `desk/` files to repair state.
- Bare `git commit` instead of `deskops closeout commit`.
- Mocks/stubs/fake data/TODO shortcuts as Executor deliverables.
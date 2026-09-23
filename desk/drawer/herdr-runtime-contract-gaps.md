# Herdr runtime contract gaps (setup side)

Status: deferred

The deskops-side work — RoleDoc-driven agent launch, per-kind runtime profiles, pinned session traces, `deskops runtime supervise` — is tracked in the deskops desk:

- `tools/deskops/desk/drawer/features/feature-herdr-supervised-execution-runtime.md`
- `tools/deskops/desk/drawer/questions/question-herdr-runtime-open-decisions.md`

What follows is what belongs to **this** repo, which owns the declarative runtime contract and the workstation-level Herdr dependency.

## 1. `desk/runtime.yaml` is read by nobody

The file declares a full runtime contract: providers for terminal/editor/navigator/agent, worktree root, and an `agent-dev` layout with a `work` tab splitting into nvim, an executor agent, a tester agent, yazi and pytest.

Grepped the whole deskops package for `runtime.yaml` / `runtime_yaml`: **zero references**. The layout that actually gets built is hardcoded in `deskops/runtime/initializer.py:33-42`.

So the declarative contract in this repo is decorative. Two coherent outcomes:

- The initializer reads it, and this file becomes the single source for desk layout. This is what `herdr/README.md` already implies: "Setup stores only the declarative contract and integration defaults."
- Or it is dead config and should be deleted rather than left to look authoritative.

The first is preferable and lines up with the deskops feature, which already makes agents document-driven. Whoever does that work needs to decide whether the layout lives here (per-workstation) or in the deskops desk (per-project), because right now it is implied to be both.

## 2. `herdr/init_opsys.py` duplicates the deskops initializer

`herdr/init_opsys.py` builds the same pane list as `deskops/runtime/initializer.py:33-42` — the same nvim/yazi/pytest panes, the same `AgentSpec("executor", kind="pi")` and `AgentSpec("tester", kind="pi")` literals, the same workspace-reuse-by-label check.

Two copies of one layout in two repos will drift the same way `ROLE_AGENT_SPECS` drifted from the role documents. Once deskops exposes `deskops runtime init` (it already does, via `deskops/cli/commands/runtime.py`), this script should become a thin wrapper over that CLI or be deleted. `install/init-herdr.sh` already shells out to it, so whichever way it goes, that wrapper needs updating too.

## 3. Herdr keeps no agent trace, and its log grows unbounded

Verified on this machine, against Herdr 0.9.0:

- `~/.config/herdr/herdr-server.log` contains **zero** `event="agent.*"` entries. Lifecycle states (`idle`/`working`/`blocked`/`done`) leave no history — they are live state only.
- Read-only calls are not logged at all. Running `herdr agent list` and `herdr pane list` produced zero new lines; only mutating calls are recorded (`changes_ui=true`, with zero `false` entries). Logged methods so far: `pane.split`, `agent.start`, `workspace.create`, `workspace.close`.
- No transcript persistence. Pane scrollback is `pane_scrollback_limit_bytes=10000000` held in memory; `session.json` stores layout only. A server restart loses it.
- Worse, TUI agents (claude, pi, codex) run on the alternate screen, and per Herdr's own documentation those rows never enter host scrollback. `agent read` returns the visible window, not history — raising `--lines` does not recover it.
- No rotation: 611KB in three days, of which ~42% (1710 of ~4050 lines) are `tab.focus` events.

Consequence for the runtime contract: Herdr cannot be the audit surface, and no amount of scraping makes it one. The trace has to come from the agent runtime itself (pi writes complete JSONL transcripts and accepts `--session <path>`), which is what the deskops feature pins into `runs/subagents/`.

The setup-side item is narrower: decide whether to rotate or prune the server log, since nothing does today.

One thing not verified — whether `agent prompt` gets logged. No `agent.prompt` appears in the history, but that may simply mean it has never been used here. Confirming it requires sending a prompt to a live agent.

## 4. Blocked intake

`deskops inbox` does not work from this repo: `Repository id 'setup' not found in registry at '/home/jp/setup/desk/registry'`. The remedy the error suggests is `deskops repo register setup --path /home/jp/setup`. Until then, notes like this one have to live in the drawer rather than go through coordination intake.

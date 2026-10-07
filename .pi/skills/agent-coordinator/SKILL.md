---
name: agent-coordinator
description: Coordinate other agent sessions as workers through herdr. Use when the task requires dispatching work to other agents (pi, codex, claude, opencode, gemini) running in herdr panes, collecting their output, and orchestrating multi-agent turn-taking. The coordinator stays interactive; workers execute.
---

# Agent Coordinator (via herdr)

You are the coordinator. Other agents run inside herdr panes as workers. You
never do work you can delegate; you define tasks, dispatch, verify, iterate.

## Discover workers

```bash
bash /home/jp/setup/herdr/coordination.sh agents
```

Returns `name status pane cwd`. Use the **pane id** (e.g. `w6:p6`) as TARGET
when several workers share a kind. A worker is only dispatchable when its
status is `idle`. `blocked` means it is waiting for input: read its pane and
answer.

## Dispatch a task (send + wait for completion + capture output)

```bash
bash /home/jp/setup/herdr/coordination.sh dispatch w6:p6 "Run the test suite in $(pwd) and report failures only"
```

- Blocks until the worker is `idle` again (timeout: $HERDR_TIMEOUT_MS, default 10 min).
- Appends PROMPT + OUTPUT tail to `$HERDR_TRANSCRIPT` (default `./.herdr-coordination.md`).
- The printed output is the pane tail; use `read` for more context.

Rules:
- One task per dispatch. State the working directory, the goal, and what to report back.
- Workers do not see this conversation. Include all needed context in the prompt.
- Never dispatch to a `working` or `blocked` worker; wait or unblock first.
- Verify: after a code change dispatch, require the worker to run tests and
  report results; do not trust "done" without output.
- Iterate: if output is insufficient, dispatch a follow-up to the same TARGET.
- Terminate: when the goal is met, summarize the transcript; do not leave
  workers mid-task. Stop after dispatching; your turn resumes when idle.

## Fire-and-forget / inspection

```bash
bash /home/jp/setup/herdr/coordination.sh say w6:p6 "message"   # no wait
bash /home/jp/setup/herdr/coordination.sh wait w6:p6 idle       # block manually
bash /home/jp/setup/herdr/coordination.sh read w6:p6            # pane output tail
```

## Start a new worker

```bash
bash /home/jp/setup/herdr/coordination.sh spawn pi /path/to/repo
```

Starts the agent kind in that cwd, **in a separate `subagents` tab** — never in the
coordinator's pane, so worker output does not flood your screen. The tab is created
on the first spawn, reused (split) afterwards, and never steals focus. Kinds:
pi, claude, codex, opencode, gemini, cursor, amp, kilo, ... (`herdr agent start --help`).
Extra args after `[cwd]` are passed to the agent executable.

Agent names are auto-numbered (`pi`, `pi2`, `pi3`, ...) so spawning several workers
of the same kind does not collide.

### Which model a worker should run

Workers are cheap labour: they execute a scoped task, not architecture. Default to
**`pi` + DeepSeek Flash via the direct `deepseek` provider**, and never burn Opus on a subagent.

Prices below are per 1M tokens, read from the live OpenRouter and DeepSeek model
APIs (not guessed). All listed models were verified to actually execute tools.

| Use | Command tail |
|---|---|
| **Default worker** | `spawn pi <cwd> --provider deepseek --model deepseek-flash` (direct DeepSeek API; the owner's choice) |
| OpenRouter alternative | `spawn pi <cwd> --provider openrouter --model '~deepseek/deepseek-v4-flash-latest'` |
| **Second choice** | `spawn pi <cwd> --provider openrouter --model '~z-ai/glm-flash-latest'` |
| **Testing the harness** | `spawn pi <cwd> --provider openrouter --model nvidia/nemotron-3.5-lightning:free` |

Quote the `~` ids — bash globs them otherwise.

Caveat: OpenRouter entries in `~/.pi/agent/models.json` carry no metadata, so pi
shows the default **128k** window in its status line even though the model serves
1.31M. Fine for scoped worker tasks; if a worker must hold a huge context, use the
direct `deepseek` provider (declared as 1M locally) or add `contextWindow` to the
entry in `models.json`.

**DeepSeek Flash.** The direct provider is *not* the cheapest route:

| id | ctx | in | out | cache read |
|---|---|---|---|---|
| `deepseek/deepseek-flash` (direct API) | 1.0M | $0.15 | $0.60 | $0.003 |
| `openrouter/~deepseek/deepseek-v4-flash-latest` | **1.31M** | **$0.04** | **$0.10** | $0.01 |

OpenRouter is ~4x cheaper on input and 6x on output, with a bigger window. The
direct API only wins on cache reads ($0.003 vs $0.01), so it is the better pick
for the scout → fork pattern, where nearly every token is a cache hit. For
one-shot workers that read fresh files, use the OpenRouter route.

DeepSeek's *direct* API doubles its price at peak: 22:00–01:00 and 03:00–07:00
Chile time (all weekend is off-peak). OpenRouter pricing is flat.

**GLM Flash.**

| id | ctx | in | out | cache read |
|---|---|---|---|---|
| `z-ai/glm-5.3-flash` | 1.31M | $0.10 | $0.33 | $0.02 |
| `~z-ai/glm-flash-latest` | 1.31M | **$0.075** | **$0.25** | $0.015 |

The `-latest` alias is the same family, cheaper. Full `z-ai/glm-5.3` is $1.40/$4.40
— 14x the Flash input price, not worth it for a worker.

**Free models** are for testing the *plumbing* (does dispatch land, does the pane
report idle) — not for real work. Verified working with tools:
`nvidia/nemotron-3.5-lightning:free` (1M ctx), `nvidia/nemotron-3-ultra-550b-a55b:free`
(1M), `nex-agi/nex-n2.5-pro:free` (262k).

Two traps:
- The `openrouter/free` auto-router is **not** usable: it resolves to
  `thinkingmachines/*`, which return `403 ... only available on agentic harnesses`.
  Always name an explicit `:free` id.
- `z-ai/glm-5.2:free` does **not** support tools — useless as a worker.

### Managing the workers tab

```bash
bash /home/jp/setup/herdr/coordination.sh workers-tab     # print tab id
bash /home/jp/setup/herdr/coordination.sh workers-focus   # look at the workers
bash /home/jp/setup/herdr/coordination.sh workers-close   # close tab + all workers
```

Finishing one worker. `close` accepts a name now, same as every other command:

```bash
bash /home/jp/setup/herdr/coordination.sh ls               # my workers: pane status name cwd
bash /home/jp/setup/herdr/coordination.sh ls --all         # every coordinator's workers
bash /home/jp/setup/herdr/coordination.sh which pi2        # pane id a target resolves to
bash /home/jp/setup/herdr/coordination.sh close pi2        # close ONE worker (name or pane id)
bash /home/jp/setup/herdr/coordination.sh reap             # close my dead workers, forget stale panes
bash /home/jp/setup/herdr/coordination.sh reap --finished  # also close my done/idle workers
bash /home/jp/setup/herdr/coordination.sh help             # full command list
```

`ls`, `reap` and `help` are aliases. When in doubt about how to close something:
`which <name>` resolves it and `close <name>` closes it.

Rename the tab with `HERDR_WORKERS_TAB=<label>` (default `subagents`).
You still reach any worker by pane id or agent name from your own tab:
`dispatch pi2 "..."`, `read wJ:p5`.

## Start a worker forked from a pi session (inherited context)

```bash
bash /home/jp/setup/herdr/coordination.sh spawn-fork pi <uuid> [/path/to/repo]
bash /home/jp/setup/herdr/coordination.sh dispatch wN "<task>"
```

- `<uuid>`: full or partial pi session id (resolves local project dir first, then
  global), a session file path, or a `PI_SESSIONS_DIR` entry. pi only; other kinds
  are rejected.
- The worker starts with the source session's whole context (explored codebase,
  prior findings) and executes its new task from a fresh turn. Source session is
  never modified.
- Usage pattern: one scout worker explores the repo (read-only dispatch), then
  fork that session per subagent. Dispatch follow-up tasks promptly — provider
  prompt-cache TTL is ~5 min, so the inherited prefix stays cheap.
- Workers that write code should each run in their own worktree
  (`herdr worktree create`) to avoid edit collisions.

## Raw surface (when helpers are not enough)

`herdr agent prompt|wait|read|send-keys|list --json`, `herdr pane send-text`,
`herdr api snapshot`.

---
name: use-deskops
description: Comprehensive Pi skill for deskops workflow. Use when working in this repository's desk/, task lifecycle, atoms, pills, rituals, graph surfaces, or deskops CLI.
---

# Use Deskops

Deskops is the workflow-domain layer for repository-local operational knowledge and execution.

Use this skill when the task involves:

- `desk/` workflow surfaces.
- Tasks, boards, drawer work, inbox notes, pills, rituals, routines, primitives, atoms, or repository registry docs.
- Desk discovery, graph checks, task advancement, promotion, closeout, or workflow automation.
- Understanding how this repo's CLI maps to the project knowledge model.
- Deciding which deskops sub-skill applies to the specific sub-task at hand.

## What deskops owns

Deskops owns the workflow domain built on top of SLDB.

It owns:

- active and deferred workflow surfaces under `desk/`
- task routing through `desk/tasks/Board.md`
- rituals, pills, atoms, routines, and primitives
- repo-local workflow commands such as `deskops add`, `deskops list`, `deskops show`, `deskops promote`, `deskops advance task`, and `deskops graph`
- operational rules for intake, promotion, execution, testing, closeout, and phase gates

It does **not** own generic structured-document infrastructure. That belongs to SLDB.

## Mandatory read route

Before changing files, recover state from repo artifacts in this order:

1. `AGENTS.md`
2. `README.md`
3. `docs/faq.md`
4. `desk/tasks/Board.md`
5. matching board-routed pills in `desk/contexts/`
6. `desk/rituals/phase.md`
7. `desk/rituals/execution.md`
8. `desk/rituals/testing.md`
9. `desk/rituals/closeout.md`
10. relevant atoms under `desk/atoms/`

Prefer semantic discovery over blind scanning when possible:

```bash
sldb find title --in physical --store .sldb --pythonpath .
sldb find topic:atoms --in semantic --store .sldb --pythonpath .
deskops graph missing
```

## Routing to deskops sub-skills

`use-deskops` is the parent entry point. For specialized workflows, load the matching sub-skill instead of overloading this one:

| Load this sub-skill | When the task involves |
|---|---|
| `deskops-task-lifecycle` | Zero-context task bundles, subagent delegation (Executor/Tester), preflight gate, anti-mock enforcement, closeout commit ritual |
| `deskops-health-and-drift` | Desk health checks, drift detection, KGDB graph repair, materialization sync |
| `deskops-inbox-coordination` | Cross-project inbox messaging, triage of incoming notes, source deletion after promotion |

Each sub-skill is a partiality of the full workflow model defined here. They assume you already know the surfaces, CLI, and workflow model from this skill.

## Workflow model

The project logic is:

- **tasks** are bounded units of work
- **boards** route active tasks and shared pills
- **pills** are reusable execution truths, not one-per-task notes
- **atoms** are durable knowledge and architecture truths
- **rituals** define the gates for execution, testing, closeout, and phases
- **drawer tasks** are deferred repo-local work not yet promoted to the active board
- **inbox notes** are incoming unclear or external input, not the default place for new repo-local project work

Key rules:

- New unrouted repo-local work starts in `desk/drawer/tasks/`, not `desk/inbox/`.
- Promote drawer work before implementation.
- Keep one coherent deliverable per task.
- Do not skip execution, testing, or closeout gates.
- Every closed task ends with its own atomic commit.
- When a whole ready dependency layer closes, run the phase ritual before starting the next layer.
- Docs are human-facing materializations of atoms, not the only durable source of truth.

## Task-state recovery commands

Use direct CLI commands instead of improvising from chat state:

```bash
deskops show board Board --root .
deskops list tasks --root .
deskops show task <task-id> --root .
deskops next <task-id> --root .
deskops graph missing --root .
git status --short --branch
```

If the task changes graph or store semantics, also use:

```bash
sldb stores check --store .sldb
deskops graph build --root .
deskops graph missing --root .
```

## CLI surface

Common deskops commands:

```bash
deskops --help
deskops faq
deskops bootstrap
deskops init .
deskops add task --root . --title "..." --goal "..." --scope "..."
deskops add atom --root . --title "..." --answer "..." --five-wh-one-plus what
deskops list tasks --root .
deskops list atoms --root .
deskops show task <task-id> --root .
deskops show atom <atom-id> --root .
deskops promote drawer-task-to-active-task <task-selector>
deskops bind pill <pill-selector> --task <task-id> --root .
deskops advance task <task-id> --root .
deskops graph build --root .
deskops graph missing --root .
deskops repo register ...
deskops desk install .
```

CLI usage rules:

- Use `deskops ...`, not `bash deskops ...`.
- Prefer local repo-root execution instead of unnecessary `--root .` in prose, but include `--root .` in explicit workflow instructions when clarity matters.
- For CLI mutation or UX experiments, use a disposable sandbox desk such as `.tmp/deskops-cli-test` unless the task intentionally changes the tracked desk.

## Role logic

Deskops workflow roles (supervisor, executor, tester) are defined as **global/system-prompt concerns**. This skill does not cover their orchestration.

For the strict subagent-delegation protocol (zero-context bundles, Executor/Tester dispatch, preflight gate, anti-mock, closeout commit), load `deskops-task-lifecycle`.

## Atoms, pills, and docs

Use these distinctions consistently:

- Put durable architecture or policy in atoms.
- Put reusable execution guardrails in pills.
- Put active routed work in tasks.
- Put deferred candidate work in drawer tasks.
- Treat docs under `docs/` as materializations of atom truth.

When a doc rule changes materially, update the relevant atom first, then reflect it in the doc.

## When to load other skills

- Load `use-sldb` for `StructuredNLDoc` models, tracked Markdown, reversible markers, `.sldb` stores, document tracking, field operations, rendering, extraction, or model changes.
- If a needed document type does not exist, do not force it into `AtomDoc`: declare a repo-local model; that flow is covered in `use-sldb` ('Declaring a repo-local model').
- Load `use-kgdb` for graph contracts, graph snapshots, provenance, node/edge behavior, or graph runtime validation.
- Load `use-spec2viz` for structured diagram specs and generated diagram projections.
- Load `deskops-task-lifecycle` for zero-context task bundles, subagent delegation, preflight, anti-mock, closeout.
- Load `deskops-health-and-drift` for desk health checks, drift detection, KGDB graph repair, materialization.
- Load `deskops-inbox-coordination` for cross-project inbox messaging, triage, source deletion.

## Validation

Minimum repo validation:

```bash
pytest
```

For CLI work, also run the affected commands directly, for example:

```bash
python -m deskops --help
deskops faq
```

For graph or store work, prefer semantic checks:

```bash
sldb stores check --store .sldb
deskops graph missing
```

## Anti-patterns

Do not:

- invent alternate workflow categories when repo docs already define them
- treat unrouted `desk/tasks/` files as active by default
- bypass the board, pills, or rituals because the task seems familiar
- use ad hoc file edits where SLDB should own the structured-document operation
- skip from implementation straight to closeout
- treat role prompts as repo-local skills (use `deskops-task-lifecycle` instead for orchestration protocol)

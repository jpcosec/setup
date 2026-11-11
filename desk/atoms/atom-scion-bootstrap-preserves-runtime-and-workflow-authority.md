---
id: atom-scion-bootstrap-preserves-runtime-and-workflow-authority
title: Scion bootstrap preserves runtime and workflow authority
five_wh_one_plus: how
tags:
- system:scion
- system:deskops
- topic:runtime
provenance: desk/tasks/task-scion-autonomy-runtime-bootstrap-and-pi-lifecycle-bridge.md
---

# Scion bootstrap preserves runtime and workflow authority

## Answer

Scion bootstrap binds explicit validated current DeskOps and SLDB sources and an owned clean worktree of an explicit canonical ref, preserving original dirty checkouts. Recovery requires matching project, coordinator name, labels, worktree ownership and runtime package content fingerprints; preserve its own descendant commits and dirty child evidence using its recorded base even if the original ref vanished. Runtime source and data edits fail provenance checks, while unrelated desk/docs/evidence changes and generated caches do not. Serialize bootstrap against the original directory inode and reconcile again under the native lock. Mount the workspace at its host absolute path and /workspace through supported volumes. Scion owns agent identity, sessions, notifications and token refresh; DeskOps owns the task lifecycle, independent testing, evidence and closeout. Native Pi events send only normalized event names and tool identifiers to sciontool; generic agent end is working, never task completion. Autonomous resume reconciles durable desk and existing children in the preserved session, without replaying the initial assignment. Native Scion v0.2.21 template sync resolves its local source from the working directory independently of the --project Hub destination. Materialize only to an explicit project .scion/templates path and synchronize from its owning project configuration root; never resolve a same-named template from another project. Bootstrap failures expose only the known command stage and exit classification, never arguments, subprocess output or credentials. The same cwd-dependent local template selection applies to native start and resume, so those commands also run from the explicit project configuration root. A linked local broker provider binds the external non-Git Scion configuration directory, with workspace_path set to the explicit shared workspace; Hub dispatch derives the workspace from those settings and may clear the request workspace override. DeskOps owns the task Git worktree rather than asking Scion to create another per-agent copy.

Scion owns the resolved provider/model for its Pi launch. The launcher supplies the resolved settings as explicit CLI model selection when the caller did not select a model; missing or invalid partial settings fail closed instead of silently selecting an unrelated provider on resume. Local pinned images use fully qualified local names so the configured remote registry cannot rewrite them. Credentials are projected with native write-only Scion secrets, never committed or passed as literal arguments.

Scion0.2.21 injects its raw model value into resume argv. A raw alias such as small must be replaced with the provisioned resolved pair before Pi treats --model as a catalogue pattern; an explicit provider/model pair is preserved. Native installation with Hub enabled publishes the source but does not update its local copy. Install local files with --no-hub first, then publish global configs; a project-scoped Hub install must use the actual project filesystem path in this version, not only its UUID. Verify the Hub config image and actual Docker image ID, not successful CLI exit alone.

A stopped Scion agent can be recreated using its saved image metadata, replacing filesystem-only launcher patches. Migrating existing agents requires their saved compatibility image names to resolve to the corrected runtime image; preserve the original image IDs under rollback tags, never erase home/session data, and prove same-session continuation on an old laboratory agent before relying on the migration. Global harness configs govern new agents; old image bindings are a separate deployment concern.

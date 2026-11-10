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

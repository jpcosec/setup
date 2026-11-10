# Scion autonomy: reproducible startup and Pi lifecycle bridge

Owner request 2026-11-10: iterate with bots and change configuration/code wherever
needed until arriving at a desk can execute authorized work without manual prompts.

Preserve Scion 0.2.21, Pi fork jpcosec/pi-mono at
e9ba9e2ebce1b49dca85ab20007038c06e486ea5, project-scoped secret handling and fixed
Pi session. No pi-subagents. Add a pinned Pi extension bridging native Pi events
to existing sciontool hook events, including clear activity on new input/tool work
and return-to-idle without equating agent_end with DeskOps closeout. Validate
deliberate blocked/completed states and token refresh behavior.

Make startup choose/configure a current isolated desk/source revision, preserve
dirty originals and work ownership, and expose consistent Git worktree paths in
every new container. Commands must import intended DeskOps/SLDB sources rather
than stale baked wheels. Configure explicit child project/auth/workspace and
fresh tester templates. Keep supervision in Scion and task authority in DeskOps.

Deliver a runnable startup recipe, durable configuration and tests, not only
another report. Acceptance uses a disposable desk with bounded tasks: ONE initial
assignment then no follow-up messages through review, child dispatch, independent
test, closeout commit and next-task/phase progress. Include controlled failure,
restart/no duplicate child, and fresh-container reconstruction. No real production
task is dispatched during runtime validation.

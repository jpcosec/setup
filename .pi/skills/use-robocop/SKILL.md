---
name: use-robocop
description: Run commands and long-lived processes on the shared robocop dev workspace through persistent tmux sessions over SSH certificates. Use when a task needs to execute, launch, inspect, or keep alive work on robocop or on the per-service dev instances it fronts, instead of running locally.
---

# Use Robocop

Robocop is the shared development workspace (`governance-agent`, AWS Lightsail, `52.44.103.237`).

It is a **control plane, not a runtime**. Robocop hosts persistent tmux sessions and the SSH
certificate signer. Services themselves run on the dev instance assigned to them in
`routing/inventario.yaml`; from robocop you jump to those instances.

Use this skill when the task involves:

- running a command on robocop rather than on the local machine
- launching or inspecting a long-lived process (server, watcher, build, agent) that must survive disconnect
- sharing a terminal session with another person or agent
- driving work toward a per-service dev instance

Do **not** use this skill for local-only edits, local tests, or anything that never leaves the repo.

## Identity model (read before running anything)

Access is by **short-lived SSH certificate**, not static keys.

- Login goes to Cognito (`login.dev.heyantonia.com`), which issues an `id_token`.
- The signer on robocop validates that token, requires the `tmux-devs` group, and signs an
  ed25519 certificate valid **8 hours**, with `no-agent-forwarding` and `no-x11-forwarding`.
- The certificate principal is the user's email normalized: `jp@heyantonia.com` → `jp-heyantonia-com`.
  That is also the Unix account on robocop.

Certificate files on the local machine:

| Path | What |
|---|---|
| `~/.ssh/robocop_ed25519` | private key |
| `~/.ssh/robocop_ed25519-cert.pub` | the certificate |
| `~/.ssh/robocop_ed25519-cert.pub.json` | `valid_until` metadata |
| `~/.config/robocop/config.toml` | signer URL, host, Cognito client |
| `~/.config/robocop/state.json` | `ssh_user` |

## Check the certificate first

A dead certificate is the most common failure. Check before anything else:

```bash
python3 -c "
import json,datetime,pathlib
p=pathlib.Path.home()/'.ssh/robocop_ed25519-cert.pub.json'
if not p.exists(): print('NO CERT -> run: robocop auth'); raise SystemExit
u=datetime.datetime.fromisoformat(json.loads(p.read_text())['valid_until'])
left=u-datetime.datetime.now(u.tzinfo)
print('EXPIRED -> run: robocop auth' if left.total_seconds()<=300 else f'ok, {left}')
"
```

**The agent cannot renew the certificate.** `robocop auth` opens a browser and needs a human
password. If it is expired, stop and ask the user to run `robocop auth`.

If `signer_url` is `http://127.0.0.1:8700`, renewal also needs the SSH tunnel running:
`bash <repo>/robocop/tunnel.sh`. Once DNS for `signer.dev.heyantonia.com` exists, the tunnel
is no longer needed.

## Connecting

Define this once per session:

```bash
SSHC="ssh -i $HOME/.ssh/robocop_ed25519 -i $HOME/.ssh/robocop_ed25519-cert.pub \
  -o IdentitiesOnly=yes -o StrictHostKeyChecking=accept-new \
  $(python3 -c "import json,pathlib;print(json.loads((pathlib.Path.home()/'.config/robocop/state.json').read_text())['ssh_user'])")@52.44.103.237"
SOCK=/srv/tmux/shared
```

Verify:

```bash
$SSHC 'id; hostname'
```

## Never use `robocop attach` as an agent

`attach` needs an interactive TTY and will fail with `open terminal failed: not a terminal`.
Agents drive tmux with `send-keys` and `capture-pane` instead.

| Goal | Use |
|---|---|
| list sessions | `robocop ls` or `$SSHC "tmux -S $SOCK ls"` |
| create session | `tmux -S $SOCK new-session -d -s <name> -c <dir>` |
| send a command | `tmux -S $SOCK send-keys -t <name> '<cmd>' Enter` |
| read output | `tmux -S $SOCK capture-pane -p -S - -t <name>` |
| kill session | `tmux -S $SOCK kill-session -t <name>` |

Always pass `-S -` to `capture-pane`. Without it you only get the visible screen, which is
often blank and looks like failure.

## Running a command and getting its real exit code

`send-keys` is fire-and-forget: it returns immediately and tells you nothing about success.
For anything whose result matters, redirect to a file, append the exit code, and poll for a
done marker.

```bash
JOB=build-$(date +%s)
$SSHC "tmux -S $SOCK new-session -d -s $JOB -c /srv/wt" 2>/dev/null || true
$SSHC "tmux -S $SOCK send-keys -t $JOB '(<YOUR COMMAND HERE>) > /tmp/$JOB.out 2>&1; echo RC=\$? >> /tmp/$JOB.out; echo __DONE__ >> /tmp/$JOB.out' Enter"

for i in $(seq 1 120); do
  $SSHC "grep -q __DONE__ /tmp/$JOB.out 2>/dev/null" && break
  sleep 5
done

$SSHC "cat /tmp/$JOB.out"
```

Read the `RC=` line. `RC=0` is success; anything else is a failure you must report.
If the loop ends without `__DONE__`, the job is still running — say so rather than
claiming success.

## Long-lived processes

For a server or watcher that should outlive the connection, start it in its own session and
leave it. Do not wait for a done marker that will never come.

```bash
$SSHC "tmux -S $SOCK new-session -d -s api-dev -c /srv/wt/<service>"
$SSHC "tmux -S $SOCK send-keys -t api-dev '<start command>' Enter"
sleep 5
$SSHC "tmux -S $SOCK capture-pane -p -S - -t api-dev | tail -30"
```

Confirm it is actually up from the captured output before reporting success. A session that
exists is not proof the process started.

## Conventions

- **One session per service or branch**, not per person. Name it after the service
  (`mepu-motor`), not after yourself.
- Worktrees live in `/srv/wt/<session>`; repo clones in `/srv/repos`; the shared socket is
  `/srv/tmux/shared` (mode `660`, group `devs`).
- `tmux-new <session> <branch>` creates a worktree plus session, and needs `TMUX_REPO` set to
  the repo path.
- **Robocop runs no services.** To run a service, jump from robocop to the dev instance
  assigned in `routing/inventario.yaml`.
- Never write secrets into `send-keys`: the command lands in shell history and in the pane.
  Use files on the server or environment files instead.

## Shared sessions

Several users and agents can attach to the same session and see each other. Before sending
keys to a session you did not create, capture the pane first and check nobody is mid-task.
Typing into someone else's shell is destructive.

## Failure routing

| Symptom | Cause | Action |
|---|---|---|
| `Permission denied (publickey)` | certificate expired or missing | ask the user for `robocop auth` |
| `open terminal failed: not a terminal` | used `attach` | use `send-keys` + `capture-pane` |
| `capture-pane` empty | missing `-S -` | re-capture with history |
| `no server running on /srv/tmux/shared` | no session exists yet | create one with `new-session -d` |
| `error connecting ... Permission denied` on socket | user not in `devs`, or socket not `660` | `provision-user <email>`; `chmod 660` the socket |
| signer `403` | user not in `tmux-devs` group | `onboard-user.sh <email>` |
| signer unreachable on renewal | tunnel down | `bash <repo>/robocop/tunnel.sh` |

## Current state

`robocop/STATUS.md` in the Governance repo is the source of truth for what is done and what is
pending. Read it before assuming a capability exists. Notably: the public signer domain is not
yet in DNS, so certificate renewal still depends on the SSH tunnel.

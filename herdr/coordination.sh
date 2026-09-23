#!/usr/bin/env bash
# coordination.sh — use herdr-managed agents as workers.
#
# A coordinator (any agent session) can dispatch tasks to agent panes and
# collect their output. Workers are interactive agents running inside herdr
# (kind: pi, codex, claude, opencode, gemini, ...).
#
# Usage (from a coordinator agent, via bash tool):
#   herdr/coordination.sh agents                 # table: name status pane cwd
#   herdr/coordination.sh dispatch <T> "<text>"  # prompt + wait idle/done + capture output
#   herdr/coordination.sh say <T> "<text>"       # fire-and-forget prompt
#   herdr/coordination.sh read <T>               # capture current pane output
#   herdr/coordination.sh wait <T> [state]       # wait for idle/done/blocked
#   herdr/coordination.sh spawn <kind> [cwd] [agent-args...]
#                                        # start agent in the workers tab
#   herdr/coordination.sh spawn-fork <kind> <uuid> [cwd]
#                                        # spawn pi forked from a session
#                                        # (uuid = full/partial pi session id,
#                                        #  path, or PI_SESSIONS_DIR entry)
#   herdr/coordination.sh workers-tab            # print the workers tab id
#   herdr/coordination.sh workers-focus          # bring the workers tab up
#   herdr/coordination.sh workers-close          # close the whole workers tab (EVERY coordinator's)
#   herdr/coordination.sh workers                # this coordinator's workers: pane status name cwd
#   herdr/coordination.sh close <pane>           # close ONE worker pane, as soon as its work is verified
#   herdr/coordination.sh workers-reap [--finished|--all]
#                                        # close this coordinator's dead workers (default), also its
#                                        # done/idle ones (--finished), or all of them (--all)
#
# Workers spawn in a separate tab (default "subagents", $HERDR_WORKERS_TAB) so
# they never flood the coordinator's screen. The tab is created on first spawn,
# reused afterwards, and never stealing focus.
#
# TARGET: agent kind (first match) or pane id (precise, e.g. w6:p6).
# Transcript: $HERDR_TRANSCRIPT (default ./.herdr-coordination.md)
set -euo pipefail

TRANSCRIPT="${HERDR_TRANSCRIPT:-.herdr-coordination.md}"
TIMEOUT_MS="${HERDR_TIMEOUT_MS:-600000}"
WORKERS_TAB="${HERDR_WORKERS_TAB:-subagents}"

die() { printf 'coordination: %s\n' "$1" >&2; exit 1; }
need_herdr() { command -v herdr >/dev/null || die "herdr not on PATH"; }

cmd_agents() {
  need_herdr
  herdr agent list | python3 -c '
import json, sys
d = json.load(sys.stdin)
seen = set()
print("%-16s %-9s %-8s %s" % ("name", "status", "pane", "cwd"))
for a in d["result"]["agents"]:
    pane = a["pane_id"]
    if pane in seen:
        continue
    seen.add(pane)
    print("%-16s %-9s %-8s %s" % (a.get("name") or a["agent"], a["agent_status"], pane, a.get("cwd", "?")))'
}

read_out() { need_herdr; herdr agent read "$1" 2>&1 || true; }

cmd_read() { need_herdr; read_out "$1"; }

cmd_wait() {
  need_herdr
  local t="$1" state="${2:-}"
  if [ -n "$state" ]; then
    herdr agent wait "$t" --until "$state"
  else
    herdr agent wait "$t" --until idle --until done
  fi
}

cmd_say() { need_herdr; local t="$1"; shift; herdr agent prompt "$t" "$*"; }

cmd_dispatch() {
  need_herdr
  local t="$1"; shift
  local status out
  status=$(herdr agent prompt "$t" "$*" --wait --until idle --until done --until blocked --timeout "$TIMEOUT_MS" 2>&1 | tail -1 || true)
  case "$status" in
    *agent_blocked*) die "target $t is blocked (waiting for user input); read it and respond" ;;
    *timeout*|*agent_prompt_stalled*) die "dispatch to $t failed: $status" ;;
  esac
  out=$(read_out "$t")
  {
    printf '\n--- %s dispatch -> %s ---\nPROMPT: %s\nOUTPUT (tail):\n%s\n' \
      "$(date '+%F %T')" "$t" "$*" "$(printf '%s' "$out" | tail -c 4000)"
  } >> "$TRANSCRIPT"
  printf '%s\n' "$out"
}

pane_id_from() { python3 -c 'import json,sys; print(json.load(sys.stdin)["result"]["pane"]["pane_id"])' 2>/dev/null || true; }

resolve_pi_session() {
  local uuid="$1"
  local base="${PI_SESSIONS_DIR:-$HOME/.pi/agent/sessions}"
  local match
  match=$(find "$base" -maxdepth 2 -name "*${uuid}*.jsonl" 2>/dev/null | sort | tail -1)
  [ -n "$match" ] || die "no pi session matching '$uuid' under $base"
  printf '%s' "$match"
}

# ---------------------------------------------------------------------------
# Worker briefing: what a subagent must know the moment it wakes up.
#
# A freshly spawned worker knows nothing about WHY it exists. Worse, a worker in
# a git worktree looks exactly like a worker in the main checkout, so it will
# happily `git checkout` a branch that another worker is using, or assume its
# siblings' files are missing. The briefing below is injected as system prompt
# at spawn time, so the worker never has to be told twice.
# ---------------------------------------------------------------------------
worker_briefing() {
  local cwd="$1" label="$2"
  ( cd "$cwd" 2>/dev/null || exit 0
    printf 'You are a SUBAGENT dispatched by a coordinator, not a standalone session.\n'
    [ -n "$label" ] && printf 'Your worker label is: %s\n' "$label"
    printf 'Working directory: %s\n' "$cwd"

    git rev-parse --is-inside-work-tree >/dev/null 2>&1 || exit 0
    local common dir branch root
    common=$(git rev-parse --git-common-dir 2>/dev/null)
    dir=$(git rev-parse --git-dir 2>/dev/null)
    branch=$(git branch --show-current 2>/dev/null)
    root=$(git rev-parse --show-toplevel 2>/dev/null)
    printf 'Git branch: %s\n' "${branch:-<detached>}"

    if [ "$(cd "$(dirname "$common")" && pwd)/$(basename "$common")" != "$(cd "$(dirname "$dir")" && pwd)/$(basename "$dir")" ]; then
      printf 'You are in a GIT WORKTREE (linked checkout), not the main repo.\n'
      printf '  worktree path : %s\n' "$root"
      printf '  shared .git   : %s\n' "$common"
      printf 'Rules that follow from that:\n'
      printf '  - Stay inside this worktree. Sibling worktrees belong to OTHER agents working in parallel.\n'
      printf '  - Do NOT checkout/switch branches: a branch is checked out by at most one worktree.\n'
      printf '  - Do NOT run destructive repo-wide commands (git gc, git worktree prune, rebase of other branches).\n'
      printf '  - Commits here are local to this branch; the coordinator integrates them.\n'
      local others
      others=$(git worktree list 2>/dev/null | awk -v r="$root" '$1!=r {print "  - "$0}')
      if [ -n "$others" ]; then
        printf 'Other worktrees on this repo (DO NOT TOUCH):\n%s\n' "$others"
      fi
    else
      printf 'You are in the MAIN checkout of this repo (not a worktree).\n'
    fi
  ) 2>/dev/null
}

# Registry of spawned workers, so they can be reaped later (see workers-reap).
# One line per worker: <epoch>\t<pane>\t<name>\t<cwd>\t<owner>
# <owner> is the coordinator's own pane ($HERDR_PANE_ID): the workers tab is shared by
# every coordinator on the machine, and a coordinator only ever reaps what it spawned.
WORKERS_DB="${HERDR_WORKERS_DB:-${TMPDIR:-/tmp}/herdr-workers-$(id -u).tsv}"
OWNER="${HERDR_PANE_ID:-unknown}"

register_worker() {
  printf '%s\t%s\t%s\t%s\t%s\n' "$(date +%s)" "$1" "$2" "$3" "$OWNER" >> "$WORKERS_DB"
}

# Drop one pane from the registry.
forget_worker() {
  [ -f "$WORKERS_DB" ] || return 0
  local tmp; tmp=$(mktemp)
  awk -F'\t' -v p="$1" '$2 != p' "$WORKERS_DB" > "$tmp" && mv "$tmp" "$WORKERS_DB"
}

# "<pane>\t<status>" for every live pane; status is "-" for a pane with no agent in it.
pane_states() {
  herdr pane list | python3 -c '
import json, sys
for p in json.load(sys.stdin)["result"]["panes"]:
    print("%s\t%s" % (p["pane_id"], (p.get("agent") and p.get("agent_status")) or "-"))' 2>/dev/null || true
}

# Close one worker pane and forget it. The explicit, always-safe way to finish a worker.
cmd_close() {
  need_herdr
  herdr pane close "$1" >/dev/null 2>&1 || true
  forget_worker "$1"
  printf 'closed %s\n' "$1"
}

# This coordinator's registered workers: pane, status, name, cwd.
cmd_workers() {
  need_herdr
  [ -f "$WORKERS_DB" ] || return 0
  local states; states=$(pane_states)
  awk -F'\t' -v o="$OWNER" '$5 == o {print $2 "\t" $3 "\t" $4}' "$WORKERS_DB" |
    while IFS=$'\t' read -r pane name cwd; do
      st=$(printf '%s\n' "$states" | awk -F'\t' -v p="$pane" '$1 == p {print $2}')
      printf '%-8s %-9s %-16s %s\n' "$pane" "${st:-gone}" "$name" "$cwd"
    done
}

# Reap this coordinator's workers. By default only what is certainly dead: a registered
# pane whose agent is gone (status "-") is closed, and one that no longer exists is
# forgotten. `done`/`idle` are NOT proof a worker finished (an agent waiting on its own
# background shell reports them), so those need --finished; --all closes every one.
cmd_workers_reap() {
  need_herdr
  local mode="${1:-}" pane st name cwd
  [ -f "$WORKERS_DB" ] || return 0
  cmd_workers | while read -r pane st name cwd; do
    case "$st" in
      gone) forget_worker "$pane"; printf 'forgot %s (%s): pane gone\n' "$pane" "$name" ;;
      -)    cmd_close "$pane" ;;
      done|idle) [ "$mode" = "--finished" ] || [ "$mode" = "--all" ] && cmd_close "$pane" || true ;;
      *)    [ "$mode" = "--all" ] && cmd_close "$pane" || true ;;
    esac
  done
}

# Tab id of the workers tab, empty if it does not exist yet.
workers_tab_id() {
  herdr tab list | WORKERS_TAB="$WORKERS_TAB" python3 -c '
import json, os, sys
label = os.environ["WORKERS_TAB"]
tabs = json.load(sys.stdin)["result"]["tabs"]
print(next((t["tab_id"] for t in tabs if t["label"] == label), ""))' 2>/dev/null || true
}

# Pane ids of a tab, oldest first.
tab_panes() {
  herdr pane list | TAB="$1" python3 -c '
import json, os, sys
tab = os.environ["TAB"]
for p in json.load(sys.stdin)["result"]["panes"]:
    if p.get("tab_id") == tab:
        print(p["pane_id"])' 2>/dev/null || true
}

cmd_workers_tab() {
  need_herdr
  local t; t=$(workers_tab_id)
  [ -n "$t" ] || die "no workers tab yet (spawn a worker first)"
  printf '%s\n' "$t"
}
cmd_workers_focus() { need_herdr; herdr tab focus "$(cmd_workers_tab)"; }
cmd_workers_close() { need_herdr; herdr tab close "$(cmd_workers_tab)"; }

# A free pane in the workers tab, creating the tab on first use. Never steals
# focus: the coordinator keeps its screen while workers pile up next door.
workers_pane() {
  local cwd="$1"
  local tab out pane last
  tab=$(workers_tab_id)
  if [ -z "$tab" ]; then
    out=$(herdr tab create --label "$WORKERS_TAB" ${cwd:+--cwd "$cwd"} --no-focus 2>&1) \
      || die "could not create workers tab: $out"
    pane=$(printf '%s' "$out" | python3 -c 'import json,sys; print(json.load(sys.stdin)["result"]["root_pane"]["pane_id"])' 2>/dev/null || true)
    [ -n "$pane" ] || die "could not read root pane of workers tab from: $out"
    printf '%s' "$pane"
    return
  fi
  last=$(tab_panes "$tab" | tail -1)
  [ -n "$last" ] || die "workers tab $tab has no panes"
  out=$(herdr pane split --pane "$last" --direction right ${cwd:+--cwd "$cwd"} 2>&1) \
    || die "could not split workers pane: $out"
  pane=$(printf '%s' "$out" | pane_id_from)
  [ -n "$pane" ] || die "could not determine new pane id from: $out"
  printf '%s' "$pane"
}

# First free agent name for a kind: pi, pi2, pi3, ... herdr requires unique
# agent names, and a coordinator spawning several workers of the same kind
# would otherwise fail on the second one.
free_agent_name() {
  local kind="$1" taken n
  taken=$(herdr agent list | python3 -c '
import json, sys
print(" ".join(a.get("name") or a["agent"] for a in json.load(sys.stdin)["result"]["agents"]))' 2>/dev/null || true)
  case " $taken " in *" $kind "*) ;; *) printf '%s' "$kind"; return ;; esac
  n=2
  while case " $taken " in *" ${kind}${n} "*) true ;; *) false ;; esac; do n=$((n + 1)); done
  printf '%s%s' "$kind" "$n"
}

cmd_spawn() {
  need_herdr
  local kind="$1"; shift
  local cwd="" args=()
  if [ $# -gt 0 ] && [[ "$1" != -* ]]; then cwd="$1"; shift; fi
  args=("$@")
  local pane name out
  local start=()
  name=$(free_agent_name "$kind")
  pane=$(workers_pane "$cwd")
  start=(herdr agent start "$name" --kind "$kind" --pane "$pane")
  if [ ${#args[@]} -gt 0 ]; then start+=(-- "${args[@]}"); fi
  # The pane was split just for this worker: do not leave it orphaned and empty.
  if ! out=$("${start[@]}" 2>&1); then
    herdr pane close "$pane" >/dev/null 2>&1 || true
    die "agent start $name ($kind) failed, pane $pane closed: $out"
  fi
  printf '%s\n' "$out"
  register_worker "$pane" "$name" "$cwd"
  printf 'spawned %s (%s) in pane %s (tab %s)\n' "$name" "$kind" "$pane" "$(workers_tab_id)"
}

cmd_spawn_fork() {
  local kind="$1" uuid="$2"
  [ "$kind" = "pi" ] || die "spawn-fork: pi sessions only (got kind: $kind)"
  [ -n "$uuid" ] || die "spawn-fork: missing session uuid"
  local path
  path=$(resolve_pi_session "$uuid")
  printf 'forking session %s\n' "$path"
  shift 2
  local cwd=""
  if [ $# -gt 0 ] && [[ "$1" != -* ]]; then cwd="$1"; shift; fi
  cmd_spawn "$kind" "${cwd:-$PWD}" --fork "$path"
}

cmd="${1:-}"; [ -n "$cmd" ] || { sed -n '2,20p' "$0"; exit 1; }
shift
case "$cmd" in dispatch|say|read|wait|spawn|close) [ $# -ge 1 ] || die "usage: coordination.sh $cmd <TARGET> [args]" ;; esac
case "$cmd" in
  spawn-fork) [ $# -ge 2 ] || die "usage: coordination.sh spawn-fork <kind> <uuid> [cwd]" ;;
esac
case "$cmd" in
  agents)     cmd_agents "$@" ;;
  dispatch)   cmd_dispatch "$@" ;;
  say)        cmd_say "$@" ;;
  read)       cmd_read "$@" ;;
  wait)       cmd_wait "$@" ;;
  spawn)      cmd_spawn "$@" ;;
  spawn-fork) cmd_spawn_fork "$@" ;;
  workers-tab)   cmd_workers_tab "$@" ;;
  workers-focus) cmd_workers_focus "$@" ;;
  workers-close) cmd_workers_close "$@" ;;
  workers)       cmd_workers "$@" ;;
  workers-reap)  cmd_workers_reap "$@" ;;
  close)         cmd_close "$@" ;;
  *)          die "unknown command: $cmd" ;;
esac

#!/usr/bin/env bash
set -euo pipefail

SETUP_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
HERDR_BIN="${HERDR_BIN:-herdr}"

if ! command -v "$HERDR_BIN" >/dev/null 2>&1; then
  printf '%s\n' "Herdr not found on PATH. Install it first: https://herdr.dev/docs/install/" >&2
  exit 1
fi

server_status="$("$HERDR_BIN" status server --json 2>&1 || true)"
if [[ "$server_status" != *'"running":true'* ]]; then
  # setsid is Linux-only; nohup alone is enough to detach on macOS.
  detach=()
  command -v setsid >/dev/null 2>&1 && detach=(setsid)
  nohup ${detach[@]+"${detach[@]}"} "$HERDR_BIN" server >"${TMPDIR:-/tmp}/deskops-herdr-server.log" 2>&1 </dev/null &
  for _ in {1..30}; do
    server_status="$("$HERDR_BIN" status server --json 2>&1 || true)"
    [[ "$server_status" == *'"running":true'* ]] && break
    sleep 0.2
  done
fi

# init_opsys.py imports deskops, so it needs an interpreter that has deskops'
# dependencies. Prefer $OPSYS_PYTHON, then the interpreter behind the installed
# `deskops` CLI (uv tool / pipx venv), then plain python3.
PYTHON="${OPSYS_PYTHON:-}"
if [[ -z "$PYTHON" ]] && ! python3 -c 'import pydantic' >/dev/null 2>&1; then
  deskops_bin="$(command -v deskops || true)"
  if [[ -n "$deskops_bin" ]]; then
    shebang="$(head -1 "$deskops_bin")"
    candidate="${shebang#\#!}"
    [[ -x "$candidate" ]] && PYTHON="$candidate"
  fi
fi

exec "${PYTHON:-python3}" "$SETUP_ROOT/herdr/init_opsys.py" "$@"

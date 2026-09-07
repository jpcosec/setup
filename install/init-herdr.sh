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
  nohup setsid "$HERDR_BIN" server >"${TMPDIR:-/tmp}/deskops-herdr-server.log" 2>&1 </dev/null &
  for _ in {1..30}; do
    server_status="$("$HERDR_BIN" status server --json 2>&1 || true)"
    [[ "$server_status" == *'"running":true'* ]] && break
    sleep 0.2
  done
fi

exec python3 "$SETUP_ROOT/herdr/init_opsys.py" "$@"

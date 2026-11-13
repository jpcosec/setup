#!/usr/bin/env bash
# Enlaza en Claude Code (~/.claude/skills) los skills de deskops/sldb que viven en ~/setup/.pi/skills.
# Hasta el 13-11 solo los veía pi: el coordinador de Claude Code se saltaba el protocolo de deskops
# (paquete de contexto cero, review preflight/bundle, tester, closeout con --run-dir). Idempotente.
set -euo pipefail
SETUP_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="$SETUP_ROOT/.pi/skills"
DST="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
mkdir -p "$DST"
for s in use-deskops deskops-task-lifecycle deskops-health-and-drift deskops-inbox-coordination use-sldb agent-coordinator; do
  [ -f "$SRC/$s/SKILL.md" ] || { printf 'falta %s/SKILL.md\n' "$SRC/$s" >&2; continue; }
  if [ -e "$DST/$s" ] && [ ! -L "$DST/$s" ]; then printf '%s existe y no es enlace: no se toca\n' "$DST/$s" >&2; continue; fi
  ln -sfn "$SRC/$s" "$DST/$s"
  printf 'skill %s -> %s\n' "$s" "$SRC/$s"
done

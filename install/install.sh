#!/usr/bin/env bash
set -euo pipefail

SETUP_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
DRY_RUN=0

if [[ "${1:-}" == "--dry-run" ]]; then
  DRY_RUN=1
fi

link_path() {
  local source="$1"
  local target="$2"

  if [[ -L "$target" && "$(readlink -- "$target")" == "$source" ]]; then
    printf 'already linked %s -> %s\n' "$target" "$source"
    return
  fi

  if [[ -e "$target" || -L "$target" ]]; then
    if [[ "$DRY_RUN" == 1 ]]; then
      printf 'would preserve existing: %s\n' "$target"
      return
    fi
    printf 'refusing to overwrite existing path: %s\n' "$target" >&2
    printf 'move it manually, then rerun this installer.\n' >&2
    return 1
  fi

  if [[ "$DRY_RUN" == 1 ]]; then
    printf 'would link %s -> %s\n' "$target" "$source"
    return
  fi

  mkdir -p "$(dirname -- "$target")"
  ln -s "$source" "$target"
  printf 'linked %s -> %s\n' "$target" "$source"
}

source_line() {
  local file="$1"
  local rc="$2"
  local line="[ -f $file ] && . $file"

  if [[ -f "$rc" ]] && grep -qxF "$line" "$rc"; then
    printf 'already sourced in %s: %s\n' "$rc" "$file"
    return
  fi

  if [[ "$DRY_RUN" == 1 ]]; then
    printf 'would add to %s: %s\n' "$rc" "$line"
    return
  fi

  printf '\n%s\n' "$line" >>"$rc"
  printf 'added to %s: %s\n' "$rc" "$line"
}

link_path "$SETUP_ROOT/wezterm/wezterm.lua" "$HOME/.wezterm.lua"
link_path "$SETUP_ROOT/wezterm/keybindings.lua" "$HOME/.config/wezterm/keybindings.lua"
link_path "$SETUP_ROOT/nvim" "$HOME/.config/nvim"
link_path "$SETUP_ROOT/yazi" "$HOME/.config/yazi"
source_line "$SETUP_ROOT/shell/yazi.sh" "$HOME/.bashrc"

printf '%s\n' "Herdr initializer: python3 $SETUP_ROOT/herdr/init_opsys.py"
printf '%s\n' "Convenience wrapper: $SETUP_ROOT/install/init-herdr.sh"
printf '%s\n' 'Add --agents to start executor/tester Pi agents.'

link_path "$SETUP_ROOT/pi/get-secret" "$HOME/.pi/agent/bin/get-secret"

printf '%s\n' 'Pi configuration is intentionally not linked automatically.'
printf '%s\n' 'Copy pi/settings.example.json to ~/.pi/agent/settings.json only after review.'
printf '%s\n' 'Keep ~/.pi/agent/models.json and auth.json machine-local.'

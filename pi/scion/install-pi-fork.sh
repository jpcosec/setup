#!/usr/bin/env bash
# Build the pinned fork without regenerating the model catalogue.
set -euo pipefail
revision=e9ba9e2ebce1b49dca85ab20007038c06e486ea5
repository=https://github.com/jpcosec/pi-mono.git
source_dir="$HOME/bin/pirate/pi-mono"
if [[ "${1:-}" == --help ]]; then
  echo 'Usage: install-pi-fork.sh (Node >=20.6, npm, git; installs pinned fork under ~/bin/pirate/pi-mono)'
  exit 0
fi
[[ $# == 0 ]] || { echo 'Unexpected arguments' >&2; exit 1; }
if [[ ! -e "$source_dir" ]]; then
  mkdir -p "$(dirname "$source_dir")"
  git clone --no-checkout "$repository" "$source_dir"
  git -C "$source_dir" checkout --detach "$revision"
fi
[[ -d "$source_dir/.git" ]] || { echo 'Expected a Git checkout; refusing replacement' >&2; exit 1; }
remote=$(git -C "$source_dir" remote get-url origin)
case "$remote" in
  https://github.com/jpcosec/pi-mono.git|https://github.com/jpcosec/pi-mono|git@github.com:jpcosec/pi-mono.git) ;;
  *) echo 'Unexpected origin; refusing build' >&2; exit 1 ;;
esac
[[ $(git -C "$source_dir" rev-parse HEAD) == "$revision" ]] || { echo 'Unexpected revision; refusing checkout or reset' >&2; exit 1; }
# Preserve every source change: require review rather than overwriting dirty files.
[[ -z $(git -C "$source_dir" status --porcelain --untracked-files=all) ]] || { echo 'Checkout has changes; refusing build without altering them' >&2; exit 1; }
cd "$source_dir"
npm ci
for package in tui ai agent coding-agent; do
  (cd "packages/$package" && ../../node_modules/.bin/tsgo -p tsconfig.build.json)
done
cd packages/coding-agent
mkdir -p dist/modes/interactive/{theme,assets} dist/core/export-html/vendor
cp src/modes/interactive/theme/*.json dist/modes/interactive/theme/
cp src/modes/interactive/assets/*.png dist/modes/interactive/assets/
cp src/core/export-html/template.{html,css,js} dist/core/export-html/
cp src/core/export-html/vendor/*.js dist/core/export-html/vendor/
chmod +x dist/cli.js
mkdir -p "$HOME/.local/bin"
if [[ -e "$HOME/.local/bin/pi" && ! -L "$HOME/.local/bin/pi" ]]; then
  echo '~/.local/bin/pi is not a symlink; refusing replacement' >&2
  exit 1
fi
ln -sfn "$source_dir/packages/coding-agent/dist/cli.js" "$HOME/.local/bin/pi"
"$HOME/.local/bin/pi" --version

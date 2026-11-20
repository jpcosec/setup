#!/usr/bin/env bash
# Install lazygit from official tarball to ~/.local/bin (Linux and macOS)
set -euo pipefail

case "$(uname -s)" in
  Linux) OS="linux" ;;
  Darwin) OS="darwin" ;;
  *) printf 'unsupported OS: %s\n' "$(uname -s)" >&2; exit 1 ;;
esac

ARCH="${LAZYGIT_ARCH:-$(uname -m)}"
case "$ARCH" in
  x86_64) ARCH_DEB="x86_64" ;;
  aarch64|arm64) ARCH_DEB="arm64" ;;
  *) printf 'unsupported architecture: %s\n' "$ARCH" >&2; exit 1 ;;
esac

VERSION="${LAZYGIT_VERSION:-}"
if [[ -z "$VERSION" ]]; then
  # sed instead of `grep -P`: BSD grep on macOS has no PCRE.
  VERSION=$(curl -sf "https://api.github.com/repos/jesseduffield/lazygit/releases/latest" \
    | sed -n 's/.*"tag_name": *"v\([^"]*\)".*/\1/p' | head -1)
fi
if [[ -z "$VERSION" ]]; then
  printf 'could not determine latest lazygit version\n' >&2
  exit 1
fi

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
cd "$tmp"

base="https://github.com/jesseduffield/lazygit/releases/download/v${VERSION}"
# Release assets switched from "Linux"/"Darwin" to lowercase OS names; try both.
OS_TITLE="$(printf '%s' "${OS:0:1}" | tr '[:lower:]' '[:upper:]')${OS:1}"
curl -fLo lazygit.tar.gz "${base}/lazygit_${VERSION}_${OS}_${ARCH_DEB}.tar.gz" \
  || curl -fLo lazygit.tar.gz "${base}/lazygit_${VERSION}_${OS_TITLE}_${ARCH_DEB}.tar.gz"
tar xf lazygit.tar.gz lazygit
mkdir -p ~/.local/bin
install lazygit ~/.local/bin/
printf 'lazygit %s installed\n' "$(~/.local/bin/lazygit --version | head -1)"

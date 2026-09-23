#!/usr/bin/env bash
# Install lazygit from official tarball to ~/.local/bin
set -euo pipefail

ARCH="${LAZYGIT_ARCH:-$(uname -m)}"
case "$ARCH" in
  x86_64) ARCH_DEB="x86_64" ;;
  aarch64|arm64) ARCH_DEB="arm64" ;;
  *) printf 'unsupported architecture: %s\n' "$ARCH" >&2; exit 1 ;;
esac

VERSION="${LAZYGIT_VERSION:-}"
if [[ -z "$VERSION" ]]; then
  VERSION=$(curl -sf "https://api.github.com/repos/jesseduffield/lazygit/releases/latest" \
    | grep -Po '"tag_name": "v\K[^"]*')
fi
if [[ -z "$VERSION" ]]; then
  printf 'could not determine latest lazygit version\n' >&2
  exit 1
fi

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
cd "$tmp"

curl -fLo lazygit.tar.gz "https://github.com/jesseduffield/lazygit/releases/download/v${VERSION}/lazygit_${VERSION}_Linux_${ARCH_DEB}.tar.gz"
tar xf lazygit.tar.gz lazygit
mkdir -p ~/.local/bin
install lazygit ~/.local/bin/
printf 'lazygit %s installed\n' "$(~/.local/bin/lazygit --version | head -1)"
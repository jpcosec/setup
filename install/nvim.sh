#!/usr/bin/env bash
# Install Neovim from official tarball to ~/.local/nvim
set -euo pipefail

ARCH="${NVIM_ARCH:-$(uname -m)}"
case "$ARCH" in
  x86_64) ARCH_DEB="x86_64" ;;
  aarch64|arm64) ARCH_DEB="arm64" ;;
  *) printf 'unsupported architecture: %s\n' "$ARCH" >&2; exit 1 ;;
esac

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
cd "$tmp"

curl -fLO "https://github.com/neovim/neovim/releases/latest/download/nvim-linux-${ARCH_DEB}.tar.gz"
tar xzf "nvim-linux-${ARCH_DEB}.tar.gz"
mkdir -p ~/.local
rm -rf ~/.local/nvim
mv "nvim-linux-${ARCH_DEB}" ~/.local/nvim
mkdir -p ~/.local/bin
ln -sf ~/.local/nvim/bin/nvim ~/.local/bin/nvim
printf 'nvim %s installed\n' "$(~/.local/bin/nvim --version | head -1)"
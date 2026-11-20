#!/usr/bin/env bash
# Install Neovim from official tarball to ~/.local/nvim (Linux and macOS)
set -euo pipefail

case "$(uname -s)" in
  Linux) OS="linux" ;;
  Darwin) OS="macos" ;;
  *) printf 'unsupported OS: %s\n' "$(uname -s)" >&2; exit 1 ;;
esac

ARCH="${NVIM_ARCH:-$(uname -m)}"
case "$ARCH" in
  x86_64) ARCH_DEB="x86_64" ;;
  aarch64|arm64) ARCH_DEB="arm64" ;;
  *) printf 'unsupported architecture: %s\n' "$ARCH" >&2; exit 1 ;;
esac

NAME="nvim-${OS}-${ARCH_DEB}"

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
cd "$tmp"

curl -fLO "https://github.com/neovim/neovim/releases/latest/download/${NAME}.tar.gz"
tar xzf "${NAME}.tar.gz"
mkdir -p ~/.local
rm -rf ~/.local/nvim
mv "$NAME" ~/.local/nvim
mkdir -p ~/.local/bin
ln -sf ~/.local/nvim/bin/nvim ~/.local/bin/nvim
printf 'nvim %s installed\n' "$(~/.local/bin/nvim --version | head -1)"

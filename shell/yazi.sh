# Wrapper de Yazi para bash/zsh. Se carga desde ~/.bashrc; ver install/install.sh.
#   q -> sale y deja la shell en la carpeta resaltada (si es archivo, en el cwd de Yazi)
#   Q -> sale y deja la shell en la carpeta de origen
# `q` usa el plugin yazi/plugins/quit-hovered.yazi, que escribe en $YAZI_HOVER_FILE.
y() {
  local tmp hov cwd
  tmp="$(mktemp -t "yazi-cwd.XXXXXX")"
  hov="$(mktemp -t "yazi-hover.XXXXXX")"
  YAZI_HOVER_FILE="$hov" yazi "$@" --cwd-file="$tmp"
  cwd="$(command cat -- "$hov" 2>/dev/null)"
  [ -n "$cwd" ] || cwd="$(command cat -- "$tmp" 2>/dev/null)"
  if [ -n "$cwd" ] && [ "$cwd" != "$PWD" ] && [ -d "$cwd" ]; then
    builtin cd -- "$cwd"
  fi
  rm -f -- "$tmp" "$hov"
}

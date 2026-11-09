# Wrapper de Yazi para bash/zsh: al salir con `q` deja la shell en la carpeta
# donde estaba Yazi (con `Q` sale sin cambiar). Se carga desde ~/.bashrc;
# ver install/install.sh.
y() {
  local tmp cwd
  tmp="$(mktemp -t "yazi-cwd.XXXXXX")"
  yazi "$@" --cwd-file="$tmp"
  if cwd="$(command cat -- "$tmp")" && [ -n "$cwd" ] && [ "$cwd" != "$PWD" ]; then
    builtin cd -- "$cwd"
  fi
  rm -f -- "$tmp"
}

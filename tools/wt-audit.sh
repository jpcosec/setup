#!/usr/bin/env bash
# Read-only audit of worktrees: can each one be deleted?
# Output TSV: verdict repo worktree branch reason
set -u
ANT_TOKEN=$(gh auth token --user jpruizAntonIA 2>/dev/null || true)

# Paths in use: cwd of live processes
inuse=$(for p in /proc/[0-9]*; do readlink "$p/cwd" 2>/dev/null; done | sort -u)

repos=(
  /mnt/ssd/proyectos/SLDB_1/deskops /mnt/ssd/proyectos/SLDB_1/sldb /mnt/ssd/proyectos/SLDB_1/spec2viz
  /mnt/ssd/proyectos/SLDB_1/scion /mnt/ssd/proyectos/SLDB_1/UIs/graph_ui
  /srv/repos/Chatbot_Infra /srv/repos/Governance /srv/repos/labchile_chatbots /srv/repos/shared_llm-gateway
  /home/robocop/AntonIA/repos/legacy/mepu/mepu
)

for repo in "${repos[@]}"; do
  [ -d "$repo" ] || continue
  url=$(git -C "$repo" remote get-url origin 2>/dev/null)
  slug=$(echo "$url" | sed -E 's#(git@[^:]+:|https://github.com/)##; s#\.git$##')
  tok=""; case "$slug" in heyantonia/*|jpruizAntonIA/*) tok="$ANT_TOKEN";; esac
  def=$(git -C "$repo" symbolic-ref -q --short refs/remotes/origin/HEAD 2>/dev/null || echo origin/main)
  main_wt=$(git -C "$repo" rev-parse --show-toplevel)
  git -C "$repo" worktree list --porcelain | awk '/^worktree /{w=$2} /^branch /{b=$2} /^detached/{b="(detached)"} /^$/{print w"\t"b; b=""}' |
  while IFS=$'\t' read -r wt br; do
    [ "$wt" = "$main_wt" ] && continue
    name=${wt##*/}; br=${br#refs/heads/}
    reason=""; verdict=""
    if [ ! -d "$wt" ]; then echo -e "BORRAR\t${repo##*/}\t$name\t$br\tprunable (la carpeta ya no existe)"; continue; fi
    case "$name" in *-runtime|*runtime*) echo -e "NO_TOCAR\t${repo##*/}\t$name\t$br\truntime del venv compartido"; continue;; esac
    if echo "$inuse" | grep -q "^$wt\(/\|$\)"; then echo -e "NO_TOCAR\t${repo##*/}\t$name\t$br\ten uso por un proceso vivo"; continue; fi
    dirty=$(git -C "$wt" status --porcelain 2>/dev/null | grep -v '^?? \.sldb_cache/\|^?? \.sldb/runtime/\|^?? \.deskops\.log\|^ M \.deskops\.log\|^?? runs/\|^?? desk/runtimes/' | wc -l)
    head=$(git -C "$wt" rev-parse HEAD)
    safe=""
    if git -C "$repo" merge-base --is-ancestor "$head" "$def" 2>/dev/null; then safe="HEAD ya está en $def"
    elif [ -n "$(git -C "$repo" branch -r --contains "$head" 2>/dev/null | head -1)" ]; then safe="HEAD está en una rama remota"
    elif [ "$br" != "(detached)" ] && [ -n "$slug" ]; then
      st=$(GH_TOKEN=$tok gh pr list -R "$slug" --head "$br" --state merged --json number -q '.[0].number' 2>/dev/null)
      [ -n "$st" ] && safe="PR #$st mergeado (squash)"
    fi
    if [ -z "$safe" ] && [ "$(git -C "$repo" cherry "$def" "$head" 2>/dev/null | grep -c '^+')" = "0" ]; then safe="sus commits ya están en $def (mismo patch)"; fi
    if [ -n "$safe" ] && [ "$dirty" = "0" ]; then verdict=BORRAR; reason="$safe; limpio"
    elif [ -n "$safe" ]; then verdict=REVISAR; reason="$safe, pero tiene $dirty cambios sin commitear"
    else verdict=REVISAR; reason="tiene commits que no están en $def ni en un PR mergeado; $dirty cambios sin commitear"; fi
    echo -e "$verdict\t${repo##*/}\t$name\t$br\t$reason"
  done
done

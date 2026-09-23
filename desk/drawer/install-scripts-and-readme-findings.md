# Install scripts and README findings

Status: deferred

From a review of the uncommitted working tree (`README.md`, `wezterm/keybindings.lua`, `nvim/lazy-lock.json`, plus the untracked `install/lazygit.sh` and `install/nvim.sh`). Nothing here is fixed yet.

## Real bugs

### 1. The README contradicts what `install.sh` does

`README.md:59` states:

> Backups of any pre-existing configs are left at `*.bak` next to the original target paths after running `install.sh`.

`install/install.sh:15-23` does the opposite: if the target exists it prints `refusing to overwrite existing path` and returns 1. There is no `.bak` anywhere in the repo. Anyone trusting that line may move an original config by hand believing a backup exists.

Correct wording: the installer refuses to overwrite; move conflicting files yourself before running it.

### 2. `install/lazygit.sh:9` fails on a clean machine

```bash
install lazygit ~/.local/bin/
```

`install` does not create the destination directory. `install/nvim.sh` does `mkdir -p ~/.local/bin`; `lazygit.sh` does not. It works here only because `~/.local/bin` already exists — and a bootstrap script is precisely for the case where it does not.

### 3. `install/lazygit.sh:6-7` fails silently with a useless error

```bash
LAZYGIT_VERSION=$(curl -s ".../releases/latest" | grep -Po '"tag_name": "v\K[^"]*')
curl -Lo lazygit.tar.gz ".../lazygit_${LAZYGIT_VERSION}_Linux_x86_64.tar.gz"
```

Unauthenticated GitHub API allows 60 requests/hour. When rate-limited, `curl -s` returns an error JSON, the `grep` does not match, `LAZYGIT_VERSION` is empty, and the URL becomes `lazygit__Linux_x86_64.tar.gz` → 404. Since `curl -Lo` has no `-f`, it writes the 404 page to `lazygit.tar.gz` and the visible failure is `tar: not in gzip format`, which says nothing about the real cause.

Needs `-f` on both scripts (`curl -fLo` / `curl -fLO`) and an empty-version guard.

Separately, the script mixes two sources of truth: it asks the API for the tag but downloads from `/releases/latest/download/`. If a release lands between the two calls the filename will not match. `/releases/download/v${LAZYGIT_VERSION}/...` is deterministic.

### 4. Hardcoded architecture

Both scripts assume `x86_64`. On ARM the download 404s. With `-f` added it at least fails clearly, but an explicit guard gives a better message.

### 5. The version table drifts by construction

`README.md` documents `nvim v0.12.5` and `lazygit v0.65.0`, but both scripts install `latest`. Either pin the version in the script (`LAZYGIT_VERSION="${LAZYGIT_VERSION:-0.65.0}"`) or have the column say "latest" instead of a frozen number.

### 6. The bootstrap block is not executable

Inside a ```bash fence the README shows:

```bash
nvim   # see install/nvim.sh or download from ...
```

which reads as "run `nvim`". Should be `bash install/nvim.sh` and `bash install/lazygit.sh`.

## Minor

- Both scripts `cd "$(mktemp -d)"` and never clean up, leaving temp dirs on every run. A `trap 'rm -rf "$tmp"' EXIT` covers it.
- `install/lazygit.sh` has no trailing newline.
- Neither new script is invoked or mentioned by `install/install.sh`, though that script does print hints for herdr and pi. Inconsistent with the rest of the directory.
- `wezterm/wezterm.lua:1-45` — the keybinding documentation block does not list the new `F11` binding added in `wezterm/keybindings.lua:39`. Worth adding precisely because `Ctrl+Shift+F` already exists as "Focus-100 layout (toggle fullscreen zoom)", which is pane zoom rather than window fullscreen — two similar names for different things.

## Reviewed, no action

- `wezterm/keybindings.lua:39` — the `F11`/`NONE` binding does not collide with anything existing and matches the shape of its neighbours.
- `nvim/lazy-lock.json` — plugin commit bumps only, expected `:Lazy update` noise.

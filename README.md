# Personal runtime setup

Versioned configuration for the local interactive workspace:

- **WezTerm**: terminal and outer session
- **Neovim**: human editor
- **Yazi**: filesystem navigator
- **Pi**: agentic worker
- **Herdr**: external runtime for desks, panes, processes, and agents
- **Opsys/DeskOps**: workflow and durable state

Secrets, OAuth state, sessions, caches, and machine-local overrides stay outside
this repository.

The agreed Scion/Pi execution model, fork provenance, and pending migration are
documented in [pi/README.md](pi/README.md).

## Runtime contract

Each DeskOps desk is one Herdr workspace. The file `desk/runtime.yaml` describes
the desired workspace layout without exposing Herdr pane IDs or process IDs.

The workspace identity is durable in Opsys/SLDB; Herdr IDs are runtime
references that may change after reconstruction.

## Tools installed

Managed outside this repo but expected on PATH for daily use:

| Tool | Version | Location |
|---|---|---|
| nvim | latest | `~/.local/nvim/` tarball (not snap) |
| lazygit | latest | `~/.local/bin/lazygit` (override with `LAZYGIT_VERSION`) |
| fd | 10.4.2 | `~/.pi/agent/bin/fd` |
| rg | 14.1.0 | `/usr/bin/rg` (system) |

### Neovim Mason LSPs

Installed via Mason:
- basedpyright
- eslint-lsp
- gopls
- lua-language-server
- marksman
- ruff
- rust-analyzer

## Shell

`shell/yazi.sh` defines `y`, a Yazi wrapper: quitting with `q` leaves the shell
in Yazi's last directory (`Q` quits without changing it). `install/install.sh`
adds a single line to `~/.bashrc` that sources it from this repo, so edits to the
function apply in new shells without reinstalling:

```bash
[ -f ~/setup/shell/yazi.sh ] && . ~/setup/shell/yazi.sh
```

## Bootstrap

```bash
# Create symlinks from this repo to XDG config paths,
# and source shell/yazi.sh from ~/.bashrc (idempotent; safe to rerun)
bash install/install.sh

# Additional tools (tarball-based, no snap)
bash install/nvim.sh
bash install/lazygit.sh

# Start Herdr server and initialize workspace
bash install/init-herdr.sh [--agents]
```


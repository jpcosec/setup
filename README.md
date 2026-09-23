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

## Bootstrap

```bash
# Create symlinks from this repo to XDG config paths
bash install/install.sh

# Additional tools (tarball-based, no snap)
bash install/nvim.sh
bash install/lazygit.sh

# Start Herdr server and initialize workspace
bash install/init-herdr.sh [--agents]
```


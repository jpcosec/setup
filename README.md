# Personal runtime setup

Versioned configuration for the local interactive workspace:

- WezTerm: terminal and outer session
- Neovim: human editor
- Yazi: filesystem navigator
- Pi: agentic worker
- Herdr: external runtime for desks, panes, processes, and agents
- Opsys/DeskOps: workflow and durable state

Secrets, OAuth state, sessions, caches, and machine-local overrides stay outside
this repository.

## Runtime contract

Each DeskOps desk is one Herdr workspace. The file desk/runtime.yaml describes
the desired workspace layout without exposing Herdr pane IDs or process IDs.

The workspace identity is durable in Opsys/SLDB; Herdr IDs are runtime
references that may change after reconstruction.


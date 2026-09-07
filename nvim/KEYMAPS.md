# Neovim Cheatsheet

Generated from `lua/config/keymaps.lua`.

## Notes

- Leader key: `<Space>`
- `s` and `S` are provided by Leap for fast visible jumps.
- `{` and `}` move between Aerial symbols instead of paragraphs.
- `]f` `[f` `]c` `[c` `]a` `[a` come from Tree-sitter textobjects.

## Code

| Mode | Key | Action |
| --- | --- | --- |
| `n` | `<leader>cf` | Format buffer |

## Files

| Mode | Key | Action |
| --- | --- | --- |
| `n` | `<leader>fE` | Reveal current file in explorer |
| `n` | `<leader>fF` | Find all files |
| `n` | `<leader>fb` | Find buffers |
| `n` | `<leader>fe` | Toggle file explorer |
| `n` | `<leader>ff` | Find project files |

## Help

| Mode | Key | Action |
| --- | --- | --- |
| `n` | `<C-p>` | Open command palette |
| `n` | `<leader>hc` | Open cheatsheet |
| `n` | `<leader>hk` | Browse keymaps |
| `n` | `<leader>hp` | Open command palette |

## Navigation

| Mode | Key | Action |
| --- | --- | --- |
| `n` | `N` | Previous search result |
| `n,x,o` | `S` | Leap across windows |
| `n` | `[a` | Previous argument |
| `n` | `[c` | Previous class |
| `n` | `[f` | Previous function |
| `n` | `]a` | Next argument |
| `n` | `]c` | Next class |
| `n` | `]f` | Next function |
| `n` | `n` | Next search result |
| `n,x,o` | `s` | Leap forward |
| `n` | `{` | Previous symbol |
| `n` | `}` | Next symbol |

## Search

| Mode | Key | Action |
| --- | --- | --- |
| `n` | `<leader>sg` | Search project text |
| `n` | `<leader>sh` | Search help tags |

## UI

| Mode | Key | Action |
| --- | --- | --- |
| `n` | `<leader>un` | Toggle line numbers |
| `n` | `<leader>uo` | Toggle outline |
| `n` | `<leader>uw` | Toggle line wrap |

## Windows

| Mode | Key | Action |
| --- | --- | --- |
| `n` | `<C-h>` | Focus left split |
| `n` | `<C-j>` | Focus lower split |
| `n` | `<C-k>` | Focus upper split |
| `n` | `<C-l>` | Focus right split |


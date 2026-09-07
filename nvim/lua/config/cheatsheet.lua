local M = {}

local function mode_label(mode)
  if type(mode) == "table" then
    return table.concat(mode, ",")
  end
  return mode
end

local function sorted_groups(keymaps)
  local grouped = {}
  local order = {}

  for _, spec in ipairs(keymaps) do
    if not grouped[spec.group] then
      grouped[spec.group] = {}
      table.insert(order, spec.group)
    end
    table.insert(grouped[spec.group], spec)
  end

  table.sort(order)
  for _, group in ipairs(order) do
    table.sort(grouped[group], function(a, b)
      return a.lhs < b.lhs
    end)
  end

  return order, grouped
end

local function render_lines(keymaps)
  local order, grouped = sorted_groups(keymaps)
  local lines = {
    "# Neovim Cheatsheet",
    "",
    "Generated from `lua/config/keymaps.lua`.",
    "",
    "## Notes",
    "",
    "- Leader key: `<Space>`",
    "- `s` and `S` are provided by Leap for fast visible jumps.",
    "- `{` and `}` move between Aerial symbols instead of paragraphs.",
    "- `]f` `[f` `]c` `[c` `]a` `[a` come from Tree-sitter textobjects.",
    "",
  }

  for _, group in ipairs(order) do
    table.insert(lines, "## " .. group)
    table.insert(lines, "")
    table.insert(lines, "| Mode | Key | Action |")
    table.insert(lines, "| --- | --- | --- |")
    for _, spec in ipairs(grouped[group]) do
      table.insert(lines, string.format("| `%s` | `%s` | %s |", mode_label(spec.mode), spec.lhs, spec.desc))
    end
    table.insert(lines, "")
  end

  return lines
end

function M.open(keymaps)
  local lines = render_lines(keymaps)
  local buf = vim.api.nvim_create_buf(false, true)

  vim.api.nvim_buf_set_lines(buf, 0, -1, false, lines)
  vim.bo[buf].bufhidden = "wipe"
  vim.bo[buf].buftype = "nofile"
  vim.bo[buf].filetype = "markdown"
  vim.bo[buf].modifiable = false

  vim.cmd("tabnew")
  vim.api.nvim_win_set_buf(0, buf)
  vim.api.nvim_buf_set_name(buf, "Neovim Cheatsheet")
end

function M.write_file(keymaps)
  local path = vim.fn.stdpath("config") .. "/KEYMAPS.md"
  local lines = render_lines(keymaps)
  local existing = vim.fn.filereadable(path) == 1 and vim.fn.readfile(path) or nil

  if existing == nil or not vim.deep_equal(existing, lines) then
    vim.fn.writefile(lines, path)
  end
end

function M.setup(keymaps)
  vim.api.nvim_create_user_command("NvimCheatsheet", function()
    M.open(keymaps)
  end, { desc = "Open generated Neovim cheatsheet" })

  M.write_file(keymaps)
end

return M

local cheatsheet = require("config.cheatsheet")

local function map(spec)
  if spec.apply == false then
    return
  end
  local opts = { desc = spec.desc, silent = true }
  if spec.expr then
    opts.expr = true
  end
  vim.keymap.set(spec.mode, spec.lhs, spec.rhs, opts)
end

local function git_files_or_find_files()
  local builtin = require("telescope.builtin")
  local ok = pcall(builtin.git_files)
  if not ok then
    builtin.find_files()
  end
end

local function toggle_numbers()
  local next_number = not vim.opt.number:get()
  vim.opt.number = next_number
  vim.opt.relativenumber = next_number
end

local function toggle_wrap()
  vim.opt.wrap = not vim.opt.wrap:get()
  vim.notify("wrap=" .. tostring(vim.opt.wrap:get()))
end

local keymaps = {
  { group = "Help", mode = "n", lhs = "<leader>hp", rhs = "<cmd>Legendary<cr>", desc = "Open command palette" },
  { group = "Help", mode = "n", lhs = "<leader>hk", rhs = "<cmd>Legendary keymaps<cr>", desc = "Browse keymaps" },
  { group = "Help", mode = "n", lhs = "<leader>hc", rhs = "<cmd>NvimCheatsheet<cr>", desc = "Open cheatsheet" },
  { group = "Help", mode = "n", lhs = "<C-p>", rhs = "<cmd>Legendary<cr>", desc = "Open command palette" },

  { group = "Files", mode = "n", lhs = "<leader>ff", rhs = git_files_or_find_files, desc = "Find project files" },
  { group = "Files", mode = "n", lhs = "<leader>fF", rhs = function() require("telescope.builtin").find_files() end, desc = "Find all files" },
  { group = "Files", mode = "n", lhs = "<leader>fb", rhs = function() require("telescope.builtin").buffers() end, desc = "Find buffers" },
  { group = "Files", mode = "n", lhs = "<leader>fe", rhs = "<cmd>NvimTreeToggle<cr>", desc = "Toggle file explorer" },
  { group = "Files", mode = "n", lhs = "<leader>fE", rhs = "<cmd>NvimTreeFindFile<cr>", desc = "Reveal current file in explorer" },

  { group = "Search", mode = "n", lhs = "<leader>sg", rhs = function() require("telescope.builtin").live_grep() end, desc = "Search project text" },
  { group = "Search", mode = "n", lhs = "<leader>sh", rhs = function() require("telescope.builtin").help_tags() end, desc = "Search help tags" },

  { group = "Code", mode = "n", lhs = "<leader>cf", rhs = function() require("conform").format({ async = true, lsp_format = "fallback" }) end, desc = "Format buffer" },

  { group = "UI", mode = "n", lhs = "<leader>uo", rhs = "<cmd>AerialToggle<cr>", desc = "Toggle outline" },
  { group = "UI", mode = "n", lhs = "<leader>un", rhs = toggle_numbers, desc = "Toggle line numbers" },
  { group = "UI", mode = "n", lhs = "<leader>uw", rhs = toggle_wrap, desc = "Toggle line wrap" },

  { group = "Windows", mode = "n", lhs = "<C-h>", rhs = "<C-w><C-h>", desc = "Focus left split" },
  { group = "Windows", mode = "n", lhs = "<C-j>", rhs = "<C-w><C-j>", desc = "Focus lower split" },
  { group = "Windows", mode = "n", lhs = "<C-k>", rhs = "<C-w><C-k>", desc = "Focus upper split" },
  { group = "Windows", mode = "n", lhs = "<C-l>", rhs = "<C-w><C-l>", desc = "Focus right split" },

  { group = "Navigation", mode = "n", lhs = "n", rhs = function() return vim.v.searchforward == 1 and "n" or "N" end, desc = "Next search result" , expr = true },
  { group = "Navigation", mode = "n", lhs = "N", rhs = function() return vim.v.searchforward == 1 and "N" or "n" end, desc = "Previous search result", expr = true },
  { group = "Navigation", mode = "n", lhs = "{", rhs = "<cmd>AerialPrev<cr>", desc = "Previous symbol" },
  { group = "Navigation", mode = "n", lhs = "}", rhs = "<cmd>AerialNext<cr>", desc = "Next symbol" },
  { group = "Navigation", mode = "n", lhs = "]f", desc = "Next function", apply = false },
  { group = "Navigation", mode = "n", lhs = "[f", desc = "Previous function", apply = false },
  { group = "Navigation", mode = "n", lhs = "]c", desc = "Next class", apply = false },
  { group = "Navigation", mode = "n", lhs = "[c", desc = "Previous class", apply = false },
  { group = "Navigation", mode = "n", lhs = "]a", desc = "Next argument", apply = false },
  { group = "Navigation", mode = "n", lhs = "[a", desc = "Previous argument", apply = false },
  { group = "Navigation", mode = { "n", "x", "o" }, lhs = "s", desc = "Leap forward", apply = false },
  { group = "Navigation", mode = { "n", "x", "o" }, lhs = "S", desc = "Leap across windows", apply = false },
}

for _, spec in ipairs(keymaps) do
  map(spec)
end

cheatsheet.setup(keymaps)

return keymaps

local opt = vim.opt

opt.hlsearch = true
opt.number = true
opt.mouse = "a"
opt.showmode = false
opt.spelllang = "en_gb"
opt.title = true
opt.titlestring = "nvim"
opt.termguicolors = true
opt.background = "dark"
opt.cursorline = true
opt.cursorcolumn = true
opt.signcolumn = "yes"
opt.wrap = false
opt.sidescrolloff = 8
opt.scrolloff = 8
opt.tabstop = 2
opt.shiftwidth = 2
opt.expandtab = true
opt.autoindent = true
opt.ignorecase = true
opt.smartcase = true
opt.gdefault = true
opt.splitright = true
opt.splitbelow = true
opt.foldmethod = "expr"
opt.foldexpr = "v:lua.vim.treesitter.foldexpr()"
opt.foldlevel = 99

vim.g.mapleader = " "
vim.g.loaded_netrw = 1
vim.g.loaded_netrwPlugin = 1

opt.clipboard:append({ "unnamed", "unnamedplus" })

local undodir = vim.fn.stdpath("cache") .. "/undo"
vim.fn.mkdir(undodir, "p")
opt.undodir = undodir
opt.undofile = true

if vim.lsp.inlay_hint and vim.lsp.inlay_hint.enable then
  vim.lsp.inlay_hint.enable(true)
end

return {
  {
    "mrjones2014/legendary.nvim",
    cmd = {
      "Legendary",
      "LegendaryRepeat",
    },
    dependencies = {
      "stevearc/dressing.nvim",
    },
    config = function()
      require("legendary").setup({
        extensions = {
          lazy_nvim = true,
        },
      })
    end,
  },
  {
    "stevearc/dressing.nvim",
    lazy = true,
  },
}

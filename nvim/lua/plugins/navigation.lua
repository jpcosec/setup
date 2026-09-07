return {
  {
    "ggandor/leap.nvim",
    event = "VeryLazy",
    config = function()
      require("leap").add_default_mappings()
    end,
  },
  {
    "AntonVanAssche/md-headers.nvim",
    ft = "markdown",
    config = function()
      local ok, md_headers = pcall(require, "md-headers")
      if ok and md_headers.setup then
        md_headers.setup()
      end
    end,
  },
}

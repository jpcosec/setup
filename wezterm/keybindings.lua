local wezterm = require("wezterm")
local act = wezterm.action

local M = {}

M.keys = {
  -- Splits
  { key = "Enter", mods = "CTRL|SHIFT", action = act.SplitVertical { domain = "CurrentPaneDomain" }, desc = "Split pane vertically" },
  { key = "Enter", mods = "CTRL|ALT", action = act.SplitHorizontal { domain = "CurrentPaneDomain" }, desc = "Split pane horizontally" },

  -- Tabs
  { key = "t", mods = "CTRL", action = act.SpawnTab "CurrentPaneDomain", desc = "Open new tab" },
  { key = "w", mods = "CTRL", action = act.CloseCurrentTab { confirm = true }, desc = "Close current tab" },
  { key = "`", mods = "CTRL", action = act.ShowLauncher, desc = "Open WezTerm launcher" },

  -- Tab switching
  { key = "1", mods = "ALT", action = act.ActivateTab(0), desc = "Switch to tab 1" },
  { key = "2", mods = "ALT", action = act.ActivateTab(1), desc = "Switch to tab 2" },
  { key = "3", mods = "ALT", action = act.ActivateTab(2), desc = "Switch to tab 3" },
  { key = "4", mods = "ALT", action = act.ActivateTab(3), desc = "Switch to tab 4" },
  { key = "5", mods = "ALT", action = act.ActivateTab(4), desc = "Switch to tab 5" },
  { key = "6", mods = "ALT", action = act.ActivateTab(5), desc = "Switch to tab 6" },
  { key = "7", mods = "ALT", action = act.ActivateTab(6), desc = "Switch to tab 7" },
  { key = "8", mods = "ALT", action = act.ActivateTab(7), desc = "Switch to tab 8" },
  { key = "9", mods = "ALT", action = act.ActivateTab(8), desc = "Switch to tab 9" },

  -- Pane and tab management
  { key = "h", mods = "CTRL", action = act.EmitEvent("hide-current-pane"), desc = "Hide current pane" },
  { key = "o", mods = "CTRL|SHIFT", action = act.EmitEvent("show-hidden-panes"), desc = "Show hidden panes" },
  { key = "s", mods = "CTRL|SHIFT", action = act.PaneSelect { mode = "SwapWithActive" }, desc = "Swap pane with selected pane" },
  { key = "b", mods = "CTRL|SHIFT", action = act.EmitEvent("layout-base"), desc = "Equalize panes" },
  { key = "m", mods = "CTRL|SHIFT", action = act.EmitEvent("layout-focus70"), desc = "Focus layout 70/30" },
  { key = "f", mods = "CTRL|SHIFT", action = act.EmitEvent("layout-focus100"), desc = "Toggle pane zoom" },
  { key = "t", mods = "CTRL|SHIFT", action = act.EmitEvent("rename-current-tab"), desc = "Rename current tab" },
  { key = "p", mods = "CTRL|SHIFT", action = act.EmitEvent("rename-current-pane"), desc = "Rename current pane" },
  { key = "d", mods = "CTRL|SHIFT", action = act.EmitEvent("move-tab-to-new-window"), desc = "Move current tab to a new window" },

  -- Move pane to predefined tabs
  { key = "1", mods = "CTRL|SHIFT", action = act.EmitEvent("move-pane-to-tab-1"), desc = "Move pane to Main tab" },
  { key = "2", mods = "CTRL|SHIFT", action = act.EmitEvent("move-pane-to-tab-2"), desc = "Move pane to Logs tab" },
  { key = "3", mods = "CTRL|SHIFT", action = act.EmitEvent("move-pane-to-tab-3"), desc = "Move pane to DB tab" },
  { key = "4", mods = "CTRL|SHIFT", action = act.EmitEvent("move-pane-to-tab-4"), desc = "Move pane to API tab" },
  { key = "5", mods = "CTRL|SHIFT", action = act.EmitEvent("move-pane-to-tab-5"), desc = "Move pane to Tests tab" },
  { key = "6", mods = "CTRL|SHIFT", action = act.EmitEvent("move-pane-to-tab-6"), desc = "Move pane to Scratch tab" },
  { key = "7", mods = "CTRL|SHIFT", action = act.EmitEvent("move-pane-to-tab-7"), desc = "Move pane to Utils tab" },
  { key = "8", mods = "CTRL|SHIFT", action = act.EmitEvent("move-pane-to-tab-8"), desc = "Move pane to Monitor tab" },
  { key = "9", mods = "CTRL|SHIFT", action = act.EmitEvent("move-pane-to-tab-9"), desc = "Move pane to Other tab" },
}

M.plugins = {
  command_picker = {
    key = "p",
    mods = "CTRL|ALT",
    title = "Command Palette",
    include_defaults = true,
    include_key_tables = false,
  },
  theme_rotator = {
    next_theme_key = "]",
    next_theme_mods = "CTRL|ALT",
    prev_theme_key = "[",
    prev_theme_mods = "CTRL|ALT",
    random_theme_key = "r",
    random_theme_mods = "CTRL|ALT",
    default_theme_key = "d",
    default_theme_mods = "CTRL|ALT",
  },
}

return M

--[[
═══════════════════════════════════════════════════════════════════════════════
🧠 WezTerm Keybindings & Behaviors Explained
═══════════════════════════════════════════════════════════════════════════════

🔹 PANE MANAGEMENT
──────────────────────────────────────────────────────────────────────────────
  Ctrl + H              → Hide current pane (moves to "Ocultos" tab)
  Ctrl + Shift + O      → Show hidden panes (restore from "Ocultos")
  Ctrl + Shift + S      → Swap pane with another (interactive selection)
  Ctrl + Shift + 1-9    → Move current pane to specific tab
                          (1=Main, 2=Logs, 3=DB, 4=API, 5=Tests,
                           6=Scratch, 7=Utils, 8=Monitor, 9=Other)

🔹 TAB MANAGEMENT
──────────────────────────────────────────────────────────────────────────────
  Alt + 1-9             → Switch to tab #1-9
  Ctrl + Shift + T      → Rename current tab
  Ctrl + Shift + P      → Rename current pane

🔹 LAYOUT CONTROL
──────────────────────────────────────────────────────────────────────────────
  Ctrl + Shift + B      → Base layout (distribute panes evenly 50/50)
  Ctrl + Shift + M      → Focus-70 layout (active pane 70%, others 30%)
  Ctrl + Shift + F      → Focus-100 layout (toggle fullscreen zoom)

🔹 SPLITS & NAVIGATION
──────────────────────────────────────────────────────────────────────────────
  Ctrl + Shift + Enter  → Split pane vertically (top/bottom)
  Ctrl + Alt + Enter    → Split pane horizontally (side-by-side)
  Ctrl + T              → Open new tab
  Ctrl + W              → Close current tab (with confirmation)
  Ctrl + `              → Open launcher (tabs, workspaces, etc.)

💡 DESIGN NOTES
──────────────────────────────────────────────────────────────────────────────
  • Hidden panes stay alive (just moved to different tab)
  • Tabs and panes can be renamed anytime
  • New tabs auto-source .wezterm-init.sh if it exists
  • Ctrl+Shift used for custom commands (avoids system conflicts)
  • IME and composed-key inputs disabled for Alt/Ctrl+Alt

═══════════════════════════════════════════════════════════════════════════════
]]--

local wezterm = require 'wezterm'
local act = wezterm.action
local cmdpicker = wezterm.plugin.require('https://github.com/abidibo/wezterm-cmdpicker')
local theme_rotator = wezterm.plugin.require('https://github.com/koh-sh/wezterm-theme-rotator')
local keybindings = dofile(os.getenv("HOME") .. "/.config/wezterm/keybindings.lua")

-- --- Global Options ---
local config = {
  color_scheme = "Builtin Dark",
  font_size = 13.0,
  use_fancy_tab_bar = true,
  hide_tab_bar_if_only_one_tab = false,
  scrollback_lines = 20000,
  window_background_opacity = 0.95,
  check_for_updates = false,

  -- evita que AltGr o IME interfieran
  use_ime = false,
  send_composed_key_when_left_alt_is_pressed = false,
  send_composed_key_when_right_alt_is_pressed = false,
}

-- === Helpers ===
local function basename(path)
  if not path then return "" end
  return path:match("([^/]+)$") or path
end

local function git_branch(cwd)
  if not cwd then return "" end
  local ok, success, stdout = pcall(function()
    return wezterm.run_child_process({
      "bash", "-lc",
      "cd " .. wezterm.shell_quote_arg(cwd) .. " && git rev-parse --abbrev-ref HEAD 2>/dev/null"
    })
  end)
  if ok and success and stdout and #stdout > 0 then
    return stdout:gsub("%s+$", "")
  end
  return ""
end

local function tab_title(tab_info)
  local cwd = tab_info.active_pane.current_working_dir and tab_info.active_pane.current_working_dir.file_path or ""
  local proj = basename(cwd)
  local branch = git_branch(cwd)
  if branch ~= "" then
    return string.format("%s [%s]", proj, branch)
  elseif proj ~= "" then
    return proj
  else
    return "shell"
  end
end

wezterm.on("format-tab-title", function(tab, tabs, panes, config, hover, max_width)
  return tab_title(tab)
end)

-- === Pane & Tab Management ===
local hidden_tab_name = "Ocultos"

local function get_or_create_tab(window, name)
  local mux_win = window:mux_window()
  for _, t in ipairs(mux_win:tabs()) do
    if t:get_title() == name then
      return t
    end
  end
  local new_tab = mux_win:spawn_tab{}
  new_tab:set_title(name)
  return new_tab
end

wezterm.on("hide-current-pane", function(window, pane)
  local hidden_tab = get_or_create_tab(window, hidden_tab_name)
  pane:move_to_tab(hidden_tab)
  window:toast_notification("WezTerm", "👻 Pane movido a tab 'Ocultos'", nil, 1500)
end)

wezterm.on("show-hidden-panes", function(window, pane)
  local mux_win = window:mux_window()
  local hidden
  for _, t in ipairs(mux_win:tabs()) do
    if t:get_title() == hidden_tab_name then
      hidden = t
      break
    end
  end
  if not hidden then
    window:toast_notification("WezTerm", "⚠️ No hay panes ocultos", nil, 1500)
    return
  end
  local target_tab = mux_win:active_tab()
  for _, p in ipairs(hidden:panes()) do
    p:move_to_tab(target_tab)
  end
  window:toast_notification("WezTerm", "👀 Panes restaurados", nil, 1500)
end)

local tab_map = {
  ["1"] = "Main",
  ["2"] = "Logs",
  ["3"] = "DB",
  ["4"] = "API",
  ["5"] = "Tests",
  ["6"] = "Scratch",
  ["7"] = "Utils",
  ["8"] = "Monitor",
  ["9"] = "Other",
}

for key, name in pairs(tab_map) do
  wezterm.on("move-pane-to-tab-" .. key, function(window, pane)
    local tab = get_or_create_tab(window, name)
    pane:move_to_tab(tab)
    window:toast_notification("WezTerm", "🧩 Pane movido a tab '" .. name .. "'", nil, 1500)
  end)
end

wezterm.on("rename-current-tab", function(window, pane)
  window:perform_action(
    wezterm.action.PromptInputLine{
      description = "Nuevo nombre para este tab:",
      action = wezterm.action_callback(function(_, _, line)
        if line then
          window:mux_window():active_tab():set_title(line)
        end
      end)
    },
    pane
  )
end)

wezterm.on("rename-current-pane", function(window, pane)
  window:perform_action(
    wezterm.action.PromptInputLine{
      description = "Nuevo nombre para este pane:",
      action = wezterm.action_callback(function(_, _, line)
        if line then
          pane:rename_pane(line)
        end
      end)
    },
    pane
  )
end)

wezterm.on("move-tab-to-new-window", function(window, pane)
  local ok, err = pcall(function()
    local tab = window:mux_window():active_tab()
    tab:move_to_new_window()
  end)

  if not ok then
    window:toast_notification("WezTerm", "⚠️ Error moviendo tab: " .. tostring(err), nil, 3000)
  end
end)

-- === Layouts ===
wezterm.on("layout-base", function(window, pane)
  window:perform_action(wezterm.action.EqualizePanes, pane)
  window:toast_notification("WezTerm", "🔄 Vista base (50/50)", nil, 1500)
end)

wezterm.on("layout-focus70", function(window, pane)
  local tab = window:mux_window():active_tab()
  local tab_id = tab:tab_id()
  local active_id = pane:pane_id()

  -- Get all panes via CLI
  local success, stdout, stderr = wezterm.run_child_process({"wezterm", "cli", "list", "--format", "json"})
  if not success then
    window:toast_notification("WezTerm", "⚠️ Error listing panes", nil, 1500)
    return
  end

  -- Parse JSON
  local all_panes = wezterm.json_parse(stdout)
  if not all_panes then
    window:toast_notification("WezTerm", "⚠️ Error parsing panes", nil, 1500)
    return
  end

  -- Filter panes in current tab, excluding active pane
  local other_panes = {}
  for _, p in ipairs(all_panes) do
    if p.tab_id == tab_id and p.pane_id ~= active_id then
      table.insert(other_panes, p.pane_id)
    end
  end

  if #other_panes == 0 then
    -- No other panes, just split 70/30
    window:perform_action(act.SplitPane{direction="Right", size={Percent=30}}, pane)
  else
    -- Create left pane (30%) first
    local result = wezterm.run_child_process({
      "wezterm", "cli", "split-pane",
      "--pane-id", tostring(active_id),
      "--left",
      "--percent", "30"
    })

    if result then
      local left_pane_id = result:gsub("%s+", "")

      -- Move all other panes to the left pane by stacking them
      for _, other_id in ipairs(other_panes) do
        wezterm.run_child_process({
          "wezterm", "cli", "split-pane",
          "--pane-id", left_pane_id,
          "--bottom",
          "--move-pane-id", tostring(other_id)
        })
      end

      -- Reactivate the original pane (right side)
      wezterm.run_child_process({
        "wezterm", "cli", "activate-pane",
        "--pane-id", tostring(active_id)
      })
    end
  end

  window:toast_notification("WezTerm", "🪟 Vista focus 70", nil, 1500)
end)

wezterm.on("layout-focus100", function(window, pane)
  if not pane:is_zoomed() then
    window:perform_action(wezterm.action.TogglePaneZoomState, pane)
    window:toast_notification("WezTerm", "🖥️ Vista 100%", nil, 1500)
  else
    window:perform_action(wezterm.action.TogglePaneZoomState, pane)
    window:toast_notification("WezTerm", "🔙 Vista base", nil, 1500)
  end
end)

-- === Keys ===
cmdpicker.add_keys(config, keybindings.keys)
theme_rotator.apply_to_config(config, keybindings.plugins.theme_rotator)
cmdpicker.apply_to_config(config, keybindings.plugins.command_picker)

-- === Default shell ===
config.default_prog = {
  "bash", "-c",
  [[
    RCFILE=$(mktemp)
    cat > "$RCFILE" << 'RCEOF'
[ -f ~/.bashrc ] && . ~/.bashrc
if [ -f .wezterm-init.sh ]; then . ./.wezterm-init.sh; fi
RCEOF
    exec bash --rcfile "$RCFILE"
  ]]
}

return config

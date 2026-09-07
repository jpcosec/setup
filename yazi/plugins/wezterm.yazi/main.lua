local get_cwd = ya.sync(function()
	return tostring(cx.active.current.cwd)
end)

local function entry()
	local cwd = get_cwd()
	-- Abre en una nueva ventana:
	local command = 'wezterm cli spawn --new-window --cwd "' .. cwd .. '"'
	os.execute(command)
end

return { entry = entry }

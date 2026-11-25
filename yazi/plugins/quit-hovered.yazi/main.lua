--- @sync entry
--- Sale de Yazi dejando en $YAZI_HOVER_FILE la carpeta resaltada (si lo
--- resaltado es un directorio). El wrapper `y` (shell/yazi.sh) la prefiere
--- sobre el cwd. Si lo resaltado es un archivo, se sale con el cwd normal.
local function hovered_dir()
	local h = cx.active.current.hovered
	if h and h.cha.is_dir then
		return tostring(h.url)
	end
end

return {
	entry = function()
		local dir = hovered_dir()
		local out = os.getenv("YAZI_HOVER_FILE")
		if dir and out and out ~= "" then
			local fh = io.open(out, "w")
			if fh then
				fh:write(dir)
				fh:close()
			end
		end
		ya.emit("quit", {})
	end,
}

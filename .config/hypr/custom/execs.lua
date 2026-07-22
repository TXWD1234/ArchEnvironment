-- This file will not be overwritten across dots-hyprland updates.
-- The file name is for the sake of organization and does not matter
-- See the corresponding files in ~/.config/hypr/hyprland for examples

hl.on("hyprland.start", function ()
	hl.exec_cmd("fcitx5")
	hl.exec_cmd("/home/TX_Jerry/.config/hypr/custom/scripts/autostart.sh")
	hl.exec_cmd("dbus-update-activation-environment --systemd SSH_AUTH_SOCK GNOME_KEYRING_CONTROL")
	hl.exec_cmd("sleep 2 && hyprctl reload")

	hl.exec_cmd("systemctl --user import-environment WAYLAND_DISPLAY XDG_CURRENT_DESKTOP")
	hl.exec_cmd("systemctl --user restart xdg-desktop-portal")
	hl.exec_cmd("/usr/lib/xdg-desktop-portal --replace &")
end)

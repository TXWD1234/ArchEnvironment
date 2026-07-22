## delete chrome lock files to make it don't died each time reboot
rm -f ~/.config/google-chrome/Default/Singleton*
## automaticly unlock the google keyring thing
eval $(/bin/gnome-keyring-daemon --start --components=secrets,pkcs11)
export SSH_AUTH_SOCK

# google-chrome-stable

# give access to windows files
sudo mount /dev/nvme0n1p3 /mnt/windows

## turn on bluetooth
rfkill unblock all
bluetoothctl
power on
agent on
default-agent
scan ons

# fix monitors
# hyprctl reload
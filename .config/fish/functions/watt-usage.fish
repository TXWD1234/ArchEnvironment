function watt-usage --wraps='watch -n1 cat /sys/class/power_supply/BAT0/power_now' --description 'alias watt-usage watch -n1 cat /sys/class/power_supply/BAT0/power_now'
    watch -n1 cat /sys/class/power_supply/BAT0/power_now $argv
end

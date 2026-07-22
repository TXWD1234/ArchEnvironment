function screen-off --wraps='sleep 1 && hyprctl dispatch dpms off' --description 'alias screen-off sleep 1 && hyprctl dispatch dpms off'
    sleep 1 && hyprctl dispatch dpms off $argv
end

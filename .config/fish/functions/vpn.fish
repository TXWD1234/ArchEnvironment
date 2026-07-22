function vpn --wraps='sudo openvpn --config ~/Documents/vpn.ovpn' --description 'alias vpn sudo openvpn --config ~/Documents/vpn.ovpn'
    sudo openvpn --config ~/Documents/vpn.ovpn $argv
end

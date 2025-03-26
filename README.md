# How to use mihomo on linuxx


1. Install mihomo and Created systemd service

https://github.com/MetaCubeX/mihomo

2. Transform your subscription url to config.toml

python3 subscribe.py url

3. Copy output.toml to /etc/mihomo/config.toml

4. Copy mihomo.service to /etc/systemd/system/mihomo.service

sudo systemctl enable mihomo

sudo systemctl start mihomo

sudo systemctl status mihomo

5. Visit the admin panel (use root start mihomo can use tun mode )
https://metacubex.github.io/metacubexd


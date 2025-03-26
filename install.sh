#!/bin/bash
if [[ -f "/usr/bin/mihomo" ]]; then
    echo "mihomo 已安装，跳过安装步骤。"
    exit
else
    echo "请手动安装建议deb"
fi

read -rp "请输入订阅链接 URL: " subscribe_url
python3 subscribe.py "$subscribe_url"
mkdir -p /etc/mihomo
cp output.toml /etc/mihomo/config.toml
echo "config.toml 生成完成。"

if [[ -f "/etc/systemd/system/mihomo.service" ]]; then
    echo "mihomo.service 已存在，跳过复制步骤。"
else
    # 复制 mihomo.service
    echo "正在设置 mihomo.service..."
    cp mihomo.service /etc/systemd/system/mihomo.service
    echo "mihomo.service 设置完成。"
fi

# 启用并启动 mihomo 服务
echo "正在启用并启动 mihomo 服务..."
sudo systemctl enable mihomo
sudo systemctl start mihomo
sudo systemctl status mihomo

# 提示访问管理面板
echo "mihomo 已启动。"
echo "请访问管理面板: https://metacubex.github.io/metacubexd"

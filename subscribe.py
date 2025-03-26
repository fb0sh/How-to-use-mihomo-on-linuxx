import sys
import json
import base64
import requests
import yaml
# https://172.247.189.143/api/v1/client/subscribe?token=f4c2e08a99e6bdff5d4ccc1dc8b8ba12


def vmesss2clash(vmess):
    vmess = base64.b64decode(vmess[8:]).decode()
    vmess = json.loads(vmess)
    # { name: 🇭🇰香港01, type: vmess, server: hk01.zzxs.one, port: 49010, uuid: 2cc68853-bec1-4355-b133-e5f236a53539, alterId: 0, cipher: auto, udp: true }
    vmess = {
        "name": vmess["ps"],
        "type": "vmess",
        "server": vmess["add"],
        "port": int(vmess["port"]),
        "uuid": vmess["id"],
        "alterId": int(vmess["aid"]),
        "cipher": "auto",
        "udp": True,
    }
    return vmess


def get_vmesss(url):
    res = requests.get(url)
    print(res.headers)
    content = base64.b64decode(res.content).decode()
    vmesss = content.splitlines()
    return vmesss


def main():
    if len(sys.argv) > 1:
        user_input = sys.argv[1]
    else:
        user_input = input("订阅链接: ")

    vmesss = get_vmesss(user_input)
    clashs = [vmesss2clash(vmess) for vmess in vmesss]

    # 读取 YAML 文件
    with open("config.yml", "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    with open("output.yaml", "w", encoding="utf-8") as file:
        yaml.safe_dump(data, file, default_flow_style=False, allow_unicode=True)
        yaml_content = "proxies:\n"
        for proxy in clashs:
            yaml_content += f"    - {str(proxy).replace("'", '')}\n"
        file.write(yaml_content)
        names = [
            f"'{vmess['name']}'" if "|" in vmess["name"] else vmess["name"]
            for vmess in clashs
        ]
        yaml_content = "proxy-groups:\n"
        yaml_content += "    - { name: PROXY, type: select, proxies: ["
        yaml_content += ",".join(names)
        yaml_content += "] }\n"
        yaml_content += "    - { name: 自动选择, type: url-test, proxies: ["
        yaml_content += ",".join(names)
        yaml_content += (
            "], url: 'http://www.gstatic.com/generate_204', interval: 86400 }\n"
        )
        yaml_content += "    - { name: 故障转移, type: fallback, proxies: ["
        yaml_content += ",".join(names)
        yaml_content += (
            "], url: 'http://www.gstatic.com/generate_204', interval: 7200 }\n"
        )
        file.write(yaml_content)
    print("Generate output.yml")


if __name__ == "__main__":
    main()

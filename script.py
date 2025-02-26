import requests
import yaml
import struct

# Список ссылок на файлы .yaml
urls = [
    "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/refs/heads/meta/geo/geosite/youtube.yaml",
    "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/refs/heads/meta/geo/geosite/facebook.yaml",
    "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/refs/heads/meta/geo/geosite/google.yaml",
    "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/refs/heads/meta/geo/geosite/microsoft.yaml",
    "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/refs/heads/meta/geo/geosite/openai.yaml",
    "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/refs/heads/meta/geo/geosite/tiktok.yaml",
    "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/refs/heads/meta/geo/geosite/trello.yaml",
    "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/refs/heads/meta/geo/geosite/perplexity.yaml",
    "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/refs/heads/meta/geo/geosite/google-gemini.yaml",
    "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/refs/heads/meta/geo/geosite/discord.yaml",
    "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/refs/heads/meta/geo/geosite/anthropic.yaml",
    "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/refs/heads/meta/geo/geosite/google-deepmind.yaml",
    "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/refs/heads/meta/geo/geosite/twitter.yaml",
    "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/refs/heads/meta/geo/geosite/spotify.yaml",
    "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/refs/heads/meta/geo/geosite/notion.yaml",
    "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/refs/heads/meta/geo/geosite/github.yaml",
    "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/refs/heads/meta/geo/geosite/telegram.yaml",
    "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/refs/heads/meta/geo/geosite/whatsapp.yaml",
    "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/refs/heads/meta/geo/geosite/instagram.yaml",
    "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/refs/heads/meta/geo/geosite/bytedance.yaml",
    "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/refs/heads/meta/geo/geosite/category-porn.yaml"
]

all_domains = set()

# Скачиваем YAML-файлы и извлекаем домены
for url in urls:
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = yaml.safe_load(response.text)
        
        if "rules" in data:
            for entry in data["rules"]:
                if isinstance(entry, str):
                    all_domains.add(entry)
                elif isinstance(entry, dict) and "domain" in entry:
                    all_domains.add(entry["domain"])
    except Exception as e:
        print(f"Ошибка при загрузке {url}: {e}")

# Создаем geosite.dat в бинарном формате
with open("geosite.dat", "wb") as f:
    for domain in sorted(all_domains):
        encoded_domain = domain.encode("utf-8")
        f.write(struct.pack(">H", len(encoded_domain)))
        f.write(encoded_domain)

print(f"Файл geosite.dat создан! ({len(all_domains)} доменов)")

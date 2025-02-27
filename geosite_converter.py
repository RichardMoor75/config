import os
import yaml
import requests
from urllib.parse import urlparse
import shutil
import sys

# Список исходных YAML-файлов
URLS = [
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

def check_dependencies():
    """Проверка наличия необходимых утилит"""
    if not shutil.which("v2ray-geosite"):
        print("::error::v2ray-geosite not found in PATH")
        print("::group::Debug Info")
        print("PATH:", os.environ.get('PATH'))
        print("::endgroup::")
        return False
    return True

def process_url(url, output_dir):
    """Обработка одного URL"""
    try:
        path = urlparse(url).path
        category = os.path.splitext(os.path.basename(path))[0]
        print(f"🔧 Processing {category}...")

        # Скачивание YAML
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        # Парсинг YAML
        data = yaml.safe_load(response.content)
        rules = data.get('payload', [])

        # Запись в текстовый формат
        output_path = os.path.join(output_dir, f"{category}.txt")
        with open(output_path, "w", encoding="utf-8") as f:
            for rule in rules:
                if isinstance(rule, dict):
                    for rule_type, value in rule.items():
                        f.write(f"{rule_type}:{value}\n")
                elif isinstance(rule, str):
                    f.write(f"domain:{rule}\n")
        
        print(f"✅ Success: {category}")
        return True

    except Exception as e:
        print(f"::warning::Error processing {url}: {str(e)}")
        return False

def compile_geosite(output_dir, output_file):
    """Компиляция geosite.dat"""
    try:
        print("🔨 Compiling geosite.dat...")
        exit_code = os.system(f"v2ray-geosite compile -o {output_file} {output_dir}")
        
        if exit_code != 0:
            print(f"::error::Compilation failed with code {exit_code}")
            return False
            
        file_size = os.path.getsize(output_file)
        print(f"🎉 Success! geosite.dat created ({file_size} bytes)")
        return True

    except Exception as e:
        print(f"::error::Compilation error: {str(e)}")
        return False

def main():
    try:
        # Настройка путей
        output_dir = "geosite"
        output_file = "geosite.dat"

        # Проверка зависимостей
        if not check_dependencies():
            sys.exit(1)

        # Создание директории
        os.makedirs(output_dir, exist_ok=True)

        # Обработка всех URL
        success_count = 0
        for url in URLS:
            if process_url(url, output_dir):
                success_count += 1

        # Проверка успешных загрузок
        if success_count == 0:
            print("::error::All URL processing failed")
            sys.exit(1)

        # Компиляция geosite.dat
        if not compile_geosite(output_dir, output_file):
            sys.exit(1)

    except Exception as e:
        print(f"::error::Main execution failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()

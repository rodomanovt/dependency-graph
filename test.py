import urllib.request
import json
import sys

def get_dependencies_via_api(crate_name, version=None):
    # Шаг 1: получить информацию о версии
    base_url = "https://crates.io"
    crate_url = f"{base_url}/api/v1/crates/{crate_name}"
    if version:
        crate_url += f"/{version}"

    try:
        with urllib.request.urlopen(crate_url) as resp:
            crate_data = json.load(resp)
    except Exception as e:
        print(f"Ошибка при получении данных пакета: {e}", file=sys.stderr)
        return []

    # Берём первую версию (самую свежую), если не указана явно
    if version is None:
        if not crate_data.get("versions"):
            print("Версии не найдены", file=sys.stderr)
            return []
        version_info = crate_data["versions"][0]
    else:
        version_info = crate_data["version"]  # при явном указании версии структура может отличаться

    # Шаг 2: получить зависимости по ссылке
    deps_path = version_info["links"]["dependencies"]
    deps_url = base_url + deps_path

    try:
        with urllib.request.urlopen(deps_url) as resp:
            deps_data = json.load(resp)
    except Exception as e:
        print(f"Ошибка при получении зависимостей: {e}", file=sys.stderr)
        return []

    # Шаг 3: извлечь имена обычных зависимостей
    dependencies = []
    for dep in deps_data.get("dependencies", []):
        if dep.get("kind") == "normal":  # пропускаем dev и build
            dependencies.append(dep["crate_id"])  # или dep["name"]

    return dependencies

# Пример использования
deps = get_dependencies_via_api("serde")
print(deps)
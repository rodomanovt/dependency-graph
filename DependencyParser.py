import urllib.request
import json
import sys

class DependencyParser:
    def __init__(self, repoUrl):
        self.repoUrl = repoUrl # https://crates.io/api/v1/crates/


    def getDependencies(self, crate_name):
        # Получение информацию о версии
        crateUrl = self.repoUrl + crate_name
        try:
            with urllib.request.urlopen(crateUrl) as resp:
                crate_data = json.load(resp)
        except Exception as e:
            print(f"Error parsing package data: {e}")
            sys.exit(1)


        if not crate_data.get("versions"):
            print("Versions not found", file=sys.stderr)
            sys.exit(1)
            return []
        # Берем самую новую версию
        version = crate_data["versions"][0]

        # получаем зависимости по ссылке
        deps_path = version["links"]["dependencies"]
        deps_url = 'https://crates.io' + deps_path
        try:
            with urllib.request.urlopen(deps_url) as resp:
                deps_data = json.load(resp)
        except Exception as e:
            print(f"Error parsing dependencies: {e}", file=sys.stderr)
            sys.exit(1)
            return []

        # извлекаем имена обычных зависимостей
        dependencies = []
        for dep in deps_data.get("dependencies", []):
            if dep.get("kind") == "normal":  # пропускаем dev и build
                dependencies.append(dep["crate_id"])  # или dep["name"]

        return dependencies


if __name__ == '__main__':
    deps = DependencyParser.getDependencies("serde")
    print(deps)
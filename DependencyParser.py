import urllib.request
import json
import sys
import re

class DependencyParser:
    def __init__(self, repoUrl):
        self.repoUrl = repoUrl # https://crates.io/api/v1/crates/
        self.repoPath = self.repoUrl


    def getDependencies(self, crateName):
        # Получение информацию о версии
        crateUrl = self.repoUrl + crateName
        try:
            with urllib.request.urlopen(crateUrl) as resp:
                crate_data = json.load(resp)
        except Exception as e:
            print(f"Error parsing package data: {e}")
            sys.exit(1)


        if not crate_data.get("versions"):
            print("Versions not found", file=sys.stderr)
            sys.exit(1)

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

        # извлекаем имена обычных зависимостей
        dependencies = []
        for dep in deps_data.get("dependencies", []):
            if dep.get("kind") == "normal":  # пропускаем dev и build
                if dep["crate_id"] != crateName: # пропускаем самозависимости
                    dependencies.append(dep["crate_id"])

        return dependencies


    def getTestDependencies(self, crateName):
        dependencies = []
        # Экранируем специальные символы в имени пакета для регулярного выражения
        escaped_name = re.escape(crateName)
        # Шаблон: "package_name" -> "dependency"
        pattern = re.compile(rf'^\s*"{escaped_name}"\s*->\s*"([^"]+)"\s*;?\s*$')

        try:
            with open(self.repoPath, 'r', encoding='utf-8') as f:
                for line in f:
                    match = pattern.match(line)
                    if match:
                        dependencies.append(match.group(1))
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {self.repoPath}")
        except Exception as e:
            raise RuntimeError(f"Error reading dot file: {e}")

        return dependencies


if __name__ == '__main__':
    parser = DependencyParser("https://crates.io/api/v1/crates/")
    deps = parser.getDependencies("rustc-std-workspace-core")
    print(deps)
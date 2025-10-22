import argparse
import os
import urllib.parse
import re
from DependencyParser import *


def getConfig():
    parser = argparse.ArgumentParser()

    # Обязательные аргументы
    parser.add_argument('packageName', type=str, help='Имя пакета')
    parser.add_argument('packageUrlPath', type=str, help='URL пакета')
    parser.add_argument('outputFile', type=str, help='Имя выходного файла')
    # Необязательные флаги
    parser.add_argument('-t', '--testRepo', action='store_true', default=False)
    parser.add_argument('-a', '--outputAscii', action='store_true', default=False)
    parser.add_argument('-d', '--maxDepth', type=int, default=1)

    args = parser.parse_args()

    return {
        'packageName': args.packageName,
        'packageUrlPath': args.packageUrlPath,
        'outputFile': args.outputFile,
        'testRepo': args.testRepo,
        'outputAscii': args.outputAscii,
        'maxDepth': args.maxDepth
    }


def isValidConfig(config: dict) -> bool:
    urlPath: str = config['packageUrlPath']

    if config['testRepo']: # если работаем с тестовым файлом
        if not os.path.isfile(urlPath):
            print(f"{urlPath}: file does not exist")
            return False

    else: # если работаем с URL репозитория

        # Проверка валидности URL
        parsed = urllib.parse.urlparse(urlPath)
        if parsed.scheme and parsed.netloc:
            return True

        # Поверка валидности домена
        regex = re.compile(
            r'^'
            r'(?:[a-zA-Z0-9]'  # первый символ
            r'(?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+'  # поддомены
            r'[a-zA-Z]{2,}$'  # TLD
        )
        if not (regex.match(urlPath)):
            print(f"{config['packageUrlPath']}: not a valid URL")
            return False

    # Проверка валидности имени файла
    filename = config['outputFile']
    if '/' in filename or '<' in filename or '>' in filename or \
            ':' in filename or '"' in filename or '|' in filename or \
            '?' in filename or '*' in filename:
        print(f"{filename}: not a valid file name")
        return False

    # Проверка валидности максимальной глубины
    if config['maxDepth'] <= 1:
        print(f"Invalid max depth: {config['maxDepth']}")
        return False

    return True


def buildDependencyGraph(config: dict):
    rootPackage = config['packageName']
    packageUrlPath = config['packageUrlPath']
    outputFile = f"{config['outputFile']}.dot" if not config['outputFile'].endswith(".dot") else config['outputFile']
    maxDepth = config['maxDepth']

    depsParser = DependencyParser(packageUrlPath)

    if maxDepth < 1:
        raise ValueError("max_depth must be at least 1")

    # Стек: (package_name, current_depth)
    stack = [(rootPackage, 0)]
    visited = set() # все обработанные пакеты
    result = set() # результат: множество ребер

    while stack:
        current, depth = stack.pop()

        if depth >= maxDepth:
            continue

        # Получаем зависимости только если ещё не обрабатывали этот пакет
        if current in visited:
            continue
        visited.add(current)

        deps = depsParser.getDependencies(current)

        for dep in deps:
            edge = (current, dep)
            if edge not in result:
                result.add(edge)
                stack.append((dep, depth + 1)) # Добавляем дочерний пакет в стек

    # Запись в dot-файл
    with open(outputFile, 'w', encoding='utf-8') as f:
        f.write("digraph Dependencies {\n")
        for parent, child in sorted(result):
            f.write(f'    "{parent}" -> "{child}";\n')
        f.write("}\n")

    print(f"Graph built successfully: {outputFile}")


def main():
    config = getConfig()
    if not isValidConfig(config):
        sys.exit(1)

    testRepo = config['testRepo']
    if not testRepo:
        buildDependencyGraph(config)
    else:
        pass


if __name__ == '__main__':
    main()
    # python3 main.py serde https://crates.io/api/v1/crates/ output -d 2
    # python3 main.py rand https://crates.io/api/v1/crates/ output -d 3
    # python3 main.py libc https://crates.io/api/v1/crates/ output -d 2
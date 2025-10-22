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

    filename = config['outputFile']
    if '/' in filename or '<' in filename or '>' in filename or \
            ':' in filename or '"' in filename or '|' in filename or \
            '?' in filename or '*' in filename:
        print(f"{filename}: not a valid file name")
        return False

    return True


def main():
    config = getConfig()
    if not isValidConfig(config):
        sys.exit(1)

    packageName = config['packageName']
    packageUrlPath = config['packageUrlPath']

    depsParser = DependencyParser(packageUrlPath)
    deps = depsParser.getDependencies(packageName)
    print(deps)

if __name__ == '__main__':
    main()
    # python3 main.py serde https://crates.io/api/v1/crates/ 2 -d 3
    # python3 main.py rand https://crates.io/api/v1/crates/ 2 -d 3
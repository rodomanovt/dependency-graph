import argparse
import os
import sys
import urllib.parse
import re


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
            print(f"{config['packageUrlPath']}: not a valid URL or domain")
            return False

    return True



def main():
    config = getConfig()
    if isValidConfig(config):
        print(config)
    else:
        sys.exit(1)

if __name__ == '__main__':
    main()
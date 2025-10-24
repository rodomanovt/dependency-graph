import re

def topological_sort_dfs(dot_file_path: str):
    # Парсим рёбра из DOT-файла
    edges = []
    with open(dot_file_path, 'r', encoding='utf-8') as f:
        for line in f:
            match = re.search(r'"([^"]+)"\s*->\s*"([^"]+)"', line)
            if match:
                parent, child = match.groups()
                edges.append((parent, child))

    # Граф изначально строился сверху вниз
    # В файле переходы записаны от корневой вершины к конечным
    # Считываем вершины, в которые мы переходили, в обратном порядке
    rights = []
    for i in range(len(edges)-1, -1, -1):
        if edges[i][1] not in rights:
            rights.append(edges[i][1])

    result = rights + [edges[0][0]] # добавляем корневую вершину
    print(result)

# topological_sort_dfs("testGraph.d2")
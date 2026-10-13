"""ABC168 D: accept any adjacent predecessor on a shortest path to room 1."""


def accepts(input_text: str, actual: str, expected: str) -> bool:
    try:
        data = list(map(int, input_text.split()))
        n, m = data[:2]
        if n < 2 or m < 1 or len(data) != 2 + 2 * m:
            return False
        graph = [set() for _ in range(n)]
        for i in range(2, len(data), 2):
            u, v = data[i:i + 2]
            if not (1 <= u <= n and 1 <= v <= n and u != v):
                return False
            graph[u - 1].add(v - 1)
            graph[v - 1].add(u - 1)
        distance = [-1] * n
        distance[0] = 0
        queue = [0]
        for u in queue:
            for v in graph[u]:
                if distance[v] == -1:
                    distance[v] = distance[u] + 1
                    queue.append(v)
        tokens = actual.split()
        if len(queue) != n:
            return tokens == ["No"]
        if len(tokens) != n or tokens[0] != "Yes":
            return False
        for v, token in enumerate(tokens[1:], 1):
            parent = int(token) - 1
            if parent not in graph[v] or distance[parent] != distance[v] - 1:
                return False
        return True
    except (ValueError, IndexError):
        return False

"""ABC126 D: each color class must have a single root-distance parity."""


def accepts(input_text: str, actual: str, expected: str) -> bool:
    try:
        data = list(map(int, input_text.split()))
        n = data[0]
        if n < 1 or len(data) != 1 + 3 * (n - 1):
            return False
        colors = actual.split()
        if len(colors) != n or any(c not in {"0", "1"} for c in colors):
            return False
        graph = [[] for _ in range(n)]
        for i in range(1, len(data), 3):
            u, v, w = data[i:i + 3]
            if not (1 <= u <= n and 1 <= v <= n and w > 0):
                return False
            graph[u - 1].append((v - 1, w & 1))
            graph[v - 1].append((u - 1, w & 1))
        parity = [-1] * n
        parity[0] = 0
        queue = [0]
        for u in queue:
            for v, w in graph[u]:
                if parity[v] == -1:
                    parity[v] = parity[u] ^ w
                    queue.append(v)
        if len(queue) != n:
            return False
        # When all distances are even, BOTH colors may be used arbitrarily.
        seen = {}
        for color, value in zip(colors, parity):
            if seen.setdefault(color, value) != value:
                return False
        return True
    except (ValueError, IndexError):
        return False

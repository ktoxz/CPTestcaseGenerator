"""Compare special checkers with independent exhaustive small-instance oracles."""
import itertools
import unittest

from scripts.codenet_checkers.p02678 import accepts as signs
from scripts.codenet_checkers.p03044 import accepts as coloring


class Additional20CheckerTests(unittest.TestCase):
    def test_coloring_against_all_pair_distances(self):
        for n in range(1, 6):
            for parents in itertools.product(*(range(v) for v in range(1, n))):
                for weights in itertools.product((1, 2), repeat=n - 1):
                    edges = [(p, v, w) for v, (p, w) in enumerate(zip(parents, weights), 1)]
                    data = str(n) + "\n" + "".join(f"{u+1} {v+1} {w}\n" for u, v, w in edges)
                    dist = [[10**6] * n for _ in range(n)]
                    for v in range(n):
                        dist[v][v] = 0
                    for u, v, w in edges:
                        dist[u][v] = dist[v][u] = w
                    for k in range(n):
                        for u in range(n):
                            for v in range(n):
                                dist[u][v] = min(dist[u][v], dist[u][k] + dist[k][v])
                    for colors in itertools.product((0, 1), repeat=n):
                        valid = all(colors[u] != colors[v] or dist[u][v] % 2 == 0
                                    for u in range(n) for v in range(n))
                        self.assertEqual(coloring(data, "\n".join(map(str, colors)), "ignored"), valid)

    def test_signs_against_paths_on_all_small_connected_graphs(self):
        for n in range(2, 5):
            possible = list(itertools.combinations(range(n), 2))
            for bits in itertools.product((0, 1), repeat=len(possible)):
                edges = [edge for edge, bit in zip(possible, bits) if bit]
                dist = [[99] * n for _ in range(n)]
                for v in range(n):
                    dist[v][v] = 0
                for u, v in edges:
                    dist[u][v] = dist[v][u] = 1
                for k in range(n):
                    for u in range(n):
                        for v in range(n):
                            dist[u][v] = min(dist[u][v], dist[u][k] + dist[k][v])
                if any(dist[0][v] == 99 for v in range(n)):
                    continue
                data = f"{n} {len(edges)}\n" + "".join(f"{u+1} {v+1}\n" for u, v in edges)
                for parents in itertools.product(range(n), repeat=n - 1):
                    valid = True
                    for start in range(1, n):
                        cur, visited = start, set()
                        while cur != 0 and cur not in visited:
                            visited.add(cur)
                            nxt = parents[cur - 1]
                            if tuple(sorted((cur, nxt))) not in edges:
                                valid = False
                                break
                            cur = nxt
                        if cur != 0 or len(visited) != dist[0][start]:
                            valid = False
                        if not valid:
                            break
                    output = "Yes\n" + "\n".join(str(p + 1) for p in parents)
                    self.assertEqual(signs(data, output, "ignored"), valid)

    def test_alternatives_and_malformed_outputs(self):
        graph = "4 4\n1 2\n1 3\n2 4\n3 4\n"
        self.assertTrue(signs(graph, "Yes\n1\n1\n2\n", ""))
        self.assertTrue(signs(graph, "Yes\n1\n1\n3\n", ""))
        for bad in ("No", "Yes 1 1", "Yes 1 1 2 3", "Yes 1 1 0", "Yes 1 1 5", "Yes 1 1 x", "Yes 1 1 1"):
            self.assertFalse(signs(graph, bad, ""))
        tree = "3\n1 2 2\n2 3 1\n"
        for good in ("0 0 1", "1 1 0"):
            self.assertTrue(coloring(tree, good, ""))
        for bad in ("0 1 1", "0 0", "0 0 1 0", "0 0 2", "0 0 x"):
            self.assertFalse(coloring(tree, bad, ""))
        self.assertTrue(coloring("3\n1 2 2\n2 3 4\n", "0 1 0", ""))


if __name__ == "__main__":
    unittest.main()

from collections import defaultdict

def dfs(graph, node, diameter):
	if node in graph:
		tap, d_min = dfs(graph, graph[node], diameter)
		d_min = min(d_min, diameter[node, graph[node]])
		return (tap, d_min)
	return (node, 1000007)

if __name__ == '__main__':
	n, edges = map(int, input().split())
	
	graph = dict()
	diameter = dict()
	tanks = set(range(1,n+1))
	taps = set(range(1,n+1))

	for _ in range(edges):
		i, j, d = map(int, input().split())
		graph[i] = j
		diameter[(i, j)] = d
		if i in taps:
			taps.remove(i)
		if j in tanks:
			tanks.remove(j)

	ans = 0
	solutions = list()
	for i in tanks:
		tap, d = dfs(graph, i, diameter)
		if i != tap:
			ans += 1
			solutions.append((i, tap, d))

	print(ans)
	for soln in solutions:
		print(soln[0], soln[1], soln[2])
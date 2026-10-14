def get_roots(start,parent,color,edges,roots):
	color[start] = 1
	if roots:
		return
	for neighbor in edges[start]:
		if color[neighbor] == 0:
			get_roots(neighbor,start,color,edges,roots)

		elif color[neighbor] == 1 and neighbor !=parent:
			if not roots.keys():
				for i in range(len(color)):
					if color[i] == 1:
						roots[i] = True 

			return 

	color[start] = 2

def solve():
	n,m = map(int,input().split())
	color = [0 for _ in range(n+1)]
	edges = [[] for _ in range(n+1)]
	visited = [False for _ in range(n+1)]
	roots = dict()

	for _ in range(m):
		u,v = map(int,input().split())
		edges[u].append(v)
		edges[v].append(u)

	get_roots(1,-1,color,edges,roots)
	if not roots.keys():
		print('NO')
		return 


	for root in roots.keys():
		stack = list()
		stack.append(root)

		while stack:
			parent = stack.pop()
			visited[parent] = True 

			for child in edges[parent]:
				if not visited[child]:
					if not roots.get(child):
						stack.append(child)
						visited[child] = True 

	for i in range(1,n+1):
		if not visited[i]:
			print('NO')
			return 

	print('FHTAGN!')

solve()
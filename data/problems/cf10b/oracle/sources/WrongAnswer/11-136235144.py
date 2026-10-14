import math

_, k = map(int, input().split())

queries = map(int, input().split())

free = [[1 for _ in range(k)] for _ in range(k)]

center = math.ceil(k/2)

for query in queries:
	s = False
	minimal_dist = k**3
	minimal_dist_xy = (0,0)

	for x in range(k):
		for y in range(k):
			if x+query < len(free[y])+1:
				if all(free[y][x:x+query]):
					dist = abs(y+1-center) + sum(map(lambda x: abs(x-center+1), range(x,x+query)))


					if dist < minimal_dist:
						minimal_dist = dist
						minimal_dist_xy = (x, y)

						s = True
	if s:
		free[minimal_dist_xy[1]][minimal_dist_xy[0]:minimal_dist_xy[0]+query] = [0] * query
		print(minimal_dist_xy[1]+1, minimal_dist_xy[0]+1, minimal_dist_xy[0]+query)
	else:
		print(-1)
n,m = map(int, input().split())
entries = [int(i) for i in input().split()]
steps = 0
for moves in range(1, n):
	position_change = max(entries[moves - 1] - entries[moves] + m, 0) / m
	steps += position_change
	entries[moves] += position_change * m
print(int(steps))
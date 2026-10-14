import sys

input = sys.stdin.readline

n, p1, p2, p3, t1, t2 = map(int, input().split())
data = [list(map(int, input().split())) for _ in range(n)]

tot = p1 * (data[0][1] - data[0][0])
for i in range(1, n):
    gap = data[i][0] - data[i - 1][1]

    tmp1 = min(t1, gap)
    tmp2 = min(t2, gap - t1)
    tmp3 = (gap - (tmp1 + tmp2))

    tot += tmp1 * p1 + tmp2 * p2 + tmp3 * p3
    tot += p1 * (data[i][1] - data[i][0])

print(tot)
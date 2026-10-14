import sys
input = sys.stdin.readline



n, k = map(int, input().split())
w = list(map(int, input().split()))
g = [[0]*k for i in range(k)]
d = [(-1, -1) for i in range(k)]
for i in range(k):
    for j in range(k):
        g[i][j] = abs(i-k//2) + abs(j-k//2)

for x in w:
    c = 2 << 30
    q = (-1, -1, -1)
    for i in range(k):
        if d[i] == (-1, -1):
            y = sum(g[i][k//2-x//2:k//2+(x+1)//2])
            if y < c:
                c = y
                q = (i+1, k//2-x//2+1, k//2+(x+1)//2)
        else:
            y = 2 << 30
            if x < d[i][0]:
                y = sum(g[i][d[i][0]-1-x:d[i][0]-1])
                if y < c:
                    c = y
                    q = (i+1, d[i][0]-x, d[i][0]-1)
            if x < k-d[i][1]+1:
                y = sum(g[i][d[i][1]:d[i][1]+x])
                if y < c:
                    c = y
                    q = (i+1, d[i][1]+1, d[i][1]+x)
    if q[0] == -1:
        print(-1)
    else:
        print(*q)
        if d[q[0]-1] == (-1, -1):
            d[q[0]-1] = (q[1], q[2])
        else:
            if q[2] <= d[q[0]-1][0]:
                d[q[0]-1] = (q[1], d[q[0]-1][1])
            else:
                d[q[0]-1] = (d[q[0]-1][0], q[2])
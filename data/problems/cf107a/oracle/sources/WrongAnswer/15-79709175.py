#!/usr/bin/env python3

n, pcnt = map(int, input().split())
pipes = [None] * n
in_cnt = [0] * n
for i in range(pcnt):
    u, v, d = map(int, input().split())
    pipes[u-1] = (v-1, d)
    in_cnt[v-1] += 1

ans = []
for i, p in enumerate(pipes):
    if in_cnt[i] == 0:
        cur, mn = i, 10_000_000
        while pipes[cur]:
            mn = min(mn, pipes[cur][1])
            cur = pipes[cur][0]
        ans.append((i+1, cur+1, mn))

print(len(ans))
for a in ans:
    print(a[0], a[1], a[2])
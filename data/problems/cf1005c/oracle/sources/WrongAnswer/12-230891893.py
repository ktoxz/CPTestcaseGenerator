# Wadea #

from collections import defaultdict
n = int(input());arr = list(map(int,input().split()));ans = 0;d = defaultdict(int )
for i in arr:
    d[i] += 1
for j in d:
    cur = 1
    ok = 0
    for jj in range(31):
        if cur - j in d:
            if cur - j == j and d[j] == 1:
                cur *= 2
                break
            ok = 1
            break
        cur *= 2
    if ok == 0:
        ans += d[j]
print(ans)
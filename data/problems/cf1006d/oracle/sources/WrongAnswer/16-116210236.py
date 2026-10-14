from sys import stdin
from collections import Counter
input = stdin.readline

n = int(input())
a = input().rstrip()
b = input().rstrip()
ans = 0
for i in range(n // 2):
    x = [a[i], a[n-i-1], b[i], b[n-i-1]]
    c = Counter(x)
    y = c.values()
    if len(y) == 4:
        ans += 2
    elif len(y) == 3:
        if x[0] == x[1] or x[2] == x[3]:
            ans += 2
        else:
            ans += 1
    elif max(y) == 3:
        ans += 1
if n % 2 > 0:
    ans += a[n // 2] != b[n // 2]
print(ans)
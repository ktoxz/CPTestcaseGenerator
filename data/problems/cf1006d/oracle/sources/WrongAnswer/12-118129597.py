from collections import defaultdict
import sys
input = sys.stdin.readline

n = int(input())
a = list(input().rstrip())
b = list(input().rstrip())
ans = 0
for i in range(n // 2):
    cnt = defaultdict(lambda : 0)
    if a[i] == a[n - i - 1] and b[i] == b[n - i - 1]:
        continue
    for j in [i, n - i - 1]:
        cnt[b[j]] += 1
    for j in [i, n - i - 1]:
        if cnt[a[j]] <= 0:
            ans += 1
        cnt[a[j]] -= 1
if n % 2:
    ans += 1 if not a[n // 2] == b[n // 2] else 0
print(ans)
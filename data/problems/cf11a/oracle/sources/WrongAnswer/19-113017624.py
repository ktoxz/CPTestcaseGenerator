#  author:  violist
#  created: 14.04.2021 15:41:42

import sys
input = sys.stdin.readline

n, d = [int(i) for i in input().split()]
a = [int(i) for i in input().split()]
ans = 1
for i in range(n - 1):
    if a[i + 1] <= a[i]:
       a[i + 1] += a[i] - a[i + 1] // d
       ans += 1
print(ans)
import sys
input = sys.stdin.readline
from collections import Counter

s = input()[:-1]
n = len(s)
k = int(input())
if k >= n:
    print(0)
    print('')
else:
    c = Counter()
    for i in s:
        c[i] += 1
    x = c.most_common()
    i = len(x) - 1
    while k > 0:
        k -= x[i][1]
        if k < 0:
            break
        s = s.replace(x[i][0],'')
        i -= 1
    print(i+1)
    print(s)
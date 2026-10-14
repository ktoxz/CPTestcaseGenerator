import sys;sc = sys.stdin.readline;out=sys.stdout.write
from collections import Counter
n=int(sc());arr=list(map(int,sc().rstrip().split()))
a=Counter(arr);ans = 0
for x in a:
    for deg in range(32):
        pow2 = 2 ** deg
        if pow2 - x > 0 and pow2 - x in a and (a[x] >= 2 or pow2 - x != x):break
        else:ans += a[x]
out(str(ans))
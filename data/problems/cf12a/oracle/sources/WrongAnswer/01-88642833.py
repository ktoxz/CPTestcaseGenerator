import sys

n = [i.strip().rstrip() for i in sys.stdin.readlines()]
if n[0][0] == n[0][2] and n[0][2] == n[2][0] and n[0][1] == n[2][1] and n[1][0] == n[1][2]:
    print("YES")
else:
    print("NO")
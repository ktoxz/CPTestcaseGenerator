import sys
input = sys.stdin.readline

n, p1, p2, p3, t1, t2 = map(int, input().split())

def power(t):
    p = p2 * min(t, t1) + p3 * max(0, t-t1)
    return p


a, c, d = 0, 0, 0
for _ in range(n):
    l, r = map(int, input().split())
    if d == 0:
        c += l*p3
        d = 1
    else:
        c += power(l-a)
    c += p1*(r-l)
    a = r

print(c)
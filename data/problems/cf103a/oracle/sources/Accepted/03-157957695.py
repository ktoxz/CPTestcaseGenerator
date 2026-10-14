import sys
input = sys.stdin.readline

n = int(input())
w = list(map(int, input().split()))
s, c = 1, 0
for i in range(n):
    c += s*(w[i]-1)
    s += 1
c += n
print(c)
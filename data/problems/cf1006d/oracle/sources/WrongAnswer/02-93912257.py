import sys
readline = sys.stdin.readline

N = int(readline())
A = list(map(ord, readline().strip()))
B = list(map(ord, readline().strip()))

ans = 0
for i in range(N//2):
    a, b, c, d = A[i], B[i], A[N-1-i], B[N-1-i]
    if a == c and b == d:
        continue
    if a == b and c == d:
        continue
    if a == d and b == c:
        continue
    if b == d or a == d or b == c:
        ans += 1
        continue
    ans += 2
if N&1:
    if A[N//2] != B[N//2]:
        ans += 1

print(ans)
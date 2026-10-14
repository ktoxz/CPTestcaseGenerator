import sys, os, io
input = io.BytesIO(os.read(0, os.fstat(0).st_size)).readline

x = int(input())
x = abs(x)
ans, c = 0, 0
while True:
    if c == x or (c > x and not (c - x) % 2):
        break
    ans += 1
    c += ans
print(ans)
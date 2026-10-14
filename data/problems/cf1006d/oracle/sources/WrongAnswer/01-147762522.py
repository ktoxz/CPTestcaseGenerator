n, s, t = int(input()), input(), input()
ans = n%2 and s[n//2] != t[n//2]
for u, v, x, y in zip(s[:n//2], s[::-1], t, t[::-1]):
    ans += (len({x, y} - {u, v}), u != v)[x == y]
print(ans)
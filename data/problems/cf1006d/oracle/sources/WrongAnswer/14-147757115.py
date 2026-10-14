n, s, t = int(input()), input(), input()
a = {}
ans = 0
for i in range((n+1)//2):
    a[t[i]] = a.get(t[i], 0) + 1
    a[t[n-i-1]] = a.get(t[n-i-1], 0) + 1
    if s[i] in a: a[s[i]] -= 1
    if s[n-i-1] in a: a[s[n-i-1]] -= 1
    ans += sum(x%2 for x in a.values())
    a.clear()
print(ans)
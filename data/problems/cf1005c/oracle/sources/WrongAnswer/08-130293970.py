n = int(input())
a = input().split(' ')
c = [0]*(10000)
for i in range(n):
    a[i] = (int(a[i]))
    c[a[i]] += 1
                
ans = 0
for i in range(n):
    ok = 0
    for j in range(30):
        x = 2**j - a[i]
        if (x in c and(c[x] > 1 or(c[x] == 1 and x != a[i]))):
            ok = 1
    if ok != 0:
        ans += 1
print(ans)
                
# Wed Sep 29 2021 21:13:34 GMT+0300 (Москва, стандартное время)
a1 = input()
a = []
ans = 0
b = []
for i in range(len(a1)):
    a.append(int(a1[i]))
    if a[i] % 3 == 0:
        b = []
        ans += 1
    else:
        b.append(a[i])
        if sum(b)%3 == 0:
               b = []
               ans += 1
        else:
            for j in range(len(b)):
                if sum(b[j:]) % 3 == 0:
                    b = []
                    ans += 1
                    
print(ans)
# Thu Sep 30 2021 19:58:41 GMT+0300 (Москва, стандартное время)
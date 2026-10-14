n = int(input())
lst = list(map(int,input().split()))
lst_of_2 = []
dct = {}
for i in range(n):
    if lst[i] in dct.keys():
        dct[lst[i]] += 1
    else:
        dct[lst[i]] = 1
x = 1
while x <= 10**9:
    lst_of_2.append(x)
    x = x*2
ans = 0
for j in range(n):
    y = lst[j]
    check = 0
    for k in range(len(lst_of_2)):
        if (lst_of_2[k]-y) in dct.keys():
            if (lst_of_2[k] - y) == y:
                if dct[y] > 1:
                    check = 1
            else:
                check = 1
                break
    if check == 0:
        ans += 1
print(ans)
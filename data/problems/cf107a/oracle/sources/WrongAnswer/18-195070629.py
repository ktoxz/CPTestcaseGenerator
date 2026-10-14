n, p = map(int, input().split())
val_list = [False] * n

num_list1 = []
num_list2 = []
ab = []
for i in range(p):
    a, b, d = map(int, input().split())
    num_list1.append(a)
    num_list2.append(b)
    ab.append(d)

fir = []
sec = []
for i in range(len(num_list2)):
    if num_list1[i] not in num_list2:
        fir.append((num_list1[i], ab[i]))
    if num_list2[i] not in num_list1:
        sec.append((num_list2[i], ab[i]))

sec.sort(key=lambda x: x[1])
fir.sort(key=lambda x: x[1])
ans = []
for i in range(len(fir)):
    ans.append((fir[i][0], sec[i][0], min(fir[i][1], sec[i][1])))
ans.sort(key=lambda x: x[0])

print(len(ans))
for i in ans:
    print(*i)
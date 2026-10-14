n, p = map(int, input().split())

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
fir.sort(key=lambda x: x[0])
ans = []
ln = len(fir)
val_list = [False] * ln
for i in range(ln):
    for j in range(ln):
        if sec[j][1] >= fir[i][1] and not val_list[j]:
            ans.append((fir[i][0], sec[j][0], min(fir[i][1], sec[j][1])))
            val_list[j] = True

print(len(ans))
for i in ans:
    print(*i)
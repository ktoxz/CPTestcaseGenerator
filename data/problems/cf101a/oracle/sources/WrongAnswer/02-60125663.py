s = input()
n = int(input())
lis = []
dic = {}
if len(s) < n:
    print(0)
else:
    for i in s:
        if i not in dic:
            dic[i] = 0
        else:
            dic[i] += 1
    for k,v in dic.items():
        lis.append(v)
    alis = []
    for k,v in dic.items():
        if v == max(lis):
            alis.append(k)
    print(len(alis))
    res = ''
    for i in alis:
        res += i
    print(res*n)
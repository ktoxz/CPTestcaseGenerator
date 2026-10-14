n = int(input())
s = input().split()
lst = []
for i in range(n):
    lst.append(int(s[i]))

st = sum(lst)
if len(lst) == 1:
    print(lst[0])
elif st == len(lst):
    print(st)
elif len(lst) ==2:
    print(st + 1)
else:
    print(st)
    print(st + len(lst))
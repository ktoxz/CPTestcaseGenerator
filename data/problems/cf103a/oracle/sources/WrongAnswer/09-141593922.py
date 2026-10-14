# inds = 0
# inde = 0
# flag = 0
# res = []

# ress = []

# t = int(input())
# for i in range(t):
#     inds = 0
#     inde = 0
#     a = int(input())
#     lst = []
#     res = []
#     str = input().split()
#     for i in range(a):
#         lst.append(int(str[i]))
#     if lst[0] >0:
#         flag = 0
#     else:
#         flag = 1

#     while inds != len(lst):
#         if inds == len(lst):
#             break
#         if inde == len(lst) - 1:
#             if inds == inde:
#                 res.append(lst[-1])
#                 break
#             else:
#                 m = max(lst[inds:inde])
#                 inds = inde
#                 res.append(m)
#                 inds += 1
#         elif (not flag and lst[inde + 1] > 0) or (flag and lst[inde + 1] < 0):
#             inde += 1
#         else:
#             inde += 1
#             m = max(lst[inds:inde])
#             inds = inde
#             res.append(m)
#             flag = not flag

#     ress.append(sum(res))

# for i in ress:
#     print(i)

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
else:
    print(st + 1)
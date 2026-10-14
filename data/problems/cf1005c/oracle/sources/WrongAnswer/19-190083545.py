n = int(input())
A = [int(x) for x in input().split()]
PT = [1]
for i in range(24):
    PT.append(2*PT[len(PT)-1])
Ok = set()
N = set()
A2 = set(A)
rn = 0
for i in A2:
    if i in N or i in Ok: continue
    cur = False
    T = False
    if A.count(i) > 1: T = True
    for k in PT:
        if k-i == i and not T: continue
        if k-i > max(A2): break
        if k-i in A2:
            cur = True
            Ok.add(i)
            Ok.add(k-i)
            break
    if not cur:
        N.add(i)
        rn += A.count(i)
# for i in range(n):
#     if A[i] in Ok or A[i] in N: continue
#     cur = False
#     for k in range(n):
#         if k != i:
#             if A[k] in N: continue
#             if A[i]+A[k] in PT:
#                 cur = True
#                 Ok.add(A[i])
#                 Ok.add(A[k])
#     if not cur:
#         N.add(A[i])
#         rn += A.count(A[i])
print(rn,N,Ok)
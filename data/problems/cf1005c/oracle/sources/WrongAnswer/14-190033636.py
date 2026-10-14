n = int(input())
A = [int(x) for x in input().split()]
PT = [1]
for i in range(23):
    PT.append(2*PT[len(PT)-1])
Ok = []
N = []
rn = 0
for i in range(n):
    cur = False
    if A[i] in N or A[i] in Ok: continue
    for k in range(i+1,n):
        if A[k] in Ok: continue
        if A[i]+A[k] in PT:
            Ok.append(A[i])
            Ok.append(A[k])
            cur = True
    if not cur:
        N.append(A[i])
        rn += N.count(A[i])
print(rn)
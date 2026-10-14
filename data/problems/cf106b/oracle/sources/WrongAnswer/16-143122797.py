import math,sys;input=sys.stdin.readline;S=lambda:input().rstrip();I=lambda:int(S());M=lambda:map(int,S().split());L=lambda:list(M());mod1=1000000007;mod2=998244353

n =I()
sp,rp,hp,cp = 0,0,0,1001
indexp = -1

values = []
for i in range(n):
    s,r,h,c = M()
    values.append([s,r,h,c])
    if s>sp and r>rp and h>hp:
        
        sp,rp,hp,cp = s,r,h,c
        

mini = cp
for i in range(n):
    if values[i][0]>=sp or values[i][1]>=rp or values[i][2]>=hp:
        if values[i][3]<=mini:
            mini = values[i][3]
            indexp = i

# print(cp)
print(indexp+1)
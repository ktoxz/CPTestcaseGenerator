n, P1, P2, P3, T1, T2=map(int,input().split())

LR=[tuple(map(int,input().split())) for i in range(n)]
ANS=0
for i in range(n):
    l,r=LR[i]
    ANS+=(r-l)*P1

    if i!=n-1:
        l2,r2=LR[i+1]

        ANS+=min(T1,l2-r)*P1
        ANS+=max(0,min(T2,l2-(r+T1))*P2)
        ANS+=max(0,(l2-(r+T1+T2))*P3)

print(ANS)
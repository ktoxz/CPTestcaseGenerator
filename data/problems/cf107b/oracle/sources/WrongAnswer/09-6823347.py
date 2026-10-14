n,m,h=map(int,input().split())
L=list(map(int,input().split()))
s=sum(L)
T=[]
def ncr(x,y):
    p=1
    T=[0]*(1001)
    for a in range(2,y+1):
        T[a]+=1
    for a in range(2,x-y+1):
        T[a]+=1
    for i in range(1,x+1):
        p*=i
        for j in range(2,max(y+1,x-y+1)):
            if(T[j]==0 or p%j!=0):
                continue
            while(p%j==0 and T[j]>=0):
                p//=j
                T[j]-=1
    return p
    
        

if(s<n):
    print(-1)
elif(L[h-1]==1 or n==1):
    print(0)
else:
    
    h=ncr(s-2,n-2)
    h/=ncr(s-1,n-1)
    print(h)
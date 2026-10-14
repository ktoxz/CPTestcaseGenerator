n=int(input())
m=int(input())
a=list(map(int,input().split()))
b=list(map(int, input().split())); x=0; l=1
for t in range(2*n):
    
    if t%2==1:
        if not (a[t//2]-1):
            l=0
            break
        x=(x*a[t//2]+m)/(a[t//2]-1)
    else:
        if not (b[t//2]-1):
            l=0
            break
        x=(x*b[t//2]+m)/(b[t//2]-1)
if l:
    print(x)
else:




    print(-1)
"""
for _ in range(int(input())):
    n,r1,c1,r2,c2=map(int,input().split())
    print(min(abs(r1-r2)+ abs(c1-c2),min(min(r1,n-r1 +1),min(c1,n-c1+1))+min(min(r2,n-r2+1),min(c2,n-c2+1))))
    #m=min(abs(r1-r2)+abs(c1-c2),min(min(r1,n-r1 +1)
    #p=r1,

for _ in range(int(input())):
    n,k=map(int,input().split())
    #l=[int(i) for i in range(1,n+1)]
    if k<n//2:
        print(2*k*n-2*k*k-k)
    else:print((n*n-n)//2)


for _ in range(int(input())):
    a,b,c=map(int,input().split())
    if a+b==c or b+c==a or a+c==b:
        print("YES")
    else:print("NO")

for _ in range(int(input())):
    n,m=map(int,input().split())
    print(m*min(2,n-1))
    
#1391B
for _ in range(int(input())):
    m,n=map(int,input().split())
    c=0
    for i in range(1,m+1):
        p=input()
        if p[-1]=="R":
            c+=1
        if i==m:
            for j in p:
                if j=="D":c+=1
    print(c)

n,m=map(int,input().split())
c=0
for _ in range(n):
    p=input()
    for i in p:
        if i=="C" or i=="M" or i=="Y":
            c+=1
if c==0:print("#Black&White")
else:print("#Color")

n=int(input())
c=0
for j in range(n):
    p=list(map(int,input().split()))
    for i in range(n):
        if i==j or i==n-j-1 or i==(n-1)//2 or j==(n-1)//2:
            c+=p[i]
print(c)

from math import gcd
m,n=sorted(map(int,input().split()))
#print(m,n)
c=6-n+1
p=int(gcd(c,6))
i=int(c/p)
j=int(6/p)
print(f"{i}/{j}")

m,n=map(int,input().split())
for i in range(1,m+1):
    if i%2==0:
        if i%4==0:
            print("#",end="")
            print("."*(n-1))
        else:
            print("."*(n-1),end="")
            print("#",end="")
            print("")
    else:
        print("#"*n)


for _ in range(int(input())):
    n=int(input())
    c2=0;c3=0
    while n%2==0:
        n//=2
        c2+=1
    while n%3==0:
        n//=3
        c3+=1
    if n!=1 or c2>c3:print(-1)
    else:
        #print(c2)
        #print(c3)
        print(2*c3-c2)

for _ in range(int(input())):
    x,y,k=map(int,input().split())
    #print(k%x)
    if k%x==y:print(k)
    else:
        if k%x<y:
            k-=(k%x+abs(x-y))
        else:
            #print(k%x)
            k-=(k%x-y)
        print(k)

for _ in range(int(input())):
    n=int(input())
    if n%2==0:print(n//2)
    else:print(n//2+1)

for _ in range(int(input())):
    n=int(input())
    print((n+1)//2)
    for i in range((n+1)//2):
        print(3*i +1,n*3 -i*3)

def sol(n,l):
    if len(l)==1:return "YES"
    for i in range(n-1):
        if l[i+1]-l[i]>1:
            return "NO"
    return "YES"
for _ in range(int(input())):
    n=int(input())
    l=sorted(list(map(int,input().split())))
    print(sol(n,l))

for _ in range(int(input())):
    a,b=map(int,input().split())
    if b-a==0:print(0)
    elif b>a:
        if abs(b-a)%2!=0:
            print(1)
        else:
            print(2)
    else:
        if abs(a-b)%2!=0:
            print(2)
        else:print(1)

for _ in range(int(input())):
    n=int(input())
    z=2**((n//2)+1) -2
    print(z)


for _ in range(int(input())):
    a,b=map(int,input().split())
    #if a-b==0:print(0)
    #elif b>a:
    p=abs(b-a)
    if p%10!=0:print(p//10 +1)
    else:print(p//10)
"""

n=int(input())
if n-10==0 or n>21:
    print(0)
else:
    if n-10==11 or n-10<10:
        print(4)
    elif n-10==10:
        print(4*4 -1)
    #elif n-10<10:
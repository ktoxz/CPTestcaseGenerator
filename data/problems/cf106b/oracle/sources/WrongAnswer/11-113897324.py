n=int(input())
x=[]
a=b=c=2**31
for i  in range(n):
    p=list(map(int,input().split()))
    p.append(i+1)
    a=min(a,p[0])
    b=min(b,p[1])
    c=min(c,p[2])
    x.append(p)
x.sort(key=lambda i:i[3])
for i in x:
    if (i[0]!=a and i[1]!=b and i[2]!=c):
        print(i[4])
        break
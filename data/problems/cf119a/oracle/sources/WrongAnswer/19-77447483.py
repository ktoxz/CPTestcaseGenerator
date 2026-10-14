a,b,c=map(int,input().split())
popitki=0
a1=a
b1=b
c1=c
while c>0:
    while c>0:
        f=a%c
        a=c
        c=f
        c=c1-a
        c1=c
        a=a1
        popitki+=1
        while c>0:
            f=b%c
            b=c
            c=f
            c=c1-b
            c1=c
            b=b1
            popitki+=1
if popitki%2==1 or c==0 :
    print(1)
else:
    print(0)
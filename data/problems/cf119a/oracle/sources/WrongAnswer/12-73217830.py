a,b,c=input().split()
a=int(a)
b=int(b)
c=int(c)
if c%(a+b)>0 and c%(a+b)<=a:
    print(0)
else:
    print(1)
n=int(input())
if n<=10:
    print(0)
else:
    x=n-10 
    c=0
    if 2<=x<10:
        c+=4
    elif x==10:
        c+=4+4+4+3 
    else:
        c+=4
    print(c)
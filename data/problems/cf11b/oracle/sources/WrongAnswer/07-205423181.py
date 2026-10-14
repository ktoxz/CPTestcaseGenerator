import math
x=abs(int(input()))
n=int((math.sqrt(8*x+1)-1)/2)
if x==(n**2+n)/2:
    print(int(n))
else:
    i=n 
    j=n+1 
    
    parx=x%2
    pari=((n**n+n)//2)%2
    parj=((n**2+3*n+2)//2)%2
    
    if pari==1 and parj==1:
        if parx==1:
            print(j)
        else:
            print(j+1)
    elif pari==0 and parj==1:
        if parx==1:
            print(j)
        else:
            print(j+2)
    elif pari==1 and parj==0:
        if parx==0:
            print(j)
        else:
            print(j+2)
    else:
        if parx==0:
            print(j)
        else:
            print(j+1)
n=int(input())
if(n%4==0):
    k=int(n/4)
    for i in range(k):
        print(4,end="")
elif(n%4==3):
    n-=7
    if(n<0):
        print(-1)
    else:
     print(7,end="")
     k=int(n/4)
     for i in range(k):
        print(4,end="")
    
elif(n%4==2):
    n-=14
    if(n<0):
        print(-1)
    else:
     print("77",end="")
     k=int(n/4)
     for i in range(k):
        print(4,end="")
    
else :
    n-=21
    if(n<0):
        print(-1)
    else:
     print("777",end="")
     k=int(n/4)
     for i in range(k):
        print(4,end="")
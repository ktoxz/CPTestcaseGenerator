x=int(input())

s=0
i=0
n=0

while s!= x:
    i+=1
    if s+i > x:
        s-=i
    else:
        s+=i
    n+=1

print(n)
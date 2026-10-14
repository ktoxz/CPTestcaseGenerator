k=int(input())
l=int(input())
for x in range(1,32):
    if k**x==l:
        print("Yes")
        x=x-1
        print(x)
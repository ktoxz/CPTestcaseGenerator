n=int(input())
l=list(map(int,input().split()))
i=0
x=0
for j in l:
    x=x+j+i
    if(j>1):
        i=i+1
print(x)
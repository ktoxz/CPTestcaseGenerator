n=int(input())
cnt=0
while n>=7 and (n%4!=0):
    n-=7
    cnt+=1
if(n%4==0):
    print("4"*(n//4)+"7"*cnt)
else:
    print(-1)
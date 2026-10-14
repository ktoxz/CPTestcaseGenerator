n=int(input())
x=n//7
y=n-x*7
if y%4==0:
    ans="4"*(y//4)+"7"*x
    print(ans)
else:
    print(-1)
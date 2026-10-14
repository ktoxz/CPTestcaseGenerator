n=int(input())
count=0
t=n
f=0
while(n%4!=0):
    count+=1
    n-=7
    if n<0:
        f=1
        break
if f==1:
    if t%7==0:
        x=t/7
        s=""
        for i in range(int(x)):
            s+="7"
        print(int(s))        
    else:
        print(-1)

else:
    x=(t-count*7)/4
    s=""
    for i in range(int(x)):
        s=s+"4"
    for i in range(count):
        s=s+"7"
    print(int(s))
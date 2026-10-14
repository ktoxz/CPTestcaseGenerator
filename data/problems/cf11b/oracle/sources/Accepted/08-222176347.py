import sys
input=sys.stdin.readline
def inp():
    return int(input())
def st():
    return input().rstrip('\n')
def lis():
    return list(map(int,input().split()))
def ma():
    return map(int,input().split())
t=1
while(t):
    t-=1
    n=inp()
    n=abs(n+0)
    cur=1
    mo=0
    x=0
    while(1):
        if((x+cur)<n):
            cur+=1
            mo+=1
            x+=cur-1
        else:
            cur+=1
            mo+=1
            x+=cur-1
            break
    if((x-n)%2):
        x+=cur
        if((x-n)%2==0):
            mo+=1
        else:
            mo+=2
    if(n==0):
        mo=0
    print(mo)
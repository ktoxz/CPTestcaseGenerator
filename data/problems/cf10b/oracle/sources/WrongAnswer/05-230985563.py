from collections import *
from math import ceil, gcd,inf
from functools import *
import sys
input = lambda: sys.stdin.readline().rstrip()  # faster!
def fun(m,x2,ll,rr):
    return sum([abs(m-x2)+abs(m-c) for c in range(ll,rr+1)])

n,k=map(int,input().split())
*arr,=map(int,input().split())
emp=[[0,k+1] for _ in range(k+1)] #l-r有人坐
midi=k//2+1
travel_order=[midi]
for i in range(1,midi):travel_order.append(midi-i);travel_order.append(midi+i)
for peos in arr:
    dist=inf;ans=(-1,)
    for row in travel_order:
        a,b=emp[row];l,r=0,k+1
        if not a:
            if peos%2==0:
                l=midi-peos//2;r=k+1-l-1
            else: 
                l=midi-peos//2;r=k+1-l
            tans=(row,l,r)       
        elif a<k+1-b:
            l=a;r=b+peos
            tans=(row,b+1,r)
        else:
            l=a-peos;r=b
            tans=(row,l,a-1)       
        if 0<l and r<k+1:
            tem=fun(midi,*tans)
            if dist>tem: 
                dist=tem;ans=tans 
                ansl,ansr=l,r 
    if ans !=(-1,) : emp[ans[0]]=[ansl,ansr];             
    print(*ans) ;


# print(emp)
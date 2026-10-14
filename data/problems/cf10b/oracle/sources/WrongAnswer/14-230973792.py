from collections import *
# from math import ceil, gcd,inf
from functools import *
import sys
input = lambda: sys.stdin.readline().rstrip()  # faster!


n,k=map(int,input().split())
*arr,=map(int,input().split())
emp=[[0,k+1] for _ in range(k+1)] #l-r有人坐
midi=k//2+1
travel_order=[midi]
for i in range(1,midi):travel_order.append(midi-i);travel_order.append(midi+i)
for peos in arr:
    f=1
    for row in travel_order:
        a,b=emp[row];l,r=0,k+1
        if not a:
            if peos%2==0:
                l=midi-peos//2;r=k+1-l-1
            else: 
                l=midi-peos//2;r=k+1-l
            ans=(row,l,r)       
        elif a<k+1-b:
            l=a;r+=peos
            ans=(row,b+1,r)
        else:
            l=a-peos;r=b
            ans=(row,l,a-1)       
        if 0<l and r<k+1:
            emp[row]=[l,r]
            print(*ans) ;f=0;break;   
    if f:print(-1)    


# print(emp,travel_order)
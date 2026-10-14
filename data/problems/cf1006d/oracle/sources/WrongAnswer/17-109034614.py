from sys import stdin,stdout
from math import gcd,sqrt,factorial,pi,inf
from collections import deque,defaultdict
from bisect import bisect,bisect_left
from itertools import permutations as per
input=stdin.readline
R=lambda:map(int,input().split())
I=lambda:int(input())
S=lambda:input().rstrip('\n')
L=lambda:list(R())
P=lambda x:stdout.write(str(x)+'\n')
nCr=lambda x,y:(f[x]*inv((f[y]*f[x-y])%N))%N

n=I()
x=S()
y=S()
ans=0
for i in range(n//2):
	a=x[i]
	b=x[-i-1]
	c=y[i]
	d=y[-i-1]
	if a==b==c==d or a==b!=c==d or a==c!=b==d or a==d!=c==b:continue
	elif c!=a==b!=d!=c or a!=c==d!=b!=a or len(set([a,b,c,d]))==4:ans+=2
	else:ans+=1
print(ans+(1 if n%2 and x[n//2]!=y[n//2] else 0))
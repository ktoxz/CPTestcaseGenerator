from math import *
k=int(input())
l=int(input())

x=log(l,k)

if(ceil(x)==floor(x)):
  print("YES")
else:
  print("NO")
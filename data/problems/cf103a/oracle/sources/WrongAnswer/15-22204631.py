import operator as op
from functools import reduce
input()
def ncr(n, r):
    r = min(r, n-r)
    if r == 0: return 1
    numer = reduce(op.mul, range(n, n-r, -1))
    denom = reduce(op.mul, range(1, r+1))
    return numer//denom
s=0
for x,i in enumerate(input().split()):
    s+=ncr(int(i)+x,x+1)
print(s)
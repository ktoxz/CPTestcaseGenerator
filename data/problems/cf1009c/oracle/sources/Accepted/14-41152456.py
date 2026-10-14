from array import array
from sys import stdin
import bisect
from bisect import *
import itertools
from itertools import *

def scan_gen():
    for line in stdin: yield from iter(line.split())
scan = scan_gen()
def nint(): return int(next(scan))
def nintk(k): return tuple(nint() for _ in range(k))
def nfloat(): return float(next(scan))
def intar_init(size): return array('i',[0]) *size
def intar(size=None):
    if size == None: size = nint()
    arr = intar_init(size) 
    for x in range(size): arr[x]=nint()
    return arr


def solve():
    n,m =nintk(2)
    sm = 0
    r1=0
    r2=0
    for i in range(n):
        r1 += i
        r2 += abs(i-n//2)
    for _ in range(m):
        x,d = nintk(2)
        sm += x*n
        if d>0:
            sm += d *r1
        else:
            sm += d*r2
    print(sm /n)

solve()
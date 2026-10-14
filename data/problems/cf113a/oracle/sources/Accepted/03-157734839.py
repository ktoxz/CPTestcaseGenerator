import sys,os,math,cmath,timeit,functools,operator,bisect
from sys import stdin,stdout,setrecursionlimit
from io import BytesIO, IOBase
from collections import defaultdict as dd , Counter
from math import factorial , gcd
from queue import PriorityQueue
from heapq import merge, heapify, heappop, heappush
try :
    from functools import cache , lru_cache
except :
    pass

ONLINE_JUDGE = __debug__

class FastIO(IOBase):
    newlines = 0

    def __init__(self, file):
        import os
        self.os = os
        self._fd = file.fileno()
        self.buffer = BytesIO()
        self.writable = "x" in file.mode or "r" not in file.mode
        self.write = self.buffer.write if self.writable else None
        self.BUFSIZE = 8192

    def read(self):
        while True:
            a = self.os.read(self._fd, max(self.os.fstat(self._fd).st_size, self.BUFSIZE))
            if not a:
                break
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(a), self.buffer.seek(ptr)
        self.newlines = 0
        return self.buffer.read()

    def readline(self):
        while self.newlines == 0:
            a = self.os.read(self._fd, max(self.os.fstat(self._fd).st_size, self.BUFSIZE))
            self.newlines = a.count(b"\n") + (not a)
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(a), self.buffer.seek(ptr)
        self.newlines -= 1
        return self.buffer.readline()

    def flush(self):
        if self.writable:
            self.os.write(self._fd, self.buffer.getvalue())
            self.buffer.truncate(0), self.buffer.seek(0)


class IOWrapper(IOBase):
    def __init__(self, file):
        self.buffer = FastIO(file)
        self.flush = self.buffer.flush
        self.writable = self.buffer.writable
        self.write = lambda s: self.buffer.write(s.encode("ascii"))
        self.read = lambda: self.buffer.read().decode("ascii")
        self.readline = lambda: self.buffer.readline().decode("ascii")

stdin, stdout = IOWrapper(stdin), IOWrapper(stdout)

input = lambda: stdin.readline().rstrip("\r\n")

start = timeit.default_timer()

primes = []
mod=10**9+7
MOD=998244353

########################################################

class DSU:
    def __init__(self,n):
        self.par = [i for i in range(n+1)]
        self.rank = [1 for i in range(n+1)]
        self.sz = [1 for i in range(n+1)]
    def find(self,x):
        if self.par[x]!=x :
            self.par[x] = self.find(self.par[x])
        return self.par[x]
    def union(self,x,y):
        rx,ry = self.find(x),self.find(y)
        if rx==ry :
            return False
        if self.rank[rx] > self.rank[ry] :
            self.sz[rx]+=self.sz[ry]
            self.par[ry]=rx
        elif self.rank[ry] > self.rank[rx] :
            self.sz[ry]+=self.sz[rx]
            self.par[rx]=ry
        else :
            self.rank[rx]+=1
            self.par[ry]=rx
            self.sz[rx]+=self.sz[ry]
        return True
    def connected(self,x,y):
        return self.find(x)==self.find(y)

def countinversions(a,ans):
    if(len(a)==1) : return a
    mid = len(a)//2
    x = a[:mid]
    y = a[mid:]
    left = countinversions(x,ans)
    right = countinversions(y,ans)
    temp = []
    i,j=0,0
    while i<len(left) and j<len(right):
        if left[i]<=right[j] :
            temp.append(left[i])
            i+=1
        else :
            temp.append(right[j])
            j+=1
            ans+=len(left)-i
    while i<len(left) : temp.append(right[i]) ; i+=1
    while j<len(right) : temp.append(left[j]) ; j+=1
    return temp

########################################################

def seive(n):
    a = []
    prime = [True for i in range(n+1)] 
    p = 2
    while (p * p <= n): 
        if (prime[p] == True): 
            for i in range(p ** 2,n + 1, p): 
                prime[i] = False
        p = p + 1
    for p in range(2,n + 1): 
        if prime[p]: 
            primes.append(p)

def lower_bound(arr, n, k):
    start = 0
    end = n-1
    while start <= end:
        mid = (start+end)//2
        if arr[mid] == k:
            return mid
        elif arr[mid] > k:
            if mid > 0:
                if arr[mid-1] < k:
                    return (mid-1)
            else:
                return -1
        else:
            if mid < (n-1):
                if arr[mid+1] > k:
                    return mid
            else:
                return mid

def upper_bound(arr, n, k):
    start = 0
    end = n-1
    while start <= end:
        mid = (start+end)//2
        if arr[mid] == k:
            return mid
        elif arr[mid] > k:
            if mid > 0:
                if arr[mid-1] < k:
                    return (mid)
            else:
                return mid
        else:
            if mid < (n-1):
                if arr[mid+1] > k:
                    return (mid+1)
            else:
                return -1

def is_sorted(arr):
    return all(arr[i]<=arr[i+1] for i in range(len(arr)-1))

def invmod(n):
    return pow(n,mod-2,mod)

def binary_search(a,x,lo=0,hi=None):
    if hi is None:
        hi = len(a)
    while lo < hi:
        mid = (lo+hi)//2
        midval = a[mid]
        if midval < x:
            lo = mid+1
        elif midval > x: 
            hi = mid
        else:
            return mid
    return -1

def ceil(a:int,b:int)->int :
    return (a+b-1)//b

def yn(x):
    if x :
        print("YES")
    else :
        print("NO")

def nCr(n,r):
    return factorial(n)//(factorial(r)*factorial(n-r))

def countinversions(arr):
    if len(arr)==1 :
        return arr,0
    left = arr[:len(arr)//2]
    right = arr[len(arr)//2:]
    left,lc = countinversions(left)
    right,rc = countinversions(right)
    c = []
    i,j,ans = 0,0,lc+rc
    while i<len(left) and j<len(right):
        if left[i] <= right[j] :
            c.append(left[i])
            i+=1
        else :
            c.append(right[j])
            ans+=len(left)-i
            j+=1
    c+=left[i:]
    c+=right[j:]
    return c,ans

########################################################

def solve():
    s=input().split()
    a=''
    tt=[]
    for x in s :
        if x[-4:]=="lios" :
            tt+=['m']
            a+='a'
        elif x[-5:]=="liala" :
            tt+=['f']
            a+='a'
        elif x[-3:]=="etr" :
            tt+=['m']
            a+='n'
        elif x[-4:]=="etra" :
            tt+=['f']
            a+='n'
        elif x[-6:]=="initis" :
            tt+=['m']
            a+='v'
        elif x[-6:]=="inites" :
            tt+=['f']
            a+='v'
        else :
            print("NO")
            return 
    if len(tt)==1 :
        print("YES")
        return
    if len(set(tt))==2 or a.count('n')!=1 :
        print("NO")
        return
    noun = a.index('n')
    temp = a.split('n')
    adj=-1 
    fl=0
    verb=len(a)+1
    for i in range(len(a)):
        if a[i]=='a' :
            adj=i
        if a[i]=='v' :
            if fl==0 :
                fl=1
                verb=i
    if noun > adj and noun < verb :
        print("YES")
        return
    print("NO")

def main():
    tc=1
    #tc=int(input())
    for _ in range(tc):
        solve()
    stop = timeit.default_timer()
    if not ONLINE_JUDGE :
        print("Time Elapsed :" , str(stop-start) , "seconds")

########################################################

def lst()->list :
    return list(map(int,input().split()))

def rowinp() :
    return map(int,input().split())

def strin()->str :
    return input()

def chlst()->list :
    return [x for x in input()]

def sint()->int :
    return int(input())

########################################################

main()

########################################################